import uuid

from django.db import models
from django.urls import reverse

from users.models import CatalogUserRel


class Catalog(models.Model):
    is_main = models.BooleanField(verbose_name="Является главным каталогом?")
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название каталога")
    child = models.ManyToManyField('self',
                                   blank=True,
                                   symmetrical=False,
                                   verbose_name="ID вложенных каталогов",
                                   )
    image = models.ImageField(verbose_name="Заглавное изображение каталога", blank=True, upload_to='images_storage')
    description = models.CharField(max_length=1000, verbose_name="Описание каталога", blank=True)

    def child_ids(self):
        cls = type(self)
        if self.child.all():
            childs_array = [cls.objects.get(id=child.id) for child in self.child.all()]
            return childs_array
        return []

    def tests_ids(self):
        if self.tests.all():
            tests_array = [test for test in self.tests.all()]
            return tests_array
        return []

    def articles_ids(self):
        if self.articles.all():
            articles_array = [article for article in self.articles.all()]
            return articles_array
        return []

    def get_absolute_url(self):
        return reverse("categories:open_catalog", kwargs={"catalog_id": self.id})

    class Meta:
        verbose_name = 'Каталог темы'
        verbose_name_plural = 'Темы'

    @classmethod
    def get_favorite_catalogs(cls, user):
        return cls.objects.filter(
            id__in=CatalogUserRel
            .objects
            .filter(user=user, is_favorite=True)
            .values('catalog_id')
        )

    @classmethod
    def get_popular(cls,
                    count: int):
        res = cls.objects.raw(
            """
            select categories_catalog.*
            from categories_catalog
            left join (select catalog_user.catalog_id,
                         count(catalog_user.catalog_id) as fav_count
                  from catalog_user
                  where catalog_user.is_favorite
                  group by catalog_user.catalog_id) as F on F.catalog_id = categories_catalog.id
            order by F.fav_count DESC 
            """
        )
        return res[:count]

    def __eq__(self, other):
        return other == self.id

    def __str__(self):
        return self.name

    def __hash__(self):
        return super().__hash__()


