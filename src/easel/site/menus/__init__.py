import logging
from typing import Any, Optional, Type, Union

from ..defaults import Defaults, Key
from ..errors import MenuConfigError
from .menus import LinkPage, LinkURL, Spacer


logger = logging.getLogger(__name__)


# See easel.site.contents
MenuClass = Union[
    Type["LinkPage"],
    Type["LinkURL"],
    Type["Spacer"],
]

MenuObj = Union[
    "LinkPage",
    "LinkURL",
    "Spacer",
]


class _MenuFactory:

    _types = {
        Key.LINK_PAGE: LinkPage,
        Key.LINK_URL: LinkURL,
        Key.SPACER: Spacer,
    }

    def build(self, config: dict) -> MenuObj:
        """Builds Menu-like object from a dictionary. See respective classes
        for documentation on accepted keys and structure."""

        try:
            menu_type: str = config[Key.TYPE]
        except KeyError as error:
            raise MenuConfigError(
                f"Missing required key '{Key.TYPE}' for Menu-like item in "
                f"{Defaults.FILENAME_SITE_YAML}."
            ) from error

        # Get Menu class based on 'menu_type'.
        Menu: Optional["MenuClass"] = self.get_type(name=menu_type)

        if Menu is None:
            raise MenuConfigError(
                f"Unsupported value '{menu_type}' for '{Key.TYPE}' for "
                f"Menu-like item in {Defaults.FILENAME_SITE_YAML}."
            )

        return Menu(**config)

    def get_type(self, name: str) -> Optional["MenuClass"]:
        return self._types.get(name, None)

    def register(self, name: str, obj: Any) -> None:
        """ Register new Menu-like object. """
        self._types[name] = obj


MenuFactory = _MenuFactory()
