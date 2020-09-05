import logging
from typing import TYPE_CHECKING, List, Optional

from . import errors, menus, pages
from . import global_config
from .helpers import Key, Utils


if TYPE_CHECKING:
    from .pages import PageObj
    from .menus import MenuObj


logger = logging.getLogger(__name__)


class Site:

    _pages: List["PageObj"] = []
    _page_current: "PageObj"

    _menu: List["MenuObj"] = []

    def __init__(self):

        logger.info(f"Building Site from {global_config.path_site}.")

        self._config = SiteConfig()

        self._build_pages()
        self._build_menu()
        self._validate_build()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {global_config.path_site}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.config.title}"

    def _build_pages(self) -> None:

        for path in global_config.path_site_pages.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith("."):
                continue

            if not list(path.glob(global_config.FILENAME_PAGE_YAML)):
                logger.warning(
                    f"Ignoring path {path}. Path contains no '{global_config.FILENAME_PAGE_YAML}' file."
                )
                continue

            page = pages.page_factory.build(site=self, path_absolute=path)

            self._pages.append(page)

    def _build_menu(self) -> None:

        if not self.config.menu:
            logger.warn(
                f"No menu will be generated. Key 'menu' in {global_config.FILENAME_SITE_YAML} is empty."
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

        logger.info(f"Rebuilding Site cache to {global_config.path_site_cache}.")

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


class SiteConfig:
    def __init__(self):

        self._data = Utils.load_config(path=global_config.file_site_yaml)

        self._validate()

        global_config.theme_name = self.theme_name

    def _validate(self) -> None:

        menu: dict = self._data.get(Key.MENU, [])

        if type(menu) is not list:
            raise errors.SiteConfigError(
                f"Expected type 'list' for '{Key.MENU}' got '{type(menu).__name__}'."
            )

        theme: dict = self._data.get(Key.THEME, {})

        if type(theme) is not dict:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Key.THEME}' got '{type(theme).__name__}'."
            )

        header: dict = self._data.get(Key.HEADER, {})

        if type(header) is not dict:
            raise errors.SiteConfigError(
                f"Expected type 'dict' for '{Key.HEADER}' got '{type(header).__name__}'."
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

    @property
    def theme_name(self) -> Optional[str]:
        return self.theme.get(Key.NAME, "")
