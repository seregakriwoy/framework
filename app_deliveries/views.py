"""Views приложения deliveries."""
from datetime import date, datetime

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from services import (
    find_delivery_by_id,
    filter_deliveries_by_date,
    get_delivery_history,
)
from storage import (
    load_contracts, load_deliveries, load_products, load_suppliers,
)


def _load_all():
    """Собрать все коллекции, соблюдая порядок связей."""
    suppliers = load_suppliers()
    contracts = load_contracts(suppliers)
    products = load_products(suppliers)
    deliveries = load_deliveries(suppliers, contracts, products)
    return suppliers, contracts, products, deliveries


def deliveries(request: HttpRequest) -> HttpResponse:
    """Страница /deliveries/: список поставок."""
    _, _, _, deliveries_list = _load_all()
    items = ""
    for d in deliveries_list:
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/deliveries/{d.id}/">
                Поставка №{d.id} от {d.delivery_date}
            </a>
            <span class="text-muted">{d.supplier.name}
                | {d.status} | {d.total():.2f} руб.</span>
        </li>"""
    content = f"""
    <h1>Поставки</h1>
    <ul class="list-group">
        {items or '<li class="list-group-item">Пусто</li>'}
    </ul>
    <form class="mt-3" method="get" action="/deliveries/filter/">
        <div class="row g-2 align-items-end">
            <div class="col-auto">
                <label class="form-label">Начало</label>
                <input type="date" name="start" class="form-control" required>
            </div>
            <div class="col-auto">
                <label class="form-label">Окончание</label>
                <input type="date" name="end" class="form-control" required>
            </div>
            <div class="col-auto">
                <button class="btn btn-primary" type="submit">
                    Показать в диапазоне
                </button>
            </div>
        </div>
    </form>
    """
    return HttpResponse(page("SupplyManager — поставки", content))


def delivery_detail(request: HttpRequest,
                    delivery_id: int) -> HttpResponse:
    """Страница /deliveries/<id>/: карточка поставки."""
    _, _, _, deliveries_list = _load_all()
    delivery = find_delivery_by_id(deliveries_list, delivery_id)
    if delivery is None:
        content = """
        <h1 class="text-danger">Поставка не найдена</h1>
        <a href="/deliveries/" class="btn btn-outline-secondary">
            ← к списку поставок
        </a>"""
        return HttpResponse(page("Поставка не найдена", content), status=404)

    badge_map = {
        "Создан": "bg-secondary",
        "Отправлен": "bg-info text-dark",
        "В пути": "bg-warning text-dark",
        "Принят": "bg-success",
        "Завершён": "bg-dark",
    }
    badge = badge_map.get(delivery.status, "bg-light text-dark")

    items_rows = "".join(
        f"<tr><td>{item.product.name}</td>"
        f"<td>{item.quantity}</td>"
        f"<td>{item.price:.2f}</td>"
        f"<td>{item.amount():.2f}</td></tr>"
        for item in delivery.items
    )

    content = f"""
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">Поставка №{delivery.id}</h5>
            <p class="card-text"><strong>Поставщик:</strong>
                <a href="/suppliers/{delivery.supplier.id}/">
                    {delivery.supplier.name}
                </a>
            </p>
            <p class="card-text"><strong>Договор:</strong>
                <a href="/contracts/{delivery.contract.id}/">
                    №{delivery.contract.number}
                </a>
            </p>
            <p class="card-text"><strong>Дата поставки:</strong>
                {delivery.delivery_date}</p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">{delivery.status}</span>
            </p>
            <a href="/deliveries/" class="btn btn-outline-secondary">
                ← к списку поставок
            </a>
        </div>
    </div>
    <h4>Позиции</h4>
    <table class="table">
        <thead><tr>
            <th>Товар</th><th>Кол-во</th><th>Цена</th><th>Сумма</th>
        </tr></thead>
        <tbody>{items_rows}</tbody>
        <tfoot><tr>
            <th colspan="3">Итого</th>
            <th>{delivery.total():.2f} руб.</th>
        </tr></tfoot>
    </table>
    """
    return HttpResponse(page(f"Поставка №{delivery.id}", content))


def deliveries_filter(request: HttpRequest) -> HttpResponse:
    """Страница /deliveries/filter/?start=...&end=...: фильтр по дате."""
    start_str = request.GET.get("start")
    end_str = request.GET.get("end")
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d").date()
        end = datetime.strptime(end_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        content = """
        <h1 class="text-danger">Неверные даты</h1>
        <a href="/deliveries/" class="btn btn-outline-secondary">
            ← к списку поставок
        </a>"""
        return HttpResponse(page("Неверные даты", content), status=400)

    _, _, _, deliveries_list = _load_all()
    result = filter_deliveries_by_date(deliveries_list, start, end)
    items = "".join(
        f'<li class="list-group-item">Поставка №{d.id} от {d.delivery_date} '
        f'— {d.supplier.name} ({d.status})</li>'
        for d in result
    ) or '<li class="list-group-item">Нет поставок в этом диапазоне</li>'
    content = f"""
    <h1>Поставки с {start} по {end}</h1>
    <ul class="list-group">{items}</ul>
    <a href="/deliveries/" class="btn btn-outline-secondary mt-3">
        ← к списку поставок
    </a>
    """
    return HttpResponse(page("Фильтр поставок", content))