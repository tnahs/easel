from flask import Blueprint

from .globals import Globals


# fmt:off
blueprint_site = Blueprint(
    name="site",
    import_name=__name__,
    static_folder=str(Globals.site_paths.root),
)
# fmt:on
