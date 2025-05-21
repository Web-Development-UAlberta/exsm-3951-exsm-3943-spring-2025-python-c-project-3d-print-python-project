from django import forms
from store.models import FulfillmentStatus


class FulfillmentStatusForm(forms.ModelForm):
    class Meta:
        model = FulfillmentStatus
        fields = ["OrderStatus"]
