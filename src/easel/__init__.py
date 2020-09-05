__version__ = "2.0.0-dev"


import logging


logging.getLogger("MARKDOWN").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {name} {levelname}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)


from typing import Optional, Union

from flask import Flask

from .site import global_config
from .site.site import Site


class Easel(Flask):
    def __init__(
        self,
        site: str,
        debug: bool = False,
        loglevel: Optional[Union[str, int]] = None,
    ):
        super().__init__(__name__)

        if loglevel is not None:
            logging.getLogger().setLevel(loglevel)

        global_config.path_site = site
        global_config.debug = debug

        # Create and bind Site.
        self._site = Site()

        # Load blueprints.
        from .site.views import blueprint_site
        from .main.views import blueprint_main

        # Register blueprints.
        self.register_blueprint(blueprint_site)
        self.register_blueprint(blueprint_main)

        @self.context_processor
        def inject_site() -> dict:
            return {"site": self._site}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{global_config.path_site}>"

    @property
    def site(self) -> Site:
        return self._site

    def run(self, **kwargs) -> None:
        super().run(
            debug=global_config.debug, extra_files=global_config.assets, **kwargs
        )

    def rebuild_cache(self) -> None:
        self._site.rebuild_cache()
