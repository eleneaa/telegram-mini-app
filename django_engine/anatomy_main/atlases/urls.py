from django.urls import path

from anatomy_main import view_builder
from . import views
from .models import Atlas

app_name = 'atlases'

urlpatterns = [
    path('', views.main, name='main'),
    path('find/', view_builder.find(Atlas, "atlas_find.html"), name='find'),
    path('open/<str:atlas_id>/', views.open_atlas, name='open_atlas'),
    path('favorite_atlases/', views.list_favorite_atlases, name='favorite_atlases'),
    path('popular_atlases/', views.list_popular_atlases, name='popular_atlases'),
    path('toggle_favorite_atlas/<str:atlas_id>/', views.toggle_favorite, name='add_to_favorite'),
    path('toggle_save_note/<str:atlas_id>/<str:note_text>/', views.toggle_save_note, name='toggle_save_note'),
]
