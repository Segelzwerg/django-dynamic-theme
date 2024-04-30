from compressor.exceptions import UncompressableFileError

from django_dynamic_theme.models import Theme


class CompressorHandleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except UncompressableFileError:
            try:
                theme = Theme.objects.get(default=True)
            except Theme.DoesNotExist:
                theme = Theme.objects.first()
            theme.write_export()
            response = self.get_response(request)
        return response
