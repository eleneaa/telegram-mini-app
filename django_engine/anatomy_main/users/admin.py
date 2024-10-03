from django.contrib import admin

from .models import User, TestUserRel, QuestionUserRel, ArticleUserRel, CatalogUserRel, AtlasUserRel
from anatomy_main.utils import (links_to_catalogs_rel, links_to_questions_rel,
                                links_to_articles_rel, links_to_tests_rel, links_to_atlases_rel)


class TestUserInline(admin.TabularInline):
    model = TestUserRel
    extra = 1


class QuestionUserInline(admin.TabularInline):
    model = QuestionUserRel
    extra = 1


class ArticleUserInline(admin.TabularInline):
    model = ArticleUserRel
    extra = 1


class CatalogUserInline(admin.TabularInline):
    model = CatalogUserRel
    extra = 1


class AtlasUserInline(admin.TabularInline):
    model = AtlasUserRel
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'favorite_tests_ids', 'completed_tests_ids', 'favorite_questions_ids',
                    'favorite_articles_ids', 'favorite_catalogs_ids', 'favorite_atlases_ids']
    inlines = [TestUserInline, QuestionUserInline, ArticleUserInline, CatalogUserInline, AtlasUserInline]

    def favorite_tests_ids(self, obj):
        return links_to_tests_rel(obj.favorite_tests_ids())
    favorite_tests_ids.short_description = 'Избранные тесты'

    def completed_tests_ids(self, obj):
        return links_to_tests_rel(obj.completed_tests_ids())
    completed_tests_ids.short_description = 'Пройденные тесты'

    def favorite_questions_ids(self, obj):
        return links_to_questions_rel(obj.favorite_questions_ids())
    favorite_questions_ids.short_description = 'Избранные вопросы'

    def favorite_articles_ids(self, obj):
        return links_to_articles_rel(obj.favorite_articles_ids())
    favorite_articles_ids.short_description = 'Избранные статьи'

    def favorite_catalogs_ids(self, obj):
        return links_to_catalogs_rel(obj.favorite_catalogs_ids())
    favorite_catalogs_ids.short_description = 'Избранные темы'

    def favorite_atlases_ids(self, obj):
        return links_to_atlases_rel(obj.favorite_atlases_ids())
    favorite_atlases_ids.short_description = 'Избранные атласы'
