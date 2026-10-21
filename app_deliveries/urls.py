from django.urls import path
from . import views

app_name = "deliveries"

urlpatterns = [
    path("", views.delivery_list, name="list"),
    path("filter/", views.delivery_filter, name="filter"),
    path("<int:delivery_id>/", views.delivery_detail, name="detail"),
]