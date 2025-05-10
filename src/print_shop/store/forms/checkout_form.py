from django import forms
from store.models import Shipping


class CheckoutForm(forms.Form):
    """
    Form for collecting shipping information during checkout
    Handles shipping method selection and expedited shipping option
    """
    shipping_method = forms.ModelChoiceField(
        queryset=Shipping.objects.all(),
        label="Shipping Method",
        empty_label="Select a shipping method",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={
            'required': 'Please select a shipping method.',
            'invalid_choice': 'Please select a valid shipping method.'
        }
    )
    expedited = forms.BooleanField(
        required=False,
        label="Expedited Shipping",
        help_text="Faster turnaround for 1.5x the cost"
    )

    def clean(self):
        """
        Validate that a shipping method is selected
        """
        cleaned_data = super().clean()
        shipping_method = cleaned_data.get('shipping_method')
        
        if not shipping_method:
            self.add_error('shipping_method', 'Please select a shipping method.')
            
        return cleaned_data
