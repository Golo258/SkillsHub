from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def register(request):
    if request.method == "POST":
        userForm = RegistrationForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            username = userForm.cleaned_data.get("username")
            messages.success(request, f"Account {username} has been created successfully")
            return redirect("blog-home")
    else:
        userForm = RegistrationForm()
    return render(request,
                  "users/register.html",
                  {"userForm": userForm})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Account has been updated successfully")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "userForm": user_form,
        "profileForm": profile_form
    }
    return render(request, "users/profile.html",
                  context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logout successfully.")
    return redirect("blog-home")
