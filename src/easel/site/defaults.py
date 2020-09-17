import logging
import pathlib
from typing import Dict, Tuple, Union


logger = logging.getLogger(__name__)


class Defaults:
    """ Primarily used to share the location of the site directory 'path_site'
    across modules as well as default/valid configuration values. """

    # Path to /repo/src/easel
    APP_ROOT = pathlib.Path(__file__).parent.parent

    DIRECTORY_NAME_BUILD: str = "build"
    DIRECTORY_NAME_CONTENTS: str = "contents"
    DIRECTORY_NAME_SRC: str = "src"
    DIRECTORY_NAME_PAGES: str = "pages"
    DIRECTORY_NAME_SITE_CACHE: str = "site-cache"
    DIRECTORY_NAME_STATIC: str = "static"
    DIRECTORY_NAME_TEMPLATES: str = "templates"
    DIRECTORY_NAME_THEMES: str = "themes"

    FILENAME_SITE_YAML: str = "site.yaml"
    FILENAME_PAGE_YAML: str = "page.yaml"
    FILENAME_THEME_YAML: str = "theme.yaml"

    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT_PRETTY: str = "YYYY-MM-DD HH:MM:SS"

    PROXY_IMAGE_FORMAT: str = "JPEG"
    PROXY_IMAGE_QUALITY: int = 95
    PROXY_IMAGE_SMALL = {
        "name": "small",
        "size": (256, 256),
    }
    PROXY_IMAGE_MEDIUM = {
        "name": "medium",
        "size": (512, 512),
    }
    PROXY_IMAGE_LARGE = {
        "name": "large",
        "size": (1024, 1024),
    }

    DEFAULT_BUILTIN_THEME_NAME: str = "sorolla"
    VALID_BUILTIN_THEME_NAMES = [
        item.name
        for item in (APP_ROOT / DIRECTORY_NAME_THEMES).iterdir()
        if item.is_dir() and not item.name.startswith(".")
    ]

    INSTALLED_THEME_NAME_PREFIX: str = "easel-"

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

    MIMETYPES: Dict[str, str] = {
        # Video
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".mov": "video/quicktime",
        # Audio
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
    }


class Key:
    ALIGN: str = "align"
    AUDIO: str = "audio"
    AUTHOR: str = "author"
    BREAK: str = "break"
    CAPTION: str = "caption"
    COLUMN_COUNT: str = "column-count"
    CONTENTS: str = "contents"
    COPYRIGHT: str = "copyright"
    COVER: str = "cover"
    CUSTOM_PATH: str = "custom-path"
    DATE: str = "date"
    DESCRIPTION: str = "description"
    EMBEDDED: str = "embedded"
    EXTRAS: str = "extras"
    FAVICON: str = "favicon"
    HEADER: str = "header"
    HEIGHT: str = "height"
    HTML: str = "html"
    ICON: str = "icon"
    IMAGE: str = "image"
    IS_GALLERY: str = "is-gallery"
    IS_INDEX: str = "is-index"
    LABEL: str = "label"
    LAYOUT: str = "layout"
    LAYOUT_GALLERY: str = "layout-gallery"
    LAZY: str = "lazy"
    LAZY_GALLERY: str = "lazy-gallery"
    LINKS_TO: str = "links-to"
    LINK_PAGE: str = "link-page"
    LINK_URL: str = "link-url"
    MENU: str = "menu"
    NAME: str = "name"
    OPTIONS: str = "options"
    PATH: str = "path"
    SHOW_CAPTIONS: str = "show-captions"
    SITE_DEBUG: str = "SITE_DEBUG"
    SITE_ROOT: str = "SITE_ROOT"
    SIZE: str = "size"
    SPACER: str = "spacer"
    TEXT: str = "text"
    TEXT_BLOCK: str = "text-block"
    THEME: str = "theme"
    TITLE: str = "title"
    TYPE: str = "type"
    URL: str = "url"
    VIDEO: str = "video"
    WIDTH: str = "width"
