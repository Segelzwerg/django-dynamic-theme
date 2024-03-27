from os import mkdir, path, remove, rmdir
from shutil import rmtree
from django_dynamic_theme.models import Background, Theme


from django.test import TestCase


class ThemeModelTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.theme_name = "test"
        self.folder = "static/"
        self.file_path = f"{self.folder}/{self.theme_name}.scss"
        if not path.exists(self.folder):
            mkdir(self.folder)
        _ = open(self.file_path, mode="w+")

    def tearDown(self) -> None:
        super().tearDown()
        if path.exists(self.file_path):
            remove(self.file_path)

    def test_export(self):
        color: str = "F0F0F0"
        background = Background.objects.create(primary_bg=color)
        theme = Theme.objects.create(name=self.theme_name, background=background)
        expected_string = "body {background: F0F0F0;}"
        self.assertEqual(expected_string, theme.export())

    def test_export_without_pre_existing_file(self):
        if path.exists(self.file_path):
            remove(self.file_path)
        color: str = "F0F0F0"
        background = Background.objects.create(primary_bg=color)
        theme = Theme.objects.create(name=self.theme_name, background=background)
        expected_string = "body {background: F0F0F0;}"
        self.assertEqual(expected_string, theme.export())


class BackgroundModelTest(TestCase):
    def test_export(self):
        color: str = "F0F0F0"
        background = Background(primary_bg=color)
        expected_string = f"background: {color};"
        self.assertEqual(expected_string, background.export())
