import logging
from typing import TYPE_CHECKING, Any, Optional, Type, Union

from ..defaults import Defaults, Key
from ..errors import ContentConfigError
from .contents import Audio, Break, Embedded, Header, Image, TextBlock, Video


if TYPE_CHECKING:
    from ..pages import PageObj


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
    "Image",
    "Video",
    "Audio",
    "Embedded",
    "TextBlock",
    "Header",
    "Break",
]


class _ContentFactory:

    _content_types = {
        Key.IMAGE: Image,
        Key.VIDEO: Video,
        Key.AUDIO: Audio,
        Key.TEXT_BLOCK: TextBlock,
        Key.EMBEDDED: Embedded,
        Key.HEADER: Header,
        Key.BREAK: Break,
    }

    def build(self, page: "PageObj", config: dict) -> ContentObj:
        """Builds Content-like object from a dictionary. See respective
        classes for documentation on accepted keys and structure."""

        try:
            content_type: str = config[Key.TYPE]
        except KeyError as error:
            raise ContentConfigError(
                f"{page}: Missing required key '{Key.TYPE}' for Content-like "
                f"item in {Defaults.FILENAME_PAGE_YAML}."
            ) from error

        # Get Content class based on 'content_type'.
        Content: Optional["ContentClass"] = self.content_types(
            content_type=content_type
        )

        if Content is None:
            raise ContentConfigError(
                f"{page}: Unsupported value '{content_type}' for "
                f"'{Key.TYPE}' for Content-like item in {Defaults.FILENAME_PAGE_YAML}."
            )

        return Content(page=page, **config)

    def content_types(self, content_type: str) -> Optional["ContentClass"]:
        return self._content_types.get(content_type, None)

    def register_content_type(self, name: str, content: Any) -> None:
        """ Register new Content-like object. """
        self._content_types[name] = content


ContentFactory = _ContentFactory()
