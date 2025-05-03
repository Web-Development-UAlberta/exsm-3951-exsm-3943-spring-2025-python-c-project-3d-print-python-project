from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import FulfillmentStatusForm
from ...models import FulfillmentStatus


# List all fulfillment statuses
def fulfillment_status_list(request):
    fulfillment_statuses = FulfillmentStatus.objects.all()
    return render(
        request, "orders/fulfillment_status_list.html", {"fulfillment_statuses": fulfillment_statuses}
    )


# Create a new fulfillment status
def add_fulfillment_status(request):
    if request.method == "POST":
        form = FulfillmentStatusForm(request.POST)
        if form.is_valid():
            fulfillment_status = form.save()
            messages.success(
                request, f"Fulfillment status {fulfillment_status.OrderStatus} was created successfully"
            )
            return redirect("fulfillment-status-list")
    else:
        form = FulfillmentStatusForm()
    return render(request, "orders/fulfillment_status_form.html", {"form": form})


# Edit an existing fulfillment status
def edit_fulfillment_status(request, pk):
    fulfillment_status = get_object_or_404(FulfillmentStatus, pk=pk)
    if request.method == "POST":
        form = FulfillmentStatusForm(request.POST, instance=fulfillment_status)
        if form.is_valid():
            fulfillment_status = form.save()
            messages.success(
                request, f"Fulfillment status {fulfillment_status.OrderStatus} was updated successfully"
            )
            return redirect("fulfillment-status-list")
    else:
        form = FulfillmentStatusForm(instance=fulfillment_status)
    return render(request, "orders/fulfillment_status_form.html", {"form": form})


# Delete an fulfillment status
def delete_fulfillment_status(request, pk):
    fulfillment_status = get_object_or_404(FulfillmentStatus, pk=pk)
    if request.method == "POST":
        name = fulfillment_status.OrderStatus
        fulfillment_status.delete()
        messages.success(request, f"Fulfillment status {name} was deleted successfully")
        return redirect("fulfillment-status-list")
    return render(
        request, "orders/fulfillment_status_confirm_delete.html", {"fulfillment_status": fulfillment_status}
    )
