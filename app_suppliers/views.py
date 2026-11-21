from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Supplier


def supplier_list(request):
    return render(request, "suppliers/supplier_list.html", {"suppliers": Supplier.objects.all()})


def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    return render(request, "suppliers/supplier_detail.html", {"supplier": supplier, "products": supplier.products.all()})


def supplier_search(request):
    query = request.GET.get("q", "").strip()
    results = Supplier.objects.none()
    if query:
        results = Supplier.objects.filter(Q(name__icontains=query) | Q(inn__contains=query))
    return render(request, "suppliers/supplier_search.html", {"query": query, "results": results})
