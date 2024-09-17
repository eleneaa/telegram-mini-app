
from django.contrib import messages
from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect

from django_engine.anatomy_main.users.forms import AuthUserForm



def signin(request):
    # Проверка, что пользователь зашел в акк
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["password"]
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect("profile")

        else:
            messages.error(request, "Пользователя не существует")
            return render(request, "avia_ticket_sales/login_page.html", context={"form": AuthUserForm})
    return render(request, "avia_ticket_sales/login_page.html", context={"form": AuthUserForm})
