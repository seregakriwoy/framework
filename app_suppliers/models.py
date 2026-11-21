from django.db import models
from django.utils import timezone


class Supplier(models.Model):
    name = models.CharField("Название", max_length=200)
    inn = models.CharField("ИНН", max_length=20)
    created_at = models.DateField("Дата регистрации", default=timezone.localdate)

    class Meta:
        verbose_name = "поставщик"
        verbose_name_plural = "поставщики"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name
