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
    def test_image_like_view_succeeds_adding_like_to_the_image_when_called_with_ajax(
        self,
    ):
        self.client.login(**self.credentials)
        self.client.get(
            reverse(
                "images:detail",
                args=[self.image.pk, self.image.slug],
            )
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": self.image.pk, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_image_like_view_fails_when_the_action_is_invalid(self):
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
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertJSONEqual(response.content, {"status": "error"})

    def test_image_like_view_succeeds_removing_like_from_the_image_when_called_with_ajax(
        self,
    ):
        self.client.login(**self.credentials)
        self.client.get(
            reverse(
                "images:detail",
                args=[self.image.pk, self.image.slug],
            )
        )
        self.client.post(
            reverse("images:like"),
            {"id": self.image.pk, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": self.image.pk, "action": "unlike"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertJSONEqual(response.content, {"status": "ok"})


class TestImageListView(ModelMixin, TestCase):
    def test_image_list_view_uses_correct_template_when_the_request_is_ajax(
        self,
    ):
        self.client.login(**self.credentials)
        response = self.client.get(
            reverse("images:list"),
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertTemplateUsed(response, "images/image/list_ajax.html")

    def test_image_list_view_uses_correct_template_when_the_request_is_not_ajax(
        self,
    ):
        self.client.login(**self.credentials)
        response = self.client.get(reverse("images:list"))
        self.assertTemplateUsed(response, "images/image/list.html")
