from flask import Blueprint

from .globals import Globals


blueprint_site = Blueprint(
    name="site",
    import_name=__name__,
    static_folder=str(Globals.site_paths.static),
    static_url_path=Globals.site_paths.static_url_path,
)
