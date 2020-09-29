import pytest

from easel.site import Site
from easel.site.defaults import Key
from easel.site.errors import Error, SiteConfigError
from easel.site.globals import Globals

from .test_configs import TestSites


@pytest.fixture(autouse=True)
def reset__Globals_site_paths_root():
    Globals.site_paths._root = None
    yield
    Globals.site_paths._root = None


# -----------------------------------------------------------------------------
# Site
# -----------------------------------------------------------------------------


def test__valid() -> None:

    Globals.init(root=TestSites.valid)

    site = Site()
    site.build()

    repr(site)

    assert site.index is not None

    assert site.get_page("page-layout") is not None
    assert site.get_page("page-layout-gallery") is not None
    assert site.get_page("page-lazy") is not None
    assert site.get_page("page-lazy-gallery") is not None

    assert site.get_page("page-missing") is None

    assert site.config.title == "Testing Title"
    assert site.config.author == "Testing Author"
    assert site.config.copyright == "Testing Copyright"
    assert site.config.description == "Testing Description"
    assert site.config.favicon == "./testing-favicon.ico"

    assert site.config.header == {
        Key.TITLE: {
            Key.LABEL: "Testing Header Title Label",
            Key.IMAGE: "./testing-header-title-image.jpg",
        },
    }

    assert Globals.site_paths.static_url_path == "/site"


def test__not_built() -> None:

    Globals.init(root=TestSites.valid)

    site = Site()

    with pytest.raises(Error):
        site.pages

    with pytest.raises(Error):
        site.menu

    with pytest.raises(Error):
        site.index


def test__rebuild_cache() -> None:

    Globals.init(root=TestSites.valid)

    site = Site()
    site.build()
    site.rebuild_cache()


def test__config_menu_empty() -> None:

    Globals.init(root=TestSites.config_menu_empty)

    site = Site()
    site.build()

    assert site.menu == []


def test__config_menu_missing_page() -> None:

    Globals.init(root=TestSites.config_menu_missing_page)

    site = Site()

    with pytest.raises(SiteConfigError):
        site.build()


def test__index_missing() -> None:

    Globals.init(root=TestSites.index_missing)

    site = Site()

    with pytest.raises(SiteConfigError):
        site.build()


def test__index_overload() -> None:

    Globals.init(root=TestSites.index_overload)

    site = Site()

    with pytest.raises(SiteConfigError):
        site.build()


# -----------------------------------------------------------------------------
# SitePaths
# -----------------------------------------------------------------------------


def test__SitePaths__root_not_set() -> None:

    with pytest.raises(SiteConfigError):
        Globals.site_paths.root


def test__SitePaths__root_missing() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root="/path/to/missing-site")


def test__SitePaths__assets() -> None:

    Globals.init(root=TestSites.valid)

    Globals.site_paths.assets


def test__SitePaths__missing_site_yaml() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.missing_site_yaml)


def test__SitePaths__contents_directory_missing() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.contents_directory_missing)


def test__SitePaths__pages_directory_missing() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.pages_directory_missing)


def test__SitePaths__pages_directory_empty() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.pages_directory_empty)


# -----------------------------------------------------------------------------
# SiteConfig
# -----------------------------------------------------------------------------


def test__SiteConfig__config_menu_type_invalid() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.config_menu_type_invalid)


def test__SiteConfig__config_header_type_invalid() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.config_header_type_invalid)


def test__SiteConfig__config_theme_type_invalid() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.config_theme_type_invalid)
