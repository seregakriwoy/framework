"""Сохранение и загрузка объектов предметной области в JSON-файлы.

Модуль отвечает за два направления:
- JSON → объекты (load_*);
- объекты → JSON (save_*).

Работа с файлами выполняется через контекстный менеджер,
ошибки чтения/записи обрабатываются исключениями.
"""
import json
import os
from typing import Any

from models import (
    Contract,
    Delivery,
    Product,
    Supplier,
)


# ---------- Вспомогательные функции ----------

def _read(filename: str) -> list[dict[str, Any]]:
    """Прочитать JSON-файл. Если файла нет или он повреждён — []."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return []


def _write(filename: str, data: list[dict[str, Any]]) -> None:
    """Записать данные в JSON-файл, создав каталог при необходимости."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка сохранения {filename}: {e}")


# ---------- Поставщики ----------

def load_suppliers(
    filename: str = "data/suppliers.json",
) -> list[Supplier]:
    """Загрузить поставщиков из JSON."""
    return [Supplier.from_data(d) for d in _read(filename)]


def save_suppliers(
    suppliers: list[Supplier],
    filename: str = "data/suppliers.json",
) -> None:
    """Сохранить поставщиков в JSON."""
    _write(filename, [s.to_dict() for s in suppliers])


# ---------- Товары ----------

def load_products(
    suppliers: list[Supplier],
    filename: str = "data/products.json",
) -> list[Product]:
    """Загрузить товары, привязав их к уже загруженным поставщикам."""
    result: list[Product] = []
    for d in _read(filename):
        product = Product.from_data(d, suppliers)
        if product is not None:
            result.append(product)
    return result


def save_products(
    products: list[Product],
    filename: str = "data/products.json",
) -> None:
    """Сохранить товары в JSON."""
    _write(filename, [p.to_dict() for p in products])


# ---------- Договоры ----------

def load_contracts(
    suppliers: list[Supplier],
    filename: str = "data/contracts.json",
) -> list[Contract]:
    """Загрузить договоры, привязав их к уже загруженным поставщикам."""
    result: list[Contract] = []
    for d in _read(filename):
        contract = Contract.from_data(d, suppliers)
        if contract is not None:
            result.append(contract)
    return result


def save_contracts(
    contracts: list[Contract],
    filename: str = "data/contracts.json",
) -> None:
    """Сохранить договоры в JSON."""
    _write(filename, [c.to_dict() for c in contracts])


# ---------- Поставки ----------

def load_deliveries(
    suppliers: list[Supplier],
    contracts: list[Contract],
    products: list[Product],
    filename: str = "data/deliveries.json",
) -> list[Delivery]:
    """Загрузить поставки, привязав их к поставщикам, договорам и товарам."""
    result: list[Delivery] = []
    for d in _read(filename):
        delivery = Delivery.from_data(d, suppliers, contracts, products)
        if delivery is not None:
            result.append(delivery)
    return result


def save_deliveries(
    deliveries: list[Delivery],
    filename: str = "data/deliveries.json",
) -> None:
    """Сохранить поставки в JSON."""
    _write(filename, [d.to_dict() for d in deliveries])