"""Application configuration for the main app."""

from django.apps import AppConfig


class DjangoDynamicThemeConfig(AppConfig):
    """
    Sets the configuration of the main app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_dynamic_theme"

    def ready(self) -> None:
        """
        Imports the signals to the app configuration.
        """
        import django_dynamic_theme.signals  # noqa F401 imports not being used pylint: disable=C0415,W0611
