from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "example_app/index.html"
