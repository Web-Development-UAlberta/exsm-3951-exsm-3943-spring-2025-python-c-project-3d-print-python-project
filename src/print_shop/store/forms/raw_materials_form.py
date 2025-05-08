from django import forms
from ..models import RawMaterials

class RawMaterialsForm(forms.ModelForm):
    class Meta:
        model = RawMaterials
        fields = "__all__"