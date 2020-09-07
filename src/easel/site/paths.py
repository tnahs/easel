import pathlib
from typing import Optional, Union

from . import errors
from .defaults import SiteDefaults


class SitePaths:

    _root: Optional[pathlib.Path] = None

    @property
    def root(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site] """

        if self._root is None:
            raise errors.SiteConfigError("Site directory must be set before running.")

        return self._root

    @root.setter
    def root(self, value: Union[pathlib.Path, str]) -> None:
        """ Sets /absolute/path/to/[site] """

        path = pathlib.Path(value)

        try:
            path = path.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                f"Site directory {path} does not exist."
            ) from error

        self._root = path

    @property
    def pages(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/pages """

        path_pages = self.root / SiteDefaults.DIRECTORY_NAME_PAGES

        try:
            path_pages = path_pages.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                "Site directory missing 'pages' sub-directory."
            ) from error

        return path_pages

    @property
    def cache(self) -> pathlib.Path:
        """ Returns /absolute/path/to/[site]/.cache """
        return self.root / SiteDefaults.DIRECTORY_NAME_CACHE


site_paths__ = SitePaths()
