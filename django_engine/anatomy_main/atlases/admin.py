from django.contrib import admin
from .models import Atlas


@admin.register(Atlas)
class UserAdmin(admin.ModelAdmin):
    exclude = ['id']
