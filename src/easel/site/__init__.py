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
    DIRECTORY_NAME_THEMES: str = "themes"
    DIRECTORY_NAME_TEMPLATES: str = "templates"
    DIRECTORY_NAME_STATIC: str = "static"
    DIRECTORY_NAME_CACHE: str = ".cache"

    FILENAME_SITE_YAML: str = "site.yaml"
    FILENAME_PAGE_YAML: str = "page.yaml"

    # https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html#jpeg
    PLACEHOLDER_FORMAT: str = "JPEG"
    PLACEHOLDER_SIZE: Tuple[int, int] = (512, 512)
    PLACEHOLDER_QUALITY: int = 95

    DEFAULT_THEME_NAME: str = "sargent"
    VALID_THEME_NAMES: List[str] = [
        DEFAULT_THEME_NAME,
        "sorolla",
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

    VALID_COLUMN_COUNT: Tuple[Union[str, int], ...] = (
        "auto",
        *range(2, 7),
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
    VALID_TEXT_EXTENSIONS: Tuple[str, ...] = (
        ".md",
        ".txt",
    )

    VALID_YAML_EXTENSIONS: Tuple[str, ...] = (
        ".yaml",
        ".yml",
    )

    VALID_CONTENT_EXTENSIONS: Tuple[str, ...] = (
        *VALID_IMAGE_EXTENSIONS,
        *VALID_VIDEO_EXTENSIONS,
        *VALID_AUDIO_EXTENSIONS,
        *VALID_TEXT_EXTENSIONS,
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
    _theme_name: str = DEFAULT_THEME_NAME

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
    def file_site_yaml(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/site.yaml """
        return self.path_site / self.FILENAME_SITE_YAML

    @property
    def path_site_pages(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/pages """

        path_site_pages = self.path_site / self.DIRECTORY_NAME_PAGES

        try:
            return path_site_pages.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError("Site missing 'pages' directory.") from error

    @property
    def path_site_cache(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/.cache """
        return self.path_site / self.DIRECTORY_NAME_CACHE

    @property
    def path_site_errors(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/errors """
        return self.path_site / self.DIRECTORY_NAME_ERRORS

    @property
    def path_site_error_404(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/errors/404 """
        return self.path_site_errors / self.DIRECTORY_NAME_ERROR_404

    @property
    def path_site_error_500(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/errors/500 """
        return self.path_site_errors / self.DIRECTORY_NAME_ERROR_500

    @property
    def path_themes(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[application]/themes. """
        return self.PATH_ROOT / self.DIRECTORY_NAME_THEMES

    @property
    def theme_name(self) -> str:
        """ Returns current theme name. """
        return self._theme_name

    @theme_name.setter
    def theme_name(self, value: Optional[str]) -> None:
        """ Sets theme name. """

        if not value:
            return

        if value not in self.VALID_THEME_NAMES:
            raise errors.SiteConfigError(
                f"Invalid theme '{value}'. Valid themes are: {self.VALID_THEME_NAMES}."
            )

        self._theme_name = value

    @property
    def path_theme(self) -> pathlib.Path:
        """ Returns the path to the current theme. """
        return self.path_themes / self.theme_name

    @property
    def path_theme_static(self) -> pathlib.Path:
        """ Returns the path to the current theme's static directory. """
        return self.path_theme / self.DIRECTORY_NAME_STATIC

    @property
    def path_theme_templates(self) -> pathlib.Path:
        """ Returns the path to the current theme's templates directory. """
        return self.path_theme / self.DIRECTORY_NAME_TEMPLATES

    @property
    def _assets_theme(self) -> List[pathlib.Path]:
        """ See Config.assets below. """
        return list(self.path_theme.glob("**/*"))

    @property
    def _assets_site(self) -> List[pathlib.Path]:
        """ See Config.assets below. """

        assets_site = []

        for item in self.path_site.glob("**/*"):

            if item.name == self.DIRECTORY_NAME_CACHE:
                continue

            assets_site.append(item)

        return assets_site

    @property
    def assets(self) -> List[pathlib.Path]:
        """ Returns a list of paths pointing to all the sub-directories and
        files inside the main site directory. When starting up a development
        server, this list is passed to the 'extra_files' argument, allowing it
        to reload when any of the site files are modifed.

        via. https://werkzeug.palletsprojects.com/en/1.0.x/serving/ """
        return [*self._assets_theme, *self._assets_site]


global_config = Config()
