from django.http import HttpRequest, JsonResponse


# Create your views here.

def main(resquest: HttpRequest):
    pass


def find(request: HttpRequest):
    pass


def open_catalog(request: HttpRequest, catalog_id: str):
    return JsonResponse({"catalog_id": catalog_id})


def favorite_catalogs(request: HttpRequest):
    pass
