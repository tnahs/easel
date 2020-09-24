import datetime
import pathlib
from typing import List, Optional

import pytest

from easel.site.contents import Audio, ContentClass, Image, TextBlock, Video
from easel.site.defaults import Key
from easel.site.globals import Globals
from easel.site.pages import Layout, LayoutGallery, Lazy, LazyGallery


root = pathlib.Path(__file__).parent / "site-testing"


Globals.init(root=root)


class PageTestConfig:
    """ Emulates a Page's 'page.yaml' without loading one. """

    is_index = True

    date = "2020-01-01"
    description = "./description.md"
    cover = "./cover.jpg"

    options = {}

    datetime_date = datetime.datetime(2020, 1, 1)
    path_description = pathlib.Path(description)
    path_cover = pathlib.Path(cover)

    def __init__(
        self,
        path: str,
        type: str,
        title: str,
        url: str,
        contents_count: int,
        contents_types: List["ContentClass"],
        contents: Optional[List[dict]] = None,
    ) -> None:

        self.path = Globals.site_paths.pages / path
        self.type = type
        self.title = title

        self.contents_count = contents_count
        self.contents_types = contents_types
        self.contents = contents if contents is not None else []

        self.url = url

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
    path="./page-lazy",
    type=Key.LAZY,
    title="PageLazy",
    url="/page-lazy",
    # Contents are generated from: ./site-testing/contents/pages/page-lazy/contents
    contents=None,
    contents_count=4,
    contents_types=[Image, Video, Audio, TextBlock],
)

test_config__lazy_gallery = PageTestConfig(
    path="./page-lazy-gallery",
    type=Key.LAZY_GALLERY,
    title="PageLazyGallery",
    url="/page-lazy-gallery",
    # Contents are generated from: ./site-testing/contents/pages/page-lazy-gallery/contents
    contents=None,
    contents_count=3,
    contents_types=[Image, Image, Image],
)


test_config__layout = PageTestConfig(
    path="./page-layout",
    type=Key.LAYOUT,
    title="PageLayout",
    url="/page-layout",
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
    ],
    contents_count=4,
    contents_types=[Image, Video, Audio, TextBlock],
)

test_config__layout_gallery = PageTestConfig(
    path="./page-layout-gallery",
    type=Key.LAYOUT_GALLERY,
    title="PageLayoutGallery",
    url="/page-layout-gallery",
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
