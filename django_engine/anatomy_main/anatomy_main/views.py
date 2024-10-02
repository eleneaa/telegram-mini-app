import hashlib
import hmac
import urllib.parse
import json
import time
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
# from django.contrib.auth import get_user_model

# User = get_user_model()


# Функция для проверки подписи Telegram
def verify_telegram_signature(init_data, bot_token):
    parsed_data = dict(urllib.parse.parse_qsl(init_data))
    check_hash = parsed_data.pop('hash', None)

    data_check_string = "\n".join([f"{key}={value}" for key, value in sorted(parsed_data.items())])
    secret_key = hmac.new(b"WebAppData", bot_token.encode('utf-8'), hashlib.sha256).digest()

    calculated_hash = hmac.new(secret_key, data_check_string.encode('utf-8'), hashlib.sha256).hexdigest()

    return check_hash == calculated_hash, parsed_data


# Функция для сохранения или обновления данных пользователя
# def save_or_update_user(parsed_data):
#     user_data = json.loads(parsed_data.get('user', '{}'))
#     telegram_id = user_data.get('id')
#     first_name = user_data.get('first_name', '')
#     last_name = user_data.get('last_name', '')
#     username = user_data.get('username', '')
#
#     if telegram_id:
#         user, created = User.objects.get_or_create(username=username, defaults={
#             'first_name': first_name,
#             'last_name': last_name,
#         })
#
#         if not created:
#             # Обновляем данные пользователя, если они изменились
#             if user.first_name != first_name or user.last_name != last_name:
#                 user.first_name = first_name
#                 user.last_name = last_name
#                 user.save()
#
#         return user
#     return None


# Основная view для обработки данных
def main(request):
    bot_token = "7887662113:AAH4eB61DIivFoXCYV3vivRk9-7iBDvjEKU"  # Замените на ваш реальный токен

    # Получаем данные пользователя из GET-запроса
    init_data = request.GET.get('user_data')

    if init_data:
        # Проверяем подпись Telegram
        is_valid, parsed_data = verify_telegram_signature(init_data, bot_token)
        if is_valid:
            # Проверяем дату авторизации, чтобы данные не устарели
            auth_date = int(parsed_data.get('auth_date', 0))
            if time.time() - auth_date > 5 * 60:  # Данные не старше 5 минут
                return JsonResponse({'status': 'error', 'message': 'Data is outdated'}, status=403)

            # Сохраняем или обновляем пользователя
            # user = save_or_update_user(parsed_data)
            user = True
            if user:
                return render(request, 'index.html', context={'user': user})

        return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=403)

    return JsonResponse({'status': 'error', 'message': 'No user data provided'}, status=400)


# Вспомогательная view для редиректа на main
def init_page(request):
    return render(request, 'index_auth_redirect.html', context={'auth_url': reverse('main')})
