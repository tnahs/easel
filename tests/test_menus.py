import pytest

from easel.site.defaults import Defaults
from easel.site.errors import MenuConfigError
from easel.site.menus import LinkPage, LinkURL, Spacer


def test__LinkPage__valid() -> None:

    config = {
        "label": "TestLinkPage",
        "links-to": "/test-link-page",
    }

    link_page = LinkPage(**config)

    repr(link_page)

    assert link_page.label == "TestLinkPage"
    assert link_page.links_to == "/test-link-page"
    assert link_page.url == "/test-link-page"


def test__LinkPage__normalize_page_path() -> None:

    normalized_page_path = "/test-link-page"

    config_00 = {
        "label": "TestLinkPage",
        "links-to": "./contents/pages/test-link-page",
    }

    config_01 = {
        "label": "TestLinkPage",
        "links-to": "./pages/test-link-page",
    }

    config_01 = {
        "label": "TestLinkPage",
        "links-to": "./test-link-page",
    }

    link_page_00 = LinkPage(**config_00)
    link_page_01 = LinkPage(**config_01)
    link_page_02 = LinkPage(**config_01)

    assert link_page_00.links_to == normalized_page_path
    assert link_page_01.links_to == normalized_page_path
    assert link_page_02.links_to == normalized_page_path


def test__LinkPage__missing_config() -> None:

    config_01 = {
        "label": "TestLinkPage",
    }

    config_02 = {
        "links-to": "/test-link-page",
    }

    with pytest.raises(MenuConfigError):
        LinkPage()

    with pytest.raises(MenuConfigError):
        LinkPage(**config_01)

    with pytest.raises(MenuConfigError):
        LinkPage(**config_02)


def test__LinkURL__valid() -> None:

    config = {
        "label": "TestLinkURL",
        "url": "www.test-link-url.com",
    }

    link_url = LinkURL(**config)

    repr(link_url)

    assert link_url.label == "TestLinkURL"
    assert link_url.url == "www.test-link-url.com"


def test__LinkURL__missing_config() -> None:

    config_01 = {
        "label": "TestLinkPage",
    }

    config_02 = {
        "url": "www.test-link-url.com",
    }

    with pytest.raises(MenuConfigError):
        LinkURL()

    with pytest.raises(MenuConfigError):
        LinkURL(**config_01)

    with pytest.raises(MenuConfigError):
        LinkURL(**config_02)


def test__Spacer__valid() -> None:

    config = {
        "label": "TestSpacer",
        "size": Defaults.DEFAULT_SIZE,
    }

    spacer = Spacer(**config)

    repr(spacer)

    assert spacer.label == "TestSpacer"
    assert spacer.size == Defaults.DEFAULT_SIZE


def test__Spacer__valid_default() -> None:

    spacer_default = Spacer()

    repr(spacer_default)

    assert spacer_default.label == None
    assert spacer_default.size == None


def test__Spacer__invalid_size() -> None:

    config_01 = {
        "size": "invalid-size",
    }

    with pytest.raises(MenuConfigError):
        Spacer(**config_01)
