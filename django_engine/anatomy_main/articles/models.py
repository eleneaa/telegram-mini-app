import uuid

from anatomy_main.models import BaseModel
from django.db import models
from django.urls import reverse
from users.models import ArticleUserRel


# Create your models here.


class Article(BaseModel):
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
                    count: int, current_category=None):

        if current_category:
            exp = f"""WITH article_results AS (SELECT articles_article.* 
                                          FROM articles_article_catalogs 
                                          LEFT JOIN articles_article ON articles_article_catalogs.article_id = articles_article.id
                                          WHERE articles_article_catalogs.catalog_id = '{current_category.id}')
                                          SELECT article_results.*
                                          FROM article_results
                """
        else:
            exp = """SELECT article_results.*
                         FROM articles_article AS article_results"""
        
        res = cls.objects.raw(
            f"""
            {exp}
            left join (select articles_user.article_id,
                         count(articles_user.article_id) as fav_count
                  from articles_user
                  where articles_user.is_favorite
                  group by articles_user.article_id) as F on F.article_id = article_results.id
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
        ).annotate(
            is_favorite=models.Value(True, output_field=models.BooleanField())
        )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.label
