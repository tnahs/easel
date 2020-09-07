import logging
import pathlib
from typing import Tuple, Union


logger = logging.getLogger(__name__)


class SiteDefaults:
    """ Primarily used to share the location of the site directory 'path_site'
    across modules as well as default/valid configuration values. """

    # Path to [repo]/src/easel
    PATH_ROOT = pathlib.Path(__file__).parent.parent

    DIRECTORY_NAME_PAGES: str = "pages"
    DIRECTORY_NAME_THEMES: str = "themes"
    DIRECTORY_NAME_TEMPLATES: str = "templates"
    DIRECTORY_NAME_THEMES: str = "themes"
    DIRECTORY_NAME_STATIC: str = "static"
    DIRECTORY_NAME_CACHE: str = ".cache"

    FILENAME_SITE_YAML: str = "site.yaml"
    FILENAME_PAGE_YAML: str = "page.yaml"

    # https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html#jpeg
    PLACEHOLDER_FORMAT: str = "JPEG"
    PLACEHOLDER_SIZE: Tuple[int, int] = (512, 512)
    PLACEHOLDER_QUALITY: int = 95

    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT_PRETTY: str = "YYYY-MM-DD HH:MM:SS"

    DEFAULT_THEME_NAME: str = "sorolla"
    VALID_THEME_NAMES = [
        item.name
        for item in (PATH_ROOT / DIRECTORY_NAME_THEMES).iterdir()
        if item.is_dir() and not item.name.startswith(".")
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
