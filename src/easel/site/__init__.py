import logging
import os
import pathlib
from typing import TYPE_CHECKING, List, Optional

from . import errors, menus, pages
from .helpers import Key, Utils
from .paths import site_paths__
from .theme import site_theme__


if TYPE_CHECKING:
    from .menus import MenuObj
    from .pages import PageObj


logger = logging.getLogger(__name__)


from .defaults import SiteDefaults


class SiteConfig:
    def __init__(self, site: "Site"):

        self._site = site

        self._data = Utils.load_config(
            path=site_paths__.root / SiteDefaults.FILENAME_SITE_YAML
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
        # TODO: Re-implement SiteConfig.header after it's clearer how missing
        # keys and values will handled. We're trying to avoid forcing the user
        # to declare blank key-value pairs as well as avoid having to traverse
        # dictionaries to provide fallback default values.
        return self._data.get(Key.HEADER, {})

    @property
    def theme(self) -> dict:
        # TODO: Re-implement SiteConfig.theme after it's clearer how themes
        # will be configured.
        return self._data.get(Key.THEME, {})


class Site:

    _config: "SiteConfig"

    _pages: List["PageObj"] = []
    _page_current: "PageObj"

    _menu: List["MenuObj"] = []

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:

        if value is True:
            os.environ["FLASK_ENV"] = "development"

        self._debug = value

    def build(self) -> None:

        logger.info(f"Building Site from {site_paths__.root}.")

        self._config = SiteConfig(site=self)

        self._build_pages()
        self._build_menu()
        self._validate_build()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {site_paths__.root}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.config.title}"

    def _build_pages(self) -> None:

        for path in site_paths__.pages.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith("."):
                continue

            if not list(path.glob(SiteDefaults.FILENAME_PAGE_YAML)):
                logger.warning(
                    f"Ignoring path {path}. Path contains no "
                    f"'{SiteDefaults.FILENAME_PAGE_YAML}' file."
                )
                continue

            page = pages.page_factory.build(site=self, path_absolute=path)

            self._pages.append(page)

    def _build_menu(self) -> None:

        if not self.config.menu:
            logger.warn(
                f"No menu will be generated. Key '{Key.MENU}' in "
                f"{SiteDefaults.FILENAME_SITE_YAML} is empty."
            )
            return

        for menu_config in self.config.menu:

            menu = menus.menu_factory.build(site=self, config=menu_config)

            self._menu.append(menu)

    def _validate_build(self) -> None:

        # NOTE: Boolean types sum like integers!
        index_pages = sum([page.config.is_index for page in self._pages])

        if index_pages > 1 or index_pages < 1:
            raise errors.SiteConfigError(
                "Site must have one and only one 'index' page."
            )

    def rebuild_cache(self):

        logger.info(f"Rebuilding Site cache to {site_paths__.cache}.")

        for page in self.pages:
            for content in page.contents:

                try:
                    content.placeholder.cache(force=True)  # type: ignore
                except AttributeError:
                    continue

    @property
    def config(self) -> "SiteConfig":
        return self._config

    @property
    def pages(self) -> List["PageObj"]:
        return self._pages

    @property
    def menu(self) -> List["MenuObj"]:
        return self._menu

    @property
    def index(self) -> Optional["PageObj"]:

        for page in self._pages:

            if not page.is_index:
                continue

            self._page_current = page

            return page

        return None

    def get_page(self, page_url: str) -> Optional["PageObj"]:

        for page in self._pages:

            if page.url != page_url:
                continue

            self._page_current = page

            return page

        return None

    @property
    def page_current(self) -> "PageObj":
        return self._page_current

    @property
    def _assets_theme(self) -> List[pathlib.Path]:
        """ TEMP: This might become obsolete with the future implementation of
        themeing. Also see SiteDefaults.assets. """
        return list(site_theme__.root.glob("**/*"))

    @property
    def _assets_site(self) -> List[pathlib.Path]:
        """ TEMP: This might dramatically change with the future implementation
        of themeing. Also see SiteDefaults.assets. """

        assets_site = []

        for item in site_paths__.root.glob("**/*"):

            if item.name == SiteDefaults.DIRECTORY_NAME_CACHE:
                continue

            assets_site.append(item)

        return assets_site

    @property
    def assets(self) -> List[pathlib.Path]:
        """ Returns a list of paths pointing to all the sub-directories and
        files inside the 'theme' and 'site' directory.

        When starting up a development server, this list is passed to the
        'extra_files' argument, allowing it to reload when any of the site
        files are modifed.

        via. https://werkzeug.palletsprojects.com/en/1.0.x/serving/ """
        return [*self._assets_theme, *self._assets_site]
