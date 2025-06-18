import uuid

from anatomy_main.models import BaseModel
from django.db import models
from django.urls import reverse
from users.models import AtlasUserRel


class Atlas(BaseModel):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(max_length=200, verbose_name='Название файла')
    atlas_file = models.ImageField(verbose_name='Файл атласа', upload_to='atlases_storage')
    catalogs = models.ManyToManyField("categories.Catalog", verbose_name="Принадлежит каталогам",
                                      related_name='atlases', blank=True)
    description = models.CharField(verbose_name="Текст атласа", max_length=1000, default='')
    tooltips = models.JSONField(verbose_name='Координаты подсказок', default=dict)

    class Meta:
        verbose_name = 'Атлас'
        verbose_name_plural = 'Атласы'

    def child_ids(self):
        cls = type(self)
        if self.child.all():
            children = [cls.objects.get(id=child.id) for child in self.child.all()]
            return children
        return []

    def get_absolute_url(self):
        return reverse("atlases:open_atlas", kwargs={"atlas_id": self.id})

    @classmethod
    def get_favorite_atlases(cls, user):
        return cls.objects.filter(
            id__in=AtlasUserRel.objects.filter(user=user, is_favorite=True).values('atlas_id')
        ).annotate(
            is_favorite=models.Value(True, output_field=models.BooleanField())
        )

    @classmethod
    def get_popular(cls, count: int, current_category=None):
        if current_category:
            exp = f"""WITH atlas_results AS (SELECT atlases_atlas.* 
                                      FROM atlases_atlas_catalogs 
                                      LEFT JOIN atlases_atlas ON atlases_atlas_catalogs.atlas_id = atlases_atlas.id
                                      WHERE atlases_atlas_catalogs.catalog_id = '{current_category.id}')
                                      SELECT atlas_results.*
                                      FROM atlas_results
            """
        else:
            exp = """SELECT atlas_results.*
                     FROM atlases_atlas AS atlas_results
                  """

        res = cls.objects.raw(
            f"""
            {exp}
            LEFT JOIN (
                SELECT atlas_user.atlas_id,
                       COUNT(atlas_user.atlas_id) AS fav_count
                FROM atlas_user
                WHERE atlas_user.is_favorite
                GROUP BY atlas_user.atlas_id
            ) AS F ON F.atlas_id = atlas_results.id
            ORDER BY F.fav_count DESC
            """
        )
        return res[:count]

    def __str__(self):
        return self.label
