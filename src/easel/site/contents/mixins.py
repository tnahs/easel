import abc
import logging
from typing import TYPE_CHECKING, Optional

from ..defaults import Defaults, Key
from ..errors import ContentConfigError
from ..markdown import markdown


if TYPE_CHECKING:
    from ..pages import PageObj


logger = logging.getLogger(__name__)


class CaptionMixin(abc.ABC):
    """Adds support for parsing and render captions from a dictionary with the
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
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def page(self) -> "PageObj":
        pass  # pragma: no cover

    @property
    def _caption_config(self) -> dict:
        return self.config.get(Key.CAPTION, {})

    def validate__caption_config(self) -> None:

        caption = self.config.get(Key.CAPTION, {})

        if type(caption) is not dict:
            raise ContentConfigError(
                f"{self.page}: Expected type 'dict' for "
                f"'{Key.CAPTION}' got '{type(caption).__name__}'."
            )

        caption_title = caption.get(Key.TITLE, "")

        if type(caption_title) is not str:
            raise ContentConfigError(
                f"{self.page}: Expected type 'str' for '{Key.CAPTION}.{Key.TITLE}' got "
                f"'{type(caption_title).__name__}'."
            )

        caption_description = caption.get(Key.DESCRIPTION, "")

        if type(caption_description) is not str:
            raise ContentConfigError(
                f"{self.page}: Expected type 'str' for '{Key.CAPTION}.{Key.DESCRIPTION}' got "
                f"'{type(caption_description).__name__}'."
            )

        if (
            self.caption_align is not None
            and self.caption_align not in Defaults.VALID_ALIGNMENTS
        ):
            raise ContentConfigError(
                f"{self.page}: Unsupported value '{self.caption_align}' for '{Key.ALIGN}'."
            )

    @property
    def caption_title(self) -> str:
        return markdown.from_string(self._caption_config.get(Key.TITLE, ""))

    @property
    def caption_description(self) -> str:
        return markdown.from_string(self._caption_config.get(Key.DESCRIPTION, ""))

    @property
    def caption_align(self) -> Optional[str]:
        return self._caption_config.get(Key.ALIGN, None)
