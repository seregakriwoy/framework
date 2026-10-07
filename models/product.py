"""Класс Product — товар."""
from typing import Any

from .supplier import Supplier


class Product:
    """Товар, поставляемый поставщиком."""

    def __init__(self, product_id: int, name: str, price: float,
                 supplier: Supplier, stock: int = 0) -> None:
        self.id = product_id
        self.name = name
        self.price = price
        self.supplier = supplier
        self.stock = stock

    def __str__(self) -> str:
        return (f"[{self.id}] {self.name} | {self.price:.2f} руб. "
                f"| поставщик: {self.supplier.name} | остаток: {self.stock}")

    def update(self, name: str | None = None,
               price: float | None = None) -> None:
        """Обновить данные товара."""
        if name is not None:
            self.name = name
        if price is not None:
            self.price = price

    def assign_supplier(self, supplier: Supplier) -> None:
        """Назначить товару нового поставщика."""
        self.supplier = supplier

    def increase_stock(self, quantity: int) -> None:
        """Увеличить остаток на складе."""
        self.stock += quantity

    def decrease_stock(self, quantity: int) -> bool:
        """Уменьшить остаток; вернуть False при нехватке."""
        if quantity > self.stock:
            return False
        self.stock -= quantity
        return True

    def is_low_stock(self, threshold: int = 10) -> bool:
        """Остаток ниже порога?"""
        return self.stock < threshold

    @classmethod
    def from_data(cls, data: dict[str, Any],
                  suppliers: list[Supplier]) -> "Product | None":
        """Создать товар из данных JSON, найдя поставщика."""
        supplier = next((s for s in suppliers if s.id == data["supplier_id"]),
                        None)
        if supplier is None:
            return None
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            supplier=supplier,
            stock=data.get("stock", 0),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "supplier_id": self.supplier.id,
            "stock": self.stock,
        }