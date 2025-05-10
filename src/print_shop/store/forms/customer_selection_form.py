from django import forms
from django.contrib.auth.models import User


class CustomerSelectionForm(forms.Form):
    """
    Form for selecting a customer when generating quotes
    Used by store owners/staff in the quote generation process
    """
    customer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False),
        required=True,
        empty_label="Select a customer",
        label="Customer",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
