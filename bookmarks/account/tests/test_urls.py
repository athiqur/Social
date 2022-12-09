from django.test import SimpleTestCase
from django.urls import resolve, reverse
from account.views import user_login


class TestUrl(SimpleTestCase):
    def test_user_login_url_is_resolved(self):
        self.assertEquals(resolve(reverse("social:login")).func, user_login)
