from django.urls import path

from . import views

app_name = 'atlases'

urlpatterns = [
    path('', views.main, name='main'),
    path('find/', views.find, name='find'),
    path('open/<str:atlas_id>/', views.open_atlas, name='open_atlas'),
    path('favorite_atlases/', views.favorite_atlases, name='favorite_atlases'),
    path('favorite/<str:atlas_id>/', views.toggle_favorite, name='add_to_favorite'),
]