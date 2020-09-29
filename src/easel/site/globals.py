import glob
import importlib
import importlib.util
import json
import logging
import os
import pathlib
from typing import Any, Generator, List, Optional, Union

from .defaults import Defaults, Key
from .errors import SiteConfigError, ThemeConfigError
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
        self.site_paths.load(root=root)

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
        self._debug = value

    @property
    def testing(self) -> bool:
        return self._testing

    @testing.setter
    def testing(self, value: bool) -> None:
        self._testing = value


class GlobalsBase:
    def __init__(self, globals: "_Globals", /):
        self.__globals = globals

    @property
    def globals(self) -> "_Globals":
        return self.__globals


class SitePaths(GlobalsBase):

    _root: Optional[pathlib.Path] = None

    def load(self, root: Optional[Union[pathlib.Path, str]]) -> None:

        # Sets the current directory as the root if no root is provided.
        path = pathlib.Path(root) if root is not None else pathlib.Path()
        self.root = path.resolve()

        self._validate()

    def _validate(self) -> None:

        if not self.root.exists():
            raise SiteConfigError(f"Site directory {self.root} not found.")

        site_yaml = self.root / Defaults.FILENAME_SITE_YAML

        if not site_yaml.exists():
            raise SiteConfigError(
                f"Site directory contains no '{Defaults.FILENAME_SITE_YAML}'."
            )

        path_contents = self.root / Defaults.DIRECTORY_NAME_CONTENTS

        try:
            path_contents = path_contents.resolve(strict=True)
        except FileNotFoundError as error:
            raise SiteConfigError(
                "Site directory missing 'contents' sub-directory."
            ) from error

        path_pages = self.contents / Defaults.DIRECTORY_NAME_PAGES

        try:
            path_pages = path_pages.resolve(strict=True)
        except FileNotFoundError as error:
            raise SiteConfigError(
                "Site directory missing 'pages' sub-directory."
            ) from error

        if not len(list(Globals.site_paths.iter_pages())):
            raise SiteConfigError(
                "Site 'pages' sub-directory contains no page directories."
            )

    @property
    def root(self) -> pathlib.Path:
        """ Returns /absolute/path/to/site-name """

        if self._root is None:
            raise SiteConfigError("Site root must be set before running.")

        return self._root

    @root.setter
    def root(self, value: pathlib.Path) -> None:
        """ Sets /absolute/path/to/site-name """
        self._root = value

    @property
    def contents(self) -> pathlib.Path:
        """ Returns /absolute/path/to/site-name/contents """
        return self.root / Defaults.DIRECTORY_NAME_CONTENTS

    @property
    def pages(self) -> pathlib.Path:
        """ Returns /absolute/path/to/site-name/contents/pages """
        return self.contents / Defaults.DIRECTORY_NAME_PAGES

    @property
    def cache(self) -> pathlib.Path:
        """ Returns /absolute/path/to/site-name/site-cache """
        return self.root / Defaults.DIRECTORY_NAME_SITE_CACHE

    @property
    def assets(self) -> List[str]:
        """Returns a list of paths pointing to all the sub-directories and
        files inside the 'contents' directory.

        This is useful for passing to a file-watcher to trigger a new build or
        reload a server."""

        return list(glob.glob(f"{self.contents}/**", recursive=True))

    @property
    def static_url_path(self) -> str:
        """ Returns an absolute url: /site """
        return Utils.urlify("site")

    def iter_pages(self) -> Generator[pathlib.Path, None, None]:
        """Returns a generator consisting of 'valid' page paths. Paths
        are filtered down to those which are directories, non private i.e names
        starting with "." or "_", and directories which contain a 'page.yaml'
        file."""

        for path in self.pages.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith(".") or path.name.startswith("_"):
                continue

            if not list(path.glob(Defaults.FILENAME_PAGE_YAML)):
                logger.warning(
                    f"Ignoring path {path}. Path contains no "
                    f"'{Defaults.FILENAME_PAGE_YAML}' file."
                )
                continue

            yield path


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
            Key.TITLE: {
                Key.LABEL: None,
                Key.IMAGE: None,
            },
        },
        Key.THEME: {
            Key.NAME: None,
            Key.PATH: None,
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
            raise SiteConfigError(
                f"Expected type 'list' for '{Key.MENU}' got '{type(menu).__name__}'."
            )

        header: dict = self._config_user.get(Key.HEADER, {})

        if type(header) is not dict:
            raise SiteConfigError(
                f"Expected type 'dict' for '{Key.HEADER}' got '{type(header).__name__}'."
            )

        theme: dict = self._config_user.get(Key.THEME, {})

        if type(theme) is not dict:
            raise SiteConfigError(
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
    def theme_path(self) -> Optional[str]:
        return self.__config[Key.THEME][Key.PATH]


class ThemePaths(GlobalsBase):

    _root: pathlib.Path

    def load(self) -> None:

        self._root = self._get_root__dispatcher()

        self._validate()

    def _validate(self) -> None:

        theme_yaml = self._root / Defaults.FILENAME_THEME_YAML

        if not theme_yaml.exists():
            raise ThemeConfigError(f"Theme missing {Defaults.FILENAME_THEME_YAML}")

        template_main_html = self._root / Defaults.FILENAME_TEMPLATE_MAIN_HTML

        if not template_main_html.exists():
            raise ThemeConfigError(
                f"Theme missing {Defaults.FILENAME_TEMPLATE_MAIN_HTML}"
            )

        template_404_html = self._root / Defaults.FILENAME_TEMPLATE_404_HTML

        if not template_404_html.exists():
            raise ThemeConfigError(
                f"Theme missing {Defaults.FILENAME_TEMPLATE_404_HTML}"
            )

    def _get_root__dispatcher(self) -> pathlib.Path:

        # Grab 'theme.name' and 'theme.path' from the 'site.yaml'.
        name: Optional[str] = self.globals.site_config.theme_name
        path: Optional[str] = self.globals.site_config.theme_path

        if name is not None and path is not None:
            logger.warning(
                "Setting both 'name' and 'custom-path' might result in unexpected behavior."
            )

        if path is not None:
            return self._get_custom_root(path=path)

        if name is None:
            return self._get_builtin_root(name=Defaults.DEFAULT_THEME_NAME_BUILTIN)

        if any(
            name.startswith(prefix)
            for prefix in [
                Defaults.THEME_NAME_PREFIX_INSTALLED,
                Defaults.THEME_NAME_PREFIX_TESTING,
            ]
        ):
            return self._get_installed_root(name=name)

        return self._get_builtin_root(name=name)

    def _get_custom_root(self, path: str) -> pathlib.Path:

        root = self.globals.site_paths.root / path

        try:
            root = root.resolve(strict=True)
        except FileNotFoundError as error:
            raise SiteConfigError(f"Custom theme {path} not found.") from error

        logger.info(f"Using custom theme from {path}.")

        return root

    @staticmethod
    def _get_installed_root(name: str) -> pathlib.Path:

        module_name = name.replace("-", "_")

        try:
            installed_theme = importlib.import_module(name=module_name)
        except ModuleNotFoundError as error:
            raise SiteConfigError(f"Installed theme '{name}' not found.") from error

        # The '__file__' attribute of 'installed_theme' is an absolute path
        # to the '__init__.py' file inside the theme directory.
        return pathlib.Path(installed_theme.__file__).parent

    @staticmethod
    def _get_builtin_root(name: str) -> pathlib.Path:
        """Returns the root directory of a built-in theme. Built-in themes
        are found in the 'themes' directory and conform to the following
        structure:

            src
            └── easel
                ├── ...
                └── themes
                    ├── ...
                    └── [NAME]
                        ├── src
               ROOT --> ├── [NAME]
                        │   ├── main.html
                        │   ├── 404.html
                        │   └── theme.yaml
                        └── package.json

        The second [NAME] directory is where the actual theme is located. The
        'src' directory contain the assets used to compile the theme i.e. SCSS
        and TypeScript files."""

        if name not in Defaults.VALID_THEME_NAMES_BUILTIN:
            raise SiteConfigError(
                f"Invalid theme name '{name}'. Available built-in themes are: "
                f"{Defaults.VALID_THEME_NAMES_BUILTIN}"
            )

        logger.info(f"Using built-in theme '{name}'.")

        return Defaults.APP_ROOT / Defaults.DIRECTORY_NAME_THEMES / name / name

    @property
    def root(self) -> pathlib.Path:
        """ Returns the root path to the current theme. """
        return self._root

    @property
    def template_main_html(self) -> pathlib.Path:
        """ Returns the path to the theme's main.html. """
        return self._root / Defaults.FILENAME_TEMPLATE_MAIN_HTML

    @property
    def template_404_html(self) -> pathlib.Path:
        """ Returns the path to the theme's 404.html. """
        return self._root / Defaults.FILENAME_TEMPLATE_404_HTML

    @property
    def assets(self) -> List[str]:
        """Returns a list of paths pointing to all the sub-directories and
        files inside the themes 'root' directory.

        This is useful for passing to a file-watcher to trigger a new build or
        reload a server."""

        return list(glob.glob(f"{self.root}/**", recursive=True))

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
