from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('list_user_completed_tests/', views.list_user_completed_tests, name='list_user_completed_tests'),
    # path('favorites/', views.favorites, name='favorites'),
    # path('notes/', views.notes, name='notes'),
]
