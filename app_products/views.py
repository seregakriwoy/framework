"""Views приложения app_products."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from db.database import get_connection

def product_list(request: HttpRequest) -> HttpResponse:
    conn = get_connection()
    products = conn.execute("""
        SELECT p.id, p.name, p.price, p.stock, s.name AS supplier_name 
        FROM products p
        JOIN suppliers s ON p.supplier_id = s.id
        ORDER BY s.name, p.name;
    """).fetchall()
    conn.close()
    return render(request, "products/product_list.html", {"products": products})

def product_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    conn = get_connection()
    # Используем CASE для вычисления флага низкого остатка
    product = conn.execute("""
        SELECT p.id, p.name, p.price, p.stock, p.supplier_id, s.name AS supplier_name,
               CASE WHEN p.stock < 10 THEN 1 ELSE 0 END AS is_low_stock
        FROM products p
        JOIN suppliers s ON p.supplier_id = s.id
        WHERE p.id = ?;
    """, (product_id,)).fetchone()
    conn.close()

    return render(request, "products/product_detail.html", {"product": product},
                  status=404 if product is None else 200)

def product_statistics(request: HttpRequest) -> HttpResponse:
    conn = get_connection()
    stats = conn.execute("""
        SELECT s.name AS supplier_name, COUNT(p.id) AS product_count
        FROM suppliers s
        LEFT JOIN products p ON s.id = p.supplier_id
        GROUP BY s.id, s.name
        ORDER BY product_count DESC;
    """).fetchall()
    conn.close()
    return render(request, "products/statistics.html", {"stats": stats})