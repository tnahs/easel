import abc
import logging
import pathlib
from typing import TYPE_CHECKING, Any, Optional, Type, Union

from . import errors, pages
from .config import config
from .helpers import Key, markdown, Utils


if TYPE_CHECKING:
    from .pages import PageObj


logger = logging.getLogger(__name__)


""" Ah, it looks like you are trying to instantiate a type, so your dict should
be typed Dict[int, Type[Message]] not Dict[int, Message]. This will cause mypy
to complain too many arguments are passed, which is correct I believe, since
the base Message doesn't have any dataclass attributes, and uses __slots__.

https://github.com/python/mypy/issues/5361#issuecomment-405113523 """
ContentClass = Union[
    Type["Image"],
    Type["Video"],
    Type["Audio"],
    Type["TextBlock"],
    Type["Embedded"],
    Type["Header"],
    Type["Break"],
]

ContentObj = Union[
    "Image", "Video", "Audio", "Embedded", "TextBlock", "Header", "Break",
]


class _ContentFactory:
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

    def build(self, page: "PageObj", content_data: dict) -> ContentObj:
        """ Builds Content-like object from a dictionary. See respective
        classes for documentation on accepted keys and structure. """

        try:
            content_type: str = content_data[Key.TYPE]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{page}: Missing required key '{Key.TYPE}' for Content-like "
                f"item in {config.FILENAME_PAGE_YAML}."
            ) from error

        # Get Content class based on 'content_type'.
        Content: Optional[ContentClass] = self.content_types(content_type=content_type)

        if Content is None:
            raise errors.ContentConfigError(
                f"{page}: Unsupported value '{content_type}' for "
                f"'{Key.TYPE}' for Content-like item in {config.FILENAME_PAGE_YAML}."
            )

        return Content(page=page, **content_data)

    def content_types(self, content_type: str) -> Optional[ContentClass]:
        return self._content_types.get(content_type, None)

    def register_content_type(self, name: str, content: Any) -> None:
        """ Register new Content-like object. """
        self._content_types[name] = content


class CaptionMixin(abc.ABC):
    """ Adds support for parsing and render captions from a dictionary with the
    following attributes:

        {
            "caption": {
                "title": [str: title],
                "description": [str: description],
            },
        }
    """

    @property
    @abc.abstractmethod
    def content_data(self) -> dict:
        pass

    @property
    @abc.abstractmethod
    def page(self) -> "PageObj":
        pass

    @property
    def caption(self) -> dict:
        return self.content_data.get(Key.CAPTION, {})

    @property
    def caption_title(self) -> str:
        return markdown.from_string(self.caption.get(Key.TITLE, ""))

    @property
    def caption_description(self) -> str:
        return markdown.from_string(self.caption.get(Key.DESCRIPTION, ""))

    @property
    def caption_align(self) -> dict:
        return self.caption.get(Key.ALIGN, None)

    def validate__caption_config(self) -> None:

        if type(self.caption) is not dict:
            raise errors.ContentConfigError(
                f"{self.page}: Expected type 'dict' for "
                f"'{Key.CAPTION}' got '{type(self.caption).__name__}'."
            )

        if (
            self.caption_align is not None
            and self.caption_align not in config.VALID_ALIGNMENTS
        ):
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.caption_align}' for '{Key.ALIGN}'."
            )


class ContentInterface(abc.ABC):
    def __init__(self, page: "PageObj", **content_data):

        self._page: "PageObj" = page
        self._content_data = content_data

        self.validate__config()

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass

    @property
    def content_data(self) -> dict:
        return self._content_data

    @property
    def page(self) -> "PageObj":
        return self._page


class FileContent(ContentInterface):
    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self.page.name} filename:{self.filename}>"

    def validate__config(self) -> None:

        try:
            self.content_data[Key.PATH]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.PATH}' for "
                f"{self.__class__.__name__} in {config.FILENAME_PAGE_YAML}."
            ) from error

        if not self.path_absolute.exists():
            raise errors.MissingContent(
                f"Missing '{self.filename}' in {self.path_absolute}."
            )

    @property
    def filename(self) -> str:
        return self.path_absolute.name

    @property
    def extension(self) -> str:
        return self.path_absolute.suffix

    @property
    def path_absolute(self) -> pathlib.Path:

        path = self.content_data[Key.PATH]

        # For Layout pages, 'path' is passed as a path relative to the page
        # directory. In this case, concatenate both paths.
        if isinstance(self.page, pages.Layout):
            return self.page.path_absolute / path

        return pathlib.Path(path)

    @property
    def path_relative(self) -> pathlib.Path:
        """ Returns a path relative to to /[site]. """
        return self.path_absolute.relative_to(config.path_site)

    @property
    def mimetype(self) -> str:
        return Utils.get_mimetype(extension=self.extension)


class Image(FileContent, CaptionMixin):
    """ Creates an Image object from a dictionary with the following
    attributes:

        {
            "type": "image",
            "path": [str: path/to/image],
        }
    """

    is_image: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in config.VALID_IMAGE_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path_absolute}."
            )

        self.validate__caption_config()


class Video(FileContent, CaptionMixin):
    """ Creates an Video object from a dictionary with the following
    attributes:

        {
            "type": "video",
            "path": [str: path/to/video],
        }
    """

    is_video: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in config.VALID_VIDEO_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path_absolute}."
            )

        self.validate__caption_config()


class Audio(FileContent, CaptionMixin):
    """ Creates an Audio object from a dictionary with the following
    attributes:

        {
            "type": "audio",
            "path": [str: path/to/audio],
        }
    """

    is_audio: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in config.VALID_AUDIO_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path_absolute}."
            )

        self.validate__caption_config()


class TextBlock(FileContent):
    """ Creates an TextBlock object from a dictionary with the following
    attributes:

        {
            "type": "text-block",
            "path": [str: path/to/text-block],
        }
    """

    is_text_block: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in config.VALID_TEXT_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path_absolute}."
            )

        if self.align is not None and self.align not in config.VALID_ALIGNMENTS:
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.align}' for '{Key.ALIGN}'."
            )

    @property
    def body(self) -> str:
        return markdown.from_file(filepath=self.path_absolute, page=self.page)

    @property
    def align(self) -> dict:
        return self.content_data.get(Key.ALIGN, None)


class Embedded(ContentInterface, CaptionMixin):
    """ Creates an Embedded object from a dictionary with the following
    attributes:

        {
            "type": "embedded",
            "html": [str: html],
        }
    """

    is_embedded: bool = True

    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self.page.name} html:{self.html[:32].strip()}>"

    def validate__config(self) -> None:
        super().validate__config()

        try:
            self.content_data[Key.HTML]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.HTML}' for "
                f"{self.__class__.__name__} in {config.FILENAME_PAGE_YAML}."
            ) from error

        self.validate__caption_config()

    @property
    def html(self) -> str:
        return self.content_data[Key.HTML]


class Header(ContentInterface):
    """ Creates an Header object from a dictionary with the following
    attributes:

        {
            "type": "header",
            "text": [str: text],
            "size": [str: size], // See easel.site.config.VALID_SIZES
        }
    """

    is_header: bool = True

    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self.page.name} text:{self.text[:32].strip()}>"

    def validate__config(self) -> None:

        try:
            self.content_data[Key.TEXT]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.TEXT}' for "
                f"{self.__class__.__name__} in {config.FILENAME_PAGE_YAML}."
            ) from error

        if self.size is not None and self.size not in config.VALID_SIZES:
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.size}' for '{Key.SIZE}'."
            )

        if self.align is not None and self.align not in config.VALID_ALIGNMENTS:
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.align}' for '{Key.ALIGN}'."
            )

    @property
    def text(self) -> str:
        return self.content_data[Key.TEXT]

    @property
    def size(self) -> str:
        return self.content_data.get(Key.SIZE, None)

    @property
    def align(self) -> dict:
        return self.content_data.get(Key.ALIGN, None)


class Break(ContentInterface):
    """ Creates an Break object from a dictionary with the following
    attributes:

        {
            "type": "break",
            "size": [str: size], // See easel.site.config.VALID_SIZES
        }
    """

    is_break: bool = True

    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self.page.name} size:{self.size}>"

    def validate__config(self) -> None:

        if self.size is not None and self.size not in config.VALID_SIZES:
            raise errors.ContentConfigError(
                f"{self.page} Unsupported value '{self.size}' for '{Key.SIZE}'."
            )

    @property
    def size(self) -> str:
        return self.content_data.get(Key.SIZE, None)


content_factory = _ContentFactory()
