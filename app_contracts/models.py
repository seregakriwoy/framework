from django.core.exceptions import ValidationError
from django.db import models

from models.contract import STATUS_ACTIVE, VALID_STATUSES


class Contract(models.Model):
    supplier = models.ForeignKey("app_suppliers.Supplier", models.PROTECT, related_name="contracts", verbose_name="Поставщик")
    number = models.CharField("Номер", max_length=100)
    start_date = models.DateField("Начало действия")
    end_date = models.DateField("Окончание действия")
    status = models.CharField("Статус", max_length=20, choices=[(s, s) for s in VALID_STATUSES], default=STATUS_ACTIVE)

    class Meta:
        verbose_name = "договор"
        verbose_name_plural = "договоры"
        ordering = ("-start_date", "pk")

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "Окончание договора должно быть не раньше начала."})

    def __str__(self):
        return f"№ {self.number}"
