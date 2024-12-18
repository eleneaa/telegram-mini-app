from django.db.models import Q
from django.shortcuts import render


def find(model, template_name: str):
    def find_view(request):
        queries = request.GET.get('label', '')
        if queries == '' or queries is None:
            objects = model.objects.all()
        else:
            objects = model.objects.filter(Q(**queries))
        return render(request,
                      template_name,
                      {'objects': objects})

    return find_view
