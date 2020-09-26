import abc
import logging
import pathlib
from typing import TYPE_CHECKING, Optional, Union

from ..defaults import Defaults, Key
from ..errors import ContentConfigError, MissingFile, UnsupportedContentType
from ..globals import Globals
from ..helpers import Utils
from ..markdown import markdown
from .mixins import CaptionMixin
from .proxies import ProxyColorManager, ProxyImageManager


if TYPE_CHECKING:
    from ..pages import PageObj
    from ..pages.pages import AbstractPage


logger = logging.getLogger(__name__)


class AbstractContent(abc.ABC):
    def __init__(self, page: Union["AbstractPage", "PageObj"], **config):

        self._page = page
        self._config = config

        self.validate__config()

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass  # pragma: no cover

    @property
    def config(self) -> dict:
        return self._config

    @property
    def page(self) -> Union["AbstractPage", "PageObj"]:
        return self._page


class File(AbstractContent):
    """Provides subclasses with file attributes for loading content from disk.
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

    def validate__config(self) -> None:

        try:
            path = self.config[Key.PATH]
        except KeyError as error:
            raise ContentConfigError(
                f"{self.page}: Missing required key '{Key.PATH}' for "
                f"{self.__class__.__name__} in {Defaults.FILENAME_PAGE_YAML}."
            ) from error

        if type(path) is not str and not isinstance(path, pathlib.Path):
            raise ContentConfigError(
                f"{self.page}: Expected type 'str' or 'pathlib.Path' for "
                f"'{Key.PATH}' got '{type(path).__name__}'."
            )

        if not path:
            raise ContentConfigError(
                f"{self.page}: Required key '{Key.PATH}' for "
                f"{self.__class__.__name__} cannot be blank."
            )

        if not self.path.exists():
            raise MissingFile(f"Missing '{self.filename}' in {self.path}.")

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
        """ Returns an absolute path to the File. """

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
    def mimetype(self) -> Optional[str]:
        return Utils.get_mimetype(extension=self.extension)


class Image(File, CaptionMixin):
    """Creates an Image Content object from a dictionary with the following
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
            raise UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path}."
            )

        self.validate__caption_config()

    @property
    def proxy_images(self) -> "ProxyImageManager":
        return self._proxy_images

    @property
    def proxy_colors(self) -> "ProxyColorManager":
        return self._proxy_colors


class Video(File, CaptionMixin):
    """Creates an Video Content object from a dictionary with the following
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
            raise UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path}."
            )

        self.validate__caption_config()


class Audio(File, CaptionMixin):
    """Creates an Audio Content object from a dictionary with the following
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
            raise UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path}."
            )

        self.validate__caption_config()


class TextBlock(File):
    """Creates an TextBlock Content object from a dictionary with the
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
            raise UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path}."
            )

        if self.align is not None and self.align not in Defaults.VALID_ALIGNMENTS:
            raise ContentConfigError(
                f"{self.page}: Unsupported value '{self.align}' for '{Key.ALIGN}'."
            )

    @property
    def body(self) -> str:
        return markdown.from_file(filepath=self.path)

    @property
    def align(self) -> dict:
        return self.config.get(Key.ALIGN, None)


class Embedded(AbstractContent, CaptionMixin):
    """Creates an Embedded Content object from a dictionary with the following
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

    def validate__config(self) -> None:
        super().validate__config()

        try:
            html = self.config[Key.HTML]
        except KeyError as error:
            raise ContentConfigError(
                f"{self.page}: Missing required key '{Key.HTML}' for "
                f"{self.__class__.__name__} in {Defaults.FILENAME_PAGE_YAML}."
            ) from error

        if type(html) is not str:
            raise ContentConfigError(
                f"{self.page}: Expected type 'str' or for '{Key.HTML}' got "
                f"'{type(html).__name__}'."
            )

        self.validate__caption_config()

    @property
    def html(self) -> str:
        return self.config[Key.HTML]


class Header(AbstractContent):
    """Creates an Header Content object from a dictionary with the following
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

    def validate__config(self) -> None:

        try:
            text = self.config[Key.TEXT]
        except KeyError as error:
            raise ContentConfigError(
                f"{self.page}: Missing required key '{Key.TEXT}' for "
                f"{self.__class__.__name__} in {Defaults.FILENAME_PAGE_YAML}."
            ) from error

        if type(text) is not str:
            raise ContentConfigError(
                f"{self.page}: Expected type 'str' or for '{Key.TEXT}' got "
                f"'{type(text).__name__}'."
            )

        if self.size is not None and self.size not in Defaults.VALID_SIZES:
            raise ContentConfigError(
                f"{self.page}: Unsupported value '{self.size}' for '{Key.SIZE}'."
            )

        if self.align is not None and self.align not in Defaults.VALID_ALIGNMENTS:
            raise ContentConfigError(
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


class Break(AbstractContent):
    """Creates an Break Content object from a dictionary with the following
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
            raise ContentConfigError(
                f"{self.page} Unsupported value '{self.size}' for '{Key.SIZE}'."
            )

    @property
    def size(self) -> str:
        return self.config.get(Key.SIZE, None)
