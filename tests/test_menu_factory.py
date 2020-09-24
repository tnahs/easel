import pytest

from easel.site.defaults import Key
from easel.site.errors import MenuConfigError
from easel.site.menus import MenuFactory


def test__MenuFactory__valid():

    config = [
        {
            "type": Key.LINK_PAGE,
            "label": "TestLinkPage",
            "links-to": "/test-link-page",
        },
        {
            "type": Key.LINK_URL,
            "label": "TestLinkURL",
            "url": "www.test-link-url.com",
        },
        {
            "type": Key.SPACER,
        },
    ]

    for menu_config in config:
        MenuFactory.build(config=menu_config)


def test__MenuFactory__missing_type():

    config = {
        "label": "missing-type",
        "links-to": "/missing-type",
    }

    with pytest.raises(MenuConfigError):
        MenuFactory.build(config=config)


def test__MenuFactory__invalid_type():

    config = {
        "type": "invalid-type",
        "label": "invalid-type",
        "links-to": "/invalid-type",
    }

    with pytest.raises(MenuConfigError):
        MenuFactory.build(config=config)


def test__MenuFactory__register_type():
    class CustomMenuType:
        pass

    name = "custom-menu-type"
    obj = CustomMenuType

    MenuFactory.register_menu_type(name=name, menu=obj)

    assert MenuFactory.menu_types(name) == obj
