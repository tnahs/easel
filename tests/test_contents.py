import pytest

from easel.site.contents import Audio, Break, Embedded, Header, Image, TextBlock, Video
from easel.site.contents.contents import File
from easel.site.defaults import Key
from easel.site.errors import ContentConfigError, MissingFile, UnsupportedContentType
from easel.site.globals import Globals
from easel.site.pages import Layout, PageObj

from .conftest import PageTestConfig


# TODO:LOW This fixture is share between 'test_content*.py' files...
@pytest.fixture
def page() -> "PageObj":
    ptc = PageTestConfig(
        # ./tests/site-testing/contents/other-pages/test-contents
        path=(Globals.site_paths.contents / "other-pages" / "test-contents")
    )

    return Layout(path=ptc.path, config=ptc.page_yaml)


# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------


def test__File__valid(page: "PageObj") -> None:

    file_name = "file"
    file_extension = ".ext"
    file_filename = f"{file_name}{file_extension}"
    file_path = f"./{file_filename}"
    # ./contents/pages/page-name/filename
    file_src = page.path.relative_to(Globals.site_paths.root) / file_filename

    file_config = {
        Key.PATH: file_path,
    }

    file = File(page=page, **file_config)

    repr(file)

    assert file.name == file_name
    assert file.filename == file_filename
    assert file.extension == file_extension
    assert file.path == page.path / file_path
    assert file.src == file_src


def test__File__missing_path(page: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        File(page=page)

    with pytest.raises(ContentConfigError):
        File(page=page, **{})


def test__File__invalid_path_type(page: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        File(page=page, path=42)

    with pytest.raises(ContentConfigError):
        File(page=page, path=None)


def test__File__blank_path(page: "PageObj") -> None:

    with pytest.raises(ContentConfigError):
        File(page=page, path="")


def test__File__missing_file(page: "PageObj") -> None:

    with pytest.raises(MissingFile):
        File(page=page, path="missing-file.ext")


def test__File__unsupported_content_type(page: "PageObj") -> None:

    with pytest.raises(UnsupportedContentType):
        Image(page=page, path="./file.ext")

    with pytest.raises(UnsupportedContentType):
        Audio(page=page, path="./file.ext")

    with pytest.raises(UnsupportedContentType):
        Video(page=page, path="./file.ext")

    with pytest.raises(UnsupportedContentType):
        TextBlock(page=page, path="./file.ext")


# -----------------------------------------------------------------------------
# Image
# -----------------------------------------------------------------------------


def test__Image__valid(page: "PageObj") -> None:

    image = Image(page=page, path="./contents/image.jpg")

    assert image.mimetype is None

    # TODO:LOW This needs re-visiting once Proxies are re-worked.
    assert image.proxy_images is not None
    assert image.proxy_colors is not None


# -----------------------------------------------------------------------------
# Audio
# -----------------------------------------------------------------------------


def test__Audio__mimetype(page: "PageObj") -> None:

    mp3 = Audio(page=page, path="./contents/audio.mp3")
    wav = Audio(page=page, path="./contents/audio.wav")

    assert mp3.mimetype == "audio/mpeg"
    assert wav.mimetype == "audio/wav"


# -----------------------------------------------------------------------------
# Video
# -----------------------------------------------------------------------------


def test__Video__mimetypes(page: "PageObj") -> None:

    mp4 = Video(page=page, path="./contents/video.mp4")
    webm = Video(page=page, path="./contents/video.webm")
    mov = Video(page=page, path="./contents/video.mov")

    assert mp4.mimetype == "video/mp4"
    assert webm.mimetype == "video/webm"
    assert mov.mimetype == "video/quicktime"


# -----------------------------------------------------------------------------
# TextBlock
# -----------------------------------------------------------------------------


def test__TextBlock__text_block(page: "PageObj") -> None:

    config = {
        Key.PATH: "./contents/text-block.md",
        Key.ALIGN: None,
    }

    text_block = TextBlock(page=page, **config)

    assert text_block.body == "<h1>TextBlock</h1>"
    assert text_block.align is None
    assert text_block.mimetype is None


def test__TextBlock__invalid_alignment(page: "PageObj") -> None:

    config = {
        Key.PATH: "./contents/text-block.md",
        Key.ALIGN: "invalid",
    }

    with pytest.raises(ContentConfigError):
        TextBlock(page=page, **config)


# -----------------------------------------------------------------------------
# Embedded
# -----------------------------------------------------------------------------


def test__Embedded__valid(page) -> None:

    embedded_html = "<tag></tag>"

    config = {
        Key.HTML: embedded_html,
    }

    embedded = Embedded(page=page, **config)

    repr(embedded)

    assert embedded.html == embedded_html


def test__Embedded__missing_html(page) -> None:

    with pytest.raises(ContentConfigError):
        Embedded(page=page)

    with pytest.raises(ContentConfigError):
        Embedded(page=page, **{})


def test__Embedded__invalid_html_type(page) -> None:

    with pytest.raises(ContentConfigError):
        Embedded(page=page, html=24)

    with pytest.raises(ContentConfigError):
        Embedded(page=page, html=None)


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------


def test__Header__valid(page) -> None:

    header_text = "Header Text"

    config = {
        Key.TEXT: header_text,
        Key.SIZE: None,
        Key.ALIGN: None,
    }

    header = Header(page=page, **config)

    repr(header)

    assert header.text == header_text
    assert header.size is None
    assert header.align is None


def test__Header__missing_text(page) -> None:

    with pytest.raises(ContentConfigError):
        Header(page=page)

    with pytest.raises(ContentConfigError):
        Header(page=page, **{})


def test__Header__invalid_text_type(page) -> None:

    with pytest.raises(ContentConfigError):
        Header(page=page, text=24)

    with pytest.raises(ContentConfigError):
        Header(page=page, text=None)


def test__Header__invalid_size(page) -> None:

    config = {
        Key.TEXT: "Header Text",
        Key.SIZE: "invalid",
    }

    with pytest.raises(ContentConfigError):
        Header(page=page, **config)


def test__Header__invalid_align(page) -> None:

    config = {
        Key.TEXT: "Header Text",
        Key.ALIGN: "invalid",
    }

    with pytest.raises(ContentConfigError):
        Header(page=page, **config)


# -----------------------------------------------------------------------------
# Break
# -----------------------------------------------------------------------------


def test__Break__break(page) -> None:

    break_ = Break(page=page)

    repr(break_)

    assert break_.size is None


def test__Break__invalid_size(page) -> None:

    with pytest.raises(ContentConfigError):
        Break(page=page, size="invalid")
