import logging
from typing import TYPE_CHECKING, List, Optional

from .defaults import Key
from .errors import SiteConfigError
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

    _pages: List["PageObj"] = []
    _menu: List["MenuObj"] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {Globals.site_paths.root}>"

    def build(self) -> None:

        logger.info(f"Building Site from {Globals.site_paths.root}.")

        if logger.getEffectiveLevel() > logging.DEBUG:
            logger.info("Set 'loglevel' to 'DEBUG' for more information.")

        self._build_pages()
        self._build_menu()

        self._validate_build()

    def _build_pages(self) -> None:

        if not len(list(Globals.site_paths.iter_pages())):
            logger.warn(
                "No pages will be generated. Site pages directory contains no "
                "page directories."
            )
            return

        self._pages = [
            PageFactory.build(path=path) for path in Globals.site_paths.iter_pages()
        ]

    def _build_menu(self) -> None:

        if not self.config.menu:
            logger.warn(
                f"No menu will be generated. Key '{Key.MENU}' in "
                f"{Defaults.FILENAME_SITE_YAML} is empty."
            )
            return

        self._menu = [MenuFactory.build(config=config) for config in self.config.menu]

    def _validate_build(self) -> None:
        self._validate_index()
        self._validate_menu()

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
        return self._pages

    @property
    def menu(self) -> List["MenuObj"]:
        return self._menu

    @property
    def index(self) -> Optional["PageObj"]:

        for page in self._pages:

            if not page.is_index:
                continue

            return page

        return None

    def get_page(self, page_url: str) -> Optional["PageObj"]:

        page_url = Utils.normalize_page_path(path=page_url)

        for page in self._pages:

            if page.url != page_url:
                continue

            return page

        return None
