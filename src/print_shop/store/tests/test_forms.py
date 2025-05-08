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

class InventoryChangeFormTest(TestCase):
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
        """Test form allows negative values if not explicitly restricted."""
        form_data = {
            "RawMaterial": self.raw_material.id,
            "QuantityWeightAvailable": -100,
            "UnitCost": 0.10,
        }
        form = InventoryChangeForm(data=form_data)
        self.assertTrue(form.is_valid())