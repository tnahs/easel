import abc
import datetime
import logging
import pathlib
from typing import TYPE_CHECKING, List, Optional, Union

from ..contents import Audio, ContentFactory, Image, TextBlock, Video
from ..defaults import Defaults, Key
from ..errors import MissingFile, PageConfigError
from ..helpers import Utils
from .mixins import GalleryMixin, LayoutMixin, LazyMixin, ShowCaptionsMixin


if TYPE_CHECKING:
    from ..contents import ContentObj


logger = logging.getLogger(__name__)


class AbstractPage(abc.ABC):
    def __init__(self, path: pathlib.Path, config: dict):

        self._path = path

        self._config = PageConfig(page=self, config=config)

        self._date: Optional[datetime.datetime] = None
        self._description: Optional["TextBlock"] = None
        self._cover: Optional["Image"] = None

        self.validate__config()

        self._validate_build__date()
        self._validate_build__description()
        self._validate_build__cover()

        # TODO:LOW Revisit how building page contents is implemented.
        self._contents: List["ContentObj"] = self.build__contents()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.directory_name}>"

    @abc.abstractmethod
    def validate__config(self) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def build__contents(self) -> List["ContentObj"]:
        pass  # pragma: no cover

    @property
    def config(self) -> "PageConfig":
        return self._config

    @property
    def contents(self) -> List["ContentObj"]:
        return self._contents

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
        return self._date

    @property
    def description(self) -> Optional["TextBlock"]:
        return self._description

    @property
    def cover(self) -> Optional["Image"]:
        return self._cover

    def _validate_build__date(self) -> None:

        if self.config.date is None:
            return
        elif type(self.config.date) is str:
            date = Utils.str_to_datetime(date=self.config.date)
        else:
            date = self.config.date

        self._date = date

    def _validate_build__description(self) -> None:

        if self.config.description is None:
            return

        path = self.path / self.config.description

        try:
            path = path.resolve(strict=True)
        except FileNotFoundError as error:
            raise MissingFile(f"Missing description {path} for {self}.") from error

        self._description = TextBlock(page=self, path=path)

    def _validate_build__cover(self) -> None:

        if self.config.cover is None:
            return

        path = self.path / self.config.cover

        try:
            path = path.resolve(strict=True)
        except FileNotFoundError as error:
            raise MissingFile(f"Missing cover {path} for {self}.") from error

        self._cover = Image(page=self, path=path)


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
            # TODO:MED Should 'PageConfig' contain these options?
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
            raise PageConfigError(
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
    def date(self) -> Optional[Union[datetime.datetime, str]]:
        # YAML can parse some date formats hence the return type.
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

    def build__contents(self) -> List[Union["Image", "Video", "Audio", "TextBlock"]]:

        items: List[Union["Image", "Video", "Audio", "TextBlock"]] = []

        for path in self._directory_contents:

            if path.suffix in Defaults.VALID_IMAGE_EXTENSIONS:
                item = Image(page=self, path=path, caption={Key.TITLE: path.stem})

            elif path.suffix in Defaults.VALID_VIDEO_EXTENSIONS:
                item = Video(page=self, path=path, caption={Key.TITLE: path.stem})

            elif path.suffix in Defaults.VALID_AUDIO_EXTENSIONS:
                item = Audio(page=self, path=path, caption={Key.TITLE: path.stem})

            elif path.suffix in Defaults.VALID_TEXT_EXTENSIONS:
                item = TextBlock(page=self, path=path)

            else:
                continue  # pragma: no cover

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

    def build__contents(self) -> List["Image"]:

        images: List["Image"] = []

        for path in self._directory_contents:

            if path.suffix not in Defaults.VALID_IMAGE_EXTENSIONS:
                logger.warning(f"Unsupported file '{path.name}' found in {self}.")
                continue

            image = Image(page=self, path=path)

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

    def build__contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

        for config in self.config.contents:

            item = ContentFactory.build(page=self, config=config)

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

    def build__contents(self) -> List["Image"]:

        images: List["Image"] = []

        for config in self.config.contents:

            image = Image(page=self, **config)

            images.append(image)

        return images
