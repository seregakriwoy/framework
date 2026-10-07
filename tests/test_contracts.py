from datetime import date, timedelta

from models import STATUS_ACTIVE, Contract, Supplier
from services import (
    create_contract, delete_contract, find_contract_by_id,
    get_expiring_contracts,
)


def _make_supplier() -> Supplier:
    return Supplier(1, "АО ООН", "125678910")


def test_create_contract():
    c = Contract(1, _make_supplier(), "Д-001",
                 date(2026, 1, 1), date(2027, 1, 1))
    assert c.id == 1
    assert c.status == STATUS_ACTIVE


def test_change_status():
    c = Contract(1, _make_supplier(), "Д-001",
                 date(2026, 1, 1), date(2027, 1, 1))
    assert c.change_status("истёк")
    assert not c.change_status("несуществующий")


def test_terminate():
    c = Contract(1, _make_supplier(), "Д-001",
                 date(2026, 1, 1), date(2027, 1, 1))
    c.terminate()
    assert c.status == "расторгнут"


def test_get_expiring_contracts():
    contracts = []
    s = _make_supplier()
    soon = date.today() + timedelta(days=10)
    far = date.today() + timedelta(days=365)
    create_contract(contracts, s, "Д-001", date.today(), soon)
    create_contract(contracts, s, "Д-002", date.today(), far)
    assert len(get_expiring_contracts(contracts, days=30)) == 1


def test_delete_contract_no_refs():
    contracts = []
    s = _make_supplier()
    create_contract(contracts, s, "Д-001",
                    date(2026, 1, 1), date(2027, 1, 1))
    assert delete_contract(contracts, [], 1)
    assert contracts == []