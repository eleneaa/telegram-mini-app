import uuid
from djongo import models


class Catalog(models.Model):
    is_main = models.BooleanField(verbose_name="Является главным каталогом?")
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название каталога")
    child = models.ArrayReferenceField(
        to='self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='childs',
        verbose_name="ID вложенных каталогов",

    )

    def child_ids(self):
        cls = type(self)
        if self.child_id:
            childs_array = [cls.objects.get(id=child) for child in self.child_id]
            return childs_array

    def __eq__(self, other):
        return other == self.id

    def __str__(self):
        return self.name
