from django.contrib import admin

from tests.models import Variant, Question, Test, QuestionVariantRel

from anatomy_main.utils import links_to_catalogs, links_to_questions


# Register your models here.

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('label', 'questions', 'catalog_ids')
    exclude = ("id", )

    def catalog_ids(self, obj):
        return links_to_catalogs(obj.catalog_ids())
    catalog_ids.short_description = 'Принадлежит каталогам'

    def questions(self, obj):
        return links_to_questions(obj.questions_ids())
    questions.short_description = 'Список вопросов'


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ("id", )


class QuestionVariantInline(admin.TabularInline):
    model = QuestionVariantRel
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('label', 'answers_ids', 'correct_answers')
    exclude = ("id",)
    inlines = [QuestionVariantInline]

    def answers_ids(self, obj):
        return obj.answers_ids()
    answers_ids.short_description = 'Варианты ответов'

    def correct_answers(self, obj):
        return obj.correct_answers()
    correct_answers.short_description = 'Правильные ответы'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'correct_variants':
            print('aaaa')
        # Обнулять список доступных вариантов только при создании нового вопроса
        return super().formfield_for_dbfield(db_field, request, **kwargs)
