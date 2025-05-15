from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from store.models import Orders, FulfillmentStatus, Models, InventoryChange 

# Check if the user is admin (Staff or Superuser)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

# @login_required
# @user_passes_test(is_admin)
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