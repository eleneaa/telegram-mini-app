import uuid

from django.db import models
from django.urls import reverse

from users.models import ArticleUserRel


# Create your models here.


class Article(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(max_length=200, verbose_name='Название файла')
    article_file = models.FileField(verbose_name='Файл статьи',
                                    upload_to='articles_storage',
                                    null=True,
                                    blank=True)
    catalogs = models.ManyToManyField("categories.Catalog", verbose_name="Принадлежит каталогам",
                                      related_name='articles', blank=True)
    article_photo = models.ImageField(verbose_name='Фотография статьи',
                                      upload_to='articles_storage',
                                      blank=True)
    pdf_file = models.FileField(verbose_name='PDF-файл статьи',
                                upload_to='articles_storage',
                                null=True,
                                default=None,
                                blank=True)

    def catalog_ids(self):
        if self.catalogs.all():
            catalogs_array = [catalog for catalog in self.catalogs.all()]
            return catalogs_array
        return []

    def get_absolute_url(self):
        return reverse("articles:open_article",
                       kwargs={"article_id": self.id})

    @classmethod
    def get_popular(cls,
                    count: int):
        res = cls.objects.raw(
            """
            select articles_article.*
            from articles_article
            left join (select articles_user.article_id,
                         count(articles_user.article_id) as fav_count
                  from articles_user
                  where articles_user.is_favorite
                  group by articles_user.article_id) as F on F.article_id = articles_article.id
            order by F.fav_count DESC 
            """
        )
        return res[:count]

    @classmethod
    def get_favorite_articles(cls, user):
        return cls.objects.filter(
            id__in=ArticleUserRel
            .objects
            .filter(user=user, is_favorite=True)
            .values('article_id')
        )

    def get_tests_by_categories(self):
        tests = set()
        for catalog in self.catalogs.all():
            if catalog.tests_ids():
                tests.update(catalog.tests_ids())

        return tests

    def get_articles_by_categories(self):
        articles = set()
        for catalog in self.catalogs.all():
            if catalog.articles_ids():
                articles.update(catalog.tests_ids())

        return articles

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.label
