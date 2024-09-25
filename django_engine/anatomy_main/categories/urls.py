from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.main, name='main'),
    path('find/', views.find, name='find'),
    path('favorite/<str:catalog_id>/', views.toggle_favorite, name='add_to_favorite'),
    path('open/<str:catalog_id>/', views.open_catalog, name='open_catalog'),
    path('favorite_catalogs/', views.favorite_catalogs, name='favorite_catalogs'),
]
