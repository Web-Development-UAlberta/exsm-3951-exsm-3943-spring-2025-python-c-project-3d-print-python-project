from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ..models import UserProfiles


class UserProfileAdminForm(forms.ModelForm):
    """Form for store owners/staff to manage user profiles"""
    
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)
    is_staff = forms.BooleanField(required=False, label="Staff status")
    is_active = forms.BooleanField(required=False, label="Active")
    
    class Meta:
        model = UserProfiles
        fields = ['Address', 'Phone']
    
    def __init__(self, *args, **kwargs):
        super(UserProfileAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['is_staff'].initial = self.instance.user.is_staff
            self.fields['is_active'].initial = self.instance.user.is_active
            self.fields['username'].widget.attrs['readonly'] = True
    
    def save(self, commit=True):
        profile = super(UserProfileAdminForm, self).save(commit=False)
        
        # Update the associated user model fields
        if not self.instance.pk:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            user.is_staff = self.cleaned_data['is_staff']
            user.is_active = self.cleaned_data['is_active']
            user.save()
            profile.user = user
        else:
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.is_staff = self.cleaned_data['is_staff']
            profile.user.is_active = self.cleaned_data['is_active']
            profile.user.save()
        
        if commit:
            profile.save()
        
        return profile


class StaffUserCreationForm(UserCreationForm):
    """Form for creating staff users with profile information"""
    
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=25, required=True)
    is_staff = forms.BooleanField(required=False, initial=True, label="Staff status")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff']
    
    def save(self, commit=True):
        user = super(StaffUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = self.cleaned_data['is_staff']
        
        if commit:
            user.save()
            user_profile = UserProfiles.objects.get(user=user)
            user_profile.Address = self.cleaned_data['address']
            user_profile.Phone = self.cleaned_data['phone']
            user_profile.save()
        
        return user
