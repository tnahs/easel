import logging
import pathlib
from typing import TYPE_CHECKING, Any, List, Optional, Type, Union

from . import contents, errors
from .config import config
from .helpers import config_loader, markdown, utils


if TYPE_CHECKING:
    from .site import Site
    from .contents import ContentType


logger = logging.getLogger(__name__)


# See easel.site.contents
_PageType = Union[
    Type["Lazy"], Type["Layout"], Type["Markdown"],
]

PageType = Union[
    "Page", "Lazy", "Layout", "Markdown",
]


class PageFactory:
    def __init__(self):
        self._page_types = {
            "lazy": Lazy,
            "layout": Layout,
            "markdown": Markdown,
        }

    def build(self, site: "Site", path_absolute: pathlib.Path) -> PageType:
        """ Builds Page-like object from a path. """

        path_page_config: pathlib.Path = path_absolute / config.FILENAME_PAGE_YAML

        page_config: dict = config_loader.load(path=path_page_config)

        try:
            page_type: str = page_config["type"]
        except KeyError as error:
            raise errors.ConfigError(
                f"Missing 'type' in {path_page_config}."
            ) from error

        # Get Menu class based on 'menu_type'.
        Page: Optional[_PageType] = self.page_types(page_type=page_type)

        if Page is None:
            raise errors.ConfigError(
                f"Unsupported value for 'type' '{page_type}' in {path_page_config}."
            )

        return Page(site=site, path_absolute=path_absolute, config=page_config)

    def page_types(self, page_type: str) -> Optional[_PageType]:
        return self._page_types.get(page_type, None)

    def register_page_type(self, name: str, page: Any) -> None:
        """ Register new Page-like object. """
        self._page_types[name] = page


class Page:

    is_lazy: bool = False
    is_layout: bool = False
    is_markdown: bool = False

    def __init__(self, site: "Site", path_absolute: pathlib.Path, config: dict):

        self._site: "Site" = site
        self._path_absolute: pathlib.Path = path_absolute
        self._config: dict = config

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.path_relative}>"

    def _validate(self) -> None:

        if self.is_gallery:

            if (
                self.gallery_column_count == "auto"
                and self.gallery_column_width == "auto"
            ):
                raise errors.ConfigError(
                    f"{self}: Cannot set 'column-count' and 'column-width' to 'auto'."
                )

            if self.gallery_column_count not in config.VALID_GALLERY_COLUMN_COUNT:
                raise errors.ConfigError(
                    f"{self}: Unsupported value for 'column-count'."
                )

    @property
    def name(self) -> str:
        return self._path_absolute.stem

    @property
    def path_absolute(self) -> pathlib.Path:
        return self._path_absolute

    @property
    def path_relative(self) -> pathlib.Path:
        """ Returns path relative to to /[site]. """
        return self._path_absolute.relative_to(config.path_site)

    @property
    def file_config(self) -> pathlib.Path:
        return self._path_absolute / config.FILENAME_PAGE_YAML

    @property
    def config(self) -> dict:
        return self._config

    @property
    def contents(self) -> List["ContentType"]:
        raise NotImplementedError

    @property
    def url(self) -> str:
        return utils.slugify(self.name)

    @property
    def is_landing(self) -> bool:
        return self._config.get("is-landing", False)

    @property
    def description(self) -> Optional[str]:

        path = self._path_absolute / config.FILENAME_PAGE_DESCRIPTION

        try:
            return markdown.from_file(filepath=path, page=self)
        except FileNotFoundError:
            return None
        except Exception as error:
            raise errors.ConfigError(
                f"Unexpected Error while loading page description {path}."
            ) from error

    # 'Lazy' and 'Layout' page attributes. Not applicable to 'Markdown' pages.

    @property
    def show_captions(self) -> bool:
        # TODO: Add a check to make sure this is ignored/errors for markdown pages.
        return self._config.get("options", {}).get("show-captions", False)

    # Gallery related attributes.

    @property
    def is_gallery(self) -> bool:
        return self._config.get("options", {}).get("is-gallery", False)

    @property
    def gallery_column_count(self) -> bool:
        return self._config.get("options", {}).get("gallery-column-count", False)

    @property
    def gallery_column_width(self) -> bool:
        return self._config.get("options", {}).get("gallery-column-width", False)


class Lazy(Page):

    is_lazy: bool = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._validate()
        super()._validate()

    def _validate(self) -> None:
        pass

    @property
    def contents(self) -> List["ContentType"]:
        return self._contents

    @property
    def _contents(self) -> List["ContentType"]:

        items: List["ContentType"] = []

        """ pathlib.PosixPath.glob() returns a generator of pathlib.PosixPath
        objects. Contains absolute paths of all items and sub-items in the
        page's folder. """
        for path in self.path_absolute.glob("**/*"):

            # Ignore directories.
            if path.is_dir():
                continue

            # Ignore hidden files.
            if path.name.startswith("."):
                continue

            # Ignore page yaml file.
            if path.name == config.FILENAME_PAGE_YAML:
                continue

            # Ignore page description markdown file.
            if path.name == config.FILENAME_PAGE_DESCRIPTION:
                continue

            if path.suffix in config.VALID_IMAGE_TYPES:
                item = contents.Image(
                    page=self, path=path, caption={"title": path.stem}
                )

            elif path.suffix in config.VALID_VIDEO_TYPES:
                item = contents.Video(
                    page=self, path=path, caption={"title": path.stem}
                )

            elif path.suffix in config.VALID_AUDIO_TYPES:
                item = contents.Audio(
                    page=self, path=path, caption={"title": path.stem}
                )

            elif path.suffix in config.VALID_TEXT_TYPES:
                item = contents.TextBlock(page=self, path=path)

            elif path.suffix in config.VALID_YAML_TYPES:
                logger.warning(f"Unused layout file '{path.name}' found in {self}.")
                continue

            else:
                logger.warning(f"Unsupported file '{path.name}' found in {self}.")
                continue

            items.append(item)

        # NOTE: 'VideoEmbedded' doesn't have 'path_absolute' property.
        items.sort(key=lambda item: item.path_absolute)

        return items


class Layout(Page):

    is_layout = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._validate()
        super()._validate()

    def _validate(self) -> None:
        pass

    @property
    def contents(self) -> List["ContentType"]:
        return self._contents

    @property
    def _contents(self) -> List["ContentType"]:

        items: List["ContentType"] = []

        for content_data in self._config["contents"]:

            item: "ContentType" = contents.content_factory.build(
                page=self, content_data=content_data
            )

            items.append(item)

        return items


class Markdown(Page):

    is_markdown = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._validate()
        super()._validate()

    def _validate(self) -> None:

        if self.show_captions:
            raise errors.ConfigError(
                "Cannot set 'options:show-caption' in 'Markdown' page. "
            )

    @property
    def contents(self) -> List["ContentType"]:
        return self._contents

    @property
    def _contents(self) -> List["ContentType"]:

        items: List["ContentType"] = []

        """ pathlib.PosixPath.glob() returns a generator of pathlib.PosixPath
        objects. Contains absolute paths of all items and sub-items in the
        page's folder. """
        for path in self.path_absolute.glob("**/*"):

            # Ignore directories.
            if path.is_dir():
                continue

            # Ignore hidden files.
            if path.name.startswith("."):
                continue

            # Ignore page description markdown file.
            if path.name == config.FILENAME_PAGE_DESCRIPTION:
                continue

            if path.suffix not in config.VALID_TEXT_TYPES:
                continue

            item = contents.TextBlock(page=self, path=path)

            items.append(item)

        # NOTE: 'VideoEmbedded' doesn't have 'path_absolute' property.
        items.sort(key=lambda items: items.path_absolute)

        return items


page_factory = PageFactory()
