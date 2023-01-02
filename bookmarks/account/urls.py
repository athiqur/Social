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
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("users/", views.UserListView.as_view(), name="user_list"),
]
