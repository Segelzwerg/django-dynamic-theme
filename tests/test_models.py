from decimal import Decimal
from os import mkdir, path, remove

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django_dynamic_theme.models import Background, Navbar, Theme

from django.test import TestCase


class ThemeModelTest(TestCase):
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

    def test_export(self):
        theme = Theme.objects.create(name=self.theme_name, background=self.background)
        expected_string = f"body {{background: {self.color};}}"
        self.assertEqual(expected_string, theme.export())

    def test_export_without_pre_existing_file(self):
        if path.exists(self.file_path):
            remove(self.file_path)
        theme = Theme.objects.create(name=self.theme_name, background=self.background)
        expected_string = f"body {{background: {self.color};}}"
        self.assertEqual(expected_string, theme.export())

    def test_export_if_background_is_changed(self):
        theme = Theme.objects.create(name=self.theme_name, background=self.background)
        new_color = "123456"
        self.background.primary_bg = new_color
        self.background.save()
        expected_string = f"body {{background: {new_color};}}"
        self.assertEqual(expected_string, theme.export())

    def test_updated_if_element_saved(self):
        theme = Theme.objects.create(name=self.theme_name, background=self.background)
        new_color = "123456"
        self.background.primary_bg = new_color
        self.background.save()
        self.assertEqual(new_color, theme.background.primary_bg)

    def test_theme_default_uniqueness(self):
        _ = Theme.objects.create(
            name="Original", default=True, background=self.background
        )
        with self.assertRaises(IntegrityError):
            _ = Theme.objects.create(
                name="Second", default=True, background=self.background
            )

    def test_background_not_deleted_after_theme_deletion(self):
        theme = Theme.objects.create(name=self.theme_name, background=self.background)
        theme.delete()
        background_fetched = Background.objects.first()
        self.assertIsNotNone(background_fetched)
        self.assertEqual(self.background, background_fetched)


class BackgroundModelTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.color: str = "F0F0F0"

    def test_export(self):
        background = Background(primary_bg=self.color)
        expected_string = f"background: {self.color};"
        self.assertEqual(expected_string, background.export())

    def test_save_if_not_attached_to_theme(self):
        background = Background.objects.create(primary_bg=self.color)
        background.primary_bg = "654987"
        background.save()
        self.assertEqual(background, Background.objects.first())

    def test_repr(self):
        background = Background(name="dark", primary_bg=self.color)
        self.assertEqual(f"Background: {background.name}", repr(background))


class NavbarTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.color = "#101010"
        self.name = "Binary"

    def test_opacity_min_value(self):
        navbar = Navbar.objects.create(
            name=self.name, background_color=self.color, opacity=-1
        )
        with self.assertRaises(ValidationError):
            navbar.clean_fields()

    def test_opacity_max_value(self):
        navbar = Navbar.objects.create(
            name=self.name, background_color=self.color, opacity=1.1
        )
        with self.assertRaises(ValidationError):
            navbar.clean_fields()

    def test_opacity_valid_value(self):
        navbar = Navbar.objects.create(
            name=self.name, background_color=self.color, opacity=Decimal(0.5)
        )
        navbar.clean_fields()
        self.assertEqual(0.5, navbar.opacity)
