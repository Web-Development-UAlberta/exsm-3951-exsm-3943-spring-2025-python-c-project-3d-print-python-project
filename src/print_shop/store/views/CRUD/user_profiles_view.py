from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from store.forms.user_profile_form import UserProfileForm, UserRegistrationForm
from store.forms.user_profile_admin_form import (
    UserProfileAdminForm,
    StaffUserCreationForm,
)
from store.models import UserProfiles


def is_staff(user):
    """Check if user is staff"""
    return user.is_staff


@login_required
def view_profile(request):
    """View own profile for logged in user"""
    user_profile = get_object_or_404(UserProfiles, user=request.user)
    return render(
        request, "user/user_profile_detail.html", {"user_profile": user_profile}
    )


@login_required
def edit_profile(request):
    """Edit own profile for logged in user"""
    user_profile = get_object_or_404(UserProfiles, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save()
            messages.success(request, "Your profile was updated successfully")
            return redirect("view-profile")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, "user/user_profile_form.html", {"form": form})


def register(request):
    """Register a new user with profile"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"Account created for {user.username}. You can now log in."
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "auth/register.html", {"form": form})


"""Admin views for store owners/staff"""


@user_passes_test(is_staff)
def user_profile_list(request):
    """List all user profiles (admin view)"""
    user_profiles = UserProfiles.objects.all()
    return render(
        request, "user/user_profile_list.html", {"user_profiles": user_profiles}
    )


@user_passes_test(is_staff)
def user_profile_detail(request, pk):
    """View details of a user profile (admin view)"""
    user_profile = get_object_or_404(UserProfiles, pk=pk)
    return render(
        request,
        "user/user_profile_detail.html",
        {"user_profile": user_profile, "is_admin_view": True},
    )


@user_passes_test(is_staff)
def add_user_profile(request):
    """Add a new user profile (admin view)"""
    if request.method == "POST":
        form = UserProfileAdminForm(request.POST)
        if form.is_valid():
            try:
                user_profile = form.save()
                messages.success(
                    request,
                    f"User profile for {user_profile.user.username} was created successfully",
                )
                return redirect("user-profile-list")
            except IntegrityError as e:
                if 'username' in str(e):
                    messages.error(
                        request,
                        f"Username '{form.cleaned_data.get('username')}' is already taken. Please choose a different username.",
                    )
                else:
                    messages.error(
                        request,
                        f"An error occurred while creating the user: {str(e)}",
                    )
    else:
        form = UserProfileAdminForm()
    return render(
        request, "user/user_profile_form.html", {"form": form, "is_admin_view": True}
    )


@user_passes_test(is_staff)
def add_staff_user(request):
    """Add a new staff user (admin view)"""
    if request.method == "POST":
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"Staff account for {user.username} was created successfully"
            )
            return redirect("user-profile-list")
    else:
        form = StaffUserCreationForm()
    return render(request, "user/staff_user_form.html", {"form": form})


@user_passes_test(is_staff)
def edit_user_profile(request, pk):
    """Edit a user profile (admin view)"""
    user_profile = get_object_or_404(UserProfiles, pk=pk)
    if request.method == "POST":
        form = UserProfileAdminForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save()
            messages.success(
                request,
                f"User profile for {user_profile.user.username} was updated successfully",
            )
            return redirect("user-profile-list")
    else:
        form = UserProfileAdminForm(instance=user_profile)
    return render(
        request, "user/user_profile_form.html", {"form": form, "is_admin_view": True}
    )


@user_passes_test(is_staff)
def delete_user_profile(request, pk):
    """Delete a user profile (admin view)"""
    user_profile = get_object_or_404(UserProfiles, pk=pk)
    user = user_profile.user
    if request.method == "POST":
        username = user.username
        user.delete()  # This will also delete the profile due to CASCADE
        messages.success(request, f"User {username} was deleted successfully")
        return redirect("user-profile-list")
    return render(
        request, "user/user_profile_confirm_delete.html", {"user_profile": user_profile}
    )


@login_required
def change_password(request):
    """Change user password"""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect("view-profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "user/change_password.html", {"form": form})
