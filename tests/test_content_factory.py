import pytest

from easel.site.contents import ContentFactory
from easel.site.defaults import Key
from easel.site.errors import ContentConfigError
from easel.site.pages import PageObj


def test__ContentFactory__valid(page_test_content_types: "PageObj") -> None:
    # GLOBALFIX

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
        ContentFactory.build(page=page_test_content_types, config=config)


def test__ContentFactory__missing_type(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        ContentFactory.build(page=page_test_content_types, config={})


def test__ContentFactory__invalid_type(page_test_content_types: "PageObj") -> None:

    config = {
        "type": "invalid-type",
    }

    with pytest.raises(ContentConfigError):
        ContentFactory.build(page=page_test_content_types, config=config)


def test__ContentFactory__register_type() -> None:
    class CustomContentType:
        pass

    name = "custom-content-type"
    obj = CustomContentType

    ContentFactory.register(name=name, obj=obj)

    assert ContentFactory.get_type(name=name) == obj
