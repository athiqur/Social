from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "social"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("", views.dashboard, name="dashboard"),
]
