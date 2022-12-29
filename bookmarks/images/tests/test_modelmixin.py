from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Profile
from images.models import Image
import urllib.request
from PIL import Image as img
from django.urls import reverse


class ModelMixin(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "athiqur",
            "password": "123",
        }
        self.user = User.objects.create_user(**self.credentials)
        Profile.objects.create(user=self.user)
        self.image = Image.objects.create(
            user=self.user,
            title="rehman",
            slug="rehman",
            url="https://assets.vogue.in/photos/5f3a37acac1b7909f36d6814/2:3/w_1920,c_limit/Mahendra%20Singh%20Dhoni%20fun%20facts.jpg",
            image="media/images/30/dhoni.jpg",
        )

    def view_image(self, image_id, image_slug, count):
        for _ in range(count):
            self.client.get(
                reverse("images:detail", args=[image_id, image_slug])
            )
