import abc
import datetime
import glob
import logging
import pathlib
from typing import TYPE_CHECKING, Any, Generator, List, Optional, Type, Union

from . import contents, errors
from .defaults import Defaults, Key
from .helpers import Utils
from .markdown import markdown


if TYPE_CHECKING:
    from . import Site
    from .contents import Audio, ContentObj, Image, TextBlock, Video


logger = logging.getLogger(__name__)


# See easel.site.contents
PageClass = Union[
    Type["Lazy"], Type["Layout"], Type["LazyGallery"], Type["LayoutGallery"],
]

PageObj = Union[
    "Lazy", "Layout", "LazyGallery", "LayoutGallery",
]


class _PageFactory:
    def __init__(self):
        self._page_types = {
            Key.LAZY: Lazy,
            Key.LAYOUT: Layout,
            Key.LAZY_GALLERY: LazyGallery,
            Key.LAYOUT_GALLERY: LayoutGallery,
        }

    def build(self, site: "Site", path: pathlib.Path) -> PageObj:
        """ Builds Page-like object from a path. """

        path_page_config: pathlib.Path = path / Defaults.FILENAME_PAGE_YAML

        page_config: dict = Utils.load_config(path=path_page_config)

        try:
            page_type: str = page_config[Key.TYPE]
        except KeyError as error:
            raise errors.PageConfigError(
                f"Missing required key '{Key.TYPE}' for Page-like item in {path}."
            ) from error

        # Get Page class based on 'page_type'.
        Page: Optional["PageClass"] = self.page_types(page_type=page_type)

        if Page is None:
            raise errors.PageConfigError(
                f"Unsupported value '{page_type}' for '{Key.TYPE}' for "
                f"Page-like item in {path}."
            )

        return Page(site=site, path=path, config=page_config)

    def page_types(self, page_type: str) -> Optional["PageClass"]:
        return self._page_types.get(page_type, None)

    def register_page_type(self, name: str, page: Any) -> None:
        """ Register new Page-like object. """
        self._page_types[name] = page


class AbstractPage(abc.ABC):
    def __init__(self, site: "Site", path: pathlib.Path, config: dict):

        self._site = site
        self._path = path

        self._config = PageConfig(page=self, config=config)

        self.validate__config()

        """ TODO:LOW To properly validate and generate proxies, self.contents
        needs to be called before the site is run. It would probably a good
        idea to cache the contents to reduce overhead on a page refresh. This
        needs a slight re-design. """
        self.contents

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.directory_name}>"

    def __str__(self):
        return f"{self.__class__.__name__}: {self.directory_name}"

    @property
    @abc.abstractmethod
    def contents(self) -> List["ContentObj"]:
        pass

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass

    @property
    def config(self) -> "PageConfig":
        return self._config

    @property
    def directory_name(self) -> str:
        return self._path.name

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @property
    def url(self) -> str:
        return Utils.urlify(self.directory_name)

    @property
    def is_index(self) -> bool:
        return self.config.is_index

    @property
    def title(self) -> Optional[str]:
        return self.config.title

    @property
    def date(self) -> Optional[datetime.datetime]:

        if self.config.date is None:
            return

        try:
            date = datetime.datetime.strptime(self.config.date, Defaults.DATE_FORMAT)
        except ValueError as error:
            raise errors.PageConfigError(
                f"Unsupported value '{self.config.date}' for {Key.DATE}. "
                f"Dates must be formatted as '{Defaults.DATE_FORMAT_PRETTY}'."
            ) from error

        return date

    @property
    def description(self) -> Optional[str]:

        if self.config.description is None:
            return

        path = self.path / self.config.description

        try:
            path = path.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.MissingContent(
                f"Missing description {path} for {self}."
            ) from error

        return markdown.from_file(filepath=path)

    @property
    def cover(self) -> Optional[pathlib.Path]:

        if self.config.cover is None:
            return

        path = self.path / self.config.cover

        try:
            path = path.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.MissingContent(f"Missing cover {path} for {self}.") from error

        return path


class PageConfig:
    """Creates a PageConfig object from a dictionary with the following
    attributes:

        {
            "is-index": [bool: False],
            "type": [str?: None],
            "title": [str?: None],
            "date": [str?: None],
            "description": [str?: None],
            "cover": [str?: None],
            "contents": [list: []],
            "options: {
                "show-captions": [bool: False],
                "column-count": [str?|int?: None],
            },

        }

    All page configuration is accessed through this class. The reason being
    that it's easier to implement mixins by declaring one abstract method
    'config' that returns a 'PageConfig' object rather than a bunch of
    different attributes."""

    # fmt:off
    _config_default = {
        Key.IS_INDEX: False,
        Key.TYPE: None,
        Key.TITLE: None,
        Key.DATE: None,
        Key.COVER: None,
        Key.DESCRIPTION: None,
        Key.CONTENTS: [],
        Key.OPTIONS: {
            Key.SHOW_CAPTIONS: False,
            Key.COLUMN_COUNT: None,
        },
    }
    # fmt:on

    def __init__(self, page: "AbstractPage", config: dict):

        self._page = page
        self._config_user: dict = config

        self._validate()

        self.__config: dict = Utils.update_dict(
            original=self._config_default, updates=self._config_user
        )

    def _validate(self) -> None:
        self._validate__options()

    def _validate__options(self) -> None:

        try:
            options = self._config_user[Key.OPTIONS]
        except KeyError:
            return

        if type(options) is not dict:
            raise errors.PageConfigError(
                f"{self}: Expected type 'dict' for '{Key.OPTIONS}' got "
                f"'{type(options).__name__}'."
            )

    @property
    def type(self) -> bool:
        return self.__config[Key.TYPE]

    @property
    def is_index(self) -> bool:
        return self.__config[Key.IS_INDEX]

    @property
    def title(self) -> Optional[str]:
        return self.__config[Key.TITLE]

    @property
    def date(self) -> str:
        return self.__config[Key.DATE]

    @property
    def description(self) -> Optional[pathlib.Path]:

        description = self.__config[Key.DESCRIPTION]

        try:
            return pathlib.Path(description)
        except TypeError:
            return None

    @property
    def cover(self) -> Optional[pathlib.Path]:

        cover = self.__config[Key.COVER]

        try:
            return pathlib.Path(cover)
        except TypeError:
            return None

    @property
    def contents(self) -> list:
        return self.__config[Key.CONTENTS]

    @property
    def options(self) -> dict:
        """Returns a dictionary of optional attributes declared in Page's
        config file. See AbstractPage subclasses Lazy LazyGallery Layout
        LayoutGallery for specifics."""
        return self.__config[Key.OPTIONS]


class LazyMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def config(self) -> "PageConfig":
        pass

    @property
    @abc.abstractmethod
    def path(self) -> pathlib.Path:
        pass

    def validate__lazy_config(self) -> None:

        if not len(list(self._directory_contents)):
            logger.warning(f"{self}: Page has no contents.")

    @property
    def _directory_contents(self) -> Generator[pathlib.Path, None, None]:
        """Returns the contents of the Page's root directory. Primarily used
        for creating Content objects to populate the Page.

        NOTE: The glob module ignores the contents of hidden directories as
        well as hidden files. Note that 'hidden' here means those which start
        with a dot. This makes it really convenient to hide whole directories
        inside Page's directory.

        Ideally we'd use pathlib here, but when recursing with Path.glob("**"),
        we get every single item including those inside hidden directories.

        https://docs.python.org/3/library/glob.html"""

        # Create a generator and feed it using iglob which returns an iterator.
        visible_paths = (
            pathlib.Path(visible_path)
            for visible_path in glob.iglob(f"{self.path}/**", recursive=True)
        )

        for path in visible_paths:

            # Ignore directories and symlinks.
            if path.is_dir() or path.is_symlink():
                continue

            # Ignore 'private' files.
            if path.name.startswith("_"):
                continue

            if path.name == Defaults.FILENAME_PAGE_YAML:
                continue

            if self.config.cover is not None:
                if path.name == self.config.cover.name:
                    continue

            if self.config.description is not None:
                if path.name == self.config.description.name:
                    continue

            if path.suffix not in Defaults.VALID_CONTENT_EXTENSIONS:
                logger.warning(f"Unsupported file '{path.name}' found in {self}.")
                continue

            if path.suffix in Defaults.VALID_YAML_EXTENSIONS:
                logger.warning(f"Unused YAML file '{path.name}' found in {self}.")
                continue

            yield path


class LayoutMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def config(self) -> "PageConfig":
        pass

    def validate__layout_config(self) -> None:

        contents = self.config.contents

        if type(contents) is not list:
            raise errors.PageConfigError(
                f"{self}: Expected type 'list' for '{Key.CONTENTS}' got "
                f"'{type(contents).__name__}'."
            )

        if not len(contents):
            logger.warning(f"{self}: Page has no contents.")


class GalleryMixin(abc.ABC):

    is_gallery: bool = True

    @property
    @abc.abstractmethod
    def config(self) -> "PageConfig":
        pass

    def validate__gallery_config(self) -> None:

        if (
            self.column_count is not None
            and self.column_count not in Defaults.VALID_COLUMN_COUNT
        ):
            raise errors.PageConfigError(
                f"{self}: Unsupported value '{self.column_count}' for "
                f"'{Key.COLUMN_COUNT}'."
            )

    @property
    def column_count(self) -> bool:
        return self.config.options[Key.COLUMN_COUNT]


class ShowCaptionsMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def config(self) -> "PageConfig":
        pass

    def validate__show_captions_config(self) -> None:

        show_captions = self.config.options[Key.SHOW_CAPTIONS]

        if type(show_captions) is not bool:
            raise errors.PageConfigError(
                f"{self}: Expected type 'bool' for '{Key.SHOW_CAPTIONS}' "
                f"got '{type(show_captions).__name__}'."
            )

    @property
    def show_captions(self) -> bool:
        return self.config.options.get(Key.SHOW_CAPTIONS, False)


class Lazy(AbstractPage, LazyMixin, ShowCaptionsMixin):
    """Creates an Lazy Page object from a dictionary with the following
    attributes:

        {
            "type": "lazy",
            "options: {
                "show-captions": [bool: False],
            }
        }
    """

    def validate__config(self) -> None:
        self.validate__lazy_config()
        self.validate__show_captions_config()

    @property
    def contents(self) -> List[Union["Image", "Video", "Audio", "TextBlock"]]:

        items: List[Union["Image", "Video", "Audio", "TextBlock"]] = []

        for path in self._directory_contents:

            if path.suffix in Defaults.VALID_IMAGE_EXTENSIONS:
                item = contents.Image(
                    page=self, path=path, caption={Key.TITLE: path.stem}
                )

            elif path.suffix in Defaults.VALID_VIDEO_EXTENSIONS:
                item = contents.Video(
                    page=self, path=path, caption={Key.TITLE: path.stem}
                )

            elif path.suffix in Defaults.VALID_AUDIO_EXTENSIONS:
                item = contents.Audio(
                    page=self, path=path, caption={Key.TITLE: path.stem}
                )

            elif path.suffix in Defaults.VALID_TEXT_EXTENSIONS:
                item = contents.TextBlock(page=self, path=path)

            else:
                continue

            items.append(item)

        items.sort(key=lambda item: item.path)

        return items


class LazyGallery(AbstractPage, LazyMixin, GalleryMixin, ShowCaptionsMixin):
    """Creates an LazyGallery Page object from a dictionary with the following
    attributes:

        {
            "type": "lazy-gallery",
            "options": {
                "show-captions": [bool: False],
                "column-count": [str?|int?: None],
            }
        }
    """

    def validate__config(self) -> None:
        self.validate__lazy_config()
        self.validate__gallery_config()
        self.validate__show_captions_config()

    @property
    def contents(self) -> List["Image"]:

        images: List["Image"] = []

        for path in self._directory_contents:

            if path.suffix not in Defaults.VALID_IMAGE_EXTENSIONS:
                logger.warning(f"Unsupported file '{path.name}' found in {self}.")
                continue

            image: "Image" = contents.Image(page=self, path=path)

            images.append(image)

        images.sort(key=lambda item: item.path)

        return images


class Layout(AbstractPage, LayoutMixin, ShowCaptionsMixin):
    """Creates an Layout Page object from a dictionary with the following
    attributes:

        {
            "type": "layout",
            "contents": [list: []],
            "options: {
                "show-captions": [bool: False],
            }
        }
    """

    def validate__config(self) -> None:
        self.validate__layout_config()
        self.validate__show_captions_config()

    @property
    def contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

        for config in self.config.contents:

            item = contents.content_factory.build(page=self, config=config)

            items.append(item)

        return items


class LayoutGallery(AbstractPage, LayoutMixin, GalleryMixin, ShowCaptionsMixin):
    """Creates an LayoutGallery Page object from a dictionary with the following
    attributes:

        {
            "type": "layout-gallery",
            "contents": [list: []],
            "options": {
                "show-captions": [bool: False],
                "column-count": [str?|int?: None],
            }
        }
    """

    def validate__config(self) -> None:
        self.validate__layout_config()
        self.validate__gallery_config()
        self.validate__show_captions_config()

    @property
    def contents(self) -> List["Image"]:

        images: List["Image"] = []

        for config in self.config.contents:

            image = contents.Image(page=self, config=config)

            images.append(image)

        return images


page_factory = _PageFactory()
