import abc
import glob
import logging
import pathlib
from typing import TYPE_CHECKING, Generator

from .. import errors
from ..defaults import Defaults, Key


if TYPE_CHECKING:
    from .pages import PageConfig


logger = logging.getLogger(__name__)


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

        Ideally we'd use pathlib here, but when recursing with
        Path.glob("**/*"), we get every single item including those inside
        hidden directories.

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
            if path.name.startswith("_") or path.name.startswith("."):
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
