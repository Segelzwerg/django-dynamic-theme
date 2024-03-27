"""Writes SCSS configuration to a file."""


# pylint: disable=too-few-public-methods
class ScssEditor:
    """
    Handler for each of the themes created.
    """

    def __init__(self, file: str) -> None:
        """
        Creates a editor instance.
        :param file: path to a scss file
        """
        self._file = file

    def write(self, output: str) -> None:
        """
        Writes the content to a scss file.
        :param: output: the SCSS configuration.
        """
        with open(self._file, mode="w", encoding="UTF-8") as file:
            file.write(output)
