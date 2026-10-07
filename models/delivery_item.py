"""Класс DeliveryItem — позиция поставки."""
from typing import Any

from .product import Product


class DeliveryItem:
    """Строка поставки: товар + количество + цена за единицу."""

    def __init__(self, product: Product, quantity: int, price: float) -> None:
        self.product = product
        self.quantity = quantity
        self.price = price

    def amount(self) -> float:
        """Стоимость позиции."""
        return self.quantity * self.price

    def __str__(self) -> str:
        return (f"{self.product.name}: {self.quantity} x "
                f"{self.price:.2f} = {self.amount():.2f} руб.")

    @classmethod
    def from_data(cls, data: dict[str, Any],
                  products: list[Product]) -> "DeliveryItem | None":
        product = next((p for p in products if p.id == data["product_id"]),
                       None)
        if product is None:
            return None
        return cls(product, data["quantity"], data["price"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_id": self.product.id,
            "quantity": self.quantity,
            "price": self.price,
        }