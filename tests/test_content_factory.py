import pytest

from easel.site.contents import ContentFactory
from easel.site.defaults import Key
from easel.site.errors import ContentConfigError
from easel.site.globals import Globals
from easel.site.pages import Layout, PageObj

from .conftest import PageTestConfig


@pytest.fixture
def page() -> "PageObj":
    ptc = PageTestConfig(
        # ./tests/site-testing/contents/other-pages/test-contents
        path=(Globals.site_paths.contents / "other-pages" / "test-contents")
    )

    return Layout(path=ptc.path, config=ptc.page_yaml)


def test__MenuFactory__valid(page):

    contents = [
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
    ]

    for config in contents:
        ContentFactory.build(page=page, config=config)


def test__MenuFactory__missing_type(page):

    with pytest.raises(ContentConfigError):
        ContentFactory.build(page=page, config={})


def test__MenuFactory__invalid_type(page):

    config = {
        "type": "invalid-type",
    }

    with pytest.raises(ContentConfigError):
        ContentFactory.build(page=page, config=config)


def test__MenuFactory__register_type():
    class CustomContentType:
        pass

    name = "custom-content-type"
    obj = CustomContentType

    ContentFactory.register(name=name, obj=obj)

    assert ContentFactory.get_type(name=name) == obj
