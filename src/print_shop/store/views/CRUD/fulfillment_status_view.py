from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.forms.fulfillment_status_form import FulfillmentStatusForm
from store.models import FulfillmentStatus, Orders


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# List all fulfillment statuses - accessible to all authenticated users
@login_required
def fulfillment_status_list(request):
    if is_admin(request.user):
        fulfillment_statuses = FulfillmentStatus.objects.all()
    else:
        fulfillment_statuses = FulfillmentStatus.objects.filter(
            order__user=request.user
        )
    fulfillment_statuses = FulfillmentStatus.objects.all()
    return render(
        request,
        "orders/fulfillment_status_list.html",
        {"fulfillment_statuses": fulfillment_statuses},
    )

# Add a new fulfillment status - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def add_fulfillment_status(request):
    if request.method == "POST":
        form = FulfillmentStatusForm(request.POST)
        if form.is_valid():
            fulfillment_status = form.save()
            messages.success(
                request,
                f"Fulfillment status {fulfillment_status.OrderStatus} was created successfully",
            )
            return redirect("fulfillment-status-list")
    else:
        form = FulfillmentStatusForm()
    return render(request, "orders/fulfillment_status_form.html", {"form": form})

# Edit an existing fulfillment status - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def edit_fulfillment_status(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    try:
        fulfillment_status = FulfillmentStatus.objects.filter(Order=order).latest('StatusChangeDate')
    except FulfillmentStatus.DoesNotExist:
        fulfillment_status = FulfillmentStatus(Order=order)
    
    if request.method == "POST":
        if 'OrderStatus' in request.POST:
            new_status = FulfillmentStatus(
                Order=order,
                OrderStatus=request.POST['OrderStatus']
            )
            new_status.save()
            messages.success(
                request,
                f"Order #{order.id} status updated to {new_status.OrderStatus}",
            )
            return redirect("order_management")
        else:
            form = FulfillmentStatusForm(request.POST, instance=fulfillment_status)
            if form.is_valid():
                fulfillment_status = form.save()
                messages.success(
                    request,
                    f"Fulfillment status {fulfillment_status.OrderStatus} was updated successfully",
                )
                return redirect("order_management")
    else:
        form = FulfillmentStatusForm(instance=fulfillment_status)
    
    return render(request, "fulfillment_status/fulfillment_status_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def edit_fulfillment_status_order_list(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    try:
        fulfillment_status = FulfillmentStatus.objects.filter(Order=order).latest('StatusChangeDate')
    except FulfillmentStatus.DoesNotExist:
        fulfillment_status = FulfillmentStatus(Order=order)
    
    if request.method == "POST":
        if 'OrderStatus' in request.POST:
            new_status = FulfillmentStatus(
                Order=order,
                OrderStatus=request.POST['OrderStatus']
            )
            new_status.save()
            messages.success(
                request,
                f"Order #{order.id} status updated to {new_status.OrderStatus}",
            )
            return redirect("orders-list")
        else:
            form = FulfillmentStatusForm(request.POST, instance=fulfillment_status)
            if form.is_valid():
                fulfillment_status = form.save()
                messages.success(
                    request,
                    f"Fulfillment status {fulfillment_status.OrderStatus} was updated successfully",
                )
                return redirect("orders-list")
    else:
        form = FulfillmentStatusForm(instance=fulfillment_status)
    
    return render(request, "fulfillment_status/fulfillment_status_form.html", {"form": form})

# Delete an fulfillment status - only accessible to admin users
@login_required
@user_passes_test(is_admin)
def delete_fulfillment_status(request, pk):
    fulfillment_status = get_object_or_404(FulfillmentStatus, pk=pk)
    if request.method == "POST":
        name = fulfillment_status.OrderStatus
        fulfillment_status.delete()
        messages.success(request, f"Fulfillment status {name} was deleted successfully")
        return redirect("fulfillment-status-list")
    return render(
        request,
        "orders/fulfillment_status_confirm_delete.html",
        {"fulfillment_status": fulfillment_status},
    )
