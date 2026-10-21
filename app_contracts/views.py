"""Views приложения app_contracts."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from services import find_contract_by_id, get_expiring_contracts
from storage import load_contracts, load_suppliers


def contract_list(request: HttpRequest) -> HttpResponse:
    """Страница /contracts/: список договоров."""
    suppliers = load_suppliers()
    contracts = load_contracts(suppliers)
    context = {"contracts": contracts}
    return render(request, "contracts/contract_list.html", context)


def contract_detail(request: HttpRequest,
                    contract_id: int) -> HttpResponse:
    """Страница /contracts/<id>/: карточка договора."""
    suppliers = load_suppliers()
    contracts = load_contracts(suppliers)
    contract = find_contract_by_id(contracts, contract_id)
    context = {"contract": contract}
    return render(
        request,
        "contracts/contract_detail.html",
        context,
        status=404 if contract is None else 200,
    )


def expiring_contracts(request: HttpRequest) -> HttpResponse:
    """Страница /contracts/expiring/: истекающие договоры."""
    suppliers = load_suppliers()
    contracts = load_contracts(suppliers)
    expiring = get_expiring_contracts(contracts, days=30)
    context = {"contracts": expiring}
    return render(request, "contracts/expiring.html", context)