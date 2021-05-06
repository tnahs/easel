import pathlib
from typing import ClassVar, Literal, Optional, Union

from pydantic import validator

from .defaults import Extensions
from .enums import E_Content, E_Size
from .globals import Globals
from .model import BaseModel
from .utils import Utils


class Caption(BaseModel):
    title: Optional[str]
    description: Optional[str]


class File(BaseModel):
    _EXTENSIONS: ClassVar[tuple[str, ...]]

    path: pathlib.Path

    def __str__(self) -> str:
        return f"<{type(self).__name__} '{self.path.name}'>"

    @validator("path")
    def validate__supported_filetypes(cls, value: pathlib.Path) -> pathlib.Path:

        if value.suffix not in cls._EXTENSIONS:
            raise ValueError(
                f"unsupported content type: {value.name}; permitted: "
                f"{', '.join(cls._EXTENSIONS)}"
            )

        return value

    @property
    def name(self) -> str:
        """Returns the filename without the extension."""
        return self.path.stem

    @property
    def filename(self) -> str:
        """Returns the whole filename."""
        return self.path.name

    @property
    def extension(self) -> str:
        """Returns the filename's extension."""
        return self.path.suffix

    @property
    def src(self) -> pathlib.Path:
        """Returns a path relative to to /site-name."""
        return self.path.relative_to(Globals.site_root)

    @property
    def mimetype(self) -> Optional[str]:
        return Utils.get_mimetype(extension=self.extension)


class Image(File):
    _EXTENSIONS = Extensions.IMAGE

    type: Literal[E_Content.IMAGE]
    caption: Optional[Caption]


class Video(File):
    _EXTENSIONS = Extensions.VIDEO

    type: Literal[E_Content.VIDEO]
    caption: Optional[Caption]


class Audio(File):
    _EXTENSIONS = Extensions.AUDIO

    type: Literal[E_Content.AUDIO]
    caption: Optional[Caption]


class Markdown(File):
    _EXTENSIONS = Extensions.MARKDOWN

    type: Literal[E_Content.MARKDOWN]


class Embedded(BaseModel):
    type: Literal[E_Content.EMBEDDED]
    html: str

    def __str__(self):
        return f"<{type(self).__name__} '{self.html[:32].strip()}'...>"


class Header(BaseModel):
    type: Literal[E_Content.HEADER]
    text: str
    size: Optional[E_Size] = E_Size.MEDIUM

    def __str__(self):
        return f"<{type(self).__name__} '{self.text[:32].strip()}'...>"


class Break(BaseModel):
    type: Literal[E_Content.BREAK]
    size: Optional[E_Size] = E_Size.MEDIUM

    def __str__(self):
        return f"<{type(self).__name__} {self.size}>"


# https://github.com/samuelcolvin/pydantic/issues/2717
Content = Union[
    Image,
    Video,
    Audio,
    Markdown,
    Embedded,
    Header,
    Break,
]
