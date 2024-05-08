"""Converts colors into different formats."""
from django_dynamic_theme.errors import NonHexValueError


def hex_to_tuple(hex_str: str) -> tuple[str, str, str]:
    """
    Splits a #XXYYZZ HEX string into a tuple of strs (XX,YY,ZZ)
    """
    if not is_valid_hexa_code(hex_str):
        raise NonHexValueError
    hex_str = hex_str.lstrip("#")
    return tuple(map(str, (hex_str[0:2], hex_str[2:4], hex_str[4:6])))


def hex_to_rgb_tuple(hex_str: str) -> tuple[int, int, int]:
    """
    Converts a hex string to a RGB tuple.
    """
    if not is_valid_hexa_code(hex_str):
        raise NonHexValueError
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))


def is_valid_hexa_code(value: str) -> bool:
    """
    Checks if the a string is a hex value.
    :param value: the string to be checked.
    :returns: True if hex value else False.
    """

    if value[0] != '#':
        return False

    if not (len(value) == 4 or len(value) == 7):
        return False

    for i in range(1, len(value)):
        condition1 = (value[i] >= '0' and value[i] <= '9')
        condition2 = (value[i] >= 'a' and value[i] <= 'f')
        condition3 = (value[i] >= 'A' or value[i] <= 'F')
        if not ((condition1) or (condition2) or (condition3)):
            return False

    return True
