from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


class Register(CreateView):
    form_class = UserRegistrationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("registeration_success")


def registeration_success(request):
    return render(request, "account/register_done.html")
