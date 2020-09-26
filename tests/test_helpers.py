import datetime

import pytest

from easel.site.defaults import Defaults
from easel.site.helpers import Utils


def test__valid_date_formats():

    date_YMD: str = f"2020{Defaults.DATE_SEPARATOR}01{Defaults.DATE_SEPARATOR}01"
    date_MDY: str = f"01{Defaults.DATE_SEPARATOR}01{Defaults.DATE_SEPARATOR}2020"
    date_DMY: str = f"01{Defaults.DATE_SEPARATOR}01{Defaults.DATE_SEPARATOR}2020"

    for date in [date_YMD, date_MDY, date_DMY]:
        datetime_date = Utils.str_to_datetime(date)
        assert datetime_date == datetime.datetime(2020, 1, 1)

    date_ISO: str = "2020-01-01 12:00:00"
    datetime_iso = Utils.str_to_datetime(date_ISO)
    assert datetime_iso == datetime.datetime(2020, 1, 1, 12, 0, 0)


def test__invalid_date_format():

    date: str = "01 01 2020"

    with pytest.raises(ValueError):
        Utils.str_to_datetime(date)
