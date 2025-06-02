from django.db.models import Q
from django.shortcuts import render


def find(model, template_name: str, limit: int = 0):
    def find_view(request):
        queries = request.GET.dict()
        if queries == '' or queries is None:
            objects = model.objects.all()
        else:
            objects = model.objects.filter(Q(**queries))
        return render(request,
                      template_name,
                      {'objects': objects if limit == 0 else objects[:limit]})

    return find_view
