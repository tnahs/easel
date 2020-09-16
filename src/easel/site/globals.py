import importlib
import json
import logging
import os
import pathlib
from typing import Any, Optional, Union

from . import errors
from .defaults import Defaults, Key
from .helpers import SafeDict, Utils


logger = logging.getLogger(__name__)


class _Globals:
    def __init__(self):

        self._site_paths = SitePaths(self)
        self._site_config = SiteConfig(self)
        self._theme_paths = ThemePaths(self)
        self._theme_config = ThemeConfig(self)

    def init(self, root: Optional[Union[pathlib.Path, str]]):

        # The site's root directory is first set.
        self.site_paths.root = root

        # Using the site's root directory, the 'site.yaml' is loaded and merged
        # with the default site config creating the final site config.
        self.site_config.load()

        # Using the 'theme' entry from the 'site.yaml', the theme's root
        # directory is determined.
        self.theme_paths.load()

        # Using the theme's root directory, the 'theme.yaml' is loaded and
        # merged with the 'theme' entry from the 'site.yaml' creating the final
        # theme config.
        self.theme_config.load()

    @property
    def site_paths(self) -> "SitePaths":
        return self._site_paths

    @property
    def site_config(self) -> "SiteConfig":
        return self._site_config

    @property
    def theme_paths(self) -> "ThemePaths":
        return self._theme_paths

    @property
    def theme_config(self) -> "ThemeConfig":
        return self._theme_config

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:

        if value is True:
            os.environ["FLASK_ENV"] = "development"

        self._debug = value


class GlobalsBase:
    def __init__(self, globals: "_Globals", /):
        self.__globals = globals

    @property
    def globals(self) -> "_Globals":
        return self.__globals


class SitePaths(GlobalsBase):

    _root: pathlib.Path

    @property
    def root(self) -> pathlib.Path:
        """ Returns /absolute/path/to/site-name """
        return self._root

    @root.setter
    def root(self, value: Optional[Union[pathlib.Path, str]]) -> None:  # type:ignore
        """ Sets /absolute/path/to/site-name """

        # Sets the current directory as the root if no root is provided.
        root = pathlib.Path(value) if value is not None else pathlib.Path()

        try:
            root = root.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                f"Site directory {root} does not exist."
            ) from error

        self._root = root

    @property
    def pages(self) -> pathlib.Path:
        """ Returns /absolute/path/to/site-name/pages """

        path_pages = (
            self.root / Defaults.DIRECTORY_NAME_CONTENTS / Defaults.DIRECTORY_NAME_PAGES
        )

        try:
            path_pages = path_pages.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                "Site directory missing 'pages' sub-directory."
            ) from error

        return path_pages

    @property
    def cache(self) -> pathlib.Path:
        """ Returns /absolute/path/to/site-name/site-cache """
        return self.root / Defaults.DIRECTORY_NAME_SITE_CACHE

    @property
    def static_url_path(self) -> str:
        """ Returns an absolute url: /site """
        return Utils.urlify("site")


class SiteConfig(GlobalsBase):

    __config: dict

    # fmt:off
    _config_default: dict = {
        Key.TITLE: None,
        Key.AUTHOR: None,
        Key.COPYRIGHT: None,
        Key.DESCRIPTION: None,
        Key.FAVICON: None,
        Key.MENU: [],
        Key.HEADER: {
            Key.TITLE: None,
            Key.IMAGE: {
                Key.PATH: None,
                Key.WIDTH: None,
                Key.HEIGHT: None,
            },
        },
        Key.THEME: {
            Key.NAME: None,
            Key.CUSTOM_PATH: None,
        },
    }
    # fmt:on
    _config_user: dict

    def load(self) -> None:

        # Load the 'site.yaml' from the site's root.
        self._config_user = Utils.load_config(
            path=self.globals.site_paths.root / Defaults.FILENAME_SITE_YAML
        )

        self._validate()

        # Merge the 'site.yaml' with the default config dictionary and set
        # the combined dictionary as the site's config.
        self.__config = Utils.update_dict(
            original=self._config_default, updates=self._config_user
        )

        # DEBUGGING
        # logger.debug(json.dumps(self.__config, indent=4))

    def _validate(self) -> None:

        menu: dict = self._config_user.get(Key.MENU, [])

        if type(menu) is not list:
            raise errors.SiteConfigError(
                f"Expected type 'list' for '{Key.MENU}' got '{type(menu).__name__}'."
            )

        header: dict = self._config_user.get(Key.HEADER, {})

        if type(header) is not dict:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Key.HEADER}' got '{type(header).__name__}'."
            )

        theme: dict = self._config_user.get(Key.THEME, {})

        if type(theme) is not dict:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Key.THEME}' got '{type(theme).__name__}'."
            )

    @property
    def title(self) -> Optional[str]:
        return self.__config[Key.TITLE]

    @property
    def author(self) -> Optional[str]:
        return self.__config[Key.AUTHOR]

    @property
    def copyright(self) -> Optional[str]:
        return self.__config[Key.COPYRIGHT]

    @property
    def description(self) -> Optional[str]:
        return self.__config[Key.DESCRIPTION]

    @property
    def favicon(self) -> Optional[str]:
        return self.__config[Key.FAVICON]

    @property
    def menu(self) -> list:
        return self.__config[Key.MENU]

    @property
    def header(self) -> dict:
        return self.__config[Key.HEADER]

    @property
    def theme(self) -> dict:
        return self.__config[Key.THEME]

    @property
    def theme_name(self) -> Optional[str]:
        return self.__config[Key.THEME][Key.NAME]

    @property
    def theme_custom_path(self) -> Optional[str]:
        return self.__config[Key.THEME][Key.CUSTOM_PATH]


class ThemePaths(GlobalsBase):

    _root: pathlib.Path

    def load(self) -> None:

        self._root = self._get_root_dispatcher()

    def _get_root_dispatcher(self) -> pathlib.Path:

        # Grab 'theme.name' and 'theme.custom-path' from the 'site.yaml'.
        name = self.globals.site_config.theme_name
        custom_path = self.globals.site_config.theme_custom_path

        if name is not None and custom_path is not None:
            logger.warning(
                "Setting both 'name' and 'custom-path' might result in unexpected behavior."
            )

        if custom_path is not None:
            return self._get_custom_root(path=custom_path)

        if name is None:
            return self._get_default_builtin_root()

        if name.startswith(Defaults.INSTALLED_THEME_NAME_PREFIX):
            return self._get_installed_root(name=name)

        return self._get_builtin_root(name=name)

    def _get_custom_root(self, path: str) -> pathlib.Path:

        root = self.globals.site_paths.root / path

        try:
            root = root.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(f"Custom theme {path} not found.") from error

        logger.info(f"Using custom theme from {path}.")

        return root

    def _get_default_builtin_root(self) -> pathlib.Path:

        logger.info(
            f"Using default built-in theme '{Defaults.DEFAULT_BUILTIN_THEME_NAME}'."
        )

        return (
            Defaults.APP_ROOT
            / Defaults.DIRECTORY_NAME_THEMES
            / Defaults.DEFAULT_BUILTIN_THEME_NAME
        )

    def _get_installed_root(self, name: str) -> pathlib.Path:

        # TODO:LOW It would be nice if this didn't need to happen.
        module_name = name.replace("-", "_")

        try:
            installed_theme = importlib.__import__(module_name)
        except ModuleNotFoundError as error:
            raise errors.SiteConfigError(
                f"Installed theme '{name}' not found."
            ) from error

        logger.info(f"Using installed theme '{name}'.")

        return pathlib.Path(installed_theme.__file__).parent

    def _get_builtin_root(self, name: str) -> pathlib.Path:

        if name not in Defaults.VALID_BUILTIN_THEME_NAMES:
            raise errors.SiteConfigError(
                f"Invalid theme name '{name}'. Available built-in themes are: "
                f"{Defaults.VALID_BUILTIN_THEME_NAMES}"
            )

        logger.info(f"Using built-in theme '{name}'.")

        return Defaults.APP_ROOT / Defaults.DIRECTORY_NAME_THEMES / name

    @property
    def root(self) -> pathlib.Path:
        """ Returns the root path to the current theme. """
        return self._root

    @property
    def static_url_path(self) -> str:
        """ Returns an absolute url: /theme """
        return Utils.urlify("theme")


class ThemeConfig(GlobalsBase):

    __config: dict

    _config_default: dict
    _config_user: dict

    def load(self) -> None:

        # Load the 'theme.yaml' from the theme root.
        self._config_default = Utils.load_config(
            path=self.globals.theme_paths.root / Defaults.FILENAME_THEME_YAML
        )

        # Grab the 'theme' entry from the 'site.yaml'.
        self._config_user = self.globals.site_config.theme

        self._validate()

        # Merge the 'theme' entry from the 'site.yaml' with the default
        # 'theme.yaml' and set the combined dictionary as the site's config.
        self.__config = Utils.update_dict(
            original=self._config_default, updates=self._config_user
        )

        # DEBUGGING
        # logger.debug(json.dumps(self.__config, indent=4))

    def _validate(self) -> None:
        pass

    def __getitem__(self, key: str) -> Any:
        try:
            return self.__config[key]
        except KeyError:
            logger.warning(
                f"{self.__class__.__name__} received a request for a missing "
                f"key '{key}'. Subsequent accesses have been suppressed."
            )

        return SafeDict()

    def __getattr__(self, key: str) -> Any:
        try:
            return self.__config[key]
        except KeyError:
            logger.warning(
                f"{self.__class__.__name__} received a request for a missing "
                f"key '{key}'. Subsequent accesses have been suppressed."
            )

        return SafeDict()


Globals = _Globals()
