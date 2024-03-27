"""Models for Themes"""

from django.contrib import admin

from django_dynamic_theme.models import Background, Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    """
    The admin model to maange the themes."""

    list_display = ["name", "background"]


@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    """
    The admin model to set the backgrounds.
    """

    list_display = ["primary_bg"]
