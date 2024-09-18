import uuid

from django.db import models

# Create your models here.


class Article(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(max_length=50, verbose_name='Название файла')
    article_file = models.FileField(verbose_name='Файл статьи', upload_to='articles_storage')
    catalogs = models.ManyToManyField("categories.Catalog", verbose_name="Принадлежит каталогам",
                                      related_name='articles', blank=True)

    def catalog_ids(self):
        if self.catalogs.all():
            catalogs_array = [catalog for catalog in self.catalogs.all()]
            return catalogs_array

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.label

