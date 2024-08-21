from os import mkdir, path, remove
from unittest.mock import MagicMock
from compressor.exceptions import UncompressableFileError
from django.conf import settings
from django.http import HttpResponse
from django.test import TestCase

from django_dynamic_theme.errors import ThemeMissingError
from django_dynamic_theme.middleware import MissingThemeHandleMiddleware
from django_dynamic_theme.models import Background, MediaGallery, Navbar, Theme


class MiddlewareTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.theme_name = "test"
        self.folder = "static/"
        self.file_path = f"{self.folder}/{self.theme_name}.scss"
        self.media_gallery = MediaGallery.objects.create(
            margin_left="auto",
            margin_right="auto",
            max_width="fit-content",
            item_align="left",
            row_margin_top="10px",
        )

        if not path.exists(self.folder):
            mkdir(self.folder)

    def tearDown(self) -> None:
        super().tearDown()
        if path.exists(self.file_path):
            remove(self.file_path)

    def test_save_file(self):
        color: str = "F0F0F0"
        background: Background = Background.objects.create(primary_bg=color)
        navbar: Navbar = Navbar.objects.create(
            name="Test", background_color="#FFFF00", text_color="#111111"
        )
        Theme.objects.create(
            name=self.theme_name,
            background=background,
            media_gallery=self.media_gallery,
            navbar=navbar,
            default=True,
        )
        request = MagicMock()
        get_response = MagicMock(side_effect=[HttpResponse()])
        middleware = MissingThemeHandleMiddleware(get_response)
        middleware.process_exception(request, UncompressableFileError())
        get_response.assert_called_with(request)
        self.assertEqual(1, get_response.call_count)
        self.assertTrue(path.exists(self.file_path))

    def test_save_file_no_default(self):
        color: str = "F0F0F0"
        background: Background = Background.objects.create(primary_bg=color)
        navbar: Navbar = Navbar.objects.create(
            name="Test", background_color="#FFFF00", text_color="#111111"
        )
        Theme.objects.create(
            name=self.theme_name,
            background=background,
            media_gallery=self.media_gallery,
            navbar=navbar,
            default=False,
        )
        request = MagicMock()
        get_response = MagicMock(side_effect=[HttpResponse()])
        middleware = MissingThemeHandleMiddleware(get_response)
        middleware.process_exception(request, UncompressableFileError())
        get_response.assert_called_with(request)
        self.assertEqual(1, get_response.call_count)
        self.assertTrue(path.exists(self.file_path))

    def test_save_file_no_theme_in_debug(self):
        settings.DEBUG = True
        request = MagicMock()
        get_response = MagicMock()
        middleware = MissingThemeHandleMiddleware(get_response)
        with self.assertWarnsMessage(Warning, "Theme is missing."):
            middleware.process_exception(request, UncompressableFileError())
        self.assertEqual(0, get_response.call_count)
        self.assertFalse(path.exists(self.file_path))

    def test_save_file_no_theme_in_production(self):
        settings.DEBUG = False
        request = MagicMock()
        get_response = MagicMock()
        middleware = MissingThemeHandleMiddleware(get_response)
        with self.assertRaises(ThemeMissingError):
            middleware.process_exception(request, UncompressableFileError())
        self.assertEqual(0, get_response.call_count)
        self.assertFalse(path.exists(self.file_path))
