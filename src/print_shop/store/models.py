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
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone


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
        default=Decimal("1.00"),
        validators=[MinValueValidator(Decimal("1.00"))],
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

    def find_for_weight(
        self, required_weight, safety_margin=Decimal("1.15"), raw_material=None
    ):
        """Find inventory with enough material for the required weight

        Args:
            required_weight: The weight needed for the order
            safety_margin: Multiplier for safety margin (default: 1.15 for 15%)
            raw_material: Optional RawMaterials instance to filter by specific material

        Returns:
            InventoryChange object with enough material, or None if not found
        """
        weight_with_margin = Decimal(required_weight) * Decimal(safety_margin)
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
        threshold = Decimal(self.RawMaterial.MaterialWeightPurchased) * Decimal("0.2")
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
            UnitCost=instance.Cost / Decimal(instance.MaterialWeightPurchased),
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
                initial_inventory.UnitCost = instance.Cost / Decimal(instance.MaterialWeightPurchased)
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
    Thumbnail = models.ImageField(upload_to="thumbnails/", null=True)
    FixedCost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("3.00"),
    )
    EstimatedPrintVolume = models.IntegerField()
    BaseInfill = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.3"),
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
    Shipping = models.ForeignKey(
        Shipping, on_delete=models.PROTECT, null=True, blank=True
    )
    TotalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    EstimatedShipDate = models.DateTimeField(null=True)
    ExpeditedService = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.User.username} - {self.CreatedAt} - {self.TotalPrice}"

    @property
    def current_status(self):
        """
        Get the most recent status of this order.
        Returns None if no status has been set.
        """
        latest_status = self.fulfillmentstatus_set.order_by("-StatusChangeDate").first()
        return latest_status.OrderStatus if latest_status else None

    def update_status(self, new_status, save=True):
        """
        Update the order status, creating a new FulfillmentStatus record.

        Args:
            new_status: The new status to set (from FulfillmentStatus.Status)
            save: Whether to save the order after updating status (default: True)
        """

        FulfillmentStatus.objects.create(
            Order=self, OrderStatus=new_status, StatusChangeDate=timezone.now()
        )

        if save:
            self.save()

    def save(self, *args, **kwargs):
        """
        Calculate total price before saving.
        If this is a new order and doesn't have a status, set it to DRAFT.
        """
        is_new = self.pk is None

        if self.pk:
            order_items = self.orderitems_set.all()
            if order_items.exists():
                items_total = sum(
                    item.ItemPrice * item.ItemQuantity
                    for item in order_items
                )
                shipping_cost = (
                    self.Shipping.Rate if self.Shipping else Decimal("0")
                )
                self.TotalPrice = items_total + shipping_cost

                if self.ExpeditedService:
                    self.TotalPrice = self.TotalPrice * Decimal("1.5")

        super().save(*args, **kwargs)

        if is_new and not self.fulfillmentstatus_set.exists():
            FulfillmentStatus.objects.create(
                Order=self,
                OrderStatus=FulfillmentStatus.Status.DRAFT,
                StatusChangeDate=timezone.now(),
            )


class OrderItems(models.Model):
    """Table to store all order items"""

    InventoryChange = models.ForeignKey(InventoryChange, on_delete=models.PROTECT)
    Order = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True, blank=True)
    Model = models.ForeignKey(Models, on_delete=models.PROTECT)
    InfillMultiplier = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal("1.00")
    )
    TotalWeight = models.IntegerField()
    CostOfGoodsSold = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    Markup = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("1.15"),
        validators=[MinValueValidator(Decimal("1.00"))],
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
                    {
                        "ItemPrice": "Item price cannot be less than the cost of goods sold."
                    }
                )
        super().clean()

    def __str__(self):
        return f"{self.Model.Name} - {self.ItemQuantity}"

    def calculate_infill_multiplier(self, infill_percentage=None):
        """
        Calculate the infill multiplier based on the given infill percentage.
        If no percentage is provided, use the model's base infill.
        """
        if infill_percentage is None:
            return Decimal('1.0')
            
        try:
            base_infill = self.Model.BaseInfill * 100
            if base_infill == 0:
                base_infill = Decimal('20')
                
            return (Decimal(infill_percentage) / base_infill).quantize(
                Decimal('0.0001'), 
                rounding=ROUND_HALF_UP
            )
        except (AttributeError, InvalidOperation, TypeError):
            return Decimal('1.0')

    def calculate_required_weight(self):
        """
        Calculate the required weight for the order item based on model, infill, and quantity.
        This is used for inventory validation before saving.
        Returns the total weight required for this order item in grams
        """
        if not hasattr(self, "InventoryChange") or not self.InventoryChange:
            return 0

        try:
            density = self.InventoryChange.RawMaterial.MaterialDensity
            infill_multiplier = self.InfillMultiplier  # Decimal
            quantity = self.ItemQuantity  # int
            estimated_print_volume = self.Model.EstimatedPrintVolume  # Decimal
            base_infill = self.Model.BaseInfill  
            volume_cm3 = estimated_print_volume * base_infill * infill_multiplier
            weight = volume_cm3 * density * quantity
            return max(1, int(weight.quantize(Decimal('1'), rounding=ROUND_HALF_UP)))
            
        except (AttributeError, TypeError, InvalidOperation) as e:
            print(f"Error in calculate_required_weight: {e}")
            return 0

    def calculate_price_components(self):
        """
        Calculate and return all price components as a dictionary.
        This ensures consistent price calculation across the application.
        Returns:
            dict: Contains 'weight', 'material_cost', 'fixed_cost', 'cost_of_goods', 'price'
        """
        weight = Decimal(self.calculate_required_weight())
        cost_per_gram = self.InventoryChange.UnitCost
        wear_tear = self.InventoryChange.RawMaterial.WearAndTearMultiplier
        fixed_cost = self.Model.FixedCost * self.ItemQuantity
        markup = self.Markup
        material_cost = (weight * cost_per_gram * wear_tear).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )
        cost_of_goods = (fixed_cost + material_cost).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )
        price = (cost_of_goods * markup).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        return {
            "weight": weight,
            "material_cost": material_cost,
            "fixed_cost": fixed_cost,
            "cost_of_goods": cost_of_goods,
            "price": price,
        }

    def save(self, *args, **kwargs):
        """
        Override save to calculate costs before saving using the shared calculation method.
        """
        self.TotalWeight = self.calculate_required_weight()
        try:
            price_components = self.calculate_price_components()
            self.CostOfGoodsSold = price_components["cost_of_goods"]
            self.ItemPrice = price_components["price"]
            super().save(*args, **kwargs)
        except (AttributeError, TypeError) as e:
            print(f"Error in OrderItems.save(): {e}")
            raise


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
