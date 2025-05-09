from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.forms.order_forms import OrdersForm
from store.models import Orders


# List all orders
def orders_list(request):
    orders = Orders.objects.all()
    return render(request, "orders/orders_list.html", {"orders": orders})


# Create a new order
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


# Edit an existing order
def edit_order(request, pk):
    order = get_object_or_404(Orders, pk=pk)
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


# Delete an order
def delete_order(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    if request.method == "POST":
        name = order.User.username
        order.delete()
        messages.success(request, f"Order {name} was deleted successfully")
        return redirect("orders-list")
    return render(
        request, "orders/orders_confirm_delete.html", {"order": order}
    )
