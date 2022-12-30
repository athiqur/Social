from django.test import TestCase
from images.tests.test_modelmixin import ModelMixin
from django.urls import reverse
from images.models import Image


class TestDetailView(ModelMixin, TestCase):
    def test_detail_view_returns_to_success_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(
            reverse("images:detail", args=[self.image.pk, self.image.slug])
        )
        self.assertTemplateUsed(response, "images/image/detail.html")

    def test_detail_view_returns_404_for_invalid_image(self):
        self.client.login(**self.credentials)
        response = self.client.get(
            reverse("images:detail", args=[1000, "image-illai"])
        )
        self.assertEquals(response.status_code, 404)
