from anatomy_main import utils
from categories.models import Catalog
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from users.models import CatalogUserRel


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


def set_current_category(request, category_id):
    request.session['current_category'] = category_id
    return redirect('main')


def unset_current_category(request, current_path_name):
    if request.session.get("current_category"):
        request.session['current_category'] = None

    return redirect(current_path_name)


def open_catalogs_list(request):
    root_catalogs = Catalog.objects.filter(is_main=True)
    return render(request, 'category_menu.html', {'catalogs': root_catalogs})
