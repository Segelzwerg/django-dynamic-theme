"""Defines the signals for this app.
"""

from django.dispatch import receiver
from django.db.models.signals import post_delete, post_migrate

from django_dynamic_theme.models import Theme
from django_dynamic_theme.util.scss_editor import ScssEditor


@receiver(post_delete, sender=Theme)
def delete_file(
    sender, instance, *args, **kwargs  # pylint: disable=unused-argument
) -> None:
    """
    Removes the scss file for a theme.
    :param sender: not used
    :param instance: the theme that has been remove.
    """
    scss_editor = ScssEditor(instance.path)
    scss_editor.delete()


@receiver(post_migrate)
def save_file(**kwargs) -> None:
    """
    Saves the default theme file.
    """
    default_theme: Theme = Theme.objects.filter(default=True).first()
    if default_theme:
        default_theme.write_export()
