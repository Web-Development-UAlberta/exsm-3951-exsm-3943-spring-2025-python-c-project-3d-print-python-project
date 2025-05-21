from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.raw_materials_form import RawMaterialsForm
from store.models import RawMaterials, InventoryChange


# Check if user is an admin (staff or superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# List all raw materials - accessible to all authenticated users
@login_required
def raw_materials_list(request):
    raw_materials = RawMaterials.objects.all()
    return render(
        request,
        "raw_materials/raw_materials_list.html",
        {"raw_materials": raw_materials},
    )


# Create a new raw material
@login_required
@user_passes_test(is_admin)
def add_raw_material(request):
    if request.method == "POST":
        form = RawMaterialsForm(request.POST)
        if form.is_valid():
            raw_material = form.save()
            material_name = raw_material.BrandName or raw_material.Filament.Name
            messages.success(
                request, f"Raw Material {material_name} was created successfully"
            )
            return redirect("current-inventory")
    else:
        form = RawMaterialsForm()
    return render(request, "raw_materials/raw_material_form.html", {"form": form})


# Edit an existing raw material - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def edit_raw_material(request, pk):
    raw_material = get_object_or_404(RawMaterials, pk=pk)
    if request.method == "POST":
        form = RawMaterialsForm(request.POST, instance=raw_material)
        if form.is_valid():
            raw_material = form.save()
            material_name = raw_material.BrandName or raw_material.Filament.Name
            messages.success(
                request, f"Raw Material {material_name} was updated successfully"
            )
            return redirect("current-inventory")
    else:
        form = RawMaterialsForm(instance=raw_material)
    return render(
        request,
        "raw_materials/raw_material_form.html",
        {
            "form": form,
        },
    )


# View details of a raw material - accessible to admin users
@login_required
@user_passes_test(is_admin)
def raw_material_detail(request, pk):
    raw_material = get_object_or_404(RawMaterials, pk=pk)
    inventory_changes = InventoryChange.objects.filter(RawMaterial=raw_material).order_by('-InventoryChangeDate')
    inventory_count = inventory_changes.count()
    has_orders = False
    if inventory_count > 0:
        from store.models import OrderItems
        has_orders = OrderItems.objects.filter(InventoryChange__RawMaterial=raw_material).exists()
    can_edit = inventory_count <= 1 and not has_orders
    cost_per_gram = 0
    if raw_material.MaterialWeightPurchased > 0:
        cost_per_gram = raw_material.Cost / raw_material.MaterialWeightPurchased
    
    context = {
        'raw_material': raw_material,
        'inventory_changes': inventory_changes,
        'can_edit': can_edit,
        'inventory_count': inventory_count,
        'has_orders': has_orders,
        'cost_per_gram': cost_per_gram
    }
    
    return render(request, 'raw_materials/raw_material_detail.html', context)


# Delete a raw material - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def delete_raw_material(request, pk):
    raw_material = get_object_or_404(RawMaterials, pk=pk)
    if request.method == "POST":
        material_name = raw_material.BrandName or raw_material.Filament.Name
        raw_material.delete()
        messages.success(
            request, f"Raw Material {material_name} was deleted successfully"
        )
        return redirect("current-inventory")
    return render(
        request,
        "raw_materials/raw_material_confirm_delete.html",
        {"raw_material": raw_material},
    )
