__version__ = "2.0.0-dev"


import logging


logging.getLogger("MARKDOWN").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {name} {levelname}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)


import os
import pathlib
from typing import Optional, Union

from flask import Flask

from .site import Site
from .site.defaults import Key
from .site.globals import Globals
from .site.helpers import Utils


class Easel(Flask):
    """ Returns a thinly wrapped Flask application instance with two bound
    attributes, Easel._site and it's accessor Easel.site which returns a
    Site object.

    TEMP: Both 'theme' and 'custom_theme' are temporary ways of setting and
    customizing the theme. Future implementations will use the 'site.yaml' to
    do this. See src.easel.site.GlobalConfig for more info. """

    def __init__(
        self,
        root: Optional[Union[pathlib.Path, str]] = None,
        /,
        loglevel: Optional[str] = None,
        debug: Optional[bool] = None,
    ):
        super().__init__(__name__)

        ENV_SITE_ROOT: Optional[str] = os.environ.get(Key.SITE_ROOT, None)
        ENV_SITE_DEBUG: str = os.environ.get(Key.SITE_DEBUG, "FALSE")

        root = root if root is not None else ENV_SITE_ROOT
        debug = debug if debug is not None else Utils.str_to_bool(ENV_SITE_DEBUG)

        logger = logging.getLogger()

        if loglevel is not None:

            # Convert loglevel to an integer for setting numeric levels.
            loglevel_parsed: Union[str, int] = int(
                loglevel
            ) if loglevel.isnumeric() else loglevel

            logger.setLevel(loglevel_parsed)

            # Also set Flask's 'werkzeug' the Easel's loglevel.
            logging.getLogger("werkzeug").setLevel(loglevel_parsed)

        # Setup/Load Globals object.
        Globals.debug = debug
        Globals.init(root=root)

        # Create and bind Site.
        self._site = Site()
        self._site.build()

        # Load blueprints.
        from .main.views import blueprint_main
        from .site.views import blueprint_site

        # Register blueprints.
        self.register_blueprint(blueprint_site)
        self.register_blueprint(blueprint_main)

        # Inject site into template context.
        self.context_processor(self._inject_into_template)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{Globals.site_paths.root}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{Globals.site_paths.root}"

    def _inject_into_template(self) -> dict:
        return {"site": self.site}

    @property
    def site(self) -> "Site":
        return self._site

    def run(self, **kwargs) -> None:
        super().run(debug=Globals.debug, extra_files=self.site.assets, **kwargs)
