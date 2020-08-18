import logging
import pathlib
from typing import Any, TYPE_CHECKING, List, Optional

from . import errors, menus, pages
from .config import config
from .helpers import Utils, Keys, SafeDict


if TYPE_CHECKING:
    from .pages import PageObj
    from .menus import MenuObj


logger = logging.getLogger(__name__)


class Site:

    _pages: List["PageObj"] = []
    _page_error_404: Optional["PageObj"] = None
    _page_error_500: Optional["PageObj"] = None
    _page_current: "PageObj"
    _menu: List["MenuObj"] = []

    def __init__(self):

        logger.info(f"Building Site from {config.path_site}.")

        self._config_data = Utils.load_config(path=config.file_site_yaml)

        self._build_pages()
        self._build_error_pages()
        self._build_menu()

        self._validate__build()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{config.path_site}>"

    def _build_pages(self) -> None:

        logger.info(f"Compiling Pages from {config.path_site_pages}.")

        for path in config.path_site_pages.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith("."):
                continue

            page = pages.page_factory.build(site=self, path_absolute=path)

            self._pages.append(page)

    def _build_error_pages(self) -> None:

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

    def _build_menu(self) -> None:

        if not self._config[Keys.MENU]:
            logger.warn(
                f"{self}: {config.FILENAME_SITE_YAML} 'menu' is empty. "
                f"No menu will be generated."
            )
            return

        for menu_data in self._config[Keys.MENU]:

            menu = menus.menu_factory.build(site=self, menu_data=menu_data)

            self._menu.append(menu)

    def _validate__build(self) -> None:

        # Boolean types sum like integers. When more than one page is set as
        # the 'landing' page this will sum to >1.
        if sum([page.is_landing for page in self._pages]) > 1:
            raise errors.SiteConfigError(
                f"{self}: Site cannot have multiple 'landing' pages."
            )

    @property
    def _config(self) -> dict:
        return {
            Keys.TITLE: self._config_data.get(Keys.TITLE, ""),
            Keys.AUTHOR: self._config_data.get(Keys.AUTHOR, ""),
            Keys.COPYRIGHT: self._config_data.get(Keys.COPYRIGHT, ""),
            Keys.FAVICON: self._config_data.get(Keys.FAVICON, ""),
            Keys.MENU: self._config_data.get(Keys.MENU, []),
        }

    @property
    def _theme(self) -> SafeDict:

        data: dict = self._config_data.get(Keys.THEME, {})

        if data is None:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Keys.THEME}' got '{type(data).__name__}'."
            )

        return SafeDict(**data)

    @property
    def _extras(self) -> SafeDict:

        data: dict = self._config_data.get(Keys.EXTRAS, {})

        if data is None:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Keys.EXTRAS}' got '{type(data).__name__}'."
            )

        return SafeDict(**data)

    @staticmethod
    def _get_config(basename: str, obj: dict, path: str) -> Any:
        """ Template Accessor Helper """

        value: dict = obj

        for key in path.split("."):

            try:
                value = value[key]
            except (KeyError, TypeError) as error:
                raise errors.TemplateConfigError(
                    f"Error accessing '{key}' in '{basename}.{path}' from object '{obj}'."
                ) from error

        return value

    def config(self, path: str) -> Any:
        """ Template Accessor """
        return self._get_config(basename="config", obj=self._config, path=path)

    def theme(self, path: str) -> Any:
        """ Template Accessor """
        return self._get_config(basename="theme", obj=self._theme, path=path)

    def extras(self, path: str) -> Any:
        """ Template Accessor """
        return self._get_config(basename="extras", obj=self._extras, path=path)

    @property
    def pages(self) -> List["PageObj"]:
        return [*self._pages, self.page_landing]

    @property
    def menu(self) -> List["MenuObj"]:
        return self._menu

    def get_page(self, page_url: str) -> Optional["PageObj"]:

        for page in self._pages:

            if page.url != page_url:
                continue

            self._page_current = page

            return page

        return None

    @property
    def page_landing(self) -> "PageObj":

        for page in self._pages:

            if not page.is_landing:
                continue

            self._page_current = page

            return page

        raise errors.SiteConfigError(
            f"{self}: Site must have one page set as the 'landing' page."
        )

    @property
    def page_current(self) -> "PageObj":
        return self._page_current

    @property
    def page_error_404(self) -> Optional["PageObj"]:
        return self._page_error_404

    @property
    def page_error_500(self) -> Optional["PageObj"]:
        return self._page_error_500

    @property
    def assets(self) -> List[pathlib.Path]:
        """ Returns a list of paths pointing to all the sub-directories and
        files inside the main site directory. When starting up a development
        server, this list is passed to the 'extra_files' argument, allowing
        it to reload when any of the site files are modifed.

        via. https://werkzeug.palletsprojects.com/en/1.0.x/serving/ """

        return list(config.path_site.glob("**/*"))
