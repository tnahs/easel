import abc
import logging
from typing import TYPE_CHECKING, Any, Optional, Type, Union

from . import errors
from .config import config
from .helpers import Utils, Keys


if TYPE_CHECKING:
    from .site import Site


logger = logging.getLogger(__name__)


# See easel.site.contents
MenuClass = Union[
    Type["LinkPage"], Type["LinkURL"], Type["Section"], Type["Spacer"],
]

MenuObj = Union[
    "LinkPage", "LinkURL", "Section", "Spacer",
]


class _MenuFactory:
    def __init__(self):
        self._menu_types = {
            "link-page": LinkPage,
            "link-url": LinkURL,
            "section": Section,
            "spacer": Spacer,
        }

    def build(self, site: "Site", menu_data: dict) -> MenuObj:
        """ Builds Menu-like object from a dictionary. See respective classes
        for documentation on accepted keys and structure. """

        try:
            menu_type: str = menu_data[Keys.TYPE]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Keys.TYPE}' for Menu-like item in "
                f"{config.FILENAME_SITE_YAML}."
            ) from error

        # Get Menu class based on 'menu_type'.
        Menu: Optional[MenuClass] = self.menu_types(menu_type=menu_type)

        if Menu is None:
            raise errors.MenuConfigError(
                f"Unsupported value '{menu_type}' for '{Keys.TYPE}' for "
                f"Menu-like item in {config.FILENAME_SITE_YAML}."
            )

        return Menu(site=site, **menu_data)

    def menu_types(self, menu_type: str) -> Optional[MenuClass]:
        return self._menu_types.get(menu_type, None)

    def register_menu_type(self, name: str, menu: Any) -> None:
        """ Register new Menu-like object. """
        self._menu_types[name] = menu


class MenuInterface(abc.ABC):
    def __init__(self, site: "Site", **menu_data):

        self._site: "Site" = site
        self._menu_data = menu_data

        self.validate__config()

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass

    @property
    def menu_data(self) -> dict:
        return self._menu_data


class LinkPage(MenuInterface):
    """ Creates an Menu-like object from a dictionary with the following
        attributes:

        {
            "type": "link-page",
            "label": [str: label],
            "links-to": [str: path/to/page],
        }
    """

    is_link_page: bool = True

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}: label:{self.label} links_to:{self.links_to}>"
        )

    def validate__config(self) -> None:

        try:
            self.menu_data[Keys.LABEL]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Keys.LABEL}' "
                f"for {self.__class__.__name__} in {config.FILENAME_SITE_YAML}."
            ) from error

        try:
            self.menu_data[Keys.LINKS_TO]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Keys.LINKS_TO}' "
                f"for {self.__class__.__name__} in {config.FILENAME_SITE_YAML}."
            ) from error

        self._validate__links_to()

    def _validate__links_to(self) -> None:

        for page in self._site.pages:
            if page.name == self.links_to:
                return

        raise errors.MenuConfigError(
            f"Menu item '{self.label}' has no corresponding page. "
            f"Page '{self.links_to}' does not exist."
        )

    @property
    def label(self) -> str:
        return self.menu_data[Keys.LABEL]

    @property
    def links_to(self) -> str:
        return self.menu_data[Keys.LINKS_TO]

    @property
    def url(self) -> str:
        return Utils.slugify(self.links_to)


class LinkURL(MenuInterface):
    """ Creates an Menu-like object from a dictionary with the following
        attributes:

        {
            "type": "link-url",
            "label": [str: label],
            "url": [str: url],
        }
    """

    is_link_url: bool = True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: url:{self.url}>"

    def validate__config(self) -> None:

        try:
            self.menu_data[Keys.LABEL]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Keys.LABEL}' "
                f"for {self.__class__.__name__} in {config.FILENAME_SITE_YAML}."
            ) from error

        try:
            self.menu_data[Keys.URL]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Keys.URL}' "
                f"for {self.__class__.__name__} in {config.FILENAME_SITE_YAML}."
            ) from error

    @property
    def label(self) -> str:
        return self.menu_data[Keys.LABEL]

    @property
    def url(self) -> str:
        return self.menu_data[Keys.URL]


class Section(MenuInterface):
    """ Creates an Menu-like object from a dictionary with the following
        attributes:

        {
            "type": "section",
            "label": [str: label],
        }
    """

    is_section: bool = True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: label:{self.label}>"

    def validate__config(self) -> None:

        try:
            self.menu_data[Keys.LABEL]
        except KeyError as error:
            raise errors.MenuConfigError(
                f"Missing required key '{Keys.LABEL}' "
                f"for {self.__class__.__name__} in {config.FILENAME_SITE_YAML}."
            ) from error

    @property
    def label(self) -> str:
        return self.menu_data[Keys.LABEL]


class Spacer(MenuInterface):
    """ Creates an Menu-like object from a dictionary with the following
        attributes:

        {
            "type": "spacer",
            "size": [str: size], // See easel.site.config.VALID_SIZES
        }
    """

    is_spacer: bool = True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: size:{self.size}>"

    def validate__config(self) -> None:

        if self.size is not None and self.size not in config.VALID_SIZES:
            raise errors.MenuConfigError(
                f"Unsupported value '{self.size}' for {Keys.SIZE} for "
                f"{self.__class__.__name__} in {config.FILENAME_SITE_YAML}."
            )

    @property
    def size(self) -> str:
        return self.menu_data.get(Keys.SIZE, None)


menu_factory = _MenuFactory()
