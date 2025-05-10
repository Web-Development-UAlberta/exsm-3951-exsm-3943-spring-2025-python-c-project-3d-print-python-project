from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
                material_id=selected_material,
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
                material_id=selected_material,
                rawmaterials__id__in=sufficient_raw_materials,
            )
            .distinct()
            .order_by("Name")
        )

        if selected_filament:
            current_inventory = current_inventory.filter(
                RawMaterial__Filament_id=selected_filament
            )

    if request.method == "POST":
        form = CustomOrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.Model = model
            order_item.IsCustom = True
            order_item.save()
            messages.success(request, f"{model.Name} has been added to your cart.")
            return redirect("custom-gallery")
    else:
        form = CustomOrderItemForm(model=model, initial={"Model": model})
        form.fields["InventoryChange"].queryset = current_inventory

    context = {
        "model": model,
        "form": form,
        "current_inventory": current_inventory,
        "available_materials": available_materials,
        "available_filaments": available_filaments,
        "selected_material": selected_material,
        "selected_filament": selected_filament,
    }

    return render(request, "gallery/model_detail.html", context)


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

            draft_order, created = Orders.objects.get_or_create(
                User=request.user,
                defaults={
                    "TotalPrice": 0,
                    "ExpeditedService": False,
                },
            )

            if created:
                FulfillmentStatus.objects.create(
                    Order=draft_order, OrderStatus=FulfillmentStatus.Status.DRAFT
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
