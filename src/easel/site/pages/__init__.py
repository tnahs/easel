import logging
import pathlib
from typing import Any, Optional, Type, Union

from ..defaults import Defaults, Key
from ..errors import PageConfigError
from ..helpers import Utils
from .pages import Layout, LayoutGallery, Lazy, LazyGallery


logger = logging.getLogger(__name__)


# See easel.site.contents
PageClass = Union[
    Type["Lazy"],
    Type["Layout"],
    Type["LazyGallery"],
    Type["LayoutGallery"],
]

PageClassLazy = Union[
    Type["LazyGallery"],
    Type["Lazy"],
]

PageClassLayout = Union[
    Type["Layout"],
    Type["LayoutGallery"],
]

PageClassGallery = Union[
    Type["LazyGallery"],
    Type["LayoutGallery"],
]

PageObj = Union[
    "Lazy",
    "Layout",
    "LazyGallery",
    "LayoutGallery",
]


class _PageFactory:

    _page_types = {
        Key.LAZY: Lazy,
        Key.LAYOUT: Layout,
        Key.LAZY_GALLERY: LazyGallery,
        Key.LAYOUT_GALLERY: LayoutGallery,
    }

    def build(self, path: pathlib.Path) -> PageObj:
        """ Builds Page-like object from a path. """

        path_page_config: pathlib.Path = path / Defaults.FILENAME_PAGE_YAML

        page_config: dict = Utils.load_config(path=path_page_config)

        try:
            page_type: str = page_config[Key.TYPE]
        except KeyError as error:
            raise PageConfigError(
                f"Missing required key '{Key.TYPE}' for Page-like item in {path}."
            ) from error

        # Get Page class based on 'page_type'.
        Page: Optional["PageClass"] = self.page_types(page_type=page_type)

        if Page is None:
            raise PageConfigError(
                f"Unsupported value '{page_type}' for '{Key.TYPE}' for "
                f"Page-like item in {path}."
            )

        return Page(path=path, config=page_config)

    def page_types(self, page_type: str) -> Optional["PageClass"]:
        return self._page_types.get(page_type, None)

    def register_page_type(self, name: str, page: Any) -> None:
        """ Register new Page-like object. """
        self._page_types[name] = page


PageFactory = _PageFactory()
