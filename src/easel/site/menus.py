import logging
from typing import TYPE_CHECKING, Any, Optional, Type, Union

from . import errors
from .config import config
from .helpers import utils


if TYPE_CHECKING:
    from .site import Site


logger = logging.getLogger(__name__)


# See easel.site.contents
_MenuType = Union[
    Type["LinkPage"], Type["LinkURL"], Type["Section"], Type["Spacer"],
]

MenuType = Union[
    "LinkPage", "LinkURL", "Section", "Spacer",
]


class MenuFactory:
    def __init__(self):
        self._menu_types = {
            "link-page": LinkPage,
            "link-url": LinkURL,
            "section": Section,
            "spacer": Spacer,
        }

    def build(self, site: "Site", menu_data: dict) -> MenuType:
        """ Builds Menu-like object from a dictionary. See respective
        classes for documentation on accepted keys and structure. """

        try:
            menu_type: str = menu_data["type"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'type' in {menu_data} in {config.file_site_yaml}."
            ) from error

        # Get Menu class based on 'menu_type'.
        Menu: Optional[_MenuType] = self.menu_types(menu_type=menu_type)

        if Menu is None:
            raise errors.ConfigError(
                f"Unsupported value for 'type' '{menu_type}' in {config.file_site_yaml}."
            )

        return Menu(site=site, **menu_data)

    def menu_types(self, menu_type: str) -> Optional[_MenuType]:
        return self._menu_types.get(menu_type, None)

    def register_menu_type(self, name: str, menu: Any) -> None:
        """ Register new Menu-like object. """
        self._menu_types[name] = menu


class LinkPage:

    is_link_page: bool = True

    def __init__(self, site: "Site", **menu_data):
        """ Creates an Menu object from a dictionary with the following
            attributes:

            {
                "type": "link-page",
                "label": [str: label],
                "links-to": [str: path/to/page],
            }
        """

        self._site: "Site" = site

        try:
            self._label: str = menu_data["label"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'label' in {menu_data} in {config.file_site_yaml}."
            ) from error

        try:
            self._links_to: str = menu_data["links-to"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'links-to' in {menu_data} in {config.file_site_yaml}."
            ) from error

        self._validate()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: label:{self._label} links_to:{self._links_to}>"

    def _validate(self) -> None:

        for page in self._site.pages:
            if page.name == self._links_to:
                return None

        raise errors.ConfigError(
            f"Menu item '{self._label}' has no corresponding page. "
            f"Page '{self._links_to}' does not exist."
        )

    @property
    def label(self) -> str:
        return self._label

    @property
    def url(self) -> str:
        return utils.slugify(self._links_to)


class LinkURL:

    is_link_url: bool = True

    def __init__(self, site: "Site", **menu_data):
        """ Creates an Menu object from a dictionary with the following
            attributes:

            {
                "type": "link-url",
                "label": [str: label],
                "url": [str: url],
            }
        """

        self._site: "Site" = site

        try:
            self._label: str = menu_data["label"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'label' in {menu_data} in {config.file_site_yaml}."
            ) from error

        try:
            self._url: str = menu_data["url"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'url' in {menu_data} in {config.file_site_yaml}."
            ) from error

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: url:{self._url}>"

    @property
    def label(self) -> str:
        return self._label

    @property
    def url(self) -> str:
        return self._url


class Section:

    is_section: bool = True

    def __init__(self, site: "Site", **menu_data):
        """ Creates an Menu object from a dictionary with the following
            attributes:

            {
                "type": "section",
                "label": [str: label],
            }
        """

        self._site: "Site" = site

        try:
            self._label: str = menu_data["label"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'label' in {menu_data} in {config.file_site_yaml}."
            ) from error

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: label:{self._label}>"

    @property
    def label(self) -> str:
        return self._label


class Spacer:

    is_spacer: bool = True

    def __init__(self, site: "Site", **menu_data):
        """ Creates an Menu object from a dictionary with the following
            attributes:

            {
                "type": "spacer",
                "size": [str: size], // See easel.site.config.VALID_SIZES
            }
        """

        self._site: "Site" = site
        self._size: str = menu_data.get("size", config.DEFAULT_SIZE)

        self._validate()

    def _validate(self) -> None:

        # Validate size.
        if self._size not in config.VALID_SIZES:
            raise errors.ConfigError(f"{self}: Unsupported 'size' '{self._size}'.")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: size:{self._size}>"

    @property
    def size(self) -> str:
        return self._size


menu_factory = MenuFactory()
