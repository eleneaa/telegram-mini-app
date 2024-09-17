from django.contrib import admin

from .models import User, TestUserRel
from anatomy_main.utils import links_to_catalogs, links_to_questions, links_to_articles, links_to_tests_rel


class TestUserInline(admin.TabularInline):
    model = TestUserRel
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'favorite_tests_ids', 'completed_tests_ids', 'favorite_questions_ids',
                    'favorite_articles_ids', 'favorite_catalogs_ids']
    inlines = [TestUserInline]

    def favorite_tests_ids(self, obj):
        return links_to_tests_rel(obj.favorite_tests_ids())
    favorite_tests_ids.short_description = 'Избранные тесты'

    def completed_tests_ids(self, obj):
        return links_to_tests_rel(obj.completed_tests_ids())
    completed_tests_ids.short_description = 'Пройденные тесты'

    def favorite_questions_ids(self, obj):
        return links_to_questions(obj.favorite_questions_ids())
    favorite_questions_ids.short_description = 'Избранные вопросы'

    def favorite_articles_ids(self, obj):
        return links_to_articles(obj.favorite_articles_ids())
    favorite_articles_ids.short_description = 'Избранные статьи'

    def favorite_catalogs_ids(self, obj):
        return links_to_catalogs(obj.favorite_catalogs_ids())
    favorite_catalogs_ids.short_description = 'Избранные темы'
