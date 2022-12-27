from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
    user_form = UserRegistrationForm(request.POST or None)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data["password"])
        new_user.save()
        Profile.objects.create(user=new_user)
        return render(
            request, "account/register_done.html", {"new_user": new_user}
        )

    else:
        return render(
            request, "account/register.html", {"user_form": user_form}
        )


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated " "successfully")

        else:
            messages.error(request, "Error updating your profile")

    else:
        user_form = UserEditForm(instance=request.user.profile)
        profile_form = ProfileEditForm(instance=request.user)

    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def registeration_success(request):
    return render(request, "account/register_done.html")


class UserListView(LoginRequiredMixin, ListView):
    login_url = "account/login"
    queryset = User.objects.filter(is_active=True)
    template_name = "account/user/list.html"
    context_object_name = "users"


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request,
        "account/user/detail.html",
        {"section": "people", "user": user},
    )


