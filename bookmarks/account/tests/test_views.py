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
        self.client.login(**self.credentials)
        response = self.client.get(reverse("social:dashboard"), follow=True)
        self.assertTemplateUsed(response, "account/dashboard.html")
