from articles.models import Article
from django.db.models import FileField
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from users.models import ArticleUserRel


# Create your views here.


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
                    question_id: str):
    user = request.user
    article_user_rel, created = ArticleUserRel.objects.get_or_create(user=user,
                                                                     article_id=question_id)
    if created:
        article_user_rel.is_favorite = True
        article_user_rel.save()
        return JsonResponse({"action": "added"})
    else:
        article_user_rel.delete()
        return JsonResponse({"action": "removed"})
