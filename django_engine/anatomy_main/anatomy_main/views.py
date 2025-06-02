import hashlib
import hmac
import json
import os
import time
import urllib.parse

import requests
from articles.models import Article
from atlases.models import Atlas
from categories.models import Catalog
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from tests.models import Test
from users.models import *
from users.models import User
from anatomy_main.utils import get_current_category

# Дада снова токен в коде
# )))))))))))))
bot_token = os.getenv('BOT_TOKEN', '7887662113:AAH4eB61DIivFoXCYV3vivRk9-7iBDvjEKU')
imgur_client_id = os.getenv('IMGUR_CLIENT_ID', '3dd1847a2c4f6e0')


# Функция для получения фотографии профиля пользователя
def get_user_profile_picture(user):
    user_id = user.telegram_id
    try:
        # Получаем фотографии профиля пользователя через API Telegram
        url = f'https://api.telegram.org/bot{bot_token}/getUserProfilePhotos?user_id={user_id}'
        response = requests.get(url)

        # Проверяем, что запрос прошел успешно
        if response.status_code == 200:
            data = response.json()

            # Проверяем, есть ли фотографии
            if data['result']['total_count'] > 0:
                # Получаем ID первого фото
                file_id = data['result']['photos'][0][0]['file_id']
                if user.last_telegram_photo_file_id == file_id:
                    return None

                # Получаем информацию о файле
                file_url = f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}'
                file_response = requests.get(file_url)

                if file_response.status_code == 200:
                    file_data = file_response.json()
                    file_path = file_data['result']['file_path']
                    file_download_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'

                    # Загружаем файл с Telegram
                    file_content = requests.get(file_download_url).content

                    # Отправляем файл на Imgur
                    headers = {'Authorization': f'Client-ID {imgur_client_id}'}
                    imgur_response = requests.post(
                        url='https://api.imgur.com/3/upload',
                        headers=headers,
                        files={'image': file_content}
                    )

                    if imgur_response.status_code == 200:
                        imgur_data = imgur_response.json()
                        return {'link': imgur_data['data']['link'], 'file_id': file_id}
                    else:
                        print("Ошибка при загрузке на Imgur:", imgur_response.json())
                        return None
                else:
                    print("Ошибка при получении файла.")
                    return None
            else:
                print("У пользователя нет фотографий.")
                return None
        else:
            print(f"Ошибка при запросе данных: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None


# Функция для проверки подписи Telegram
def verify_telegram_signature(init_data, bot_token):
    parsed_data = dict(urllib.parse.parse_qsl(init_data))
    check_hash = parsed_data.pop('hash', None)

    data_check_string = "\n".join([f"{key}={value}" for key, value in sorted(parsed_data.items())])
    secret_key = hmac.new(b"WebAppData", bot_token.encode('utf-8'), hashlib.sha256).digest()

    calculated_hash = hmac.new(secret_key, data_check_string.encode('utf-8'), hashlib.sha256).hexdigest()

    return check_hash == calculated_hash, parsed_data


# Функция для сохранения или обновления данных пользователя
def save_or_update_user(parsed_data):
    user_data = json.loads(parsed_data.get('user', '{}'))
    telegram_id = user_data.get('id')
    first_name = user_data.get('first_name', '')
    last_name = user_data.get('last_name', '')
    telegram_username = user_data.get('username', '')
    username = f"tg_{telegram_id}"

    if telegram_id:
        user, created = User.objects.get_or_create(telegram_id=telegram_id, defaults={
            'username': username,
            'telegram_username': telegram_username,
            'telegram_id': telegram_id,
            'first_name': first_name,
            'last_name': last_name,
        })

        if not created:
            # Обновляем данные пользователя, если они изменились
            if user.first_name != first_name or user.last_name != last_name or user.telegram_username != telegram_username or user.username != username:
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.telegram_username = telegram_username
        telegram_photo_data = get_user_profile_picture(user)
        if telegram_photo_data:
            user.telegram_photo_url = telegram_photo_data['link']
            user.last_telegram_photo_file_id = telegram_photo_data['file_id']
        user.save()
        return user
    return None


def build_url_from_start_param(start_param):
    try:
        if '_' in start_param:
            resource_type, resource_id = start_param.split('_', 1)
            if resource_type == 'article':
                return reverse('open_article', args=[resource_id])
            elif resource_type == 'test':
                return reverse('tests:open_test', args=[resource_id])
            elif resource_type == 'atlas':
                return reverse('atlases:open_atlas', args=[resource_id])
            elif resource_type == 'category':
                return reverse('categories:open_catalog', args=[resource_id])
            elif resource_type == 'note':
                return reverse('delete_note', args=[resource_id])
        else:
            if start_param == 'profile':
                return reverse('users:profile')
            elif start_param == 'favorites':
                return reverse('favorites')
            elif start_param == 'notes':
                return reverse('notes')
            elif start_param == 'popular_tests':
                return reverse('tests:list_popular_tests')
            elif start_param == 'popular_articles':
                return reverse('popular_articles')
            elif start_param == 'popular_atlases':
                return reverse('atlases:popular_atlases')
        return None
    except Exception as e:
        print(f"Error building URL from start_param: {e}")
        return None


# Основная view для обработки данных
def main(request):
    # Получаем данные пользователя из GET-запроса
    init_data = request.GET.get('user_data')

    category = get_current_category(request)

    popular_tests = Test.get_popular(count=6, current_category=category)
    popular_atlases = Atlas.get_popular(count=6, current_category=category)
    popular_articles = Article.get_popular(count=6, current_category=category)
    if not init_data and request.user.is_authenticated:
        return render(request, 'main.html', context={'user': request.user,
                                                     'popular_tests': popular_tests,
                                                     'popular_atlases': popular_atlases,
                                                     'popular_articles': popular_articles,
                                                     'category': category})

    if init_data:
        # Проверяем подпись Telegram
        is_valid, parsed_data = verify_telegram_signature(init_data, bot_token)
        if is_valid:
            # Проверяем дату авторизации, чтобы данные не устарели
            auth_date = int(parsed_data.get('auth_date', 0))
            if time.time() - auth_date > 5 * 60:  # Данные не старше 5 минут
                return JsonResponse({'status': 'error', 'message': 'Data is outdated'}, status=403)

            # Сохраняем или обновляем пользователя
            user = save_or_update_user(parsed_data)
            start_params = parsed_data.get('start_param', None)

            if user:
                login(user=user, request=request)
                if start_params:
                    redirect_url = build_url_from_start_param(start_params)
                    if redirect_url:
                        return redirect(redirect_url)

                return render(request, 'main.html', context={'user': request.user,
                                                             'popular_tests': popular_tests,
                                                             'popular_atlases': popular_atlases,
                                                             'popular_articles': popular_articles})
        return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=403)

    return JsonResponse({'status': 'error', 'message': 'No user data provided'}, status=400)


# Вспомогательная view для редиректа на main
def init_page(request):
    return render(request, 'index_auth_redirect.html', context={'auth_url': reverse('main')})


def test(request):
    return render(request, 'test.html', context={'user': request.user})


def notes(request):
    return render(request, 'notes.html', context=request.user.get_notes())


def delete_note(request, object_id):
    object_ = None
    if TestUserRel.objects.filter(test_id=object_id).exists():
        print('test')
        object_ = TestUserRel.objects.get(test_id=object_id)
    elif AtlasUserRel.objects.filter(atlas_id=object_id).exists():
        print('atlas')
        object_ = AtlasUserRel.objects.get(atlas_id=object_id)
    elif ArticleUserRel.objects.filter(article_id=object_id).exists():
        print('article')
        object_ = ArticleUserRel.objects.get(article_id=object_id)
    print(object_)
    if object_:
        object_.note = ""
        object_.save()

    return redirect("notes")


def favorites(request):
    return render(request, 'favorites.html', context={"tests": Test.get_favorite_tests(request.user),
                                                      'atlases': Atlas.get_favorite_atlases(request.user),
                                                      'articles': Article.get_favorite_articles(request.user)})
