from django.shortcuts import render

from store.models import Orders, FulfillmentStatus, Models, InventoryChange 


def admin_dashboard(request):
    total_orders = Orders.objects.count()

    active_statuses = ['Draft', 'Pending', 'Paid', 'Printing']
    active_orders = FulfillmentStatus.objects.filter(OrderStatus__in=active_statuses).count()

    pending_uploads = Models.objects.filter(FilePath__isnull=True).count()

    inventory_warnings = sum(1 for inv in InventoryChange.objects.select_related('RawMaterial') if inv.needs_reorder)

    context = {
        "total_orders": total_orders,
        "active_orders": active_orders,
        "pending_uploads": pending_uploads,
        "inventory_warnings": inventory_warnings,
   
    }
    return render(request, 'admin_dashboard/admin_dashboard_list.html', context)