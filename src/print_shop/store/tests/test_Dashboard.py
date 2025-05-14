# dashboard/tests.py
from django.test import TestCase
from django.urls import reverse
from store.models import Order, Material


class DashboardTests(TestCase):
    def setUp(self):
        Order.objects.create(
            model_name="Widget A",
            material="PLA",
            quantity=2,
            status="Active",
            priority="High",
        )
        Order.objects.create(
            model_name="Widget B",
            material="ABS",
            quantity=3,
            status="Completed",
            priority="Low",
        )
        Material.objects.create(material_type="ABS", quantity=1, cost=15.0)
        Material.objects.create(material_type="PLA", quantity=10, cost=12.0)

    def test_dashboard_data(self):
        response = self.client.get(
            reverse("dashboard")
        )  # Make sure this URL name matches your `urls.py`
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_orders"], 2)
        self.assertEqual(response.context["active_orders"], 1)
        self.assertEqual(response.context["inventory_warnings"], 1)
