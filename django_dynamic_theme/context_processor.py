"""Defines extra contexts for this application globally."""

from django_dynamic_theme.models import Theme


# pylint: disable=no-member
def theme(_) -> dict[str, str]:
    """
    Defines the url to the theme to be used.
    Returns: url to theme in a dict.
    """

    try:
        admin_default: Theme = Theme.objects.get(default=True)
        return {"theme_file": f"{admin_default.name}.scss"}
    except Theme.DoesNotExist:
        return {"theme_file": "theme.scss"}
