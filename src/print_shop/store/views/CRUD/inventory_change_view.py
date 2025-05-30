from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.inventory_form import InventoryChangeForm
from store.models import InventoryChange, RawMaterials


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# List all inventory changes - accessible to all authenticated users
@login_required
def inventory_change_list(request):
    inventory_changes = InventoryChange.objects.all()
    return render(
        request,
        "inventory/inventory_change_list.html",
        {"inventory_changes": inventory_changes},
    )


# Show details of a specific raw material's inventory
@login_required
@user_passes_test(is_admin)
def current_inventory_levels(request):
    """
    Display the current inventory levels for all raw materials.
    If inventory levels are low, mark them for reorder.
    Uses the RawMaterials.current_inventory property from the model manager.
    """
    raw_materials = RawMaterials.objects.select_related(
        'Filament__Material'
    ).order_by(
        'Filament__Material__Name',
        'Filament__Name',
        'PurchasedDate'
    )
    raw_materials_with_inventory = []
    for raw_material in raw_materials:
        current_inventory = raw_material.current_inventory
        if current_inventory:
            raw_materials_with_inventory.append({
                "raw_material": raw_material,
                "inventory_change": current_inventory,
                "needs_reorder": current_inventory.needs_reorder,
            })
    return render(
        request,
        "inventory/current_inventory_levels.html",
        {
            "raw_materials_with_inventory": raw_materials_with_inventory,
        },
    )


# Show details of a specific inventory change - accessible to all users
@login_required
def inventory_change_detail(request, pk):
    inventory_change = get_object_or_404(InventoryChange, pk=pk)
    return render(
        request,
        "inventory/inventory_change_detail.html",
        {"inventory_change": inventory_change},
    )


# Create a new inventory change - only accessible to admin users
@login_required
@user_passes_test(is_admin)
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


# Edit an existing inventory change - only accessible to admin users
@login_required
@user_passes_test(is_admin)
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


# Delete an inventory change - only accessible to admin users
@login_required
@user_passes_test(is_admin)
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
