from django import forms
from store.models import Materials


class MaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = ["Name"]
