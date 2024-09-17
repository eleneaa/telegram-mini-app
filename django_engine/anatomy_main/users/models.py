from django.contrib.auth.models import AbstractUser
from django.db import models


class TestUserRel(models.Model):
    test = models.ForeignKey('tests.Test', on_delete=models.CASCADE, related_name='test_id', verbose_name='Тест')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_id')
    is_completed = models.BooleanField(default=False, verbose_name='Тест пройден?')
    is_favorite = models.BooleanField(default=False, verbose_name='Тест в избранном?')

    class Meta:
        db_table = 'tests_user'
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return f'{self.test}'


class User(AbstractUser):

    telegram_username = models.CharField(max_length=100, blank=True)

    favorite_tests = models.ManyToManyField("tests.Test", verbose_name="Список избранных тестов", symmetrical=False,
                                            related_name='user_tests',
                                            through='TestUserRel')

    favorites_questions = models.ManyToManyField("tests.Question", blank=True, symmetrical=False,
                                                 related_name='question',
                                                 verbose_name="Список избранных вопросов")

    favorites_articles = models.ManyToManyField("articles.Article", blank=True, symmetrical=False,
                                                related_name='articles',
                                                verbose_name="Список избранных статей")

    favorites_catalogs = models.ManyToManyField("categories.Catalog", blank=True, symmetrical=False,
                                                related_name='catalogs',
                                                verbose_name="Список избранных тем")

    def favorite_tests_ids(self):
        if self.favorite_tests.all():
            childs_array = [test for test in TestUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array

    def completed_tests_ids(self):
        if self.favorite_tests.all():
            childs_array = [test for test in TestUserRel.objects.filter(is_completed=True, user_id=self.id)]
            return childs_array

    def favorite_questions_ids(self):
        if self.favorites_questions.all():
            childs_array = [question for question in self.favorites_questions.all()]
            return childs_array

    def favorite_articles_ids(self):
        if self.favorites_articles.all():
            childs_array = [article for article in self.favorites_articles.all()]
            return childs_array

    def favorite_catalogs_ids(self):
        if self.favorites_catalogs.all():
            childs_array = [article for article in self.favorites_catalogs.all()]
            return childs_array

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'auth_user'
