import pytest

from easel.site import Site
from easel.site.errors import ConfigLoadError, Error, SiteConfigError
from easel.site.globals import Globals

from .test_configs import TestSites


def test__Site__valid() -> None:

    Globals.init(root=TestSites.valid)

    site = Site()
    site.build()

    repr(site)

    assert site.index is not None

    assert site.get_page("page-layout") is not None
    assert site.get_page("page-layout-gallery") is not None
    assert site.get_page("page-lazy") is not None
    assert site.get_page("page-lazy-gallery") is not None

    assert site.get_page("page-non-existant") is None


def test__Site__not_built() -> None:

    Globals.init(root=TestSites.valid)

    site = Site()

    with pytest.raises(Error):
        site.pages

    with pytest.raises(Error):
        site.menu

    with pytest.raises(Error):
        site.index


def test__Site__rebuild_cache() -> None:

    Globals.init(root=TestSites.valid)

    site = Site()
    site.build()
    site.rebuild_cache()


def test__Site__missing_site_yaml() -> None:

    with pytest.raises(ConfigLoadError):
        Globals.init(root=TestSites.missing_site_yaml)


def test__Site__contents_directory_missing() -> None:

    Globals.init(root=TestSites.contents_directory_missing)

    with pytest.raises(SiteConfigError):
        Globals.site_paths.contents


def test__Site__pages_directory_missing() -> None:

    Globals.init(root=TestSites.pages_directory_missing)

    with pytest.raises(SiteConfigError):
        Globals.site_paths.pages


def test__Site__pages_directory_empty() -> None:

    Globals.init(root=TestSites.pages_directory_empty)

    site = Site()

    with pytest.raises(SiteConfigError):
        site.build()


def test__Site__menu_empty() -> None:

    Globals.init(root=TestSites.menu_empty)

    site = Site()
    site.build()

    assert site.menu == []


def test__Site__menu_type_invalid() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.menu_type_invalid)


def test__Site__menu_missing_page() -> None:

    Globals.init(root=TestSites.menu_missing_page)

    site = Site()

    with pytest.raises(SiteConfigError):
        site.build()


def test__Site__index_missing() -> None:

    Globals.init(root=TestSites.index_missing)

    site = Site()

    with pytest.raises(SiteConfigError):
        site.build()


def test__Site__index_overload() -> None:

    Globals.init(root=TestSites.index_overload)

    site = Site()

    with pytest.raises(SiteConfigError):
        site.build()
