from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserProfileForm
from ...models import UserProfile

# List all user profiles
def user_profile_list(request):
    user_profiles = UserProfile.objects.all()
    return render(
        request, "user/user_profile_list.html", {"user_profiles": user_profiles}
    )


# Create a new user profile
def add_user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save()
            messages.success(
                request, f"User profile {user_profile.user.username} was created successfully"
            )
            return redirect("user-profile-list")
    else:
        form = UserProfileForm()
    return render(request, "user/user_profile_form.html", {"form": form})


# Edit an existing user profile
def edit_user_profile(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save()
            messages.success(
                request, f"User profile {user_profile.user.username} was updated successfully"
            )
            return redirect("user-profile-list")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, "user/user_profile_form.html", {"form": form})


# Delete an user profile
def delete_user_profile(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        name = user_profile.user.username
        user_profile.delete()
        messages.success(request, f"User profile {name} was deleted successfully")
        return redirect("user-profile-list")
    return render(
        request, "user/user_profile_confirm_delete.html", {"user_profile": user_profile}
    )

