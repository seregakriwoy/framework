"""Класс Contract — договор с поставщиком."""
from datetime import date, datetime
from typing import Any

from .supplier import Supplier


STATUS_ACTIVE = "активен"
STATUS_EXPIRED = "истёк"
STATUS_TERMINATED = "расторгнут"

VALID_STATUSES = (STATUS_ACTIVE, STATUS_EXPIRED, STATUS_TERMINATED)


class Contract:
    """Договор с поставщиком."""

    def __init__(self, contract_id: int, supplier: Supplier,
                 number: str, start_date: date, end_date: date,
                 status: str = STATUS_ACTIVE) -> None:
        self.id = contract_id
        self.supplier = supplier
        self.number = number
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def __str__(self) -> str:
        return (f"[{self.id}] №{self.number} | поставщик: {self.supplier.name} "
                f"| {self.start_date}–{self.end_date} | {self.status}")

    def update(self, number: str | None = None,
               start_date: date | None = None,
               end_date: date | None = None) -> None:
        """Обновить условия договора."""
        if number is not None:
            self.number = number
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date

    def change_status(self, status: str) -> bool:
        """Изменить статус. False, если статус недопустим."""
        if status not in VALID_STATUSES:
            return False
        self.status = status
        return True

    def terminate(self) -> None:
        """Расторгнуть договор."""
        self.status = STATUS_TERMINATED

    def is_active(self) -> bool:
        """Договор активен?"""
        return self.status == STATUS_ACTIVE

    def is_expiring(self, days: int = 30) -> bool:
        """Договор истекает в ближайшие N дней (только активный)."""
        if not self.is_active():
            return False
        return 0 <= (self.end_date - date.today()).days <= days

    def is_expired(self) -> bool:
        """Договор уже истёк?"""
        return self.end_date < date.today() and self.status != STATUS_TERMINATED

    @classmethod
    def from_data(cls, data: dict[str, Any],
                  suppliers: list[Supplier]) -> "Contract | None":
        supplier = next((s for s in suppliers if s.id == data["supplier_id"]),
                        None)
        if supplier is None:
            return None
        return cls(
            contract_id=data["id"],
            supplier=supplier,
            number=data["number"],
            start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
            end_date=datetime.strptime(data["end_date"], "%Y-%m-%d").date(),
            status=data.get("status", STATUS_ACTIVE),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "supplier_id": self.supplier.id,
            "number": self.number,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "status": self.status,
        }