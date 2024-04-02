"""Tests the context processor(s)"""

from django.test import TestCase

from django_dynamic_theme.context_processor import theme
from django_dynamic_theme.models import Background, Theme


class ThemeTest(TestCase):
    """Tests the theme context processor."""

    def test_theme_file(self):
        self.assertDictEqual({"theme_file": "theme.scss"}, theme(""))

    def test_theme_file_defined_by_admin(self):
        background = Background.objects.create(name="black", primary_bg="000000")
        admin_theme = Theme.objects.create(
            name="Admin", default=True, background=background
        )
        self.assertDictEqual({"theme_file": f"{admin_theme.name}.scss"}, theme(""))
