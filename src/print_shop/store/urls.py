from django.urls import path
from .views.CRUD import models_view
from .views.CRUD import suppliers_view
from .views.CRUD import materials_view

urlpatterns = [
    path("", models_view.models_list, name="models-list"),
    path("models/", models_view.models_list, name="models-list"),
    path("models/add/", models_view.add_model, name="add-model"),
    path("models/edit/<int:pk>/", models_view.edit_model, name="edit-model"),
    path("models/delete/<int:pk>/", models_view.delete_model, name="delete-model"),

    path("suppliers/", suppliers_view.supplier_list, name="suppliers-list"),
    path("suppliers/add/", suppliers_view.add_supplier, name="add-supplier"),
    path("suppliers/edit/<int:pk>/", suppliers_view.edit_supplier, name="edit-supplier"),
    path("suppliers/delete/<int:pk>/", suppliers_view.delete_supplier, name="delete-supplier"),

    path("materials/", materials_view.materials_list, name="materials-list"),
    path("materials/add/", materials_view.add_material, name="add-material"),
    path("materials/edit/<int:pk>/", materials_view.edit_material, name="edit-material"),
    path("materials/delete/<int:pk>/", materials_view.delete_material, name="delete-material"),
]