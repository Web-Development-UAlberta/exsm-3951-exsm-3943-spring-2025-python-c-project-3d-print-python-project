from django import forms
from ..models import Materials

class MaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = ["Name"]