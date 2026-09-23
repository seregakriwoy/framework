import json
import os
from typing import Any

def _load(filename: str) -> list[dict[str, Any]]:
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"The file {filename} is damaged.")
        return []

def _save(filename: str, data: list[dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Failed to write to {filename}: {e}")

def load_suppliers(filename: str = "data/suppliers.json") -> list[dict]:
    return _load(filename)

def save_suppliers(suppliers: list[dict], filename: str = "data/suppliers.json") -> None:
    _save(filename, suppliers)

def load_products(filename: str = "data/products.json") -> list[dict]:
    return _load(filename)

def save_products(products: list[dict], filename: str = "data/products.json") -> None:
    _save(filename, products)

def load_contracts(filename: str = "data/contracts.json") -> list[dict]:
    return _load(filename)

def save_contracts(contracts: list[dict], filename: str = "data/contracts.json") -> None:
    _save(filename, contracts)