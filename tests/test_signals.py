from os import mkdir, path, remove
from django.test import TestCase

from django_dynamic_theme.models import Background, MediaGallery, Navbar, Theme


class SignalTest(TestCase):

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

    def test_file_created_during_startup(self):
        self.assertTrue(path.exists(self.file_path))

    def test_no_error_startup_with_out_theme(self):
        self.assertTrue(path.exists(self.file_path))
