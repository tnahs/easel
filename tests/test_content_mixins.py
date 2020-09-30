import pytest

from easel.site.contents import Audio, Embedded, Image, Video
from easel.site.defaults import Key
from easel.site.errors import ContentConfigError
from easel.site.pages import PageObj


def test__CaptionsMixin__Image__valid(page_test_content_types: "PageObj") -> None:

    caption_title = "Title"
    caption_description = "Description"

    config = {
        Key.PATH: "./contents/image.jpg",
        Key.CAPTION: {
            Key.TITLE: caption_title,
            Key.DESCRIPTION: caption_description,
        },
    }

    image = Image(page=page_test_content_types, **config)

    assert image.caption_title == f"<p>{caption_title}</p>"
    assert image.caption_description == f"<p>{caption_description}</p>"
    assert image.caption_align is None


def test__CaptionsMixin__Video__valid(page_test_content_types: "PageObj") -> None:

    caption_title = "Title"
    caption_description = "Description"

    config = {
        Key.PATH: "./contents/video.mp4",
        Key.CAPTION: {
            Key.TITLE: caption_title,
            Key.DESCRIPTION: caption_description,
        },
    }

    video = Video(page=page_test_content_types, **config)

    assert video.caption_title == f"<p>{caption_title}</p>"
    assert video.caption_description == f"<p>{caption_description}</p>"
    assert video.caption_align is None


def test__CaptionsMixin__Audio__valid(page_test_content_types: "PageObj") -> None:

    caption_title = "Title"
    caption_description = "Description"

    config = {
        Key.PATH: "./contents/audio.mp3",
        Key.CAPTION: {
            Key.TITLE: caption_title,
            Key.DESCRIPTION: caption_description,
        },
    }

    audio = Audio(page=page_test_content_types, **config)

    assert audio.caption_title == f"<p>{caption_title}</p>"
    assert audio.caption_description == f"<p>{caption_description}</p>"
    assert audio.caption_align is None


def test__CaptionsMixin__Embedded__valid(page_test_content_types: "PageObj") -> None:

    caption_title = "Title"
    caption_description = "Description"

    config = {
        Key.HTML: "<tag></tag>",
        Key.CAPTION: {
            Key.TITLE: caption_title,
            Key.DESCRIPTION: caption_description,
        },
    }

    embedded = Embedded(page=page_test_content_types, **config)

    assert embedded.caption_title == f"<p>{caption_title}</p>"
    assert embedded.caption_description == f"<p>{caption_description}</p>"
    assert embedded.caption_align is None


def test__CaptionsMixin__invalid_caption_type(
    page_test_content_types: "PageObj",
) -> None:

    config = {
        Key.PATH: "./contents/image.jpg",
        Key.CAPTION: None,
    }

    with pytest.raises(ContentConfigError):
        Image(page=page_test_content_types, **config)

    config = {
        Key.PATH: "./contents/image.jpg",
        Key.CAPTION: {
            Key.TITLE: None,
        },
    }

    with pytest.raises(ContentConfigError):
        Image(page=page_test_content_types, **config)

    config = {
        Key.PATH: "./contents/image.jpg",
        Key.CAPTION: {
            Key.DESCRIPTION: None,
        },
    }

    with pytest.raises(ContentConfigError):
        Image(page=page_test_content_types, **config)


def test__CaptionsMixin__invalid_alignment(page_test_content_types: "PageObj") -> None:

    config = {
        Key.PATH: "./contents/image.jpg",
        Key.CAPTION: {
            Key.TITLE: "",
            Key.DESCRIPTION: "",
            Key.ALIGN: "invalid",
        },
    }

    with pytest.raises(ContentConfigError):
        Image(page=page_test_content_types, **config)
