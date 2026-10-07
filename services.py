"""Операции над коллекциями объектов (сервисный слой)."""
from datetime import date
from typing import Optional

from models import (
    STATUS_TERMINATED, Contract, Delivery, DeliveryItem,
    Product, Supplier,
)


def _next_id(items: list) -> int:
    return max((i.id for i in items), default=0) + 1


# ---------------- Поставщики ----------------

def add_supplier(suppliers: list[Supplier], name: str, inn: str) -> Supplier:
    s = Supplier(_next_id(suppliers), name, inn)
    suppliers.append(s)
    return s


def find_supplier_by_id(suppliers: list[Supplier],
                        supplier_id: int) -> Optional[Supplier]:
    return next((s for s in suppliers if s.id == supplier_id), None)


def search_suppliers(suppliers: list[Supplier],
                     query: str) -> list[Supplier]:
    q = query.lower()
    return [s for s in suppliers if q in s.name.lower() or q in s.inn]


def delete_supplier(suppliers: list[Supplier],
                    products: list[Product],
                    contracts: list[Contract],
                    supplier_id: int) -> bool:
    """Удалить поставщика, если нет ссылок на него."""
    s = find_supplier_by_id(suppliers, supplier_id)
    if s is None:
        return False
    if any(p.supplier is s for p in products):
        return False
    if any(c.supplier is s for c in contracts):
        return False
    suppliers.remove(s)
    return True


def show_suppliers(suppliers: list[Supplier]) -> None:
    if not suppliers:
        print("Список поставщиков пуст.")
        return
    for s in suppliers:
        print(s)


# ---------------- Товары ----------------

def add_product(products: list[Product], name: str, price: float,
                supplier: Supplier) -> Product:
    p = Product(_next_id(products), name, price, supplier)
    products.append(p)
    return p


def find_product_by_id(products: list[Product],
                       product_id: int) -> Optional[Product]:
    return next((p for p in products if p.id == product_id), None)


def get_products_by_supplier(products: list[Product],
                             supplier: Supplier) -> list[Product]:
    return [p for p in products if p.supplier is supplier]


def show_products(products: list[Product]) -> None:
    if not products:
        print("Список товаров пуст.")
        return
    for p in products:
        print(p)


# ---------------- Договоры ----------------

def create_contract(contracts: list[Contract], supplier: Supplier,
                    number: str, start: date, end: date) -> Contract:
    c = Contract(_next_id(contracts), supplier, number, start, end)
    contracts.append(c)
    return c


def find_contract_by_id(contracts: list[Contract],
                        contract_id: int) -> Optional[Contract]:
    return next((c for c in contracts if c.id == contract_id), None)


def delete_contract(contracts: list[Contract],
                    deliveries: list[Delivery],
                    contract_id: int) -> bool:
    """Удалить договор, если на него нет ссылок в поставках."""
    c = find_contract_by_id(contracts, contract_id)
    if c is None:
        return False
    if any(d.contract is c for d in deliveries):
        return False
    contracts.remove(c)
    return True


def get_expiring_contracts(contracts: list[Contract],
                           days: int = 30) -> list[Contract]:
    return [c for c in contracts if c.is_expiring(days)]


def show_contracts(contracts: list[Contract]) -> None:
    if not contracts:
        print("Список договоров пуст.")
        return
    for c in contracts:
        print(c)


# ---------------- Поставки ----------------

def create_delivery(deliveries: list[Delivery], supplier: Supplier,
                    contract: Contract, delivery_date: date,
                    items: list[DeliveryItem]) -> Delivery:
    d = Delivery(_next_id(deliveries), supplier, contract,
                 delivery_date, items)
    deliveries.append(d)
    return d


def find_delivery_by_id(deliveries: list[Delivery],
                        delivery_id: int) -> Optional[Delivery]:
    return next((d for d in deliveries if d.id == delivery_id), None)


def get_all_deliveries(deliveries: list[Delivery]) -> list[Delivery]:
    return list(deliveries)


def get_delivery_history(deliveries: list[Delivery],
                         supplier: Supplier | None = None
                         ) -> list[Delivery]:
    result = sorted(deliveries, key=lambda d: d.delivery_date)
    if supplier is not None:
        result = [d for d in result if d.supplier is supplier]
    return result


def filter_deliveries_by_date(deliveries: list[Delivery],
                              start: date,
                              end: date) -> list[Delivery]:
    return [d for d in deliveries if d.is_in_period(start, end)]


def show_deliveries(deliveries: list[Delivery]) -> None:
    if not deliveries:
        print("Список поставок пуст.")
        return
    for d in deliveries:
        print(d)