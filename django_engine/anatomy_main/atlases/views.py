from anatomy_main import utils
from categories.models import Catalog
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from users.models import AtlasUserRel

from .models import Atlas


def main(request: HttpRequest):
    popular_atlases = Atlas.get_popular(10)
    favorite_atlases = Atlas.get_favorite_atlases(request.user)
    categories = Catalog.objects.all()
    return render(request, 'atlases_main_page.html', {
        'popular_atlases': popular_atlases,
        'favorite_atlases': favorite_atlases,
        'categories': categories
    })


def open_atlas(request: HttpRequest,
               atlas_id: str):
    atlas = get_object_or_404(Atlas, id=atlas_id)
    atlas_user_rel: AtlasUserRel = AtlasUserRel.objects.get_or_create(user=request.user,
                                                                      atlas_id=atlas_id)[0]

    if request.method == "POST":
        utils.toggle_save_note(request, atlas_id, AtlasUserRel, 'atlas_id', request.POST.get("note"))

    try:
        rel_field = AtlasUserRel.objects.get(atlas=atlas, user=request.user)
    except AtlasUserRel.DoesNotExist:
        note = ''
    else:
        note = rel_field.note

    return render(request,
                  'atlas.html',
                  {
                      "atlas": atlas,
                      'tests': atlas.get_tests_by_categories(),
                      'articles': atlas.get_articles_by_categories(),
                      "is_favorite": atlas_user_rel.is_favorite,
                      'note': note
                  })


@require_POST
def toggle_save_note(request, atlas_id, note_text=''):
    return utils.toggle_save_note(request, atlas_id, AtlasUserRel, 'atlas_id', note_text)


@require_POST
def toggle_favorite(request: HttpRequest,
                    atlas_id: str):
    return utils.toggle_favorite(request,
                                 atlas_id,
                                 AtlasUserRel,
                                 "atlas_id")


def list_favorite_atlases(request):
    return render(request, 'list_atlases_page.html', context={"atlases": Atlas.get_favorite_atlases(request.user)})


def list_popular_atlases(request):
    return render(request, 'list_atlases_page.html', context={"atlases": Atlas.get_popular(count=10)})


def find(request: HttpRequest):
    queries = request.GET
    atlases = Atlas.objects.filter(Q(label__icontains=queries.get('label', '')))
    return render(request, 'atlas_find.html', {'atlases': atlases})


def open_articles_by_atlases(request, atlas_id: str):
    atlas = get_object_or_404(Atlas, id=atlas_id)
    return render(request, "list_articles_page.html", context={'articles': atlas.get_articles_by_categories()})


def open_tests_by_atlases(request, atlas_id: str):
    atlas = get_object_or_404(Atlas, id=atlas_id)
    return render(request, "list_tests_page.html", context={'tests': atlas.get_tests_by_categories()})
