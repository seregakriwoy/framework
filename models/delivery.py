"""Класс Delivery — поставка."""
from datetime import date
from typing import Any

from .contract import Contract
from .delivery_item import DeliveryItem
from .supplier import Supplier


STATUS_CREATED = "Создан"
STATUS_SENT = "Отправлен"
STATUS_IN_TRANSIT = "В пути"
STATUS_ACCEPTED = "Принят"
STATUS_COMPLETED = "Завершён"

STATUS_FLOW = [
    STATUS_CREATED,
    STATUS_SENT,
    STATUS_IN_TRANSIT,
    STATUS_ACCEPTED,
    STATUS_COMPLETED,
]


class Delivery:
    """Поставка товаров от поставщика по договору."""

    def __init__(self, delivery_id: int, supplier: Supplier,
                 contract: Contract, delivery_date: date,
                 items: list[DeliveryItem],
                 status: str = STATUS_CREATED,
                 created_at: str | None = None) -> None:
        self.id = delivery_id
        self.supplier = supplier
        self.contract = contract
        self.delivery_date = delivery_date
        self.items = items
        self.status = status
        self.created_at = created_at or date.today().strftime("%Y-%m-%d")

    def __str__(self) -> str:
        return (f"[{self.id}] {self.supplier.name} | "
                f"{self.delivery_date} | {self.status} | "
                f"{self.total():.2f} руб.")

    def total(self) -> float:
        """Сумма поставки."""
        return sum(item.amount() for item in self.items)

    def next_status(self) -> str | None:
        """Следующий статус в цепочке или None, если финальный."""
        idx = STATUS_FLOW.index(self.status)
        if idx + 1 < len(STATUS_FLOW):
            return STATUS_FLOW[idx + 1]
        return None

    def change_status(self, new_status: str | None = None) -> bool:
        """Перевести на следующий шаг или на указанный статус.

        Возвращает False, если переход недопустим.
        """
        target = new_status or self.next_status()
        if target is None or target not in STATUS_FLOW:
            return False
        current = STATUS_FLOW.index(self.status)
        target_idx = STATUS_FLOW.index(target)
        if target_idx != current + 1:
            return False
        self.status = target
        return True

    def accept(self) -> bool:
        """Принять поставку: перевести в статус «Принят» и увеличить остатки."""
        if self.status != STATUS_IN_TRANSIT:
            return False
        for item in self.items:
            item.product.increase_stock(item.quantity)
        self.status = STATUS_ACCEPTED
        return True

    def complete(self) -> bool:
        """Завершить поставку."""
        if self.status != STATUS_ACCEPTED:
            return False
        self.status = STATUS_COMPLETED
        return True

    def acceptance_act(self) -> str:
        """Сформировать текст акта приёмки."""
        lines = [
            f"АКТ ПРИЁМКИ №{self.id}",
            f"Поставщик: {self.supplier.name}",
            f"Договор: №{self.contract.number}",
            f"Дата поставки: {self.delivery_date}",
            f"Статус: {self.status}",
            "Позиции:",
        ]
        for item in self.items:
            lines.append(f"  - {item}")
        lines.append(f"ИТОГО: {self.total():.2f} руб.")
        return "\n".join(lines)

    def is_in_period(self, start: date, end: date) -> bool:
        """Дата поставки в диапазоне?"""
        return start <= self.delivery_date <= end

    @classmethod
    def from_data(cls, data: dict[str, Any],
                  suppliers: list[Supplier],
                  contracts: list[Contract],
                  products: list) -> "Delivery | None":
        supplier = next((s for s in suppliers if s.id == data["supplier_id"]),
                        None)
        contract = next((c for c in contracts if c.id == data["contract_id"]),
                        None)
        if supplier is None or contract is None:
            return None
        items = []
        for raw in data.get("items", []):
            item = DeliveryItem.from_data(raw, products)
            if item is not None:
                items.append(item)
        return cls(
            delivery_id=data["id"],
            supplier=supplier,
            contract=contract,
            delivery_date=date.fromisoformat(data["delivery_date"]),
            items=items,
            status=data.get("status", STATUS_CREATED),
            created_at=data.get("created_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "supplier_id": self.supplier.id,
            "contract_id": self.contract.id,
            "delivery_date": self.delivery_date.isoformat(),
            "status": self.status,
            "created_at": self.created_at,
            "items": [item.to_dict() for item in self.items],
        }