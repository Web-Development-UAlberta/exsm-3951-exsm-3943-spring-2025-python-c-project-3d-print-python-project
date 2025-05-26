from django import forms
from store.models import InventoryChange


class InventoryChangeForm(forms.ModelForm):
    class Meta:
        model = InventoryChange
        fields = "__all__"
