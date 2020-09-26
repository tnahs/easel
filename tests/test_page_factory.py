import pytest

from easel.site.errors import PageConfigError
from easel.site.globals import Globals
from easel.site.pages import PageFactory


OTHER_PAGES = Globals.site_paths.contents / "other-pages"


def test__PageFactory__valid():

    for path in Globals.site_paths.iter_pages():
        PageFactory.build(path=path)


def test__PageFactory__missing_type():

    path = OTHER_PAGES / "test-missing-type"

    with pytest.raises(PageConfigError):
        PageFactory.build(path=path)


def test__PageFactory__invalid_type():

    path = OTHER_PAGES / "test-invalid-type"

    with pytest.raises(PageConfigError):
        PageFactory.build(path=path)


def test__PageFactory__register_type():
    class CustomPageType:
        pass

    name = "custom-page-type"
    obj = CustomPageType

    PageFactory.register(name=name, obj=obj)

    assert PageFactory.get_type(name=name) == obj
