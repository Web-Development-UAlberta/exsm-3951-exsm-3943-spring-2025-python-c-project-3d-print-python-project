"""
3D Print Shop Models based on ERD
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Materials(models.Model):
    """Parent table to store all material names for filament and resin"""

    Name = models.CharField(max_length=100)


class Filament(models.Model):
    """Child table to store all filament names and their properties - Parent to RawMaterials"""

    Name = models.CharField(max_length=255)
    Material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    ColorHexCode = models.CharField(max_length=6)


class Suppliers(models.Model):
    """Parent table to store all suppliers"""

    Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=255)
    Phone = models.CharField(max_length=25)
    Email = models.EmailField(max_length=255)


class RawMaterials(models.Model):
    """Child table to store all raw materials and their properties"""

    Supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    Filament = models.ForeignKey(Filament, on_delete=models.CASCADE)
    BrandName = models.CharField(max_length=100, null=True)
    Cost = models.DecimalField(max_digits=10, decimal_places=2)
    MaterialWeightPurchased = models.IntegerField()
    MaterialDensity = models.DecimalField(max_digits=3, decimal_places=2)
    ReorderLeadTime = models.IntegerField()
    WearAndTearMultiplier = models.DecimalField(
        max_digits=3, decimal_places=2, default=1.00
    )
    PurchasedDate = models.DateTimeField(auto_now_add=True)


class InventoryChange(models.Model):
    """Child table to store all inventory changes"""

    RawMaterial = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    QuantityWeightAvailable = models.IntegerField()
    InventoryChangeDate = models.DateTimeField(auto_now_add=True)
    UnitCost = models.DecimalField(max_digits=10, decimal_places=2)


class Models(models.Model):
    """Table to store all models"""

    Name = models.CharField(max_length=255)
    Description = models.TextField(null=True)
    FilePath = models.FileField(upload_to="models/")
    Thumbnail = models.BinaryField(null=True)
    FixedCost = models.DecimalField(max_digits=10, decimal_places=2)
    EstimatedPrintVolume = models.IntegerField()
    BaseInfill = models.DecimalField(max_digits=3, decimal_places=2)
    CreatedAt = models.DateTimeField(auto_now_add=True)


class UserProfiles(models.Model):
    """Table to store all user profiles"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    Address = models.CharField(max_length=255)
    Phone = models.CharField(max_length=25)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update the user profile when the user is created or updated."""
    if created:
        UserProfiles.objects.create(user=instance)
    else:
        instance.profile.save()


class Shipping(models.Model):
    """Table to store all shipping information"""

    Name = models.CharField(max_length=255)
    Rate = models.DecimalField(max_digits=10, decimal_places=2)
    ShipTime = models.IntegerField()


class Orders(models.Model):
    """Table to store all orders"""

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    TotalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    EstimatedShipDate = models.DateTimeField(null=True)
    ExpeditedService = models.BooleanField(default=False)


class OrderItems(models.Model):
    """Table to store all order items"""

    InventoryChange = models.ForeignKey(InventoryChange, on_delete=models.CASCADE)
    Order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    Model = models.ForeignKey(Models, on_delete=models.CASCADE)
    InfillMultiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    TotalWeight = models.IntegerField()
    CostOfGoodsSold = models.DecimalField(max_digits=10, decimal_places=2)
    Markup = models.DecimalField(max_digits=3, decimal_places=2, default=0.15)
    ItemPrice = models.DecimalField(max_digits=10, decimal_places=2)
    ItemQuantity = models.IntegerField()
    IsCustom = models.BooleanField()


class FulfillmentStatus(models.Model):
    """Table to store all fulfillment status"""

    class Status(models.TextChoices):
        """Enum for order status"""

        DRAFT = "Draft", "Draft"
        PENDING_PAYMENT = "Pending", "Pending"
        PAID = "Paid", "Paid"
        PRINTING = "Printing", "Printing"
        SHIPPED = "Shipped", "Shipped"
        CANCELED = "Canceled", "Canceled"
        REFUNDED = "Refunded", "Refunded"

    Order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    OrderStatus = Status.choices
    StatusChangeDate = models.DateTimeField(auto_now_add=True)
