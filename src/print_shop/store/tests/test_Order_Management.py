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
    Models,
)


class OrderManagementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin123")
        # Make the user a staff member to access admin views
        self.user.is_staff = True
        self.user.save()
        self.client.login(username="admin", password="admin123")

        # Create a 3D model
        self.model = Models.objects.create(
            Name="Test Cube",
            Description="A test cube model",
            FilePath="models/cube.stl",
            Thumbnail="thumbnails/cube.jpg",
            EstimatedPrintVolume=100,
            BaseInfill=0.3,
            FixedCost=3.00,
        )

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
        response = self.client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, 200)

    ##  Filter by Status, Material, Priority

    def test_filter_by_status(self):
        response = self.client.get(reverse("orders-list"), {"status": "Pending"})
        self.assertEqual(response.status_code, 200)

    def test_order_view_exists(self):
        response = self.client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, 200)

    def test_order_edit_exists(self):
        response = self.client.get(reverse("edit-order", args=[self.order.id]))
        self.assertEqual(response.status_code, 200)

    def test_order_delete_exists(self):
        response = self.client.post(reverse("delete-order", args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
