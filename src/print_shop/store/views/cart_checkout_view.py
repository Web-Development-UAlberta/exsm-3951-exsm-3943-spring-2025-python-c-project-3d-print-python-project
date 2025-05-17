from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from store.models import (
    OrderItems,
    Orders,
    Shipping,
    FulfillmentStatus,
)
from store.forms.checkout_form import CheckoutForm


def get_cart_items(request):
    """
    Get cart items for the current user's active draft order.
    Users must be logged in to have a cart to track adding items to cart.
    """
    if not request.user.is_authenticated:
        return OrderItems.objects.none()

    draft_order = get_draft_order(request)
    if not draft_order:
        return OrderItems.objects.none()

    return OrderItems.objects.filter(Order=draft_order).select_related(
        "Model", "InventoryChange__RawMaterial__Filament__Material"
    )


def get_draft_order(request):
    """
    Get the user's active draft order.
    Returns the most recent order that has a current status of DRAFT.
    """
    if not request.user.is_authenticated:
        return None

    user_orders = Orders.objects.filter(User=request.user).order_by("-CreatedAt")

    for order in user_orders:
        if order.current_status == FulfillmentStatus.Status.DRAFT:
            return order

    return None


def calculate_shipping(shipping, subtotal):
    """
    Calculate shipping cost and estimated ship date
    """
    shipping_cost = shipping.Rate
    estimated_ship_date = timezone.now() + timezone.timedelta(days=5)

    return {
        "shipping_cost": shipping_cost,
        "estimated_ship_date": estimated_ship_date,
    }


@login_required
def cart_view(request):
    """
    View for displaying the user's cart
    """
    cart_items = get_cart_items(request)

    subtotal = sum(item.ItemPrice for item in cart_items)

    context = {"cart_items": cart_items, "subtotal": subtotal}

    return render(request, "cart/cart.html", context)


@login_required
def remove_from_cart(request, item_id):
    """
    Remove an item from the cart
    """
    item = get_object_or_404(OrderItems, pk=item_id, Order__User=request.user)
    if "customer" not in request.session:
        request.session["customer"] = request.user.id

    if request.method == "POST":
        item_name = item.Model.Name
        item.delete()
        messages.success(request, f"{item_name} has been removed from your cart.")

    return redirect("cart")


@login_required
def update_cart_item(request, item_id):
    """
    Update the quantity of an item in the cart
    Checks if there's sufficient inventory for the new quantity
    """
    item = get_object_or_404(OrderItems, pk=item_id, Order__User=request.user)

    if request.method == "POST":
        try:
            new_quantity = int(request.POST.get("quantity", 1))

            if new_quantity <= 0:
                item_name = item.Model.Name
                item.delete()
                messages.success(
                    request, f"{item_name} has been removed from your cart."
                )
                item_name = item.Model.Name
                item.delete()
                messages.success(
                    request, f"{item_name} has been removed from your cart."
                )
                return redirect("cart")

            original_quantity = item.ItemQuantity

            item.ItemQuantity = new_quantity
            total_weight = item.calculate_required_weight()

            raw_material = item.InventoryChange.RawMaterial
            sufficient_inventory = raw_material.find_inventory_for_weight(total_weight)

            if sufficient_inventory:
                item.save()
                messages.success(request, f"Quantity updated to {new_quantity}.")
            else:
                item.ItemQuantity = original_quantity
                item.save()
                messages.error(
                    request,
                    f"Not enough inventory available for the requested quantity.",
                )
        except ValueError:
            messages.error(request, "Please enter a valid quantity.")

    return redirect("cart")


@login_required
def checkout(request):
    """
    Checkout - Step 1 - Initialize checkout
    """
    cart_items = get_cart_items(request)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")
    draft_order = get_draft_order(request)
    if not draft_order:
        messages.error(request, "Your cart could not be found.")
        return redirect("cart")
    subtotal = sum(item.ItemPrice for item in cart_items)
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        shipping_method = form.cleaned_data["shipping_method"]
        expedited = form.cleaned_data["expedited"]
        request.session["checkout_shipping_id"] = shipping_method.id
        request.session["checkout_expedited"] = expedited
        return redirect("checkout-confirm")
    default_shipping = Shipping.objects.first()
    shipping_cost = default_shipping.Rate if default_shipping else Decimal("0")

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "form": form,
        "base_total": subtotal + shipping_cost,
    }

    return render(request, "cart/checkout.html", context)


@login_required
def checkout_confirm(request):
    """
    Checkout Step 2 - Confirm order
    """
    cart_items = get_cart_items(request)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")
    draft_order = get_draft_order(request)
    if not draft_order:
        messages.error(request, "Your cart could not be found.")
        return redirect("cart")
    shipping_id = request.session.get("checkout_shipping_id")
    expedited = request.session.get("checkout_expedited", False)
    if not shipping_id:
        messages.error(request, "Please select a shipping method.")
        return redirect("checkout")
    shipping = get_object_or_404(Shipping, pk=shipping_id)
    subtotal = sum(item.ItemPrice * item.ItemQuantity for item in cart_items)
    shipping_details = calculate_shipping(shipping, subtotal)
    shipping_cost = shipping_details["shipping_cost"]
    estimated_ship_date = shipping_details["estimated_ship_date"]
    base_total = subtotal + shipping_cost
    expedited_fee = base_total * Decimal("0.5")
    expedited_total = base_total * Decimal("1.5")
    total = expedited_total if expedited else base_total

    context = {
        "cart_items": cart_items,
        "shipping": shipping,
        "expedited": expedited,
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "base_total": base_total,
        "expedited_fee": expedited_fee,
        "expedited_total": expedited_total,
        "total": total,
        "estimated_ship_date": estimated_ship_date,
    }
    if request.method == "POST":
        draft_order.Shipping = shipping
        draft_order.TotalPrice = expedited_total if expedited else base_total
        draft_order.ExpeditedService = expedited
        draft_order.EstimatedShipDate = estimated_ship_date
        draft_order.save()
        draft_order.update_status(FulfillmentStatus.Status.PENDING_PAYMENT, save=False)
        if "checkout_shipping_id" in request.session:
            del request.session["checkout_shipping_id"]
        if "checkout_expedited" in request.session:
            del request.session["checkout_expedited"]
        messages.success(request, "Your order has been placed successfully!")
        return redirect("order-success", order_id=draft_order.id)

    return render(request, "cart/checkout_confirm.html", context)


@login_required
def order_success(request, order_id):
    """
    Order success page with payment pending status indicator to conditionally render payment instructions
    """
    order = get_object_or_404(Orders, pk=order_id, User=request.user)
    order_items = order.orderitems_set.all().select_related("Model")
    fulfillment_status = order.fulfillmentstatus_set.latest("StatusChangeDate")

    payment_pending = (
        fulfillment_status.OrderStatus == FulfillmentStatus.Status.PENDING_PAYMENT
    )

    context = {
        "order": order,
        "order_items": order_items,
        "status": fulfillment_status,
        "payment_pending": payment_pending,
        "total": order.TotalPrice,
    }

    return render(request, "cart/order_success.html", context)
