"""Middlewares for the dynamic theme app."""

from compressor.exceptions import UncompressableFileError

from django_dynamic_theme.errors import ThemeMissingError
from django_dynamic_theme.models import Theme


# pylint: disable=too-few-public-methods
class MissingThemeHandleMiddleware:
    """
    Detects if the theme file is missing.
    If a default theme is set it will export this one.
    If there is not default theme it will export the first one.
    If no theme exists it will raise an error.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    # pylint: disable=no-member
    def __call__(self, request):
        try:
            response = self.get_response(request)
        except UncompressableFileError as uncomp_error:
            try:
                theme = Theme.objects.get(default=True)
            except Theme.DoesNotExist:
                theme = Theme.objects.first()
            if theme is None:
                raise ThemeMissingError from uncomp_error
            theme.write_export()
            response = self.get_response(request)
        return response
