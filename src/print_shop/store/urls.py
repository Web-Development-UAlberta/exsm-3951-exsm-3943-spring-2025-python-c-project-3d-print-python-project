from django.urls import path
from .views.CRUD import models_view
from .views.CRUD import suppliers_view

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
]