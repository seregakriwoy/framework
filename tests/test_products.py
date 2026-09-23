from products import (
    add_products, get_product_by_id, get_products_by_supplier,
)


def test_add_product():
    products = []
    p = add_products(products, "Болт", 12.5, 1)
    assert p["id"] == 1
    assert p["supplier_id"] == 1


def test_get_products_by_supplier():
    products = []
    add_products(products, "Болт", 12.5, 1)
    add_products(products, "Гайка", 5.0, 1)
    add_products(products, "Шайба", 2.0, 2)
    assert len(get_products_by_supplier(products, 1)) == 2


def test_find_product_by_id():
    products = []
    add_products(products, "Болт", 12.5, 1)
    assert get_product_by_id(products, 1)["name"] == "Болт"
    assert get_product_by_id(products, 99) is None