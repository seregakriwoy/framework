from django import forms

from .models import Product


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("image",)
        help_texts = {"image": "Выберите фотографию товара в формате изображения."}
