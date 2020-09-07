from flask import Blueprint

from .globals import site_globals


# fmt:off
blueprint_site = Blueprint(
    name="site",
    import_name=__name__,
    static_folder=str(site_globals.paths.root),
)
# fmt:on
