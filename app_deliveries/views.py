from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from app_contracts.models import Contract
from models.contract import STATUS_ACTIVE
from models.delivery import STATUS_CREATED
from .forms import DeliveryFilterForm, DeliveryForm, DeliveryItems
from .models import Delivery


def delivery_list(request):
    form = DeliveryFilterForm(request.GET)
    deliveries = Delivery.objects.select_related("supplier").annotate(
        total=Sum(F("items__quantity") * F("items__product__price"), default=0)
    )
    valid = form.is_valid()
    if valid:
        data = form.cleaned_data
        for field, lookup in (("start", "delivery_date__gte"), ("end", "delivery_date__lte"),
                              ("supplier", "supplier"), ("contract", "contract"), ("status", "status")):
            if data[field]:
                deliveries = deliveries.filter(**{lookup: data[field]})
        deliveries = deliveries.order_by(data["sort"] or "-delivery_date", "pk")
    else:
        deliveries = deliveries.none()
    available = None
    if valid and data["start"] and data["start"] == data["end"]:
        day = data["start"]
        booked = Delivery.objects.scheduled(day).values_list("contract_id", flat=True)
        available = Contract.objects.filter(
            status=STATUS_ACTIVE, start_date__lte=day, end_date__gte=day
        ).exclude(pk__in=booked)
        if data["supplier"]:
            available = available.filter(supplier=data["supplier"])
    page = Paginator(deliveries, 10).get_page(request.GET.get("page"))
    return render(request, "deliveries/delivery_list.html", {"form": form, "deliveries": page, "available": available}, status=200 if valid else 400)


def delivery_detail(request, delivery_id):
    delivery = get_object_or_404(Delivery.objects.select_related("supplier", "contract"), pk=delivery_id)
    items = list(delivery.items.select_related("product"))
    return render(request, "deliveries/delivery_detail.html", {
        "delivery": delivery, "items": items, "total": sum(item.amount for item in items),
    })


@require_http_methods(["GET", "POST"])
@transaction.atomic
def delivery_edit(request, delivery_id=None):
    delivery = Delivery() if delivery_id is None else get_object_or_404(Delivery.objects.select_for_update(), pk=delivery_id)
    if delivery.status != STATUS_CREATED:
        return HttpResponse("Изменить можно только созданную поставку.", status=409)
    data = request.POST if request.method == "POST" else None
    form = DeliveryForm(data, instance=delivery)
    items = DeliveryItems(data, instance=delivery)
    if request.method == "POST":
        valid = form.is_valid()
        if items.is_valid() and valid:
            form.save()
            items.save()
            return redirect("deliveries:detail", delivery_id=delivery.pk)
    return render(request, "deliveries/delivery_form.html", {"form": form, "items": items, "delivery": delivery})


@require_POST
@transaction.atomic
def delivery_cancel(request, delivery_id):
    delivery = get_object_or_404(Delivery, pk=delivery_id)
    if not delivery.cancel():
        return HttpResponse("Отмена доступна только до отправки.", status=409)
    return redirect("deliveries:detail", delivery_id=delivery.pk)
