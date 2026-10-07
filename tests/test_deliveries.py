from datetime import date

from models import (
    STATUS_CREATED, STATUS_IN_TRANSIT,
    Contract, DeliveryItem, Product, Supplier,
)
from services import (
    create_contract, create_delivery, find_delivery_by_id,
    filter_deliveries_by_date, get_delivery_history,
)


def _setup():
    supplier = Supplier(1, "АО ООН", "125678910")
    product = Product(1, "Болт", 12.5, supplier)
    contract = Contract(1, supplier, "Д-001",
                        date(2026, 1, 1), date(2027, 1, 1))
    return supplier, product, contract


def test_create_delivery():
    supplier, product, contract = _setup()
    deliveries = []
    items = [DeliveryItem(product, 100, 12.5)]
    d = create_delivery(deliveries, supplier, contract,
                        date(2026, 9, 30), items)
    assert d.id == 1
    assert d.status == STATUS_CREATED
    assert d.total() == 100 * 12.5


def test_change_status_only_forward():
    supplier, product, contract = _setup()
    deliveries = []
    items = [DeliveryItem(product, 100, 12.5)]
    d = create_delivery(deliveries, supplier, contract,
                        date(2026, 9, 30), items)
    assert d.change_status()                 # Создан -> Отправлен
    assert d.change_status()                 # Отправлен -> В пути
    assert d.status == STATUS_IN_TRANSIT
    assert not d.change_status("Создан")     # назад нельзя


def test_accept_increases_stock():
    supplier, product, contract = _setup()
    deliveries = []
    items = [DeliveryItem(product, 10, 5.0)]
    d = create_delivery(deliveries, supplier, contract,
                        date(2026, 9, 30), items)
    d.change_status()  # -> Отправлен
    d.change_status()  # -> В пути
    assert d.accept()
    assert product.stock == 10
    assert d.status == "Принят"


def test_history_and_filter():
    supplier, product, contract = _setup()
    deliveries = []
    d1 = create_delivery(deliveries, supplier, contract,
                         date(2026, 9, 10), [DeliveryItem(product, 1, 1.0)])
    d2 = create_delivery(deliveries, supplier, contract,
                         date(2026, 9, 20), [DeliveryItem(product, 1, 1.0)])
    history = get_delivery_history(deliveries)
    assert history[0] is d1 and history[1] is d2
    result = filter_deliveries_by_date(deliveries,
                                       date(2026, 9, 15), date(2026, 9, 25))
    assert result == [d2]