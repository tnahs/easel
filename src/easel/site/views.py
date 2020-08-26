from flask import Blueprint

from . import global_config


# fmt:off
blueprint_site = Blueprint(
    name="site",
    import_name=__name__,
    static_folder=str(global_config.path_site),
)
# fmt:on
