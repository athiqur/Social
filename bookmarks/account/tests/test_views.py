from django.test import TestCase
from django.urls import reverse
from account.tests.test_modelmixintestcase import ModelMixinTestCase


class TestUserLogin(ModelMixinTestCase, TestCase):
    def test_auth_login_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.client.get(reverse("social:login")), "registration/login.html"
        )

    def test_auth_login_view_uses_correct_template_after_successful_login(
        self,
    ):
        self.logIn()
        response = self.client.get(reverse("social:dashboard"), follow=True)
        self.assertTemplateUsed(response, "account/dashboard.html")


class TestLogoutView(ModelMixinTestCase, TestCase):
    def test_auth_logout_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.client.get(reverse("social:logout")),
            "registration/logged_out.html",
        )

    def test_auth_logout_view_uses_correct_template_after_successful_logout(
        self,
    ):
        self.logIn()
        self.logOut()
        response = self.client.get(reverse("social:dashboard"), follow=True)
        self.assertTemplateUsed(response, "account/dashboard.html")


class TestPasswordChangeView(ModelMixinTestCase, TestCase):
    def test_auth_password_change_view_uses_correct_template(self):
        self.logIn()
        self.assertTemplateUsed(
            self.client.get(reverse("social:password_change")),
            "registration/password_change_form.html",
        )

    def test_auth_password_change_done_view_uses_correct_template(self):
        self.logIn()
        self.assertTemplateUsed(
            self.client.get(reverse("social:password_change_done")),
            "registration/password_change_done.html",
        )
