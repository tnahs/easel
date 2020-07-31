__version__ = "0.1.2"


import logging
import os

from flask import Flask

from .site.config import config
from .site.site import Site


logging.getLogger("MARKDOWN").setLevel("ERROR")
logging.basicConfig(
    level=logging.ERROR,
    format="{asctime} {name} {levelname}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)


logger = logging.getLogger(__name__)


class Easel:

    _app: Flask = Flask(__name__)

    def __init__(
        self,
        path_user_site: str,
        path_custom_assets: str = None,
        log_level: str = "ERROR",
    ):

        self._set_log_level(log_level=log_level)

        config.path_user_site = path_user_site
        config.path_assets = path_custom_assets

        # Load Blueprints
        from .site.views import blueprint_site
        from .main.views import blueprint_main

        # Register Blueprints
        self._app.register_blueprint(blueprint_site)
        self._app.register_blueprint(blueprint_main)

        # Bind Site
        self._app.site = Site()

        @self._app.context_processor
        def inject_site() -> dict:
            return {"site": self._app.site}

    def _set_log_level(self, log_level: str) -> None:
        logging.getLogger().setLevel(log_level)

    @property
    def app(self):
        return self._app

    def run(self, log_level: str = "DEBUG"):
        os.environ["FLASK_ENV"] = "development"
        self._set_log_level(log_level=log_level)
        self._app.run(extra_files=self._app.site.assets)
