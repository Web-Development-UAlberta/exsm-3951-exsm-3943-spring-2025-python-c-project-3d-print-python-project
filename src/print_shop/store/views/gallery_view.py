from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
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


def model_detail(request, model_id):
    """
    Detail view for a specific model with material selection
    """
    model = get_object_or_404(Models, pk=model_id)
    quantity = int(request.GET.get("quantity", 1))
    infill_percentage = int(request.GET.get("infill", 30))

    base_infill = model.BaseInfill * 100
    multiplier = infill_percentage / base_infill

    raw_materials = RawMaterials.objects.filter(
        inventorychange__in=InventoryChange.objects.available()
    ).distinct()

    sufficient_raw_materials = []
    for raw_material in raw_materials:
        inventory = raw_material.inventorychange_set.available().first()
        if not inventory:
            continue

        temp_order_item = OrderItems(
            Model=model,
            InventoryChange=inventory,
            InfillMultiplier=multiplier,
            ItemQuantity=quantity,
            IsCustom=True,
        )

        total_weight = temp_order_item.calculate_required_weight()

        sufficient_inventory = raw_material.find_inventory_for_weight(total_weight)
        if sufficient_inventory:
            sufficient_raw_materials.append(raw_material.id)

    current_inventory = (
        InventoryChange.objects.available()
        .filter(RawMaterial_id__in=sufficient_raw_materials)
        .select_related("RawMaterial__Filament__Material")
    )

    available_materials = (
        Materials.objects.filter(
            filament__rawmaterials__id__in=sufficient_raw_materials
        )
        .distinct()
        .order_by("Name")
    )

    available_filaments = Filament.objects.none()

    selected_material = request.GET.get("material")
    selected_filament = request.GET.get("filament")

    if selected_material:
        available_filaments = (
            Filament.objects.filter(
                Material_id=selected_material,
                rawmaterials__id__in=sufficient_raw_materials,
            )
            .distinct()
            .order_by("Name")
        )

        if selected_filament:
            current_inventory = current_inventory.filter(
                RawMaterial__Filament_id=selected_filament
            )
    form = CustomOrderItemForm(model=model, initial={"Model": model})
    form.fields["InventoryChange"].queryset = current_inventory

    if request.method == "POST":
        if selected_filament and current_inventory.exists():
            try:
                best_inventory = current_inventory.first()
                infill_percentage = int(request.POST.get("infill_percentage", 30))
                quantity = int(request.POST.get("ItemQuantity", 1))

                base_infill = model.BaseInfill * 100
                multiplier = infill_percentage / base_infill

                draft_order = get_draft_order(request)

                if not draft_order:
                    draft_order = Orders.objects.create(
                        User=request.user,
                        TotalPrice=0,
                        ExpeditedService=False,
                        Shipping=None,
                    )
                order_item = OrderItems(
                    Model=model,
                    InventoryChange=best_inventory,
                    InfillMultiplier=multiplier,
                    ItemQuantity=quantity,
                    IsCustom=True,
                    Order=draft_order,
                )
                order_item.save()

                messages.success(request, f"{model.Name} has been added to your cart.")
                return redirect("cart")
            except Exception as e:
                messages.error(request, f"Error adding item to cart: {str(e)}")
                print(f"Error: {str(e)}")
        else:
            messages.error(
                request, "Please select a material and color before adding to cart."
            )

    default_infill = int(float(model.BaseInfill) * 100)

    context = {
        "model": model,
        "form": form,
        "current_inventory": current_inventory,
        "available_materials": available_materials,
        "available_filaments": available_filaments,
        "selected_material": selected_material,
        "selected_filament": selected_filament,
        "default_infill": default_infill,
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
        infill_percentage = Decimal(
            request.GET.get("infill", str(int(model.BaseInfill * 100)))
        )
        quantity = int(request.GET.get("quantity", "1"))
        base_infill_percentage = model.BaseInfill * 100
        infill_multiplier = infill_percentage / base_infill_percentage
        base_volume = model.EstimatedPrintVolume * model.BaseInfill
        volume_cm3 = base_volume * infill_multiplier
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
                "model_volume_cm3": Decimal(str(model.EstimatedPrintVolume)),
                "base_infill": (model.BaseInfill * 100).quantize(Decimal("0.01")),
                "effective_infill": infill_percentage.quantize(Decimal("0.01")),
                "density": Decimal(str(inventory.RawMaterial.MaterialDensity)),
                "cost_per_gram": Decimal(str(inventory.UnitCost)).quantize(
                    Decimal("0.0001")
                ),
                "wear_tear": Decimal(
                    str(inventory.RawMaterial.WearAndTearMultiplier)
                ).quantize(Decimal("0.0001")),
                "weight_per_item": (weight / Decimal(str(quantity))).quantize(
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
    with simple sorting by model name, material, and color
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

    context = {
        "premade_items": premade_items,
    }

    return render(request, "gallery/premade_gallery.html", context)


def premade_item_detail(request, item_id):
    """
    Detail view for a specific premade item
    """
    item = get_object_or_404(OrderItems, pk=item_id, Order__isnull=True, IsCustom=False)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to add items to your cart.")
            return redirect("login")

        form = PremadeItemCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            draft_order = get_draft_order(request)

            if not draft_order:
                draft_order = Orders.objects.create(
                    User=request.user,
                    TotalPrice=0,
                    ExpeditedService=False,
                    Shipping=None,
                )

            OrderItems.objects.create(
                Order=draft_order,
                Model=item.Model,
                InventoryChange=item.InventoryChange,
                InfillMultiplier=item.InfillMultiplier,
                ItemQuantity=quantity,
                ItemPrice=item.ItemPrice,
                IsCustom=False,
            )

            messages.success(request, f"{quantity} x {item.Model.Name} added to cart.")
            return redirect("cart")
    else:
        form = PremadeItemCartForm(initial={"item_id": item.id})

    context = {"item": item, "form": form}

    return render(request, "gallery/premade_item_detail.html", context)
