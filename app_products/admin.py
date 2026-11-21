from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "supplier", "price", "stock")
    list_filter = ("supplier",)
    search_fields = ("name", "supplier__name")
    ordering = ("name", "pk")
    list_select_related = ("supplier",)
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        return ("supplier",) if obj and obj.delivery_items.exists() else ()
