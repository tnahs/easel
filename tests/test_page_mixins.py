import pytest

from easel.site.defaults import Key
from easel.site.errors import PageConfigError
from easel.site.pages import (
    Lazy,
    LazyGallery,
    PageClass,
    PageClassGallery,
    PageClassLayout,
)

from .conftest import PageTestConfig
from .test_configs import TestSites


# -----------------------------------------------------------------------------
# LazyMixin
# -----------------------------------------------------------------------------


def test__LazyMixin__directory_contents() -> None:

    path = (
        TestSites.misc_tests
        / "contents"
        / "pages"
        / "page-test-lazy-mixin-directory-contents"
    )

    Lazy(path=path, config={})
    LazyGallery(path=path, config={})


# -----------------------------------------------------------------------------
# LayoutMixin
# -----------------------------------------------------------------------------


def run__LayoutMixin__no_contents(
    cls: "PageClassLayout", ptc: "PageTestConfig"
) -> None:
    # GLOBALFIX

    page_yaml = ptc.page_yaml.copy()
    page_yaml[Key.CONTENTS] = []

    cls(path=ptc.path, config=page_yaml)


def run__LayoutMixin__invalid_contents_type(
    cls: "PageClassLayout", ptc: "PageTestConfig"
) -> None:

    page_yaml = ptc.page_yaml.copy()
    page_yaml[Key.CONTENTS] = "invalid-type"

    with pytest.raises(PageConfigError):
        cls(path=ptc.path, config=page_yaml)


def test__LayoutMixin__no_contents(layout_pages) -> None:
    for cls, ptc in layout_pages.items():
        run__LayoutMixin__no_contents(cls=cls, ptc=ptc)


def test__LayoutMixin__invalid_contents_type(layout_pages) -> None:
    for cls, ptc in layout_pages.items():
        run__LayoutMixin__invalid_contents_type(cls=cls, ptc=ptc)


# -----------------------------------------------------------------------------
# GalleryMixin
# -----------------------------------------------------------------------------


def run__GalleryMixin__column_count_set(
    cls: "PageClassGallery", ptc: "PageTestConfig"
) -> None:
    # GLOBALFIX

    count = 3

    page_yaml = ptc.page_yaml.copy()
    page_yaml[Key.OPTIONS] = {Key.COLUMN_COUNT: count}

    page = cls(path=ptc.path, config=page_yaml)

    assert page.config.options[Key.COLUMN_COUNT] == count
    assert page.column_count == count


def run__GalleryMixin__column_count_unset(
    cls: "PageClassGallery", ptc: "PageTestConfig"
) -> None:
    # GLOBALFIX

    page = cls(path=ptc.path, config=ptc.page_yaml)

    assert page.config.options[Key.COLUMN_COUNT] is None
    assert page.column_count is None


def run__GalleryMixin__column_count_invalid_count(
    cls: "PageClassGallery", ptc: "PageTestConfig"
) -> None:

    count = 0

    page_yaml = ptc.page_yaml.copy()
    page_yaml[Key.OPTIONS] = {Key.COLUMN_COUNT: count}

    with pytest.raises(PageConfigError):
        cls(path=ptc.path, config=page_yaml)


def run__GalleryMixin__column_count_invalid_type(
    cls: "PageClassGallery", ptc: "PageTestConfig"
) -> None:

    count = []

    page_yaml = ptc.page_yaml.copy()
    page_yaml[Key.OPTIONS] = {Key.COLUMN_COUNT: count}

    with pytest.raises(PageConfigError):
        cls(path=ptc.path, config=page_yaml)


def test__GalleryMixin__column_count_set(gallery_pages) -> None:
    for cls, ptc in gallery_pages.items():
        run__GalleryMixin__column_count_set(cls=cls, ptc=ptc)


def test__GalleryMixin__column_count_unset(gallery_pages) -> None:
    for cls, ptc in gallery_pages.items():
        run__GalleryMixin__column_count_unset(cls=cls, ptc=ptc)


def test__GalleryMixin__column_count_invalid_count(gallery_pages) -> None:
    for cls, ptc in gallery_pages.items():
        run__GalleryMixin__column_count_invalid_count(cls=cls, ptc=ptc)


def test__GalleryMixin__column_count_invalid_type(gallery_pages) -> None:
    for cls, ptc in gallery_pages.items():
        run__GalleryMixin__column_count_invalid_type(cls=cls, ptc=ptc)


# -----------------------------------------------------------------------------
# ShowCaptionsMixin
# -----------------------------------------------------------------------------


def run__ShowCaptionsMixin__set(cls: "PageClass", ptc: "PageTestConfig") -> None:

    page_yaml = ptc.page_yaml.copy()
    page_yaml[Key.OPTIONS] = {Key.SHOW_CAPTIONS: True}

    page = cls(path=ptc.path, config=page_yaml)

    assert page.config.options[Key.SHOW_CAPTIONS] is True
    assert page.show_captions is True


def run__ShowCaptionsMixin__unset(cls: "PageClass", ptc: "PageTestConfig") -> None:

    page = cls(path=ptc.path, config=ptc.page_yaml)

    assert page.config.options[Key.SHOW_CAPTIONS] is False
    assert page.show_captions is False


def run__ShowCaptionsMixin__invalid_type(
    cls: "PageClass", ptc: "PageTestConfig"
) -> None:

    page_yaml = ptc.page_yaml.copy()
    page_yaml[Key.OPTIONS] = {Key.SHOW_CAPTIONS: "invalid-type"}

    with pytest.raises(PageConfigError):
        cls(path=ptc.path, config=page_yaml)


def test__ShowCaptionsMixin__set(show_captions_pages) -> None:
    for cls, ptc in show_captions_pages.items():
        run__ShowCaptionsMixin__set(cls=cls, ptc=ptc)


def test__ShowCaptionsMixin__unset(show_captions_pages) -> None:
    for cls, ptc in show_captions_pages.items():
        run__ShowCaptionsMixin__unset(cls=cls, ptc=ptc)


def test__ShowCaptionsMixin__invalid_type(show_captions_pages) -> None:
    for cls, ptc in show_captions_pages.items():
        run__ShowCaptionsMixin__invalid_type(cls=cls, ptc=ptc)
