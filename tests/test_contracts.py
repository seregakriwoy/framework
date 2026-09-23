from datetime import date, timedelta

from contracts import (
    STATUS_ACTIVE, create_contract, get_expired_contracts,
)


def test_create_contract():
    contracts = []
    c = create_contract(contracts, 1, "Д-001",
                        date(2026, 1, 1), date(2027, 1, 1))
    assert c["id"] == 1
    assert c["status"] == STATUS_ACTIVE


def test_get_expiring_contracts():
    contracts = []
    soon = date.today() + timedelta(days=10)
    far = date.today() + timedelta(days=365)
    create_contract(contracts, 1, "Д-001", date.today(), soon)
    create_contract(contracts, 1, "Д-002", date.today(), far)
    assert len(get_expired_contracts(contracts, days=30)) == 1