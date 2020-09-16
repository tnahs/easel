import abc
import logging
import pathlib
from typing import TYPE_CHECKING, Any, Optional, Type, Union

from . import errors
from .defaults import Defaults, Key
from .globals import Globals
from .helpers import Utils
from .markdown import markdown
from .proxies import ProxyColorManager, ProxyImageManager


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
            Key.IMAGE: Image,
            Key.VIDEO: Video,
            Key.AUDIO: Audio,
            Key.TEXT_BLOCK: TextBlock,
            Key.EMBEDDED: Embedded,
            Key.HEADER: Header,
            Key.BREAK: Break,
        }

    def build(self, page: "PageObj", config: dict) -> ContentObj:
        """ Builds Content-like object from a dictionary. See respective
        classes for documentation on accepted keys and structure. """

        try:
            content_type: str = config[Key.TYPE]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{page}: Missing required key '{Key.TYPE}' for Content-like "
                f"item in {Defaults.FILENAME_PAGE_YAML}."
            ) from error

        # Get Content class based on 'content_type'.
        Content: Optional["ContentClass"] = self.content_types(
            content_type=content_type
        )

        if Content is None:
            raise errors.ContentConfigError(
                f"{page}: Unsupported value '{content_type}' for "
                f"'{Key.TYPE}' for Content-like item in {Defaults.FILENAME_PAGE_YAML}."
            )

        return Content(page=page, **config)

    def content_types(self, content_type: str) -> Optional["ContentClass"]:
        return self._content_types.get(content_type, None)

    def register_content_type(self, name: str, content: Any) -> None:
        """ Register new Content-like object. """
        self._content_types[name] = content


class CaptionMixin(abc.ABC):
    """ Adds support for parsing and render captions from a dictionary with the
    following attributes:

        {
            "caption": {
                "title": [str?: None],
                "description": [str?: None],
            },
        }
    """

    @property
    @abc.abstractmethod
    def config(self) -> dict:
        pass

    @property
    @abc.abstractmethod
    def page(self) -> "PageObj":
        pass

    @property
    def _caption_config(self) -> dict:
        return self.config.get(Key.CAPTION, {})

    @property
    def caption_title(self) -> str:
        return markdown.from_string(self._caption_config.get(Key.TITLE, ""))

    @property
    def caption_description(self) -> str:
        return markdown.from_string(self._caption_config.get(Key.DESCRIPTION, ""))

    @property
    def caption_align(self) -> Optional[str]:
        return self._caption_config.get(Key.ALIGN, None)

    def validate__caption_config(self) -> None:

        if type(self._caption_config) is not dict:
            raise errors.ContentConfigError(
                f"{self.page}: Expected type 'dict' for "
                f"'{Key.CAPTION}' got '{type(self._caption_config).__name__}'."
            )

        if (
            self.caption_align is not None
            and self.caption_align not in Defaults.VALID_ALIGNMENTS
        ):
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.caption_align}' for '{Key.ALIGN}'."
            )


class ContentInterface(abc.ABC):
    def __init__(self, page: "PageObj", **config):

        self._page = page
        self._config = config

        self.validate__config()

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass

    @property
    def config(self) -> dict:
        return self._config

    @property
    def page(self) -> "PageObj":
        return self._page


class FileContent(ContentInterface):
    """ Provides subclasses with file attributes for loading content from disk.
        Requires that the config dictionary contain with the following
        attributes:

        {
            "path": [str|pathlib.Path: None],
        }
    """

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: page:{self.page.directory_name} "
            f"filename:{self.filename}>"
        )

    def __str__(self):
        return f"{self.__class__.__name__}: {self.filename}"

    def validate__config(self) -> None:

        try:
            self.config[Key.PATH]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.PATH}' for "
                f"{self.__class__.__name__} in {Defaults.FILENAME_PAGE_YAML}."
            ) from error

        # TODO:LOW Check type of self.config[Key.PATH]

        if not self.path.exists():
            raise errors.MissingContent(f"Missing '{self.filename}' in {self.path}.")

    @property
    def name(self) -> str:
        """ Returns the filename without the extension. """
        return self.path.stem

    @property
    def filename(self) -> str:
        """ Returns the whole filename. """
        return self.path.name

    @property
    def extension(self) -> str:
        """ Returns the filename's extension. """
        return self.path.suffix

    @property
    def path(self) -> pathlib.Path:
        """ Returns an absolute path to the FileContent. """

        path = self.config[Key.PATH]

        # For Layout/LayoutGallery Pages, 'path' is passed as a string-type
        # containing a path to the file relative to the Page's root directory.
        if not isinstance(path, pathlib.Path):
            return self.page.path / path

        # For Lazy/LazyGallery Pages, 'path' is passed as a pathlib.Path object
        # containing an absolute path to the file.
        return path

    @property
    def src(self) -> pathlib.Path:
        """ Returns a path relative to to /site-name. """
        return self.path.relative_to(Globals.site_paths.root)

    @property
    def mimetype(self) -> str:
        return Utils.get_mimetype(extension=self.extension)


class Image(FileContent, CaptionMixin):
    """ Creates an Image Content object from a dictionary with the following
    attributes:

        {
            "type": "image",
            "path": [str|pathlib.Path: None],
        }
    """

    is_image: bool = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._proxy_images = ProxyImageManager(image=self)
        self._proxy_colors = ProxyColorManager(image=self)

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in Defaults.VALID_IMAGE_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path}."
            )

        self.validate__caption_config()

    @property
    def proxy_images(self) -> ProxyImageManager:
        return self._proxy_images

    @property
    def proxy_colors(self) -> ProxyColorManager:
        return self._proxy_colors


class Video(FileContent, CaptionMixin):
    """ Creates an Video Content object from a dictionary with the following
    attributes:

        {
            "type": "video",
            "path": [str|pathlib.Path: None],
        }
    """

    is_video: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in Defaults.VALID_VIDEO_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path}."
            )

        self.validate__caption_config()


class Audio(FileContent, CaptionMixin):
    """ Creates an Audio Content object from a dictionary with the following
    attributes:

        {
            "type": "audio",
            "path": [str|pathlib.Path: None],
        }
    """

    is_audio: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in Defaults.VALID_AUDIO_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path}."
            )

        self.validate__caption_config()


class TextBlock(FileContent):
    """ Creates an TextBlock Content object from a dictionary with the
    following attributes:

        {
            "type": "text-block",
            "path": [str|pathlib.Path: None],
            "align": [str: None],
        }
    """

    is_text_block: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in Defaults.VALID_TEXT_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path}."
            )

        if self.align is not None and self.align not in Defaults.VALID_ALIGNMENTS:
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.align}' for '{Key.ALIGN}'."
            )

    @property
    def body(self) -> str:
        return markdown.from_file(filepath=self.path)

    @property
    def align(self) -> dict:
        return self.config.get(Key.ALIGN, None)


class Embedded(ContentInterface, CaptionMixin):
    """ Creates an Embedded Content object from a dictionary with the following
    attributes:

        {
            "type": "embedded",
            "html": [str: None],
        }
    """

    is_embedded: bool = True

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: page:{self.page.directory_name} "
            f"html:{self.html[:32].strip()}...>"
        )

    def __str__(self):
        return f"{self.__class__.__name__}: {self.html[:32].strip()}..."

    def validate__config(self) -> None:
        super().validate__config()

        try:
            self.config[Key.HTML]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.HTML}' for "
                f"{self.__class__.__name__} in {Defaults.FILENAME_PAGE_YAML}."
            ) from error

        self.validate__caption_config()

    @property
    def html(self) -> str:
        return self.config[Key.HTML]


class Header(ContentInterface):
    """ Creates an Header Content object from a dictionary with the following
    attributes:

        {
            "type": "header",
            "text": [str: text],
            "size": [str?: None],
            "align": [str?: None],
        }
    """

    is_header: bool = True

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: page:{self.page.directory_name} "
            f"text:{self.text[:32].strip()}...>"
        )

    def __str__(self):
        return f"{self.__class__.__name__}: {self.text[:32].strip()}..."

    def validate__config(self) -> None:

        try:
            self.config[Key.TEXT]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.TEXT}' for "
                f"{self.__class__.__name__} in {Defaults.FILENAME_PAGE_YAML}."
            ) from error

        if self.size is not None and self.size not in Defaults.VALID_SIZES:
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.size}' for '{Key.SIZE}'."
            )

        if self.align is not None and self.align not in Defaults.VALID_ALIGNMENTS:
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.align}' for '{Key.ALIGN}'."
            )

    @property
    def text(self) -> str:
        return self.config[Key.TEXT]

    @property
    def size(self) -> str:
        return self.config.get(Key.SIZE, None)

    @property
    def align(self) -> dict:
        return self.config.get(Key.ALIGN, None)


class Break(ContentInterface):
    """ Creates an Break Content object from a dictionary with the following
    attributes:

        {
            "type": "break",
            "size": [str?: None],
        }
    """

    is_break: bool = True

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: page:{self.page.directory_name} "
            f"size:{self.size}>"
        )

    def validate__config(self) -> None:

        if self.size is not None and self.size not in Defaults.VALID_SIZES:
            raise errors.ContentConfigError(
                f"{self.page} Unsupported value '{self.size}' for '{Key.SIZE}'."
            )

    @property
    def size(self) -> str:
        return self.config.get(Key.SIZE, None)


content_factory = _ContentFactory()
