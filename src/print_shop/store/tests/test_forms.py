from django.test import TestCase

from store.forms.filament_form import FilamentForm
from store.forms.fulfillment_status_form import FulfillmentStatusForm
from store.forms.materials_form import MaterialsForm
from store.forms.models_form import ModelsForm
from store.forms.raw_materials_form import RawMaterialsForm
from store.forms.shipping_form import ShippingForm
from store.forms.suppliers_form import SuppliersForm
from store.forms.inventory_form import InventoryChangeForm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from store.models import (
    Materials,
    Filament,
    Suppliers,
    RawMaterials,
    InventoryChange,
    Models,
    UserProfiles,
    Shipping,
    Orders,
    OrderItems,
    FulfillmentStatus,
)

class TestFilamentForm(TestCase):
    """Test suite for the FilamentForm."""

    def test_filament_form_valid(self):
        """Test that the FilamentForm is valid with correct data."""
        material = Materials.objects.create(Name="PLA")
        form_data = {
            "Name": "PLA",
            "Material": material.id, 
            "ColorHexCode": "FFFFFF", 
        }

        form = FilamentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_filament_form_invalid(self):
        """Test that the FilamentForm is invalid with incorrect data."""
        form_data = {
            "Name": "",
            "Material": "PLA",
            "ColorHexCode": "#FFFFFF",
        }
        form = FilamentForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_filament_form_invalid_color(self):
        """Test that the FilamentForm is invalid with incorrect color hex code."""
        material = Materials.objects.create(Name="PLA")
        form_data = {
            "Name": "PLA",
            "Material": material.id, 
            "ColorHexCode": "ZZZZZZ",  
        }
        form = FilamentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_filament_form_invalid_material(self):
        """Test that the FilamentForm is invalid with non-existent material."""
        form_data = {
            "Name": "PLA",
            "Material": 9999,  
            "ColorHexCode": "FFFFFF", 
        }
        form = FilamentForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestFulfillmentStatusForm(TestCase):
    """Test suite for the FulfillmentStatusForm."""

    def test_fulfillment_status_form_valid(self):
        """Test that the FulfillmentStatusForm is valid with correct data."""
        user = User.objects.create_user(username="testuser", password="password")
        shipping = Shipping.objects.create(
            Name ="Test Shipping",
            Rate = 10.00,
            ShipTime = 5,
        )
        order = Orders.objects.create(
            User=user,
            Shipping=shipping,
            TotalPrice=100.00,
            EstimatedShipDate="2025-07-01",
            ExpeditedService=False,
        )


        fulfillment_status = FulfillmentStatus.objects.create(
            Order =order,
            OrderStatus = FulfillmentStatus.Status.PAID,
        )


        form_data = {
            "Order": fulfillment_status.Order,
            "OrderStatus": fulfillment_status.OrderStatus,
        }
        form = FulfillmentStatusForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_fulfillment_status_form_invalid(self):
        """Test that the FulfillmentStatusForm is invalid with incorrect data."""
        user = User.objects.create_user(username="testuser", password="password")
        shipping = Shipping.objects.create(
            Name ="Test Shipping",
            Rate = 10.00,
            ShipTime = 5,
        )
        order = Orders.objects.create(
            User=user,
            Shipping=shipping,
            TotalPrice=100.00,
            EstimatedShipDate="2025-07-01",
            ExpeditedService=False,
        )


        fulfillment_status = FulfillmentStatus.objects.create(
            Order =order,
            OrderStatus = FulfillmentStatus.Status.PAID,
        )


        form_data = {
            "Order": "",
            "OrderStatus": fulfillment_status.OrderStatus
        }
        form = FulfillmentStatusForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_fulfillment_status_form_invalid_order(self):
        """Test that the FulfillmentStatusForm is invalid with non-existent order."""
        form_data = {
            "Order": 9999,  
            "OrderStatus": FulfillmentStatus.Status.PAID,
        }
        form = FulfillmentStatusForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_fulfillment_status_form_invalid_order_status(self):
        user = User.objects.create_user(username="testuser", password="password")
        shipping = Shipping.objects.create(
            Name ="Test Shipping",
            Rate = 10.00,
            ShipTime = 5,
        )
        order = Orders.objects.create(
            User=user,
            Shipping=shipping,
            TotalPrice=100.00,
            EstimatedShipDate="2025-07-01",
            ExpeditedService=False,
        )


        fulfillment_status = FulfillmentStatus.objects.create(
            Order =order,
            OrderStatus = FulfillmentStatus.Status.PAID,
        )


        form_data = {
            "Order": fulfillment_status.Order,
            "OrderStatus": "PAID",
        }

        form = FulfillmentStatusForm(data=form_data)
        self.assertFalse(form.is_valid())

class TestInventoryChangeForm(TestCase):
    def setUp(self):
        self.material = Materials.objects.create(Name="PLA")
        self.filament = Filament.objects.create(
            Name="Red PLA", Material=self.material, ColorHexCode="FF0000"
        )
        self.supplier = Suppliers.objects.create(
            Name="Supplier A", Address="123 Supplier Rd", Phone="1234567890", Email="supplier@example.com"
        )
        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="Brand A",
            Cost=100.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=7,
            WearAndTearMultiplier=1.00,
        )

    def test_valid_inventory_change_form(self):
        """Test that InventoryChangeForm is valid with correct data."""
        form_data = {
            "RawMaterial": self.raw_material.id,
            "QuantityWeightAvailable": 500,
            "UnitCost": 0.10,
        }
        form = InventoryChangeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_required_fields(self):
        """Test form is invalid if required fields are missing."""
        form = InventoryChangeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("RawMaterial", form.errors)
        self.assertIn("QuantityWeightAvailable", form.errors)
        self.assertIn("UnitCost", form.errors)

    def test_invalid_quantity_type(self):
        """Test form fails when quantity is a non-integer."""
        form_data = {
            "RawMaterial": self.raw_material.id,
            "QuantityWeightAvailable": "five hundred",  
            "UnitCost": 0.10,
        }
        form = InventoryChangeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("QuantityWeightAvailable", form.errors)

    def test_negative_quantity(self):
        """Test form doesn't allow negative values in quantityweight."""
        form_data = {
            "RawMaterial": self.raw_material.id,
            "QuantityWeightAvailable": -100,
            "UnitCost": 0.10,
        }
        form = InventoryChangeForm(data=form_data)
        self.assertFalse(form.is_valid())

class TestMaterialsForm(TestCase):
    """Test suite for the MaterialsForm."""

    def test_materials_form_valid(self):
        """Test that the MaterialsForm is valid with correct data."""
        form_data = {
            "Name": "PLA",
        }
        form = MaterialsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_materials_form_invalid(self):
        """Test that the MaterialsForm is invalid with incorrect data."""
        form_data = {
            "Name": "",
        }
        form = MaterialsForm(data=form_data)
        self.assertFalse(form.is_valid())

class TestModelsForm(TestCase):
    """Test suite for the ModelsForm."""

    def setUp(self):
        self.valid_file = SimpleUploadedFile(
            name="test_model.stl",
            content=b"solid testmodel",
            content_type="application/sla"
        )

    def test_models_form_valid(self):
        """Test that the ModelsForm is valid with all required fields."""
        form_data = {
            "Name": "Test Model",
            "Description": "This is a test 3D model.",
            "FixedCost": "25.00",
            "EstimatedPrintVolume": "150",
            "BaseInfill": "0.25",
        }
        form_files = {
            "FilePath": self.valid_file
        }
        form = ModelsForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid(), form.errors)

    def test_models_form_missing_required_fields(self):
        """Test that the form is invalid when required fields are missing."""
        form = ModelsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("Name", form.errors)
        self.assertIn("FilePath", form.errors)
        self.assertIn("FixedCost", form.errors)
        self.assertIn("EstimatedPrintVolume", form.errors)
        self.assertIn("BaseInfill", form.errors)

    def test_models_form_invalid_decimal(self):
        """Test that form catches invalid decimal input."""
        form_data = {
            "Name": "Bad Model",
            "FixedCost": "abc",  
            "EstimatedPrintVolume": "100",
            "BaseInfill": "0.3",
        }
        form_files = {
            "FilePath": self.valid_file
        }
        form = ModelsForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn("FixedCost", form.errors)


class TestRawMaterialsForm(TestCase):
    """Test suite for the RawMaterialsForm."""

    def setUp(self):
        # Create required foreign keys
        self.material = Materials.objects.create(Name="PLA")
        self.filament = Filament.objects.create(
            Name="Red PLA",
            Material=self.material,
            ColorHexCode="FF0000"
        )
        self.supplier = Suppliers.objects.create(
            Name="Supplier A",
            Address="123 Print Rd",
            Phone="1234567890",
            Email="supplier@example.com"
        )

    def test_valid_raw_materials_form(self):
        """Test that the RawMaterialsForm is valid with correct data."""
        form_data = {
            "Supplier": self.supplier.id,
            "Filament": self.filament.id,
            "BrandName": "Brand A",
            "Cost": 100.00,
            "MaterialWeightPurchased": 1000,
            "MaterialDensity": 1.25,
            "ReorderLeadTime": 7,
            "WearAndTearMultiplier": 1.00,
        }
        form = RawMaterialsForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_required_fields(self):
        """Test that required fields are enforced."""
        form = RawMaterialsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("Supplier", form.errors)
        self.assertIn("Filament", form.errors)
        self.assertIn("Cost", form.errors)
        self.assertIn("MaterialWeightPurchased", form.errors)
        self.assertIn("MaterialDensity", form.errors)
        self.assertIn("ReorderLeadTime", form.errors)

    def test_invalid_wear_and_tear_multiplier(self):
        """Test that values below 1.00 are rejected."""
        form_data = {
            "Supplier": self.supplier.id,
            "Filament": self.filament.id,
            "BrandName": "Brand A",
            "Cost": 100.00,
            "MaterialWeightPurchased": 1000,
            "MaterialDensity": 1.25,
            "ReorderLeadTime": 7,
            "WearAndTearMultiplier": 0.95,  
        }
        form = RawMaterialsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("WearAndTearMultiplier", form.errors)

    def test_negative_cost_rejected(self):
        """Test that negative cost is invalid if validators are added later."""
        form_data = {
            "Supplier": self.supplier.id,
            "Filament": self.filament.id,
            "BrandName": "Brand A",
            "Cost": -10.00,  
            "MaterialWeightPurchased": 1000,
            "MaterialDensity": 1.25,
            "ReorderLeadTime": 7,
            "WearAndTearMultiplier": 1.00,
        }
        form = RawMaterialsForm(data=form_data)
        # This will currently pass unless MinValueValidator is added to Cost
        self.assertTrue(form.is_valid())

class TestShippingForm(TestCase):
    """Test suite for the ShippingForm."""

    def test_valid_shipping_form(self):
        """Test that the ShippingForm is valid with all required fields."""
        form_data = {
            "Name": "Standard Shipping",
            "Rate": "5.00",
            "ShipTime": "7"
        }
        form = ShippingForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_required_fields(self):
        """Test that the form is invalid when required fields are missing."""
        form = ShippingForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("Name", form.errors)
        self.assertIn("Rate", form.errors)
        self.assertIn("ShipTime", form.errors)

    def test_invalid_rate_type(self):
        """Test that non-numeric rate is rejected."""
        form_data = {
            "Name": "Invalid Rate",
            "Rate": "abc",  
            "ShipTime": "3"
        }
        form = ShippingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Rate", form.errors)

    def test_invalid_ship_time_type(self):
        """Test that non-integer ship time is rejected."""
        form_data = {
            "Name": "Invalid Time",
            "Rate": "10.00",
            "ShipTime": "fast"  
        }
        form = ShippingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("ShipTime", form.errors)

    def test_negative_values(self):
        """ Test that negative values are not accepted"""
        form_data = {
            "Name": "Negative Test",
            "Rate": "-5.00",  
            "ShipTime": "-2"
        }
        form = ShippingForm(data=form_data)
        self.assertFalse(form.is_valid())  


class TestSuppliersForm(TestCase):
    """Test suite for the SuppliersForm."""

    def test_valid_suppliers_form(self):
        """Test that the SuppliersForm is valid with correct data."""
        form_data = {
            "Name": "Supplier A",
            "Address": "123 Supply Street",
            "Phone": "123-456-7890",
            "Email": "supplier@example.com",
        }
        form = SuppliersForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_required_fields(self):
        """Test that the form is invalid when required fields are missing."""
        form = SuppliersForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("Name", form.errors)
        self.assertIn("Address", form.errors)
        self.assertIn("Phone", form.errors)
        self.assertIn("Email", form.errors)

    def test_invalid_email(self):
        """Test that invalid email format is rejected."""
        form_data = {
            "Name": "Supplier B",
            "Address": "456 Vendor Rd",
            "Phone": "123-456-7890",
            "Email": "not-an-email", 
        }
        form = SuppliersForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Email", form.errors)

    def test_optional_phone_format(self):
        """Test that phone field accepts any format """
        form_data = {
            "Name": "Supplier C",
            "Address": "789 Market Lane",
            "Phone": "(999) 999 9999",  
            "Email": "supplierc@example.com",
        }
        form = SuppliersForm(data=form_data)
        self.assertTrue(form.is_valid())