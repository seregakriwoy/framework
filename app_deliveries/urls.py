from django.urls import path

from . import views

app_name = "deliveries"
urlpatterns = [
    path("", views.delivery_list, name="list"),
    path("filter/", views.delivery_list, name="filter"),
    path("create/", views.delivery_edit, name="create"),
    path("<int:delivery_id>/", views.delivery_detail, name="detail"),
    path("<int:delivery_id>/edit/", views.delivery_edit, name="edit"),
    path("<int:delivery_id>/cancel/", views.delivery_cancel, name="cancel"),
]
