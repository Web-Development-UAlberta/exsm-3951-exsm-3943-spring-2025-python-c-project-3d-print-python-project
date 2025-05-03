from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages

def login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid credentials")
    return render(request, "accounts/login.html")


def logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return render(request, "accounts/logout_confirm.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile-list")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def account_update(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated")
            return redirect("profile-list")
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, "accounts/account_update.html", {"form": form})


@login_required
def account_delete(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, "Account deleted")
        return redirect("home")
    return render(request, "accounts/account_confirm_delete.html")