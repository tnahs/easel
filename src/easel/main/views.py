from typing import TYPE_CHECKING, Optional

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    url_for,
)

from ..site.config import config


if TYPE_CHECKING:
    from easel.site.pages import PageType


blueprint_main = Blueprint(
    name="main",
    import_name=__name__,
    template_folder=str(config.path_templates),
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
    static_url_path=str(config.path_static),
    static_folder=str(config.path_static),
)


@blueprint_main.route("/")
def page_landing() -> str:

    page: Optional["PageType"] = current_app.site.page_landing

    return render_template("page.jinja2", page=page)


@blueprint_main.route("/<path:page_url>")
def render_page(page_url: str) -> str:

    page: Optional["PageType"] = current_app.site.get_page(page_url=page_url)

    if page is None:
        abort(404)

    return render_template("page.jinja2", page=page)


@blueprint_main.errorhandler(404)
def error_404(error):

    page: Optional["PageType"] = current_app.site.page_error_404

    if page is None:
        return redirect(url_for("main.page_landing"))

    return render_template("page.jinja2", page=page)


@blueprint_main.errorhandler(500)
def error_500(error):

    page: Optional["PageType"] = current_app.site.page_error_500

    if page is None:
        return redirect(url_for("main.page_landing"))

    return render_template("page.jinja2", page=page)
