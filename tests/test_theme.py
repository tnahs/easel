import sys

import pytest

from easel.site.errors import SiteConfigError, ThemeConfigError
from easel.site.globals import Globals
from easel.site.helpers import SafeDict
from tests.test_configs import TESTING_DATA_ROOT, TestSites


# -----------------------------------------------------------------------------
# ThemePaths
# -----------------------------------------------------------------------------


def test__invalid() -> None:

    with pytest.raises(SiteConfigError):
        Globals.theme_paths.root


def test__builtin_valid_default() -> None:

    Globals.init(root=TestSites.theme_builtin_valid_default)

    assert Globals.theme_paths.assets is not None
    assert Globals.theme_paths.template_main_html is not None
    assert Globals.theme_paths.template_404_html is not None
    assert Globals.theme_paths.static_url_path == "/theme"


def test__builtin_valid_01() -> None:

    Globals.init(root=TestSites.theme_builtin_valid_01)


def test__builtin_valid_02() -> None:

    Globals.init(root=TestSites.theme_builtin_valid_02)


def test__builtin_invalid() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.theme_builtin_invalid)


def test__installed_valid() -> None:

    theme_path = str(TESTING_DATA_ROOT / "themes-installed")

    sys.path.append(theme_path)

    Globals.init(root=TestSites.theme_installed_valid)

    sys.path.pop()


def test__installed_missing() -> None:

    theme_path = str(TESTING_DATA_ROOT / "themes-installed")

    sys.path.append(theme_path)

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.theme_installed_missing)

    sys.path.pop()


def test__custom_valid_warning() -> None:

    Globals.init(root=TestSites.theme_custom_valid_warning)


def test__custom_valid() -> None:

    Globals.init(root=TestSites.theme_custom_valid)

    # The directory for 'custom-theme' is located inside the site directory
    # for 'theme-custom-valid' at ./tests/data/sites/site-theme-custom-valid.
    assert Globals.theme_paths.root == TestSites.theme_custom_valid / "custom-theme"


def test__custom_missing() -> None:

    with pytest.raises(SiteConfigError):
        Globals.init(root=TestSites.theme_custom_missing)


def test__custom_missing_theme_yaml() -> None:

    with pytest.raises(ThemeConfigError):
        Globals.init(root=TestSites.theme_custom_missing_theme_yaml)


def test__custom_missing_main_html() -> None:

    with pytest.raises(ThemeConfigError):
        Globals.init(root=TestSites.theme_custom_missing_main_html)


def test__custom_missing_404_html() -> None:

    with pytest.raises(ThemeConfigError):
        Globals.init(root=TestSites.theme_custom_missing_404_html)


# -----------------------------------------------------------------------------
# ThemeConfig
# -----------------------------------------------------------------------------


def test__SafeDict() -> None:

    Globals.init(root=TestSites.valid)

    assert isinstance(Globals.theme_config.missing_attr, SafeDict)
    assert isinstance(Globals.theme_config["missing_item"], SafeDict)
    assert isinstance(Globals.theme_config.missing_attr.missing_attr, SafeDict)
    assert isinstance(Globals.theme_config["missing_item"]["missing_item"], SafeDict)
