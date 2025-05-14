from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Orders, OrderItems, FulfillmentStatus


@login_required
def order_tracking(request):
    """
    Order tracking page for customers to view their orders
    """
    # Get the user's orders
    orders = Orders.objects.filter(User=request.user).prefetch_related(
        'orderitems_set', 
        'orderitems_set__Model', 
        'orderitems_set__InventoryChange__RawMaterial__Filament__Material',
        'fulfillmentstatus_set'
    ).order_by('-CreatedAt')
    
    # Get the latest order for summary display
    latest_order = orders.first()
    
    context = {
        "orders": orders,
        "latest_order": latest_order,
    }
    
    return render(request, "customer_facing_pages/order_tracking.html", context)


@login_required
def order_details(request, order_id):
    """
    Order details page for customers to view a specific order
    """
    order = get_object_or_404(Orders, id=order_id, User=request.user)

    order.orderitems_set.select_related(
        'Model', 'InventoryChange__RawMaterial__Filament__Material'
    )
    
    context = {
        "order": order,
    }
    
    return render(request, "customer_facing_pages/order_details.html", context)
