"""Tests the context processor(s)"""

from django.test import TestCase

from django_dynamic_theme.context_processor import theme


class ThemeTest(TestCase):
    """Tests the theme context processor."""

    def test_theme_file(self):
        self.assertDictEqual({"theme_file": "theme.scss"}, theme(""))
