from flask import Blueprint

from .config import config


# fmt:off
blueprint_site = Blueprint(
    name="site",
    import_name=__name__,
    static_folder=str(config.path_user_site),
)
# fmt:on
