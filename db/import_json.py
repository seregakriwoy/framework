import json
import os
from db.database import get_connection

DATA_DIR = "data/"

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main():
    conn = get_connection()
    try:
        # 1. Поставщики
        suppliers = load_json("suppliers.json")
        conn.executemany(
            "INSERT INTO suppliers (id, name, inn, created_at) VALUES (?, ?, ?, ?)",
            [(s["id"], s["name"], s["inn"], s["created_at"]) for s in suppliers]
        )

        # 2. Товары
        products = load_json("products.json")
        conn.executemany(
            "INSERT INTO products (id, name, price, stock, supplier_id) VALUES (?, ?, ?, ?, ?)",
            # Обрати внимание: если в JSON supplier хранится как объект, нужно взять supplier["id"]
            [(p["id"], p["name"], p["price"], p["stock"], p["supplier"]["id"] if isinstance(p.get("supplier"), dict) else p.get("supplier_id")) for p in products]
        )

        # 3. Договоры
        contracts = load_json("contracts.json")
        conn.executemany(
            "INSERT INTO contracts (id, number, start_date, end_date, status, supplier_id) VALUES (?, ?, ?, ?, ?, ?)",
            [(c["id"], c["number"], c["start_date"], c["end_date"], c["status"], c["supplier"]["id"] if isinstance(c.get("supplier"), dict) else c.get("supplier_id")) for c in contracts]
        )

        # 4. Поставки
        deliveries = load_json("deliveries.json")
        conn.executemany(
            "INSERT INTO deliveries (id, delivery_date, status, supplier_id, contract_id) VALUES (?, ?, ?, ?, ?)",
            [(d["id"], d["delivery_date"], d["status"], d["supplier"]["id"] if isinstance(d.get("supplier"), dict) else d.get("supplier_id"), d["contract"]["id"] if isinstance(d.get("contract"), dict) else d.get("contract_id")) for d in deliveries]
        )

        # 5. Позиции поставок (если они лежат в отдельном файле или внутри deliveries)
        # Предположим, они лежат внутри deliveries в ключе 'items'
        delivery_items_data = []
        for d in deliveries:
            for item in d.get("items", []):
                delivery_items_data.append((
                    item.get("id", len(delivery_items_data) + 1), # Генерируем ID если нет
                    d["id"],
                    item["product"]["id"] if isinstance(item.get("product"), dict) else item.get("product_id"),
                    item["quantity"]
                ))

        conn.executemany(
            "INSERT INTO delivery_items (id, delivery_id, product_id, quantity) VALUES (?, ?, ?, ?)",
            delivery_items_data
        )

        conn.commit()
        print("Данные успешно импортированы!")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при импорте: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()