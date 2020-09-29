from typing import TYPE_CHECKING, Optional

from flask import Blueprint, abort, current_app, render_template

from easel.site.defaults import Defaults

from ..site.globals import Globals


if TYPE_CHECKING:
    from easel.site.pages import PageObj


blueprint_theme = Blueprint(
    name="theme",
    import_name=__name__,
    template_folder=str(Globals.theme_paths.root),
    static_folder=str(Globals.theme_paths.root),
    static_url_path=Globals.theme_paths.static_url_path,
)


@blueprint_theme.route("/")
def index() -> str:

    page: "PageObj" = current_app.site.index

    return render_template(Defaults.FILENAME_TEMPLATE_MAIN_HTML, page=page)


@blueprint_theme.route("/<path:page_url>")
def render_page(page_url: str) -> str:

    page: Optional["PageObj"] = current_app.site.get_page(page_url=page_url)

    if page is None:
        abort(404)

    return render_template(Defaults.FILENAME_TEMPLATE_MAIN_HTML, page=page)


@blueprint_theme.errorhandler(404)
def error_404(error):
    return render_template(Defaults.FILENAME_TEMPLATE_404_HTML)
