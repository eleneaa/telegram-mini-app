from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    # path('favorites/', views.favorites, name='favorites'),
    # path('notes/', views.notes, name='notes'),
]
