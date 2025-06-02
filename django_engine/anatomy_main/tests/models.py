import uuid

from anatomy_main.models import BaseModel
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from users.models import TestUserRel


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
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(verbose_name='Описание вопроса', max_length=500)
    variants = models.ManyToManyField("Variant", verbose_name="Список правильных ответов", symmetrical=False,
                                      related_name='correct_variants',
                                      through='QuestionVariantRel')
    question_type = models.CharField(choices=QuestionType.choices, verbose_name="Тип вопроса",
                                     default=QuestionType.multipy_choice, max_length=200)

    points = models.IntegerField(default=1, verbose_name='Количество баллов за вопрос')

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


class Test(BaseModel):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(verbose_name='Название теста', max_length=200)
    questions_list = models.ManyToManyField("Question", verbose_name='Список вопросов')
    catalogs = models.ManyToManyField("categories.Catalog", verbose_name="Принадлежит каталогам",
                                      related_name='tests', blank=True)
    test_photo = models.ImageField(verbose_name='Фотография теста', upload_to='tests_storage', blank=True)
    time_limit = models.IntegerField(default=None, null=True, verbose_name='Время на ответ в секундах')

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

    @classmethod
    def get_favorite_tests(cls, user):
        return cls.objects.filter(
            id__in=TestUserRel.objects.filter(user=user, is_favorite=True).values('test_id')
        )

    @classmethod
    def get_completed_tests(cls, user,
                            count: int = None):
        res = cls.objects.filter(
            id__in=TestUserRel.objects.filter(user=user, is_completed=True).values('test_id')
        )
        if count:
            return res[:count]
        else:
            return res

    @classmethod
    def get_popular(cls,
                    count: int = None, current_category=None):
        if current_category:
            exp = f"""WITH tests_results AS (SELECT tests_test.* 
                                      FROM tests_test_catalogs 
                                      LEFT JOIN tests_test ON tests_test_catalogs.test_id = tests_test.id
                                      WHERE tests_test_catalogs.catalog_id = '{current_category.id}')
                                      SELECT tests_results.*
                                      FROM tests_results
            """
        else:
            exp = """SELECT tests_results.*
                     FROM tests_test AS tests_results
                  """
        res = cls.objects.raw(
            f"""
            {exp}
            left join (select tests_user.test_id,
                         count(tests_user.test_id) as fav_count
                  from tests_user
                  where tests_user.is_favorite
                  group by tests_user.test_id) as F on F.test_id = tests_results.id
            order by F.fav_count DESC 
            """
        )
        if count:
            return res[:count]
        else:
            return res

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.label
