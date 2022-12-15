from django.test import TestCase
from django.urls import reverse, reverse_lazy
from account.tests.test_modelmixintestcase import ModelMixinTestCase


class TestUserLogin(ModelMixinTestCase, TestCase):
    def test_auth_login_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.client.get(reverse("login")), "registration/login.html"
        )

    def test_auth_login_view_uses_correct_template_after_successful_login(
        self,
    ):
        self.client.login(**self.credentials)
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertTemplateUsed(response, "account/dashboard.html")


class TestLogoutView(ModelMixinTestCase, TestCase):
    def test_auth_logout_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.client.get(reverse("logout")),
            "registration/logged_out.html",
        )

    def test_auth_logout_view_uses_correct_template_after_successful_logout(
        self,
    ):
        self.client.login(**self.credentials)
        self.client.logout
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertTemplateUsed(response, "account/dashboard.html")


class TestPasswordChangeView(ModelMixinTestCase, TestCase):
    def test_auth_password_change_view_uses_correct_template(self):
        self.client.login(**self.credentials)
        self.assertTemplateUsed(
            self.client.get(reverse("password_change")),
            "registration/password_change_form.html",
        )

    def test_auth_password_change_done_view_uses_correct_template(self):
        self.client.login(**self.credentials)
        self.assertTemplateUsed(
            self.client.get(reverse("password_change_done")),
            "registration/password_change_done.html",
        )


class TestRegisterView(TestCase):
    def test_register_view_uses_correct_template_for_unsuccessful_registration(
        self,
    ):
        response = self.client.get(
            reverse("register"),
            {
                "username": "athiqur@gmail.com",
                "first_name": "athiqur",
                "email": "athiqurking@gmail.com",
                "password": "123",
                "password2": "123",
            },
        )
        self.assertTemplateUsed(response, "account/register.html")

    def test_register_view_uses_success_view_after_successful_registration(
        self,
    ):
        response = self.client.post(
            reverse("register"),
            {
                "username": "athiqur@gmail.com",
                "first_name": "athiqur",
                "email": "athiqurking@gmail.com",
                "password": "123",
                "password2": "123",
            },
        )
        self.assertTemplateUsed(response, "account/register_done.html")

    def test_edit_view_uses_success_view_after_editing(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "athiqur@gmail.com",
                "first_name": "athiqur",
                "email": "athiqurking@gmail.com",
                "password": "123",
                "password2": "123",
            },
        )
        self.assertTemplateUsed(response, "account/register_done.html")
