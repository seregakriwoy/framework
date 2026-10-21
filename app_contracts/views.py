"""Views приложения app_contracts."""
from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from db.database import get_connection

def contract_list(request: HttpRequest) -> HttpResponse:
    """Страница /contracts/: список договоров."""
    conn = get_connection()
    contracts = conn.execute("""
        SELECT c.id, c.number, c.start_date, c.end_date, c.status, s.name AS supplier_name
        FROM contracts c
        JOIN suppliers s ON c.supplier_id = s.id
        ORDER BY c.start_date DESC;
    """).fetchall()
    conn.close()

    context = {"contracts": contracts}
    return render(request, "contracts/contract_list.html", context)


def contract_detail(request: HttpRequest, contract_id: int) -> HttpResponse:
    """Страница /contracts/<id>/: карточка договора."""
    conn = get_connection()
    contract = conn.execute("""
        SELECT c.id, c.number, c.start_date, c.end_date, c.status, s.name AS supplier_name, s.inn
        FROM contracts c
        JOIN suppliers s ON c.supplier_id = s.id
        WHERE c.id = ?;
    """, (contract_id,)).fetchone()
    conn.close()

    context = {"contract": contract}
    return render(
        request,
        "contracts/contract_detail.html",
        context,
        status=404 if contract is None else 200,
    )


def expiring_contracts(request: HttpRequest) -> HttpResponse:
    """Страница /contracts/expiring/: истекающие договоры (в течение 30 дней)."""
    conn = get_connection()

    # Вычисляем дату через 30 дней
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Параметризованный запрос с фильтрацией по датам
    contracts = conn.execute("""
        SELECT c.id, c.number, c.start_date, c.end_date, c.status, s.name AS supplier_name
        FROM contracts c
        JOIN suppliers s ON c.supplier_id = s.id
        WHERE c.end_date BETWEEN ? AND ?
        ORDER BY c.end_date ASC;
    """, (current_date, future_date)).fetchall()
    conn.close()

    context = {"contracts": contracts}
    return render(request, "contracts/expiring.html", context)