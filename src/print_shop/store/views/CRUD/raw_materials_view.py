from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.raw_materials_form import RawMaterialsForm
from store.models import RawMaterials


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
            return redirect("raw-materials-list")
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
            return redirect("raw-materials-list")
    else:
        form = RawMaterialsForm(instance=raw_material)
    return render(
        request,
        "raw_materials/raw_material_form.html",
        {
            "form": form,
        },
    )


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
        return redirect("raw-materials-list")
    return render(
        request,
        "raw_materials/raw_material_confirm_delete.html",
        {"raw_material": raw_material},
    )
