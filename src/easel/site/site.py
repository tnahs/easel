import logging
from typing import TYPE_CHECKING, List, Optional

from .defaults import Key
from .errors import Error, SiteConfigError
from .globals import Globals
from .helpers import Utils
from .menus import LinkPage, MenuFactory
from .pages import PageFactory


if TYPE_CHECKING:
    from .globals import SiteConfig
    from .menus import MenuObj
    from .pages import PageObj


logger = logging.getLogger(__name__)


from .defaults import Defaults


class Site:

    _pages: Optional[List["PageObj"]] = None
    _menu: Optional[List["MenuObj"]] = None

    _index: Optional["PageObj"] = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {Globals.site_paths.root}>"

    def build(self) -> None:

        logger.info(f"Building Site from {Globals.site_paths.root}.")

        if logger.getEffectiveLevel() > logging.DEBUG:  # pragma: no cover
            logger.info("Set 'loglevel' to 'DEBUG' for more information.")

        self._build()
        self._validate()

    def _build(self) -> None:
        self._build_pages()
        self._build_menu()
        self._set_index()

    def _build_pages(self) -> None:

        if not len(list(Globals.site_paths.iter_pages())):
            raise SiteConfigError("Site pages directory contains no page directories.")

        self._pages = [
            PageFactory.build(path=path) for path in Globals.site_paths.iter_pages()
        ]

    def _build_menu(self) -> None:

        if not self.config.menu:
            logger.warning(
                f"No menu will be generated. Key '{Key.MENU}' in "
                f"{Defaults.FILENAME_SITE_YAML} is empty."
            )

        self._menu = [MenuFactory.build(config=config) for config in self.config.menu]

    def _set_index(self) -> None:

        for page in self._pages:

            if not page.is_index:
                continue

            self._index = page

    def _validate(self) -> None:
        self._validate_menu()
        self._validate_index()

    def _validate_index(self) -> None:

        # Boolean types sum like integers!
        index_pages = sum([page.is_index for page in self._pages])

        if index_pages > 1 or index_pages < 1:
            raise SiteConfigError("Site must have one and only one 'index' page.")

    def _validate_menu(self) -> None:

        page_urls: List[str] = [page.url for page in self.pages]

        menu_items: List["LinkPage"] = [
            menu for menu in self.menu if isinstance(menu, LinkPage)
        ]

        for menu_item in menu_items:
            if menu_item.url not in page_urls:
                raise SiteConfigError(
                    f"Menu item '{menu_item.label}' has no corresponding "
                    f"page. Page '{menu_item.links_to}' not found."
                )

    def rebuild_cache(self) -> None:
        # TODO:LOW This method might have room for some optimization.

        logger.info(f"Rebuilding site-cache to {Globals.site_paths.cache}.")

        for page in self.pages:
            for content in page.contents:

                try:
                    content.proxy_images.cache(force=True)  # type: ignore
                    content.proxy_colors.cache(force=True)  # type: ignore
                except AttributeError:
                    continue

    @property
    def config(self) -> "SiteConfig":
        return Globals.site_config

    @property
    def pages(self) -> List["PageObj"]:

        if self._pages is None:
            raise Error("Site must be built before accessing pages.")

        return self._pages

    @property
    def menu(self) -> List["MenuObj"]:

        if self._menu is None:
            raise Error("Site must be built before accessing menu.")

        return self._menu

    @property
    def index(self) -> "PageObj":

        if self._index is None:
            raise Error("Site must be built before accessing index.")

        return self._index

    def get_page(self, page_url: str) -> Optional["PageObj"]:

        page_url = Utils.normalize_page_path(path=page_url)

        for page in self.pages:

            if page.url != page_url:
                continue

            return page

        return None
