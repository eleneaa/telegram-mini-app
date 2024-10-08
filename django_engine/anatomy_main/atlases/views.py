from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import ImageField, Q

from anatomy_main import utils
from .models import Atlas
from users.models import AtlasUserRel
from categories.models import Catalog

def main(request: HttpRequest):
    popular_atlases = Atlas.get_popular(10)
    favorite_atlases = Atlas.get_favorite_atlases(request.user)
    categories = Catalog.objects.all()
    return render(request, 'all_atlases.html', {
        'popular_atlases': popular_atlases,
        'favorite_atlases': favorite_atlases,
        'categories': categories
    })


def open_atlas(request: HttpRequest,
                 atlas_id: str):
    atlas = get_object_or_404(Atlas, id=atlas_id)
    file: ImageField = atlas.atlas_file
    atlas_user_rel: AtlasUserRel = AtlasUserRel.objects.get_or_create(user=request.user,
                                                                            atlas_id=atlas_id)[0]
    return render(request,
                  file.name.split('/')[-1],
                  {
                      "article": atlas,
                      "is_favorite": atlas_user_rel.is_favorite
                  })


@require_POST
def toggle_favorite(request: HttpRequest,
                    atlas_id: str):
    return utils.toggle_favorite(request,
                                 atlas_id,
                                 AtlasUserRel,
                                 "atlas_id")


def favorite_atlases(request: HttpRequest):
    return render(request, 'atlases_favorite.html', {
        'favorite_atlases': request.user.favorite_atlases_ids()
    })


def find(request: HttpRequest):
    queries = request.GET
    atlases = Atlas.objects.filter(Q(label__icontains=queries.get('label', '')))
    return render(request, 'atlas_find.html', {'atlases': atlases})