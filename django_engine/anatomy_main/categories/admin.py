from django.contrib import admin

from .models import Catalog
from anatomy_main.utils import links_to_catalogs, links_to_tests, links_to_articles, links_to_atlases


class TestInline(admin.TabularInline):
    model = Catalog.tests.through
    extra = 1
    verbose_name = 'Тест'
    verbose_name_plural = 'Тесты'


class ArticleInline(admin.TabularInline):
    model = Catalog.articles.through
    extra = 1
    verbose_name = 'Статья'
    verbose_name_plural = 'Статьи'


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_main', 'child_ids', 'tests_ids', 'articles_ids', 'atlases_ids']
    inlines = [TestInline, ArticleInline]
    search_fields = ('name',)
    exclude = ['id']

    is_invalid = False

    def child_ids(self, obj):
        return links_to_catalogs(obj.child_ids())
    child_ids.short_description = 'Дочерние каталоги (Подкаталоги)'

    def tests_ids(self, obj):
        return links_to_tests(obj.tests_ids())
    tests_ids.short_description = 'Список тестов'

    def articles_ids(self, obj):
        return links_to_articles(obj.articles_ids())
    articles_ids.short_description = 'Список статей'

    def atlases_ids(self, obj):
        return links_to_atlases(obj.atlases_ids())
    atlases_ids.short_description = 'Список атласов'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'child':
            if request.resolver_match.kwargs.get("object_id"):
                current_instance = self.get_object(request, request.resolver_match.kwargs['object_id'])
                if current_instance:
                    # Исключается возможность добавлять "самого себя" во вложенные каталоги
                    kwargs['queryset'] = Catalog.objects.exclude(id=current_instance.id)

                    # Исключается возможность добавлять главные каталоги во вложенные каталоги
                    kwargs['queryset'] = kwargs['queryset'].exclude(is_main=True)

        return super().formfield_for_dbfield(db_field, request, **kwargs)
