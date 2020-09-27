import pytest

from easel.site.errors import PageConfigError
from easel.site.globals import Globals
from easel.site.pages import PageFactory

from .test_configs import TestSites


def test__PageFactory__valid() -> None:

    Globals.init(root=TestSites.valid)

    for path in Globals.site_paths.iter_pages():
        PageFactory.build(path=path)


def test__PageFactory__missing_type() -> None:

    path = TestSites.misc_tests / "contents" / "pages" / "page-test-page-type-missing"

    with pytest.raises(PageConfigError):
        PageFactory.build(path=path)


def test__PageFactory__invalid_type() -> None:

    path = TestSites.misc_tests / "contents" / "pages" / "page-test-page-type-invalid"

    with pytest.raises(PageConfigError):
        PageFactory.build(path=path)


def test__PageFactory__register_type() -> None:
    class CustomPageType:
        pass

    name = "custom-page-type"
    obj = CustomPageType

    PageFactory.register(name=name, obj=obj)

    assert PageFactory.get_type(name=name) == obj
