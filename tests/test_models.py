from django_dynamic_theme.models import Background, Theme


from django.test import TestCase


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