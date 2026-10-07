"""Сохранение и загрузка объектов в JSON."""
import json
import os
from typing import Any

from models import Contract, Delivery, Product, Supplier


def _read(filename: str) -> list[dict[str, Any]]:
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return []


def _write(filename: str, data: list[dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка сохранения {filename}: {e}")


def load_suppliers(filename: str = "data/suppliers.json") -> list[Supplier]:
    return [Supplier.from_data(d) for d in _read(filename)]


def save_suppliers(suppliers: list[Supplier],
                   filename: str = "data/suppliers.json") -> None:
    _write(filename, [s.to_dict() for s in suppliers])


def load_products(suppliers: list[Supplier],
                  filename: str = "data/products.json") -> list[Product]:
    result = []
    for d in _read(filename):
        p = Product.from_data(d, suppliers)
        if p is not None:
            result.append(p)
    return result


def save_products(products: list[Product],
                  filename: str = "data/products.json") -> None:
    _write(filename, [p.to_dict() for p in products])


def load_contracts(suppliers: list[Supplier],
                   filename: str = "data/contracts.json") -> list[Contract]:
    result = []
    for d in _read(filename):
        c = Contract.from_data(d, suppliers)
        if c is not None:
            result.append(c)
    return result


def save_contracts(contracts: list[Contract],
                   filename: str = "data/contracts.json") -> None:
    _write(filename, [c.to_dict() for c in contracts])


def load_deliveries(suppliers: list[Supplier],
                    contracts: list[Contract],
                    products: list[Product],
                    filename: str = "data/deliveries.json") -> list[Delivery]:
    result = []
    for d in _read(filename):
        delivery = Delivery.from_data(d, suppliers, contracts, products)
        if delivery is not None:
            result.append(delivery)
    return result


def save_deliveries(deliveries: list[Delivery],
                    filename: str = "data/deliveries.json") -> None:
    _write(filename, [d.to_dict() for d in deliveries])