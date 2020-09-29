import pytest

from easel.site.globals import Globals

from .test_configs import TestSites


@pytest.fixture(autouse=True)
def reset__Globals_site_paths_root():
    Globals.site_paths._root = None
    yield
    Globals.site_paths._root = None


def test__debug() -> None:

    Globals.init(root=TestSites.valid)

    Globals.debug = True
    assert Globals.debug is True

    Globals.debug = False
    assert Globals.debug is False
