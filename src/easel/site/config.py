import logging
import pathlib
from typing import List, Optional, Tuple, Union

from . import errors


logger = logging.getLogger(__name__)


class Config:

    PATH_ROOT = pathlib.Path(__file__).parent.parent

    DIRECTORY_NAME_PAGES: str = "pages"
    DIRECTORY_NAME_ERRORS: str = "errors"
    DIRECTORY_NAME_ERROR_404: str = "404"
    DIRECTORY_NAME_ERROR_500: str = "500"

    FILENAME_SITE_YAML: str = "site.yaml"
    FILENAME_PAGE_YAML: str = "page.yaml"
    FILENAME_PAGE_DESCRIPTION: str = "page-description.md"

    DEFAULT_THEME: str = "vertical"
    VALID_THEMES: List[str] = [
        DEFAULT_THEME,
        "horizontal",
    ]

    DEFAULT_SIZE = "medium"
    VALID_SIZES: Tuple[str, ...] = (
        "small",
        DEFAULT_SIZE,
        "large",
    )

    VALID_ALIGNMENTS: Tuple[str, ...] = (
        "left",
        "center",
        "right",
        "justify",
    )

    VALID_GALLERY_COLUMN_COUNT: Tuple[Union[str, int], ...] = (
        "auto",
        2,
        3,
        4,
        5,
        6,
    )

    VALID_IMAGE_EXTENSIONS: Tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    )
    VALID_VIDEO_EXTENSIONS: Tuple[str, ...] = (
        ".mp4",
        ".webm",
        ".mov",
    )
    VALID_AUDIO_EXTENSIONS: Tuple[str, ...] = (
        ".mp3",
        ".wav",
    )
    VALID_YAML_EXTENSIONS: Tuple[str, ...] = (
        ".yaml",
        ".yml",
    )
    VALID_TEXT_EXTENSIONS: Tuple[str, ...] = (
        ".md",
        ".txt",
    )

    MIMETYPES = {
        # Video
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".mov": "video/quicktime",
        # Audio
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
    }

    _path_site: Optional[pathlib.Path] = None
    _theme_name: str = DEFAULT_THEME

    @property
    def path_site(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site] """

        if self._path_site is None:
            raise errors.SiteConfigError("Site directory must be set before running.")

        return self._path_site

    @path_site.setter
    def path_site(self, value: str) -> None:
        """ Sets /absolute/path/to/[site] """

        path_site = pathlib.Path(value)

        try:
            path_site = path_site.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                f"Site directory {path_site} does not exist."
            ) from error

        self._path_site = path_site

    @property
    def path_site_pages(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/pages """

        path_site_pages = self.path_site / self.DIRECTORY_NAME_PAGES

        try:
            return path_site_pages.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError("Site missing 'pages' directory.") from error

    @property
    def path_site_errors(self) -> Optional[pathlib.Path]:
        """ Returns /absolute/path/to/[site]/errors """

        path_site_errors = self.path_site / self.DIRECTORY_NAME_ERRORS

        try:
            return path_site_errors.resolve(strict=True)
        except FileNotFoundError:
            return None

    @property
    def file_site_yaml(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/site.yaml """
        return self.path_site / self.FILENAME_SITE_YAML

    @property
    def theme_name(self) -> str:
        """ Returns current theme name. """
        return self._theme_name

    @theme_name.setter
    def theme_name(self, value: Optional[str]) -> None:
        """ Sets theme name. """

        if not value:
            return

        if value not in self.VALID_THEMES:
            raise errors.SiteConfigError(
                f"Invalid theme '{value}'. Valid themes are: {self.VALID_THEMES}."
            )

        self._theme_name = value

    @property
    def path_themes(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[application]/themes. """
        return self.PATH_ROOT / "themes"

    @property
    def path_theme(self) -> pathlib.Path:
        """ Returns the path to the current theme. """
        return self.path_themes / self.theme_name

    @property
    def path_theme_static(self) -> pathlib.Path:
        """ Returns the path to the current theme's static directory. """
        return self.path_theme / "static"

    @property
    def path_theme_templates(self) -> pathlib.Path:
        """ Returns the path to the current theme's templates directory. """
        return self.path_theme / "templates"

    '''
    @property
    def path_custom_theme(self) -> Optional[pathlib.Path]:
        """ Returns the path to a custom theme. """
        return self._path_custom_theme

    @path_custom_theme.setter
    def path_custom_theme(self, value: Optional[str]) -> None:
        """ Sets the path to a custom theme. """

        if not value:
            return

        path_custom_theme = pathlib.Path(value)

        try:
            path_custom_theme = path_custom_theme.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                f"Custom theme directory '{path_custom_theme}' does not exist."
            ) from error

        logger.info(f"Using custom theme from {path_custom_theme}.")

        self._path_custom_theme = path_custom_theme
    '''

    @property
    def _assets_theme(self) -> List[pathlib.Path]:
        """ See Config.assets below. """
        return list(self.path_theme.glob("**/*"))

    @property
    def _assets_site(self) -> List[pathlib.Path]:
        """ See Config.assets below. """
        return list(self.path_site.glob("**/*"))

    @property
    def assets(self) -> List[pathlib.Path]:
        """ Returns a list of paths pointing to all the sub-directories and
        files inside the main site directory. When starting up a development
        server, this list is passed to the 'extra_files' argument, allowing it
        to reload when any of the site files are modifed.

        via. https://werkzeug.palletsprojects.com/en/1.0.x/serving/ """
        return [*self._assets_theme, *self._assets_site]


config = Config()
