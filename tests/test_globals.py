from easel.site.globals import Globals
from tests.test_configs import TestSites


def test__debug() -> None:

    Globals.init(root=TestSites.valid)

    Globals.debug = True
    assert Globals.debug is True

    Globals.debug = False
    assert Globals.debug is False


def test__testing() -> None:

    Globals.init(root=TestSites.valid)

    Globals.testing = True
    assert Globals.testing is True

    Globals.testing = False
    assert Globals.testing is False
