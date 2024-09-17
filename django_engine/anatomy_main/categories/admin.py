from django.contrib import admin

from categories.models import Catalog


class TestInline(admin.TabularInline):
    model = Catalog.catalogs_list.through
    extra = 0


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_main', 'child_ids', 'tests_ids']
    inlines = [TestInline]
    search_fields = ('name',)
    exclude = ['id']

    is_invalid = False

    def child_ids(self, obj):
        return obj.child_ids()
    child_ids.short_description = 'Имена дочерних элементов'

    def tests_ids(self, obj):
        return obj.tests_ids()
    tests_ids.short_description = 'Список тестов'

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
