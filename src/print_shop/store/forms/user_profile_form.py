from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ..models import UserProfiles


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)
    
    class Meta:
        model = UserProfiles
        fields = ['Address', 'Phone']
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.email = self.cleaned_data['email']
        
        if commit:
            profile.user.save()
            profile.save()
        
        return profile


class UserRegistrationForm(UserCreationForm):
    """Form for registering a new user with profile information"""
    
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=25, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            user_profile = UserProfiles.objects.get(user=user)
            user_profile.Address = self.cleaned_data['address']
            user_profile.Phone = self.cleaned_data['phone']
            user_profile.save()
        
        return user
