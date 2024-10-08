from django.urls import path
from . import views

app_name = 'atlases'

urlpatterns = [
    path('', views.main, name='all_atlases'),
    # path('favorites/', views.favorites, name='favorites'),
    # path('notes/', views.notes, name='notes'),
]
