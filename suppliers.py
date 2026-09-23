from datetime import datetime

def _next_id(items: list[dict]) -> int:
    return max((i["id"] for i in items), default=0)+1

def create_supplier(suppliers:list[dict], name: str, inn: str) -> dict:
    supplier = {
        "id": _next_id(suppliers),
        "name": name,
        "inn": inn,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    suppliers.append(supplier)
    return supplier

def get_supplier_by_id(suppliers: list[dict], supplier_id: int) -> dict | None:
    for supplier in suppliers:
        if supplier["id"] == supplier_id:
            return supplier
    return None

def search_suppliers(suppliers:list[dict], query: str) -> list[dict]:
    q = query.lower()
    return [s for s in suppliers
        if q in s["name"].lower() or q in s["inn"]]

def update_supplier(suppliers: list[dict], supplier_id: int, name: str | None = None, inn: str | None = None) -> bool:
    s = get_supplier_by_id(suppliers, supplier_id)
    if s is None:
        return False
    if name is not None:
        s["name"] = name
    if inn is not None:
        s["inn"] = inn
    return True

def delete_supplier(suppliers: list[dict], supplier_id: int) -> bool:
    s = get_supplier_by_id(suppliers, supplier_id)
    if s is None:
        return False
    suppliers.remove(s)
    return True

def get_all_suppliers(suppliers: list[dict]) -> None:
    if not suppliers:
        print("No suppliers found.")
        return
    for supplier in suppliers:
        print(f"[{supplier["id"]}] {supplier['name']} | ИНН: {supplier['inn']}"
              f"| зарегистрирован: {supplier['created_at']}")