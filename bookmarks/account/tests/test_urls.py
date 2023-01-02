from django.test import SimpleTestCase
from django.urls import resolve, reverse
from account.views import dashboard


class TestUrl(SimpleTestCase):
    def test_dashboard_url_is_resolved(self):
        self.assertEquals(resolve(reverse("dashboard")).func, dashboard)
