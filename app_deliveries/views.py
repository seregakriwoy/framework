"""Views приложения app_deliveries."""
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from services import (
    filter_deliveries_by_date,
    find_delivery_by_id,
    get_delivery_history,
)
from storage import (
    load_contracts, load_deliveries, load_products, load_suppliers,
)


def _load_all():
    suppliers = load_suppliers()
    contracts = load_contracts(suppliers)
    products = load_products(suppliers)
    deliveries = load_deliveries(suppliers, contracts, products)
    return deliveries


def delivery_list(request: HttpRequest) -> HttpResponse:
    """Страница /deliveries/: список поставок."""
    deliveries = _load_all()
    context = {"deliveries": deliveries}
    return render(request, "deliveries/delivery_list.html", context)


def delivery_detail(request: HttpRequest,
                    delivery_id: int) -> HttpResponse:
    """Страница /deliveries/<id>/: карточка поставки."""
    deliveries = _load_all()
    delivery = find_delivery_by_id(deliveries, delivery_id)
    context = {"delivery": delivery}
    return render(
        request,
        "deliveries/delivery_detail.html",
        context,
        status=404 if delivery is None else 200,
    )


def delivery_filter(request: HttpRequest) -> HttpResponse:
    """Страница /deliveries/filter/?start=...&end=...: фильтр по дате."""
    start_str = request.GET.get("start")
    end_str = request.GET.get("end")

    try:
        start = datetime.strptime(start_str, "%Y-%m-%d").date()
        end = datetime.strptime(end_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return render(
            request,
            "deliveries/filter_error.html",
            status=400,
        )

    deliveries = _load_all()
    result = filter_deliveries_by_date(deliveries, start, end)
    context = {
        "start": start,
        "end": end,
        "deliveries": result,
    }
    return render(request, "deliveries/delivery_filter.html", context)