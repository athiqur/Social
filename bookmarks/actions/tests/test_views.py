from django.test import TestCase
from actions.models import Action
from django.contrib.auth.models import User
from django.urls import reverse
from actions.utils import create_action
from actions.tests.test_actionmixin import ActionMixinTestCase


class TestActionView(ActionMixinTestCase, TestCase):
    def test_action_stream_succeeds_showing_in_dashboard(self):
        self.client.login(**self.credentials_1)
        self.client.post(
            reverse("images:like"),
            {"id": self.user1.pk, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.client.login(**self.credentials_2)
        dashboard_display = self.client.get(reverse("dashboard"))
        self.assertQuerysetEqual(
            dashboard_display.context.get("actions"),
            Action.objects.filter(verb="likes"),
        )

    def test_action_stream_does_not_show_our_own_action_in_dashboard(self):
        self.client.login(**self.credentials_1)
        self.image.users_like(self.user1)
        dashboard_display = self.client.get(reverse("dashboard"))
        self.assertQuerysetEqual(dashboard_display.context.get("actions"), [])
