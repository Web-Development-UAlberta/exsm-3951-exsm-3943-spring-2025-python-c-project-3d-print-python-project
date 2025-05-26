from django import forms
from store.models import Models


class ModelsForm(forms.ModelForm):
    Thumbnail = forms.ImageField(required=False)
    
    class Meta:
        model = Models
        fields = "__all__"
