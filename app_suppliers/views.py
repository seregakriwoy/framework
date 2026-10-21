"""Views приложения app_suppliers."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from services import (
    find_supplier_by_id,
    get_products_by_supplier,
    search_suppliers,
)
from storage import load_products, load_suppliers


def supplier_list(request: HttpRequest) -> HttpResponse:
    """Страница /suppliers/: список поставщиков."""
    suppliers = load_suppliers()
    context = {"suppliers": suppliers}
    return render(request, "suppliers/supplier_list.html", context)


def supplier_detail(request, supplier_id):
    suppliers = load_suppliers()
    supplier = find_supplier_by_id(suppliers, supplier_id)
    products = []
    if supplier:
        products = get_products_by_supplier(load_products(suppliers), supplier)
    return render(request, "suppliers/supplier_detail.html",
                  {"supplier": supplier, "products": products})


def supplier_search(request: HttpRequest) -> HttpResponse:
    """Страница /suppliers/search/?q=...: поиск поставщиков."""
    query = request.GET.get("q", "").strip()
    results = search_suppliers(load_suppliers(), query) if query else []
    context = {
        "query": query,
        "results": results,
    }
    return render(request, "suppliers/supplier_search.html", context)