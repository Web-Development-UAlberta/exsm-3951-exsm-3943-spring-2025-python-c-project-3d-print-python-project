from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.forms.inventory_form import InventoryChangeForm
from store.models import InventoryChange, RawMaterials


# List all inventory changes
def inventory_change_list(request):
    inventory_changes = InventoryChange.objects.all()
    return render(
        request,
        "inventory/inventory_change_list.html",
        {"inventory_changes": inventory_changes},
    )


def current_inventory_levels(request):
    """
    Display the current inventory levels for all raw materials.
    If inventory levels are low, mark them for reorder.
    Uses the RawMaterials.current_inventory property from the model manager.
    """
    raw_materials_with_inventory = [
        {
            "raw_material": raw_material,
            "inventory_change": raw_material.current_inventory,
            "needs_reorder": raw_material.current_inventory.needs_reorder
            if raw_material.current_inventory
            else False,
        }
        for raw_material in RawMaterials.objects.all()
        if raw_material.current_inventory
    ]
    return render(
        request,
        "inventory/current_inventory_levels.html",
        {
            "raw_materials_with_inventory": raw_materials_with_inventory,
        },
    )


# Show details of a specific inventory change
def inventory_change_detail(request, pk):
    inventory_change = get_object_or_404(InventoryChange, pk=pk)
    return render(
        request,
        "inventory/inventory_change_detail.html",
        {"inventory_change": inventory_change},
    )


# Create a new inventory change
def add_inventory_change(request):
    if request.method == "POST":
        form = InventoryChangeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory Change was recorded successfully")
            return redirect("inventory-change-list")
    else:
        form = InventoryChangeForm()
    return render(request, "inventory/inventory_change_form.html", {"form": form})


# Edit an existing inventory change
def edit_inventory_change(request, pk):
    inventory_change = get_object_or_404(InventoryChange, pk=pk)
    if request.method == "POST":
        form = InventoryChangeForm(request.POST, instance=inventory_change)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory Change was updated successfully")
            return redirect("inventory-change-list")
    else:
        form = InventoryChangeForm(instance=inventory_change)
    return render(request, "inventory/inventory_change_form.html", {"form": form})


# Delete an inventory change
def delete_inventory_change(request, pk):
    inventory_change = get_object_or_404(InventoryChange, pk=pk)
    if request.method == "POST":
        inventory_change.delete()
        messages.success(request, "Inventory Change was deleted successfully")
        return redirect("inventory-change-list")
    return render(
        request,
        "inventory/inventory_change_confirm_delete.html",
        {"inventory_change": inventory_change},
    )
