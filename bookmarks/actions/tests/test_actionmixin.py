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
        urllib.request.urlretrieve(
            "https://assets.vogue.in/photos/5f3a37acac1b7909f36d6814/2:3/w_1920,c_limit/Mahendra%20Singh%20Dhoni%20fun%20facts.jpg",
            "rehman.jpg",
        )
        img.open("rehman.jpg")
        self.image = Image.objects.create(
            user=self.user2,
            title="tests",
            slug="tests",
            image="rehman.jpg",
        )
