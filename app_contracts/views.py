from datetime import timedelta

from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from models.contract import STATUS_ACTIVE
from .models import Contract


def contract_list(request):
    return render(request, "contracts/contract_list.html", {"contracts": Contract.objects.select_related("supplier")})


def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract.objects.select_related("supplier"), pk=contract_id)
    return render(request, "contracts/contract_detail.html", {"contract": contract})


def expiring_contracts(request):
    today = timezone.localdate()
    contracts = Contract.objects.select_related("supplier").filter(
        status=STATUS_ACTIVE, end_date__range=(today, today + timedelta(days=30))
    ).order_by("end_date", "pk")
    return render(request, "contracts/expiring.html", {"contracts": contracts})
