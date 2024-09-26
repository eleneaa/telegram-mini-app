from django.db.models import FileField, Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from anatomy_main import utils
from articles.models import Article
from categories.models import Catalog
from users.models import ArticleUserRel


# Create your views here.

def main(request: HttpRequest):
    popular_articles = Article.get_popular(10)
    favorite_articles = Article.get_favorite_articles(request.user)
    categories = Catalog.objects.all()
    return render(request, 'all_articles.html', {
        'popular_articles': popular_articles,
        'favorite_articles': favorite_articles,
        'categories': categories
    })


def open_article(request: HttpRequest,
                 article_id: str):
    article = get_object_or_404(Article, id=article_id)
    file: FileField = article.article_file
    article_user_rel: ArticleUserRel = ArticleUserRel.objects.get_or_create(user=request.user,
                                                                            article_id=article_id)[0]
    return render(request,
                  file.name.split('/')[-1],
                  {
                      "article": article,
                      "is_favorite": article_user_rel.is_favorite
                  })


@require_POST
def toggle_favorite(request: HttpRequest,
                    article_id: str):
    return utils.toggle_favorite(request,
                                 article_id,
                                 ArticleUserRel,
                                 "article_id")


def favorite_articles(request: HttpRequest):
    return render(request, 'article_favorite.html', {
        'favorite_articles': request.user.favorite_articles_ids()
    })


def find(request: HttpRequest):
    queries = request.GET
    articles = Article.objects.filter(Q(label__icontains=queries.get('label', '')))
    return render(request, 'article_find.html', {'articles': articles})
