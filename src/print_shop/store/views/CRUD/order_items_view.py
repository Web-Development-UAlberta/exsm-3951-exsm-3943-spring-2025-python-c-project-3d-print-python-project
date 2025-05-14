from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.order_forms import OrderItemsForm
from store.models import OrderItems


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

# List all order items - accessible to all authenticated users
@login_required
def order_items_list(request):
    # Check if the user is admin
    if is_admin(request.user):
        # If the user is admin, show all order items
        order_items = OrderItems.objects.all()
    else:
        # If the user is not admin, show only their own order items
        order_items = OrderItems.objects.filter(user=request.user)
    return render(request, "orders/order_items_list.html", {"order_items": order_items})


# Create a new order item - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def add_order_item(request):
    if request.method == "POST":
        form = OrderItemsForm(request.POST)
        if form.is_valid():
            order_item = form.save()
            messages.success(
                request, f"Order item {order_item.Model.Name} was created successfully"
            )
            return redirect("order-items-list")
    else:
        form = OrderItemsForm()
    return render(request, "orders/order_items_form.html", {"form": form})


# Edit an existing order item - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def edit_order_item(request, pk):
    order_item = get_object_or_404(OrderItems, pk=pk)
    if request.method == "POST":
        form = OrderItemsForm(request.POST, instance=order_item)
        if form.is_valid():
            order_item = form.save()
            messages.success(
                request, f"Order item {order_item.Model.Name} was updated successfully"
            )
            return redirect("order-items-list")
    else:
        form = OrderItemsForm(instance=order_item)
    return render(request, "orders/order_items_form.html", {"form": form})


# Delete an order item - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def delete_order_item(request, pk):
    order_item = get_object_or_404(OrderItems, pk=pk)
    if request.method == "POST":
        name = order_item.Model.Name
        order_item.delete()
        messages.success(request, f"Order item {name} was deleted successfully")
        return redirect("order-items-list")
    return render(
        request, "orders/order_items_confirm_delete.html", {"order_item": order_item}
    )
