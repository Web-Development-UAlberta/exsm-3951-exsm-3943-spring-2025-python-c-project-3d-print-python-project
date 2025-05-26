from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.suppliers_form import SuppliersForm
from store.models import Suppliers


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# List all suppliers - accessible to admin users
@login_required
@user_passes_test(is_admin)
def supplier_list(request):
    suppliers = Suppliers.objects.all()
    return render(request, "suppliers/supplier_list.html", {"suppliers": suppliers})


# Create a new supplier - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def add_supplier(request):
    if request.method == "POST":
        form = SuppliersForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(
                request, f"Supplier {supplier.Name} was created successfully"
            )
            return redirect("suppliers-list")
    else:
        form = SuppliersForm()
    return render(request, "suppliers/supplier_form.html", {"form": form})


# Edit an existing supplier - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def edit_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == "POST":
        form = SuppliersForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(
                request, f"Supplier {supplier.Name} was updated successfully"
            )
            return redirect("suppliers-list")
    else:
        form = SuppliersForm(instance=supplier)
    return render(request, "suppliers/supplier_form.html", {"form": form})


# Delete a supplier - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def delete_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == "POST":
        name = Suppliers.Name
        try:
            supplier.delete()
            messages.success(request, f"Supplier {name} was deleted successfully")
        except Exception as e:
            messages.error(
                request, f"Failed to delete supplier. The supplier may be in use."
            )
        return redirect("suppliers-list")
    return render(
        request, "suppliers/supplier_confirm_delete.html", {"supplier": supplier}
    )
