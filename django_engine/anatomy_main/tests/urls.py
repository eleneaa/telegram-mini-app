from django.urls import path

from anatomy_main import view_builder
from . import views
from .models import Test

app_name = 'tests'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('find/', view_builder.find(Test, "test_main_page.html"), name='find'),
    path('find_preview/', view_builder.find(Test, "find_preview_tests_component.html", 5), name='find_preview'),
    path('open/<str:test_id>/', views.open_test, name='open_test'),
    path('list_favorite_tests/', views.list_favorite_tests, name='list_favorite_tests'),
    path('list_popular_tests/', views.list_popular_tests, name='list_popular_tests'),
    path('toggle_favorite_test/<str:test_id>/', views.toggle_favorite_test, name='add_test_to_favorite'),
    path('run/<str:test_id>/', views.start_test, name='start_test'),
    path('run/<str:test_id>/questions/<int:question_id>/', views.question_detail, name='question_detail'),
    path('run/<str:test_id>/results/', views.test_results, name='test_results'),
    path('favorite/<str:question_id>/', views.toggle_favorite, name='add_to_favorite'),
    path("toggle_save_note_test/<str:test_id>/<str:note_text>/", views.toggle_save_note_test,
         name='toggle_save_note_test'),
    path("toggle_save_note_test/<str:test_id>/", views.toggle_save_note_test, name='toggle_save_note_test')
]
