from django.contrib import admin

from app_deliveries.admin import DeliveryInline
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "inn", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "inn")
    ordering = ("name", "pk")
    list_per_page = 20
    inlines = (DeliveryInline,)
