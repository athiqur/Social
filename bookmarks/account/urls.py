from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path(
        "success/", views.registeration_success, name="registeration_success"
    ),
    path("edit/", views.edit, name="edit"),
]
