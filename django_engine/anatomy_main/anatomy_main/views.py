from django.shortcuts import render


def main(request, user_data):
    print(user_data)
    return render(request, 'index.html')
