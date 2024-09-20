from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    #path('', views.main, name='main'),
    #path('find/', views.find, name='find'),
    #path('find/<string:article_id>/', views.find_article, name='find_article'),
    path('open/<str:article_id>/', views.open_article, name='open_article'),
    #path('favorite_articles/', views.favorite_articles, name='favorite_articles'),
    path('favorite/<str:question_id>/', views.toggle_favorite, name='add_to_favorite'),

]
