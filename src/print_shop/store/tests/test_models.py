from django.test import TestCase
from store.models import Materials, Filament, Suppliers, RawMaterials, InventoryChange, Models, UserProfiles, Shipping, Orders, OrderItems, FulfillmentStatus

class MaterialsModelTestCase(TestCase):
    """Test case for the Materials model."""

    def setUp(self):
        """Set up a test material."""
        self.material = Materials.objects.create(Name="PLA")

    def test_material_creation(self):
        """Test that the material is created correctly."""
        self.assertEqual(self.material.Name, "PLA")
        self.assertEqual(str(Materials.objects.count()), "1")


class FilamentModelTestCase(TestCase):
    """Test case for the Filament model."""

    def setUp(self):
        """Set up a test filament."""
        self.material = Materials.objects.create(Name="PLA")
        self.filament = Filament.objects.create(
            Name="PLA Filament",
            Material=self.material,
            ColorHexCode="FF0000"
        )

    def test_filament_creation(self):
        """Test that the filament is created correctly."""
        self.assertEqual(self.filament.Name, "PLA Filament")
        self.assertEqual(self.filament.Material, self.material)
        self.assertEqual(self.filament.ColorHexCode, "FF0000")
        self.assertEqual(str(Filament.objects.count()), "1")

    def test_filament_relationship(self):
        """Test the relationship between Filament and Materials."""
        self.assertEqual(self.filament.Material.Name, "PLA")
        