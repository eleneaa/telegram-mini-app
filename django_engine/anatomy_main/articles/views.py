import os

from django.db.models import FileField, Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from anatomy_main import utils
from articles.models import Article
from categories.models import Catalog
from users.models import ArticleUserRel
from anatomy_main.settings import MEDIA_ROOT


# Create your views here.

def main(request: HttpRequest):
    popular_articles = Article.get_popular(10)
    favorite_articles = Article.get_favorite_articles(request.user)
    categories = Catalog.objects.all()
    return render(request, 'articles_main_page.html', {
        'popular_articles': popular_articles,
        'favorite_articles': favorite_articles,
        'categories': categories
    })


def open_article(request: HttpRequest,
                 article_id: str):
    article = get_object_or_404(Article, id=article_id)
    file = article.article_file
    pdf_file = article.pdf_file

    article_user_rel: ArticleUserRel = ArticleUserRel.objects.get_or_create(user=request.user,
                                                                            article_id=article_id)[0]

    try:
        rel_field = ArticleUserRel.objects.get(article=article, user=request.user)
    except ArticleUserRel.DoesNotExist:
        note = ''
    else:
        note = rel_field.note

    article_content_path = os.path.join(MEDIA_ROOT, str(file)) if file else None
    return render(request,
                  'article.html',
                  {
                      "pdf": pdf_file.url if pdf_file else None,
                      "article": article,
                      "is_favorite": article_user_rel.is_favorite,
                      'tests': article.get_tests_by_categories(),
                      'articles': article.get_articles_by_categories(),
                      'article_content_path': (article_content_path
                                               if article_content_path and os.path.exists(article_content_path)
                                               else None),
                      "note": note
                  })


@require_POST
def toggle_favorite(request: HttpRequest,
                    article_id: str):
    return utils.toggle_favorite(request,
                                 article_id,
                                 ArticleUserRel,
                                 "article_id")


@require_POST
def toggle_save_note(request, article_id, note_text=''):
    return utils.toggle_save_note(request, article_id, ArticleUserRel, 'article_id', note_text)


def find(request: HttpRequest):
    queries = request.GET
    articles = Article.objects.filter(Q(label__icontains=queries.get('label', '')))
    return render(request, 'article_find.html', {'articles': articles})


def list_favorite_articles(request):
    return render(request, 'list_articles_page.html', context={"articles": Article.get_favorite_articles(request.user)})


def list_popular_articles(request):
    return render(request, 'list_articles_page.html', context={"articles": Article.get_popular(count=10)})