import pytest

from easel.site.defaults import Key
from easel.site.errors import MenuConfigError
from easel.site.menus import MenuFactory


def test__MenuFactory__valid() -> None:

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

    for config in config:
        MenuFactory.build(config=config)


def test__MenuFactory__missing_type() -> None:

    with pytest.raises(MenuConfigError):
        MenuFactory.build(config={})


def test__MenuFactory__invalid_type() -> None:

    config = {
        "type": "invalid-type",
    }

    with pytest.raises(MenuConfigError):
        MenuFactory.build(config=config)


def test__MenuFactory__register_type() -> None:
    class CustomMenuType:
        pass

    name = "custom-menu-type"
    obj = CustomMenuType

    MenuFactory.register(name=name, obj=obj)

    assert MenuFactory.get_type(name=name) == obj
