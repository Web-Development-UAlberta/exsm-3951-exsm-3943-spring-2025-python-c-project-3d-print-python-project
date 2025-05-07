from django.urls import path
from .views.CRUD import models_view

urlpatterns = [
    path("", models_view.models_list, name="models-list"),
    path("models/", models_view.models_list, name="models-list"),
    path("models/add/", models_view.add_model, name="add-model"),
    path("models/edit/<int:pk>/", models_view.edit_model, name="edit-model"),
    path("models/delete/<int:pk>/", models_view.delete_model, name="delete-model"),
]