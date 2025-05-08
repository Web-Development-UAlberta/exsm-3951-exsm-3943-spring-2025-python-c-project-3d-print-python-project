from django.test import TestCase

from store.forms.filament_form import FilamentForm
from store.forms.fulfillment_status_form import FulfillmentStatusForm
from store.forms.materials_form import MaterialsForm
from store.forms.models_form import ModelsForm
from store.forms.raw_materials_form import RawMaterialsForm
from store.forms.shipping_form import ShippingForm
from store.forms.suppliers_form import SuppliersForm
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