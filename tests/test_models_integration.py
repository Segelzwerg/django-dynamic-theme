from os import mkdir, path, remove
from django.test import TestCase

from django_dynamic_theme.models import Background, Theme


class BackgroundIntegrationTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.theme_name = "test"
        self.folder = "static/"
        self.file_path = f"{self.folder}/{self.theme_name}.scss"
        self.color: str = "F0F0F0"
        self.background: Background = Background.objects.create(primary_bg=self.color)
        if not path.exists(self.folder):
            mkdir(self.folder)
        _ = open(self.file_path, mode="w+")

    def tearDown(self) -> None:
        super().tearDown()
        if path.exists(self.file_path):
            remove(self.file_path)

    def test_theme_export_if_background_saved(self):
        new_color = "987654"
        theme = Theme.objects.create(name=self.theme_name, background=self.background)
        self.background.primary_bg = new_color
        self.background.save()
        with open(self.file_path) as theme_file:
            exported_string = theme_file.read()
            expected_string = f"body {{background: {new_color};}}"
            self.assertEqual(expected_string, exported_string)
        self.assertEqual(new_color, theme.background.primary_bg)
