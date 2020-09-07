from typing import TYPE_CHECKING, Optional

from flask import Blueprint, abort, current_app, render_template

from ..site.theme import site_theme__


if TYPE_CHECKING:
    from easel.site.pages import PageObj


blueprint_main = Blueprint(
    name="main",
    import_name=__name__,
    template_folder=str(site_theme__.path_templates),
    # Explicitly setting 'url_prefix' to an emptry string to set this
    # blueprint to be served when accesting the base url i.e. 'www.site.com'.
    url_prefix="",
    # [I]f the blueprint does not have a 'url_prefix', it is not possible to
    # access the blueprint’s static folder. This is because the URL would be
    # '/static' in this case, and the application’s '/static' route takes
    # precedence. Unlike template folders, blueprint static folders are not
    # searched if the file does not exist in the application static folder.
    #
    # via https://flask.palletsprojects.com/en/1.1.x/blueprints/#static-files
    static_url_path=str(site_theme__.path_static),
    static_folder=str(site_theme__.path_static),
)


@blueprint_main.route("/")
def index() -> str:

    page: Optional["PageObj"] = current_app.site.index

    if page is None:
        abort(404)

    return render_template("main.html", page=page)


@blueprint_main.route("/<path:page_url>")
def render_page(page_url: str) -> str:

    page: Optional["PageObj"] = current_app.site.get_page(page_url=page_url)

    if page is None:
        abort(404)

    return render_template("main.html", page=page)


@blueprint_main.errorhandler(404)
def error_404(error):
    return render_template("404.html")
