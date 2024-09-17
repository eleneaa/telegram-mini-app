from django.contrib import admin
from .models import Article
from anatomy_main.utils import links_to_catalogs


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('label', 'catalog_ids')
    exclude = ("id", )

    def catalog_ids(self, obj):
        return links_to_catalogs(obj.catalog_ids())
    catalog_ids.short_description = 'Принадлежит каталогам'
