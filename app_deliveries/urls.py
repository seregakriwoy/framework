from django.urls import path
from . import views

urlpatterns = [
    path("", views.deliveries, name="deliveries"),
    path("filter/", views.deliveries_filter, name="deliveries_filter"),
    path("<int:delivery_id>/", views.delivery_detail,
         name="delivery_detail"),
]