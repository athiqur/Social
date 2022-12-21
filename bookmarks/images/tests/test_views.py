from django.test import TestCase
from images.tests.test_modelmixin import ModelMixin
from django.urls import reverse

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


class TestImageLikeView(ModelMixin, TestCase):
    def test_image_like_view_succeeds_adding_like_to_the_image(self):
        self.client.login(**self.credentials)
        self.client.get(
            reverse(
                "images:detail",
                args=[self.image.pk, self.image.slug],
            )
        )
        self.image.users_like.add(self.user)
        self.assertIsNotNone(self.image.users_like.first())

    def test_image_like_view_returns_status_error_for_invalid_action(self):
        self.client.login(**self.credentials)
        self.client.get(
            reverse(
                "images:detail",
                args=[self.image.pk, self.image.slug],
            )
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": self.image.pk, "action": "None"},
        )
        self.assertJSONEqual(response.content, {"status": "error"})

    def test_image_like_view_succeeds_removing_like_from_the_image(self):
        self.client.login(**self.credentials)
        self.client.get(
            reverse(
                "images:detail",
                args=[self.image.pk, self.image.slug],
            )
        )
        self.image.users_like.add(self.user)
        self.image.users_like.remove(self.user)
        self.assertIsNone(self.image.users_like.first())
