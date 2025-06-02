"""
URL configuration for anatomy_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import main, init_page, notes, delete_note, favorites

urlpatterns = [
    path('', init_page),
    path('home/', main, name='main'),
    path('admin/', admin.site.urls),
    path("tests/", include('tests.urls')),
    path("categories/", include('categories.urls')),
    path("articles/", include('articles.urls')),
    path('atlases/', include('atlases.urls'), name='atlases'),
    path("user/", include('users.urls')),
    path("notes/", notes, name='notes'),
    path('notes/delete_note/<str:object_id>', delete_note, name="delete_note"),
    path('favorites/', favorites, name='favorites')
]
