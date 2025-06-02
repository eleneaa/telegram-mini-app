from django.urls import path

from anatomy_main import view_builder
from . import views
from .models import Article

app_name = 'articles'

urlpatterns = [
    path('', views.main, name='main'),
    path('find/', view_builder.find(Article, "articles_main_page.html"), name='find'),
    path('find_preview/', view_builder.find(Article, "find_preview_articles_component.html", 5), name='find_preview'),
    path('open/<str:article_id>/', views.open_article, name='open_article'),
    path('popular_articles/', views.list_popular_articles, name='popular_articles'),
    path('favorite_articles/', views.list_favorite_articles, name='favorite_articles'),
    path('toggle_favorite_article/<str:article_id>/', views.toggle_favorite, name='add_to_favorite'),
    path('toggle_save_note/<str:article_id>/<str:note_text>/', views.toggle_save_note, name='toggle_save_note'),
    path('atlases/<str:article_id>', views.open_atlases_by_article, name='open_atlases_by_article'),
    path('articles/<str:article_id>', views.open_tests_by_article, name='open_tests_by_article')
]
