from django.urls import path
from . import views

urlpatterns = [
    path("", views.contracts, name="contracts"),
    path("expiring/", views.expiring_contracts, name="contracts_expiring"),
    path("<int:contract_id>/", views.contract_detail,
         name="contract_detail"),
]