# Create your views here.
# views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Test, Question, QuestionType
from anatomy_main import utils
from django.urls import reverse

from users.models import QuestionUserRel, TestUserRel


def start_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    first_question_id = test.questions_ids()[0].id
    return redirect('tests:question_detail', test_id=test_id, question_id=first_question_id)


def question_detail(request, test_id, question_id):
    test = get_object_or_404(Test, id=test_id)
    question = get_object_or_404(Question, id=question_id, test=test)
    question_user = QuestionUserRel.objects.filter(question_id=question_id, user_id=request.user.id)
    is_favorite = False
    if question_user:
        is_favorite = question_user[0].is_favorite

    if request.method == 'POST' and request.POST.getlist("answer[]"):
        answer = request.POST.getlist('answer[]')
        # Сохраняем ответ (можно добавить логику для сохранения ответов пользователя)
        request.session.setdefault('answers', {})[question.id] = {"answers": answer,
                                                                  'question_type': question.question_type}
        request.session.modified = True

        # Переходим к следующему вопросу или к результатам
        next_question = test.questions_list.filter(id__gt=question.id).first()
        if next_question:
            return redirect(reverse('tests:question_detail', kwargs={"test_id": test.id,
                                                                     "question_id": next_question.id}))
        else:
            return redirect(reverse('tests:test_results', kwargs={'test_id': test.id}))

    return render(request, 'question.html', {'test': test, 'question': question,
                                             'variants': question.variants.all(),
                                             "is_favorite": is_favorite,
                                             "question_type": question.question_type})


def test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    # Сохраняем запись, что тест завершен
    if test.id not in request.user.completed_tests_ids():
        entity, created = TestUserRel.objects.get_or_create(test_id=test_id, user_id=request.user.id)
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
    paginate_by = 5
    template_name = 'all_tests_page.html'

    context_object_name = 'tests'

    def get_queryset(self):
        return Test.objects.all()
