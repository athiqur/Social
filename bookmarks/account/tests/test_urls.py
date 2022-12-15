from django.test import SimpleTestCase
from django.urls import resolve, reverse
from account.views import dashboard, register, registeration_success, edit


class TestUrl(SimpleTestCase):
    def test_dashboard_url_is_resolved(self):
        self.assertEquals(resolve(reverse("dashboard")).func, dashboard)

    def test_registeration_url_is_resolved(self):
        self.assertEquals(resolve(reverse("register")).func, register)

    def test_registration_done_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("registeration_success")).func,
            registeration_success,
        )

    def test_edit_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("edit")).func,
            edit,
        )
