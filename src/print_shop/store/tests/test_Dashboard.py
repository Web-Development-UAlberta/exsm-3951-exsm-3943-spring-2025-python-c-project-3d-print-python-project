from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from store.models import (
    Orders,
    OrderItems,
    Shipping,
    Materials,
    Models,
    InventoryChange,
    RawMaterials,
    Suppliers,
    Filament,
)


class DashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", is_staff=True
        )

        self.client.login(username="testuser", password="testpass")

        shipping = Shipping.objects.create(
            Name="Standard Shipping", Rate=5.99, ShipTime=3
        )

        order1 = Orders.objects.create(
            User=self.user,
            Shipping=shipping,
            TotalPrice=100.00,
            EstimatedShipDate=timezone.now() + timedelta(days=7),
            ExpeditedService=True,
        )
        order2 = Orders.objects.create(
            User=self.user,
            Shipping=shipping,
            TotalPrice=50.00,
            EstimatedShipDate=timezone.now() + timedelta(days=3),
            ExpeditedService=False,
        )

        material_pla = Materials.objects.create(Name="PLA")
        material_abs = Materials.objects.create(Name="ABS")

        filament_pla = Filament.objects.create(
            Name="PLA", ColorHexCode="FFFFFF", Material=material_pla
        )
        filament_abs = Filament.objects.create(
            Name="ABS", ColorHexCode="000000", Material=material_abs
        )

        supplier = Suppliers.objects.create(
            Name="Default Supplier",
            Address="123 Main St",
            Phone="1234567890",
            Email="test@supplier.com",
        )

        raw_material_pla = RawMaterials.objects.create(
            Supplier=supplier,
            Filament=filament_pla,
            BrandName="BrandX",
            Cost=Decimal("20.00"),
            MaterialWeightPurchased=1000,
            MaterialDensity=Decimal("1.24"),
            ReorderLeadTime=5,
            WearAndTearMultiplier=Decimal("1.05"),
        )
        raw_material_abs = RawMaterials.objects.create(
            Supplier=supplier,
            Filament=filament_abs,
            BrandName="BrandY",
            Cost=Decimal("22.00"),
            MaterialWeightPurchased=500,
            MaterialDensity=Decimal("1.04"),
            ReorderLeadTime=7,
            WearAndTearMultiplier=Decimal("1.10"),
        )

        inventory_change_pla = InventoryChange.objects.create(
            RawMaterial=raw_material_pla,
            UnitCost=Decimal("0.05"),
            QuantityWeightAvailable=99,
        )
        inventory_change_abs = InventoryChange.objects.create(
            RawMaterial=raw_material_abs,
            UnitCost=Decimal("0.07"),
            QuantityWeightAvailable=101,
        )

        model_a = Models.objects.create(
            Name="Widget A",
            BaseInfill=Decimal("0.20"),
            FixedCost=Decimal("2.00"),
            EstimatedPrintVolume=Decimal("100.0"),
        )
        model_b = Models.objects.create(
            Name="Widget B",
            BaseInfill=Decimal("0.25"),
            FixedCost=Decimal("1.50"),
            EstimatedPrintVolume=Decimal("120.0"),
        )
        model_c = Models.objects.create(
            Name="Widget C",
            BaseInfill=Decimal("0.30"),
            FixedCost=Decimal("1.75"),
            EstimatedPrintVolume=Decimal("90.0"),
        )

        OrderItems.objects.create(
            InventoryChange=inventory_change_pla,
            Order=order1,
            Model=model_a,
            InfillMultiplier=Decimal("1.0"),
            TotalWeight=200,
            CostOfGoodsSold=Decimal("20.00"),
            Markup=Decimal("1.15"),
            ItemPrice=Decimal("23.00"),
            ItemQuantity=2,
            IsCustom=False,
        )
        OrderItems.objects.create(
            InventoryChange=inventory_change_abs,
            Order=order1,
            Model=model_b,
            InfillMultiplier=Decimal("1.0"),
            TotalWeight=300,
            CostOfGoodsSold=Decimal("25.00"),
            Markup=Decimal("1.10"),
            ItemPrice=Decimal("27.50"),
            ItemQuantity=3,
            IsCustom=False,
        )
        OrderItems.objects.create(
            InventoryChange=inventory_change_pla,
            Order=order2,
            Model=model_c,
            InfillMultiplier=Decimal("1.0"),
            TotalWeight=100,
            CostOfGoodsSold=Decimal("10.00"),
            Markup=Decimal("1.20"),
            ItemPrice=Decimal("12.00"),
            ItemQuantity=1,
            IsCustom=False,
        )

    def test_dashboard_data(self):
        response = self.client.get(reverse("admin_dashboard"))
        print("Inventory warnings count:", response.context.get("inventory_warnings"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["total_orders"], 2)
        self.assertEqual(response.context["active_orders"], 2)
        self.assertEqual(response.context["inventory_warnings"], 2)
