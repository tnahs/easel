import logging
import pathlib
from typing import TYPE_CHECKING, List, Optional

from . import errors, menus, pages
from .defaults import Key
from .globals import Globals


if TYPE_CHECKING:
    from .globals import _SiteConfig
    from .menus import MenuObj
    from .pages import PageObj


logger = logging.getLogger(__name__)


from .defaults import Defaults


class Site:

    _pages: List["PageObj"] = []
    _page_current: "PageObj"

    _menu: List["MenuObj"] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {Globals.site_paths.root}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.config.title}"

    def build(self) -> None:

        logger.info(f"Building Site from {Globals.site_paths.root}.")

        if logger.getEffectiveLevel() > logging.DEBUG:
            logger.info("Set 'loglevel' to 'DEBUG' for more information.")

        self._build_pages()
        self._build_menu()
        self._validate_build()

    def _build_pages(self) -> None:

        for path in Globals.site_paths.pages.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith("."):
                continue

            if not list(path.glob(Defaults.FILENAME_PAGE_YAML)):
                logger.warning(
                    f"Ignoring path {path}. Path contains no "
                    f"'{Defaults.FILENAME_PAGE_YAML}' file."
                )
                continue

            page = pages.page_factory.build(site=self, path_absolute=path)

            self._pages.append(page)

    def _build_menu(self) -> None:

        if not self.config.menu:
            logger.warn(
                f"No menu will be generated. Key '{Key.MENU}' in "
                f"{Defaults.FILENAME_SITE_YAML} is empty."
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

        logger.info(f"Rebuilding Site cache to {Globals.site_paths.cache}.")

        for page in self.pages:
            for content in page.contents:

                try:
                    content.placeholder.cache(force=True)  # type: ignore
                except AttributeError:
                    continue

    @property
    def config(self) -> "_SiteConfig":
        return Globals.site_config

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
        themeing. Also see Site.assets. """
        return list(Globals.theme_paths.root.glob("**/*"))

    @property
    def _assets_site(self) -> List[pathlib.Path]:
        """ TEMP: This might dramatically change with the future implementation
        of themeing. Also see Site.assets. """

        assets_site = []

        for item in Globals.site_paths.root.glob("**/*"):

            if item.name == Defaults.DIRECTORY_NAME_CACHE:
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
