from decimal import Decimal
from os import mkdir, path, remove

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django_dynamic_theme.models import Background, MediaGallery, Navbar, Theme

from django.test import TestCase


class ThemeModelTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.theme_name = "test"
        self.folder = "static/"
        self.file_path = f"{self.folder}/{self.theme_name}.scss"
        self.color: str = "F0F0F0"
        self.media_gallery = MediaGallery.objects.create(
            margin_left="auto",
            margin_right="auto",
            max_width="fit-content",
            item_align="left",
            row_margin_top="10px",
        )
        self.background: Background = Background.objects.create(primary_bg=self.color)
        self.navbar: Navbar = Navbar.objects.create(
            name="Test", background_color="#FFFF00", text_color="#111111"
        )
        if not path.exists(self.folder):
            mkdir(self.folder)
        _ = open(self.file_path, mode="w+")
        self.theme = Theme.objects.create(
            name=self.theme_name,
            background=self.background,
            media_gallery=self.media_gallery,
            navbar=self.navbar,
        )
        self.expected_string = f"""body {{{self.background.export()}}}
{self.media_gallery.export()}
{self.navbar.export()}"""

    def tearDown(self) -> None:
        super().tearDown()
        if path.exists(self.file_path):
            remove(self.file_path)

    def test_export(self):
        self.assertEqual(self.expected_string, self.theme.export())

    def test_export_without_pre_existing_file(self):
        if path.exists(self.file_path):
            remove(self.file_path)
        self.assertEqual(self.expected_string, self.theme.export())

    def test_export_if_background_is_changed(self):
        new_color = "123456"
        self.background.primary_bg = new_color
        self.background.save()
        expected_string = f"""body {{{self.background.export()}}}
{self.media_gallery.export()}
{self.navbar.export()}"""
        self.assertEqual(expected_string, self.theme.export())

    def test_updated_if_element_saved(self):
        new_color = "123456"
        self.background.primary_bg = new_color
        self.background.save()
        self.assertEqual(new_color, self.theme.background.primary_bg)

    def test_theme_default_uniqueness(self):
        _ = Theme.objects.create(
            name="Original",
            default=True,
            background=self.background,
            media_gallery=self.media_gallery,
            navbar=self.navbar,
        )
        with self.assertRaises(IntegrityError):
            _ = Theme.objects.create(
                name="Second", default=True, background=self.background
            )

    def test_background_not_deleted_after_theme_deletion(self):
        self.theme.delete()
        background_fetched = Background.objects.first()
        self.assertIsNotNone(background_fetched)
        self.assertEqual(self.background, background_fetched)


class BackgroundModelTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.color: str = "F0F0F0"

    def test_export(self):
        background = Background(primary_bg=self.color)
        expected_string = f"background-color: {self.color};"
        self.assertEqual(expected_string, background.export())

    def test_save_if_not_attached_to_theme(self):
        background = Background.objects.create(primary_bg=self.color)
        background.primary_bg = "654987"
        background.save()
        self.assertEqual(background, Background.objects.first())

    def test_repr(self):
        background = Background(name="dark", primary_bg=self.color)
        self.assertEqual(f"Background: {background.name}", repr(background))


class MediaGalleryTest(TestCase):
    def test_export(self):
        margin = "auto"
        media_gallery = MediaGallery(
            margin_left=margin,
            margin_right=margin,
            max_width="fit-content",
            item_align="left",
            row_margin_top="10px",
        )
        expected_string = f""".mediagallery {{margin-left: {margin};
margin-right: {margin};
max-width: fit-content;
text-align: left;
.row {{margin-top: 10px;}}}}"""
        self.assertEqual(expected_string, media_gallery.export())


class NavbarTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.color = "#101010"
        self.name = "Binary"

    def test_opacity_min_value(self):
        navbar = Navbar.objects.create(
            name=self.name, background_color=self.color, opacity=Decimal(-1)
        )
        with self.assertRaisesMessage(
            ValidationError,
            "{'opacity': ['Ensure this value is greater than or equal to 0.']}",
        ):
            navbar.clean_fields()

    def test_opacity_max_value(self):
        navbar = Navbar.objects.create(
            name=self.name, background_color=self.color, opacity=Decimal(1.5)
        )
        with self.assertRaisesMessage(
            ValidationError,
            "{'opacity': ['Ensure this value is less than or equal to 1.']}",
        ):
            navbar.clean_fields()

    def test_opacity_valid_value(self):
        navbar = Navbar.objects.create(
            name=self.name, background_color=self.color, opacity=Decimal(0.5)
        )
        navbar.clean_fields()
        self.assertEqual(0.5, navbar.opacity)

    def test_export(self):
        navbar = Navbar.objects.create(
            name=self.name,
            background_color=self.color,
            opacity=Decimal(0.5),
            font_size="x-large",
            text_color="#FF0000",
            text_opacity=1,
        )
        expected_navbar = ".navbar {background-color: rgba(16,16,16,0.50) !important;}"
        expected_navlink = ".nav-link {font-size:x-large;color:rgba(255,0,0,1.00);}"
        expected_string = f"{expected_navbar}\n{expected_navlink}"
        self.assertEqual(expected_string, navbar.export())
