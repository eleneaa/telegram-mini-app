
from django.contrib import messages
from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect

from users.models import User
from tests.models import Test
from atlases.models import Atlas
from articles.models import Article

# from django_engine.anatomy_main.users.forms import AuthUserForm


def profile(request):
    user = request.user
    favorite_tests = user.favorite_tests_ids()
    completed_tests = Test.get_completed_tests(user, count=6)
    favorite_questions = user.favorite_questions_ids()
    favorite_articles = user.favorite_articles_ids()
    favorite_catalogs = user.favorite_catalogs_ids()
    favorite_atlases = user.favorite_atlases_ids()

    context = {
        'user': user,
        'favorite_tests': favorite_tests,
        'completed_tests': completed_tests,
        'favorite_questions': favorite_questions,
        'favorite_articles': favorite_articles,
        'favorite_catalogs': favorite_catalogs,
        'favorite_atlases': favorite_atlases,
    }
    return render(request, 'profile.html', context=context)


# def signin(request):
#     # Проверка, что пользователь зашел в акк
#     if request.user.is_authenticated:
#         return redirect('profile')
#
#     if request.method == "POST":
#         username = request.POST["username"]
#         pass1 = request.POST["password"]
#         user = authenticate(username=username, password=pass1)
#         if user is not None:
#             login(request, user)
#             return redirect("profile")
#
#         else:
#             messages.error(request, "Пользователя не существует")
#             return render(request, "avia_ticket_sales/login_page.html", context={"form": AuthUserForm})
#     return render(request, "avia_ticket_sales/login_page.html", context={"form": AuthUserForm})
