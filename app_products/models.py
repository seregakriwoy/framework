from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    price = models.DecimalField("Цена", max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField("Остаток", default=0)
    supplier = models.ForeignKey("app_suppliers.Supplier", models.PROTECT, related_name="products", verbose_name="Поставщик")
    image = models.ImageField("Фото товара", upload_to="products/%Y/%m/", blank=True)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ("name", "pk")

    @property
    def slug(self):
        return slugify(self.name, allow_unicode=True) or "товар"

    def get_absolute_url(self):
        return reverse("products:card", kwargs={"product_id": self.pk, "slug": self.slug})

    def __str__(self):
        return self.name
