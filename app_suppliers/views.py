"""Views приложения suppliers."""
from django.http import HttpRequest, HttpResponse

from homepage.views import page
from services import (
    find_supplier_by_id,
    get_products_by_supplier,
    search_suppliers,
)
from storage import load_products, load_suppliers


def suppliers(request: HttpRequest) -> HttpResponse:
    """Страница /suppliers/: список поставщиков."""
    items = ""
    for s in load_suppliers():
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/suppliers/{s.id}/">{s.name}</a>
            <span class="text-muted">ИНН: {s.inn}</span>
        </li>"""
    content = f"""
    <h1>Поставщики</h1>
    <ul class="list-group">{items or '<li class="list-group-item">Пусто</li>'}</ul>
    """
    return HttpResponse(page("SupplyManager — поставщики", content))


def supplier_detail(request: HttpRequest, supplier_id: int) -> HttpResponse:
    """Страница /suppliers/<id>/: карточка поставщика."""
    suppliers_list = load_suppliers()
    supplier = find_supplier_by_id(suppliers_list, supplier_id)
    if supplier is None:
        content = """
        <h1 class="text-danger">Поставщик не найден</h1>
        <a href="/suppliers/" class="btn btn-outline-secondary">
            ← к списку поставщиков
        </a>"""
        return HttpResponse(
            page("Поставщик не найден", content), status=404
        )

    products_list = load_products(suppliers_list)
    own_products = get_products_by_supplier(products_list, supplier)
    product_items = "".join(
        f'<li class="list-group-item">{p.name} — {p.price:.2f} руб.</li>'
        for p in own_products
    ) or '<li class="list-group-item">Нет товаров</li>'

    content = f"""
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">{supplier.name}</h5>
            <p class="card-text"><strong>ID:</strong> {supplier.id}</p>
            <p class="card-text"><strong>ИНН:</strong> {supplier.inn}</p>
            <p class="card-text"><strong>Дата регистрации:</strong>
                {supplier.created_at}</p>
            <a href="/suppliers/" class="btn btn-outline-secondary">
                ← к списку поставщиков
            </a>
        </div>
    </div>
    <h4>Товары поставщика</h4>
    <ul class="list-group">{product_items}</ul>
    """
    return HttpResponse(page(supplier.name, content))


def suppliers_search(request: HttpRequest) -> HttpResponse:
    """Страница /suppliers/search/?q=...: поиск поставщиков."""
    query = request.GET.get("q", "")
    results = search_suppliers(load_suppliers(), query) if query else []
    items = "".join(
        f'<li class="list-group-item">{s.name} (ИНН: {s.inn})</li>'
        for s in results
    ) or '<li class="list-group-item">Ничего не найдено</li>'
    content = f"""
    <h1>Поиск поставщиков</h1>
    <form class="mb-3" method="get">
        <div class="input-group">
            <input type="text" name="q" value="{query}"
                   class="form-control" placeholder="Название или ИНН">
            <button class="btn btn-primary" type="submit">Найти</button>
        </div>
    </form>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Поиск поставщиков", content))
