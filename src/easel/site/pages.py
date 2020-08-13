import abc
import logging
import pathlib
from typing import TYPE_CHECKING, Any, List, Optional, Type, Union

from . import contents, errors
from .config import config
from .helpers import config_loader, markdown, utils


if TYPE_CHECKING:
    from .site import Site
    from .contents import ContentObj


logger = logging.getLogger(__name__)


# See easel.site.contents
PageClass = Union[
    Type["Lazy"], Type["Layout"], Type["Markdown"],
]

PageObj = Union[
    "Page", "Lazy", "Layout", "Markdown",
]


class _PageFactory:
    def __init__(self):
        self._page_types = {
            "lazy": Lazy,
            "layout": Layout,
            "markdown": Markdown,
        }

    def build(self, site: "Site", path_absolute: pathlib.Path) -> PageObj:
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
        Page: Optional[PageClass] = self.page_types(page_type=page_type)

        if Page is None:
            raise errors.ConfigError(
                f"Unsupported value for 'type' '{page_type}' in {path_page_config}."
            )

        return Page(site=site, path_absolute=path_absolute, config=page_config)

    def page_types(self, page_type: str) -> Optional[PageClass]:
        return self._page_types.get(page_type, None)

    def register_page_type(self, name: str, page: Any) -> None:
        """ Register new Page-like object. """
        self._page_types[name] = page


class Page(abc.ABC):
    def __init__(self, site: "Site", path_absolute: pathlib.Path, config: dict):

        self._site: "Site" = site
        self._path_absolute: pathlib.Path = path_absolute
        self._config: dict = config

        self.validate()

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.path_relative}>"

    @property
    @abc.abstractmethod
    def contents(self) -> List["ContentObj"]:
        pass

    @abc.abstractmethod
    def validate(self) -> None:
        pass

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

    @property
    def options(self) -> dict:

        options = self._config.get("options", {})

        if options is None:
            raise errors.ConfigError(f"{self}: Cannot set 'options' to None.")

        return options


class CaptionsMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def options(self) -> dict:
        pass

    @property
    def show_captions(self) -> bool:
        return self.options.get("show-captions", False)


class GalleryMixin(abc.ABC):
    def validate_gallery(self) -> None:

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
    @abc.abstractmethod
    def options(self) -> dict:
        pass

    @property
    def is_gallery(self) -> bool:
        return self.options.get("is-gallery", False)

    @property
    def gallery_column_count(self) -> bool:
        return self.options.get(
            "gallery-column-count", config.DEFAULT_GALLERY_COLUMN_COUNT
        )

    @property
    def gallery_column_width(self) -> bool:
        return self.options.get(
            "gallery-column-width", config.DEFAULT_GALLERY_COLUMN_WIDTH
        )


class Lazy(Page, CaptionsMixin, GalleryMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self) -> None:
        self.validate_gallery()

    @property
    def contents(self) -> List["ContentObj"]:
        return self._contents

    @property
    def _contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

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

        # Ignoring type because 'VideoEmbedded' doesn't have 'path_absolute'
        # property. However a 'VideoEmbedded' will never show up in this list.
        items.sort(key=lambda item: item.path_absolute)  # type: ignore

        return items


class Layout(Page, CaptionsMixin, GalleryMixin):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> None:
        pass

    @property
    def contents(self) -> List["ContentObj"]:
        return self._contents

    @property
    def _contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

        for content_data in self._config["contents"]:

            item: "ContentObj" = contents.content_factory.build(
                page=self, content_data=content_data
            )

            items.append(item)

        return items


class Markdown(Page, GalleryMixin):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # TODO: Log warning when 'show-captions' is present.
        # logger.warning("Cannot set 'options:show-caption' in 'Markdown' page. ")

    def validate(self) -> None:
        pass

    @property
    def contents(self) -> List["ContentObj"]:
        return self._contents

    @property
    def _contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

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

        # Ignoring type because 'VideoEmbedded' doesn't have 'path_absolute'
        # property. However a 'VideoEmbedded' will never show up in this list.
        items.sort(key=lambda items: items.path_absolute)  # type:ignore

        return items


page_factory = _PageFactory()
