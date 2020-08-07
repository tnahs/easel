__version__ = "0.1.2"


import logging
import os

from flask import Flask

from .site.config import config
from .site.site import Site


logging.getLogger("MARKDOWN").setLevel("ERROR")
logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {name} {levelname}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)


logger = logging.getLogger(__name__)


class Easel(Flask):
    def __init__(self, path_user_site: str, path_custom_assets: str = None):
        super().__init__(__name__)

        config.path_user_site = path_user_site
        config.path_assets = path_custom_assets

        # Load blueprints.
        from .site.views import blueprint_site
        from .main.views import blueprint_main

        # Register blueprints.
        self.register_blueprint(blueprint_site)
        self.register_blueprint(blueprint_main)

        # Bind Site.
        self._site = Site()

        @self.context_processor
        def inject_site() -> dict:
            return {"site": self._site}

    @property
    def site(self) -> Site:
        return self._site

    def run(self, loglevel: str = "DEBUG"):
        os.environ["FLASK_ENV"] = "development"
        logging.getLogger().setLevel(loglevel)
        super().run(debug=True, extra_files=self._site.assets)
