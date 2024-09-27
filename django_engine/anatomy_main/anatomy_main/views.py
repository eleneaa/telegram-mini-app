from django.shortcuts import render
from django.urls import reverse


def main(request):
    print(request.GET)
    return render(request, 'index.html')


def init_page(request):
    return render(request, 'index_auth_redirect.html', context={ 'auth_url': reverse('main') })