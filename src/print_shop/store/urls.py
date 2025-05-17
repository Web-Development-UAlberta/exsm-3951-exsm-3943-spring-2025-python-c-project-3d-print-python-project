from django.urls import path
from django.contrib.auth import views as auth_views
from store.views.CRUD import models_view
from store.views.CRUD import suppliers_view
from store.views.CRUD import materials_view
from store.views.CRUD import filament_view
from store.views.CRUD import raw_materials_view
from store.views.CRUD import shipping_view
from store.views.CRUD import fulfillment_status_view
from store.views.CRUD import inventory_change_view
from store.views.CRUD import user_profiles_view
from store.views.CRUD import orders_view
from store.views.CRUD import order_items_view
from store.views import gallery_view
from store.views import product_admin_view
from store.views import cart_checkout_view
from store.views import home_page_view
from store.views import order_tracking_view

urlpatterns = [
    # Home Page URL
    path("", home_page_view.home_page_view, name="home"),
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
    # Fulfillment Status URLs
    path(
        "fulfillment-status/",
        fulfillment_status_view.fulfillment_status_list,
        name="fulfillment-status-list",
    ),
    path(
        "fulfillment-status/add/",
        fulfillment_status_view.add_fulfillment_status,
        name="add-fulfillment-status",
    ),
    path(
        "fulfillment-status/edit/<int:pk>/",
        fulfillment_status_view.edit_fulfillment_status,
        name="edit-fulfillment-status",
    ),
    path(
        "fulfillment-status/delete/<int:pk>/",
        fulfillment_status_view.delete_fulfillment_status,
        name="delete-fulfillment-status",
    ),
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", user_profiles_view.register, name="register"),
    # User Profile URLs - Customer views
    path("profile/", user_profiles_view.view_profile, name="view-profile"),
    path("profile/edit/", user_profiles_view.edit_profile, name="edit-profile"),
    path("profile/change-password/", user_profiles_view.change_password, name="change-password"),
    # User Profile URLs - Admin views
    path(
        "user-profiles/", user_profiles_view.user_profile_list, name="user-profile-list"
    ),
    path(
        "user-profiles/<int:pk>/",
        user_profiles_view.user_profile_detail,
        name="user-profile-detail",
    ),
    path(
        "user-profiles/add/",
        user_profiles_view.add_user_profile,
        name="add-user-profile",
    ),
    path(
        "user-profiles/add-staff/",
        user_profiles_view.add_staff_user,
        name="add-staff-user",
    ),
    path(
        "user-profiles/edit/<int:pk>/",
        user_profiles_view.edit_user_profile,
        name="edit-user-profile",
    ),
    path(
        "user-profiles/delete/<int:pk>/",
        user_profiles_view.delete_user_profile,
        name="delete-user-profile",
    ),
    # Order URLs
    path("orders/", orders_view.orders_list, name="orders-list"),
    path("orders/add/", orders_view.add_order, name="add-order"),
    path("orders/edit/<int:pk>/", orders_view.edit_order, name="edit-order"),
    path("orders/delete/<int:pk>/", orders_view.delete_order, name="delete-order"),
    # Order Items URLs
    path("order-items/", order_items_view.order_items_list, name="order-items-list"),
    path("order-items/add/", order_items_view.add_order_item, name="add-order-item"),
    path(
        "order-items/edit/<int:pk>/",
        order_items_view.edit_order_item,
        name="edit-order-item",
    ),
    path(
        "order-items/delete/<int:pk>/",
        order_items_view.delete_order_item,
        name="delete-order-item",
    ),
    # Gallery URLs
    path("gallery/custom/", gallery_view.custom_gallery, name="custom-gallery"),
    path(
        "gallery/model/<int:model_id>/", gallery_view.model_detail, name="model-detail"
    ),
    path("gallery/premade/", gallery_view.premade_gallery, name="premade-gallery"),
    path(
        "gallery/premade/<int:item_id>/",
        gallery_view.premade_item_detail,
        name="premade-item-detail",
    ),
    # API URLs for the customized item to get available filaments for a material
    path(
        "store/api/model/<int:model_id>/material/<int:material_id>/filaments/",
        gallery_view.get_filaments_for_material,
        name="get-filaments-for-material",
    ),
    path(
        "store/api/model/<int:model_id>/filament/<int:filament_id>/calculate-price/",
        gallery_view.calculate_price,
        name="calculate-price",
    ),
    # Cart and Checkout URLs
    path("cart/", cart_checkout_view.cart_view, name="cart"),
    path(
        "cart/remove/<int:item_id>/",
        cart_checkout_view.remove_from_cart,
        name="remove-from-cart",
    ),
    path(
        "cart/update/<int:item_id>/",
        cart_checkout_view.update_cart_item,
        name="update-cart-item",
    ),
    path("checkout/", cart_checkout_view.checkout, name="checkout"),
    path(
        "checkout/confirm/",
        cart_checkout_view.checkout_confirm,
        name="checkout-confirm",
    ),
    path(
        "orders/success/<int:order_id>/",
        cart_checkout_view.order_success,
        name="order-success",
    ),
    # Order Tracking URLs
    path("orders/tracking/", order_tracking_view.order_tracking, name="order_tracking"),
    path("orders/details/<int:order_id>/", order_tracking_view.order_details, name="order_details"),
    # Product Admin URLs (for store staff to manage premade items)
    path(
        "product-admin/premade/",
        product_admin_view.premade_items_list,
        name="product-admin-premade-items",
    ),
    path(
        "product-admin/premade/add/",
        product_admin_view.add_premade_item,
        name="product-admin-add-premade",
    ),
    path(
        "product-admin/premade/edit/<int:pk>/",
        product_admin_view.edit_premade_item,
        name="product-admin-edit-premade",
    ),
    path(
        "product-admin/premade/delete/<int:pk>/",
        product_admin_view.delete_premade_item,
        name="product-admin-delete-premade",
    ),
    # Quote Generation URL
    path(
        "product-admin/quote/generate/",
        product_admin_view.generate_quote,
        name="product-admin-generate-quote",
    ),
]
