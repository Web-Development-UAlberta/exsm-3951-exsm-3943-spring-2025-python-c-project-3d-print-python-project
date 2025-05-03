from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MaterialsForm
from ...models import Materials


# List all materials
def materials_list(request):
    materials = Materials.objects.all()
    return render(request, "materials/materials_list.html", {"materials": materials})


# Create a new material
def add_material(request):
    if request.method == "POST":
        form = MaterialsForm(request.POST)
        if form.is_valid():
            material = form.save()
            messages.success(
                request, f"Material {material.Name} was created successfully"
            )
            return redirect("materials-list")
    else:
        form = MaterialsForm()
    return render(request, "materials/material_form.html", {"form": form})


# Edit an existing material
def edit_material(request, pk):
    material = get_object_or_404(Materials, pk=pk)
    if request.method == "POST":
        form = MaterialsForm(request.POST, instance=material)
        if form.is_valid():
            material = form.save()
            messages.success(
                request, f"Material {material.Name} was updated successfully"
            )
            return redirect("materials-list")
    else:
        form = MaterialsForm(instance=material)
    return render(request, "materials/material_form.html", {"form": form})


# Delete a material
def delete_material(request, pk):
    material = get_object_or_404(Materials, pk=pk)
    if request.method == "POST":
        name = material.Name
        material.delete()
        messages.success(request, f"Material {name} was deleted successfully")
        return redirect("materials-list")
    return render(
        request, "materials/material_confirm_delete.html", {"material": material}
    )
