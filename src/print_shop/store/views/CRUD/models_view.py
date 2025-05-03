from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ModelsForm
from ...models import Models


# List all models
def models_list(request):
    models = Models.objects.all()
    return render(request, "models/models_list.html", {"models": models})


# Create a new model
def add_model(request):
    if request.method == "POST":
        form = ModelsForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            messages.success(request, f"Model {model.Name} was created successfully")
            return redirect("models-list")
    else:
        form = ModelsForm()
    return render(request, "models/model_form.html", {"form": form})


# Edit an existing model
def edit_model(request, pk):
    model = get_object_or_404(Models, pk=pk)
    if request.method == "POST":
        form = ModelsForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            model = form.save()
            messages.success(request, f"Model {model.Name} was updated successfully")
            return redirect("models-list")
    else:
        form = ModelsForm(instance=model)
    return render(request, "models/model_form.html", {"form": form})


# Delete a model
def delete_model(request, pk):
    model = get_object_or_404(Models, pk=pk)
    if request.method == "POST":
        name = model.Name
        model.delete()
        messages.success(request, f"Model {name} was deleted successfully")
        return redirect("models-list")
    return render(request, "models/model_confirm_delete.html", {"model": model})
