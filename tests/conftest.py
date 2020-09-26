import datetime
import pathlib
from typing import List, Optional, Union

import pytest

from easel.site.contents import (
    Audio,
    Break,
    ContentClass,
    Embedded,
    Header,
    Image,
    TextBlock,
    Video,
)
from easel.site.defaults import Key
from easel.site.globals import Globals
from easel.site.pages import Layout, LayoutGallery, Lazy, LazyGallery


root = pathlib.Path(__file__).parent / "site-testing"


Globals.init(root=root)


class PageTestConfig:
    """ Emulates a Page's 'page.yaml' without loading one. """

    def __init__(
        self,
        path: Union[pathlib.Path, str],
        type: Optional[str] = None,
        is_index: Optional[bool] = None,
        title: Optional[str] = None,
        date: Optional[str] = None,
        description: Optional[str] = None,
        cover: Optional[str] = None,
        contents: Optional[List[dict]] = None,
        contents_count: Optional[int] = None,
        contents_types: Optional[List["ContentClass"]] = None,
        options: Optional[dict] = None,
        url: Optional[str] = None,
    ) -> None:

        self.path = pathlib.Path(path)
        self.type = type
        self.title = title

        self.contents_count = contents_count
        self.contents_types = contents_types
        self.contents = contents if contents is not None else []

        self.is_index = is_index
        self.date = date
        self.description = description
        self.cover = cover
        self.options = options if options is not None else {}

        self.url = url

    @property
    def datetime_date(self) -> Optional[datetime.datetime]:

        if self.date is None:
            return

        return datetime.datetime.strptime(self.date, "%Y-%m-%d")

    @property
    def path_description(self) -> Optional[pathlib.Path]:
        if self.description is None:
            return

        return pathlib.Path(self.description)

    @property
    def path_cover(self) -> Optional[pathlib.Path]:
        if self.cover is None:
            return

        return pathlib.Path(self.cover)

    @property
    def page_yaml(self) -> dict:
        return {
            Key.IS_INDEX: self.is_index,
            Key.TYPE: self.type,
            Key.TITLE: self.title,
            Key.DATE: self.date,
            Key.DESCRIPTION: self.description,
            Key.COVER: self.cover,
            Key.CONTENTS: self.contents,
            Key.OPTIONS: self.options,
        }


test_config__lazy = PageTestConfig(
    path=Globals.site_paths.pages / "page-lazy",
    type=Key.LAZY,
    is_index=False,
    title="PageLazy",
    date="2020-01-01",
    description="./description.md",
    cover="./cover.jpg",
    # Contents are generated from: ./site-testing/contents/pages/page-lazy/contents
    contents=None,
    contents_count=4,
    contents_types=[Image, Video, Audio, TextBlock],
    url="/page-lazy",
)

test_config__lazy_gallery = PageTestConfig(
    path=Globals.site_paths.pages / "page-lazy-gallery",
    type=Key.LAZY_GALLERY,
    is_index=False,
    title="PageLazyGallery",
    date="2020-01-01",
    description="./description.md",
    cover="./cover.jpg",
    # Contents are generated from: ./site-testing/contents/pages/page-lazy-gallery/contents
    contents=None,
    contents_count=3,
    contents_types=[Image, Image, Image],
    url="/page-lazy-gallery",
)


test_config__layout = PageTestConfig(
    path=Globals.site_paths.pages / "page-layout",
    type=Key.LAYOUT,
    is_index=False,
    title="PageLayout",
    date="2020-01-01",
    description="./description.md",
    cover="./cover.jpg",
    contents=[
        {
            Key.TYPE: Key.IMAGE,
            Key.PATH: "./contents/image.jpg",
        },
        {
            Key.TYPE: Key.VIDEO,
            Key.PATH: "./contents/video.mp4",
        },
        {
            Key.TYPE: Key.AUDIO,
            Key.PATH: "./contents/audio.mp3",
        },
        {
            Key.TYPE: Key.TEXT_BLOCK,
            Key.PATH: "./contents/text-block.md",
        },
        {
            Key.TYPE: Key.EMBEDDED,
            Key.HTML: "<tag></tag>",
        },
        {
            Key.TYPE: Key.HEADER,
            Key.TEXT: "Header Text",
        },
        {
            Key.TYPE: Key.BREAK,
        },
    ],
    contents_count=7,
    contents_types=[
        Image,
        Video,
        Audio,
        TextBlock,
        Embedded,
        Header,
        Break,
    ],
    url="/page-layout",
)

test_config__layout_gallery = PageTestConfig(
    path=Globals.site_paths.pages / "page-layout-gallery",
    type=Key.LAYOUT_GALLERY,
    is_index=False,
    title="PageLayoutGallery",
    date="2020-01-01",
    description="./description.md",
    cover="./cover.jpg",
    contents=[
        {
            Key.TYPE: Key.IMAGE,
            Key.PATH: "./contents/image-01.jpg",
        },
        {
            Key.TYPE: Key.IMAGE,
            Key.PATH: "./contents/image-02.jpg",
        },
        {
            Key.TYPE: Key.IMAGE,
            Key.PATH: "./contents/image-03.jpg",
        },
    ],
    contents_count=3,
    contents_types=[Image, Image, Image],
    url="/page-layout-gallery",
)


@pytest.fixture(scope="session")
def all_pages():
    return {
        Lazy: test_config__lazy,
        LazyGallery: test_config__lazy_gallery,
        Layout: test_config__layout,
        LayoutGallery: test_config__layout_gallery,
    }


@pytest.fixture(scope="session")
def lazy_pages():
    return {
        Lazy: test_config__lazy,
        LazyGallery: test_config__lazy_gallery,
    }


@pytest.fixture(scope="session")
def gallery_pages():
    return {
        LazyGallery: test_config__lazy_gallery,
        LayoutGallery: test_config__layout_gallery,
    }


@pytest.fixture(scope="session")
def layout_pages():
    return {
        Layout: test_config__layout,
        LayoutGallery: test_config__layout_gallery,
    }


@pytest.fixture(scope="session")
def show_captions_pages():
    return {
        Lazy: test_config__lazy,
        LazyGallery: test_config__lazy_gallery,
        Layout: test_config__layout,
        LayoutGallery: test_config__layout_gallery,
    }
