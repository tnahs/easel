import abc
import logging
import json
import pathlib
from typing import TYPE_CHECKING, Any, Optional, Type, Tuple, Union

import PIL.Image
import PIL.ImageFilter

from . import errors
from . import global_config
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

    def build(self, page: "PageObj", config: dict) -> ContentObj:
        """ Builds Content-like object from a dictionary. See respective
        classes for documentation on accepted keys and structure. """

        try:
            content_type: str = config[Key.TYPE]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{page}: Missing required key '{Key.TYPE}' for Content-like "
                f"item in {global_config.FILENAME_PAGE_YAML}."
            ) from error

        # Get Content class based on 'content_type'.
        Content: Optional[ContentClass] = self.content_types(content_type=content_type)

        if Content is None:
            raise errors.ContentConfigError(
                f"{page}: Unsupported value '{content_type}' for "
                f"'{Key.TYPE}' for Content-like item in {global_config.FILENAME_PAGE_YAML}."
            )

        return Content(page=page, **config)

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
            and self.caption_align not in global_config.VALID_ALIGNMENTS
        ):
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.caption_align}' for '{Key.ALIGN}'."
            )


class Placeholder:
    def __init__(self, image: "Image"):

        self._original_image = image

        self._color: Tuple[int, int, int]

        self.cache()

    def cache(self, force: bool = False) -> None:
        self._create_cache_directory()
        self._cache_or_load(force=force)

    def _create_cache_directory(self) -> None:
        self._cache_directory.mkdir(parents=True, exist_ok=True)

    def _cache_or_load(self, force: bool) -> None:

        if self._has_cache is False or force is True:
            self._cache()

        try:
            with open(self.path_absolute_color, "r") as f:
                self._color = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            logger.warning(
                f"Error reading '{self._original_image.name}' cache. Re-caching."
            )
            self._cache()

        if type(self._color) is not list:
            logger.warning(
                f"Invalid color data for '{self._original_image.filename}'. Re-caching."
            )
            self._cache()

    def _cache(self) -> None:
        """ PIL Exceptions Reference

        Image.open Exceptions:

            IOError
                If the file cannot be found, or the image cannot be opened and
                identified.

        https://pillow.readthedocs.io/en/5.1.x/reference/Image.html#PIL.Image.open
        """

        logger.debug(f"Caching color and image for '{self._original_image.filename}'.")

        with PIL.Image.open(self._original_image.path_absolute) as image:

            image = image.convert("RGB")

            self._save_image(image=image)
            self._save_color(image=image)

    def _save_image(self, image: PIL.Image.Image) -> None:
        """ Image.save Exceptions:

            KeyError
                If the output format could not be determined from the file
                name. Use the format option to solve this.

            IOError
                If the file could not be written. The file may have been
                created, and may contain partial data.

        https://pillow.readthedocs.io/en/5.1.x/reference/Image.html#PIL.Image.Image.save
        """

        image.thumbnail(global_config.PLACEHOLDER_SIZE)
        image.save(
            self.path_absolute_image,
            format=global_config.PLACEHOLDER_FORMAT,
            quality=global_config.PLACEHOLDER_QUALITY,
        )

    def _save_color(self, image: PIL.Image.Image) -> None:

        image = image.resize((1, 1))
        color = image.getpixel((0, 0))

        with open(self.path_absolute_color, "w") as f:
            json.dump(color, f)

        self._color = color  # type: ignore

    @property
    def _has_cache(self) -> bool:
        return self.path_absolute_image.exists() and self.path_absolute_color.exists()

    @property
    def _cache_directory(self) -> pathlib.Path:
        """ Returns an absolute path to the cache directory. Transforms the
        original image path to the cache path:

            /site/pages/page-name/image-name.jpg
            /site/.cache/page-name/image-name
        """
        return (
            global_config.path_site_cache
            / self._original_image.path_relative.parent
            / self._original_image.name
        )

    @property
    def path_absolute_image(self) -> pathlib.Path:
        """ Returns a absolute path to the cached image:

            /site/.cache/page-name/image-name/image.ext
        """
        return self._cache_directory / f"image{self._original_image.extension}"

    @property
    def path_relative_image(self) -> pathlib.Path:
        """ Returns a relative path to the cached image:

            .cache/page-name/image-name/image.ext
        """
        return self.path_absolute_image.relative_to(global_config.path_site)

    @property
    def path_absolute_color(self) -> pathlib.Path:
        """ Returns a absolute path to the cached image:

            /site/.cache/page-name/image-name/color.json
        """
        return self._cache_directory / "color.json"

    @property
    def color(self) -> list:
        """ Returns the color as a list. This is because this value is passed
        to HTML then Javascript. It's easier to parse a list in Javascript than
        a Tuple. """
        return list(self._color)


class ContentInterface(abc.ABC):
    def __init__(self, page: "PageObj", **config):

        self._page: "PageObj" = page
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
    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self.page.name} filename:{self.filename}>"

    def __str__(self):
        return f"{self.__class__.__name__}: {self.filename}"

    def validate__config(self) -> None:

        try:
            self.config[Key.PATH]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.PATH}' for "
                f"{self.__class__.__name__} in {global_config.FILENAME_PAGE_YAML}."
            ) from error

        # TODO: Check type of self.config[Key.PATH]

        if not self.path_absolute.exists():
            raise errors.MissingContent(
                f"Missing '{self.filename}' in {self.path_absolute}."
            )

    @property
    def name(self) -> str:
        """ Returns the filename without the extension. """
        return self.path_absolute.stem

    @property
    def filename(self) -> str:
        """ Returns the whole filename. """
        return self.path_absolute.name

    @property
    def extension(self) -> str:
        """ Returns the filename's extension. """
        return self.path_absolute.suffix

    @property
    def path_absolute(self) -> pathlib.Path:
        """ Returns an absolute path to the FileContent. """

        path = self.config[Key.PATH]

        # For Layout/LayoutGallery Pages, 'path' is passed as a string-type
        # containing a path to the file relative to the Page's root directory.
        if not isinstance(path, pathlib.Path):
            return self.page.path_absolute / path

        # For Lazy/LazyGallery Pages, 'path' is passed as a pathlib.Path object
        # containing an absolute path to the file.
        return path

    @property
    def path_relative(self) -> pathlib.Path:
        """ Returns a path relative to to /[site]. """
        return self.path_absolute.relative_to(global_config.path_site)

    @property
    def mimetype(self) -> str:
        return Utils.get_mimetype(extension=self.extension)


class Image(FileContent, CaptionMixin):
    """ Creates an Image object from a dictionary with the following
    attributes:

        {
            "type": "image",
            "path": [str|pathlib.Path: path/to/image],
        }
    """

    is_image: bool = True

    _placeholder: Optional[Placeholder] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # QUESTION: Is there a better way to do this?
        # if getattr(self.page, "is_gallery", False):
        self._placeholder = Placeholder(image=self)

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in global_config.VALID_IMAGE_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path_absolute}."
            )

        self.validate__caption_config()

    @property
    def placeholder(self) -> Optional[Placeholder]:
        return self._placeholder


class Video(FileContent, CaptionMixin):
    """ Creates an Video object from a dictionary with the following
    attributes:

        {
            "type": "video",
            "path": [str|pathlib.Path: path/to/video],
        }
    """

    is_video: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in global_config.VALID_VIDEO_EXTENSIONS:
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
            "path": [str|pathlib.Path: path/to/audio],
        }
    """

    is_audio: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in global_config.VALID_AUDIO_EXTENSIONS:
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
            "path": [str|pathlib.Path: path/to/text-block],
            "align": [str: align], // See easel.site.config.GlobalConfig.VALID_ALIGNMENTS
        }
    """

    is_text_block: bool = True

    def validate__config(self) -> None:
        super().validate__config()

        if self.extension not in global_config.VALID_TEXT_EXTENSIONS:
            raise errors.UnsupportedContentType(
                f"{self}: Unsupported {self.__class__.__name__} type "
                f"'{self.filename}' in {self.path_absolute}."
            )

        if self.align is not None and self.align not in global_config.VALID_ALIGNMENTS:
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.align}' for '{Key.ALIGN}'."
            )

    @property
    def body(self) -> str:
        return markdown.from_file(filepath=self.path_absolute, page=self.page)

    @property
    def align(self) -> dict:
        return self.config.get(Key.ALIGN, None)


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
        return f"<{self.__class__.__name__}: page:{self.page.name} html:{self.html[:32].strip()}...>"

    def __str__(self):
        return f"{self.__class__.__name__}: {self.html[:32].strip()}..."

    def validate__config(self) -> None:
        super().validate__config()

        try:
            self.config[Key.HTML]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.HTML}' for "
                f"{self.__class__.__name__} in {global_config.FILENAME_PAGE_YAML}."
            ) from error

        self.validate__caption_config()

    @property
    def html(self) -> str:
        return self.config[Key.HTML]


class Header(ContentInterface):
    """ Creates an Header object from a dictionary with the following
    attributes:

        {
            "type": "header",
            "text": [str: text],
            "size": [str: size], // See easel.site.config.GlobalConfig.VALID_SIZES
            "align": [str: align], // See easel.site.config.GlobalConfig.VALID_ALIGNMENTS
        }
    """

    is_header: bool = True

    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self.page.name} text:{self.text[:32].strip()}...>"

    def __str__(self):
        return f"{self.__class__.__name__}: {self.text[:32].strip()}..."

    def validate__config(self) -> None:

        try:
            self.config[Key.TEXT]
        except KeyError as error:
            raise errors.ContentConfigError(
                f"{self.page}: Missing required key '{Key.TEXT}' for "
                f"{self.__class__.__name__} in {global_config.FILENAME_PAGE_YAML}."
            ) from error

        if self.size is not None and self.size not in global_config.VALID_SIZES:
            raise errors.ContentConfigError(
                f"{self.page}: Unsupported value '{self.size}' for '{Key.SIZE}'."
            )

        if self.align is not None and self.align not in global_config.VALID_ALIGNMENTS:
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
    """ Creates an Break object from a dictionary with the following
    attributes:

        {
            "type": "break",
            "size": [str: size], // See easel.site.config.GlobalConfig.VALID_SIZES
        }
    """

    is_break: bool = True

    def __repr__(self):
        return f"<{self.__class__.__name__}: page:{self.page.name} size:{self.size}>"

    def validate__config(self) -> None:

        if self.size is not None and self.size not in global_config.VALID_SIZES:
            raise errors.ContentConfigError(
                f"{self.page} Unsupported value '{self.size}' for '{Key.SIZE}'."
            )

    @property
    def size(self) -> str:
        return self.config.get(Key.SIZE, None)


content_factory = _ContentFactory()
