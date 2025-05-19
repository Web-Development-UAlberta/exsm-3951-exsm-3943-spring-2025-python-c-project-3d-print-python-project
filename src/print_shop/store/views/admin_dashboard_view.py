from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from store.models import Orders, FulfillmentStatus, Models, InventoryChange
from django.db.models import Q


# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_orders = Orders.objects.count()

    active_statuses = ["Draft", "Pending", "Paid", "Printing"]
    active_orders = FulfillmentStatus.objects.filter(
        OrderStatus__in=active_statuses
    ).count()

    pending_uploads = Models.objects.filter(FilePath__isnull=True).count()

    inventory_warnings = sum(
        1
        for inv in InventoryChange.objects.select_related("RawMaterial")
        if inv.needs_reorder
    )

    context = {
        "total_orders": total_orders,
        "active_orders": active_orders,
        "pending_uploads": pending_uploads,
        "inventory_warnings": inventory_warnings,
    }
    return render(request, "admin_dashboard/admin_dashboard_list.html", context)


@login_required
@user_passes_test(is_admin)
def inventory_management(request):
    query = request.GET.get("q", "")
    material = request.GET.get("material", "")
    quantity = request.GET.get("quantity", "")

    inventory = InventoryChange.objects.select_related(
        "RawMaterial__Filament__Material"
    ).all()

    if query:
        inventory = inventory.filter(
            Q(RawMaterial__Filament__Name__icontains=query)
            | Q(RawMaterial__Filament__Material__Name__icontains=query)
        )

    if material:
        inventory = inventory.filter(
            RawMaterial__Filament__Material__Name__icontains=material
        )

    if quantity:
        try:
            quantity = int(quantity)
            inventory = inventory.filter(QuantityWeightAvailable__gte=quantity)
        except ValueError:
            pass

    return render(
        request, "admin_dashboard/inventory_management.html", {"inventory": inventory}
    )


@login_required
@user_passes_test(is_admin)
def order_management(request):
    search = request.GET.get("search", "")
    material = request.GET.get("material", "")
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")

    orders = Orders.objects.all()

    if search:
        orders = orders.filter(
            Q(orderitems__Model__Name__icontains=search)
            | Q(
                orderitems__InventoryChange__RawMaterial__Filament__Material__Name__icontains=search
            )
        ).distinct()

    if material:
        orders = orders.filter(
            orderitems__InventoryChange__RawMaterial__Filament__Material__Name__icontains=material
        ).distinct()

    if status:
        orders = [
            o
            for o in orders
            if o.current_status and status.lower() in o.current_status.lower()
        ]

    if priority:
        if priority.lower() == "high":
            orders = orders.filter(ExpeditedService=True)
        elif priority.lower() == "normal":
            orders = orders.filter(ExpeditedService=False)

    context = {"orders": orders}
    return render(request, "admin_dashboard/order_management.html", context)
