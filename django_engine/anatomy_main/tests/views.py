# Create your views here.
# views.py
from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from anatomy_main import utils
from users.models import QuestionUserRel, TestUserRel
from .models import Test, Question, QuestionType


def start_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    # questions = test.questions_ids()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT "tests_question"."id",
       "tests_question"."label",
       "tests_question"."question_type",
       ARRAY_AGG("P0"."variant_name_and_id") AS "variants_list"
        FROM "tests_question"
                 INNER JOIN "tests_test_questions_list" ON ("tests_question"."id" = "tests_test_questions_list"."question_id")
                 LEFT OUTER JOIN "question_variants" ON ("tests_question"."id" = "question_variants"."question_id")
                 LEFT OUTER JOIN (SELECT "tests_variant"."id"                                  as id,
                                         "tests_variant"."name" || ' ' || "tests_variant"."id" as "variant_name_and_id"
                                  FROM "tests_variant") AS "P0"
                                 ON ("question_variants"."variant_id" = "P0"."id")
        WHERE "tests_test_questions_list"."test_id" = %s
        GROUP BY "tests_question".id
        """, [test_id]
        )
        questions = [
            dict(zip([col[0] for col in cursor.description], row))
            for row in cursor.fetchall()
        ]

    for question in questions:
        variants_list = []
        for i in question['variants_list']:
            name, _id = i.split(' ')
            variants_list.append({"name": name, "id": _id})
        question['variants_list'] = variants_list

    request.session["questions"] = list(questions)
    request.session['current_question'] = 0

    request.session['test'] = {'label': test.label, 'id': test.id}

    request.session['question_user_rels'] = list(QuestionUserRel
                                                 .objects
                                                 .filter(question_id__in=[question['id'] for question in questions],
                                                         user_id=request.user.telegram_id)
                                                 .all()
                                                 .values())

    first_question_id = questions[0]['id']
    return redirect('tests:question_detail', test_id=test_id, question_id=first_question_id)


def question_detail(request, test_id, question_index):
    test = get_object_or_404(Test, id=test_id)

    # определяем к какому вопросу относится запрос
    if request.method == "POST":
        current_question_index = int(request.POST.get('question_index'))
        request.session["current_question"] = current_question_index
    else:
        current_question_index = request.session["current_question"]

    try:
        question = request.session["questions"][current_question_index]
    except IndexError:
        print(f'Вопросы закончились Сессия: {request.session}')
        return redirect('tests:test_results', test_id=test_id)
    question_user_rels: list[dict] = request.session['question_user_rels']
    try:
        question_user = next(filter(lambda x: x['question_id'] == question_id, question_user_rels))
    except StopIteration:
        question_user = None
    is_favorite = False
    if question_user:
        is_favorite = question_user['is_favorite']

    if request.method == 'POST' and request.POST.getlist("answer[]") and request.POST.getlist("answer[]")[0] != '':
        answer = request.POST.getlist('answer[]')
        # Сохраняем ответ (можно добавить логику для сохранения ответов пользователя)
        request.session.setdefault('answers', {})[question['id']] = {"answers": answer,
                                                                     'question_type': question['question_type']}
        request.session.modified = True

        # Переходим к следующему вопросу или к результатам

        request.session['current_question'] += 1

        current_question = request.session['current_question']
        its_not_last_question = len(request.session["questions"]) > current_question

        if its_not_last_question:
            next_question = request.session["questions"][request.session['current_question']]
            return redirect(reverse('tests:question_detail', kwargs={"test_id": test.id,
                                                                     "question_id": next_question['id']}))
        else:
            return redirect(reverse('tests:test_results', kwargs={'test_id': test.id}))

    return render(request, 'question.html', {'test': test, 'question': question,
                                             'variants': question['variants_list'],
                                             "is_favorite": is_favorite,
                                             "question_type": question['question_type'],
                                             'question_index': current_question_index})


def test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    # Сохраняем запись, что тест завершен
    if test.id not in request.user.completed_tests_ids():
        entity, created = TestUserRel.objects.get_or_create(test_id=test_id, user_id=request.user.telegram_id)
        entity.is_completed = True
        entity.save()
    answers = request.session.get('answers', {})
    total_questions = len(answers)
    score = 0
    for key, answer in answers.items():
        question_obj = Question.objects.get(id=key)
        user_answers = answer.get("answers")
        question_type = answer.get("question_type")
        if question_type == QuestionType.input_type:
            user_answers = user_answers[0].lower()
            correct_answers = list(map(lambda x: x.variant.name.lower(), question_obj.correct_answers()))
            if user_answers in correct_answers:
                score += 1
        else:
            correct_ids = list(map(lambda x: x.variant_id, question_obj.correct_answers()))
            if all(map(lambda x: x in correct_ids, user_answers)) and len(user_answers) == len(correct_ids):
                score += 1

    return render(request, 'test_results.html', {'test': test, 'score': score, 'total_questions': total_questions})


@require_POST
def toggle_favorite(request, question_id):
    return utils.toggle_favorite(request,
                                 question_id,
                                 QuestionUserRel,
                                 "question_id")


@require_POST
def toggle_favorite_test(request, test_id):
    return utils.toggle_favorite(request,
                                 test_id,
                                 TestUserRel,
                                 "test_id")


@require_POST
def toggle_save_note_test(request, test_id, note_text=''):
    return utils.toggle_save_note(request, test_id, TestUserRel, 'test_id', note_text)


def open_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    try:
        rel_field = TestUserRel.objects.get(test=test, user=request.user)
    except TestUserRel.DoesNotExist:
        is_favorite = False
        note = ''
    else:
        is_favorite = rel_field.is_favorite
        note = rel_field.note
    return render(request, 'test_page.html', context={'test': test,
                                                      'is_favorite': is_favorite,
                                                      'note': note})


class TestsView(ListView):
    model = Test
    paginate_by = 8
    template_name = 'all_tests_page.html'

    context_object_name = 'tests'

    def get_queryset(self):
        return Test.objects.all()
