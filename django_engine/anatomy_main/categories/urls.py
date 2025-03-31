from django.urls import path

from anatomy_main import view_builder
from . import views
from .models import Catalog

app_name = 'categories'

urlpatterns = [
    path('', views.main, name='main'),
    path('find/', view_builder.find(Catalog, "all_categories.html"), name='find'),
    path('find_preview/', view_builder.find(Catalog, "find_preview_categories_component.html", 5), name='find_preview'),
    path('favorite/<str:catalog_id>/', views.toggle_favorite, name='add_to_favorite'),
    path('open/<str:catalog_id>/', views.open_catalog, name='open_catalog'),
    path('favorite_catalogs/', views.favorite_catalogs, name='favorite_catalogs'),
]
