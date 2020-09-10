__version__ = "2.0.0-dev"


import logging


logging.getLogger("werkzeug").setLevel(logging.ERROR)
logging.getLogger("MARKDOWN").setLevel(logging.ERROR)
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
    Site object. """

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
        from .site.views import blueprint_site
        from .theme.views import blueprint_theme

        # Register blueprints.
        self.register_blueprint(blueprint_site)
        self.register_blueprint(blueprint_theme)

        # Inject site into template context.
        self.context_processor(self._context__site)

        # Register custom static url filters.
        self.jinja_env.filters["static_site"] = self._filter__static_site
        self.jinja_env.filters["static_theme"] = self._filter__static_theme

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{Globals.site_paths.root}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{Globals.site_paths.root}"

    def _context__site(self) -> dict:
        return {"site": self._site}
        # return dict(site=self._site)

    @staticmethod
    def _filter__static_site(path) -> str:
        """ Returns the path as absolute url to the site's static directory:

            /[site-static]/path

        See Globals.site_paths.static_url_path """
        return Utils.urlify(f"{Globals.site_paths.static_url_path}{os.sep}{path}")

    @staticmethod
    def _filter__static_theme(path) -> str:
        """ Returns the path as absolute url to the themes's static directory:

            /[theme-name]/[theme-static]/path

        See Globals.theme_paths.static_url_path """
        return Utils.urlify(f"{Globals.theme_paths.static_url_path}{os.sep}{path}")

    @property
    def site(self) -> "Site":
        return self._site

    def run(self, **kwargs) -> None:
        super().run(debug=Globals.debug, extra_files=self.site.assets, **kwargs)
