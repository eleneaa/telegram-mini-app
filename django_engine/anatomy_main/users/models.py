from django.contrib.auth.models import AbstractUser
from django.db import models


class TestUserRel(models.Model):
    test = models.ForeignKey('tests.Test', on_delete=models.CASCADE, related_name='test_user_id', verbose_name='Тест')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_test_id')
    is_completed = models.BooleanField(default=False, verbose_name='Тест пройден?')
    is_favorite = models.BooleanField(default=False, verbose_name='Тест в избранном?')
    note = models.CharField(default='', blank=True, verbose_name='Заметка к тесту', max_length=150)

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


class AtlasUserRel(models.Model):
    atlas = models.ForeignKey('atlases.Atlas', on_delete=models.CASCADE, related_name='atlas_user_id',
                              verbose_name='Атлас')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_atlas_id')
    is_favorite = models.BooleanField(default=False, verbose_name='Атлас в избранном?')
    note = models.CharField(default='', blank=True, verbose_name='Заметка к атласу', max_length=150)

    class Meta:
        db_table = 'atlas_user'
        verbose_name = 'Атлас'
        verbose_name_plural = 'Атласы'

    def __str__(self):
        return f'{self.atlas}'


class QuestionUserRel(models.Model):
    question = models.ForeignKey('tests.Question', on_delete=models.CASCADE, related_name="qu_user_id",
                                 verbose_name='Вопрос')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_qu_id')
    is_favorite = models.BooleanField(default=False, verbose_name='Вопрос в избранном?')
    note = models.CharField(default='', blank=True, verbose_name='Заметка к вопросу', max_length=150)

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
    note = models.CharField(default='', blank=True, verbose_name='Заметка к статье', max_length=150)

    class Meta:
        db_table = 'articles_user'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.article}'


class User(AbstractUser):
    # last_user_data = models.CharField(default='', blank=True, verbose_name='Последняя юзер дата', max_length=None)
    telegram_id = models.BigIntegerField(default=0, blank=False, verbose_name='Telegram ID', unique=True, primary_key=True)
    # first_name = models.CharField(default='', blank=True, verbose_name='Имя пользователя', max_length=65)
    # last_name = models.CharField(default='', blank=True, verbose_name='Фамилия пользователя', max_length=65)
    telegram_username = models.CharField(default='', blank=True, null=True, verbose_name='Username пользователя', max_length=33)

    # # Theme settings for Telegram Mini App (default to light theme)
    # background_color = models.CharField(default='#ffffff', blank=True, verbose_name='Цвет фона',
    #                                     max_length=7)  # Белый фон
    # text_color = models.CharField(default='#000000', blank=True, verbose_name='Цвет текста',
    #                               max_length=7)  # Черный текст
    # button_color = models.CharField(default='#0088cc', blank=True, verbose_name='Цвет кнопки',
    #                                 max_length=7)  # Синий (как в Telegram)
    # button_text_color = models.CharField(default='#ffffff', blank=True, verbose_name='Цвет текста на кнопке',
    #                                      max_length=7)  # Белый текст на кнопке
    # navbar_background = models.CharField(default='#ffffff', blank=True, verbose_name='Цвет фона навбара',
    #                                      max_length=7)  # Белый навбар
    # navbar_text = models.CharField(default='#000000', blank=True, verbose_name='Цвет текста навбара',
    #                                max_length=7)  # Черный текст в навбаре
    # navbar_link = models.CharField(default='#0088cc', blank=True, verbose_name='Цвет ссылки навбара',
    #                                max_length=7)  # Ссылки того же цвета, что и кнопки
    # navbar_link_hover = models.CharField(default='#005f8c', blank=True, verbose_name='Цвет ссылки при наведении',
    #                                      max_length=7)  # Более темный синий при наведении

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

    favorites_atlases = models.ManyToManyField("atlases.Atlas", blank=True, symmetrical=False,
                                               related_name='atlases',
                                               verbose_name="Список избранных атласов",
                                               through='AtlasUserRel')

    def favorite_tests_ids(self):
        if self.favorite_tests.all():
            childs_array = [test for test in TestUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array
        return []

    def completed_tests_ids(self):
        if self.favorite_tests.all():
            childs_array = [test for test in TestUserRel.objects.filter(is_completed=True, user_id=self.id)]
            return childs_array
        return []

    def favorite_questions_ids(self):
        if self.favorite_questions.all():
            childs_array = [question for question in QuestionUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array
        return []

    def favorite_articles_ids(self):
        if self.favorites_articles.all():
            childs_array = [article for article in ArticleUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array
        return []

    def favorite_catalogs_ids(self):
        if self.favorites_catalogs.all():
            childs_array = [article for article in CatalogUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array
        return []

    def favorite_atlases_ids(self):
        if self.favorites_atlases.all():
            childs_array = [atlas for atlas in AtlasUserRel.objects.filter(is_favorite=True, user_id=self.id)]
            return childs_array
        return []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'auth_user'
