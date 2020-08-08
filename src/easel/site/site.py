import logging
import pathlib
from typing import TYPE_CHECKING, List, Optional

from . import errors, menus, pages
from .config import config
from .helpers import config_loader


if TYPE_CHECKING:
    from .pages import PageType
    from .menus import MenuType


logger = logging.getLogger(__name__)


class Site:
    def __init__(self):

        logger.info(f"Building Site from {config.path_site}.")

        self._pages: List["PageType"] = []
        self._menu: List["MenuType"] = []

        self._page_error_404: Optional["PageType"] = None
        self._page_error_500: Optional["PageType"] = None

        self._page_current: "PageType"

        self._config: dict = config_loader.load(path=config.file_site_yaml)

        self._build_pages()
        self._build_error_pages()
        self._build_menu()

        self._validate_build()

    def __repr__(self):
        return f"<{self.__class__.__name__}:{config.path_site}>"

    def _build_pages(self):

        logger.info(f"Compiling Pages from {config.path_site_pages}.")

        for path in config.path_site_pages.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith("."):
                continue

            page = pages.page_factory.build(site=self, path_absolute=path)

            self._pages.append(page)

    def _build_error_pages(self):

        if not config.path_site_errors:
            return

        path_error_404 = config.path_site_errors / config.DIRECTORY_NAME_ERROR_404

        if path_error_404.exists():
            self._page_error_404 = pages.page_factory.build(
                site=self, path_absolute=path_error_404
            )

        path_error_500 = config.path_site_errors / config.DIRECTORY_NAME_ERROR_500

        if path_error_500.exists():
            self._page_error_500 = pages.page_factory.build(
                site=self, path_absolute=path_error_500
            )

    def _build_menu(self):

        if not self._config["menu"]["items"]:
            logger.warn(
                f"{config.FILENAME_SITE_YAML}:menu:items is empty. "
                f"No menu will be generated."
            )
            return

        for menu_data in self._config["menu"]["items"]:

            menu = menus.menu_factory.build(site=self, menu_data=menu_data)

            self._menu.append(menu)

    def _validate_build(self):

        # Booleans sum like integers. When more than one page is set as the
        # 'landing' page this will sum to >1.
        if sum([page.is_landing for page in self._pages]) > 1:
            raise errors.ConfigError("Site cannot have multiple 'landing' pages.")

    @property
    def config(self) -> dict:
        return self._config

    @property
    def pages(self) -> List["PageType"]:
        return [*self._pages, self.page_landing]

    @property
    def menu(self) -> List["MenuType"]:
        return self._menu

    def get_page(self, page_url: str) -> Optional["PageType"]:

        for page in self._pages:

            if page.url != page_url:
                continue

            self.page_current = page

            return page

        return None

    @property
    def page_landing(self) -> "PageType":

        for page in self._pages:

            if not page.is_landing:
                continue

            self.page_current = page

            return page

        raise errors.ConfigError("Site must have one page set as the 'landing' page.")

    @property
    def page_current(self) -> "PageType":
        return self._page_current

    @page_current.setter
    def page_current(self, page) -> None:
        self._page_current = page

    @property
    def page_error_404(self) -> Optional["PageType"]:
        return self._page_error_404

    @property
    def page_error_500(self) -> Optional["PageType"]:
        return self._page_error_500

    @property
    def assets(self) -> List[pathlib.Path]:
        """ Returns a list of paths pointing to all the sub-directories and
        files inside the main site directory. When starting up a development
        server, this list is passed to the 'extra_files' argument, allowing
        it to reload when any of the site files are modifed.

        via. https://werkzeug.palletsprojects.com/en/1.0.x/serving/ """

        return list(config.path_site.glob("**/*"))
