import pathlib
from typing import Literal, Optional, Union

from pydantic import HttpUrl

from .enums import E_Menu, E_Size
from .model import BaseModel


class LinkPage(BaseModel):
    type: Literal[E_Menu.LINK_PAGE]
    label: Optional[str]
    path: pathlib.Path


class LinkURL(BaseModel):
    type: Literal[E_Menu.LINK_URL]
    label: Optional[str]
    url: HttpUrl


class Spacer(BaseModel):
    type: Literal[E_Menu.SPACER]
    label: Optional[str]
    size: Optional[E_Size] = E_Size.MEDIUM


Menu = Union[LinkPage, LinkURL, Spacer]
