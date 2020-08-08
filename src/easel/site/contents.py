import logging
import pathlib
from typing import TYPE_CHECKING, Any, Optional, Type, Union

from flask import url_for

from . import errors
from .config import config
from .helpers import markdown


if TYPE_CHECKING:
    from .pages import PageType


logger = logging.getLogger(__name__)


""" Ah, it looks like you are trying to instantiate a type, so your dict should
b typed Dict[int, Type[Message]] not Dict[int, Message]. This will cause mypy
to complain too many arguments are passed, which is correct I believe, since
the base Message doesn't have any dataclass attributes, and uses __slots__.

https://github.com/python/mypy/issues/5361#issuecomment-405113523 """
_ContentType = Union[
    Type["Image"],
    Type["Video"],
    Type["Audio"],
    Type["TextBlock"],
    Type["Embedded"],
    Type["Header"],
    Type["Break"],
]

ContentType = Union[
    "Image", "Video", "Audio", "Embedded", "TextBlock", "Header", "Break",
]


class ContentFactory:
    def __init__(self):
        self._content_types = {
            "image": Image,
            "video": Video,
            "audio": Audio,
            "text-block": TextBlock,
            "embedded": Embedded,
            "header": Header,
            "break": Break,
        }

    def build(self, page: "PageType", content_data: dict) -> ContentType:
        """ Builds Content-like object from a dictionary. See respective
        classes for documentation on accepted keys and structure. """

        try:
            content_type: str = content_data["type"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'type' in {content_data} in {page.file_config}."
            ) from error

        # Get Content class based on 'content_type'.
        Content: Optional[_ContentType] = self.content_types(content_type=content_type)

        if Content is None:
            raise errors.ConfigError(
                f"Unsupported value for 'type' '{content_type}' in {page.file_config}."
            )

        return Content(page=page, **content_data)

    def content_types(self, content_type: str) -> Optional[_ContentType]:
        return self._content_types.get(content_type, None)

    def register_content_type(self, name: str, content: Any) -> None:
        """ Register new Content-like object. """
        self._content_types[name] = content


class Image:

    is_image: bool = True

    def __init__(self, page: "PageType", **content_data):
        """ Creates an Image object from a dictionary with the following
        attributes:

            {
                "type": "image",
                "path": [str: path/to/image],
                "caption": {
                    "title": [str: title],
                    "description": [str: description],
                },
            }
        """
        self._page: "PageType" = page

        try:
            path: str = content_data["path"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'path' in {content_data} in {self._page.file_config}."
            ) from error

        # For Layout pages, 'path' is passed as a path relative to the page
        # directory. In this case, concatenate both paths.
        if self._page.is_layout:
            self._path_absolute: pathlib.Path = self._page.path_absolute / path
        else:
            self._path_absolute: pathlib.Path = pathlib.Path(path)

        caption: Optional[dict] = content_data.get("caption")

        if caption is not None:
            self._title: str = caption.get("title", "")
            self._description: str = caption.get("description", "")

        self._validate()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: page:{self._page} filename:{self._filename}>"
        )

    def _validate(self) -> None:

        # Validate image exists.
        if not self._path_absolute.exists():
            raise errors.MissingContent(
                f"Missing '{self._filename}' in {self._path_absolute}."
            )

        # Validate if supported image type.
        if self._filetype not in config.VALID_IMAGE_TYPES:
            raise errors.UnsupportedContentType(
                f"Unsupported image type '{self._filename}' in {self._path_absolute}."
            )

    @property
    def _filename(self) -> str:
        return self._path_absolute.name

    @property
    def _filetype(self) -> str:
        return self._path_absolute.suffix

    @property
    def path_absolute(self) -> pathlib.Path:
        return self._path_absolute

    @property
    def path_relative(self) -> pathlib.Path:
        """ Returns path relative to to /[site]. """
        return self._path_absolute.relative_to(config.path_site)

    @property
    def src(self) -> str:
        return url_for("site.static", filename=self.path_relative)

    @property
    def title(self) -> str:
        return markdown.from_string(self._title)

    @property
    def description(self) -> str:
        return markdown.from_string(self._description)


class Video:

    is_video: bool = True

    MIME_TYPES = {".mp4": "video/mpeg", ".webm": "video/webm"}

    def __init__(self, page: "PageType", **content_data):
        """ Creates an Video object from a dictionary with the following
        attributes:

            {
                "type": "video",
                "path": [str: path/to/video],
                "caption": {
                    "title": [str: title],
                    "description": [str: description],
                },
            }
        """
        self._page: "PageType" = page

        try:
            path: str = content_data["path"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'path' in {content_data} in {self._page.file_config}."
            ) from error

        # For Layout pages, 'path' is passed as a path relative to the page
        # directory. In this case, concatenate both paths.
        if self._page.is_layout:
            self._path_absolute: pathlib.Path = self._page.path_absolute / path
        else:
            self._path_absolute: pathlib.Path = pathlib.Path(path)

        caption: Optional[dict] = content_data.get("caption")

        if caption is not None:
            self._title: str = caption.get("title", "")
            self._description: str = caption.get("description", "")

        self._validate()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: page:{self._page} filename:{self._filename}>"
        )

    def _validate(self) -> None:

        # Validate video exists.
        if not self._path_absolute.exists():
            raise errors.MissingContent(
                f"Missing '{self._filename}' in {self._path_absolute}."
            )

        # Validate if supported video type.
        if self._filetype not in config.VALID_VIDEO_TYPES:
            raise errors.UnsupportedContentType(
                f"Unsupported video type '{self._filename}' in {self._path_absolute}."
            )

    @property
    def _filename(self) -> str:
        return self._path_absolute.name

    @property
    def _filetype(self) -> str:
        return self._path_absolute.suffix

    @property
    def path_absolute(self) -> pathlib.Path:
        return self._path_absolute

    @property
    def path_relative(self) -> pathlib.Path:
        """ Returns path relative to to /[site]. """
        return self._path_absolute.relative_to(config.path_site)

    @property
    def src(self) -> str:
        return url_for("site.static", filename=self.path_relative)

    @property
    def mime_type(self) -> str:
        return self.MIME_TYPES[self._filetype]

    @property
    def title(self) -> str:
        return markdown.from_string(self._title)

    @property
    def description(self) -> str:
        return markdown.from_string(self._description)


class Embedded:

    is_embedded: bool = True

    def __init__(self, page: "PageType", **content_data):
        """ Creates an Embedded object from a dictionary with the following
        attributes:

            {
                "type": "embedded",
                "html": [str: html],
                "caption": {
                    "title": [str: title],
                    "description": [str: description],
                },
            }
        """

        self._page: "PageType" = page

        try:
            self._html: str = content_data["html"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'html' in {content_data} in {self._page.file_config}."
            ) from error

        caption: Optional[dict] = content_data.get("caption")

        if caption is not None:
            self._title: str = caption.get("title", "")
            self._description: str = caption.get("description", "")

        self._validate()

    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self._page} html:{self._html}>"

    def _validate(self) -> None:
        pass

    @property
    def html(self) -> str:
        return self._html

    @property
    def title(self) -> str:
        return markdown.from_string(self._title)

    @property
    def description(self) -> str:
        return markdown.from_string(self._description)


class Audio:

    is_audio: bool = True

    MIME_TYPES = {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
    }

    def __init__(self, page: "PageType", **content_data):
        """ Creates an Audio object from a dictionary with the following
        attributes:

            {
                "type": "audio",
                "path": [str: path/to/audio],
                "caption": {
                    "title": [str: title],
                    "description": [str: description],
                },
            }
        """

        self._page: "PageType" = page

        try:
            path: str = content_data["path"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'path' in {content_data} in {self._page.file_config}."
            ) from error

        # For Layout pages, 'path' is passed as a path relative to the page
        # directory. In this case, concatenate both paths.
        if self._page.is_layout:
            self._path_absolute: pathlib.Path = self._page.path_absolute / path
        else:
            self._path_absolute: pathlib.Path = pathlib.Path(path)

        caption: Optional[dict] = content_data.get("caption")

        if caption is not None:
            self._title: str = caption.get("title", "")
            self._description: str = caption.get("description", "")

        self._validate()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: page:{self._page} filename:{self._filename}>"
        )

    def _validate(self) -> None:

        # Validate audio exists.
        if not self._path_absolute.exists():
            raise errors.MissingContent(
                f"Missing '{self._filename}' in {self._path_absolute}."
            )

        # Validate if supported audio type.
        if self._filetype not in config.VALID_AUDIO_TYPES:
            raise errors.UnsupportedContentType(
                f"Unsupported audio type '{self._filename}' in {self._path_absolute}."
            )

    @property
    def _filename(self) -> str:
        return self._path_absolute.name

    @property
    def _filetype(self) -> str:
        return self._path_absolute.suffix

    @property
    def path_absolute(self) -> pathlib.Path:
        return self._path_absolute

    @property
    def path_relative(self) -> pathlib.Path:
        """ Returns path relative to to /[site]. """
        return self._path_absolute.relative_to(config.path_site)

    @property
    def src(self) -> str:
        return url_for("site.static", filename=self.path_relative)

    @property
    def mime_type(self) -> str:
        return self.MIME_TYPES[self._filetype]

    @property
    def title(self) -> str:
        return markdown.from_string(self._title)

    @property
    def description(self) -> str:
        return markdown.from_string(self._description)


class TextBlock:

    is_text_block: bool = True

    def __init__(self, page: "PageType", **content_data):
        """ Creates an TextBlock object from a dictionary with the following
        attributes:

            {
                "type": "text-block",
                "path": [str: path/to/text],
            }
        """

        self._page: "PageType" = page

        try:
            path: str = content_data["path"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'path' in {content_data} in {self._page.file_config}."
            ) from error

        # For Layout pages, 'path' is passed as a path relative to the page
        # directory. In this case, concatenate both paths.
        if self._page.is_layout:
            self._path_absolute: pathlib.Path = self._page.path_absolute / path
        else:
            self._path_absolute: pathlib.Path = pathlib.Path(path)

        self._validate()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: page:{self._page} filename:{self._filename}>"
        )

    def _validate(self) -> None:

        # Validate text file exists.
        if not self._path_absolute.exists():
            raise errors.MissingContent(
                f"Missing '{self._filename}' in {self._path_absolute}."
            )

        # Validate if supported text type.
        if self._filetype not in config.VALID_TEXT_TYPES:
            raise errors.UnsupportedContentType(
                f"Unsupported text type '{self._filename}' in {self._path_absolute}."
            )

    @property
    def _filename(self) -> str:
        return self._path_absolute.name

    @property
    def _filetype(self) -> str:
        return self._path_absolute.suffix

    @property
    def path_absolute(self) -> pathlib.Path:
        return self._path_absolute

    @property
    def path_relative(self) -> pathlib.Path:
        """ Returns path relative to to /[site]. """
        return self._path_absolute.relative_to(config.path_site)

    @property
    def body(self) -> str:
        return markdown.from_file(filepath=self._path_absolute, page=self._page)


class Header:

    is_header: bool = True

    def __init__(self, page: "PageType", **content_data):
        """ Creates an Header object from a dictionary with the following
        attributes:

            {
                "type": "header",
                "body": [str: body],
                "size": [str: size], // See easel.site.config.VALID_SIZES
            }
        """

        self._page: "PageType" = page

        try:
            self._body: str = content_data["body"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'body' in {content_data} in {self._page.file_config}."
            ) from error

        self._size: str = content_data.get("size", config.DEFAULT_SIZE)

        self._validate()

    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self._page} body:{self.body[:32].strip()}>"

    def _validate(self) -> None:

        # Validate size.
        if self._size not in config.VALID_SIZES:
            raise errors.ConfigError(
                f"{self}: Unsupported size '{self._size}' for Header."
            )

    @property
    def body(self) -> str:
        return self._body

    @property
    def size(self) -> str:
        return self._size


class Break:

    is_break: bool = True

    def __init__(self, page: "PageType", **content_data):
        """ Creates an VideoEmbedded object from a dictionary with the following
        attributes:

            {
                "type": "break",
                "size": [str: size], // See easel.site.config.VALID_SIZES
            }
        """

        self._page: "PageType" = page
        self._size: str = content_data.get("size", config.DEFAULT_SIZE)

        self._validate()

    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self._page} size:{self._size}>"

    def _validate(self) -> None:

        # Validate size.
        if self._size not in config.VALID_SIZES:
            raise errors.ConfigError(
                f"{self}: Unsupported size '{self._size}' for Break."
            )

    @property
    def size(self) -> str:
        return self._size


content_factory = ContentFactory()
