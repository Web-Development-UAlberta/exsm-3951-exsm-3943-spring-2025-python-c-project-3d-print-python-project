from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.forms.raw_materials_form import RawMaterialsForm
from ...models import RawMaterials


# List all raw materials
def raw_materials_list(request):
    raw_materials = RawMaterials.objects.all()
    return render(
        request,
        "raw_materials/raw_materials_list.html",
        {"raw_materials": raw_materials},
    )


# Create a new raw material
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


# Edit an existing raw material
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


# Delete a raw material
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
