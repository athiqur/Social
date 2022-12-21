from django.test import TestCase
from images.tests.test_modelmixin import ModelMixin
from django.urls import reverse
from images.models import Image

class TestDetailView(ModelMixin, TestCase):
    def test_detail_view_returns_to_success_view(self):
        self.client.login(**self.credentials)
        self.client.post(
            reverse("images:create"),
            {
                "title": "rehman",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
            },
        )
        response = self.client.get(
            reverse("images:detail", args=[1, "rehman"])
        )
        self.assertTemplateUsed(response, "images/image/detail.html")

    def test_detail_view_returns_404_for_no_image(self):
        self.client.login(**self.credentials)
        response = self.client.get(
            reverse("images:detail", args=[1, "rehman"])
        )
        self.assertEquals(response.status_code, 404)


class TestImageLikeView(ModelMixin, TestCase):
    def test_image_like_view_succeeds_adding_like_to_the_image(self):
        self.client.login(**self.credentials)
        self.client.post(
            reverse("images:create"),
            {
                "title": "rehman",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
            },
        )
        self.client.get(
            reverse(
                "images:detail",
                args=[Image.objects.first().pk, Image.objects.first().slug],
            )
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": Image.objects.first().pk, "action": "like"},
        )
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_image_like_view_fails_adding_like_or_unlike_to_the_image(self):
        self.client.login(**self.credentials)
        self.client.post(
            reverse("images:create"),
            {
                "title": "rehman",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
            },
        )
        self.client.get(
            reverse(
                "images:detail",
                args=[Image.objects.first().pk, Image.objects.first().slug],
            )
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": Image.objects.first().pk, "action": "None"},
        )
        self.assertJSONEqual(response.content, {"status": "error"})

    def test_image_like_view_succeeds_removing_like_from_the_image(self):
        self.client.login(**self.credentials)
        self.client.post(
            reverse("images:create"),
            {
                "title": "rehman",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
            },
        )
        self.client.get(
            reverse(
                "images:detail",
                args=[Image.objects.first().pk, Image.objects.first().slug],
            )
        )
        self.client.post(
            reverse("images:like"),
            {"id": Image.objects.first().pk, "action": "like"},
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": Image.objects.first().pk, "action": "unlike"},
        )
        self.assertJSONEqual(response.content, {"status": "ok"})
