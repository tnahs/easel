from easel.site.markdown import Markdown


def test__from_file__assets_paths_valid() -> None:
    pass


def test__from_string__valid() -> None:

    # fmt:off
    render_01 = Markdown.from_string(
        "# Lorem Ipsum\n"
        "Dolor sit amet consectetur adipisicing elit."
    )
    # fmt:on
    render_02 = Markdown.from_string(string=None)

    # fmt:off
    assert render_01 == (
        "<h1>Lorem Ipsum</h1>\n"
        "<p>Dolor sit amet consectetur adipisicing elit.</p>"
    )
    # fmt:on

    assert render_02 == ""
