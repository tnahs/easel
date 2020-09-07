# import pathlib
# import logging
# from typing import TYPE_CHECKING, List, Optional, Union

# from . import errors, menus, pages
# from . import global_config
# from .helpers import Key, Utils


# if TYPE_CHECKING:
#     from .pages import PageObj
#     from .menus import MenuObj


# logger = logging.getLogger(__name__)


# class SiteConfig:
#     def __init__(self, site: "Site"):

#         self._site = site

#         self._data = Utils.load_config(
#             path=self._site.path / global_config.FILENAME_SITE_YAML
#         )

#         self._validate()

#     def _validate(self) -> None:

#         menu: dict = self._data.get(Key.MENU, [])

#         if type(menu) is not list:
#             raise errors.SiteConfigError(
#                 f"Expected type 'list' for '{Key.MENU}' got '{type(menu).__name__}'."
#             )

#         header: dict = self._data.get(Key.HEADER, {})

#         if type(header) is not dict:
#             raise errors.SiteConfigError(
#                 f"Expected type 'dict' for '{Key.HEADER}' got '{type(header).__name__}'."
#             )

#         theme: dict = self._data.get(Key.THEME, {})

#         if type(theme) is not dict:
#             raise errors.SiteConfigError(
#                 f"Expected type 'dict' for '{Key.THEME}' got '{type(theme).__name__}'."
#             )

#     @property
#     def title(self) -> str:
#         return self._data.get(Key.TITLE, "")

#     @property
#     def author(self) -> str:
#         return self._data.get(Key.AUTHOR, "")

#     @property
#     def copyright(self) -> str:
#         return self._data.get(Key.COPYRIGHT, "")

#     @property
#     def description(self) -> str:
#         return self._data.get(Key.DESCRIPTION, "")

#     @property
#     def favicon(self) -> str:
#         return self._data.get(Key.FAVICON, "")

#     @property
#     def menu(self) -> list:
#         return self._data.get(Key.MENU, [])

#     @property
#     def header(self) -> dict:
#         # TODO: Re-implement SiteConfig.header after it's clearer how missing
#         # keys and values will handled. We're trying to avoid forcing the user
#         # to declare blank key-value pairs as well as avoid having to traverse
#         # dictionaries to provide fallback default values.
#         return self._data.get(Key.HEADER, {})

#     @property
#     def theme(self) -> dict:
#         # TODO: Re-implement SiteConfig.theme after it's clearer how themes
#         # will be configured.
#         return self._data.get(Key.THEME, {})


# class Site:

#     _path: Optional[pathlib.Path] = None
#     _config: "SiteConfig"

#     _theme_name: Optional[str] = None
#     _path_theme_custom: Optional[pathlib.Path] = None

#     _pages: List["PageObj"] = []
#     _page_current: "PageObj"

#     _menu: List["MenuObj"] = []

#     def build(self) -> None:

#         logger.info(f"Building Site from {self.path}.")

#         self._config = SiteConfig(site=self)

#         self._build_pages()
#         self._build_menu()
#         self._validate_build()

#     def __repr__(self) -> str:
#         return f"<{self.__class__.__name__}: {self.path}>"

#     def __str__(self) -> str:
#         return f"{self.__class__.__name__}: {self.config.title}"

#     def _build_pages(self) -> None:

#         for path in self.path_pages.iterdir():

#             if not path.is_dir():
#                 continue

#             if path.name.startswith("."):
#                 continue

#             if not list(path.glob(global_config.FILENAME_PAGE_YAML)):
#                 logger.warning(
#                     f"Ignoring path {path}. Path contains no "
#                     f"'{global_config.FILENAME_PAGE_YAML}' file."
#                 )
#                 continue

#             page = pages.page_factory.build(site=self, path_absolute=path)

#             self._pages.append(page)

#     def _build_menu(self) -> None:

#         if not self.config.menu:
#             logger.warn(
#                 f"No menu will be generated. Key '{Key.MENU}' in "
#                 f"{global_config.FILENAME_SITE_YAML} is empty."
#             )
#             return

#         for menu_config in self.config.menu:

#             menu = menus.menu_factory.build(site=self, config=menu_config)

#             self._menu.append(menu)

#     def _validate_build(self) -> None:

#         # NOTE: Boolean types sum like integers!
#         index_pages = sum([page.config.is_index for page in self._pages])

#         if index_pages > 1 or index_pages < 1:
#             raise errors.SiteConfigError(
#                 "Site must have one and only one 'index' page."
#             )

#     def rebuild_cache(self):

#         logger.info(f"Rebuilding Site cache to {self.path_cache}.")

#         for page in self.pages:
#             for content in page.contents:

#                 try:
#                     content.placeholder.cache(force=True)  # type: ignore
#                 except AttributeError:
#                     continue

#     @property
#     def path(self) -> pathlib.Path:
#         """ Returns /absolute/path/to/[site] """

#         if self._path is None:
#             raise errors.SiteConfigError("Site directory must be set before running.")

#         return self._path

#     @path.setter
#     def path(self, value: Union[pathlib.Path, str]) -> None:
#         """ Sets /absolute/path/to/[site] """

#         path = pathlib.Path(value)

#         try:
#             path = path.resolve(strict=True)
#         except FileNotFoundError as error:
#             raise errors.SiteConfigError(
#                 f"Site directory {path} does not exist."
#             ) from error

#         self._path = path

#     @property
#     def path_pages(self) -> pathlib.Path:
#         """ Returns /absolute/path/to/[site]/pages """

#         path_pages = self.path / global_config.DIRECTORY_NAME_PAGES

#         try:
#             path_pages = path_pages.resolve(strict=True)
#         except FileNotFoundError as error:
#             raise errors.SiteConfigError(
#                 "Site directory missing 'pages' sub-directory."
#             ) from error

#         return path_pages

#     @property
#     def path_cache(self) -> pathlib.Path:
#         """ Returns /absolute/path/to/[site]/.cache """
#         return self.path / global_config.DIRECTORY_NAME_CACHE

#     @property
#     def theme_name(self) -> str:
#         """ Returns the name of the current theme. This method is accessed only
#         if a path to a custom theme is not set. """

#         if self._theme_name is None:
#             return global_config.DEFAULT_THEME_NAME

#         return self._theme_name

#     @theme_name.setter
#     def theme_name(self, value: Optional[str]) -> None:
#         """ Changes the current theme name. """

#         if not value:
#             return

#         if value not in global_config.VALID_THEME_NAMES:
#             raise errors.SiteConfigError(
#                 f"Invalid theme name '{value}'. Available themes are: "
#                 f"{global_config.VALID_THEME_NAMES}"
#             )

#         self._theme_name = value

#     @property
#     def path_theme(self) -> pathlib.Path:
#         """ Returns the path to the current theme. """

#         if self._path_theme_custom is None:
#             return (
#                 global_config.PATH_ROOT
#                 / global_config.DIRECTORY_NAME_THEMES
#                 / self.theme_name
#             )

#         return self._path_theme_custom

#     @path_theme.setter
#     def path_theme(self, value: Optional[Union[pathlib.Path, str]]) -> None:
#         """ Sets the theme path to a custom location. """

#         if not value:
#             return

#         path_theme = pathlib.Path(value)

#         try:
#             path_theme = path_theme.resolve(strict=True)
#         except FileNotFoundError as error:
#             raise errors.SiteConfigError(
#                 f"Theme directory {value} not found."
#             ) from error

#         self._path_theme_custom = path_theme

#     @property
#     def path_theme_static(self) -> pathlib.Path:
#         """ Returns the path to the current theme's static directory. """
#         return self.path_theme / global_config.DIRECTORY_NAME_STATIC

#     @property
#     def path_theme_templates(self) -> pathlib.Path:
#         """ Returns the path to the current theme's templates directory. """
#         return self.path_theme / global_config.DIRECTORY_NAME_TEMPLATES

#     @property
#     def config(self) -> "SiteConfig":
#         return self._config

#     @property
#     def pages(self) -> List["PageObj"]:
#         return self._pages

#     @property
#     def menu(self) -> List["MenuObj"]:
#         return self._menu

#     @property
#     def index(self) -> Optional["PageObj"]:

#         for page in self._pages:

#             if not page.is_index:
#                 continue

#             self._page_current = page

#             return page

#         return None

#     def get_page(self, page_url: str) -> Optional["PageObj"]:

#         for page in self._pages:

#             if page.url != page_url:
#                 continue

#             self._page_current = page

#             return page

#         return None

#     @property
#     def page_current(self) -> "PageObj":
#         return self._page_current

#     @property
#     def _assets_theme(self) -> List[pathlib.Path]:
#         """ TEMP: This might become obsolete with the future implementation of
#         themeing. Also see GlobalConfig.assets. """
#         return list(self.path_theme.glob("**/*"))

#     @property
#     def _assets_site(self) -> List[pathlib.Path]:
#         """ TEMP: This might dramatically change with the future implementation
#         of themeing. Also see GlobalConfig.assets. """

#         assets_site = []

#         for item in self.path.glob("**/*"):

#             if item.name == global_config.DIRECTORY_NAME_CACHE:
#                 continue

#             assets_site.append(item)

#         return assets_site

#     @property
#     def assets(self) -> List[pathlib.Path]:
#         """ Returns a list of paths pointing to all the sub-directories and
#         files inside the 'theme' and 'site' directory.

#         When starting up a development server, this list is passed to the
#         'extra_files' argument, allowing it to reload when any of the site
#         files are modifed.

#         via. https://werkzeug.palletsprojects.com/en/1.0.x/serving/ """
#         return [*self._assets_theme, *self._assets_site]
