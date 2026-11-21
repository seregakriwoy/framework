from django.db.models import Count, Q, Sum
from app_deliveries.models import OPEN_STATUSES, DeliveryStatus
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from app_suppliers.models import Supplier
from .forms import ProductImageForm
from .models import Product


def product_list(request):
    products = Product.objects.select_related("supplier").order_by("supplier__name", "name", "pk")
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id, slug=None):
    product = get_object_or_404(Product.objects.select_related("supplier"), pk=product_id)
    if slug is not None and slug != product.slug:
        raise Http404("Товар по этому адресу не найден.")
    return render(request, "products/product_detail.html", {"product": product})


def product_statistics(request):
    stats = Supplier.objects.values("id", "name").annotate(
        product_count=Count("products", distinct=True),
        open_count=Count("deliveries", filter=Q(deliveries__status__in=OPEN_STATUSES), distinct=True),
        completed_count=Count("deliveries", filter=Q(deliveries__status=DeliveryStatus.COMPLETED), distinct=True),
        cancelled_count=Count("deliveries", filter=Q(deliveries__status=DeliveryStatus.CANCELLED), distinct=True),
    ).order_by("-product_count", "name")
    stock = Product.objects.aggregate(total=Sum("stock", default=0))
    return render(request, "products/statistics.html", {"stats": stats, "stock": stock["total"]})


@require_http_methods(["GET", "POST"])
def product_image(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductImageForm(instance=product)
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:detail", product_id=product.pk)
    return render(request, "products/product_image.html", {"form": form, "product": product})
