import logging
import pathlib
from typing import Tuple, Union, Optional

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
    FILENAME_PAGE_BODY: str = "page-body.md"

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

    VALID_IMAGE_TYPES: Tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    )
    VALID_VIDEO_TYPES: Tuple[str, ...] = (
        ".mp4",
        ".webm",
        ".mov",
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

    MIMETYPES = {
        # Video
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".mov": "video/quicktime",
        # Audio
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
    }

    def __init__(self):

        self._path_site: Optional[pathlib.Path] = None
        self._path_assets: pathlib.Path = self.PATH_ROOT / "main" / "assets"

    @property
    def path_site(self) -> pathlib.Path:

        if self._path_site is None:
            raise errors.SiteConfigError("Site path must be set before running.")

        return self._path_site

    @path_site.setter
    def path_site(self, value: str) -> None:
        # /absolute/path/to/[site]

        path_site = pathlib.Path(value)

        try:
            path_site = path_site.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                f"Site path '{path_site}' does not exist."
            ) from error

        self._path_site = path_site

    @property
    def path_site_pages(self) -> pathlib.Path:
        # /absolute/path/to/[site]/pages

        path_site_pages = self.path_site / self.DIRECTORY_NAME_PAGES

        try:
            path_site_pages = path_site_pages.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError("Site missing 'pages' directory.") from error

        return path_site_pages

    @property
    def path_site_errors(self) -> Optional[pathlib.Path]:
        # /absolute/path/to/[site]/errors

        path_site_errors = self.path_site / self.DIRECTORY_NAME_ERRORS

        try:
            path_site_errors = path_site_errors.resolve(strict=True)
        except FileNotFoundError:
            return None

        return path_site_errors

    @property
    def file_site_yaml(self) -> pathlib.Path:
        # /absolute/path/to/[site]/site.yaml
        return self.path_site / self.FILENAME_SITE_YAML

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
            raise errors.SiteConfigError(
                f"Site 'path' directory {path_assets} does not exist."
            ) from error

        logger.info(f"Using custom assets directory: {path_assets}.")

        self._path_assets = path_assets

    @property
    def path_templates(self) -> pathlib.Path:
        return self._path_assets / "templates"

    @property
    def path_static(self) -> pathlib.Path:
        return self._path_assets / "static"

    def get_mimetype(self, filetype: str) -> str:

        if not filetype.startswith("."):
            filetype = f".{filetype}"

        mimetype = self.MIMETYPES.get(filetype, None)

        if mimetype is None:
            logger.warning(f"Unsupported MIME Type '{filetype}' detected.")
            return ""

        return mimetype


config = Config()
