# Generated by Django 5.2 on 2025-05-03 05:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="InventoryChange",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("QuantityWeightAvailable", models.IntegerField()),
                ("InventoryChangeDate", models.DateTimeField(auto_now_add=True)),
                ("UnitCost", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Materials",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Models",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=255)),
                ("Description", models.TextField(null=True)),
                ("FilePath", models.FileField(upload_to="models/")),
                ("Thumbnail", models.BinaryField(null=True)),
                ("FixedCost", models.DecimalField(decimal_places=2, max_digits=10)),
                ("EstimatedPrintVolume", models.IntegerField()),
                ("BaseInfill", models.DecimalField(decimal_places=2, max_digits=3)),
                ("CreatedAt", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Shipping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=255)),
                ("Rate", models.DecimalField(decimal_places=2, max_digits=10)),
                ("ShipTime", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Suppliers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=100)),
                ("Address", models.CharField(max_length=255)),
                ("Phone", models.CharField(max_length=25)),
                ("Email", models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Filament",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=255)),
                ("ColorHexCode", models.CharField(max_length=6)),
                (
                    "Material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.materials",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Orders",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("TotalPrice", models.DecimalField(decimal_places=2, max_digits=10)),
                ("CreatedAt", models.DateTimeField(auto_now_add=True)),
                ("EstimatedShipDate", models.DateTimeField(null=True)),
                ("ExpeditedService", models.BooleanField(default=False)),
                (
                    "User",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "Shipping",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.shipping"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItems",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "InfillMultiplier",
                    models.DecimalField(decimal_places=2, default=1.0, max_digits=3),
                ),
                ("TotalWeight", models.IntegerField()),
                (
                    "CostOfGoodsSold",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "Markup",
                    models.DecimalField(decimal_places=2, default=0.15, max_digits=3),
                ),
                ("ItemPrice", models.DecimalField(decimal_places=2, max_digits=10)),
                ("ItemQuantity", models.IntegerField()),
                ("IsCustom", models.BooleanField()),
                (
                    "InventoryChange",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.inventorychange",
                    ),
                ),
                (
                    "Model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.models"
                    ),
                ),
                (
                    "Order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.orders"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FulfillmentStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("StatusChangeDate", models.DateTimeField(auto_now_add=True)),
                (
                    "Order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.orders"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RawMaterials",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("BrandName", models.CharField(max_length=100, null=True)),
                ("Cost", models.DecimalField(decimal_places=2, max_digits=10)),
                ("MaterialWeightPurchased", models.IntegerField()),
                (
                    "MaterialDensity",
                    models.DecimalField(decimal_places=2, max_digits=3),
                ),
                ("ReorderLeadTime", models.IntegerField()),
                (
                    "WearAndTearMultiplier",
                    models.DecimalField(decimal_places=2, default=1.0, max_digits=3),
                ),
                ("PurchasedDate", models.DateTimeField(auto_now_add=True)),
                (
                    "Filament",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.filament"
                    ),
                ),
                (
                    "Supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.suppliers",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="inventorychange",
            name="RawMaterial",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="store.rawmaterials"
            ),
        ),
        migrations.CreateModel(
            name="UserProfiles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Address", models.CharField(max_length=255)),
                ("Phone", models.CharField(max_length=25)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
