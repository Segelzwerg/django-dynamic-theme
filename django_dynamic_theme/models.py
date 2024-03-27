"""Admins modles for Theme."""

from colorfield.fields import ColorField
from django.db import models

from django_dynamic_theme.utill.scss_editor import ScssEditor


class Background(models.Model):
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
        return self.name

    def __repr__(self) -> str:
        return f"Background: {self.name}"


class Theme(models.Model):
    """
    Combines all values.
    """

    name = models.CharField(max_length=50)
    background = models.ForeignKey(Background, on_delete=models.CASCADE)

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
        return f"body {{{self.background.export()}}}"

    def save(self, *args, **kwargs) -> None:
        """
        Saves the Theme object and writes it's content to the SCSS file.
        """
        super().save(*args, **kwargs)
        scss_editor = ScssEditor(self.path)
        scss_editor.write(self.export())
