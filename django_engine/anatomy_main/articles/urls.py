from django.urls import path

from django_engine.anatomy_main.articles.views import article_view, add_favorite_view

app_name = "articles"

urlpatterns = [

    path('open/<str:uuid>', article_view, name='article'),
    path('favorite/<str:uuid>', add_favorite_view, name='add_favorite_article'),
]