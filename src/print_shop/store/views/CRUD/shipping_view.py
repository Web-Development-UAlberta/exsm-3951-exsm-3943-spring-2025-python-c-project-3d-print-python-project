from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.shipping_form import ShippingForm
from store.models import Shipping


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# List all shipping methods - accessible to all authenticated users
@login_required
def shipping_list(request):
    shipping = Shipping.objects.all()
    return render(request, "shipping/shipping_list.html", {"shipping": shipping})


# Create a new shipping method - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def add_shipping(request):
    if request.method == "POST":
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping = form.save()
            messages.success(
                request, f"Shipping {shipping.Name} was created successfully"
            )
            return redirect("shipping-list")
    else:
        form = ShippingForm()
    return render(request, "shipping/shipping_form.html", {"form": form})


# Edit an existing shipping method - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def edit_shipping(request, pk):
    shipping = get_object_or_404(Shipping, pk=pk)
    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            shipping = form.save()
            messages.success(
                request, f"Shipping {shipping.Name} was updated successfully"
            )
            return redirect("shipping-list")
    else:
        form = ShippingForm(instance=shipping)
    return render(request, "shipping/shipping_form.html", {"form": form})


# Delete a shipping method - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def delete_shipping(request, pk):
    shipping = get_object_or_404(Shipping, pk=pk)
    if request.method == "POST":
        name = shipping.Name
        shipping.delete()
        messages.success(request, f"Shipping {name} was deleted successfully")
        return redirect("shipping-list")
    return render(
        request, "shipping/shipping_confirm_delete.html", {"shipping": shipping}
    )
