from django.db import models
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.utils.html import format_html


def links_to_catalogs(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:categories_catalog_change", args=[obj.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.name)
        rel_list += "</ol>"
        return format_html(rel_list)


def links_to_catalogs_rel(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:categories_catalog_change", args=[obj.catalog.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.catalog.name)
        rel_list += "</ol>"
        return format_html(rel_list)


def links_to_tests(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:tests_test_change", args=[obj.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.label)
        rel_list += "</ol>"
        return format_html(rel_list)


def links_to_tests_rel(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:tests_test_change", args=[obj.test.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.test.label)
        rel_list += "</ol>"
        return format_html(rel_list)


def links_to_articles(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:articles_article_change", args=[obj.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.label)
        rel_list += "</ol>"
        return format_html(rel_list)


def links_to_articles_rel(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:articles_article_change", args=[obj.article.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.article.label)
        rel_list += "</ol>"
        return format_html(rel_list)


def links_to_questions(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:tests_question_change", args=[obj.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.label)
        rel_list += "</ol>"
        return format_html(rel_list)


def links_to_questions_rel(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:tests_question_change", args=[obj.question.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.question.label)
        rel_list += "</ol>"
        return format_html(rel_list)


def toggle_favorite(request: HttpRequest,
                    model_id: str,
                    rel_user_model_type: type[models.Model],
                    rel_column_name: str):
    user = request.user
    model_user_rel, created = rel_user_model_type.objects.get_or_create(user=user,
                                                                        **{rel_column_name: model_id})
    if created:
        model_user_rel.is_favorite = True
        model_user_rel.save()
        return JsonResponse({"action": "added"})
    else:
        model_user_rel.delete()
        return JsonResponse({"action": "removed"})
