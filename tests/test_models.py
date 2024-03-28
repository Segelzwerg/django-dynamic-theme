from os import mkdir, path, remove

from django.db import IntegrityError
from django_dynamic_theme.models import Background, Theme

from django.test import TestCase


class ThemeModelTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.theme_name = "test"
        self.folder = "static/"
        self.file_path = f"{self.folder}/{self.theme_name}.scss"
        color: str = "F0F0F0"
        self.background = Background.objects.create(primary_bg=color)
        if not path.exists(self.folder):
            mkdir(self.folder)
        _ = open(self.file_path, mode="w+")

    def tearDown(self) -> None:
        super().tearDown()
        if path.exists(self.file_path):
            remove(self.file_path)

    def test_export(self):
        theme = Theme.objects.create(name=self.theme_name, background=self.background)
        expected_string = "body {background: F0F0F0;}"
        self.assertEqual(expected_string, theme.export())

    def test_export_without_pre_existing_file(self):
        if path.exists(self.file_path):
            remove(self.file_path)
        theme = Theme.objects.create(name=self.theme_name, background=self.background)
        expected_string = "body {background: F0F0F0;}"
        self.assertEqual(expected_string, theme.export())

    def test_theme_default_uniqueness(self):
        _ = Theme.objects.create(
            name="Original", default=True, background=self.background
        )
        with self.assertRaises(IntegrityError):
            _ = Theme.objects.create(
                name="Second", default=True, background=self.background
            )


class BackgroundModelTest(TestCase):
    def test_export(self):
        color: str = "F0F0F0"
        background = Background(primary_bg=color)
        expected_string = f"background: {color};"
        self.assertEqual(expected_string, background.export())
