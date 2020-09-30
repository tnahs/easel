import pytest

from easel.site.contents import ContentClass, Image, TextBlock
from easel.site.errors import MissingFile, PageConfigError
from easel.site.globals import Globals
from easel.site.pages import PageClass

from .conftest import PageTestConfig


def run__Page__valid(cls: "PageClass", ptc: "PageTestConfig") -> None:

    Globals.init(root=ptc.site)

    page = cls(path=ptc.path, config=ptc.page_yaml)

    repr(page)

    assert page.config.type == ptc.type
    assert page.config.is_index is ptc.is_index
    assert page.config.title == ptc.title
    assert page.config.date == ptc.date
    assert page.config.description == ptc.path_description
    assert page.config.cover == ptc.path_cover

    assert len(page.contents) == ptc.contents_count

    for index, content in enumerate(page.contents):
        content_type: "ContentClass" = ptc.contents_types[index]
        assert isinstance(content, content_type)  # type: ignore

    assert page.directory_name == ptc.path.name
    assert page.path == ptc.path
    assert page.url == ptc.url
    assert page.is_index is ptc.is_index
    assert page.title == ptc.title
    assert page.date == ptc.datetime_date
    assert isinstance(page.description, TextBlock)
    assert isinstance(page.cover, Image)


def run__Page__no_date_cover_description(
    cls: "PageClass", ptc: "PageTestConfig"
) -> None:

    Globals.init(root=ptc.site)

    page_yaml = ptc.page_yaml

    del page_yaml["date"]
    del page_yaml["description"]
    del page_yaml["cover"]

    page = cls(path=ptc.path, config=page_yaml)

    assert page.config.date is None
    assert page.config.description is None
    assert page.config.cover is None

    assert page.date is None
    assert page.description is None
    assert page.cover is None


def run__Page__invaid_date_format(cls: "PageClass", ptc: "PageTestConfig") -> None:

    page_yaml = ptc.page_yaml
    page_yaml["date"] = "invalid-date-format"

    with pytest.raises(ValueError):
        cls(path=ptc.path, config=page_yaml)


def run__Page__missing_description(cls: "PageClass", ptc: "PageTestConfig") -> None:

    page_yaml = ptc.page_yaml
    page_yaml["description"] = "./missing-description.md"

    with pytest.raises(MissingFile):
        cls(path=ptc.path, config=page_yaml)


def run__Page__missing_cover(cls: "PageClass", ptc: "PageTestConfig") -> None:

    page_yaml = ptc.page_yaml
    page_yaml["cover"] = "./missing-cover.jpg"

    with pytest.raises(MissingFile):
        cls(path=ptc.path, config=page_yaml)


def run__Page__invalid_options_type(cls: "PageClass", ptc: "PageTestConfig") -> None:

    page_yaml = ptc.page_yaml
    page_yaml["options"] = "invalid-type"

    with pytest.raises(PageConfigError):
        cls(path=ptc.path, config=page_yaml)


def test__Page__valid(all_pages) -> None:
    for cls, ptc in all_pages.items():
        run__Page__valid(cls=cls, ptc=ptc)


def test__Page__no_date_cover_description(all_pages) -> None:
    for cls, ptc in all_pages.items():
        run__Page__no_date_cover_description(cls=cls, ptc=ptc)


def test__Page__invaid_date_format(all_pages) -> None:
    for cls, ptc in all_pages.items():
        run__Page__invaid_date_format(cls=cls, ptc=ptc)


def test__Page__missing_description(all_pages) -> None:
    for cls, ptc in all_pages.items():
        run__Page__missing_description(cls=cls, ptc=ptc)


def test__Page__missing_cover(all_pages) -> None:
    for cls, ptc in all_pages.items():
        run__Page__missing_cover(cls=cls, ptc=ptc)


def test__Page__invalid_options_type(all_pages) -> None:
    for cls, ptc in all_pages.items():
        run__Page__invalid_options_type(cls=cls, ptc=ptc)
