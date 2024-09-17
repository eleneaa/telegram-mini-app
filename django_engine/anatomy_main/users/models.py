from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    favorites_tests = models.ManyToManyField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'auth_user'