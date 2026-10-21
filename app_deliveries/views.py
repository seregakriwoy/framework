"""Views приложения app_deliveries."""
from datetime import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from db.database import get_connection

def delivery_list(request: HttpRequest) -> HttpResponse:
    conn = get_connection()
    deliveries = conn.execute("""
        SELECT d.id, d.delivery_date, d.status,
               d.supplier_id,          -- <-- добавили
               s.name AS supplier_name,
               c.number AS contract_number
        FROM deliveries d
        JOIN suppliers s ON d.supplier_id = s.id
        JOIN contracts c ON d.contract_id = c.id
        ORDER BY d.delivery_date DESC;
    """).fetchall()
    conn.close()
    return render(request, "deliveries/delivery_list.html", {"deliveries": deliveries})

def delivery_detail(request: HttpRequest, delivery_id: int) -> HttpResponse:
    conn = get_connection()
    delivery = conn.execute("""
        SELECT d.id, d.delivery_date, d.status, d.supplier_id, d.contract_id,
               s.name AS supplier_name, c.number AS contract_number
        FROM deliveries d
        JOIN suppliers s ON d.supplier_id = s.id
        JOIN contracts c ON d.contract_id = c.id
        WHERE d.id = ?;
    """, (delivery_id,)).fetchone()

    items = []
    total_sum = 0
    if delivery:
        # Вычисляем сумму (количество * цену) прямо в SQL
        items = conn.execute("""
            SELECT di.id, di.quantity, p.id AS product_id, p.name AS product_name, 
                   p.price, (di.quantity * p.price) AS amount
            FROM delivery_items di
            JOIN products p ON di.product_id = p.id
            WHERE di.delivery_id = ?;
        """, (delivery_id,)).fetchall()
        # Считаем общий итог
        total_sum = sum(item["amount"] for item in items)

    conn.close()

    context = {"delivery": delivery, "items": items, "total": total_sum}
    return render(request, "deliveries/delivery_detail.html", context,
                  status=404 if delivery is None else 200)

def delivery_filter(request: HttpRequest) -> HttpResponse:
    start_str = request.GET.get("start")
    end_str = request.GET.get("end")

    if not start_str or not end_str:
        return render(request, "deliveries/filter_error.html", status=400)

    try:
        datetime.strptime(start_str, "%Y-%m-%d")
        datetime.strptime(end_str, "%Y-%m-%d")
    except ValueError:
        return render(request, "deliveries/filter_error.html", status=400)

    conn = get_connection()
    result = conn.execute("""
        SELECT d.id, d.delivery_date, d.status, s.name AS supplier_name
        FROM deliveries d
        JOIN suppliers s ON d.supplier_id = s.id
        WHERE d.delivery_date BETWEEN ? AND ?
        ORDER BY d.delivery_date;
    """, (start_str, end_str)).fetchall()
    conn.close()

    return render(request, "deliveries/delivery_filter.html", {
        "start": start_str, "end": end_str, "deliveries": result
    })