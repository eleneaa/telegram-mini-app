from django.urls import path

from anatomy_main import view_builder
from . import views
from .models import Atlas

app_name = 'atlases'

urlpatterns = [
    path('', views.main, name='main'),
    path('find/', view_builder.find(Atlas, "atlases_main_page.html"), name='find'),
    path('find_preview/', view_builder.find(Atlas, "find_preview_atlases_component.html", 5), name='find_preview'),
    path('open/<str:atlas_id>/', views.open_atlas, name='open_atlas'),
    path('favorite_atlases/', views.list_favorite_atlases, name='favorite_atlases'),
    path('popular_atlases/', views.list_popular_atlases, name='popular_atlases'),
    path('toggle_favorite_atlas/<str:atlas_id>/', views.toggle_favorite, name='add_to_favorite'),
    path('toggle_save_note/<str:atlas_id>/<str:note_text>/', views.toggle_save_note, name='toggle_save_note'),
    path('toggle_save_note/<str:atlas_id>/', views.toggle_save_note, name='toggle_save_note'),
    path('articles/<str:atlas_id>', views.open_articles_by_atlases, name='open_articles_by_atlases'),
    path('tests/<str:atlas_id>', views.open_tests_by_atlases, name='open_tests_by_atlases')
]
