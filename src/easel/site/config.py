import logging
import pathlib
from typing import Tuple, Union, Optional

from . import errors


logger = logging.getLogger(__name__)


class ConfigKeys:
    PATH_USER_SITE: str = "PATH_USER_SITE"


class Config:

    PATH_ROOT = pathlib.Path(__file__).parent.parent

    DIRECTORY_NAME_PAGES: str = "pages"

    FILENAME_SITE_YAML: str = "site.yaml"
    FILENAME_PAGE_YAML: str = "page.yaml"
    FILENAME_PAGE_DESCRIPTION: str = "page-description.md"
    FILENAME_PAGE_BODY: str = "page-body.md"

    DEFAULT_SIZE = "medium"
    VALID_SIZES: Tuple[str, ...] = (
        "small",
        DEFAULT_SIZE,
        "large",
    )

    # TODO: Implement this with validation methods.
    DEFAULT_ALIGNMENT: str = "left"
    VALID_ALIGNMENTS: Tuple[str, ...] = (
        DEFAULT_ALIGNMENT,
        "center",
        "right",
        "justify",
    )

    DEFAULT_GALLERY_COLUMN_WIDTH: str = "250px"
    DEFAULT_GALLERY_COLUMN_COUNT: str = "auto"
    VALID_GALLERY_COLUMN_COUNT: Tuple[Union[str, int], ...] = (
        DEFAULT_GALLERY_COLUMN_COUNT,
        2,
        3,
        4,
        5,
        6,
    )

    VALID_IMAGE_TYPES: Tuple[str, ...] = (
        ".jpg",
        ".png",
        ".gif",
    )
    VALID_VIDEO_TYPES: Tuple[str, ...] = (
        ".mp4",
        ".webm",
    )
    VALID_AUDIO_TYPES: Tuple[str, ...] = (
        ".mp3",
        ".wav",
    )
    VALID_YAML_TYPES: Tuple[str, ...] = (
        ".yaml",
        ".yml",
    )
    VALID_TEXT_TYPES: Tuple[str, ...] = (
        ".md",
        ".txt",
    )

    def __init__(self):

        self._path_user_site: Optional[pathlib.Path] = None
        self._path_assets: pathlib.Path = self.PATH_ROOT / "main" / "assets"

    @property
    def path_user_site(self) -> pathlib.Path:

        if self._path_user_site is None:
            raise errors.ConfigError(
                f"{ConfigKeys.PATH_USER_SITE} must be set before running."
            )

        return self._path_user_site

    @path_user_site.setter
    def path_user_site(self, value: str) -> None:
        # /absolute/path/to/[site]

        path_user_site = pathlib.Path(value)

        try:
            path_user_site = path_user_site.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.ConfigError(
                f"{ConfigKeys.PATH_USER_SITE} directory {path_user_site} does not exist."
            ) from error

        self._path_user_site = path_user_site

    @property
    def path_user_site_pages(self) -> pathlib.Path:
        # /absolute/path/to/[site]/pages

        path_user_site_pages = self.path_user_site / self.DIRECTORY_NAME_PAGES

        try:
            path_user_site_pages = path_user_site_pages.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.ConfigError("Site missing 'pages' directory.") from error

        return path_user_site_pages

    @property
    def file_site_yaml(self) -> pathlib.Path:
        # /absolute/path/to/[site]/site.yaml
        return self.path_user_site / self.FILENAME_SITE_YAML

    @property
    def path_assets(self) -> pathlib.Path:
        return self._path_assets

    @path_assets.setter
    def path_assets(self, value: Optional[str]):

        if value is None:
            return

        path_assets = pathlib.Path(value)

        try:
            path_assets = path_assets.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.ConfigError(
                f"{ConfigKeys.PATH_USER_SITE} directory {path_assets} does not exist."
            ) from error

        logger.debug(f"Using custom assets directory: {path_assets}.")

        self._path_assets = path_assets

    @property
    def path_templates(self) -> pathlib.Path:
        return self._path_assets / "templates"

    @property
    def path_static(self) -> pathlib.Path:
        return self._path_assets / "static"


config = Config()
