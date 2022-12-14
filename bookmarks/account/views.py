from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Profile
from django.views.generic.edit import ModelFormMixin


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


class Register(CreateView):
    form_class = UserRegistrationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("registeration_success")

    def dispatch(self, request, *args, **kwargs):
        self.user_form = UserRegistrationForm(request.POST or None)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = self.user_form.save(commit=False)
        new_user.set_password(self.user_form.cleaned_data["password"])
        new_user.save()
        Profile.objects.create(user=new_user)
        return super().form_valid(form)


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
