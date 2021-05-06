import abc
import datetime
import glob
import logging
import pathlib
from typing import Any, Iterator, Literal, Optional, Union

from pydantic import validator

from .contents import Audio, Caption, Content, Image, Markdown, Video
from .defaults import Extensions
from .enums import E_Content, E_Filename, E_Page
from .model import BaseModel


logger = logging.getLogger(__name__)


class PageOptions(BaseModel):
    show_captions: bool = False
    column_count: Optional[int]


class BasePage(BaseModel):

    path: pathlib.Path
    index: Optional[bool] = False
    title: str
    date: Optional[datetime.date]
    description: Optional[pathlib.Path]
    cover: Optional[pathlib.Path]
    contents: Optional[list[Content]] = []
    options: Optional[PageOptions]

    def __str__(self) -> str:
        return f"<{type(self).__name__} '{self.title}'>"

    @validator("description", "cover")
    def validate__description_and_cover_exist(
        cls, value: Optional[pathlib.Path], values: dict[str, Any]
    ):

        if value is None:
            return

        root: pathlib.Path = values.get("path")  # type: ignore
        path = root / value
        path = path.resolve()

        if not path.exists():
            raise ValueError(f"{value.name} does not exist")

        return path

    @validator("contents")
    def validate__content_files_exist(
        cls, contents: Optional[list[Content]], values: dict[str, Any]
    ):

        for content in contents:

            try:
                path_file = content.path  # type: ignore
            except AttributeError:
                continue

            root: pathlib.Path = values.get("path")  # type: ignore
            path = root / path_file
            path = path.resolve()

            if not path.exists():
                raise ValueError(f"{path_file.name} does not exist")

            content.path = path

        return contents

    @property
    def valid_directory_contents(self) -> Iterator[pathlib.Path]:
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
        valid_paths = (
            pathlib.Path(path)
            for path in glob.iglob(f"{self.path}/**/*", recursive=True)
        )

        for path in valid_paths:

            # Ignore directories and symlinks.
            if path.is_dir() or path.is_symlink():
                continue

            # Ignore 'private' files.
            if path.name.startswith("_") or path.name.startswith("."):
                continue

            if path.name == E_Filename.PAGE_YAML:
                continue

            if self.cover is not None:
                if path.name == self.cover.name:
                    continue

            if self.description is not None:
                if path.name == self.description.name:
                    continue

            if path.suffix in Extensions.YAML:
                logger.warning(f"Unused YAML file '{path.name}' found in {self}.")
                continue

            if path.suffix not in Extensions.CONTENT:
                logger.warning(f"Unsupported file '{path.name}' found in {self}.")
                continue

            yield path


class PageAuto(BasePage):
    type: Literal[E_Page.AUTO]

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.contents = sorted(
            list(self.compile_contents()),
            key=lambda content: content.path,  # type: ignore
        )

    def compile_contents(self) -> Iterator[Content]:

        for path in self.valid_directory_contents:

            if path.suffix in Extensions.IMAGE:
                yield Image(
                    path=path,
                    type=E_Content.IMAGE.value,
                    caption=Caption(
                        title=path.stem,
                    ),
                )

            if path.suffix in Extensions.VIDEO:
                yield Video(
                    path=path,
                    type=E_Content.VIDEO.value,
                    caption=Caption(
                        title=path.stem,
                    ),
                )

            if path.suffix in Extensions.AUDIO:
                yield Audio(
                    path=path,
                    type=E_Content.AUDIO.value,
                    caption=Caption(
                        title=path.stem,
                    ),
                )

            if path.suffix in Extensions.MARKDOWN:
                yield Markdown(
                    path=path,
                    type=E_Content.MARKDOWN.value,
                    caption=Caption(
                        title=path.stem,
                    ),
                )


class PageAutoGallery(BasePage):
    type: Literal[E_Page.AUTO_GALLERY]

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.contents = sorted(
            list(self.compile_contents()),
            key=lambda content: content.path,  # type: ignore
        )

    def compile_contents(self) -> Iterator[Content]:

        for path in self.valid_directory_contents:

            if path.suffix in Extensions.IMAGE:
                yield Image(
                    path=path,
                    type=E_Content.IMAGE.value,
                    caption=Caption(
                        title=path.stem,
                    ),
                )


class PageLayout(BasePage):
    type: Literal[E_Page.LAYOUT]


class PageLayoutGallery(BasePage):
    type: Literal[E_Page.LAYOUT_GALLERY]


Page = Union[
    PageAuto,
    PageAutoGallery,
    PageLayout,
    PageLayoutGallery,
]
