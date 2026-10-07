"""Views приложения homepage: главная страница и общий каркас."""
from django.http import HttpRequest, HttpResponse


BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
BOOTSTRAP_JS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
)


def page(title: str, content: str) -> str:
    """Единый HTML-каркас всех страниц проекта."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">SupplyManager</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/suppliers/">Поставщики</a>
                <a class="nav-link" href="/products/">Товары</a>
                <a class="nav-link" href="/contracts/">Договоры</a>
                <a class="nav-link" href="/deliveries/">Поставки</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {content}
    </main>
    <script src="{BOOTSTRAP_JS}"></script>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница проекта."""
    content = """
    <h1 class="display-4">SupplyManager</h1>
    <p class="lead">Система управления поставщиками, товарами,
    договорами и поставками.</p>
    <p>Основные разделы:</p>
    <a href="/suppliers/" class="btn btn-primary me-2">Поставщики</a>
    <a href="/products/" class="btn btn-primary me-2">Товары</a>
    <a href="/contracts/" class="btn btn-secondary me-2">Договоры</a>
    <a href="/deliveries/" class="btn btn-secondary">Поставки</a>
    """
    return HttpResponse(page("SupplyManager", content))


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    """Собственная страница 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )