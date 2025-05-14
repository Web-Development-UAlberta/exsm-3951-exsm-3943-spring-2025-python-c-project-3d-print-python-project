from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import (
    Orders,
    OrderItems,
    InventoryChange,
    Materials,
    Filament,
    RawMaterials,
    Suppliers,
    Shipping,
)


class OrderManagementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin123")
        self.client.login(username="admin", password="admin123")

        self.material = Materials.objects.create(Name="PLA")
        self.filament = Filament.objects.create(
            Name="PLA Blue", Material=self.material, ColorHexCode="0000FF"
        )
        self.supplier = Suppliers.objects.create(
            Name="Test Supplier", Address="123 St", Phone="12345", Email="a@test.com"
        )
        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="BrandX",
            Cost=10.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=5,
        )
        self.inventory = InventoryChange.objects.create(
            RawMaterial=self.raw_material, QuantityWeightAvailable=500, UnitCost=2.00
        )
        self.shipping = Shipping.objects.create(Name="Standard", Rate=5.00, ShipTime=3)
        self.order = Orders.objects.create(
            User=self.user, Shipping=self.shipping, TotalPrice=50.00
        )
        OrderItems.objects.create(
            InventoryChange=self.inventory,
            Order=self.order,
            Model=self.model,
            InfillMultiplier=1.00,
            TotalWeight=100,
            CostOfGoodsSold=10.00,
            ItemPrice=20.00,
            ItemQuantity=2,
            IsCustom=False,
        )

    def test_order_list_view(self):
        response = self.client.get(reverse("order_management"))  # Adjust URL name
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.model.Name)

    ##  Filter by Status, Material, Priority

    def test_filter_by_status(self):
        response = self.client.get(reverse("order_management"), {"status": "Pending"})
        self.assertEqual(response.status_code, 200)

    def test_filter_by_material(self):
        response = self.client.get(reverse("order_management"), {"material": "PLA"})
        self.assertContains(response, "PLA")

    def test_filter_by_priority(self):
        # You’d need a priority field on Orders or OrderItems for this test to work
        response = self.client.get(reverse("order_management"), {"priority": "High"})
        self.assertEqual(response.status_code, 200)

    ## Search by Model Name or Order ID

    def test_search_model_name(self):
        response = self.client.get(reverse("order_management"), {"search": "Cube"})
        self.assertContains(response, "Cube")

    def test_search_order_id(self):
        response = self.client.get(
            reverse("order_management"), {"search": str(self.order.id)}
        )
        self.assertContains(response, str(self.order.id))

    ## Actions: View/Edit/Delete

    def test_order_view_exists(self):
        response = self.client.get(reverse("order_detail", args=[self.order.id]))
        self.assertEqual(response.status_code, 200)

    def test_order_edit_exists(self):
        response = self.client.get(reverse("order_edit", args=[self.order.id]))
        self.assertEqual(response.status_code, 200)

    def test_order_delete_exists(self):
        response = self.client.post(reverse("order_delete", args=[self.order.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after delete
