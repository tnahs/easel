import logging
import pathlib
from typing import Any, Iterator, Optional

from .enums import E_Directory, E_Filename
from .errors import SiteConfigError
from .globals import Globals
from .menu import Menu
from .model import BaseModel
from .pages import Page
from .utils import Utils


logger = logging.getLogger(__name__)


class Site(BaseModel):

    title: str
    author: Optional[str]
    copyright: Optional[str]
    description: Optional[str]
    favicon: Optional[str]
    menu: Optional[list[Menu]]
    pages: list[Page]

    def __str__(self) -> str:
        return f"<{type(self).__name__} '{self.title}'>"

    def __init__(self) -> None:

        self.validate__site_directory_structure()

        pages = self.get_page_configs()
        config = Utils.load_config(self.path / E_Filename.SITE_YAML.value)

        super().__init__(pages=pages, **config)

        logger.info(f"Building Site from {self.path}.")

        if logger.getEffectiveLevel() > logging.DEBUG:  # pragma: no cover
            logger.info("Set 'loglevel' to 'DEBUG' for more information.")

        if not self.menu:
            logger.warning(
                f"No menu will be generated. Key 'menu' in "
                f"{E_Filename.SITE_YAML.value} is empty."
            )

    def validate__site_directory_structure(self) -> None:

        if not self.path_contents.exists():
            raise SiteConfigError(
                f"site directory missing '{E_Directory.CONTENTS.value}' sub-directory"
            )

        if not self.path_pages.exists():
            raise SiteConfigError(
                f"site directory missing '{E_Directory.PAGES.value}' sub-directory"
            )

    @property
    def path(self) -> pathlib.Path:
        return Globals.site_root

    @property
    def path_contents(self) -> pathlib.Path:
        return self.path / E_Directory.CONTENTS.value

    @property
    def path_pages(self) -> pathlib.Path:
        return self.path_contents / E_Directory.PAGES.value

    '''
    @property
    def static_url_path(self) -> str:
        """Returns the absolute url: /site"""
        return Utils.urlify("site")

    @property
    def assets(self) -> list[str]:
        """Returns a list of paths pointing to all the sub-directories and
        files inside the 'contents' directory. This is useful for passing to a
        file-watcher to trigger a new build or reload a server."""

        return list(glob.glob(f"{self.path_contents}/**", recursive=True))
    '''

    def get_page_configs(self) -> Iterator[dict[str, Any]]:
        """Returns a iterator consisting of 'valid' page paths. Paths
        are filtered down to those which are directories, non private i.e names
        starting with "." or "_", and directories which contain a 'page.yaml'
        file."""

        for path in self.path_pages.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith(".") or path.name.startswith("_"):
                continue

            if not list(path.glob(E_Filename.PAGE_YAML.value)):
                logger.warning(
                    f"Ignoring path {path}. Path contains no "
                    f"'{E_Filename.PAGE_YAML.value}' file."
                )
                continue

            config = Utils.load_config(path / E_Filename.PAGE_YAML.value)
            config["path"] = path

            yield config
