from django import forms
from store.models import RawMaterials


class RawMaterialsForm(forms.ModelForm):
    class Meta:
        model = RawMaterials
        fields = "__all__"
