from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from anatomy_main import utils
from categories.models import Catalog
from users.models import CatalogUserRel


from .models import Atlas
from users.models import AtlasUserRel


def main(request: HttpRequest):
    return render(request,
                  'all_categories.html',
                  {'popular_catalogs': Catalog.get_popular(5)})


def find(request: HttpRequest):
    queries = request.GET
    catalogs = Catalog.objects.filter(Q(name__icontains=queries.get('name', '')))
    return render(request,
                  'categories_find.html',
                  {'catalogs': catalogs})


def open_catalog(request: HttpRequest, catalog_id: str):
    return render(request,
                  'category.html',
                  {'catalog': get_object_or_404(Catalog, id=catalog_id)})


def favorite_catalogs(request: HttpRequest):
    return render(request,
                  'category_favorite.html',
                  {'catalogs': request.user.favorite_catalogs_ids()})


@require_POST
def toggle_favorite(request, catalog_id: str):
    return utils.toggle_favorite(request,
                                 catalog_id,
                                 CatalogUserRel,
                                 "catalog_id")


def main(request: HttpRequest):
    popular_atlases = Atlas.get_popular(10)
    favorite_atlases = Atlas.get_favorite_atlases(request.user)
    return render(request, 'all_atlases.html', {
        'popular_atlases': popular_atlases,
        'favorite_atlases': favorite_atlases
    })


def open_atlas(request: HttpRequest, atlas_id: str):
    atlas = get_object_or_404(Atlas, id=atlas_id)
    atlas_user_rel, _ = AtlasUserRel.objects.get_or_create(user=request.user, atlas_id=atlas_id)
    return render(request, 'open_atlas.html', {
        "atlas": atlas,
        "is_favorite": atlas_user_rel.is_favorite
    })


@require_POST
def toggle_favorite_atlas(request: HttpRequest, atlas_id: str):
    return utils.toggle_favorite(request, atlas_id, AtlasUserRel, "atlas_id")


def favorite_atlases(request: HttpRequest):
    return render(request, 'atlas_favorite.html', {
        'favorite_atlases': request.user.favorite_atlases_ids()
    })
