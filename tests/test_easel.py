import pytest

from easel import Easel, __version__
from easel.site.errors import ThemeConfigError
from easel.site.globals import Globals

from .test_configs import TestSites


@pytest.fixture(autouse=True)
def reset__Globals_site_paths_root():
    Globals.site_paths._root = None
    yield
    Globals.site_paths._root = None


def test__version() -> None:
    assert __version__ == "2.0.0-dev"


def test__Easel__valid() -> None:

    easel = Easel(TestSites.valid, loglevel="DEBUG", debug=True, testing=True)
    easel.run(watch=True)

    repr(easel)

    assert type(easel._context()) is dict
    assert Globals.debug is True
    assert Globals.testing is True


def test__Easel__filters_valid() -> None:

    easel = Easel(TestSites.valid)

    site_url = easel._filter__site_url(path="path/to/testing")
    theme_url = easel._filter__theme_url(path="path/to/testing")
    theme_css_url = easel._filter__theme_url(path="css/bundle-#.css")
    theme_js_url = easel._filter__theme_url(path="javascript/bundle-#.js")

    assert site_url == "/site/path/to/testing"
    assert theme_url == "/theme/path/to/testing"
    assert theme_css_url is not None
    assert theme_js_url is not None


def test__Easel__filters_invalid() -> None:

    easel = Easel(TestSites.valid)

    with pytest.raises(ThemeConfigError):
        easel._filter__theme_url(path="missing-#.css")

    with pytest.raises(ThemeConfigError):
        easel._filter__theme_url(path="missing-#.js")
