import copy

from django.contrib import admin

from categories.models import Catalog


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_main', 'child_ids']
    search_fields = ('name',)
    exclude = ['id']

    is_invalid = False

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'child':
            if request.resolver_match.kwargs.get("object_id"):
                current_instance = self.get_object(request, request.resolver_match.kwargs['object_id'])
                if current_instance:
                    kwargs['queryset'] = Catalog.objects.exclude(id=current_instance.id)

                    if not current_instance.is_main:
                        kwargs['queryset'] = kwargs['queryset'].exclude(is_main__in=[True])

        return super().formfield_for_dbfield(db_field, request, **kwargs)
