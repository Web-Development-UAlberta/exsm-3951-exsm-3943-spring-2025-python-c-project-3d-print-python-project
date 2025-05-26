from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.models_form import ModelsForm
from store.models import Models


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# List all models - accessible to all authenticated users
@login_required
def models_list(request):
    models = Models.objects.all()
    return render(request, "models/models_list.html", {"models": models})


# Create a new model - only accessible to admin users
@login_required
@user_passes_test(is_admin)
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


# Edit an existing model - only accessible to admin users
@login_required
@user_passes_test(is_admin)
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


# Delete a model - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def delete_model(request, pk):
    model = get_object_or_404(Models, pk=pk)
    if request.method == "POST":
        name = Models.Name
        try:
            model.delete()
            messages.success(request, f"Model {name} was deleted successfully")
        except Exception as e:
            messages.error(request, f"Failed to delete model. The model may be in use.")
        return redirect("models-list")
    return render(request, "models/model_confirm_delete.html", {"model": model})
