from django import forms
from ..models import FulfillmentStatus

class FulfillmentStatusForm(forms.ModelForm):
    class Meta:
        model = FulfillmentStatus
        fields = ['Order', 'OrderStatus']