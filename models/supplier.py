"""Класс Supplier — поставщик."""
from datetime import datetime
from typing import Any


class Supplier:
    """Поставщик товаров."""

    def __init__(self, supplier_id: int, name: str, inn: str,
                 created_at: str | None = None) -> None:
        self.id = supplier_id
        self.name = name
        self.inn = inn
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d")

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} | ИНН: {self.inn}"

    def update(self, name: str | None = None,
               inn: str | None = None) -> None:
        """Обновить данные поставщика."""
        if name is not None:
            self.name = name
        if inn is not None:
            self.inn = inn

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Supplier":
        """Создать поставщика из данных JSON."""
        return cls(
            supplier_id=data["id"],
            name=data["name"],
            inn=data["inn"],
            created_at=data.get("created_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать в структуру для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "inn": self.inn,
            "created_at": self.created_at,
        }