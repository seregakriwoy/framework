"""Views приложения app_products."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from services import find_product_by_id
from storage import load_products, load_suppliers


def product_list(request: HttpRequest) -> HttpResponse:
    """Страница /products/: список товаров."""
    suppliers = load_suppliers()
    products = load_products(suppliers)
    context = {"products": products}
    return render(request, "products/product_list.html", context)


def product_detail(request: HttpRequest,
                   product_id: int) -> HttpResponse:
    """Страница /products/<id>/: карточка товара."""
    suppliers = load_suppliers()
    products = load_products(suppliers)
    product = find_product_by_id(products, product_id)
    context = {"product": product}
    return render(
        request,
        "products/product_detail.html",
        context,
        status=404 if product is None else 200,
    )