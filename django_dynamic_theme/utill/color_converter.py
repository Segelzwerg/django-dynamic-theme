"""Converts colors into different formats."""


def hex_to_tuple(hex_str: str) -> tuple[str, str, str]:
    """
    Splits a #XXYYZZ HEX string into a tuple of strs (XX,YY,ZZ)
    """
    hex_str = hex_str.lstrip("#")
    return tuple(map(str, (hex_str[0:2], hex_str[2:4], hex_str[4:6])))


def hex_to_rgb_tuple(hex_str: str) -> tuple[int, int, int]:
    """
    Converts a hex string to a RGB tuple.
    """
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))
