from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
