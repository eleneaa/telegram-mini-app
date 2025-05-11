# Create your views here.
# views.py
import base64
import random
import uuid
from datetime import timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context, Template
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from anatomy_main import utils
from users.models import QuestionUserRel, TestUserRel
from .models import Test, Question, QuestionType


def generate_random_test(request: HttpRequest,
                         num_questions: int):
    question_ids = list(Question.objects.values_list('id', flat=True))
    selected_ids = random.sample(question_ids, min(len(question_ids), num_questions))

    test = Test.objects.create(
        label=f'Случайный тест на {min(len(question_ids), num_questions)} вопросов',
    )
    test.questions_list.add(*selected_ids)
    test.save()
    return redirect('tests:start_test', test_id=test.id)


def encode_uuid_to_code(u):
    return base64.urlsafe_b64encode(u.encode('utf-8')).rstrip(b'=').decode('ascii')  # ~22 символа


def decode_code_to_uuid(code):
    padded = code + '=' * (-len(code) % 4)
    return base64.urlsafe_b64decode(padded).decode("utf-8")


def generate_word_by_test(request: HttpRequest, test_id: str):
    return JsonResponse({
        "code": encode_uuid_to_code(test_id)
    })


def run_test_by_code(request: HttpRequest, code: str):
    test_id = decode_code_to_uuid(code)
    return redirect('tests:start_test', test_id=test_id)


def start_test(request, test_id):
    try:
        test = Test.objects.prefetch_related('questions_list').get(id=test_id)
    except ObjectDoesNotExist:
        raise Http404
    test.questions_list.prefetch_related('variants')
    request.session['test'] = {
        'id': test.id,
        'label': test.label,
        'question_count': len(test.questions_list.all()),
        'time_stop': (timedelta(seconds=test.time_limit) + timezone.now()).isoformat() if test.time_limit else None
    }

    questions: list[Question] = list(test.questions_list.all())
    request.session['questions'] = [
        {
            'id': q.id,
            'question_type': q.question_type,
            'label': q.label,
            'points': q.points,
            'variants': [
                {
                    'id': v.id,
                    'text': v.name
                } for v in q.variants.all()
            ]
        }
        for q in questions]

    question_user_rels = QuestionUserRel.objects.filter(user_id=request.user.pk,
                                                        question__in=questions).all()

    request.session['question_user_rels'] = dict(map(lambda q: (q.question_id, {
        'id': q.id,
        'is_favorite': q.is_favorite,
        'note': q.note
    }), question_user_rels))

    return redirect('tests:question_detail', test_id=test_id, question_id=0, permanent=False)


def question_detail(request, test_id, question_id):
    if (any(key not in request.session for key in ['test', 'questions', 'question_user_rels']) or
            question_id >= len(request.session["questions"]) or
            question_id < 0 or
            request.session['test']['id'] != test_id):
        return redirect('tests:start_test', test_id=test_id)

    test = request.session['test']

    try:
        question = request.session["questions"][question_id]
    except IndexError:
        return redirect('tests:test_results', test_id=test_id)

    if request.method == 'POST' and request.POST.getlist("answer[]") and request.POST.getlist("answer[]")[0] != '':
        answer = request.POST.getlist('answer[]')
        # Сохраняем ответ (можно добавить логику для сохранения ответов пользователя)
        request.session.setdefault('answers', {})[question['id']] = {"answers": answer,
                                                                     'question_type': question['question_type']}
        request.session.modified = True

        its_last_question = question_id + 1 >= len(request.session["questions"])

        if its_last_question:
            return redirect('tests:test_results', test_id=test_id)
        else:
            return redirect('tests:question_detail', test_id=test_id, question_id=question_id + 1)

    question_user_rels: dict[str, dict] = request.session['question_user_rels']
    question_user = question_user_rels.get(str(question_id), None)

    is_favorite = False
    if question_user:
        is_favorite = question_user['is_favorite']

    question_text = question['label']
    label_context = Context({
        'test': test,
        'question': question,
        'variants': question['variants'],
        'is_favorite': is_favorite,
        "question_type": question['question_type'],
        'question_index': question_id + 1,
        'all_questions_count': len(request.session["questions"]),
        'time_stop': test.get('time_stop'),
        'question_text': question_text
    })
    label_template = Template(question_text)
    question_text = label_template.render(label_context)

    return render(request, 'question.html',
                  {
                      'test': test,
                      'question': question,
                      'variants': question['variants'],
                      'is_favorite': is_favorite,
                      "question_type": question['question_type'],
                      'question_index': question_id + 1,
                      'all_questions_count': len(request.session["questions"]),
                      'time_stop': test.get('time_stop'),
                      'question_text': question_text
                  })


def test_results(request, test_id):
    if any(key not in request.session for key in ['test', 'questions', 'question_user_rels', 'answers']):
        return redirect('tests:start_test', test_id=test_id)

    test = get_object_or_404(Test, id=test_id)
    # Сохраняем запись, что тест завершен
    entity, created = TestUserRel.objects.get_or_create(test_id=test_id, user=request.user)
    entity.is_completed = True
    entity.last_try = timezone.now()
    entity.save()
    answers = request.session.get('answers', {})
    total_questions = len(answers)
    score = 0
    user_results = []
    for key, answer in answers.items():
        question_obj = Question.objects.get(id=key)
        user_answers = answer.get("answers")
        question_type = answer.get("question_type")
        if question_type == QuestionType.input_type:
            user_answers = user_answers[0].lower()
            correct_answers = list(map(lambda x: x.variant.name.lower(),
                                       question_obj.correct_answers()))
            ans_data = {
                "qid": key,
                "question": question_obj.label,
                "user_answers": user_answers,
                "correct_answers": correct_answers,
                "is_correct": False,
                'question_obj': question_obj
            }
            user_results.append(ans_data)
            if user_answers in correct_answers:
                score += question_obj.points
                ans_data['is_correct'] = True
        else:
            correct_ids = list(map(lambda x: x.variant_id, question_obj.correct_answers()))
            user_variants = ", ".join(
                map(lambda x: x.name, filter(lambda x: x.id in user_answers, question_obj.answers_ids())))
            correct_variants = list(
                map(lambda x: x.name, filter(lambda x: x.id in correct_ids, question_obj.answers_ids())))
            ans_data = {"qid": key,
                        "question": question_obj.label,
                        "user_answers": user_variants,
                        "correct_answers": correct_variants,
                        "is_correct": False,
                        'question_obj': question_obj}

            user_results.append(ans_data)
            if all(map(lambda x: x in correct_ids, user_answers)) and len(user_answers) == len(correct_ids):
                score += question_obj.points
                ans_data['is_correct'] = True
    questions_order = {q["id"]: i for i, q in enumerate(request.session['questions'])}
    questions_data = {q["id"]: q for q in request.session['questions']}
    user_results.sort(key=lambda x: questions_order[x["qid"]])
    for i, val in enumerate(user_results):
        val["question_number"] = i + 1
        val['question_data'] = questions_data[val['qid']]

    del request.session['questions']
    del request.session['answers']
    del request.session['question_user_rels']
    time_stop = request.session['test'].get('time_stop')
    del request.session['test']

    if time_stop is not None and timezone.now() > datetime.fromisoformat(time_stop):
        score = 0

    test_total_points = 0
    for question in test.questions_list.all():
        test_total_points += question.points

    return render(request,
                  'test_results.html',
                  {
                      'test': test,
                      'score': score,
                      'total_questions': total_questions,
                      "user_results": user_results,
                      "time_stop": time_stop,
                      "test_total_points": test_total_points
                  })


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
                                                      'atlases': test.get_atlases_by_categories(),
                                                      'articles': test.get_articles_by_categories(),
                                                      'note': note})


def open_atlases_by_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, "list_atlases_page.html", context={"atlases": test.get_atlases_by_categories()})


def open_articles_by_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, "list_articles_page.html", context={"articles": test.get_articles_by_categories()})


def main_page(request):
    popular_tests = Test.get_popular(10)
    favorite_tests = [test_id.test_id for test_id in request.user.favorite_tests_ids()]
    favorite_tests = Test.objects.filter(id__in=favorite_tests)
    return render(request, "test_main_page.html", context={"popular_tests": popular_tests,
                                                           "favorite_tests": favorite_tests})


def list_favorite_tests(request):
    return render(request, 'list_tests_page.html', context={"tests": Test.get_favorite_tests(request.user)})


def list_popular_tests(request):
    return render(request, 'list_tests_page.html', context={"tests": Test.get_popular()})


class TestsView(ListView):
    model = Test
    paginate_by = 8
    template_name = 'all_tests_page.html'

    context_object_name = 'tests'

    def get_queryset(self):
        return Test.objects.all()


def retry_last_test(request: HttpRequest):
    user_tests = TestUserRel.objects.filter(user=request.user)

    if len(user_tests) == 0:
        return redirect("tests:main")

    last_test = user_tests.latest('last_try')
    return redirect("tests:open_test", test_id=last_test.test_id)
