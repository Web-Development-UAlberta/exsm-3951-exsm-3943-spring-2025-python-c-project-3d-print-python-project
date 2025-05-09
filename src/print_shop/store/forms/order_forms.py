from django import forms
from django.core.exceptions import ValidationError
from store.models import Orders, OrderItems, InventoryChange


def validate_inventory_availability(inventory, weight_with_margin):
    """
    Validate inventory availability and find alternative inventory if needed.

    Args:
        inventory: The InventoryChange object to check
        weight_with_margin: The required weight with safety margin applied

    Returns:
        (sufficient_inventory, error_message): A tuple containing either:
        - An InventoryChange with enough material and None, or
        - None and an error message if no sufficient inventory found
    """
    if inventory.QuantityWeightAvailable >= weight_with_margin:
        return inventory, None

    raw_material = inventory.RawMaterial
    sufficient_inventory = InventoryChange.objects.find_for_weight(
        required_weight=weight_with_margin / 1.15, raw_material=raw_material
    )

    if sufficient_inventory:
        return sufficient_inventory, None
    else:
        error_message = (
            f"Not enough inventory available. Need {weight_with_margin:.0f}g (including 15% margin) "
            f"but only {inventory.QuantityWeightAvailable}g available in the selected inventory."
        )
        return None, error_message


class OrdersForm(forms.ModelForm):
    """Form for creating and editing orders"""

    class Meta:
        model = Orders
        fields = ["User", "Shipping", "ExpeditedService"]


class OrderItemsForm(forms.ModelForm):
    """
    Form for creating and editing order items
    Acts as the base form.
    """

    infill_percentage = forms.IntegerField(
        min_value=5, max_value=100, help_text="Select infill percentage (5-100%)"
    )

    """
    For normal orders we need to hide is_custom and order fields
    as customers should not be able to change them
    """

    class Meta:
        model = OrderItems
        fields = ["Model", "InventoryChange", "ItemQuantity", "Order", "IsCustom"]
        widgets = {
            "IsCustom": forms.HiddenInput(),
            "Order": forms.HiddenInput(),
        }

    """
    Initialize the form with additional arguments
    to set the values of is_custom, order, and model
    For pre-made items, is_custom is set to False
    For custom items, is_custom is set to True
    Order and Model are none to start until they are set.
    """

    def __init__(self, *args, **kwargs):
        is_custom = kwargs.pop("is_custom", False)
        order = kwargs.pop("order", None)
        model = kwargs.pop("model", None)

        super().__init__(*args, **kwargs)
        self.initial["IsCustom"] = is_custom

        if order is not None:
            self.initial["Order"] = order

        """Use the custom manager to filter 'available' inventory"""
        self.fields["InventoryChange"].queryset = InventoryChange.objects.available()

        """
        If model is provided, set initial infill percentage to model's base infill
        This allows customers to see the starting infill percentage when they first load the form
        Or if the item instance exists with an infill multiplier, set the initial infill percentage off of the multiplier
        """
        if model:
            self.initial["infill_percentage"] = int(model.BaseInfill * 100)
        elif (
            self.instance.pk and self.instance.InfillMultiplier and self.instance.Model
        ):
            base_infill = self.instance.Model.BaseInfill * 100
            self.initial["infill_percentage"] = int(
                base_infill * self.instance.InfillMultiplier
            )

    def clean(self):
        """
        Clean the form data to ensure it is valid based on our business logic
        Validate that there is enough inventory available for the order
        """
        cleaned_data = super().clean()

        if "Model" not in cleaned_data or "InventoryChange" not in cleaned_data:
            return cleaned_data

        model = cleaned_data["Model"]
        inventory = cleaned_data["InventoryChange"]
        infill_percentage = cleaned_data.get(
            "infill_percentage", int(model.BaseInfill * 100)
        )
        quantity = cleaned_data.get("ItemQuantity", 1)
        multiplier = round(infill_percentage / (model.BaseInfill * 100), 2)
        is_custom = cleaned_data.get("IsCustom", self.initial.get("IsCustom", False))

        item = OrderItems(
            Model=model,
            InventoryChange=inventory,
            InfillMultiplier=multiplier,
            ItemQuantity=quantity,
            IsCustom=is_custom,
        )

        required_weight = item.calculate_required_weight()
        weight_with_margin = required_weight * 1.15
        sufficient_inventory, error_message = validate_inventory_availability(
            inventory, weight_with_margin
        )

        if sufficient_inventory and sufficient_inventory != inventory:
            cleaned_data["InventoryChange"] = sufficient_inventory
        elif error_message:
            raise ValidationError(error_message)

        return cleaned_data


class AdminItemForm(OrderItemsForm):
    """
    Form for store owners to create pre-made items or generate quotes
    1. Creating pre-made items (IsCustom=False) for the store inventory
    2. Generating custom quotes (IsCustom=True) for customers
    Store owners can toggle between these two modes using the IsCustom checkbox.
    """

    class Meta(OrderItemsForm.Meta):
        fields = ["Model", "InventoryChange", "ItemQuantity", "IsCustom"]

    def __init__(self, *args, **kwargs):
        kwargs["is_custom"] = False
        super().__init__(*args, **kwargs)

        self.fields["IsCustom"].widget = forms.CheckboxInput()
        self.fields[
            "IsCustom"
        ].help_text = "Check to create a custom order quote, uncheck for pre-made item"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.Order = None

        if commit:
            instance.save()
        return instance


class CustomOrderItemForm(OrderItemsForm):
    """Form for customers to create custom order items"""

    class Meta(OrderItemsForm.Meta):
        fields = [
            "Model",
            "InventoryChange",
            "ItemQuantity",
            "infill_percentage",
        ]

    def __init__(self, *args, **kwargs):
        kwargs["is_custom"] = True
        super().__init__(*args, **kwargs)

        if "IsCustom" in self.fields:
            del self.fields["IsCustom"]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance


class PremadeItemCartForm(forms.Form):
    """Form for adding pre-made items to cart - used by customers in the gallery"""

    quantity = forms.IntegerField(min_value=1, initial=1)
    item_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()

        if "item_id" not in cleaned_data or "quantity" not in cleaned_data:
            return cleaned_data

        item_id = cleaned_data["item_id"]
        quantity = cleaned_data["quantity"]

        try:
            item = OrderItems.objects.get(pk=item_id, Order__isnull=True)
        except OrderItems.DoesNotExist:
            raise ValidationError("Item not found or already in an order")

        item = OrderItems(
            Model=item.Model,
            InventoryChange=item.InventoryChange,
            InfillMultiplier=item.InfillMultiplier,
            ItemQuantity=quantity,
            IsCustom=item.IsCustom,
        )

        total_weight = item.calculate_required_weight()
        weight_with_margin = total_weight * 1.15

        inventory = item.InventoryChange
        sufficient_inventory, error_message = validate_inventory_availability(
            inventory, weight_with_margin
        )

        if sufficient_inventory and sufficient_inventory != inventory:
            original_item = OrderItems.objects.get(pk=item_id)
            original_item.InventoryChange = sufficient_inventory
            original_item.save()

            item.InventoryChange = sufficient_inventory
        elif error_message:
            raise ValidationError(error_message)

        return cleaned_data
