from categories.models import Catalog

class CatalogRepository:
    @staticmethod
    def get_objects():
        return Catalog.objects.all()

    @staticmethod
    def get_catalog(id_: str):
        return Catalog.objects.get(id=id_)