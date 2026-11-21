from django import forms
from django.utils import timezone
from django.forms import BaseInlineFormSet, inlineformset_factory

from app_contracts.models import Contract
from app_suppliers.models import Supplier
from .models import Delivery, DeliveryItem


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self):
        super().__init__(format="%Y-%m-%d")


class DeliveryFilterForm(forms.Form):
    start = forms.DateField(label="С даты", required=False, widget=DateInput)
    end = forms.DateField(label="По дату", required=False, widget=DateInput)
    supplier = forms.ModelChoiceField(label="Поставщик", queryset=Supplier.objects.all(), required=False)
    contract = forms.ModelChoiceField(label="Договор", queryset=Contract.objects.all(), required=False)
    status = forms.ChoiceField(label="Статус", choices=[("", "Все статусы"), *Delivery._meta.get_field("status").choices], required=False)
    sort = forms.ChoiceField(label="Сортировка", required=False, choices=[
        ("-delivery_date", "Сначала новые"), ("delivery_date", "Сначала старые"), ("supplier__name", "По поставщику"),
    ])

    def clean(self):
        data = super().clean()
        if data.get("start") and data.get("end") and data["end"] < data["start"]:
            self.add_error("end", "Конец периода должен быть не раньше начала.")
        return data


class DeliveryForm(forms.ModelForm):
    def clean_delivery_date(self):
        day = self.cleaned_data["delivery_date"]
        if day < timezone.localdate() and (not self.instance.pk or day != self.instance.delivery_date):
            raise forms.ValidationError("Для новой даты выберите сегодняшний или будущий день.")
        return day

    class Meta:
        model = Delivery
        fields = ("supplier", "contract", "delivery_date")
        widgets = {"delivery_date": DateInput()}
        help_texts = {"contract": "Выберите действующий на дату поставки договор этого поставщика."}


class ItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            data = form.cleaned_data
            product = data.get("product")
            if product and not data.get("DELETE") and product.supplier_id != self.instance.supplier_id:
                form.add_error("product", "Товар должен принадлежать поставщику заказа.")


DeliveryItems = inlineformset_factory(
    Delivery, DeliveryItem, formset=ItemFormSet, fields=("product", "quantity"),
    extra=1, min_num=1, validate_min=True, can_delete=True,
)
