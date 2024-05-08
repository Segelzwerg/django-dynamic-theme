"""Errors that can be raised from dynamic theme."""


class ThemeMissingError(Exception):
    """
    Is raised if not theme is set.
    """


class NonHexValueError(Exception):
    """
    Is raised when a value that is not a valid HEX color string is passed to the color converter.
    """
