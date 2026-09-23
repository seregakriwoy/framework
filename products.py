from suppliers import _next_id


def add_products(products: list[dict], name: str, price: float, supplier_id: int) -> dict:
    product = {
        "id": _next_id(products),
        "name": name,
        "price": price,
        "supplier_id": supplier_id
    }
    products.append(product)
    return product


def get_product_by_id(products: list[dict], product_id: int) -> dict | None:
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def get_products_by_supplier(products: list[dict], supplier_id: int) -> list[dict]:
    return [p for p in products if p["supplier_id"] == supplier_id]


def get_all_products(products: list[dict]) -> None:
    if not products:
        print("No products found")
        return
    for product in products:
        print(f"{product['id']} {product['name']} | {product['price']:.2f} руб."
              f" поставщик #{product['supplier_id']}")


def update_products(products: list[dict], product_id: int, name: str | None = None, price: float | None = None) -> bool:
   product = get_product_by_id(products, product_id)
   if product is None:
       return False
   if name is not None:
       product["name"] = name
   if price is not None:
       product["price"] = price
   return True

def delete_products(products: list[dict], product_id: int) -> bool:
    product = get_product_by_id(products, product_id)
    if product is None:
        return False
    products.remove(product)
    return True

def assign_supplier_to_products(products: list[dict], product_id: int, supplier_id: int) -> bool:
    product = get_product_by_id(products, product_id)
    if product is None:
        return False
    product["supplier_id"] = supplier_id
    return True
