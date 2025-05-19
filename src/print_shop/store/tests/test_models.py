from django.test import TestCase
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
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import os
from decimal import Decimal


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
            Name="PLA Filament", Material=self.material, ColorHexCode="FF0000"
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

    def test_color_code_valid(self):
        """Test that the color hex code is valid."""
        filament = Filament.objects.create(
            Name="Green Filament", Material=self.material, ColorHexCode="00FF00"
        )
        self.assertEqual(filament.ColorHexCode, "00FF00")


class SuppliersModelTestCase(TestCase):
    """Test case for the Suppliers model."""

    def setUp(self):
        """Set up a test supplier."""
        self.supplier = Suppliers.objects.create(
            Name="Supplier A",
            Address="123 Supplier St.",
            Phone="123-456-7890",
            Email="info@3dprintsupplies.com",
        )

    def test_supplier_creation(self):
        """Test that the supplier is created correctly."""
        self.assertEqual(self.supplier.Name, "Supplier A")
        self.assertEqual(self.supplier.Address, "123 Supplier St.")
        self.assertEqual(self.supplier.Phone, "123-456-7890")
        self.assertEqual(
            self.supplier.Email,
            "info@3dprintsupplies.com",
        )
        self.assertEqual(str(Suppliers.objects.count()), "1")


class RawMaterialsModelTestCase(TestCase):
    """Test case for the RawMaterials model."""

    def setUp(self):
        """Set up a test raw material."""
        self.material = Materials.objects.create(Name="PLA")
        self.supplier = Suppliers.objects.create(
            Name="Supplier A",
            Address="123 Supplier St.",
            Phone="123-456-7890",
            Email="info@3dprintsupplies.com",
        )
        self.filament = Filament.objects.create(
            Name="PLA Filament", Material=self.material, ColorHexCode="FF0000"
        )

        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="Brand A",
            Cost=20.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=7,
            WearAndTearMultiplier=1.00,
        )

    def test_raw_material_creation(self):
        """Test that the raw material is created correctly."""
        self.assertEqual(self.raw_material.Supplier, self.supplier)
        self.assertEqual(self.raw_material.Filament, self.filament)
        self.assertEqual(self.raw_material.BrandName, "Brand A")
        self.assertEqual(self.raw_material.Cost, 20.00)
        self.assertEqual(self.raw_material.MaterialWeightPurchased, 1000)
        self.assertEqual(self.raw_material.MaterialDensity, 1.25)
        self.assertEqual(self.raw_material.ReorderLeadTime, 7)
        self.assertEqual(self.raw_material.WearAndTearMultiplier, 1.00)
        self.assertEqual(str(RawMaterials.objects.count()), "1")

    def test_raw_material_relationship(self):
        """Test the relationship between RawMaterials and Suppliers."""
        self.assertEqual(self.raw_material.Supplier.Name, "Supplier A")
        self.assertEqual(self.raw_material.Filament.Name, "PLA Filament")
        self.assertEqual(self.raw_material.Filament.Material.Name, "PLA")
        self.assertEqual(self.raw_material.Filament.ColorHexCode, "FF0000")


class InventoryChangeModelTestCase(TestCase):
    """Test case for the InventoryChange model."""

    def setUp(self):
        """Set up a test inventory change."""
        self.material = Materials.objects.create(Name="PLA")
        self.supplier = Suppliers.objects.create(
            Name="Supplier A",
            Address="123 Supplier St.",
            Phone="123-456-7890",
            Email="info@3dprintsupplies.com",
        )
        self.filament = Filament.objects.create(
            Name="PLA Filament", Material=self.material, ColorHexCode="FF0000"
        )
        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="Brand A",
            Cost=20.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=7,
            WearAndTearMultiplier=1.00,
        )
        self.inventory_change = InventoryChange.objects.create(
            RawMaterial=self.raw_material,
            QuantityWeightAvailable=500,
            UnitCost=20.00,
        )

    def test_inventory_change_creation(self):
        """Test that the inventory change is created correctly."""
        self.assertEqual(self.inventory_change.RawMaterial, self.raw_material)
        self.assertEqual(self.inventory_change.QuantityWeightAvailable, 500)
        self.assertEqual(self.inventory_change.UnitCost, 20.00)
        self.assertEqual(InventoryChange.objects.count(), 2)
        # test cases to confirm the latest inventory change is the one we just created
        latest_inventory = InventoryChange.objects.latest("InventoryChangeDate")
        # self.assertEqual(latest_inventory.QuantityWeightAvailable, 500)
        # self.assertEqual(latest_inventory.UnitCost, 20.00)

    def test_inventory_change_relationship(self):
        """Test the relationship between InventoryChange and RawMaterials."""
        self.assertEqual(self.inventory_change.RawMaterial.Supplier.Name, "Supplier A")
        self.assertEqual(
            self.inventory_change.RawMaterial.Filament.Name, "PLA Filament"
        )
        self.assertEqual(
            self.inventory_change.RawMaterial.Filament.Material.Name, "PLA"
        )
        self.assertEqual(
            self.inventory_change.RawMaterial.Filament.ColorHexCode, "FF0000"
        )


class ModelsModelTestCase(TestCase):
    """Test case for the Models model."""

    def setUp(self):
        """Set up a test model."""
        # Create a test STL file
        stl_file = SimpleUploadedFile(
            "test_model.stl", b"file_content", content_type="application/sla"
        )

        # Create a test image file for thumbnail
        image_file = SimpleUploadedFile(
            "test_thumbnail.png",
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82",
            content_type="image/png",
        )

        # Create a model with a thumbnail
        self.model_with_thumbnail = Models.objects.create(
            Name="3D Model With Thumbnail",
            FilePath=stl_file,
            Description="A test model with thumbnail",
            FixedCost=100.00,
            EstimatedPrintVolume=500,
            BaseInfill=0.2,
            Thumbnail=image_file,
        )

        # Create a model without a thumbnail
        stl_file2 = SimpleUploadedFile(
            "test_model2.stl", b"file_content", content_type="application/sla"
        )

        self.model_without_thumbnail = Models.objects.create(
            Name="3D Model Without Thumbnail",
            FilePath=stl_file2,
            Description=None,
            FixedCost=100.00,
            EstimatedPrintVolume=500,
            BaseInfill=0.2,
            Thumbnail=None,
        )

        # Clean up files after test
        self.files_to_clean = []
        if os.path.exists(self.model_with_thumbnail.FilePath.path):
            self.files_to_clean.append(self.model_with_thumbnail.FilePath.path)
        if os.path.exists(self.model_with_thumbnail.Thumbnail.path):
            self.files_to_clean.append(self.model_with_thumbnail.Thumbnail.path)
        if os.path.exists(self.model_without_thumbnail.FilePath.path):
            self.files_to_clean.append(self.model_without_thumbnail.FilePath.path)

    def test_model_creation(self):
        """Test that the model is created correctly."""
        self.assertEqual(self.model_with_thumbnail.Name, "3D Model With Thumbnail")
        self.assertEqual(self.model_with_thumbnail.FixedCost, 100.00)
        self.assertEqual(self.model_with_thumbnail.EstimatedPrintVolume, 500)
        self.assertEqual(self.model_with_thumbnail.BaseInfill, 0.2)
        self.assertEqual(Models.objects.count(), 2)

    def test_model_file_upload(self):
        """Test that the model file is uploaded correctly."""
        self.assertIn("test_model", self.model_with_thumbnail.FilePath.name)
        self.assertIn("test_model2", self.model_without_thumbnail.FilePath.name)

    def test_nullable_fields(self):
        """Test that nullable fields are handled correctly."""
        self.assertIsNone(self.model_without_thumbnail.Description)
        self.assertIsNone(self.model_without_thumbnail.Thumbnail.name)

    def test_thumbnail_field(self):
        """Test that the thumbnail field works correctly."""
        # Test that the thumbnail was saved
        self.assertIsNotNone(self.model_with_thumbnail.Thumbnail)
        self.assertIn("test_thumbnail", self.model_with_thumbnail.Thumbnail.name)
        self.assertTrue(
            self.model_with_thumbnail.Thumbnail.name.startswith("thumbnails/")
        )

    def tearDown(self):
        """Clean up after tests."""
        for file_path in self.files_to_clean:
            if os.path.exists(file_path):
                os.remove(file_path)


class UserProfilesModelTestCase(TestCase):
    """Test case for the UserProfiles model."""

    def setUp(self):
        """Set up a test user profile."""

        self.user = User.objects.create_user(
            username="johndoe", email="test@example.com", password="testpass123"
        )
        # Create a user profile for the test user
        self.user_profile = self.user.user_profile
        # Set some initial values for the user profile fields
        self.user_profile.Address = "123 Main St."
        self.user_profile.Phone = "123-456-7890"
        self.user_profile.save()

    def test_user_profile_creation(self):
        """Test that the user profile is created correctly."""
        self.assertTrue(isinstance(self.user_profile, UserProfiles))
        self.assertEqual(self.user_profile.Address, "123 Main St.")
        self.assertEqual(self.user_profile.Phone, "123-456-7890")
        self.assertEqual(str(UserProfiles.objects.count()), "1")


class ShippingModelTestCase(TestCase):
    """Test case for the Shipping model."""

    def setUp(self):
        """Set up a test shipping option."""
        self.shipping = Shipping.objects.create(
            Name="Standard Shipping",
            Rate=5.00,
            ShipTime=7,
        )

    def test_shipping_creation(self):
        """Test that the shipping option is created correctly."""
        self.assertEqual(self.shipping.Name, "Standard Shipping")
        self.assertEqual(self.shipping.Rate, 5.00)
        self.assertEqual(self.shipping.ShipTime, 7)
        self.assertEqual(str(Shipping.objects.count()), "1")


class OrdersModelTestCase(TestCase):
    """Test case for the Orders model."""

    def setUp(self):
        """Set up a test order."""
        self.user = User.objects.create_user(
            username="johndoe", email="johndoe@example.com", password="testpass123"
        )
        self.shipping = Shipping.objects.create(
            Name="Standard Shipping",
            Rate=5.00,
            ShipTime=7,
        )
        self.order = Orders.objects.create(
            User=self.user,
            Shipping=self.shipping,
            TotalPrice=100.00,
            EstimatedShipDate=None,
            ExpeditedService=False,
        )

    def test_order_creation(self):
        """Test that the order is created correctly."""
        self.assertEqual(self.order.User, self.user)
        self.assertEqual(self.order.Shipping, self.shipping)
        self.assertEqual(self.order.TotalPrice, 100.00)
        self.assertIsNone(self.order.EstimatedShipDate)
        self.assertFalse(self.order.ExpeditedService)
        self.assertEqual(str(Orders.objects.count()), "1")

    def test_order_relationship(self):
        """Test the relationship between Orders and User."""
        self.assertEqual(self.order.User.username, "johndoe")
        self.assertEqual(self.order.Shipping.Name, "Standard Shipping")

    def test_order_expedited_service(self):
        """Test that expedited service is handled correctly."""
        self.order.ExpeditedService = True
        self.order.save()
        self.assertTrue(self.order.ExpeditedService)


class OrderItemsModelTestCase(TestCase):
    """Test case for the OrderItems model."""

    def setUp(self):
        """Set up a test order item."""
        self.user = User.objects.create_user(
            username="johndoe",
            email="johndoe@example.com",
            password="testpass123",
        )
        self.shipping = Shipping.objects.create(
            Name="Standard Shipping",
            Rate=5.00,
            ShipTime=7,
        )
        self.order = Orders.objects.create(
            User=self.user,
            Shipping=self.shipping,
            TotalPrice=100.00,
            EstimatedShipDate=None,
            ExpeditedService=False,
        )
        self.material = Materials.objects.create(Name="PLA")
        self.supplier = Suppliers.objects.create(
            Name="Supplier A",
            Address="123 Supplier St.",
            Phone="123-456-7890",
            Email="supplier@supplier.com",
        )
        self.filament = Filament.objects.create(
            Name="PLA Filament", Material=self.material, ColorHexCode="FF0000"
        )
        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="Brand A",
            Cost=20.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=7,
            WearAndTearMultiplier=1.00,
        )
        self.inventory_change = InventoryChange.objects.create(
            RawMaterial=self.raw_material,
            QuantityWeightAvailable=500,
            UnitCost=20.00,
        )
        self.model = Models.objects.create(
            Name="3D Model",
            FilePath=SimpleUploadedFile(
                "test_model.stl", b"file_content", content_type="application/sla"
            ),
            Description=None,
            FixedCost=100.00,
            EstimatedPrintVolume=500,
            BaseInfill=0.2,
            Thumbnail=None,
        )
        self.order_item = OrderItems.objects.create(
            InventoryChange=self.inventory_change,
            Order=self.order,
            Model=self.model,
            InfillMultiplier=1.5,
            ItemQuantity=2,
            IsCustom=False,
        )

        if os.path.exists(self.model.FilePath.path):
            os.remove(self.model.FilePath.path)

    def test_order_item_creation(self):
        """Test that the order item is created correctly."""
        self.assertEqual(self.order_item.InventoryChange, self.inventory_change)
        self.assertEqual(self.order_item.Order, self.order)
        self.assertEqual(self.order_item.Model, self.model)
        self.assertEqual(self.order_item.InfillMultiplier, 1.5)

        # Use business logic to calculate expected values
        expected_volume_cm3 = (
            self.model.EstimatedPrintVolume
            * self.model.BaseInfill
            * self.order_item.InfillMultiplier
        )
        # Calculate weight for a single item, then multiply by quantity
        single_item_weight = int(
            expected_volume_cm3 * self.raw_material.MaterialDensity
        )
        expected_weight = single_item_weight * self.order_item.ItemQuantity
        expected_material_cost = (
            expected_weight
            * self.inventory_change.UnitCost
            * self.raw_material.WearAndTearMultiplier
        )
        expected_cogs = Decimal(str(self.model.FixedCost)) + Decimal(
            str(expected_material_cost)
        )
        expected_price = expected_cogs * Decimal(str(self.order_item.Markup))

        # Test that calculated fields match expected values
        self.assertEqual(self.order_item.TotalWeight, expected_weight)
        self.assertEqual(float(self.order_item.CostOfGoodsSold), float(expected_cogs))
        self.assertEqual(float(self.order_item.ItemPrice), float(expected_price))

        self.assertEqual(self.order_item.ItemQuantity, 2)
        self.assertFalse(self.order_item.IsCustom)

    def test_order_item_relationship(self):
        """Test the relationship between OrderItems and Orders."""
        self.assertEqual(self.order_item.Order.User.username, "johndoe")
        self.assertEqual(
            self.order_item.InventoryChange.RawMaterial.Filament.Name, "PLA Filament"
        )
        self.assertEqual(self.order_item.Model.Name, "3D Model")
        self.assertEqual(self.order_item.InventoryChange.QuantityWeightAvailable, 500)
        self.assertEqual(self.order_item.InventoryChange.UnitCost, 20.00)

    def test_order_item_is_custom(self):
        """Test that the IsCustom field is handled correctly."""
        self.order_item.IsCustom = True
        self.order_item.save()
        self.assertTrue(self.order_item.IsCustom)

    def test_order_item_quantity(self):
        """Test that the ItemQuantity field is handled correctly."""
        original_weight = self.order_item.TotalWeight
        original_cogs = self.order_item.CostOfGoodsSold
        original_price = self.order_item.ItemPrice
        original_quantity = self.order_item.ItemQuantity

        # Calculate expected new weight based on new quantity
        new_quantity = 5
        self.order_item.ItemQuantity = new_quantity
        self.order_item.save()

        # Calculate expected values after quantity change
        expected_volume_cm3 = (
            self.model.EstimatedPrintVolume
            * self.model.BaseInfill
            * self.order_item.InfillMultiplier
        )
        single_item_weight = int(
            expected_volume_cm3 * self.raw_material.MaterialDensity
        )
        expected_weight = single_item_weight * new_quantity
        expected_material_cost = (
            expected_weight
            * self.inventory_change.UnitCost
            * self.raw_material.WearAndTearMultiplier
        )
        expected_cogs = Decimal(str(self.model.FixedCost)) + Decimal(
            str(expected_material_cost)
        )
        expected_price = expected_cogs * Decimal(str(self.order_item.Markup))

        # Quantity change should affect calculated values
        self.assertEqual(self.order_item.ItemQuantity, new_quantity)
        self.assertEqual(self.order_item.TotalWeight, expected_weight)
        self.assertEqual(float(self.order_item.CostOfGoodsSold), float(expected_cogs))
        self.assertEqual(float(self.order_item.ItemPrice), float(expected_price))

        # Verify that values have changed from original
        self.assertNotEqual(self.order_item.TotalWeight, original_weight)
        self.assertNotEqual(self.order_item.CostOfGoodsSold, original_cogs)
        self.assertNotEqual(self.order_item.ItemPrice, original_price)

    def test_order_item_infill_multiplier(self):
        """Test that the InfillMultiplier field is handled correctly and recalculates dependent fields."""
        original_weight = self.order_item.TotalWeight
        original_cogs = self.order_item.CostOfGoodsSold
        original_price = self.order_item.ItemPrice

        # Change infill multiplier
        self.order_item.InfillMultiplier = 2.0
        self.order_item.save()

        # Calculate new expected values
        expected_volume_cm3 = (
            self.model.EstimatedPrintVolume
            * self.model.BaseInfill
            * self.order_item.InfillMultiplier
        )
        single_item_weight = int(
            expected_volume_cm3 * self.raw_material.MaterialDensity
        )
        expected_weight = single_item_weight * self.order_item.ItemQuantity
        expected_material_cost = (
            expected_weight
            * self.inventory_change.UnitCost
            * self.raw_material.WearAndTearMultiplier
        )
        expected_cogs = Decimal(str(self.model.FixedCost)) + Decimal(
            str(expected_material_cost)
        )
        expected_price = expected_cogs * Decimal(str(self.order_item.Markup))

        # Verify that changing infill multiplier affects calculated fields
        self.assertEqual(self.order_item.InfillMultiplier, 2.0)
        self.assertEqual(self.order_item.TotalWeight, expected_weight)
        self.assertEqual(float(self.order_item.CostOfGoodsSold), float(expected_cogs))
        self.assertEqual(float(self.order_item.ItemPrice), float(expected_price))

        # Verify that values have changed from original
        self.assertNotEqual(self.order_item.TotalWeight, original_weight)
        self.assertNotEqual(self.order_item.CostOfGoodsSold, original_cogs)
        self.assertNotEqual(self.order_item.ItemPrice, original_price)


class FulfillmentStatusModelTestCase(TestCase):
    """Test case for the FulfillmentStatus model."""

    def setUp(self):
        """Set up a test fulfillment status."""
        self.user = User.objects.create_user(
            username="johndoe",
            email="johndoe@example.com",
            password="testpass123",
        )
        self.shipping = Shipping.objects.create(
            Name="Standard Shipping",
            Rate=5.00,
            ShipTime=7,
        )
        self.order = Orders.objects.create(
            User=self.user,
            Shipping=self.shipping,
            TotalPrice=100.00,
            EstimatedShipDate=None,
            ExpeditedService=False,
        )
        self.fulfillment_status = FulfillmentStatus.objects.create(
            Order=self.order, OrderStatus=FulfillmentStatus.Status.PAID
        )

        self.fulfillment_status.save()

    def test_fulfillment_status_creation(self):
        """Test that the fulfillment status is created correctly."""
        self.assertEqual(self.fulfillment_status.Order, self.order)
        self.assertEqual(
            self.fulfillment_status.OrderStatus, FulfillmentStatus.Status.PAID
        )
        self.assertEqual(str(FulfillmentStatus.objects.count()), "1")

    def test_fulfillment_status_relationship(self):
        """Test the relationship between FulfillmentStatus and Orders."""
        self.assertEqual(self.fulfillment_status.Order.User.username, "johndoe")
        self.assertEqual(
            self.fulfillment_status.Order.Shipping.Name, "Standard Shipping"
        )
        self.assertEqual(self.fulfillment_status.Order.TotalPrice, 100.00)
