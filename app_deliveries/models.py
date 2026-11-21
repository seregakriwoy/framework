from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from models.contract import STATUS_ACTIVE
from models.delivery import STATUS_ACCEPTED, STATUS_COMPLETED, STATUS_CREATED, STATUS_IN_TRANSIT, STATUS_SENT


class DeliveryStatus(models.TextChoices):
    CREATED = STATUS_CREATED, "Создан"
    SENT = STATUS_SENT, "Отправлен"
    IN_TRANSIT = STATUS_IN_TRANSIT, "В пути"
    ACCEPTED = STATUS_ACCEPTED, "Принят"
    COMPLETED = STATUS_COMPLETED, "Завершён"
    CANCELLED = "Отменён", "Отменён"


OPEN_STATUSES = (DeliveryStatus.CREATED, DeliveryStatus.SENT, DeliveryStatus.IN_TRANSIT)


class DeliveryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=OPEN_STATUSES)

    def scheduled(self, day):
        return self.active().filter(delivery_date=day)


class Delivery(models.Model):
    objects = DeliveryQuerySet.as_manager()

    supplier = models.ForeignKey("app_suppliers.Supplier", models.PROTECT, related_name="deliveries", verbose_name="Поставщик")
    contract = models.ForeignKey("app_contracts.Contract", models.PROTECT, related_name="deliveries", verbose_name="Договор")
    delivery_date = models.DateField("Дата поставки")
    status = models.CharField("Статус", max_length=20, choices=DeliveryStatus.choices, default=STATUS_CREATED)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("contract", "delivery_date"), condition=models.Q(status__in=OPEN_STATUSES),
                name="one_open_delivery_per_contract_day",
            ),
        ]
        verbose_name = "поставка"
        verbose_name_plural = "поставки"
        ordering = ("-delivery_date", "-pk")

    def clean(self):
        if not self.contract_id:
            return
        contract = self.contract
        if self.supplier_id and contract.supplier_id != self.supplier_id:
            raise ValidationError({"contract": "Выберите договор указанного поставщика."})
        if self.status == STATUS_CREATED and contract.status != STATUS_ACTIVE:
            raise ValidationError({"contract": "Для заказа нужен активный договор."})
        if self.delivery_date and not contract.start_date <= self.delivery_date <= contract.end_date:
            raise ValidationError({"delivery_date": "Дата поставки должна входить в срок действия договора."})

        if self.delivery_date and self.status in OPEN_STATUSES:
            conflicts = Delivery.objects.scheduled(self.delivery_date).filter(contract_id=self.contract_id).exclude(pk=self.pk)
            if conflicts.exists():
                raise ValidationError({"delivery_date": "На эту дату по договору уже запланирована поставка."})

    def cancel(self):
        """Повторная отмена сохраняет результат первого запроса."""
        changed = Delivery.objects.filter(pk=self.pk, status=DeliveryStatus.CREATED).update(
            status=DeliveryStatus.CANCELLED
        )
        if changed:
            self.status = DeliveryStatus.CANCELLED
            return True
        self.refresh_from_db(fields=["status"])
        return self.status == DeliveryStatus.CANCELLED

    def __str__(self):
        return f"Поставка № {self.pk}"


class DeliveryItem(models.Model):
    delivery = models.ForeignKey(Delivery, models.CASCADE, related_name="items", verbose_name="Поставка")
    product = models.ForeignKey("app_products.Product", models.PROTECT, related_name="delivery_items", verbose_name="Товар")
    quantity = models.PositiveIntegerField("Количество", validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "позиция поставки"
        verbose_name_plural = "позиции поставок"

    @property
    def amount(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product} × {self.quantity}"
