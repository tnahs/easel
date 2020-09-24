import abc
import logging
from typing import Optional

from ..defaults import Defaults, Key
from ..errors import MenuConfigError
from ..helpers import Utils


logger = logging.getLogger(__name__)


class AbstractMenu(abc.ABC):
    def __init__(self, **config):

        self._config = config

        self.validate__config()

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def label(self) -> Optional[str]:
        pass  # pragma: no cover

    @property
    def config(self) -> dict:
        return self._config


class LinkPage(AbstractMenu):
    """Creates a LinkPage Menu object from a dictionary with the following
    attributes:

    {
        "type": "link-page",
        "label": [str: None],
        "links-to": [str: None],
    }
    """

    is_link_page: bool = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config[Key.LINKS_TO] = Utils.normalize_page_path(
            path=self.config[Key.LINKS_TO]
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}: label:{self.label} links_to:{self.links_to}>"
        )

    def validate__config(self) -> None:

        try:
            self.config[Key.LABEL]
        except KeyError as error:
            raise MenuConfigError(
                f"Missing required key '{Key.LABEL}' "
                f"for {self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            ) from error

        try:
            self.config[Key.LINKS_TO]
        except KeyError as error:
            raise MenuConfigError(
                f"Missing required key '{Key.LINKS_TO}' "
                f"for {self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            ) from error

    @property
    def label(self) -> str:
        return self.config[Key.LABEL]

    @property
    def links_to(self) -> str:
        return self.config[Key.LINKS_TO]

    @property
    def url(self) -> str:
        return Utils.urlify(self.links_to)


class LinkURL(AbstractMenu):
    """Creates an LinkURL Menu object from a dictionary with the following
    attributes:

    {
        "type": "link-url",
        "label": [str: None],
        "url": [str: None],
    }
    """

    is_link_url: bool = True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: url:{self.url}>"

    def validate__config(self) -> None:

        try:
            self.config[Key.LABEL]
        except KeyError as error:
            raise MenuConfigError(
                f"Missing required key '{Key.LABEL}' "
                f"for {self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            ) from error

        try:
            self.config[Key.URL]
        except KeyError as error:
            raise MenuConfigError(
                f"Missing required key '{Key.URL}' "
                f"for {self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            ) from error

    @property
    def label(self) -> str:
        return self.config[Key.LABEL]

    @property
    def url(self) -> str:
        return self.config[Key.URL]


class Spacer(AbstractMenu):
    """Creates an Spacer Menu object from a dictionary with the following
    attributes:

    {
        "type": "spacer",
        "label": [str?: None],
        "size": [str?: None]
    }
    """

    is_spacer: bool = True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: size:{self.size}>"

    def validate__config(self) -> None:

        if self.size is not None and self.size not in Defaults.VALID_SIZES:
            raise MenuConfigError(
                f"Unsupported value '{self.size}' for {Key.SIZE} for "
                f"{self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            )

    @property
    def label(self) -> Optional[str]:
        return self.config.get(Key.LABEL, None)

    @property
    def size(self) -> str:
        return self.config.get(Key.SIZE, None)
