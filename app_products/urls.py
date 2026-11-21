from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.product_list, name="list"),
    path("statistics/", views.product_statistics, name="statistics"),
    path("catalog/<int:product_id>/<str:slug>/", views.product_detail, name="card"),
    path("<int:product_id>/", views.product_detail, name="detail"),
    path("<int:product_id>/image/", views.product_image, name="image"),
]
