import sqlite3
from contextlib import closing
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app_contracts.models import Contract
from app_deliveries.models import Delivery, DeliveryItem
from app_products.models import Product
from app_suppliers.models import Supplier


class Command(BaseCommand):
    help = "Переносит данные ПР7 в пустые предметные таблицы с сохранением ID."

    def add_arguments(self, parser):
        parser.add_argument("source", nargs="?", type=Path, default=settings.BASE_DIR / "data/supply_manager.sqlite")

    @transaction.atomic
    def handle(self, source, **options):
        tables = (
            ("suppliers", Supplier), ("products", Product), ("contracts", Contract),
            ("deliveries", Delivery), ("delivery_items", DeliveryItem),
        )
        if any(model.objects.exists() for _, model in tables):
            raise CommandError("Импорт возможен только в пустые предметные таблицы.")
        with closing(sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)) as db:
            db.row_factory = sqlite3.Row
            db.execute("BEGIN")
            for table, model in tables:
                rows = db.execute(f"SELECT * FROM {table} ORDER BY id")
                objects = [model(**dict(row)) for row in rows]
                model.objects.bulk_create(objects)
                self.stdout.write(f"{table}: {len(objects)}")
