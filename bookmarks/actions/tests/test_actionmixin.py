import urllib.request
from PIL import Image as img
from django.test import TestCase
from django.contrib.auth.models import User
from images.models import Image


class ActionMixinTestCase(TestCase):
    def setUp(self):
        self.credentials_1 = {"username": "athiqur", "password": "123"}
        self.credentials_2 = {"username": "rehman", "password": "123"}
        self.user1 = User.objects.create_user(**self.credentials_1)
        self.user2 = User.objects.create_user(**self.credentials_2)
        self.image = Image.objects.create(
            user=self.user2,
            title="tests",
            slug="tests",
            image="rehman.jpg",
        )
