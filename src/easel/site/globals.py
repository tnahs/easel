import os
import pathlib
from typing import Optional, Union

from . import errors
from .defaults import Key, SiteDefaults
from .helpers import Utils


class SiteGlobals:
    def __init__(self):

        self._paths = SitePaths(self)
        self._theme = SiteTheme(self)
        self._config = SiteConfig(self)

    @property
    def paths(self) -> "SitePaths":
        return self._paths

    @property
    def theme(self) -> "SiteTheme":
        return self._theme

    @property
    def config(self) -> "SiteConfig":
        return self._config


class SitePaths:
    _root: Optional[pathlib.Path] = None

    def __init__(self, root: "SiteGlobals"):

        self.__global = root

        path = os.environ.get(Key.SITE_ROOT, None)

        if path is not None:
            self.root = path

    @property
    def root(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site] """

        if self._root is None:
            raise errors.SiteConfigError("Site directory must be set before running.")

        return self._root

    @root.setter
    def root(self, value: Union[pathlib.Path, str]) -> None:
        """ Sets /absolute/path/to/[site] """

        path = pathlib.Path(value)

        try:
            path = path.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                f"Site directory {path} does not exist."
            ) from error

        self._root = path

    @property
    def pages(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/pages """

        path_pages = self.root / SiteDefaults.DIRECTORY_NAME_PAGES

        try:
            path_pages = path_pages.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                "Site directory missing 'pages' sub-directory."
            ) from error

        return path_pages

    @property
    def cache(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/.cache """
        return self.root / SiteDefaults.DIRECTORY_NAME_CACHE


class SiteConfig:
    def __init__(self, root: "SiteGlobals"):

        self.__global = root

    def load(self) -> None:

        self._data = Utils.load_config(
            path=self.__global.paths.root / SiteDefaults.FILENAME_SITE_YAML
        )

        self._validate()

    def _validate(self) -> None:

        menu: dict = self._data.get(Key.MENU, [])

        if type(menu) is not list:
            raise errors.SiteConfigError(
                f"Expected type 'list' for '{Key.MENU}' got '{type(menu).__name__}'."
            )

        header: dict = self._data.get(Key.HEADER, {})

        if type(header) is not dict:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Key.HEADER}' got '{type(header).__name__}'."
            )

        theme: dict = self._data.get(Key.THEME, {})

        if type(theme) is not dict:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Key.THEME}' got '{type(theme).__name__}'."
            )

    @property
    def title(self) -> str:
        return self._data.get(Key.TITLE, "")

    @property
    def author(self) -> str:
        return self._data.get(Key.AUTHOR, "")

    @property
    def copyright(self) -> str:
        return self._data.get(Key.COPYRIGHT, "")

    @property
    def description(self) -> str:
        return self._data.get(Key.DESCRIPTION, "")

    @property
    def favicon(self) -> str:
        return self._data.get(Key.FAVICON, "")

    @property
    def menu(self) -> list:
        return self._data.get(Key.MENU, [])

    @property
    def header(self) -> dict:
        # TODO:LOW Re-implement SiteConfig.header after it's clearer how missing
        # keys and values will handled. We're trying to avoid forcing the user
        # to declare blank key-value pairs as well as avoid having to traverse
        # dictionaries to provide fallback default values.
        return self._data.get(Key.HEADER, {})

    @property
    def theme(self) -> dict:
        # TODO:LOW Re-implement SiteConfig.theme after it's clearer how themes
        # will be configured.
        return self._data.get(Key.THEME, {})


class SiteTheme:

    _root: Optional[pathlib.Path] = None
    _name: Optional[str] = None

    def __init__(self, root: "SiteGlobals"):

        self.__global = root

    @property
    def root(self) -> pathlib.Path:
        """ Returns the path to the current theme. """

        if self._root is None:
            return (
                SiteDefaults.APP_ROOT / SiteDefaults.DIRECTORY_NAME_THEMES / self.name
            )

        return self._root

    @root.setter
    def root(self, value: Optional[Union[pathlib.Path, str]]) -> None:
        """ Sets the theme path to a location outside of the application.

        NOTE:THEME Currently this only supports a custom theme that is local to
        the user. However future implementations will allow user-created themes
        to be shared and installed."""

        if not value:
            return

        path_theme = pathlib.Path(value)

        try:
            path_theme = path_theme.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                f"Theme directory {value} not found."
            ) from error

        self._root = path_theme

    @property
    def static(self) -> pathlib.Path:
        """ Returns the path to the current theme's static directory. """
        return self.root / SiteDefaults.DIRECTORY_NAME_STATIC

    @property
    def templates(self) -> pathlib.Path:
        """ Returns the path to the current theme's templates directory. """
        return self.root / SiteDefaults.DIRECTORY_NAME_TEMPLATES

    @property
    def name(self) -> str:
        """ Returns the name of the current theme. This method is accessed only
        if a path to a custom theme is not set. """

        if self._name is None:
            return SiteDefaults.DEFAULT_THEME_NAME

        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        """ Changes the current theme name. """

        if not value:
            return

        if value not in SiteDefaults.VALID_THEME_NAMES:

            # NOTE:THEME This is where we'd attempt to load an installed theme.

            raise errors.SiteConfigError(
                f"Invalid theme name '{value}'. Available themes are: "
                f"{SiteDefaults.VALID_THEME_NAMES}"
            )

        self._name = value


site_globals = SiteGlobals()
