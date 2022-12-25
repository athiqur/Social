from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Profile


class ModelMixin(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "athiqur",
            "password": "123",
        }
        self.user = User.objects.create_user(**self.credentials)
        Profile.objects.create(user=self.user)
