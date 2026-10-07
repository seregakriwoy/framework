from models import Product, Supplier
from services import (
    add_product, add_supplier, find_product_by_id,
    get_products_by_supplier,
)


def test_create_product():
    s = Supplier(1, "АО ООН", "125678910")
    p = Product(1, "Болт", 12.5, s)
    assert p.id == 1
    assert p.supplier is s


def test_assign_supplier():
    s1 = Supplier(1, "A", "1")
    s2 = Supplier(2, "B", "2")
    p = Product(1, "Болт", 12.5, s1)
    p.assign_supplier(s2)
    assert p.supplier is s2


def test_increase_decrease_stock():
    s = Supplier(1, "A", "1")
    p = Product(1, "Болт", 12.5, s)
    p.increase_stock(10)
    assert p.stock == 10
    assert p.decrease_stock(3)
    assert p.stock == 7
    assert not p.decrease_stock(100)
    assert p.stock == 7


def test_get_products_by_supplier():
    suppliers = []
    s1 = add_supplier(suppliers, "A", "1")
    s2 = add_supplier(suppliers, "B", "2")
    products = []
    add_product(products, "Болт", 12.5, s1)
    add_product(products, "Гайка", 5.0, s1)
    add_product(products, "Шайба", 2.0, s2)
    assert len(get_products_by_supplier(products, s1)) == 2
    assert len(get_products_by_supplier(products, s2)) == 1