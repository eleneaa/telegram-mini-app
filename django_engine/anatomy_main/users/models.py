from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    favorites_tests = models.ManyToManyField("tests.Test", blank=True, symmetrical=False,
                                             related_name='tests')
    favorites_catalogs = models.ManyToManyField("categories.Catalog", blank=True, symmetrical=False,
                                                related_name='catalogs')
    favorites_articles = models.ManyToManyField("articles.Article", blank=True, symmetrical=False,
                                                related_name='articles')
    favorites_questions = models.ManyToManyField("tests.Question", blank=True, symmetrical=False,
                                                 related_name='questions')
    finished_tests = models.ManyToManyField("tests.Test", blank=True, symmetrical=False,
                                            related_name='finished_tests')

    def questions_ids(self):
        if self.favorites_questions.all():
            childs_array = [question for question in self.favorites_questions.all()]
            return childs_array

    def catalog_ids(self):
        if self.favorites_catalogs.all():
            childs_array = [catalog for catalog in self.favorites_catalogs.all()]
            return childs_array

    def articles_ids(self):
        if self.favorites_articles.all():
            childs_array = [article for article in self.favorites_articles.all()]
            return childs_array

    def tests_ids(self):
        if self.favorites_tests.all():
            childs_array = [test for test in self.favorites_tests.all()]
            return childs_array

    def finished_tests_ids(self):
        if self.finished_tests.all():
            childs_array = [f_test for f_test in self.finished_tests.all()]
            return childs_array

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'auth_user'
