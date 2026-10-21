"""Views приложения homepage: главная страница и 404."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница проекта."""
    return render(request, "homepage/index.html")


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    """Собственная страница 404."""
    return render(
        request,
        "homepage/404.html",
        status=404,
    )