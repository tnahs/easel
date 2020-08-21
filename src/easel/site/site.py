import logging
import pathlib
from typing import TYPE_CHECKING, List, Optional

from flask.globals import current_app

from . import errors, menus, pages
from .config import config
from .helpers import Key, SafeDict, Utils


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
        self._config = self._parse_config()

        self._validate_config()

        self._build_pages()
        self._build_error_pages()
        self._build_menu()

        self._validate_build()

        self._set_theme()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{config.path_site}>"

    def _parse_config(self) -> dict:

        title = self._config_data.get(Key.TITLE, "")
        author = self._config_data.get(Key.AUTHOR, "")
        copyright_ = self._config_data.get(Key.COPYRIGHT, "")
        favicon = self._config_data.get(Key.FAVICON, "")

        menu = self._config_data.get(Key.MENU, [])

        header = SafeDict(**self._config_data.get(Key.HEADER, {}))

        theme = SafeDict(**self._config_data.get(Key.THEME, {}))

        return {
            Key.TITLE: title,
            Key.AUTHOR: author,
            Key.COPYRIGHT: copyright_,
            Key.FAVICON: favicon,
            Key.MENU: menu,
            Key.HEADER: header,
            Key.THEME: theme,
        }

    def _validate_config(self) -> None:

        menu: dict = self._config_data.get(Key.MENU, [])

        if type(menu) is not list:
            raise errors.SiteConfigError(
                f"Expected type 'list' for '{Key.MENU}' got '{type(menu).__name__}'."
            )

        theme: dict = self._config_data.get(Key.THEME, {})

        if type(theme) is not dict:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Key.THEME}' got '{type(theme).__name__}'."
            )

        header: dict = self._config_data.get(Key.HEADER, {})

        if type(header) is not dict:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Key.HEADER}' got '{type(header).__name__}'."
            )

    def _build_pages(self) -> None:

        for path in config.path_site_pages.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith("."):
                continue

            if not list(path.glob(config.FILENAME_PAGE_YAML)):
                logger.warning(
                    f"Ignoring path {path}. Path contains no '{config.FILENAME_PAGE_YAML}' file."
                )
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

        if not self.config[Key.MENU]:
            logger.warn(
                f"No menu will be generated. Key 'menu' in {config.FILENAME_SITE_YAML} is empty."
            )
            return

        for menu_data in self.config[Key.MENU]:

            menu = menus.menu_factory.build(site=self, menu_data=menu_data)

            self._menu.append(menu)

    def _validate_build(self) -> None:

        # (Boolean types sum like integers!)
        index_pages = sum([page.is_index for page in self._pages])

        if index_pages > 1 or index_pages < 1:
            raise errors.SiteConfigError(
                "Site must have one and only one 'index' page."
            )

    def _set_theme(self) -> None:

        theme_name = self.config[Key.THEME].get(Key.NAME, None)

        if theme_name is None:
            return

        config.theme_name = theme_name

    @property
    def config(self) -> dict:
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
    def page_error_404(self) -> Optional["PageObj"]:
        return self._page_error_404

    @property
    def page_error_500(self) -> Optional["PageObj"]:
        return self._page_error_500
