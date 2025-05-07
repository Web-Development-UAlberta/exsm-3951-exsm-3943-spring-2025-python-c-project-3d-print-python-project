from django.urls import path
from .views.CRUD import models_view
from .views.CRUD import suppliers_view
from .views.CRUD import materials_view
from .views.CRUD import filament_view
from .views.CRUD import raw_materials_view
from .views.CRUD import shipping_view
from .views.CRUD import fulfillment_status_view
from .views.CRUD import inventory_change_view

urlpatterns = [
    path("", models_view.models_list, name="models-list"),
    # 3D Models URLs
    path("models/", models_view.models_list, name="models-list"),
    path("models/add/", models_view.add_model, name="add-model"),
    path("models/edit/<int:pk>/", models_view.edit_model, name="edit-model"),
    path("models/delete/<int:pk>/", models_view.delete_model, name="delete-model"),
    # Supplier URLs
    path("suppliers/", suppliers_view.supplier_list, name="suppliers-list"),
    path("suppliers/add/", suppliers_view.add_supplier, name="add-supplier"),
    path(
        "suppliers/edit/<int:pk>/", suppliers_view.edit_supplier, name="edit-supplier"
    ),
    path(
        "suppliers/delete/<int:pk>/",
        suppliers_view.delete_supplier,
        name="delete-supplier",
    ),
    # Material URLs
    path("materials/", materials_view.materials_list, name="materials-list"),
    path("materials/add/", materials_view.add_material, name="add-material"),
    path(
        "materials/edit/<int:pk>/", materials_view.edit_material, name="edit-material"
    ),
    path(
        "materials/delete/<int:pk>/",
        materials_view.delete_material,
        name="delete-material",
    ),
    # Filament URLs
    path("filaments/", filament_view.filament_list, name="filament-list"),
    path("filaments/add/", filament_view.add_filament, name="add-filament"),
    path("filaments/edit/<int:pk>/", filament_view.edit_filament, name="edit-filament"),
    path(
        "filaments/delete/<int:pk>/",
        filament_view.delete_filament,
        name="delete-filament",
    ),
    # Raw Material URLs
    path(
        "raw-materials/",
        raw_materials_view.raw_materials_list,
        name="raw-materials-list",
    ),
    path(
        "raw-materials/add/",
        raw_materials_view.add_raw_material,
        name="add-raw-material",
    ),
    path(
        "raw-materials/edit/<int:pk>/",
        raw_materials_view.edit_raw_material,
        name="edit-raw-material",
    ),
    path(
        "raw-materials/delete/<int:pk>/",
        raw_materials_view.delete_raw_material,
        name="delete-raw-material",
    ),
    # Inventory URLs
    path(
        "inventory/current",
        inventory_change_view.current_inventory_levels,
        name="current-inventory",
    ),
    path(
        "inventory/all",
        inventory_change_view.inventory_change_list,
        name="inventory-change-list",
    ),
    path(
        "inventory/<int:pk>/",
        inventory_change_view.inventory_change_detail,
        name="inventory-change-detail",
    ),
    path(
        "inventory/add/",
        inventory_change_view.add_inventory_change,
        name="add-inventory-change",
    ),
    path(
        "inventory/edit/<int:pk>/",
        inventory_change_view.edit_inventory_change,
        name="edit-inventory-change",
    ),
    path(
        "inventory/delete/<int:pk>/",
        inventory_change_view.delete_inventory_change,
        name="delete-inventory-change",
    ),
    # Shipping URLs
    path("shipping/", shipping_view.shipping_list, name="shipping-list"),
    path("shipping/add/", shipping_view.add_shipping, name="add-shipping"),
    path("shipping/edit/<int:pk>/", shipping_view.edit_shipping, name="edit-shipping"),
    path(
        "shipping/delete/<int:pk>/",
        shipping_view.delete_shipping,
        name="delete-shipping",
    ),
    # Fulfillment Status URLs disabled until Orders forms/templates are created
    # path("fulfillment-status/", fulfillment_status_view.fulfillment_status_list, name="fulfillment-status-list"),
    # path("fulfillment-status/add/", fulfillment_status_view.add_fulfillment_status, name="add-fulfillment-status"),
    # path("fulfillment-status/edit/<int:pk>/", fulfillment_status_view.edit_fulfillment_status, name="edit-fulfillment-status"),
    # path("fulfillment-status/delete/<int:pk>/", fulfillment_status_view.delete_fulfillment_status, name="delete-fulfillment-status"),
]
