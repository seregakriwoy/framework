from django.urls import path
from . import views

urlpatterns = [
    path("", views.suppliers, name="suppliers"),
    path("search/", views.suppliers_search, name="suppliers_search"),
    path("<int:supplier_id>/", views.supplier_detail, name="supplier_detail"),
]