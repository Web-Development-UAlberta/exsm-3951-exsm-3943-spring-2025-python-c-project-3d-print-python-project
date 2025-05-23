from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import InventoryChange
from store.models import Materials, Filament, Suppliers, RawMaterials


class InventoryManagementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='adminuser',
            password='testpassword123',
            is_staff=True,  # or is_superuser=True
        )
        self.client.login(username='adminuser', password='testpassword123')

        # Create material, filament, supplier, raw material, and inventory objects
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

    def test_inventory_view_loads(self):
        response = self.client.get(reverse("inventory_management"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABS Red")

    def test_inventory_search_by_material_name(self):
        response = self.client.get(reverse("inventory_management"), {"q": "ABS"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABS")

    def test_filter_by_material(self):
        response = self.client.get(
            reverse("inventory_management"), {"material": self.material.Name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABS")

    def test_filter_by_quantity_min(self):
        response = self.client.get(
            reverse("inventory_management"), {"quantity": 100}
        )
        self.assertEqual(response.status_code, 200)
        # The quantity in self.inventory is 500, so check for that
        self.assertContains(response, "500")

    def test_inventory_edit_view_exists(self):
        response = self.client.get(reverse("inventory_edit", args=[self.inventory.id]))
        self.assertEqual(response.status_code, 200)

    def test_inventory_delete_view_exists(self):
        response = self.client.post(reverse("inventory_delete", args=[self.inventory.id]))
        self.assertEqual(response.status_code, 302)
        # Confirm deletion
        exists = InventoryChange.objects.filter(id=self.inventory.id).exists()
        self.assertFalse(exists)
