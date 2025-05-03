from django.shortcuts import render, redirect, get_object_or_404, messages
from .forms import SuppliersForm
from ...models import Suppliers

# List all suppliers
def supplier_list(request):
    suppliers = Suppliers.objects.all()
    return render(request, 'supplier/supplier_list.html', {'suppliers': suppliers})

# Create a new supplier
def add_supplier(request):
    if request.method == 'POST':
        form = SuppliersForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier {supplier.Name} was created successfully')
            return redirect('suppliers-list')
    else:
        form = SuppliersForm()
    return render(request, 'suppliers/supplier_form.html', {'form': form})

# Edit an existing supplier
def edit_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == 'POST':
        form = SuppliersForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier {supplier.Name} was updated successfully')
            return redirect('suppliers-list')
    else:
        form = SuppliersForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form})

# Delete a supplier
def delete_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == 'POST':
        name = supplier.Name
        supplier.delete()
        messages.success(request, f'Supplier {name} was deleted successfully')
        return redirect('suppliers-list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})