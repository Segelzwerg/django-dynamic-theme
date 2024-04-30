from compressor.exceptions import UncompressableFileError

from django_dynamic_theme.models import Theme


class CompressorHandleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except UncompressableFileError:
            Theme.objects.get(default=True).save()
            response = self.get_response(request)
        return response
