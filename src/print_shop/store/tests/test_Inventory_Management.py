from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Materials, Filament, Suppliers, RawMaterials, InventoryChange


class InventoryManagementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin123")
        self.user.is_staff = True
        self.user.save()
        self.client.login(username="admin", password="admin123")

        self.material = Materials.objects.create(Name="ABS")
        self.filament = Filament.objects.create(
            Name="ABS Red", Material=self.material, ColorHexCode="FF0000"
        )
        self.supplier = Suppliers.objects.create(
            Name="TestSupplier",
            Address="123 Main",
            Phone="1234567890",
            Email="test@supplier.com",
        )

        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="MakerBrand",
            Cost=20.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=7,
        )

        self.inventory = InventoryChange.objects.create(
            RawMaterial=self.raw_material, QuantityWeightAvailable=500, UnitCost=2.00
        )

    ##  Inventory View Loads
    def test_inventory_view_loads(self):
        response = self.client.get(reverse("current-inventory"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABS Red")

    ## Actions: Edit / Delete
    def test_inventory_edit_view_exists(self):
        response = self.client.get(
            reverse("edit-raw-material", args=[self.raw_material.id])
        )
        self.assertEqual(response.status_code, 200)
