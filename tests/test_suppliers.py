from suppliers import (
    create_supplier, delete_supplier, get_supplier_by_id,
    search_suppliers, update_supplier,
)


def test_add_supplier():
    suppliers = []
    s = create_supplier(suppliers, "АО ООН", "125678910")
    assert s["id"] == 1
    assert len(suppliers) == 1


def test_find_supplier_by_id():
    suppliers = []
    create_supplier(suppliers, "АО ООН", "125678910")
    assert get_supplier_by_id(suppliers, 1) is not None
    assert get_supplier_by_id(suppliers, 99) is None


def test_search_suppliers_by_name():
    suppliers = []
    create_supplier(suppliers, "АО ООН", "125678910")
    create_supplier(suppliers, "Ромашка", "987654321")
    assert len(search_suppliers(suppliers, "оон")) == 1


def test_search_suppliers_by_inn():
    suppliers = []
    create_supplier(suppliers, "АО ООН", "125678910")
    assert len(search_suppliers(suppliers, "1256")) == 1


def test_update_supplier():
    suppliers = []
    create_supplier(suppliers, "АО ООН", "125678910")
    assert update_supplier(suppliers, 1, name="Новое имя")
    assert suppliers[0]["name"] == "Новое имя"


def test_delete_supplier():
    suppliers = []
    create_supplier(suppliers, "АО ООН", "125678910")
    assert delete_supplier(suppliers, 1)
    assert suppliers == []