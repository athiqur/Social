from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Profile


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "athiqur",
            "password": "123",
        }
        User.objects.create_user(**self.credentials)
        Profile.objects.create(user=self.user)
