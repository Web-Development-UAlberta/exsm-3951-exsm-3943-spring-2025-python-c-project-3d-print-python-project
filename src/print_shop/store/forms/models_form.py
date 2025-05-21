from django import forms
from store.models import Models


class ModelsForm(forms.ModelForm):
    class Meta:
        model = Models
        fields = [
            "Name",
            "Description",
            "FilePath",
            "FixedCost",
            "EstimatedPrintVolume",
            "BaseInfill",
        ]
