from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.materials_form import MaterialsForm
from store.models import Materials


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# List all materials - accessible to all authenticated users
@login_required
def materials_list(request):
    materials = Materials.objects.all()
    return render(request, "materials/materials_list.html", {"materials": materials})


# Create a new material - only accessible to admin users
@login_required
@user_passes_test(is_admin)
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


# Edit an existing material - only accessible to admin users
@login_required
@user_passes_test(is_admin)
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


# Delete a material - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def delete_material(request, pk):
    material = get_object_or_404(Materials, pk=pk)
    if request.method == "POST":
        name = Materials.Name
        try:
            material.delete()
            messages.success(request, f"Material {name} was deleted successfully")
        except Exception as e:
            messages.error(
                request, "Failed to delete material. The material may be in use."
            )
        return redirect("materials-list")
    return render(
        request, "materials/material_confirm_delete.html", {"material": material}
    )
