from flask import Blueprint

from .paths import site_paths__


# fmt:off
blueprint_site = Blueprint(
    name="site",
    import_name=__name__,
    static_folder=str(site_paths__.root),
)
# fmt:on
