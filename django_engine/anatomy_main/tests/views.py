# Create your views here.
# views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Test, Question

from django.urls import reverse

from users.models import QuestionUserRel


def question_detail(request, test_id, question_id):
    test = get_object_or_404(Test, id=test_id)
    question = get_object_or_404(Question, id=question_id, test=test)
    question_user = QuestionUserRel.objects.filter(question_id=question_id, user_id=request.user.id)
    is_favorite = False
    if question_user:
        is_favorite = question_user[0].is_favorite

    if request.method == 'POST':
        if request.POST.getlist("answer[]"):
            answer = request.POST.getlist('answer[]')
            # Сохраняем ответ (можно добавить логику для сохранения ответов пользователя)
            request.session.setdefault('answers', {})[question.id] = answer
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
                                                      "is_favorite": is_favorite})


def test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    answers = request.session.get('answers', {})
    score = 0
    total_questions = test.questions_list.count()
    for question in test.questions_list.all():
        correct_ids = list(map(lambda x: x.variant_id, question.correct_answers()))
        if all(map(lambda x: x in correct_ids, answers[question.id])) and len(answers[question.id]) == len(correct_ids):
            print(score)
            score += 1

    return render(request, 'test_results.html', {'test': test, 'score': score, 'total_questions': total_questions})


@require_POST
def toggle_favorite(request, question_id):
    print(Question.objects.all())
    question = get_object_or_404(Question, id=question_id)
    favorite, created = QuestionUserRel.objects.get_or_create(user=request.user, question=question, is_favorite=True)
    if created:
        # Элемент был добавлен в избранное
        action = "added"
    else:
        # Элемент был удален из избранного
        favorite.delete()
        action = "removed"

    return JsonResponse({'action': action})
