import uuid
from django.db import models


class Catalog(models.Model):
    is_main = models.BooleanField(verbose_name="Является главным каталогом?")
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название каталога")
    child = models.ManyToManyField('self',
                                   blank=True,
                                   symmetrical=False,
                                   verbose_name="ID вложенных каталогов",
                                   )

    def child_ids(self):
        cls = type(self)
        if self.child.all():
            childs_array = [cls.objects.get(id=child.id) for child in self.child.all()]
            return childs_array

    def __eq__(self, other):
        return other == self.id

    def __str__(self):
        return self.name

    def __hash__(self):
        return super().__hash__()
