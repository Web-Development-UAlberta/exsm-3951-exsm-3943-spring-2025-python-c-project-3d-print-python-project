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
    premade_items = (
        OrderItems.objects.filter(Order__isnull=True, IsCustom=False)
        .select_related("Model", "InventoryChange__RawMaterial__Filament__Material")
        .order_by(
            "Model__Name",
            "InventoryChange__RawMaterial__Filament__Material__Name",
            "InventoryChange__RawMaterial__Filament__Name",
        )
    )

    context = {"premade_items": premade_items}

    return render(request, "admin/premade_items_list.html", context)


@login_required
@user_passes_test(is_staff)
def add_premade_item(request):
    """
    Add a new premade item (admin view) with FIFO inventory checks
    """
    selected_model = request.GET.get("model")
    selected_material = request.GET.get("material")
    selected_filament = request.GET.get("filament")
    infill_percentage = int(request.GET.get("infill", 30))
    all_models = Models.objects.order_by("Name")

    available_items = []
    available_materials = []
    available_filaments = []
    
    if selected_model:
        model = get_object_or_404(Models, pk=selected_model)
        available_items = get_available_inventory_items(
            model=model,
            selected_filament=selected_filament,
            quantity=1,
            infill_percentage=infill_percentage,
        )
        
        available_materials = list(
            {item["material"] for item in available_items if item["material"]}
        )
        available_filaments = list(
            {item["filament"] for item in available_items if item["filament"]}
        )
        
        if selected_material:
            available_filaments = [
                f
                for f in available_filaments
                if str(f.Material_id) == str(selected_material)
            ]
    else:
        current_inventory = InventoryChange.objects.available().select_related(
            "RawMaterial__Filament__Material"
        )
        available_materials = (
            Materials.objects.filter(
                filament__rawmaterials__inventorychange__in=current_inventory
            )
            .distinct()
            .order_by("Name")
        )
    
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    
    if request.method == "POST" and is_ajax:
        try:
            model_id = request.POST.get("Model")
            inventory_id = request.POST.get("InventoryChange")
            infill_multiplier = request.POST.get("InfillMultiplier")
            calculated_price = request.POST.get("calculated_price")
            
            if not model_id:
                return JsonResponse(
                    {"status": "error", "message": "Please select a model"},
                    status=400,
                )
                
            model = get_object_or_404(Models, pk=model_id)
            
            infill_multiplier = Decimal(infill_multiplier)
            infill_percentage = int(infill_multiplier * model.BaseInfill * 100)
            
            available_items = get_available_inventory_items(
                model=model,
                quantity=1,
                infill_percentage=infill_percentage,
            )
            
            if not available_items:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "No inventory available for the selected model",
                    },
                    status=400,
                )
            
            selected_item = None
            if inventory_id:
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
                
            if not selected_item:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "No inventory available for the selected options",
                    },
                    status=400,
                )
                
            selected_inventory = selected_item["inventory"]
            temp_order_item = OrderItems(
                Model=model,
                InventoryChange=selected_inventory,
                ItemQuantity=1,
                IsCustom=False,
                InfillMultiplier=infill_multiplier,
            )
            
            total_weight = temp_order_item.calculate_required_weight()
            
            if not selected_inventory.RawMaterial.find_inventory_for_weight(total_weight):
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Insufficient inventory available for the selected options",
                    },
                    status=400,
                )
                
            price_components = temp_order_item.calculate_price_components()
            
            order_item = OrderItems(
                Model=model,
                InventoryChange=selected_inventory,
                InfillMultiplier=infill_multiplier,
                ItemQuantity=1,
                IsCustom=False,
                TotalWeight=price_components["weight"],
                CostOfGoodsSold=price_components["cost_of_goods"],
                ItemPrice=price_components["price"],
            )
            order_item.save()
            
            return JsonResponse(
                {
                    "status": "success",
                    "message": f"Premade item '{model.Name}' was created successfully",
                    "redirect_url": reverse("product-admin-premade-items"),
                }
            )
            
        except Exception as e:
            error_msg = f"Error creating premade item: {str(e)}"
            return JsonResponse({"status": "error", "message": error_msg}, status=400)
    
    form = AdminItemForm(initial={"IsCustom": False})
    
    context = {
        "form": form,
        "title": "Add Premade Item",
        "all_models": all_models,
        "available_materials": available_materials,
        "available_filaments": available_filaments,
        "selected_model": selected_model,
        "selected_material": selected_material,
        "selected_filament": selected_filament,
        "default_infill": int(model.BaseInfill * 100) if selected_model else infill_percentage,
    }
    
    if selected_model:
        model = get_object_or_404(Models, pk=selected_model)
        context["model"] = model
    
    return render(request, "admin/premade_item_form.html", context)


@login_required
@user_passes_test(is_staff)
def edit_premade_item(request, pk):
    """
    Edit an existing premade item (admin view)
    Uses the same inventory selection logic as the add_premade_item view
    """
    item = get_object_or_404(OrderItems, pk=pk, Order__isnull=True, IsCustom=False)
    
    selected_model = request.GET.get("model", str(item.Model_id) if item.Model else None)
    selected_material = request.GET.get("material", str(item.InventoryChange.RawMaterial.Filament.Material_id) if item.InventoryChange else None)
    selected_filament = request.GET.get("filament", str(item.InventoryChange.RawMaterial.Filament_id) if item.InventoryChange else None)
    infill_percentage = int(request.GET.get("infill", int(item.InfillMultiplier * (item.Model.BaseInfill * 100)) if item.Model else 30))
    
    all_models = Models.objects.order_by("Name")
    
    available_items = []
    available_materials = []
    available_filaments = []
    
    if selected_model:
        model = get_object_or_404(Models, pk=selected_model)
        available_items = get_available_inventory_items(
            model=model,
            selected_filament=selected_filament,
            quantity=1,
            infill_percentage=infill_percentage,
        )
        
        available_materials = list(
            {item["material"] for item in available_items if item["material"]}
        )
        available_filaments = list(
            {item["filament"] for item in available_items if item["filament"]}
        )
        
        if selected_material:
            available_filaments = [
                f
                for f in available_filaments
                if str(f.Material_id) == str(selected_material)
            ]
    else:
        current_inventory = InventoryChange.objects.available().select_related(
            "RawMaterial__Filament__Material"
        )
        available_materials = (
            Materials.objects.filter(
                filament__rawmaterials__inventorychange__in=current_inventory
            )
            .distinct()
            .order_by("Name")
        )
    
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    
    if request.method == "POST" and is_ajax:
        try:
            model_id = request.POST.get("Model")
            inventory_id = request.POST.get("InventoryChange")
            infill_multiplier = request.POST.get("InfillMultiplier")
            calculated_price = request.POST.get("calculated_price")
            
            if not model_id:
                return JsonResponse(
                    {"status": "error", "message": "Please select a model"},
                    status=400,
                )
                
            model = get_object_or_404(Models, pk=model_id)
            
            infill_multiplier = Decimal(infill_multiplier)
            infill_percentage = int(infill_multiplier * model.BaseInfill * 100)
            
            available_items = get_available_inventory_items(
                model=model,
                quantity=1,
                infill_percentage=infill_percentage,
            )
            
            if not available_items:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "No inventory available for the selected model",
                    },
                    status=400,
                )
            
            selected_item = None
            if inventory_id:
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
                
            if not selected_item:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "No inventory available for the selected options",
                    },
                    status=400,
                )
                
            selected_inventory = selected_item["inventory"]
            temp_order_item = OrderItems(
                Model=model,
                InventoryChange=selected_inventory,
                ItemQuantity=1,
                IsCustom=False,
                InfillMultiplier=infill_multiplier,
            )
            
            total_weight = temp_order_item.calculate_required_weight()
            
            if not selected_inventory.RawMaterial.find_inventory_for_weight(total_weight):
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Insufficient inventory available for the selected options",
                    },
                    status=400,
                )
                
            price_components = temp_order_item.calculate_price_components()
            
            item.Model = model
            item.InventoryChange = selected_inventory
            item.InfillMultiplier = infill_multiplier
            item.TotalWeight = price_components["weight"]
            item.CostOfGoodsSold = price_components["cost_of_goods"]
            item.ItemPrice = price_components["price"]
            item.save()
            
            return JsonResponse(
                {
                    "status": "success",
                    "message": f"Premade item '{model.Name}' was updated successfully",
                    "redirect_url": reverse("product-admin-premade-items"),
                }
            )
            
        except Exception as e:
            error_msg = f"Error updating premade item: {str(e)}"
            return JsonResponse({"status": "error", "message": error_msg}, status=400)
    
    form = AdminItemForm(instance=item)
    
    context = {
        "form": form,
        "title": "Edit Premade Item",
        "all_models": all_models,
        "available_materials": available_materials,
        "available_filaments": available_filaments,
        "selected_model": selected_model,
        "selected_material": selected_material,
        "selected_filament": selected_filament,
        "default_infill": infill_percentage,
        "item": item,
    }
    
    if selected_model:
        model = get_object_or_404(Models, pk=selected_model)
        context["model"] = model
    
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
    infill_percentage = int(request.GET.get("infill", 30))
    selected_model = request.GET.get("model")
    selected_material = request.GET.get("material")
    selected_filament = request.GET.get("filament")

    all_models = Models.objects.order_by("Name")
    customer_form = CustomerSelectionForm()

    available_items = []
    available_materials = []
    available_filaments = []

    if selected_model:
        model = get_object_or_404(Models, pk=selected_model)
        available_items = get_available_inventory_items(
            model=model,
            selected_filament=selected_filament,
            quantity=quantity,
            infill_percentage=infill_percentage,
        )

        available_materials = list(
            {item["material"] for item in available_items if item["material"]}
        )
        available_filaments = list(
            {item["filament"] for item in available_items if item["filament"]}
        )

        if selected_material:
            available_filaments = [
                f
                for f in available_filaments
                if str(f.Material_id) == str(selected_material)
            ]
    else:
        current_inventory = InventoryChange.objects.available().select_related(
            "RawMaterial__Filament__Material"
        )
        available_materials = (
            Materials.objects.filter(
                filament__rawmaterials__inventorychange__in=current_inventory
            )
            .distinct()
            .order_by("Name")
        )

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
                    {"status": "error", "message": "Please select a customer"},
                    status=400,
                )

            customer = get_object_or_404(User, pk=customer_id)
            model_id = request.POST.get("model_id")
            if not model_id:
                return JsonResponse(
                    {"status": "error", "message": "Please select a model"},
                    status=400,
                )

            model = get_object_or_404(Models, pk=model_id)

            inventory_id = request.POST.get("inventory_id")
            quantity = 1
            infill_percentage = Decimal(
                request.POST.get("infill_percentage", model.BaseInfill * 100)
            )
            available_items = get_available_inventory_items(
                model=model,
                quantity=quantity,
                infill_percentage=int(infill_percentage),
            )
            selected_item = None

            if inventory_id:
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

            if not selected_item:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "No inventory available for the selected options",
                    },
                    status=400,
                )

            selected_inventory = selected_item["inventory"]
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
                        "status": "error",
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

            calculated_price = request.POST.get("calculated_price")

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
                    "status": "success",
                    "message": f"Quote for {model.Name} has been created for {customer.username}.",
                    "redirect_url": reverse("orders-list"),
                }
            )

        except Exception as e:
            error_msg = f"Error creating quote: {str(e)}"
            return JsonResponse({"status": "error", "message": error_msg}, status=400)

    context = {
        "all_models": all_models,
        "customer_form": customer_form,
        "available_materials": available_materials,
        "available_filaments": available_filaments,
        "selected_model": selected_model,
        "selected_material": selected_material,
        "selected_filament": selected_filament,
        "quantity": quantity,
        "default_infill": int(model.BaseInfill * 100)
        if selected_model
        else infill_percentage,
    }
    if selected_model:
        model = get_object_or_404(Models, pk=selected_model)
        context["model"] = model

    return render(request, "admin/quote_form.html", context)
