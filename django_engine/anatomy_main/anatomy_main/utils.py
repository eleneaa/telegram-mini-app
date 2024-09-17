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


def links_to_tests(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:tests_test_change", args=[obj.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.label)
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


def links_to_questions(objects):
    if objects:
        rel_list = "<ol style=padding-left:'0'>"
        for obj in objects:
            link = reverse("admin:tests_question_change", args=[obj.id])
            rel_list += "<li><a href='%s'>%s</a></li>" % (link, obj.label)
        rel_list += "</ol>"
        return format_html(rel_list)