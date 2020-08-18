import abc
import logging
import pathlib
from typing import TYPE_CHECKING, Any, List, Optional, Type, Union

from . import contents, errors
from .config import config
from .helpers import markdown, Utils, Keys


if TYPE_CHECKING:
    from .site import Site
    from .contents import ContentObj


logger = logging.getLogger(__name__)


# See easel.site.contents
PageClass = Union[
    Type["Lazy"], Type["Layout"], Type["Markdown"],
]

PageObj = Union[
    "Lazy", "Layout", "Markdown",
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

        page_config: dict = Utils.load_config(path=path_page_config)

        try:
            page_type: str = page_config[Keys.TYPE]
        except KeyError as error:
            raise errors.PageConfigError(
                f"Missing required key '{Keys.TYPE}' for Page-like item in {path_absolute}."
            ) from error

        # Get Menu class based on 'menu_type'.
        Page: Optional[PageClass] = self.page_types(page_type=page_type)

        if Page is None:
            raise errors.PageConfigError(
                f"Unsupported value '{page_type}' for '{Keys.TYPE}' for "
                f"Page-like item in {path_absolute}."
            )

        return Page(site=site, path_absolute=path_absolute, config=page_config)

    def page_types(self, page_type: str) -> Optional[PageClass]:
        return self._page_types.get(page_type, None)

    def register_page_type(self, name: str, page: Any) -> None:
        """ Register new Page-like object. """
        self._page_types[name] = page


class ShowCaptionsMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def options(self) -> dict:
        pass

    @property
    def show_captions(self) -> bool:
        return self.options.get(Keys.SHOW_CAPTIONS, False)


class GalleryMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def options(self) -> dict:
        pass

    def validate__gallery_config(self) -> None:

        if not self.is_gallery:
            return

        if self.gallery_column_count == "auto" and self.gallery_column_width == "auto":
            raise errors.PageConfigError(
                f"{self}: Cannot set '{Keys.GALLERY_COLUMN_COUNT}' and "
                f"'{Keys.GALLERY_COLUMN_WIDTH}' to 'auto'."
            )

        if self.gallery_column_count not in config.VALID_GALLERY_COLUMN_COUNT:
            raise errors.PageConfigError(
                f"{self}: Unsupported value '{self.gallery_column_count}' for "
                f"'{Keys.GALLERY_COLUMN_COUNT}'."
            )

    @property
    def is_gallery(self) -> bool:
        return self.options.get(Keys.IS_GALLERY, False)

    @property
    def gallery_column_count(self) -> bool:
        return self.options.get(Keys.GALLERY_COLUMN_COUNT, None)

    @property
    def gallery_column_width(self) -> bool:
        return self.options.get(Keys.GALLERY_COLUMN_WIDTH, None)

    @property
    def gallery_column_gap(self) -> bool:
        return self.options.get(Keys.GALLERY_COLUMN_GAP, None)


class PageInterface(abc.ABC):
    def __init__(self, site: "Site", path_absolute: pathlib.Path, config: dict):

        self._site: "Site" = site
        self._path_absolute: pathlib.Path = path_absolute
        self._config: dict = config

        self.validate__options()
        self.validate__config()

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.path_relative}>"

    @property
    @abc.abstractmethod
    def contents(self) -> List["ContentObj"]:
        pass

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass

    """ TODO
    def validate__description(self) -> None:

        try:
            self.config["description"]
        except KeyError:
            self.config["description"] = None
            return

        if not self.file_description.exists():
            raise errors.MissingContent("")
    """

    def validate__options(self) -> None:

        try:
            options = self.config[Keys.OPTIONS]
        except KeyError:
            return

        if type(options) is not dict:
            raise errors.PageConfigError(
                f"{self}: Expected type 'dict' for '{Keys.OPTIONS}' got '{type(options).__name__}'."
            )

    @property
    def config(self) -> dict:
        return self._config

    @property
    def options(self) -> dict:
        """ Returns a dictionary of optional page attributes defined in
        the 'page.yaml':

            {
                "is-gallery": [bool: false],
                "gallery-column-count": [str|int: auto],
                "gallery-column-width": [str: 250px],
                Keys.SHOW_CAPTIONS: [bool: false]
            }
        """
        return self.config.get(Keys.OPTIONS, {})

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
    def file_page_yaml(self) -> pathlib.Path:
        return self._path_absolute / config.FILENAME_PAGE_YAML

    """ TODO
    @property
    def file_description(self) -> pathlib.Path:
        return self._path_absolute / self.config["description"]
    """

    @property
    def url(self) -> str:
        return Utils.slugify(self.name)

    @property
    def is_landing(self) -> bool:
        return self.config.get(Keys.IS_LANDING, False)

    @property
    def description(self) -> Optional[str]:

        path = self._path_absolute / config.FILENAME_PAGE_DESCRIPTION

        try:
            # TODO: Figure out how to properly type this.
            return markdown.from_file(filepath=path, page=self)
        except FileNotFoundError:
            return None
        except Exception as error:
            raise errors.PageConfigError(
                f"Unexpected Error while loading page description {path}."
            ) from error


class Lazy(PageInterface, GalleryMixin, ShowCaptionsMixin):
    """ Creates an Markdown Page object from a dictionary with the following
    attributes:

        {
            "type": "lazy",
        }
    """

    def validate__config(self) -> None:
        self.validate__gallery_config()

    @property
    def contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

        # pathlib.PosixPath.glob() returns a generator of pathlib.PosixPath
        # objects. Contains absolute paths of all items and sub-items in the
        # page's folder.
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
                    page=self, path=path, caption={Keys.TITLE: path.stem}
                )

            elif path.suffix in config.VALID_VIDEO_TYPES:
                item = contents.Video(
                    page=self, path=path, caption={Keys.TITLE: path.stem}
                )

            elif path.suffix in config.VALID_AUDIO_TYPES:
                item = contents.Audio(
                    page=self, path=path, caption={Keys.TITLE: path.stem}
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

        # 'VideoEmbedded' doesn't have the property 'path_absolute' however
        # we're ignoring the typing error here because 'VideoEmbedded' will
        # never show up in this list.
        items.sort(key=lambda item: item.path_absolute)  # type: ignore

        return items


class Layout(PageInterface, GalleryMixin, ShowCaptionsMixin):
    """ Creates an Markdown Page object from a dictionary with the following
    attributes:

        {
            "type": "layout",
            "contents": [list<Contents>: []],
        }
    """

    def validate__config(self) -> None:

        try:
            contents = self.config[Keys.CONTENTS]
        except KeyError as error:
            raise errors.PageConfigError(
                f"Missing required key '{Keys.CONTENTS}' in for "
                f"{self.__class__.__name__} in {config.FILENAME_PAGE_YAML}."
            ) from error
        else:
            if type(contents) is not list:
                raise errors.PageConfigError(
                    f"{self}: Expected type 'list' for '{Keys.CONTENTS}' got "
                    f"'{type(contents).__name__}'."
                )
            if not len(contents):
                logger.warning(f"{self}: Page has no contents.")

        self.validate__gallery_config()

    @property
    def contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

        for content_data in self.config[Keys.CONTENTS]:

            item: "ContentObj" = contents.content_factory.build(
                page=self, content_data=content_data
            )

            items.append(item)

        return items


class Markdown(PageInterface, GalleryMixin):
    """ Creates an Markdown Page object from a dictionary with the following
    attributes:

        {
            "type": "markdown",
        }
    """

    def validate__config(self) -> None:

        if Keys.SHOW_CAPTIONS in self.options.keys():
            logger.warning(
                f"{self}: Markdown pages do not support captions. "
                f"Ignoring '{Keys.OPTIONS}.{Keys.SHOW_CAPTIONS}'."
            )

        self.validate__gallery_config()

    @property
    def contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

        # pathlib.PosixPath.glob() returns a generator of pathlib.PosixPath
        # objects. Contains absolute paths of all items and sub-items in the
        # page's folder.
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

        # 'VideoEmbedded' doesn't have the property 'path_absolute' however
        # we're ignoring the typing error here because 'VideoEmbedded' will
        # never show up in this list.
        items.sort(key=lambda items: items.path_absolute)  # type:ignore

        return items


page_factory = _PageFactory()
