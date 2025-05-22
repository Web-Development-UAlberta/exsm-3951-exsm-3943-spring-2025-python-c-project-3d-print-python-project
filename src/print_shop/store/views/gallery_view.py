from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from store.models import (
    Models,
    InventoryChange,
    OrderItems,
    Filament,
    Materials,
    RawMaterials,
    Orders,
    FulfillmentStatus,
)
from store.forms.order_forms import CustomOrderItemForm, PremadeItemCartForm
from store.views.cart_checkout_view import get_draft_order


def custom_gallery(request):
    """
    Gallery for custom orders where users select a material type first,
    then are shown available filaments in inventory for that material
    """
    models = Models.objects.all().order_by("Name")
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

    available_colors = Filament.objects.none()

    selected_material = request.GET.get("material")

    if selected_material:
        available_colors = (
            Filament.objects.filter(
                Material_id=selected_material,
                rawmaterials__inventorychange__in=current_inventory,
            )
            .distinct()
            .order_by("Name")
        )

    context = {
        "models": models,
        "available_materials": available_materials,
        "available_colors": available_colors,
        "selected_material": selected_material,
    }

    return render(request, "gallery/custom_gallery.html", context)


def get_available_inventory_items(
    model, selected_filament=None, quantity=1, infill_percentage=30
):
    """
    Helper method to get available inventory items with sufficient quantity.
    Returns a list of dictionaries containing inventory and related data.

    Args:
        model: The 3D model being ordered
        selected_filament: Optional filament ID to filter by
        quantity: Number of items being ordered
        infill_percentage: The final infill percentage (e.g., 20 for 20%)
    """
    base_infill = model.BaseInfill * 100
    infill_multiplier = Decimal(infill_percentage) / base_infill

    inventory_items = (
        InventoryChange.objects.available()
        .select_related(
            "RawMaterial", "RawMaterial__Filament", "RawMaterial__Filament__Material"
        )
        .distinct()
    )

    sufficient_items = []

    for inventory in inventory_items:
        if not inventory.RawMaterial or not hasattr(inventory.RawMaterial, "Filament"):
            continue

        if selected_filament and str(inventory.RawMaterial.Filament_id) != str(
            selected_filament
        ):
            continue

        temp_order_item = OrderItems(
            Model=model,
            InventoryChange=inventory,
            InfillMultiplier=infill_multiplier,
            ItemQuantity=quantity,
            IsCustom=True,
        )

        total_weight = temp_order_item.calculate_required_weight()

        if inventory.RawMaterial.find_inventory_for_weight(total_weight):
            sufficient_items.append(
                {
                    "id": inventory.id,
                    "raw_material": inventory.RawMaterial,
                    "inventory": inventory,
                    "weight": total_weight,
                    "filament": inventory.RawMaterial.Filament,
                    "material": inventory.RawMaterial.Filament.Material
                    if inventory.RawMaterial.Filament
                    else None,
                }
            )

    return sufficient_items

@login_required
def model_detail(request, model_id):
    """
    Detail view for a specific model with material selection
    """
    model = get_object_or_404(Models, pk=model_id)
    quantity = int(request.GET.get("quantity", 1))
    infill_percentage = int(request.GET.get("infill", 30))
    selected_material = request.GET.get("material")
    selected_filament = request.GET.get("filament")

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

    form = CustomOrderItemForm(model=model, initial={"Model": model})
    form.fields["InventoryChange"].queryset = InventoryChange.objects.filter(
        id__in=[item["inventory"].id for item in available_items]
    )

    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        try:
            inventory_id = request.POST.get("inventory_id")
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
                        "success": False,
                        "message": "No inventory available for the selected options",
                    },
                    status=400,
                )

            quantity = int(request.POST.get("ItemQuantity", 1))
            infill_percentage = Decimal(
                request.POST.get("infill_percentage", model.BaseInfill * 100)
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
                        "success": False,
                        "message": "Insufficient inventory available for the selected options",
                    },
                    status=400,
                )

            draft_order = get_draft_order(request) or Orders.objects.create(
                User=request.user,
                TotalPrice=0,
                ExpeditedService=False,
                Shipping=None,
            )

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
                    "success": True,
                    "message": f"{model.Name} has been added to your cart.",
                    "redirect_url": reverse("cart"),
                }
            )

        except Exception as e:
            error_msg = f"Error adding item to cart: {str(e)}"
            print(f"Error: {error_msg}")
            return JsonResponse({"success": False, "message": error_msg}, status=400)

    context = {
        "model": model,
        "form": form,
        "available_materials": available_materials,
        "available_filaments": available_filaments,
        "selected_material": selected_material,
        "selected_filament": selected_filament,
        "default_infill": int(model.BaseInfill * 100),
    }

    return render(request, "gallery/model_detail.html", context)


@require_http_methods(["GET"])
def get_filaments_for_material(request, model_id, material_id):
    """
    API endpoint to get filaments for a specific material that have available inventory.
    This is used by the frontend to populate the filament dropdown when a material is selected.
    Uses the same inventory logic as calculate_price to ensure consistency.
    """
    try:
        model = get_object_or_404(Models, pk=model_id)
        material = get_object_or_404(Materials, pk=material_id)
        raw_materials = (
            RawMaterials.objects.filter(
                Filament__Material=material,
                inventorychange__QuantityWeightAvailable__gt=0,
            )
            .select_related("Filament")
            .distinct()
        )

        sufficient_filaments = set()

        for raw_material in raw_materials.order_by("PurchasedDate"):
            temp_order_item = OrderItems(
                Model=model,
                InfillMultiplier=1.0,
                ItemQuantity=1,
                IsCustom=True,
            )

            required_weight = temp_order_item.calculate_required_weight()

            inventory = InventoryChange.objects.find_for_weight(
                required_weight=required_weight,
                safety_margin=Decimal("1.15"),
                raw_material=raw_material,
            )
            if inventory:
                sufficient_filaments.add(raw_material.Filament_id)

        filaments = Filament.objects.filter(id__in=sufficient_filaments).order_by(
            "Name"
        )

        filaments_data = [
            {
                "id": filament.id,
                "name": f"{filament.Name}",
                "color_code": f"#{filament.ColorHexCode}",
            }
            for filament in filaments
        ]

        return JsonResponse(
            {
                "status": "success",
                "filaments": filaments_data,
            }
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@require_http_methods(["GET"])
def calculate_price(request, model_id, filament_id):
    """
    API endpoint to calculate the estimated price based on model, filament, infill, and quantity.
    Uses FIFO inventory management to find the appropriate inventory record.
    """
    try:
        model = get_object_or_404(Models, pk=model_id)
        filament = get_object_or_404(Filament, pk=filament_id)
        base_infill_percentage = model.BaseInfill * 100
        try:
            infill_percentage = Decimal(
                request.GET.get("infill", str(int(base_infill_percentage)))
            )
            infill_percentage = max(
                Decimal("1"), min(Decimal("100"), infill_percentage)
            )
        except (TypeError, ValueError, InvalidOperation):
            infill_percentage = base_infill_percentage

        quantity = int(request.GET.get("quantity", "1"))

        temp_order_item = OrderItems(Model=model)
        infill_multiplier = temp_order_item.calculate_infill_multiplier(
            infill_percentage
        )

        volume_cm3 = model.EstimatedPrintVolume * model.BaseInfill * infill_multiplier
        raw_material = RawMaterials.objects.filter(
            Filament=filament, inventorychange__QuantityWeightAvailable__gt=0
        ).first()

        if not raw_material:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No available inventory for this filament",
                },
                status=400,
            )

        weight_per_item = volume_cm3 * raw_material.MaterialDensity
        required_weight = int(weight_per_item * quantity * Decimal("1.15"))

        inventory = InventoryChange.objects.find_for_weight(
            required_weight=required_weight,
            safety_margin=Decimal("1.0"),
            raw_material=raw_material,
        )

        if not inventory:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Not enough inventory available for the selected options",
                },
                status=400,
            )

        temp_order_item = OrderItems(
            Model=model,
            InventoryChange=inventory,
            InfillMultiplier=infill_multiplier,
            ItemQuantity=quantity,
            IsCustom=True,
        )
        price_components = temp_order_item.calculate_price_components()
        weight = price_components["weight"]
        cost_of_goods = price_components["cost_of_goods"]
        price = price_components["price"]

        response_data = {
            "status": "success",
            "price": price.quantize(Decimal("0.01")),
            "weight": weight,
            "cost_of_goods": cost_of_goods.quantize(Decimal("0.01")),
            "infill": infill_percentage,
            "quantity": quantity,
            "inventory_id": inventory.id,
            "debug": {
                "model_volume_cm3": Decimal(model.EstimatedPrintVolume),
                "base_infill": (model.BaseInfill * 100).quantize(Decimal("0.01")),
                "effective_infill": infill_percentage.quantize(Decimal("0.01")),
                "density": inventory.RawMaterial.MaterialDensity,
                "cost_per_gram": inventory.UnitCost.quantize(Decimal("0.0001")),
                "wear_tear": inventory.RawMaterial.WearAndTearMultiplier.quantize(
                    Decimal("0.0001")
                ),
                "weight_per_item": (weight / Decimal(quantity)).quantize(
                    Decimal("0.01")
                ),
                "material_cost": str(price_components["material_cost"]),
                "fixed_cost": str(price_components["fixed_cost"]),
            },
        }

        return JsonResponse(response_data, json_dumps_params={"default": str})

    except Exception as e:
        import traceback

        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def premade_gallery(request):
    """
    Gallery for premade items (OrderItems with no Order assigned)
    Groups identical items by model, material, color, and price
    """
    premade_items = (
        OrderItems.objects.filter(Order__isnull=True, IsCustom=False)
        .select_related(
            "Model",
            "InventoryChange__RawMaterial__Filament__Material",
            "InventoryChange__RawMaterial__Filament",
        )
        .order_by(
            "Model__Name",
            "InventoryChange__RawMaterial__Filament__Material__Name",
            "InventoryChange__RawMaterial__Filament__Name",
        )
    )

    grouped_items = {}
    for item in premade_items:
        infill_percentage = round(item.Model.BaseInfill * item.InfillMultiplier * 100)
        key = (
            item.Model.id,
            item.InventoryChange.RawMaterial.Filament.Material.id,
            item.InventoryChange.RawMaterial.Filament.id,
            str(item.ItemPrice),
            infill_percentage,
        )

        if key not in grouped_items:
            grouped_items[key] = {
                "model": item.Model,
                "material": item.InventoryChange.RawMaterial.Filament.Material,
                "filament": item.InventoryChange.RawMaterial.Filament,
                "price": item.ItemPrice,
                "infill_percentage": infill_percentage,
                "quantity": 1,
                "first_item": item,
            }
        else:
            grouped_items[key]["quantity"] += 1

    context = {
        "grouped_items": grouped_items.values(),
    }

    return render(request, "gallery/premade_gallery.html", context)

@login_required
def premade_item_detail(request, item_id):
    """
    Detail view for a specific premade item
    """
    item = get_object_or_404(
        OrderItems.objects.select_related(
            "Model",
            "InventoryChange__RawMaterial__Filament__Material",
            "InventoryChange__RawMaterial__Filament",
        ),
        pk=item_id,
        Order__isnull=True,
        IsCustom=False,
    )

    available_quantity = OrderItems.objects.filter(
        Model=item.Model,
        InventoryChange__RawMaterial__Filament=item.InventoryChange.RawMaterial.Filament,
        Order__isnull=True,
        IsCustom=False,
        ItemPrice=item.ItemPrice,
    ).count()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to add items to your cart.")
            return redirect("login")

        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity > available_quantity:
                messages.error(request, f"Cannot add {quantity} items. Only {available_quantity} in stock.")
                return redirect("premade-item-detail", item_id=item_id)
            quantity = max(1, min(quantity, available_quantity))

            draft_order = get_draft_order(request)
            if not draft_order:
                draft_order = Orders.objects.create(
                    User=request.user,
                    TotalPrice=0,
                    ExpeditedService=False,
                    Shipping=None,
                )

            items_to_add = OrderItems.objects.filter(
                Model=item.Model,
                InventoryChange__RawMaterial__Filament=item.InventoryChange.RawMaterial.Filament,
                Order__isnull=True,
                IsCustom=False,
                ItemPrice=item.ItemPrice,
            ).order_by("id")[:quantity]

            if not items_to_add.exists():
                messages.error(request, "This item is no longer available.")
                return redirect("premade-gallery")

            for item_to_add in items_to_add:
                item_to_add.Order = draft_order
                item_to_add.save()

            draft_order.TotalPrice = sum(
                item.ItemPrice * item.ItemQuantity
                for item in draft_order.orderitems_set.all()
            )
            draft_order.save()

            messages.success(request, f"{quantity} x {item.Model.Name} added to cart.")
            return redirect("cart")

        except (ValueError, Exception) as e:
            messages.error(
                request, "An error occurred while adding the item to your cart."
            )
            return redirect("premade-item-detail", item_id=item_id)

    infill_percentage = round(item.Model.BaseInfill * item.InfillMultiplier * 100)

    context = {
        "item": item,
        "available_quantity": available_quantity,
        "infill_percentage": infill_percentage,
    }

    return render(request, "gallery/premade_item_detail.html", context)
