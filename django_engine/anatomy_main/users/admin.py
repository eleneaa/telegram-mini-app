from django.contrib import admin

from users.models import User, News


# Register your models here.


@admin.register(User)
class TicketAdmin(admin.ModelAdmin):
    pass
