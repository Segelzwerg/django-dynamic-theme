from .. import errors

"""Converts colors into different formats."""


def hex_to_tuple(hex_str: str) -> tuple[str, str, str]:
    """
    Splits a #XXYYZZ HEX string into a tuple of strs (XX,YY,ZZ)
    """
    if not isValidHexaCode(hex_str):
        raise errors.NonHexValueError
    hex_str = hex_str.lstrip("#")
    return tuple(map(str, (hex_str[0:2], hex_str[2:4], hex_str[4:6])))


def hex_to_rgb_tuple(hex_str: str) -> tuple[int, int, int]:
    """
    Converts a hex string to a RGB tuple.
    """
    if not is_valid_hexa_code(hex_str):
        raise errors.NonHexValueError
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))


def is_valid_hexa_code(str):

    if (str[0] != '#'):
        return False

    if (not (len(str) == 4 or len(str) == 7)):
        return False

    for i in range(1, len(str)):
        condition1 = (str[i] >= '0' and str[i] <= '9')
        condition2 = (str[i] >= 'a' and str[i] <= 'f')
        condition3 = (str[i] >= 'A' or str[i] <= 'F')
        if (not ((condition1) or (condition2) or (condition3))):
            return False

    return True
