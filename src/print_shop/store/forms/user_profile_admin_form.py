from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
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
        fields = ["Address", "Phone"]

    field_order = [
        "username",
        "email",
        "first_name",
        "last_name",
        "Address",
        "Phone",
        "password1",
        "password2",
        "is_staff",
        "is_active",
    ]

    def __init__(self, *args, **kwargs):
        super(UserProfileAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["username"].initial = self.instance.user.username
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email
            self.fields["is_staff"].initial = self.instance.user.is_staff
            self.fields["is_active"].initial = self.instance.user.is_active
            self.fields["username"].widget.attrs["readonly"] = True

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        if not self.instance.pk:
            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                email=self.cleaned_data["email"],
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
            )
            user.set_password(self.cleaned_data["password1"])
            user.is_staff = self.cleaned_data["is_staff"]
            user.is_active = self.cleaned_data["is_active"]
            user.save()
            profile = UserProfiles.objects.get(user=user)
            profile.Address = self.cleaned_data["Address"]
            profile.Phone = self.cleaned_data["Phone"]
            if commit:
                profile.save()
            return profile
        else:
            profile = self.instance
            profile.Address = self.cleaned_data["Address"]
            profile.Phone = self.cleaned_data["Phone"]
            profile.user.first_name = self.cleaned_data["first_name"]
            profile.user.last_name = self.cleaned_data["last_name"]
            profile.user.email = self.cleaned_data["email"]
            profile.user.is_staff = self.cleaned_data["is_staff"]
            profile.user.is_active = self.cleaned_data["is_active"]
            password1 = self.cleaned_data.get("password1")
            if password1 and password1.strip():
                profile.user.set_password(password1)
            profile.user.save()
            if commit:
                profile.save()
            return profile

            if commit:
                profile.save()

        return profile


class StaffUserCreationForm(UserCreationForm):
    """Form for creating users (staff or regular) with profile information"""

    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=25, required=True)
    is_staff = forms.BooleanField(required=False, initial=False, label="Staff status")
    is_active = forms.BooleanField(required=False, initial=True, label="Active")

    field_order = [
        "username",
        "email",
        "first_name",
        "last_name",
        "address",
        "phone",
        "password1",
        "password2",
        "is_staff",
        "is_active",
    ]

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "is_staff",
            "is_active",
        ]

    def save(self, commit=True):
        user = super(StaffUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = self.cleaned_data["is_staff"]
        user.is_active = self.cleaned_data["is_active"]

        if commit:
            user.save()
            user_profile = UserProfiles.objects.get(user=user)
            user_profile.Address = self.cleaned_data["address"]
            user_profile.Phone = self.cleaned_data["phone"]
            user_profile.save()

        return user
