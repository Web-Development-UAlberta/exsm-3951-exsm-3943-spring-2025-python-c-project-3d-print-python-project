from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from store.models import OrderItems, Orders, FulfillmentStatus
from store.forms.order_forms import AdminItemForm
from store.forms.customer_selection_form import CustomerSelectionForm


def is_staff(user):
    """Check if user is staff"""
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def premade_items_list(request):
    """
    List all premade items (admin view)
    """
    premade_items = OrderItems.objects.filter(
        Order__isnull=True, IsCustom=False
    ).select_related("Model", "InventoryChange__RawMaterial__Filament__Material")

    context = {"premade_items": premade_items}

    return render(request, "admin/premade_items_list.html", context)


@login_required
@user_passes_test(is_staff)
def add_premade_item(request):
    """
    Add a new premade item (admin view)
    """
    if request.method == "POST":
        form = AdminItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(
                request, f"Premade item '{item.Model.Name}' was created successfully"
            )
            return redirect("product-admin-premade-items")
    else:
        form = AdminItemForm()

    context = {"form": form, "title": "Add Premade Item"}

    return render(request, "admin/premade_item_form.html", context)


@login_required
@user_passes_test(is_staff)
def edit_premade_item(request, pk):
    """
    Edit an existing premade item (admin view)
    """
    item = get_object_or_404(OrderItems, pk=pk, Order__isnull=True, IsCustom=False)

    if request.method == "POST":
        form = AdminItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            messages.success(
                request, f"Premade item '{item.Model.Name}' was updated successfully"
            )
            return redirect("product-admin-premade-items")
    else:
        form = AdminItemForm(instance=item)

    context = {"form": form, "title": "Edit Premade Item"}

    return render(request, "admin/premade_item_form.html", context)


@login_required
@user_passes_test(is_staff)
def delete_premade_item(request, pk):
    """
    Delete a premade item (admin view)
    """
    item = get_object_or_404(OrderItems, pk=pk, Order__isnull=True, IsCustom=False)

    if request.method == "POST":
        name = item.Model.Name
        item.delete()
        messages.success(request, f"Premade item '{name}' was deleted successfully")
        return redirect("product-admin-premade-items")

    context = {"item": item}

    return render(request, "admin/premade_item_confirm_delete.html", context)



@login_required
@user_passes_test(is_staff)
def generate_quote(request):
    """
    Generate a custom order quote for a customer
    This allows store owners to create quotes for customers who request them in-store
    """
    if request.method == "POST":
        form = AdminItemForm(request.POST)
        customer_form = CustomerSelectionForm(request.POST)
        
        if form.is_valid() and customer_form.is_valid():
            item = form.save(commit=False)
            item.IsCustom = True
            customer = customer_form.cleaned_data['customer']
            order = Orders.objects.create(
                User=customer,
                Shipping=None,
                TotalPrice=0,
                ExpeditedService=False
            )
            FulfillmentStatus.objects.create(
                Order=order,
                OrderStatus=FulfillmentStatus.Status.DRAFT
            )
            item.Order = order
            item.save()
            messages.success(
                request, f"Quote for '{item.Model.Name}' was generated successfully for {customer.username}"
            )
            return redirect("orders-list")
    else:
        form = AdminItemForm(initial={'IsCustom': True})
        customer_form = CustomerSelectionForm()
    
    context = {
        "form": form,
        "customer_form": customer_form,
        "title": "Generate Customer Quote"
    }

    return render(request, "admin/quote_form.html", context)
