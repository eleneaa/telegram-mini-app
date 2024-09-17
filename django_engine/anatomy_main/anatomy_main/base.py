import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    catalogs = models.ManyToManyField('self', verbose_name="Принадлежит каталогу", related_name='catalogs_list')

    class Meta:
        abstract = True
