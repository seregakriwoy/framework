from django.contrib import admin, messages
from django.db import transaction
from django.db.models import F

from app_products.models import Product

from models.delivery import STATUS_ACCEPTED, STATUS_CREATED, STATUS_FLOW
from .forms import ItemFormSet
from .models import Delivery, DeliveryItem


class DeliveryInline(admin.TabularInline):
    model = Delivery
    fields = ("delivery_date", "status")
    readonly_fields = fields
    can_delete = False
    extra = 0
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


class ItemInline(admin.TabularInline):
    model = DeliveryItem
    formset = ItemFormSet
    extra = 1
    min_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        return super().get_formset(request, obj, validate_min=True, **kwargs)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "delivery_date", "supplier", "contract", "status")
    list_filter = ("status", "delivery_date", "supplier")
    search_fields = ("supplier__name", "contract__number")
    ordering = ("-delivery_date", "-pk")
    list_select_related = ("supplier", "contract")
    list_per_page = 20
    readonly_fields = ("status",)
    inlines = (ItemInline,)
    actions = ("advance_status",)

    @admin.action(description="Перевести на следующий этап поставки")
    @transaction.atomic
    def advance_status(self, request, queryset):
        changed = 0
        for delivery in queryset.select_for_update().filter(status__in=STATUS_FLOW[:-1]):
            next_status = STATUS_FLOW[STATUS_FLOW.index(delivery.status) + 1]
            if next_status == STATUS_ACCEPTED:
                for item in delivery.items.all():
                    Product.objects.filter(pk=item.product_id).update(stock=F("stock") + item.quantity)
            delivery.status = next_status
            delivery.save(update_fields=["status"])
            changed += 1
        self.message_user(request, f"Переведено на следующий этап: {changed}.", messages.SUCCESS)


    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and (obj is None or obj.status == STATUS_CREATED)


@admin.register(DeliveryItem)
class DeliveryItemAdmin(admin.ModelAdmin):
    list_display = ("delivery", "product", "quantity")
    search_fields = ("product__name", "delivery__contract__number")
    list_filter = ("product__supplier",)
    list_select_related = ("delivery", "product")
    ordering = ("delivery", "pk")
    list_per_page = 20

    # Позиции редактируются комплектом в карточке поставки.
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
