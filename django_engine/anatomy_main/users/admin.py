from django.contrib import admin

from .models import User
from anatomy_main.utils import links_to_catalogs, links_to_questions, links_to_articles, links_to_tests


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'questions_ids', 'catalog_ids', 'articles_ids', 'tests_ids', 'finished_tests_ids']

    def questions_ids(self, obj):
        return links_to_questions(obj.questions_ids())
    questions_ids.short_description = 'Избранные вопросы'

    def catalog_ids(self, obj):
        return links_to_catalogs(obj.catalog_ids())
    catalog_ids.short_description = 'Избранные темы'

    def articles_ids(self, obj):
        return links_to_articles(obj.articles_ids())
    articles_ids.short_description = 'Избранные статьи'

    def tests_ids(self, obj):
        return links_to_tests(obj.tests_ids())
    tests_ids.short_description = 'Избранные тесты'

    def finished_tests_ids(self, obj):
        return links_to_tests(obj.finished_tests_ids())
    finished_tests_ids.short_description = 'Пройденные тесты'
