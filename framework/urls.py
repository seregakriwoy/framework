"""Корневая маршрутизация проекта."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("suppliers/", include("app_suppliers.urls")),
    path("products/", include("app_products.urls")),
    path("contracts/", include("app_contracts.urls")),
    path("deliveries/", include("app_deliveries.urls")),
]

handler404 = "homepage.views.page_not_found"