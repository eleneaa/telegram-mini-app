from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('', views.TestsView.as_view(), name='main'),
    # path('find/', views.find, name='find'),
    # path('find/<str:catalog_id>/', views.find_catalog_tests, name='find_catalog_tests'),
    # path('favorite_tests/', views.favorite_tests, name='favorite_tests'),
    # path('favorite_questions/', views.favorite_tests, name='favorite_questions'),
    # path('finished_tests/', views.finished_tests, name='finished_tests'),
    path('open/<str:test_id>/', views.open_test, name='open_test'),
    path('toggle_favorite_test/<str:test_id>/', views.toggle_favorite_test, name='add_test_to_favorite'),
    path('run/<str:test_id>/', views.start_test, name='start_test'),
    path('run/<str:test_id>/questions/<int:question_id>/', views.question_detail, name='question_detail'),
    path('run/<str:test_id>/results/', views.test_results, name='test_results'),
    path('favorite/<str:question_id>/', views.toggle_favorite, name='add_to_favorite'),
    path("toggle_save_note_test/<str:test_id>/<str:note_text>/", views.toggle_save_note_test, name='toggle_save_note_test'),
    path("toggle_save_note_test/<str:test_id>/", views.toggle_save_note_test, name='toggle_save_note_test')
]
