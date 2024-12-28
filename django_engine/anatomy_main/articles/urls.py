from django.urls import path

from anatomy_main import view_builder
from . import views
from .models import Article

app_name = 'articles'

urlpatterns = [
    path('', views.main, name='main'),
    path('find/', view_builder.find(Article, "article_find.html"), name='find'),
    path('open/<str:article_id>/', views.open_article, name='open_article'),
    path('popular_articles/', views.list_popular_articles, name='popular_articles'),
    path('favorite_articles/', views.list_favorite_articles, name='favorite_articles'),
    path('toggle_favorite_article/<str:article_id>/', views.toggle_favorite, name='add_to_favorite'),
    path('toggle_save_note/<str:article_id>/<str:note_text>/', views.toggle_save_note, name='toggle_save_note'),
]
