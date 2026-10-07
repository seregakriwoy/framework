"""Views приложения contracts."""
from datetime import date

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models import STATUS_ACTIVE
from services import find_contract_by_id, get_expiring_contracts
from storage import load_contracts, load_suppliers


def contracts(request: HttpRequest) -> HttpResponse:
    """Страница /contracts/: список договоров."""
    suppliers_list = load_suppliers()
    contracts_list = load_contracts(suppliers_list)
    items = ""
    for c in contracts_list:
        badge = {
            "активен": "bg-success",
            "истёк": "bg-warning text-dark",
            "расторгнут": "bg-secondary",
        }.get(c.status, "bg-light text-dark")
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/contracts/{c.id}/">№{c.number}
                ({c.supplier.name})</a>
            <span class="badge {badge}">{c.status}</span>
        </li>"""
    content = f"""
    <h1>Договоры</h1>
    <ul class="list-group">
        {items or '<li class="list-group-item">Пусто</li>'}
    </ul>
    <p class="mt-3">
        <a href="/contracts/expiring/" class="btn btn-outline-warning">
            Истекающие договоры
        </a>
    </p>
    """
    return HttpResponse(page("SupplyManager — договоры", content))


def contract_detail(request: HttpRequest, contract_id: int) -> HttpResponse:
    """Страница /contracts/<id>/: карточка договора."""
    suppliers_list = load_suppliers()
    contracts_list = load_contracts(suppliers_list)
    contract = find_contract_by_id(contracts_list, contract_id)
    if contract is None:
        content = """
        <h1 class="text-danger">Договор не найден</h1>
        <a href="/contracts/" class="btn btn-outline-secondary">
            ← к списку договоров
        </a>"""
        return HttpResponse(page("Договор не найден", content), status=404)

    active = contract.is_active()
    badge = "bg-success" if active else "bg-secondary"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Договор №{contract.number}</h5>
            <p class="card-text"><strong>ID:</strong> {contract.id}</p>
            <p class="card-text"><strong>Поставщик:</strong>
                <a href="/suppliers/{contract.supplier.id}/">
                    {contract.supplier.name}
                </a>
            </p>
            <p class="card-text"><strong>Период:</strong>
                {contract.start_date} — {contract.end_date}</p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">{contract.status}</span>
            </p>
            <a href="/contracts/" class="btn btn-outline-secondary">
                ← к списку договоров
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Договор №{contract.number}", content))


def expiring_contracts(request: HttpRequest) -> HttpResponse:
    """Страница /contracts/expiring/: истекающие договоры."""
    suppliers_list = load_suppliers()
    contracts_list = load_contracts(suppliers_list)
    expiring = get_expiring_contracts(contracts_list, days=30)
    items = "".join(
        f'<li class="list-group-item">№{c.number} ({c.supplier.name}) — '
        f'до {c.end_date}</li>'
        for c in expiring
    ) or '<li class="list-group-item">Нет истекающих договоров</li>'
    content = f"""
    <h1>Истекающие договоры (ближайшие 30 дней)</h1>
    <ul class="list-group">{items}</ul>
    <a href="/contracts/" class="btn btn-outline-secondary mt-3">
        ← к списку договоров
    </a>
    """
    return HttpResponse(page("Истекающие договоры", content))