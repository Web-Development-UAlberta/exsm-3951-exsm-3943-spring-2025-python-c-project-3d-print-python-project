"""
3D Print Shop Models based on ERD
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, MinValueValidator
from django.db.models import Max, OuterRef, Subquery


class Materials(models.Model):
    """Parent table to store all material names for filament and resin"""

    Name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Name}"


class Filament(models.Model):
    """Child table to store all filament names and their properties - Parent to RawMaterials"""

    Name = models.CharField(max_length=255)
    Material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    ColorHexCode = models.CharField(
        max_length=6, validators=[RegexValidator(r"^[0-9A-Fa-f]{6}$")]
    )

    def __str__(self):
        return f"{self.Material.Name} - {self.ColorHexCode}"


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

    Supplier = models.ForeignKey(Suppliers, on_delete=models.PROTECT)
    Filament = models.ForeignKey(Filament, on_delete=models.PROTECT)
    BrandName = models.CharField(max_length=100, null=True)
    Cost = models.DecimalField(max_digits=10, decimal_places=2)
    MaterialWeightPurchased = models.IntegerField()
    MaterialDensity = models.DecimalField(max_digits=3, decimal_places=2)
    ReorderLeadTime = models.IntegerField()
    WearAndTearMultiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.00,
        validators=[MinValueValidator(1.00)],
    )
    PurchasedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Filament.Name} - {self.Filament.ColorHexCode} - {self.MaterialWeightPurchased}g"

    @property
    def current_inventory(self):
        """Get the most recent inventory level"""
        return self.inventorychange_set.order_by("-InventoryChangeDate").first()


class InventoryChange(models.Model):
    """Child table to store all inventory changes"""

    RawMaterial = models.ForeignKey(RawMaterials, on_delete=models.PROTECT)
    QuantityWeightAvailable = models.IntegerField()
    InventoryChangeDate = models.DateTimeField(auto_now_add=True)
    UnitCost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.RawMaterial.Filament.Name} - {self.QuantityWeightAvailable}g"

    @property
    def needs_reorder(self):
        """
        Check if current inventory level is below reorder threshold
        Threshold set to 20% of original amount
        """
        threshold = self.RawMaterial.MaterialWeightPurchased * 0.2
        return self.QuantityWeightAvailable < threshold


@receiver(post_save, sender=RawMaterials)
def create_or_update_initial_inventory(sender, instance, created, **kwargs):
    """
    Create initial inventory record when new raw material is added
    Update the initial inventory record when raw material is updated
    but only if there is only one inventory record for that raw material
    and there are no order items linked to that inventory record
    """
    if created:
        InventoryChange.objects.create(
            RawMaterial=instance,
            QuantityWeightAvailable=instance.MaterialWeightPurchased,
            UnitCost=instance.Cost / instance.MaterialWeightPurchased,
        )
    else:
        initial_inventory = (
            InventoryChange.objects.filter(RawMaterial=instance)
            .order_by("InventoryChangeDate")
            .first()
        )
        if initial_inventory:
            inventory_count = InventoryChange.objects.filter(
                RawMaterial=instance
            ).count()
            has_orders = OrderItems.objects.filter(
                InventoryChange__RawMaterial=instance
            ).exists()
            if inventory_count == 1 or not has_orders:
                initial_inventory.QuantityWeightAvailable = (
                    instance.MaterialWeightPurchased
                )
                initial_inventory.UnitCost = (
                    instance.Cost / instance.MaterialWeightPurchased
                )
                initial_inventory.save(
                    update_fields=["QuantityWeightAvailable", "UnitCost"]
                )


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

    def __str__(self):
        return f"{self.Name}"


class UserProfiles(models.Model):
    """Table to store all user profiles"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    Address = models.CharField(max_length=255)
    Phone = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update the user profile when the user is created or updated."""
    if created:
        UserProfiles.objects.create(user=instance)
    else:
        instance.user_profile.save()


class Shipping(models.Model):
    """Table to store all shipping information"""

    Name = models.CharField(max_length=255)
    Rate = models.DecimalField(max_digits=10, decimal_places=2)
    ShipTime = models.IntegerField()

    def __str__(self):
        return f"{self.Name} - {self.Rate} - {self.ShipTime} days"


class Orders(models.Model):
    """Table to store all orders"""

    User = models.ForeignKey(User, on_delete=models.PROTECT)
    Shipping = models.ForeignKey(Shipping, on_delete=models.PROTECT)
    TotalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    EstimatedShipDate = models.DateTimeField(null=True)
    ExpeditedService = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.User.username} - {self.CreatedAt} - {self.TotalPrice}"

    def save(self, *args, **kwargs):
        """Calculate total price before saving"""
        if self.pk:
            order_items = self.orderitems_set.all()
            items_total = sum(
                item.ItemPrice * item.ItemQuantity for item in order_items
            )
            shipping_cost = self.Shipping.Rate
            self.TotalPrice = items_total + shipping_cost
            if self.ExpeditedService:
                self.TotalPrice *= 1.5

        super().save(*args, **kwargs)


class OrderItems(models.Model):
    """Table to store all order items"""

    InventoryChange = models.ForeignKey(InventoryChange, on_delete=models.PROTECT)
    Order = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True, blank=True)
    Model = models.ForeignKey(Models, on_delete=models.PROTECT)
    InfillMultiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    TotalWeight = models.IntegerField()
    CostOfGoodsSold = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    Markup = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.15,
        validators=[MinValueValidator(1.00)],
    )
    ItemPrice = models.DecimalField(max_digits=10, decimal_places=2)
    ItemQuantity = models.IntegerField()
    IsCustom = models.BooleanField()

    def __str__(self):
        return f"{self.Model.Name} - {self.ItemQuantity}"

    def save(self, *args, **kwargs):
        """Calculate costs before saving"""
        cost_per_gram = self.InventoryChange.UnitCost
        density = self.InventoryChange.RawMaterial.MaterialDensity
        wear_tear = self.InventoryChange.RawMaterial.WearAndTearMultiplier
        volume_cm3 = (
            self.Model.EstimatedPrintVolume
            * self.Model.BaseInfill
            * self.InfillMultiplier
        )
        self.TotalWeight = int(volume_cm3 * density)
        material_cost = self.TotalWeight * cost_per_gram * wear_tear
        self.CostOfGoodsSold = self.Model.FixedCost + material_cost
        self.ItemPrice = self.CostOfGoodsSold * self.Markup

        super().save(*args, **kwargs)


@receiver(post_save, sender=OrderItems)
def create_inventory_change(sender, instance, created, **kwargs):
    """Create inventory change when order item is created"""
    if created:
        inventory = instance.InventoryChange
        new_quantity = inventory.QuantityWeightAvailable - instance.TotalWeight
        InventoryChange.objects.create(
            RawMaterial=inventory.RawMaterial,
            QuantityWeightAvailable=new_quantity,
            UnitCost=inventory.UnitCost,
        )


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
    # OrderStatus = Status.choices
    OrderStatus = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    StatusChangeDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.Order.User.username} - {self.OrderStatus} - {self.StatusChangeDate}"
        )
