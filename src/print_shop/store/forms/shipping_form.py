from django import forms
from store.models import Shipping


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ["Name", "Rate", "ShipTime"]
