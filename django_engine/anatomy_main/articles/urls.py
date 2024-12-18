from django.urls import path

from anatomy_main import view_builder
from . import views
from .models import Article

app_name = 'articles'

urlpatterns = [
    path('', views.main, name='main'),
    path('find/', view_builder.find(Article, "article_find.html"), name='find'),
    #path('find/<string:article_id>/', views.find_article, name='find_article'),
    path('open/<str:article_id>/', views.open_article, name='open_article'),
    path('favorite_articles/', views.favorite_articles, name='favorite_articles'),
    path('favorite/<str:article_id>/', views.toggle_favorite, name='add_to_favorite'),

]
