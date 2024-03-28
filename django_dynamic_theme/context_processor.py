"""Defines extra contexts for this application globally."""


def theme_url(request) -> dict[str, str]:
    """
    Defines the url to the theme to be used.
    Returns: url to theme in a dict.
    """
    return {"theme_url": "static/theme.scss"}
