import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.
class QuestionType(models.TextChoices):
    single_choice = 'radio', _("Один правильный ответ")
    multipy_choice = 'checkbox', _("Несколько правильных ответов")
    input_type = 'input', _("Ввод текста")


class QuestionVariantRel(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_id')
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE, related_name='variant_id', verbose_name='Вариант')
    is_correct = models.BooleanField(default=False, verbose_name='Является правильным?')

    class Meta:
        db_table = 'question_variants'
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return f'{self.variant}'


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
    variants = models.ManyToManyField("Variant", verbose_name="Список правильных ответов", symmetrical=False,
                                      related_name='correct_variants',
                                      through='QuestionVariantRel')
    question_type = models.CharField(choices=QuestionType.choices, verbose_name="Тип вопроса",
                                     default=QuestionType.multipy_choice, max_length=50)

    def answers_ids(self):
        if self.variants.all():
            childs_array = [variant for variant in self.variants.all()]
            return childs_array

    def correct_answers(self):
        if self.variants.all():
            correct_variants = QuestionVariantRel.objects.filter(question_id=self.id, is_correct=True)
            return [variant for variant in correct_variants]

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
        return []

    def catalog_ids(self):
        if self.catalogs.all():
            childs_array = [catalog for catalog in self.catalogs.all()]
            return childs_array
        return []

    def get_absolute_url(self):
        return reverse("tests:open_test", kwargs={"test_id": self.id})

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.label
