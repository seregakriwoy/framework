"""Views приложения products."""
from django.http import HttpRequest, HttpResponse

from homepage.views import page
from services import find_product_by_id
from storage import load_products, load_suppliers


def products(request: HttpRequest) -> HttpResponse:
    """Страница /products/: список товаров."""
    suppliers_list = load_suppliers()
    products_list = load_products(suppliers_list)
    items = ""
    for p in products_list:
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/products/{p.id}/">{p.name}</a>
            <span class="text-muted">
                {p.price:.2f} руб. | остаток: {p.stock}
            </span>
        </li>"""
    content = f"""
    <h1>Товары</h1>
    <ul class="list-group">
        {items or '<li class="list-group-item">Пусто</li>'}
    </ul>
    """
    return HttpResponse(page("SupplyManager — товары", content))


def product_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    """Страница /products/<id>/: карточка товара."""
    suppliers_list = load_suppliers()
    products_list = load_products(suppliers_list)
    product = find_product_by_id(products_list, product_id)
    if product is None:
        content = """
        <h1 class="text-danger">Товар не найден</h1>
        <a href="/products/" class="btn btn-outline-secondary">
            ← к списку товаров
        </a>"""
        return HttpResponse(page("Товар не найден", content), status=404)

    low = product.is_low_stock()
    badge = "bg-danger" if low else "bg-success"
    label = "низкий остаток" if low else "в наличии"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{product.name}</h5>
            <p class="card-text"><strong>ID:</strong> {product.id}</p>
            <p class="card-text"><strong>Цена:</strong>
                {product.price:.2f} руб.</p>
            <p class="card-text"><strong>Поставщик:</strong>
                <a href="/suppliers/{product.supplier.id}/">
                    {product.supplier.name}
                </a>
            </p>
            <p class="card-text">
                <strong>Остаток:</strong> {product.stock}
                <span class="badge {badge}">{label}</span>
            </p>
            <a href="/products/" class="btn btn-outline-secondary">
                ← к списку товаров
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(product.name, content))