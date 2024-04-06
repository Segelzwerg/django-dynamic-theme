"""Converts colors into different formats."""


def hex_to_tuple(rgb: str) -> tuple[str, str, str]:
    """
    Splits a #XXYYZZ HEX string into a tuple of strs (XX,YY,ZZ)
    """
    rgb = rgb.replace("#", "")
    return tuple((rgb[0:2], rgb[2:4], rgb[4:6]))
