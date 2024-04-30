from os import mkdir, path, remove
from unittest.mock import MagicMock
from compressor.exceptions import UncompressableFileError
from django.test import TestCase

from django_dynamic_theme.errors import ThemeMissingError
from django_dynamic_theme.middleware import MissingThemeHandleMiddleware
from django_dynamic_theme.models import Background, Navbar, Theme


class MiddlewareTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.theme_name = "test"
        self.folder = "static/"
        self.file_path = f"{self.folder}/{self.theme_name}.scss"

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
            name=self.theme_name, background=background, navbar=navbar, default=True
        )
        request = MagicMock()
        get_response = MagicMock(side_effect=[UncompressableFileError, "200"])
        middleware = MissingThemeHandleMiddleware(get_response)
        response = middleware(request)
        get_response.assert_called_with(request)
        self.assertEqual(2, get_response.call_count)
        self.assertEqual("200", response)
        self.assertTrue(path.exists(self.file_path))

    def test_save_file_no_default(self):
        color: str = "F0F0F0"
        background: Background = Background.objects.create(primary_bg=color)
        navbar: Navbar = Navbar.objects.create(
            name="Test", background_color="#FFFF00", text_color="#111111"
        )
        Theme.objects.create(
            name=self.theme_name, background=background, navbar=navbar, default=False
        )
        request = MagicMock()
        get_response = MagicMock(side_effect=[UncompressableFileError, "200"])
        middleware = MissingThemeHandleMiddleware(get_response)
        response = middleware(request)
        get_response.assert_called_with(request)
        self.assertEqual(2, get_response.call_count)
        self.assertEqual("200", response)
        self.assertTrue(path.exists(self.file_path))

    def test_save_file_no_theme(self):
        request = MagicMock()
        get_response = MagicMock(side_effect=[UncompressableFileError, "200"])
        middleware = MissingThemeHandleMiddleware(get_response)
        _ = middleware(request)
        with self.assertRaises(ThemeMissingError):
            get_response.assert_called_with(request)
        self.assertEqual(1, get_response.call_count)
        self.assertFalse(path.exists(self.file_path))
