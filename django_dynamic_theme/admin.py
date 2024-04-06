"""Models for Themes"""

from django.contrib import admin

from django_dynamic_theme.models import Background, Navbar, Theme


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


@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    """
    The admin model for the navigation bar.
    """

    list_display = [
        "background_color",
        "opacity",
        "font_size",
        "text_color",
        "text_opacity",
    ]
