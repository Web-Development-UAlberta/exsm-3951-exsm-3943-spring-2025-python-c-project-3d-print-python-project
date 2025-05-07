from django import forms
from ..models import Filament

class FilamentForm(forms.ModelForm):
    class Meta:
        model = Filament
        fields = ["Name", "Material", "ColorHexCode"]