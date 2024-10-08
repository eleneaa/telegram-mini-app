import uuid

from django.db import models
from django.urls import reverse
from users.models import AtlasUserRel


class Atlas(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    label = models.CharField(max_length=50, verbose_name='Название файла')
    atlas_file = models.ImageField(verbose_name='Файл атласа', upload_to='atlases_storage')
    catalogs = models.ManyToManyField("categories.Catalog", verbose_name="Принадлежит каталогам",
                                      related_name='atlases', blank=True)

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
            SELECT atlases_atlas.*
            FROM atlases_atlas
            LEFT JOIN (
                SELECT atlas_user.atlas_id,
                       COUNT(atlas_user.atlas_id) AS fav_count
                FROM atlas_user
                WHERE atlas_user.is_favorite
                GROUP BY atlas_user.atlas_id
            ) AS F ON F.atlas_id = atlases_atlas.id
            ORDER BY F.fav_count DESC
            """
        )
        return res[:count]

    def __str__(self):
        return self.label
