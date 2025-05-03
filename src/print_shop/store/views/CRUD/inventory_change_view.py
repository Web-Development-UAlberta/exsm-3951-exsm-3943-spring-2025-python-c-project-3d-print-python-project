from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import InventoryChangeForm
from ...models import InventoryChange


# List all inventory changes
def inventory_change_list(request):
    inventory_changes = InventoryChange.objects.all()
    return render(
        request,
        "inventory_change/inventory_change_list.html",
        {"inventory_changes": inventory_changes},
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
    return render(
        request, "inventory_change/inventory_change_form.html", {"form": form}
    )


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
    return render(
        request, "inventory_change/inventory_change_form.html", {"form": form}
    )


# Delete an inventory change
def delete_inventory_change(request, pk):
    inventory_change = get_object_or_404(InventoryChange, pk=pk)
    if request.method == "POST":
        inventory_change.delete()
        messages.success(request, "Inventory Change was deleted successfully")
        return redirect("inventory-change-list")
    return render(
        request,
        "inventory_change/inventory_change_confirm_delete.html",
        {"inventory_change": inventory_change},
    )
