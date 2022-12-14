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
from django.http import JsonResponse, response
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact
from actions.utils import create_action
from actions.models import Action


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id", flat=True)
    if following_ids:
        actions = (
            actions.filter(user_id__in=following_ids)
            .select_related("user", "user__profile")
            .prefetch_related("target")[:10]
        )
    return render(
        request,
        "account/dashboard.html",
        {"section": "dashboard", "actions": actions},
    )


def register(request):
    user_form = UserRegistrationForm(request.POST or None)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data["password"])
        new_user.save()
        Profile.objects.create(user=new_user)
        create_action(new_user, "has created an account")
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


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    try:
        user = User.objects.get(id=user_id)
        if action == "follow":
            Contact.objects.get_or_create(user_from=request.user, user_to=user)
            create_action(request.user, "is following", user)
            return JsonResponse({"status": "ok"})
        elif action == "unfollow":
            Contact.objects.filter(
                user_from=request.user, user_to=user
            ).delete()
            return JsonResponse({"status": "ok"})

    except User.DoesNotExist:
        return JsonResponse({"status": "error"})

    return JsonResponse({"status": "error"})
