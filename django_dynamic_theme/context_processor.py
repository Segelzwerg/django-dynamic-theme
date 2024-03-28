"""Defines extra contexts for this application globally."""


def theme(request) -> dict[str, str]:
    """
    Defines the url to the theme to be used.
    Returns: url to theme in a dict.
    """
    return {"theme_file": "theme.scss"}
