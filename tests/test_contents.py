import pytest

from easel.site.contents import Audio, Break, Embedded, Header, Image, TextBlock, Video
from easel.site.contents.contents import File
from easel.site.defaults import Key
from easel.site.errors import ContentConfigError, MissingFile, UnsupportedContentType
from easel.site.globals import Globals
from easel.site.pages import PageObj


# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------


def test__File__valid(page_test_content_types: "PageObj") -> None:
    # GLOBALFIX

    file_name = "file"
    file_extension = ".ext"
    file_filename = f"{file_name}{file_extension}"
    file_path = f"./{file_filename}"
    # ./contents/pages/page-name/filename
    file_src = (
        page_test_content_types.path.relative_to(Globals.site_paths.root)
        / file_filename
    )

    file_config = {
        Key.PATH: file_path,
    }

    file = File(page=page_test_content_types, **file_config)

    repr(file)

    assert file.name == file_name
    assert file.filename == file_filename
    assert file.extension == file_extension
    assert file.path == page_test_content_types.path / file_path
    assert file.src == file_src


def test__File__missing_path(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        File(page=page_test_content_types)

    with pytest.raises(ContentConfigError):
        File(page=page_test_content_types, **{})


def test__File__invalid_path_type(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        File(page=page_test_content_types, path=42)

    with pytest.raises(ContentConfigError):
        File(page=page_test_content_types, path=None)


def test__File__blank_path(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        File(page=page_test_content_types, path="")


def test__File__missing_file(page_test_content_types: "PageObj") -> None:

    with pytest.raises(MissingFile):
        File(page=page_test_content_types, path="missing-file.ext")


def test__File__unsupported_content_type(page_test_content_types: "PageObj") -> None:

    with pytest.raises(UnsupportedContentType):
        Image(page=page_test_content_types, path="./file.ext")

    with pytest.raises(UnsupportedContentType):
        Video(page=page_test_content_types, path="./file.ext")

    with pytest.raises(UnsupportedContentType):
        Audio(page=page_test_content_types, path="./file.ext")

    with pytest.raises(UnsupportedContentType):
        TextBlock(page=page_test_content_types, path="./file.ext")


# -----------------------------------------------------------------------------
# Image
# -----------------------------------------------------------------------------


def test__Image__valid(page_test_content_types: "PageObj") -> None:
    # GLOBALFIX

    image = Image(page=page_test_content_types, path="./contents/image.jpg")

    assert image.mimetype is None

    # TODO:LOW This needs re-visiting once Proxies are re-worked.
    assert image.proxy_images is not None
    assert image.proxy_colors is not None


# -----------------------------------------------------------------------------
# Audio
# -----------------------------------------------------------------------------


def test__Audio__mimetype(page_test_content_types: "PageObj") -> None:

    mp3 = Audio(page=page_test_content_types, path="./contents/audio.mp3")
    wav = Audio(page=page_test_content_types, path="./contents/audio.wav")

    assert mp3.mimetype == "audio/mpeg"
    assert wav.mimetype == "audio/wav"


# -----------------------------------------------------------------------------
# Video
# -----------------------------------------------------------------------------


def test__Video__mimetypes(page_test_content_types: "PageObj") -> None:

    mp4 = Video(page=page_test_content_types, path="./contents/video.mp4")
    webm = Video(page=page_test_content_types, path="./contents/video.webm")
    mov = Video(page=page_test_content_types, path="./contents/video.mov")

    assert mp4.mimetype == "video/mp4"
    assert webm.mimetype == "video/webm"
    assert mov.mimetype == "video/quicktime"


# -----------------------------------------------------------------------------
# TextBlock
# -----------------------------------------------------------------------------


def test__TextBlock__valid(page_test_content_types: "PageObj") -> None:
    # GLOBALFIX

    config = {
        Key.PATH: "./contents/text-block.md",
        Key.ALIGN: None,
    }

    text_block = TextBlock(page=page_test_content_types, **config)

    assert text_block.body == "<h1>TextBlock</h1>"
    assert text_block.align is None
    assert text_block.mimetype is None


def test__TextBlock__invalid_alignment(page_test_content_types: "PageObj") -> None:

    config = {
        Key.PATH: "./contents/text-block.md",
        Key.ALIGN: "invalid",
    }

    with pytest.raises(ContentConfigError):
        TextBlock(page=page_test_content_types, **config)


# -----------------------------------------------------------------------------
# Embedded
# -----------------------------------------------------------------------------


def test__Embedded__valid(page_test_content_types: "PageObj") -> None:

    embedded_html = "<tag></tag>"

    config = {
        Key.HTML: embedded_html,
    }

    embedded = Embedded(page=page_test_content_types, **config)

    repr(embedded)

    assert embedded.html == embedded_html


def test__Embedded__missing_html(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        Embedded(page=page_test_content_types)

    with pytest.raises(ContentConfigError):
        Embedded(page=page_test_content_types, **{})


def test__Embedded__invalid_html_type(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        Embedded(page=page_test_content_types, html=24)

    with pytest.raises(ContentConfigError):
        Embedded(page=page_test_content_types, html=None)


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------


def test__Header__valid(page_test_content_types: "PageObj") -> None:

    header_text = "Header Text"

    config = {
        Key.TEXT: header_text,
        Key.SIZE: None,
        Key.ALIGN: None,
    }

    header = Header(page=page_test_content_types, **config)

    repr(header)

    assert header.text == header_text
    assert header.size is None
    assert header.align is None


def test__Header__missing_text(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        Header(page=page_test_content_types)

    with pytest.raises(ContentConfigError):
        Header(page=page_test_content_types, **{})


def test__Header__invalid_text_type(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        Header(page=page_test_content_types, text=24)

    with pytest.raises(ContentConfigError):
        Header(page=page_test_content_types, text=None)


def test__Header__invalid_size(page_test_content_types: "PageObj") -> None:

    config = {
        Key.TEXT: "Header Text",
        Key.SIZE: "invalid",
    }

    with pytest.raises(ContentConfigError):
        Header(page=page_test_content_types, **config)


def test__Header__invalid_align(page_test_content_types: "PageObj") -> None:

    config = {
        Key.TEXT: "Header Text",
        Key.ALIGN: "invalid",
    }

    with pytest.raises(ContentConfigError):
        Header(page=page_test_content_types, **config)


# -----------------------------------------------------------------------------
# Break
# -----------------------------------------------------------------------------


def test__Break__break(page_test_content_types: "PageObj") -> None:

    break_ = Break(page=page_test_content_types)

    repr(break_)

    assert break_.size is None


def test__Break__invalid_size(page_test_content_types: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        Break(page=page_test_content_types, size="invalid")
