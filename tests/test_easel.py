import os

import pytest

from easel import Easel, __version__
from easel.site.defaults import Key
from easel.site.errors import SiteConfigError, ThemeConfigError
from easel.site.globals import Globals
from tests.test_configs import TestSites


def test__version() -> None:
    assert __version__ == "2.0.0-dev"


def test__Easel__valid() -> None:

    easel = Easel(TestSites.valid, loglevel="DEBUG", debug=True, testing=True)
    easel.run(watch=True)

    repr(easel)

    assert type(easel._context()) is dict
    assert Globals.debug is True
    assert Globals.testing is True


def test__Easel__valid_alternate() -> None:

    os.environ[Key.SITE_ROOT] = str(TestSites.valid)
    os.environ[Key.SITE_DEBUG] = "TRUE"
    os.environ[Key.SITE_TESTING] = "TRUE"

    easel = Easel()

    assert type(easel._context()) is dict
    assert Globals.debug is True
    assert Globals.testing is True

    del os.environ[Key.SITE_ROOT]
    del os.environ[Key.SITE_DEBUG]
    del os.environ[Key.SITE_TESTING]


def test__Easel__invalid() -> None:

    # Instantiating an Easel instance without the 'root' argument sets the
    # current directory as the site-root. This should raise a SiteConfigError
    # seeing as the testing directory isn't a valid site.
    with pytest.raises(SiteConfigError):
        Easel()

    with pytest.raises(SiteConfigError):
        Easel("./missing-site")

    with pytest.raises(SiteConfigError):
        Easel(TestSites.missing_site_yaml)


def test__Easel__filters_valid() -> None:

    easel = Easel(TestSites.valid)

    site_url = easel._filter__site_url(path="path/to/testing")
    theme_url = easel._filter__theme_url(path="path/to/testing")
    theme_css_url = easel._filter__theme_url(path="css/bundle-#.css")
    theme_js_url = easel._filter__theme_url(path="javascript/bundle-#.js")

    assert site_url == "/site/path/to/testing"
    assert theme_url == "/theme/path/to/testing"

    # ./src/easel/themes/theme-name/theme-name/css/bundle-###.css
    assert theme_css_url is not None

    # ./src/easel/themes/theme-name/theme-name/javascript/bundle-###.js
    assert theme_js_url is not None


def test__Easel__filters_invalid() -> None:

    easel = Easel(TestSites.valid)

    with pytest.raises(ThemeConfigError):
        easel._filter__theme_url(path="missing-#.css")

    with pytest.raises(ThemeConfigError):
        easel._filter__theme_url(path="missing-#.js")
