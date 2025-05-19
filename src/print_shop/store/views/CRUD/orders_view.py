from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.forms.order_forms import OrdersForm
from store.models import Orders


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# Owner or admin check
def is_owner_or_admin(user, order):
    return user.is_authenticated and (user == order.User or is_admin(user))


# List all orders - accessible to all authenticated users
@login_required
def orders_list(request):
    if is_admin(request.user):
        orders = Orders.objects.all()
    else:
        orders = Orders.objects.filter(User=request.user)
    return render(request, "orders/orders_list.html", {"orders": orders})


# Create a new order - only accessible to all authenticated users
@login_required
def add_order(request):
    if request.method == "POST":
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(
                request, f"Order {order.User.username} was created successfully"
            )
            return redirect("orders-list")
    else:
        form = OrdersForm()
    return render(request, "orders/orders_form.html", {"form": form})


# Edit an existing order - only accessible to admin users
@login_required
def edit_order(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    if not is_owner_or_admin(request.user, order):
        messages.error(request, "You do not have permission to edit this order.")
        return redirect("orders-list")

    if request.method == "POST":
        form = OrdersForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            messages.success(
                request, f"Order {order.User.username} was updated successfully"
            )
            return redirect("orders-list")
    else:
        form = OrdersForm(instance=order)
    return render(request, "orders/orders_form.html", {"form": form})


# Delete an order - only accessible to admin users
@login_required
def delete_order(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    if not is_owner_or_admin(request.user, order):
        messages.error(request, "You do not have permission to delete this order.")
        return redirect("orders-list")

    if request.method == "POST":
        name = order.User.username
        order.delete()
        messages.success(request, f"Order {name} was deleted successfully")
        return redirect("orders-list")
    return render(request, "orders/orders_confirm_delete.html", {"order": order})
