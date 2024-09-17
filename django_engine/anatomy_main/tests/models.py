import uuid

from django.db import models


# Create your models here.
class Variant(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(max_length=50, verbose_name='Описание вопроса')
    variants = models.ManyToManyField("Variant", verbose_name="Список ответов", symmetrical=False,
                                      related_name='variants')
    correct_variants = models.ManyToManyField("Variant", verbose_name="Список правильных ответов", symmetrical=False,
                                              related_name='correct_variants')

    def answers_ids(self):
        if self.variants.all():
            childs_array = [variant for variant in self.variants.all()]
            return childs_array

    def correct_answers_ids(self):
        if self.correct_variants.all():
            childs_array = [variant for variant in self.correct_variants.all()]
            return childs_array

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.label


class Test(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(max_length=50, verbose_name='Название теста')
    questions_list = models.ManyToManyField("Question", verbose_name='Список вопросов')
    catalogs = models.ManyToManyField("categories.Catalog", verbose_name="Принадлежит каталогам",
                                      related_name='tests', blank=True)

    def questions_ids(self):
        if self.questions_list.all():
            childs_array = [questions for questions in self.questions_list.all()]
            return childs_array

    def catalog_ids(self):
        if self.catalogs.all():
            childs_array = [catalog for catalog in self.catalogs.all()]
            return childs_array

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.label
