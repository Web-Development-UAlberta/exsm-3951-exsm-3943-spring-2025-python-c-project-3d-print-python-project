from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.filament_form import FilamentForm
from store.models import Filament


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# List all filaments - accessible to all authenticated users
@login_required
def filament_list(request):
    filaments = Filament.objects.all()
    return render(request, "filament/filament_list.html", {"filaments": filaments})


# Create a new filament - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def add_filament(request):
    if request.method == "POST":
        form = FilamentForm(request.POST)
        if form.is_valid():
            filament = form.save()
            messages.success(
                request, f"Filament {filament.Name} was created successfully"
            )
            return redirect("filament-list")
    else:
        form = FilamentForm()
    return render(request, "filament/filament_form.html", {"form": form})


# Edit an existing filament - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def edit_filament(request, pk):
    filament = get_object_or_404(Filament, pk=pk)
    if request.method == "POST":
        form = FilamentForm(request.POST, instance=filament)
        if form.is_valid():
            filament = form.save()
            messages.success(
                request, f"Filament {filament.Name} was updated successfully"
            )
            return redirect("filament-list")
    else:
        form = FilamentForm(instance=filament)
    return render(request, "filament/filament_form.html", {"form": form})


# Delete a filament - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def delete_filament(request, pk):
    filament = get_object_or_404(Filament, pk=pk)
    if request.method == "POST":
        name = filament.Name
        filament.delete()
        messages.success(request, f"Filament {name} was deleted successfully")
        return redirect("filament-list")
    return render(
        request, "filament/filament_confirm_delete.html", {"filament": filament}
    )
