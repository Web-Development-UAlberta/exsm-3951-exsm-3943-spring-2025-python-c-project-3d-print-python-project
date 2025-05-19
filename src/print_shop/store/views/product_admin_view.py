from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
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
from store.forms.order_forms import CustomOrderItemForm
from store.views.gallery_view import get_available_inventory_items
from decimal import Decimal


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
    ).select_related("Model", "InventoryChange__RawMaterial__Filament__Material").order_by(
        "Model__Name",
        "InventoryChange__RawMaterial__Filament__Material__Name",
        "InventoryChange__RawMaterial__Filament__Name"
    )

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
    quantity = 1
    infill_percentage = 30
    all_models = Models.objects.order_by("Name")
    customer_form = CustomerSelectionForm()
    available_items = []
    available_materials = []
    available_filaments = []
    model = None
    form = None

    context = {
        "all_models": all_models,
        "customer_form": customer_form,
        "default_infill": 30,
    }
    if (
        request.method == "GET"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
        and not request.POST
    ):
        return render(request, "admin/quote_form.html", context)

    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        try:
            customer_id = request.POST.get("customer_id")
            if not customer_id:
                return JsonResponse(
                    {"success": False, "message": "Please select a customer"},
                    status=400,
                )

            customer = get_object_or_404(User, pk=customer_id)

            model_id = request.POST.get("model_id")
            if not model_id:
                return JsonResponse(
                    {"success": False, "message": "Please select a model"},
                    status=400,
                )

            model = get_object_or_404(Models, pk=model_id)

            inventory_id = request.POST.get("inventory_id")
            quantity = int(request.POST.get("ItemQuantity", 1))
            infill_percentage = Decimal(
                request.POST.get("infill_percentage", model.BaseInfill * 100)
            )

            selected_inventory = None
            if inventory_id:
                try:
                    selected_inventory = InventoryChange.objects.get(id=inventory_id)
                except InventoryChange.DoesNotExist:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Selected inventory not found",
                        },
                        status=400,
                    )

            available_items = get_available_inventory_items(
                model=model,
                quantity=quantity,
                infill_percentage=int(infill_percentage),
            )

            selected_item = None
            if selected_inventory:
                selected_item = next(
                    (
                        item
                        for item in available_items
                        if str(item["inventory"].id) == str(inventory_id)
                    ),
                    None,
                )

            if not selected_item and available_items:
                selected_item = available_items[0]
                selected_inventory = selected_item["inventory"]

            if not selected_item or not selected_inventory:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "No inventory available for the selected options",
                    },
                    status=400,
                )

            temp_order_item = OrderItems(
                Model=model,
                InventoryChange=selected_inventory,
                ItemQuantity=quantity,
                IsCustom=True,
            )

            infill_multiplier = temp_order_item.calculate_infill_multiplier(
                infill_percentage
            )
            temp_order_item.InfillMultiplier = infill_multiplier

            total_weight = temp_order_item.calculate_required_weight()

            if not selected_inventory.RawMaterial.find_inventory_for_weight(
                total_weight
            ):
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Insufficient inventory available for the selected options",
                    },
                    status=400,
                )

            original_user = request.user
            request.user = customer

            draft_order = get_draft_order(request) or Orders.objects.create(
                User=customer,
                TotalPrice=0,
                ExpeditedService=False,
                Shipping=None,
            )

            if original_user:
                request.user = original_user

            price_components = temp_order_item.calculate_price_components()

            order_item = OrderItems(
                Model=model,
                InventoryChange=selected_inventory,
                InfillMultiplier=infill_multiplier,
                ItemQuantity=quantity,
                IsCustom=True,
                Order=draft_order,
                TotalWeight=price_components["weight"],
                CostOfGoodsSold=price_components["cost_of_goods"],
                ItemPrice=price_components["price"],
            )
            order_item.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": f"Quote for {model.Name} has been created for {customer.username}.",
                    "redirect_url": reverse("orders-list"),
                }
            )

        except Exception as e:
            error_msg = f"Error creating quote: {str(e)}"
            print(f"Error: {error_msg}")
            return JsonResponse({"success": False, "message": error_msg}, status=400)

    return render(request, "admin/quote_form.html", context)
