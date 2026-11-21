from django.contrib import admin

from app_deliveries.admin import DeliveryInline
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("number", "supplier", "start_date", "end_date", "status")
    list_filter = ("status", "end_date")
    search_fields = ("number", "supplier__name")
    list_select_related = ("supplier",)
    ordering = ("-end_date", "number")
    list_per_page = 20
    inlines = (DeliveryInline,)

    def get_readonly_fields(self, request, obj=None):
        return ("supplier", "start_date", "end_date") if obj and obj.deliveries.exists() else ()
