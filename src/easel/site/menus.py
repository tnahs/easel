import abc
import logging
from typing import TYPE_CHECKING, Any, Optional, Type, Union

from . import errors
from .defaults import Defaults, Key
from .helpers import Utils


if TYPE_CHECKING:
    from . import Site


logger = logging.getLogger(__name__)


# See easel.site.contents
MenuClass = Union[
    Type["LinkPage"], Type["LinkURL"], Type["Spacer"],
]

MenuObj = Union[
    "LinkPage", "LinkURL", "Spacer",
]


class _MenuFactory:
    def __init__(self):
        self._menu_types = {
            Key.LINK_PAGE: LinkPage,
            Key.LINK_URL: LinkURL,
            Key.SPACER: Spacer,
        }

    def build(self, site: "Site", config: dict) -> MenuObj:
        """ Builds Menu-like object from a dictionary. See respective classes
        for documentation on accepted keys and structure. """

        try:
            menu_type: str = config[Key.TYPE]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Key.TYPE}' for Menu-like item in "
                f"{Defaults.FILENAME_SITE_YAML}."
            ) from error

        # Get Menu class based on 'menu_type'.
        Menu: Optional["MenuClass"] = self.menu_types(menu_type=menu_type)

        if Menu is None:
            raise errors.MenuConfigError(
                f"Unsupported value '{menu_type}' for '{Key.TYPE}' for "
                f"Menu-like item in {Defaults.FILENAME_SITE_YAML}."
            )

        return Menu(site=site, **config)

    def menu_types(self, menu_type: str) -> Optional["MenuClass"]:
        return self._menu_types.get(menu_type, None)

    def register_menu_type(self, name: str, menu: Any) -> None:
        """ Register new Menu-like object. """
        self._menu_types[name] = menu


class MenuInterface(abc.ABC):
    def __init__(self, site: "Site", **config):

        self._site = site
        self._config = config

        self.validate__config()

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass

    @property
    def config(self) -> dict:
        return self._config

    @abc.abstractmethod
    def label(self) -> Optional[str]:
        pass


class LinkPage(MenuInterface):
    """ Creates a LinkPage Menu object from a dictionary with the following
        attributes:

        {
            "type": "link-page",
            "label": [str: None],
            "links-to": [str: None],
        }
    """

    is_link_page: bool = True

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}: label:{self.label} links_to:{self.links_to}>"
        )

    def validate__config(self) -> None:

        try:
            self.config[Key.LABEL]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Key.LABEL}' "
                f"for {self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            ) from error

        try:
            links_to = self.config[Key.LINKS_TO]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Key.LINKS_TO}' "
                f"for {self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            ) from error

        self.config[Key.LINKS_TO] = Utils.normalize_page_path(path=links_to)

        self._validate__links_to()

    def _validate__links_to(self) -> None:

        for page in self._site.pages:
            if page.url == self.url:
                return

        raise errors.MenuConfigError(
            f"Menu item '{self.label}' has no corresponding page. "
            f"Page '{self.links_to}' does not exist."
        )

    @property
    def label(self) -> str:
        return self.config[Key.LABEL]

    @property
    def links_to(self) -> str:
        return self.config[Key.LINKS_TO]

    @property
    def url(self) -> str:
        return Utils.urlify(self.links_to)


class LinkURL(MenuInterface):
    """ Creates an LinkURL Menu object from a dictionary with the following
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
            raise errors.MenuConfigError(
                f"Missing required key '{Key.LABEL}' "
                f"for {self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            ) from error

        try:
            self.config[Key.URL]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Key.URL}' "
                f"for {self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            ) from error

    @property
    def label(self) -> str:
        return self.config[Key.LABEL]

    @property
    def url(self) -> str:
        return self.config[Key.URL]


class Spacer(MenuInterface):
    """ Creates an Spacer Menu object from a dictionary with the following
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
            raise errors.MenuConfigError(
                f"Unsupported value '{self.size}' for {Key.SIZE} for "
                f"{self.__class__.__name__} in {Defaults.FILENAME_SITE_YAML}."
            )

    @property
    def label(self) -> Optional[str]:
        return self.config.get(Key.LABEL, None)

    @property
    def size(self) -> str:
        return self.config.get(Key.SIZE, None)


menu_factory = _MenuFactory()
