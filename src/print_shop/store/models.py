"""
3D Print Shop Models based on ERD
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    FileExtensionValidator,
)
from django.core.exceptions import ValidationError


class Materials(models.Model):
    """Parent table to store all material names for filament and resin"""

    Name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Name}"


class Filament(models.Model):
    """
    Child table of Materials to store all filament names and their properties
    Parent to RawMaterials
    """

    Name = models.CharField(max_length=255)
    Material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    ColorHexCode = models.CharField(
        max_length=6,
        validators=[RegexValidator(r"^[0-9A-Fa-f]{6}$")],
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
    """
    Child table to store all raw materials and their properties
    Parent to Inventory change, when a new raw material is added
    it will create an inventory change record
    and set the quantity available to the amount purchased
    and the unit cost to the cost per gram
    This will be used to track the inventory of raw materials
    and to calculate the cost of goods sold for each order item.
    Inventory follows a First In First Out (FIFO) principle
    """

    Supplier = models.ForeignKey(Suppliers, on_delete=models.PROTECT)
    Filament = models.ForeignKey(Filament, on_delete=models.PROTECT)
    BrandName = models.CharField(max_length=100, null=True)
    Cost = models.DecimalField(max_digits=10, decimal_places=2)
    MaterialWeightPurchased = models.IntegerField()
    MaterialDensity = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
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
        """
        Get available inventory following FIFO principle for this specific material.
        Uses the InventoryChangeManager's available method but filters for this material.
        """
        return InventoryChange.objects.available().filter(RawMaterial=self).first()

    def find_inventory_for_weight(self, required_weight, safety_margin=1.15):
        """
        Find inventory with enough material for the required weight (with safety margin).
        Uses the InventoryChangeManager's logic but filters for this specific material.
        """
        return InventoryChange.objects.find_for_weight(
            required_weight=required_weight,
            safety_margin=safety_margin,
            raw_material=self,
        )


class InventoryChangeManager(models.Manager):
    """Custom manager for InventoryChange to handle FIFO inventory queries"""

    def available(self):
        """Get all available inventory following FIFO principles"""
        return self.filter(QuantityWeightAvailable__gt=0).order_by(
            "RawMaterial__PurchasedDate", "-InventoryChangeDate"
        )

    def find_for_weight(self, required_weight, safety_margin=1.15, raw_material=None):
        """Find inventory with enough material for the required weight

        Args:
            required_weight: The weight needed for the order
            safety_margin: Multiplier for safety margin (default: 1.15 for 15%)
            raw_material: Optional RawMaterials instance to filter by specific material

        Returns:
            InventoryChange object with enough material, or None if not found
        """
        weight_with_margin = required_weight * safety_margin
        available_inventory = self.available()

        if raw_material:
            available_inventory = available_inventory.filter(RawMaterial=raw_material)

        for inventory in available_inventory:
            if inventory.QuantityWeightAvailable >= weight_with_margin:
                return inventory
        return None


class InventoryChange(models.Model):
    """Child table to store all inventory changes"""

    RawMaterial = models.ForeignKey(RawMaterials, on_delete=models.PROTECT)
    QuantityWeightAvailable = models.IntegerField(validators=[MinValueValidator(0)])
    InventoryChangeDate = models.DateTimeField(auto_now_add=True)
    UnitCost = models.DecimalField(max_digits=10, decimal_places=2)
    objects = InventoryChangeManager()

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
    """Parent table to store all models"""

    Name = models.CharField(max_length=255)
    Description = models.TextField(null=True)
    FilePath = models.FileField(
        upload_to="models/",
        validators=[
            FileExtensionValidator(allowed_extensions=["stl", "obj", "3mf", "amf"])
        ],
    )
    Thumbnail = models.BinaryField(null=True)
    FixedCost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=3.00,
    )
    EstimatedPrintVolume = models.IntegerField()
    BaseInfill = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.3,
    )
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
    """
    Create or update the user profile when the user is created or updated.
    By adding UserProfile as a one-to-one field to the User model,
    it keeps authentication separate from the user profile but allows us to access it easily.
    """
    if created:
        UserProfiles.objects.create(user=instance)
    else:
        instance.user_profile.save()


class Shipping(models.Model):
    """Parent table to store all shipping information"""

    Name = models.CharField(max_length=255)
    Rate = models.DecimalField(max_digits=10, decimal_places=2)
    ShipTime = models.IntegerField(validators=[MinValueValidator(0)])

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
    ItemPrice = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    ItemQuantity = models.IntegerField(validators=[MinValueValidator(0)])
    IsCustom = models.BooleanField()

    def clean(self):
        """
        Ensure item price is not below cost of goods sold
        """
        if self.ItemPrice is not None and self.CostOfGoodsSold is not None:
            if self.ItemPrice < self.CostOfGoodsSold:
                raise ValidationError(
                    {"ItemPrice": "Item price cannot be less than the cost of goods sold."}
                )
        super().clean()
       
        
    def __str__(self):
        return f"{self.Model.Name} - {self.ItemQuantity}"

    def calculate_required_weight(self):
        """
        Calculate the required weight for the order item based on model, infill, and quantity.
        This is used for inventory validation before saving.
        Returns the total weight required for this order item in grams
        """
        density = self.InventoryChange.RawMaterial.MaterialDensity
        volume_cm3 = (
            self.Model.EstimatedPrintVolume
            * self.Model.BaseInfill
            * self.InfillMultiplier
        )
        return int(volume_cm3 * density) * self.ItemQuantity

    def save(self, *args, **kwargs):
        """
        Override save to calculate costs before saving.
        Cost of goods sold is calculated as:
        TotalWeight = Volume * Base infill * Infill multiplier * Material density * Quantity
        MaterialCost = TotalWeight * cost per gram * wear and tear
        CostOfGoodsSold = Fixed cost + material cost
        Item price = Cost of goods sold * markup
        """
        self.TotalWeight = self.calculate_required_weight()
        cost_per_gram = self.InventoryChange.UnitCost
        wear_tear = self.InventoryChange.RawMaterial.WearAndTearMultiplier
        material_cost = self.TotalWeight * cost_per_gram * wear_tear
        self.CostOfGoodsSold = self.Model.FixedCost + material_cost
        self.ItemPrice = self.CostOfGoodsSold * self.Markup

        super().save(*args, **kwargs)


@receiver(post_save, sender=OrderItems)
def create_inventory_change(sender, instance, created, **kwargs):
    """
    Create inventory change when order item is created
    """
    if created:
        inventory = instance.InventoryChange
        new_quantity = inventory.QuantityWeightAvailable - instance.TotalWeight
        InventoryChange.objects.create(
            RawMaterial=inventory.RawMaterial,
            QuantityWeightAvailable=new_quantity,
            UnitCost=inventory.UnitCost,
        )


@receiver(post_delete, sender=OrderItems)
def restore_inventory_on_delete(sender, instance, **kwargs):
    """
    Restore inventory when order item is deleted
    """
    inventory = instance.InventoryChange
    new_quantity = inventory.QuantityWeightAvailable + instance.TotalWeight
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
    OrderStatus = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    StatusChangeDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.Order.User.username} - {self.OrderStatus} - {self.StatusChangeDate}"
        )
