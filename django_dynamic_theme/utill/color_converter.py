"""Converts colors into different formats."""


def hex_to_tuple(hex: str) -> tuple[str, str, str]:
    """
    Splits a #XXYYZZ HEX string into a tuple of strs (XX,YY,ZZ)
    """
    hex = hex.lstrip("#")
    return tuple(map(str, (hex[0:2], hex[2:4], hex[4:6])))


def hex_to_rgb_tuple(hex: str) -> tuple[int, int, int]:
    """
    Converts a hex string to a RGB tuple.
    """
    hex = hex.lstrip("#")
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
