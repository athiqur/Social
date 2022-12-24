from django.test import TestCase
from images.tests.test_modelmixin import ModelMixin
from django.urls import reverse


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
