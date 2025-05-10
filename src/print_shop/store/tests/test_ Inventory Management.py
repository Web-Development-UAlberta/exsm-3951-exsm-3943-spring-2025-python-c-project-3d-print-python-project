from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Materials, Filament, Suppliers, RawMaterials, InventoryChange

class InventoryManagementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin123")
        self.client.login(username="admin", password="admin123")

        self.material = Materials.objects.create(Name="ABS")
        self.filament = Filament.objects.create(Name="ABS Red", Material=self.material, ColorHexCode="FF0000")
        self.supplier = Suppliers.objects.create(Name="TestSupplier", Address="123 Main", Phone="1234567890", Email="test@supplier.com")

        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="MakerBrand",
            Cost=20.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=7
        )

        self.inventory = InventoryChange.objects.create(
            RawMaterial=self.raw_material,
            QuantityWeightAvailable=500,
            UnitCost=2.00
        )
    ##  Inventory View Loads
    def test_inventory_view_loads(self):
        response = self.client.get(reverse("inventory_management"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABS Red")

    ## Search Functionality
    def test_inventory_search_by_material_name(self):
        response = self.client.get(reverse("inventory_management"), {"search": "ABS"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABS")
        
    ## Filter Functionality
    def test_filter_by_material(self):
        response = self.client.get(reverse("inventory_management"), {"material": self.material.id})
        self.assertContains(response, "ABS")

    def test_filter_by_quantity_min(self):
        response = self.client.get(reverse("inventory_management"), {"min_quantity": 100})
        self.assertContains(response, "100")
        
    ## Actions: Edit / Delete
    def test_inventory_edit_view_exists(self):
        response = self.client.get(reverse("inventory_edit", args=[self.inventory.id]))
        self.assertEqual(response.status_code, 200)

    def test_inventory_delete_view_exists(self):
        response = self.client.post(reverse("inventory_delete", args=[self.inventory.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after delete
    
        
  
