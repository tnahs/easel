import logging
import pathlib
from typing import TYPE_CHECKING, List, Optional

from . import errors, menus, pages
from .config import config
from .helpers import config_loader


if TYPE_CHECKING:
    from .pages import PageObj
    from .menus import MenuObj


logger = logging.getLogger(__name__)


class SafeDict(dict):
    """ https://stackoverflow.com/a/25840834 """

    def __getitem__(self, key):

        if key not in self:
            return self.setdefault(key, type(self)())

        return super().__getitem__(key)


class Site:

    _pages: List["PageObj"] = []
    _page_error_404: Optional["PageObj"] = None
    _page_error_500: Optional["PageObj"] = None
    _page_current: "PageObj"
    _menu: List["MenuObj"] = []

    def __init__(self):

        logger.info(f"Building Site from {config.path_site}.")

        self._config = self._load_config()

        self._build_pages()
        self._build_error_pages()
        self._build_menu()

        self._validate__build()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{config.path_site}>"

    def _load_config(self) -> dict:

        data: dict = config_loader.load(path=config.file_site_yaml)

        page = data.get("page", {})

        colors = data.get("colors", {})

        menu = data.get("menu", {})
        menu_header = menu.get("header", {})
        menu_header_image = menu_header.get("image", {})

        return {
            "title": data.get("title", ""),
            "favicon": data.get("favicon", ""),
            "copyright": data.get("copyright", ""),
            "author": data.get("author", ""),
            "page": {
                "width": page.get("width", ""),
                #
            },
            "colors": {
                "accent-base": colors.get("accent-base", ""),
                "accent-light": colors.get("accent-light", ""),
            },
            "menu": {
                "width": menu.get("width", ""),
                "align": menu.get("align", ""),
                "items_": menu.get("items", []),
                "header": {
                    "label": menu_header.get("label", ""),
                    "image": {
                        "path": menu_header_image.get("path", ""),
                        "width": menu_header_image.get("width", ""),
                        "height": menu_header_image.get("height", ""),
                    },
                },
            },
        }

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

        if not self._config["menu"]["items_"]:
            logger.warn(
                f"{self}: {config.FILENAME_SITE_YAML} missing 'menu.items'. "
                f"No menu will be generated."
            )
            return

        for menu_data in self._config["menu"]["items_"]:

            menu = menus.menu_factory.build(site=self, menu_data=menu_data)

            self._menu.append(menu)

    def _validate__build(self) -> None:

        # Boolean types sum like integers. When more than one page is set as
        # the 'landing' page this will sum to >1.
        if sum([page.is_landing for page in self._pages]) > 1:
            raise errors.ConfigError(
                f"{self}: Site cannot have multiple 'landing' pages."
            )

    @property
    def config(self) -> dict:
        return self._config

    @property
    def theme(self) -> SafeDict:
        return SafeDict({"key_one": "value_one"})

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

        raise errors.ConfigError(
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
