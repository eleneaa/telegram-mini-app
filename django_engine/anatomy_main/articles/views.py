from articles.models import Article
from django.core.exceptions import PermissionDenied
from django.db.models import FileField
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from users.models import ArticleUserRel


# Create your views here.


def article_view(request: HttpRequest,
                 uuid: str):
    if not request.user.is_authenticated:
        raise PermissionDenied
    article = get_object_or_404(Article, id=uuid)
    file: FileField = article.article_file
    article_user_rel: ArticleUserRel = ArticleUserRel.objects.get_or_create(user=request.user,
                                                                            article_id=uuid)[0]
    return render(request,
                  file.name.split('/')[-1],
                  {
                      "article_uuid": article.id,
                      "is_favorite": article_user_rel.is_favorite
                  })


def add_favorite_view(request: HttpRequest,
                      uuid: str):
    if request.method != "POST":
        return redirect(reverse("articles:article", args=[uuid]))
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied
    article_user_rel: ArticleUserRel = ArticleUserRel.objects.get_or_create(user=user, article_id=uuid)[0]
    article_user_rel.is_favorite = True
    article_user_rel.save()
    return redirect(reverse("articles:article", args=[uuid]))

