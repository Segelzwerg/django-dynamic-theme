"""Admins modles for Theme."""

from abc import ABCMeta
from colorfield.fields import ColorField
from django.db import models


from django_dynamic_theme.utill.scss_editor import ScssEditor


class AbstractModelMeta(ABCMeta, type(models.Model)):
    """Abstract class for the meta to avoid metaclass exception"""

    pass


class ThemeElement(models.Model, metaclass=AbstractModelMeta):
    """Abstract class for theme elements."""

    class Meta:
        abstract = True

    def export(self) -> str:
        pass

    def save(self, *args, **kwargs) -> None:
        """
        Saves the ThemeElement object and
        triggers the themes to write it's content to the SCSS file.
        """
        super().save(*args, **kwargs)
        themes = self.theme_set.all()
        for theme in themes:
            theme.export()


class Background(ThemeElement):
    """
    Stores the background colors.
    """

    name = models.CharField(max_length=50)
    primary_bg = ColorField(verbose_name="Primary Name")

    def export(self) -> str:
        """
        Exports it's values as string in SCSS format.
        """
        return f"background: {self.primary_bg};"

    def __str__(self) -> str:
        """
        Returns the name as string conversion.
        """
        return str(self.name)

    def __repr__(self) -> str:
        """
        Returns the type and the name as representation.
        """
        return f"Background: {self.name}"


class Theme(models.Model):
    """
    Combines all values.
    """

    name = models.CharField(max_length=50)
    default = models.BooleanField(default=False)
    background: Background = models.ForeignKey(Background, on_delete=models.CASCADE)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta class of the Theme."""

        constraints = [
            models.UniqueConstraint(
                fields=["default"],
                condition=models.Q(default=True),
                name="Only one theme can be default.",
            )
        ]

    @property
    def path(self) -> str:
        """
        Returns the path based on the file name.
        """
        return f"static/{self.name}.scss"

    def export(self) -> str:
        """
        Exports all listed configurations as string in SCSS format.
        """
        return f"body {{{self.background.export()}}}"  # pylint: disable=no-member

    def save(self, *args, **kwargs) -> None:
        """
        Saves the Theme object and writes it's content to the SCSS file.
        """
        super().save(*args, **kwargs)
        scss_editor = ScssEditor(self.path)
        scss_editor.write(self.export())
