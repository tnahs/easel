import abc
import logging
import pathlib
from typing import TYPE_CHECKING, Any, Generator, List, Optional, Type, Union

from . import contents, errors
from . import global_config
from .helpers import Key, Utils


if TYPE_CHECKING:
    from .site import Site
    from .contents import ContentObj, Image, Audio, Video, TextBlock


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
            "lazy": Lazy,
            "layout": Layout,
            "lazy-gallery": LazyGallery,
            "layout-gallery": LayoutGallery,
        }

    def build(self, site: "Site", path_absolute: pathlib.Path) -> PageObj:
        """ Builds Page-like object from a path. """

        path_page_config: pathlib.Path = path_absolute / global_config.FILENAME_PAGE_YAML

        page_config: dict = Utils.load_config(path=path_page_config)

        try:
            page_type: str = page_config[Key.TYPE]
        except KeyError as error:
            raise errors.PageConfigError(
                f"Missing required key '{Key.TYPE}' for Page-like item in {path_absolute}."
            ) from error

        # Get Menu class based on 'menu_type'.
        Page: Optional[PageClass] = self.page_types(page_type=page_type)

        if Page is None:
            raise errors.PageConfigError(
                f"Unsupported value '{page_type}' for '{Key.TYPE}' for "
                f"Page-like item in {path_absolute}."
            )

        return Page(site=site, path_absolute=path_absolute, config=page_config)

    def page_types(self, page_type: str) -> Optional[PageClass]:
        return self._page_types.get(page_type, None)

    def register_page_type(self, name: str, page: Any) -> None:
        """ Register new Page-like object. """
        self._page_types[name] = page


class PageInterface(abc.ABC):
    def __init__(self, site: "Site", path_absolute: pathlib.Path, config: dict):

        self._site: "Site" = site
        self._path_absolute: pathlib.Path = path_absolute

        self._config = PageConfig(page=self, data=config)

        self.validate__config()

        """ TEMP/NOTE/FIXME: To properly validate and generate placeholder
        images for Gallery Pages, self.contents needs to be called before the
        site is run. It would probably a good idea to cache the contents to
        reduce overhead on a page refresh. This needs a slight redesign. """
        self.contents

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.path_relative}>"

    def __str__(self):
        return f"{self.__class__.__name__}: {self.path_relative}"

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
    def name(self) -> str:
        return self._path_absolute.stem

    @property
    def path_absolute(self) -> pathlib.Path:
        return self._path_absolute

    @property
    def path_relative(self) -> pathlib.Path:
        """ Returns path relative to to /[site]. """
        return self._path_absolute.relative_to(global_config.path_site)

    @property
    def url(self) -> str:
        return Utils.slugify(self.name)

    # TODO: Properly implement 'cover' and 'description'.

    @property
    def cover(self) -> pathlib.Path:
        return self.path_relative / self.config.cover

    @property
    def description(self) -> pathlib.Path:
        return self.path_relative / self.config.description


class PageConfig:
    """ Creates a PageConfig object from a dictionary with the following
    attributes:

        {
            "is-index": [bool: false],
            "type": [str: page-type],  // See _PageFactory.page_types
            "title": [str: title],
            "cover": [str: path/to/cover],
            "description": [str: path/to/description],
            "options: [dict: options],
        }
    """

    def __init__(self, page: "PageInterface", data: dict):

        self._page = page
        self._data: dict = data

        self._validate()

    def _validate(self) -> None:
        self._validate__options()

    def _validate__options(self) -> None:

        try:
            options = self._data[Key.OPTIONS]
        except KeyError:
            return

        if type(options) is not dict:
            raise errors.PageConfigError(
                f"{self}: Expected type 'dict' for '{Key.OPTIONS}' got "
                f"'{type(options).__name__}'."
            )

    @property
    def data(self) -> dict:
        """ Returns the raw config data dict. Used to access configurations
        not common to all Pages. For example: LayoutMixin._contents """
        return self._data

    @property
    def type(self) -> bool:
        return self._data[Key.TYPE]

    @property
    def is_index(self) -> bool:
        return self._data.get(Key.IS_INDEX, False)

    @property
    def title(self) -> str:
        return self._data.get(Key.TITLE, "")

    # TODO: Properly implement 'cover' and 'description'.

    @property
    def cover(self) -> pathlib.Path:
        return pathlib.Path(self._data.get(Key.COVER, ""))

    @property
    def description(self) -> pathlib.Path:
        return pathlib.Path(self._data.get(Key.DESCRIPTION, ""))

    @property
    def options(self) -> dict:
        """ Returns a dictionary of optional attributes declared in Page's
        config file. See PageInterface subclasses Lazy LazyGallery Layout
        LayoutGallery for specifics. """
        return self._data.get(Key.OPTIONS, {})


class LazyMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def config(self) -> "PageConfig":
        pass

    @property
    @abc.abstractmethod
    def path_absolute(self) -> pathlib.Path:
        pass

    def validate__lazy_config(self) -> None:
        pass

    @property
    def _contents(self) -> Generator[pathlib.Path, None, None]:
        """ Returns the contents of the Page's root directory. Primarily used
        for creating Content objects to populate the Page. """

        for path in self.path_absolute.glob("**/*"):

            # Ignore directories.
            if path.is_dir():
                continue

            # Ignore hidden files.
            if path.name.startswith("."):
                continue

            if path.name == global_config.FILENAME_PAGE_YAML:
                continue

            # TODO: Properly implement 'cover' and 'description'.
            if path.name == self.config.description.name:
                continue

            if path.suffix not in global_config.VALID_CONTENT_EXTENSIONS:
                logger.warning(f"Unsupported file '{path.name}' found in {self}.")
                continue

            if path.suffix in global_config.VALID_YAML_EXTENSIONS:
                logger.warning(f"Unused YAML file '{path.name}' found in {self}.")
                continue

            yield path


class LayoutMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def config(self) -> "PageConfig":
        pass

    def validate__layout_config(self) -> None:

        try:
            contents = self.config.data[Key.CONTENTS]
        except KeyError as error:
            raise errors.PageConfigError(
                f"Missing required key '{Key.CONTENTS}' in for "
                f"{self.__class__.__name__} in {global_config.FILENAME_PAGE_YAML}."
            ) from error
        else:
            if type(contents) is not list:
                raise errors.PageConfigError(
                    f"{self}: Expected type 'list' for '{Key.CONTENTS}' got "
                    f"'{type(contents).__name__}'."
                )
            if not len(contents):
                logger.warning(f"{self}: Page has no contents.")

    @property
    def _contents(self) -> List[dict]:
        """ Returns the content items declared in the Page's config file.
        Primarily used for creating Content objects to populate the Page. """
        return self.config.data[Key.CONTENTS]


class GalleryMixin(abc.ABC):

    is_gallery = True  # QUESTION: Is there a better way to do this?

    @property
    @abc.abstractmethod
    def config(self) -> "PageConfig":
        pass

    def validate__gallery_config(self) -> None:

        if self.column_count == "auto" and self.column_width == "auto":
            raise errors.PageConfigError(
                f"{self}: Cannot set '{Key.COLUMN_COUNT}' and "
                f"'{Key.COLUMN_WIDTH}' to 'auto'."
            )

        if (
            self.column_count is not None
            and self.column_count not in global_config.VALID_COLUMN_COUNT
        ):
            raise errors.PageConfigError(
                f"{self}: Unsupported value '{self.column_count}' for "
                f"'{Key.COLUMN_COUNT}'."
            )

    @property
    def column_count(self) -> bool:
        return self.config.options.get(Key.COLUMN_COUNT, None)

    @property
    def column_width(self) -> bool:
        return self.config.options.get(Key.COLUMN_WIDTH, None)


class ShowCaptionsMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def config(self) -> "PageConfig":
        pass

    def validate__show_captions_config(self) -> None:

        try:
            show_captions = self.config.options[Key.SHOW_CAPTIONS]
        except KeyError:
            return

        if type(show_captions) is not bool:
            raise errors.PageConfigError(
                f"{self}: Expected type 'bool' for '{Key.SHOW_CAPTIONS}' "
                f"got '{type(show_captions).__name__}'."
            )

    @property
    def show_captions(self) -> bool:
        return self.config.options.get(Key.SHOW_CAPTIONS, False)


class Lazy(PageInterface, LazyMixin, ShowCaptionsMixin):
    """ Creates an Lazy Page object from a dictionary with the following
    attributes:

        {
            "type": "lazy",
            "options: {
                "show-captions": [bool: false],
            }
        }
    """

    def validate__config(self) -> None:
        self.validate__lazy_config()
        self.validate__show_captions_config()

    @property
    def contents(self) -> List[Union["Image", "Video", "Audio", "TextBlock"]]:

        items: List[Union["Image", "Video", "Audio", "TextBlock"]] = []

        for path in self._contents:

            if path.suffix in global_config.VALID_IMAGE_EXTENSIONS:
                item = contents.Image(
                    page=self, path=path, caption={Key.TITLE: path.stem}
                )

            elif path.suffix in global_config.VALID_VIDEO_EXTENSIONS:
                item = contents.Video(
                    page=self, path=path, caption={Key.TITLE: path.stem}
                )

            elif path.suffix in global_config.VALID_AUDIO_EXTENSIONS:
                item = contents.Audio(
                    page=self, path=path, caption={Key.TITLE: path.stem}
                )

            elif path.suffix in global_config.VALID_TEXT_EXTENSIONS:
                item = contents.TextBlock(page=self, path=path)

            else:
                continue

            items.append(item)

        items.sort(key=lambda item: item.path_absolute)

        return items


class LazyGallery(PageInterface, LazyMixin, GalleryMixin, ShowCaptionsMixin):
    """ Creates an LazyGallery Page object from a dictionary with the following
    attributes:

        {
            "type": "lazy-gallery",
            "options": {
                "column-count": [str|int: auto],
                "column-width": [str: 250px],
                "show-captions": [bool: false],
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

        for path in self._contents:

            if path.suffix not in global_config.VALID_IMAGE_EXTENSIONS:
                logger.warning(f"Unsupported file '{path.name}' found in {self}.")
                continue

            image: "Image" = contents.Image(page=self, path=path)

            images.append(image)

        images.sort(key=lambda item: item.path_absolute)

        return images


class Layout(PageInterface, LayoutMixin, ShowCaptionsMixin):
    """ Creates an Layout Page object from a dictionary with the following
    attributes:

        {
            "type": "layout",
            "contents": [list<ContentObj>: []],
            "options: {
                "show-captions": [bool: false],
            }
        }
    """

    def validate__config(self) -> None:
        self.validate__layout_config()
        self.validate__show_captions_config()

    @property
    def contents(self) -> List["ContentObj"]:

        items: List["ContentObj"] = []

        for config in self._contents:

            # fmt:off
            item: "ContentObj" = contents.content_factory.build(page=self, config=config)
            # fmt:on

            items.append(item)

        return items


class LayoutGallery(PageInterface, LayoutMixin, GalleryMixin, ShowCaptionsMixin):
    """ Creates an LayoutGallery Page object from a dictionary with the following
    attributes:

        {
            "type": "layout-gallery",
            "contents": [list<Images>: []],
            "options": {
                "column-count": [str|int: auto],
                "column-width": [str: 250px],
                "show-captions": [bool: false],
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

        for config in self._contents:

            image: "Image" = contents.Image(page=self, config=config)

            images.append(image)

        return images


page_factory = _PageFactory()
