import copy
import datetime
import os

import pytest

from easel.site.defaults import Defaults
from easel.site.errors import ConfigLoadError
from easel.site.helpers import SafeDict, Utils
from tests.test_configs import TestYAML


# -----------------------------------------------------------------------------
# Utils.load_config
# -----------------------------------------------------------------------------


def test__load_config__valid() -> None:

    config = Utils.load_config(path=TestYAML.valid)

    assert config["data"] == "valid"


def test__load_config__invalid() -> None:

    with pytest.raises(ConfigLoadError):
        Utils.load_config(path=TestYAML.invalid)


def test__load_config__empty() -> None:

    config = Utils.load_config(path=TestYAML.empty)

    assert config == {}


def test__load_config__missing() -> None:

    with pytest.raises(ConfigLoadError):
        Utils.load_config(path=TestYAML.missing)


# -----------------------------------------------------------------------------
# Utils.str_to_bool
# -----------------------------------------------------------------------------


def test__str_to_bool() -> None:

    assert Utils.str_to_bool(value="TRUE") is True
    assert Utils.str_to_bool(value="ENABLED") is True
    assert Utils.str_to_bool(value="YES") is True
    assert Utils.str_to_bool(value="1") is True

    assert Utils.str_to_bool(value="FALSE") is False
    assert Utils.str_to_bool(value="DISABLED") is False
    assert Utils.str_to_bool(value="NO") is False
    assert Utils.str_to_bool(value="0") is False
    assert Utils.str_to_bool(value="") is False


def test__get_mimetype__valid() -> None:

    mp4 = Utils.get_mimetype(extension=".mp4")
    webm = Utils.get_mimetype(extension=".webm")
    mov = Utils.get_mimetype(extension=".mov")
    mp3 = Utils.get_mimetype(extension=".mp3")
    wav = Utils.get_mimetype(extension=".wav")

    assert mp4 == "video/mp4"
    assert webm == "video/webm"
    assert mov == "video/quicktime"
    assert mp3 == "audio/mpeg"
    assert wav == "audio/wav"


def test__get_mimetype__valid_alternate() -> None:

    mp4 = Utils.get_mimetype(extension="mp4")
    webm = Utils.get_mimetype(extension="webm")
    mov = Utils.get_mimetype(extension="mov")
    mp3 = Utils.get_mimetype(extension="mp3")
    wav = Utils.get_mimetype(extension="wav")

    assert mp4 == "video/mp4"
    assert webm == "video/webm"
    assert mov == "video/quicktime"
    assert mp3 == "audio/mpeg"
    assert wav == "audio/wav"


def test__get_mimetype__missing() -> None:

    ext = Utils.get_mimetype(extension="ext")

    assert ext is None


# -----------------------------------------------------------------------------
# Utils.str_to_datetime
# -----------------------------------------------------------------------------


def test__str_to_datetime__valid() -> None:

    date_YMD: str = f"2020{Defaults.DATE_SEPARATOR}01{Defaults.DATE_SEPARATOR}01"
    date_MDY: str = f"01{Defaults.DATE_SEPARATOR}01{Defaults.DATE_SEPARATOR}2020"
    date_DMY: str = f"01{Defaults.DATE_SEPARATOR}01{Defaults.DATE_SEPARATOR}2020"

    for date in [date_YMD, date_MDY, date_DMY]:
        datetime_date = Utils.str_to_datetime(date)
        assert datetime_date == datetime.datetime(2020, 1, 1)

    date_ISO: str = "2020-01-01 12:00:00"
    datetime_iso = Utils.str_to_datetime(date_ISO)
    assert datetime_iso == datetime.datetime(2020, 1, 1, 12, 0, 0)


def test__str_to_datetime__invalid() -> None:

    date: str = "01 01 2020"

    with pytest.raises(ValueError):
        Utils.str_to_datetime(date)


# -----------------------------------------------------------------------------
# Utils.slugify
# -----------------------------------------------------------------------------


def test__slugify() -> None:

    symbols = Utils.slugify(string="string#with%symbols!")
    spaces = Utils.slugify(string="string with spaces")
    spaces_multiple = Utils.slugify(string="  string  with  spaces  ")
    unicode_normalized = Utils.slugify(string="strịng wïth unîcödé")
    unicode_allowed = Utils.slugify(string="strịng wïth unîcödé", allow_unicode=True)

    assert symbols == "stringwithsymbols"
    assert spaces == "string-with-spaces"
    assert spaces_multiple == "string-with-spaces"
    assert unicode_normalized == "string-with-unicode"
    assert unicode_allowed == "strịng-wïth-unîcödé"


# -----------------------------------------------------------------------------
# Utils.normalize_page_path
# -----------------------------------------------------------------------------


def test__normalize_page_path() -> None:

    paths = [
        "./contents/pages/page-name",
        "/contents/pages/page-name",
        "contents/pages/page-name",
        "./pages/page-name",
        "/pages/page-name",
        "pages/page-name",
        "./page-name",
        "/page-name",
        "page-name",
    ]

    for path in paths:

        path_normalized = Utils.normalize_page_path(path=path)

        assert path_normalized == "/page-name"


# -----------------------------------------------------------------------------
# Utils.urlify
# -----------------------------------------------------------------------------


def test__urlify__valid() -> None:

    path = f"{os.sep}path{os.sep}to{os.sep}asset"

    url = Utils.urlify(path=path, leading_slash=False)
    url_slash = Utils.urlify(path=path)

    assert url == f"path{os.sep}to{os.sep}asset"
    assert url_slash == f"{os.sep}path{os.sep}to{os.sep}asset"


def test__urlify__valid_slugify() -> None:

    path = f"{os.sep}path with spaces and s#ymbo$ls{os.sep}to{os.sep}asset"

    url_slugified = Utils.urlify(path=path, slugify=True)

    assert (
        url_slugified == f"{os.sep}path-with-spaces-and-symbols{os.sep}to{os.sep}asset"
    )


# -----------------------------------------------------------------------------
# Utils.update_dict
# -----------------------------------------------------------------------------


@pytest.fixture
def original_dict() -> dict:
    return {
        "int": 0,
        "string": "string",
        "dict": {
            "int": 0,
            "string": "string",
            "dict": {
                "string": "string",
            },
            "list": [
                "string",
            ],
        },
        "list": [
            "string",
        ],
    }


def test__update_dict__whole(original_dict) -> None:

    updates = {
        "int": 999,
        "string": "updated-string",
        "dict": {
            "int": 999,
            "string": "updated-string",
            "dict": {
                "string": "updated-string",
            },
            "list": [
                "updated-string",
            ],
        },
        "list": [
            "updated-string",
        ],
    }

    updated = Utils.update_dict(original=original_dict, updates=updates)

    assert updated == updates


def test__update_dict__partial(original_dict) -> None:

    updates = {
        "dict": {
            "dict": {
                "string": "updated-string",
            },
        }
    }

    updated_expected = {
        "int": 0,
        "string": "string",
        "dict": {
            "int": 0,
            "string": "string",
            "dict": {
                # Only this line should be updated.
                "string": "updated-string",
            },
            "list": [
                "string",
            ],
        },
        "list": [
            "string",
        ],
    }

    updated02 = Utils.update_dict(original=original_dict, updates=updates)

    assert updated02 == updated_expected


def test__update_dict__extras(original_dict) -> None:

    key = "extra-dict"
    value = {
        "extra-string": "extra-string",
    }

    updates = {
        key: value,
    }

    updated_expected = copy.deepcopy(original_dict)
    updated_expected[key] = value

    updated02 = Utils.update_dict(original=original_dict, updates=updates)

    assert updated02 == updated_expected


def test__SafeDict__both() -> None:

    safe_dict = SafeDict()

    assert isinstance(safe_dict.missing_attr, SafeDict)
    assert isinstance(safe_dict["missing_item"], SafeDict)
    assert isinstance(safe_dict.missing_attr.missing_attr, SafeDict)
    assert isinstance(safe_dict["missing_item"]["missing_item"], SafeDict)
