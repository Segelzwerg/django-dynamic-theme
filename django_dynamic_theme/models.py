"""Admins modles for Theme."""

from abc import ABCMeta, abstractmethod
from decimal import Decimal
from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from django_dynamic_theme.util.color_converter import hex_to_rgb_tuple
from django_dynamic_theme.util.scss_editor import ScssEditor


# pylint: disable=too-many-ancestors
class FontSizeChoice(models.TextChoices):
    """
    List of pre defined css font sizes.
    Or px or em or % see https://developer.mozilla.org/en-US/docs/Web/CSS/font-size
    """

    XX_SMALL = "xx-small"
    X_SMALL = "x-small"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    X_LARGE = "x-large"
    XX_LARGE = "xx-large"
    XXX_LARGE = "xxx-large"


class AbstractModelMeta(ABCMeta, type(models.Model)):
    """Abstract class for the meta to avoid metaclass exception"""


class ThemeElement(models.Model, metaclass=AbstractModelMeta):
    """
    Abstract class for theme elements.
    :param name: The name of that configuration.
    """

    name = models.CharField(max_length=50)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta class for ThemeElement"""

        abstract = True

    @abstractmethod
    def export(self) -> str:
        """
        Exports the key value pairs as string.
        """

    def save(self, *args, **kwargs) -> None:
        """
        Saves the ThemeElement object and
        triggers the themes to write it's content to the SCSS file.
        """
        super().save(*args, **kwargs)
        themes = self.theme_set.all()  # pylint: disable=no-member
        for theme in themes:
            theme.write_export()

    def __str__(self) -> str:
        """
        Returns the name as string conversion.
        """
        return str(self.name)

    def __repr__(self) -> str:
        """
        Returns the type and the name as representation.
        """
        return f"{self.__class__.__name__}: {self.name}"


class Background(ThemeElement):
    """
    Stores the background colors.
    :param primary_bg: The color of the primary background.
    """

    primary_bg = ColorField(verbose_name="Primary Name")

    def export(self) -> str:
        """
        Exports it's values as string in SCSS format.
        """
        return f"background-color: {self.primary_bg};"


class MediaGallery(ThemeElement):
    """
    A specialization of a n-dimensional list for the purpose of videos / images.
    :param margin_left: The margin of the entire media gallery on left side.
    :param margin_right: The margin of the entire media gallery on right side.
    :param max_width: The maximum width of the entire media gallery.
    :param item_align: The align of the single items within a row.
    :param row_margin_top: The top margin between rows.
    """

    margin_left = models.CharField(max_length=50)
    margin_right = models.CharField(max_length=50)
    max_width = models.CharField(max_length=50)
    item_align = models.CharField(max_length=50)
    row_margin_top = models.CharField(max_length=50)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta definitions of Media Gallery"""
        verbose_name = "Media Gallery"
        verbose_name_plural = "Media Galleries"

    def export(self) -> str:
        """Returns configuration as string."""

        margin_left = f"margin-left: {self.margin_left};"
        margin_right = f"margin-right: {self.margin_right};"
        max_width = f"max-width: {self.max_width};"
        text_align = f"text-align: {self.item_align};"
        row = f".row {{margin-top: {self.row_margin_top};}}"
        media_gallery = f""".mediagallery {{{margin_left}
{margin_right}
{max_width}
{text_align}
{row}}}"""
        return media_gallery


class Navbar(ThemeElement):
    """
    Stores the theming of bootstrap 5 nav bar
    :param background_color: Background color of the Navbar
    :param opacity: How transparent the background is. 0 is full transparent.
    :param font_size: The size of nav bar font.
    :param text_color: Color of the nav bar text.
    :param text_opacity: How transparent the text is. 0 is full transparent.
    """

    background_color = ColorField()
    opacity = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=Decimal(1.00),
    )
    font_size = models.CharField(
        max_length=20, choices=FontSizeChoice.choices, default=FontSizeChoice.MEDIUM
    )
    text_color = ColorField()
    text_opacity = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=Decimal(1.00),
    )

    def export(self) -> str:
        """
        Exports the navbar properties as strings.
        """
        bg_color = ",".join(str(x) for x in hex_to_rgb_tuple(self.background_color))
        navbar = f".navbar {{background-color: rgba({bg_color},{self.opacity:.2f}) !important;}}"
        text_color = (
            ",".join(str(x) for x in hex_to_rgb_tuple(self.text_color))
            + f",{self.text_opacity:.2f}"
        )
        navlink = f".nav-link {{font-size:{self.font_size};color:rgba({text_color});}}"
        return f"{navbar}\n{navlink}"


class Theme(models.Model):
    """
    Combines all values.
    :param name: Name of the theme. Also used as file name + .scss. See self.path()
    :param default: Unique. If that is the default theme.
    :param background: ThemeElement for background.
    :param media_gallery: ThemeElement for media gallery.
    :param navrbar: ThemeElement for nav bar.
    """

    name = models.CharField(max_length=50)
    default = models.BooleanField(default=False)
    background: Background = models.ForeignKey(Background, on_delete=models.CASCADE)
    media_gallery: MediaGallery = models.ForeignKey(
        MediaGallery, default=None, null=True, on_delete=models.DO_NOTHING
    )
    navbar: Navbar = models.ForeignKey(
        Navbar, default=None, null=True, on_delete=models.DO_NOTHING
    )

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

    # pylint: disable=no-member
    def export(self) -> str:
        """
        Exports all listed configurations as string in SCSS format.
        """
        background = self.background.export()
        if not self.media_gallery:
            mediagallery = ''
        else:
            mediagallery = self.media_gallery.export()
        if not self.navbar:
            navbar = ''
        else:
            navbar = self.navbar.export()

        return f"""body {{{background}}}
{mediagallery}
{navbar}"""

    def write_export(self) -> None:
        """Writes the content of the export to the file."""
        scss_editor = ScssEditor(self.path)
        scss_editor.write(self.export())

    def save(self, *args, **kwargs) -> None:
        """
        Saves the Theme object and writes it's content to the SCSS file.
        """
        super().save(*args, **kwargs)
        self.write_export()
