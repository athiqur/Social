from django.test import TestCase
from django.urls import reverse
from account.views import user_login
from django.contrib.auth import get_user
from account.tests.test_modelmixintestcase import ModelMixinTestCase


class TestUserLogin(ModelMixinTestCase, TestCase):
    def test_user_login_is_authenticated(self):
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_user_login_uses_correct_template(self):
        self.assertTemplateUsed(
            self.client.get(reverse("social:login")), "account/login.html"
        )
