from django import forms
from ..models import Suppliers

class SuppliersForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ['Name', 'Address' , 'Phone', 'Email',]
        