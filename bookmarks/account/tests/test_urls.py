from django.test import SimpleTestCase
from django.urls import resolve, reverse
from account.views import dashboard, Register, registeration_success


class TestUrl(SimpleTestCase):
    def test_dashboard_url_is_resolved(self):
        self.assertEquals(resolve(reverse("dashboard")).func, dashboard)

    def test_registeration_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("register")).func.view_class, Register
        )

    def test_registration_done_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("registeration_success")).func,
            registeration_success,
        )
