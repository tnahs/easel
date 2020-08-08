__version__ = "1.0.0"


import logging
import os
from typing import Optional, Union

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
    def __init__(self, site: str, custom_assets: str = None):
        super().__init__(__name__)

        config.path_site = site
        config.path_assets = custom_assets

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

    def run(
        self, loglevel: Optional[Union[str, int]] = None, debug: bool = True, **kwargs
    ):

        if debug:
            os.environ["FLASK_ENV"] = "development"

        if loglevel is not None:
            logging.getLogger().setLevel(loglevel)

        super().run(debug=debug, extra_files=self._site.assets, **kwargs)
