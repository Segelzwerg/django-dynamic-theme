from unittest.mock import MagicMock, mock_open, patch
from django.test import TestCase

from django_dynamic_theme.utill.color_converter import hex_to_tuple
from django_dynamic_theme.utill.scss_editor import ScssEditor


class ScssEditorTest(TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_write_scss(self, open_mock: MagicMock):
        editor = ScssEditor("static/theme.scss")
        editor.write("test")
        file = open_mock.return_value
        open_mock.assert_called_once_with(
            "static/theme.scss", mode="w+", encoding="UTF-8"
        )
        file.write.assert_called_once_with("test")


class ColorConverterTest(TestCase):
    def test_hex_converter(self):
        rgb = "#1234FF"
        expected_tuple = ("12", "34", "FF")
        self.assertEqual(expected_tuple, hex_to_tuple(rgb))
