from models import Supplier
from services import (
    add_supplier, delete_supplier, find_supplier_by_id,
    search_suppliers,
)


def test_create_supplier():
    s = Supplier(1, "АО ООН", "125678910")
    assert s.id == 1
    assert s.name == "АО ООН"
    assert s.inn == "125678910"
    assert "АО ООН" in str(s)


def test_add_supplier():
    suppliers = []
    s = add_supplier(suppliers, "АО ООН", "125678910")
    assert s.id == 1
    assert len(suppliers) == 1


def test_find_supplier_by_id():
    suppliers = []
    add_supplier(suppliers, "АО ООН", "125678910")
    assert find_supplier_by_id(suppliers, 1) is not None
    assert find_supplier_by_id(suppliers, 99) is None


def test_search_suppliers():
    suppliers = []
    add_supplier(suppliers, "АО ООН", "125678910")
    add_supplier(suppliers, "Ромашка", "987654321")
    assert len(search_suppliers(suppliers, "оон")) == 1
    assert len(search_suppliers(suppliers, "1256")) == 1


def test_update_supplier():
    suppliers = []
    s = add_supplier(suppliers, "АО ООН", "125678910")
    s.update(name="Новое имя")
    assert s.name == "Новое имя"
    assert s.inn == "125678910"


def test_delete_supplier_no_refs():
    suppliers = []
    add_supplier(suppliers, "АО ООН", "125678910")
    assert delete_supplier(suppliers, [], [], 1)
    assert suppliers == []