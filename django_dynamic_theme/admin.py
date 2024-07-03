"""Models for Themes"""

from django.contrib import admin

from django_dynamic_theme.models import Background, MediaGallery, Navbar, Theme


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

    list_display = ["name", "primary_bg"]


@admin.register(MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    """
    The admin model for the media gallery.
    """

    list_display = [
        "name",
        "margin_left",
        "margin_right",
        "max_width",
        "item_align",
        "row_margin_top",
    ]


@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    """
    The admin model for the navigation bar.
    """

    list_display = [
        "name",
        "background_color",
        "opacity",
        "font_size",
        "text_color",
        "text_opacity",
    ]
