import uuid

from django.db import models
from django.urls import reverse
from users.models import AtlasUserRel



class Atlas(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(max_length=50, verbose_name='Название файла')
    atlas_file = models.ImageField(verbose_name='Файл атласа', upload_to='atlases_storage')
    catalogs = models.ManyToManyField("categories.Catalog", verbose_name="Принадлежит каталогам",
                                      related_name='articles', blank=True)

    def child_ids(self):
        cls = type(self)
        if self.child.all():
            children = [cls.objects.get(id=child.id) for child in self.child.all()]
            return children
        return []

    def get_absolute_url(self):
        return reverse("atlas:open_atlas", kwargs={"atlas_id": self.id})

    @classmethod
    def get_favorite_atlases(cls, user):
        return cls.objects.filter(
            id__in=AtlasUserRel.objects.filter(user=user, is_favorite=True).values('atlas_id')
        )

    @classmethod
    def get_popular(cls, count: int):
        res = cls.objects.raw(
            """
            SELECT atlas.*
            FROM atlas
            LEFT JOIN (
                SELECT catalog_user.atlas_id,
                       COUNT(catalog_user.atlas_id) AS fav_count
                FROM catalog_user
                WHERE catalog_user.is_favorite
                GROUP BY catalog_user.atlas_id
            ) AS F ON F.atlas_id = atlas.id
            ORDER BY F.fav_count DESC
            """
        )
        return res[:count]