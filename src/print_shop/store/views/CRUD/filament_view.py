from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.forms.filament_form import FilamentForm
from store.models import Filament


# List all filaments
def filament_list(request):
    filaments = Filament.objects.all()
    return render(request, "filament/filament_list.html", {"filaments": filaments})


# Create a new filament
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


# Edit an existing filament
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


# Delete a filament
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
