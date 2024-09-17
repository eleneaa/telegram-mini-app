# telegram-mini-app
telegram mini app for the study of animal anatomy

# Запуск проекта
1. docker compose build
2. docker compose up -d
3. Настроить виртуальное окружение (venv)
4. pip install -r requirements.txt
5. Перейти в рабочую папку (cd django/anatomy_main)
6. Ввести команды для применения миграций в postgres: python manage.py migrate
7. Ввести команду python manage.py createsuperuser для создания пользователя, под которым будете в админку входить
8. Запустить приложение через команду: python manage.py runserver :)
