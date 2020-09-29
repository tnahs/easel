from typing import Dict

import pytest

from easel.site.globals import Globals
from easel.site.pages import (
    Layout,
    LayoutGallery,
    Lazy,
    LazyGallery,
    PageClass,
    PageObj,
)

from .test_configs import (
    PageTestConfig,
    test_config__layout,
    test_config__layout_gallery,
    test_config__lazy,
    test_config__lazy_gallery,
    test_config__test_content_types,
)


# -----------------------------------------------------------------------------
# Pages in ./tests/sites/site-valid/contents/pages
# -----------------------------------------------------------------------------


@pytest.fixture(scope="session")
def all_pages() -> Dict["PageClass", "PageTestConfig"]:
    """Returns a dictionary of *all* Page classes with their respective test
    configuration. Each key:value pair referring to a page directory in
    ./tests/sites/site-valid/contents/pages.

    These are purposefully un-instantiated so that each test has the
    possibility to modify the configuration as needed to testdifferent valid
    and invalid cases."""

    return {
        Lazy: test_config__lazy,
        LazyGallery: test_config__lazy_gallery,
        Layout: test_config__layout,
        LayoutGallery: test_config__layout_gallery,
    }


@pytest.fixture(scope="session")
def lazy_pages() -> Dict["PageClass", "PageTestConfig"]:
    """Returns a dictionary of Page classes that implement 'LazyMixin' along
    with their respective test configuration.

    See 'all_pages()' above for details."""

    return {
        Lazy: test_config__lazy,
        LazyGallery: test_config__lazy_gallery,
    }


@pytest.fixture(scope="session")
def layout_pages() -> Dict["PageClass", "PageTestConfig"]:
    """Returns a dictionary of Page classes that implement 'LayoutMixin' along
    with their respective test configuration.

    See 'all_pages()' above for details."""

    return {
        Layout: test_config__layout,
        LayoutGallery: test_config__layout_gallery,
    }


@pytest.fixture(scope="session")
def gallery_pages() -> Dict["PageClass", "PageTestConfig"]:
    """Returns a dictionary of Page classes that implement 'GalleryMixin' along
    with their respective test configuration.

    See 'all_pages()' above for details."""

    return {
        LazyGallery: test_config__lazy_gallery,
        LayoutGallery: test_config__layout_gallery,
    }


@pytest.fixture(scope="session")
def show_captions_pages() -> Dict["PageClass", "PageTestConfig"]:
    """Returns a dictionary of Page classes that implement 'ShowCaptionsMixin'
    along with their respective test configuration.

    See 'all_pages()' above for details."""

    return {
        Lazy: test_config__lazy,
        LazyGallery: test_config__lazy_gallery,
        Layout: test_config__layout,
        LayoutGallery: test_config__layout_gallery,
    }


# -----------------------------------------------------------------------------
# Pages in ./tests/sites/site-misc-tests/contents/pages
# -----------------------------------------------------------------------------


@pytest.fixture(scope="session")
def page_test_content_types() -> "PageObj":
    """Returns an instantiated Layout page referring to the page directory in
    ./tests/sites/site-misc-tests/contents/pages/page-test-content-types. This
    is primarily used to test Content-like object creation. It's a dummy page
    to pass in when a Content-like object is instantiated."""

    """ NOTE: Creating Content-like objects *requires* 'Globals.init()' to be
    called (which essentially sets 'Globals.site_paths.root'). This is because
    Content-like objects that implement 'File' must be able return their path
    relative to the site. However Menu-like and Page-like objects can be
    created without calling the 'Globals.init()'. """

    Globals.init(root=test_config__test_content_types.site)

    return Layout(
        path=test_config__test_content_types.path,
        config=test_config__test_content_types.page_yaml,
    )
