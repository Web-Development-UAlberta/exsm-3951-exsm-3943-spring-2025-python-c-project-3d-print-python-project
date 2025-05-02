"""
3D Print Shop Models based on ERD
"""

from django.db import models


class Materials(models.Model):
    """Parent table to store all material names for filament and resin"""

    Name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Name}"


class Filament(models.Model):
    """Child table to store all filament names and their properties - Parent to RawMaterials"""

    Name = models.CharField(max_length=255)
    Material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    ColorHexCode = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.Name}, #{self.ColorHexCode} - {self.Material}"


class Suppliers(models.Model):
    """Parent table to store all suppliers"""

    Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=255)
    Phone = models.CharField(max_length=25)
    Email = models.EmailField(max_length=255)

    def __str__(self):
        return f"{self.Name}"


class RawMaterials(models.Model):
    """Child table to store all raw materials and their properties"""

    Supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    Filament = models.ForeignKey(Filament, on_delete=models.CASCADE)
    BrandName = models.CharField(max_length=100).null = True
    Cost = models.DecimalField(max_digits=10, decimal_places=2)
    MaterialWeightPurchased = models.IntegerField()
    MaterialDensity = models.DecimalField(3, 2)
    ReorderLeadTime = models.IntegerField()
    WearAndTearMultiplier = models.DecimalField(max_digits=3, decimal_places=2).default(
        1.00
    )
    PurchasedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Filament},${self.Cost} - {self.Supplier}, {self.MaterialWeightPurchased} grams"


class InventoryChange(models.Model):
    """Child table to store all inventory changes"""

    RawMaterial = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    QuantityWeightAvailbale = models.IntegerField()
    InventoryChangeDate = models.DateTimeField(auto_now_add=True)
    UnitCost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.RawMaterial} - {self.QuantityWeightAvailbale} grams at ${self.UnitCost}"


class Models(models.Model):
    """Table to store all models"""

    Name = models.CharField(max_length=255)
    Description = models.TextField()
    FilePath = models.FileField(upload_to="models/")
    Thumbnail = models.BinaryField().null = True
    FixedCost = models.DecimalField(max_digits=10, decimal_places=2)
    EstimatedPrintVolume = models.IntegerField()
    BaseInfill = models.DecimalField(max_digits=3, decimal_places=2)
    CreatedAt = models.DateTimeField(auto_now_add=True)
