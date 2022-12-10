from django.test import TestCase
from django.contrib.auth.models import User


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "athiqur",
            "password": "123",
        }
        User.objects.create_user(**self.credentials)

    def logIn(self):
        self.client.login(**self.credentials)

    def logOut(self):
        self.client.logout
