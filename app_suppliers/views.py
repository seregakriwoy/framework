"""Views приложения app_suppliers."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from db.database import get_connection

def supplier_list(request: HttpRequest) -> HttpResponse:
    """Страница /suppliers/: список поставщиков."""
    conn = get_connection()
    suppliers = conn.execute("""
        SELECT id, name, inn, created_at 
        FROM suppliers 
        ORDER BY name;
    """).fetchall()
    conn.close()

    context = {"suppliers": suppliers}
    return render(request, "suppliers/supplier_list.html", context)


def supplier_detail(request: HttpRequest, supplier_id: int) -> HttpResponse:
    """Страница /suppliers/<id>/: карточка поставщика с его товарами."""
    conn = get_connection()

    # Получаем самого поставщика (параметризованный запрос)
    supplier = conn.execute("""
        SELECT id, name, inn, created_at 
        FROM suppliers 
        WHERE id = ?;
    """, (supplier_id,)).fetchone()

    products = []
    if supplier:
        # Получаем товары этого поставщика (связь через supplier_id)
        products = conn.execute("""
            SELECT id, name, price, stock 
            FROM products 
            WHERE supplier_id = ? 
            ORDER BY name;
        """, (supplier_id,)).fetchall()

    conn.close()

    return render(request, "suppliers/supplier_detail.html",
                  {"supplier": supplier, "products": products},
                  status=404 if supplier is None else 200)


def supplier_search(request: HttpRequest) -> HttpResponse:
    """Страница /suppliers/search/?q=...: поиск поставщиков."""
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        conn = get_connection()
        # Поиск по имени или ИНН с использованием LIKE
        results = conn.execute("""
            SELECT id, name, inn 
            FROM suppliers 
            WHERE name LIKE ? OR inn LIKE ?
            ORDER BY name;
        """, (f"%{query}%", f"%{query}%")).fetchall()
        conn.close()

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "suppliers/supplier_search.html", context)