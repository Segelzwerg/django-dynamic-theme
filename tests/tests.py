from unittest.mock import MagicMock, mock_open, patch
from django.test import TestCase

from django_dynamic_theme.models import Background, Theme
from django_dynamic_theme.utill.scss_editor import ScssEditor


class ThemeModelTest(TestCase):
    def test_export(self):
        color: str = "F0F0F0"
        background = Background.objects.create(primary_bg=color)
        theme = Theme.objects.create(background=background)
        expected_string = "body {background: F0F0F0;}"
        self.assertEqual(expected_string, theme.export())


class BackgroundModelTest(TestCase):
    def test_export(self):
        color: str = "F0F0F0"
        background = Background(primary_bg=color)
        expected_string = f"background: {color};"
        self.assertEqual(expected_string, background.export())


class ScssEditorTest(TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_write_scss(self, open_mock: MagicMock):
        editor = ScssEditor("static/theme.scss")
        editor.write("test")
        file = open_mock.return_value
        open_mock.assert_called_once_with("static/theme.scss", mode="w")
        file.write.assert_called_once_with("test")
