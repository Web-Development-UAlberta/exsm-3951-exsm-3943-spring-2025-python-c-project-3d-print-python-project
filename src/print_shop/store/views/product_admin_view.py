from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from store.models import (
    OrderItems,
    Models,
    Materials,
    Filament,
    Orders,
    FulfillmentStatus,
    InventoryChange,
)
from store.forms.order_forms import AdminItemForm
from store.views.cart_checkout_view import get_draft_order
from store.forms.customer_selection_form import CustomerSelectionForm


def is_staff(user):
    """Check if user is staff"""
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def premade_items_list(request):
    """
    List all premade items (admin view)
    """
    premade_items = OrderItems.objects.filter(
        Order__isnull=True, IsCustom=False
    ).select_related("Model", "InventoryChange__RawMaterial__Filament__Material")

    context = {"premade_items": premade_items}

    return render(request, "admin/premade_items_list.html", context)


@login_required
@user_passes_test(is_staff)
def add_premade_item(request):
    """
    Add a new premade item (admin view) with FIFO inventory checks
    """
    available_models = Models.objects.all().order_by("Name")
    available_materials = Materials.objects.all().order_by("Name")
    default_infill = 30
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if request.method == "POST":
        try:
            form = AdminItemForm(request.POST, request.FILES)

            if not form.is_valid():
                if is_ajax:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Form validation failed",
                            "errors": form.errors.get_json_data(),
                        },
                        status=400,
                    )
                return render(
                    request,
                    "admin/premade_item_form.html",
                    {
                        "form": form,
                        "title": "Add Premade Item",
                        "available_models": available_models,
                        "available_materials": available_materials,
                        "default_infill": default_infill,
                    },
                )

            with transaction.atomic():
                item = form.save(commit=False)
                infill_percentage = form.cleaned_data.get("infill_percentage")
                if infill_percentage is not None:
                    item.InfillMultiplier = item.calculate_infill_multiplier(
                        infill_percentage
                    )
                item.IsCustom = False
                item.save()

                required_weight = item.calculate_required_weight()

                available_inventory = (
                    item.InventoryChange.RawMaterial.find_inventory_for_weight(
                        required_weight
                    )
                )

                if not available_inventory:
                    transaction.set_rollback(True)
                    error_msg = "Insufficient inventory available for the selected filament. Please check available stock."
                    if is_ajax:
                        return JsonResponse(
                            {
                                "success": False,
                                "message": error_msg,
                                "errors": {"__all__": [error_msg]},
                            },
                            status=400,
                        )
                    messages.error(request, error_msg)
                    return redirect(request.path_info)

                if item.InventoryChange_id != available_inventory.id:
                    item.InventoryChange = available_inventory
                    item.save()

                success_msg = (
                    f"Premade item '{item.Model.Name}' was created successfully"
                )
                if is_ajax:
                    return JsonResponse(
                        {
                            "success": True,
                            "message": success_msg,
                            "redirect_url": reverse("product-admin-premade-items"),
                        }
                    )
                messages.success(request, success_msg)
                return redirect("product-admin-premade-items")

        except Exception as e:
            error_msg = f"Error creating premade item: {str(e)}"
            if is_ajax:
                return JsonResponse(
                    {"success": False, "message": error_msg}, status=400
                )
            messages.error(request, error_msg)
            return redirect(request.path_info)
    else:
        form = AdminItemForm(initial={"IsCustom": False})

    context = {
        "form": form,
        "title": "Add Premade Item",
        "available_models": available_models,
        "available_materials": available_materials,
        "default_infill": default_infill,
    }

    if is_ajax:
        return JsonResponse(
            {"success": False, "message": "Invalid request", "errors": {}}, status=400
        )

    return render(request, "admin/premade_item_form.html", context)

    context = {
        "form": form,
        "title": "Add Premade Item",
        "available_models": available_models,
        "available_materials": available_materials,
        "default_infill": default_infill,
    }

    return render(request, "admin/premade_item_form.html", context)


@login_required
@user_passes_test(is_staff)
def edit_premade_item(request, pk):
    """
    Edit an existing premade item (admin view)
    """
    item = get_object_or_404(OrderItems, pk=pk, Order__isnull=True, IsCustom=False)
    available_models = Models.objects.all().order_by("Name")
    available_materials = Materials.objects.all().order_by("Name")
    default_infill = (
        int(item.InfillMultiplier * (item.Model.BaseInfill * 100)) if item.Model else 30
    )

    if request.method == "POST":
        form = AdminItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.IsCustom = False
            item.save()
            messages.success(
                request, f"Premade item '{item.Model.Name}' was updated successfully"
            )
            return redirect("product-admin-premade-items")
    else:
        form = AdminItemForm(instance=item)

    context = {
        "form": form,
        "title": "Edit Premade Item",
        "available_models": available_models,
        "available_materials": available_materials,
        "default_infill": default_infill,
    }

    return render(request, "admin/premade_item_form.html", context)


@login_required
@user_passes_test(is_staff)
def delete_premade_item(request, pk):
    """
    Delete a premade item (admin view)
    """
    item = get_object_or_404(OrderItems, pk=pk, Order__isnull=True, IsCustom=False)

    if request.method == "POST":
        name = item.Model.Name
        item.delete()
        messages.success(request, f"Premade item '{name}' was deleted successfully")
        return redirect("product-admin-premade-items")

    context = {"item": item}

    return render(request, "admin/premade_item_confirm_delete.html", context)


@login_required
@user_passes_test(is_staff)
def generate_quote(request):
    """
    Generate a custom order quote for a customer
    This allows store owners to create quotes on behalf of a customer
    Because of how we create carts, we need to temporarily set the request.user to the customer.
    """
    if request.method == "POST":
        form = AdminItemForm(request.POST)
        customer_form = CustomerSelectionForm(request.POST)

        if form.is_valid() and customer_form.is_valid():
            customer = customer_form.cleaned_data["customer"]
            original_user = request.user
            request.user = customer

            try:
                draft_order = get_draft_order(request)

                if not draft_order:
                    draft_order = Orders.objects.create(
                        User=customer,
                        TotalPrice=0,
                        ExpeditedService=False,
                        Shipping=None,
                    )
            finally:
                request.user = original_user

            item = form.save(commit=False)
            item.IsCustom = True
            item.Order = draft_order
            item.save()
            messages.success(
                request,
                f"Quote for '{item.Model.Name}' was generated successfully for {customer.username}",
            )
            return redirect("orders-list")
    else:
        form = AdminItemForm(initial={"IsCustom": True})
        customer_form = CustomerSelectionForm()

    context = {
        "form": form,
        "customer_form": customer_form,
        "title": "Generate Customer Quote",
    }

    return render(request, "admin/quote_form.html", context)
