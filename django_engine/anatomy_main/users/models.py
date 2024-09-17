from django.contrib.auth.models import AbstractUser
from django.db import models


class TestUserRel(models.Model):
    test = models.ForeignKey('tests.Test', on_delete=models.CASCADE, related_name='test_user_id', verbose_name='Тест')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_test_id')
    is_completed = models.BooleanField(default=False, verbose_name='Тест пройден?')
    is_favorite = models.BooleanField(default=False, verbose_name='Тест в избранном?')

    class Meta:
        db_table = 'tests_user'
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return f'{self.test}'


class CatalogUserRel(models.Model):
    catalog = models.ForeignKey('categories.Catalog', on_delete=models.CASCADE,
                                related_name='cat_user_id', verbose_name='Каталог')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_cat_id')
    is_favorite = models.BooleanField(default=False, verbose_name='Каталог в избранном?')

    class Meta:
        db_table = 'catalog_user'
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    def __str__(self):
        return f'{self.catalog}'


class QuestionUserRel(models.Model):
    question = models.ForeignKey('tests.Question', on_delete=models.CASCADE, related_name="qu_user_id",
                                 verbose_name='Вопрос')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_qu_id')
    is_favorite = models.BooleanField(default=False, verbose_name='Вопрос в избранном?')

    class Meta:
        db_table = 'question_user'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.question}'


class ArticleUserRel(models.Model):
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, related_name="ar_user_id",
                                verbose_name='Статья')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_ar_id')
    is_favorite = models.BooleanField(default=False, verbose_name='Статья в избранном?')

    class Meta:
        db_table = 'articles_user'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.article}'


class User(AbstractUser):
    favorite_tests = models.ManyToManyField("tests.Test", verbose_name="Список избранных тестов", symmetrical=False,
                                            related_name='user_tests',
                                            through='TestUserRel')

    favorite_questions = models.ManyToManyField("tests.Question", verbose_name="Список избранных вопросов",
                                                symmetrical=False,
                                                related_name='user_questions',
                                                through='QuestionUserRel')

    favorites_articles = models.ManyToManyField("articles.Article", blank=True, symmetrical=False,
                                                related_name='articles',
                                                verbose_name="Список избранных статей",
                                                through='ArticleUserRel')

    favorites_catalogs = models.ManyToManyField("categories.Catalog", blank=True, symmetrical=False,
                                                related_name='catalogs',
                                                verbose_name="Список избранных тем",
                                                through='CatalogUserRel')

    def favorite_tests_ids(self):
        if self.favorite_tests.all():
            # print(TestUserRel.objects.filter(is_favorite=True, user_id=self.id)
            childs_array = [test for test in TestUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array

    def completed_tests_ids(self):
        if self.favorite_tests.all():
            childs_array = [test for test in TestUserRel.objects.filter(is_completed=True, user_id=self.id)]
            return childs_array

    def favorite_questions_ids(self):
        if self.favorite_questions.all():
            childs_array = [question for question in QuestionUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array

    def favorite_articles_ids(self):
        if self.favorites_articles.all():
            childs_array = [article for article in ArticleUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array

    def favorite_catalogs_ids(self):
        if self.favorites_catalogs.all():
            childs_array = [article for article in CatalogUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'auth_user'
