"""Application configuration for the main app."""

from django.apps import AppConfig


class DjangoDynamicThemeConfig(AppConfig):
    """
    Sets the configuration of the main app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_dynamic_theme"
