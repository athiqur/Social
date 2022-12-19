from images.models import Image
from django.test import TestCase


class TestImageModel(TestCase):
    def test_title_field_max_size_equals_to_200_characters(self):
        self.assertEqual(Image._meta.get_field("title").max_length, 200)

    def test_slug_field_max_size_equals_to_200_characters(self):
        self.assertEqual(Image._meta.get_field("slug").max_length, 200)
