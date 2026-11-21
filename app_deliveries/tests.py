from datetime import timedelta
from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from app_contracts.models import Contract
from app_products.models import Product
from app_suppliers.models import Supplier
from .models import Delivery, DeliveryStatus


class SupplyWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.day = timezone.localdate()
        cls.supplier = Supplier.objects.create(name="Север", inn="1234567890")
        cls.product = Product.objects.create(name="Кофе", price="12.50", supplier=cls.supplier)
        cls.contract = Contract.objects.create(
            supplier=cls.supplier, number="17", start_date=cls.day, end_date=cls.day + timedelta(days=90),
        )

    def payload(self):
        return {
            "supplier": self.supplier.pk, "contract": self.contract.pk, "delivery_date": self.day.isoformat(),
            "items-TOTAL_FORMS": 1, "items-INITIAL_FORMS": 0,
            "items-0-product": self.product.pk, "items-0-quantity": 2,
        }

    def create_order(self):
        response = self.client.post(reverse("deliveries:create"), self.payload())
        self.assertEqual(response.status_code, 302)
        return Delivery.objects.get()

    def test_edit_conflict_cancel_and_rebook(self):
        order = self.create_order()
        edit = reverse("deliveries:edit", args=[order.pk])
        data = self.payload()
        data.update({"items-INITIAL_FORMS": 1, "items-0-id": order.items.get().pk, "items-0-quantity": 3})
        self.assertEqual(self.client.post(edit, data).status_code, 302)
        self.assertEqual(order.items.get().quantity, 3)
        self.assertContains(self.client.post(reverse("deliveries:create"), self.payload()), "уже запланирована")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Delivery.objects.create(contract=self.contract, supplier=self.supplier, delivery_date=self.day)
        cancel = reverse("deliveries:cancel", args=[order.pk])
        self.assertEqual(self.client.get(cancel).status_code, 405)
        self.assertEqual(Client(enforce_csrf_checks=True).post(cancel).status_code, 403)
        self.assertEqual(self.client.post(cancel).status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, DeliveryStatus.CANCELLED)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(self.client.post(edit, data).status_code, 409)
        self.assertEqual(self.client.post(reverse("deliveries:create"), self.payload()).status_code, 302)

    def test_invalid_orders_do_not_save_partial_data(self):
        other = Supplier.objects.create(name="Другой", inn="999")
        other_product = Product.objects.create(name="Чай", price=20, supplier=other)
        for changes in (
            {"supplier": other.pk}, {"contract": 99999}, {"delivery_date": "ошибка"},
            {"delivery_date": self.day + timedelta(days=91)}, {"delivery_date": self.day - timedelta(days=1)},
            {"items-0-quantity": 0}, {"items-0-product": other_product.pk}, {"items-TOTAL_FORMS": 0},
        ):
            with self.subTest(changes=changes):
                response = self.client.post(reverse("deliveries:create"), self.payload() | changes)
                self.assertContains(response, "errorlist")
                self.assertFalse(Delivery.objects.exists())

    def test_filters_pagination_and_query_count(self):
        for offset in range(12):
            Delivery.objects.create(supplier=self.supplier, contract=self.contract, delivery_date=self.day + timedelta(days=offset))
        params = {"supplier": self.supplier.pk, "sort": "delivery_date"}
        response = self.client.get(reverse("deliveries:list"), params)
        self.assertContains(response, "sort=delivery_date&amp;page=2")
        self.assertEqual(response.context["deliveries"][0].delivery_date, self.day)
        second = self.client.get(reverse("deliveries:list"), params | {"page": 2})
        self.assertEqual(len(second.context["deliveries"]), 2)
        day = self.day.isoformat()
        daily = self.client.get(reverse("deliveries:filter"), {"start": day, "end": day})
        self.assertContains(daily, "Свободных договоров нет")
        self.assertEqual(self.client.get(reverse("deliveries:filter"), {"start": "?"}).status_code, 400)
        self.assertEqual(self.client.get(reverse("deliveries:detail", args=[99999])).status_code, 404)
        detail_url = reverse("deliveries:detail", args=[response.context["deliveries"][0].pk])
        with self.assertNumQueries(2):
            self.assertEqual(self.client.get(detail_url).status_code, 200)

    def test_admin_workflow_and_receipt(self):
        order = self.create_order()
        self.client.force_login(get_user_model().objects.create_superuser("tester"))
        url = reverse("admin:app_deliveries_delivery_changelist")
        for model in ("app_suppliers_supplier", "app_products_product", "app_contracts_contract", "app_deliveries_deliveryitem"):
            self.assertEqual(self.client.get(reverse(f"admin:{model}_changelist")).status_code, 200)
        self.assertContains(self.client.get(reverse("admin:app_contracts_contract_change", args=[self.contract.pk])), "Поставки")
        for status in (DeliveryStatus.SENT, DeliveryStatus.IN_TRANSIT, DeliveryStatus.ACCEPTED, DeliveryStatus.COMPLETED):
            self.client.post(url, {"action": "advance_status", "_selected_action": [order.pk]})
            order.refresh_from_db()
            self.assertEqual(order.status, status)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 2)

    def test_image_upload_and_slug(self):
        url = reverse("products:image", args=[self.product.pk])
        with TemporaryDirectory() as folder, self.settings(MEDIA_ROOT=folder):
            invalid = SimpleUploadedFile("bad.png", b"bad")
            self.assertContains(self.client.post(url, {"image": invalid}), "errorlist")
            buf = BytesIO()
            Image.new("RGB", (2, 2)).save(buf, "PNG")
            image = SimpleUploadedFile("coffee.png", buf.getvalue(), content_type="image/png")
            self.assertEqual(self.client.post(url, {"image": image}).status_code, 302)
            self.product.refresh_from_db()
            self.assertContains(self.client.get(self.product.get_absolute_url()), self.product.image.url)
            self.assertEqual(self.client.get(reverse("products:card", args=[self.product.pk, "wrong"])).status_code, 404)
