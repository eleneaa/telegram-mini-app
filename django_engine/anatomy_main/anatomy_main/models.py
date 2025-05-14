from django.db import models


class BaseModel(models.Model):
    """ Базовый класс для Тестов, Атласов и Статей """

    class Meta:
        abstract = True

    def get_tests_by_categories(self):
        """ Получение списка тестов по категориям """
        tests = set()
        for catalog in self.catalogs.all():
            if catalog.tests_ids():
                tests.update(catalog.tests_ids())

        return tests

    def get_articles_by_categories(self):
        """ Получение списка статей по категориям """
        articles = set()
        for catalog in self.catalogs.all():
            if catalog.articles_ids():
                articles.update(catalog.articles_ids())

        return articles

    def get_atlases_by_categories(self):
        """ Получение списка атласов по категориям """
        articles = set()
        for catalog in self.catalogs.all():
            if catalog.atlases_ids():
                articles.update(catalog.atlases_ids())

        return articles
