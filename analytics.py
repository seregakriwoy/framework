"""Аналитические функции."""
from datetime import date

from models import (
    STATUS_ACCEPTED, STATUS_COMPLETED, Contract,
    Delivery, Product, Supplier,
)


def get_total_spent(deliveries: list[Delivery],
                    start: date | None = None,
                    end: date | None = None) -> float:
    """Общая сумма затрат по принятым/завершённым поставкам."""
    total = 0.0
    for d in deliveries:
        if d.status not in (STATUS_ACCEPTED, STATUS_COMPLETED):
            continue
        if start and end and not d.is_in_period(start, end):
            continue
        total += d.total()
    return total


def get_supplier_rating(deliveries: list[Delivery]
                        ) -> list[tuple[Supplier, float]]:
    """Рейтинг поставщиков по объёму поставок (убывание)."""
    totals: dict[int, float] = {}
    objects: dict[int, Supplier] = {}
    for d in deliveries:
        totals[d.supplier.id] = totals.get(d.supplier.id, 0) + d.total()
        objects[d.supplier.id] = d.supplier
    return sorted(((objects[k], v) for k, v in totals.items()),
                  key=lambda x: x[1], reverse=True)


def get_stock_balance(products: list[Product]) -> dict[int, int]:
    """Остатки товаров на складе: {product_id: quantity}."""
    return {p.id: p.stock for p in products}


def get_low_stock_products(products: list[Product],
                           threshold: int = 10) -> list[Product]:
    """Товары с остатком ниже порога."""
    return [p for p in products if p.is_low_stock(threshold)]