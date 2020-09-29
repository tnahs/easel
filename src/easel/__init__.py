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
import re
from typing import Optional, Union

from flask import Flask

from .site import Site
from .site.defaults import Key
from .site.errors import ThemeConfigError
from .site.globals import Globals
from .site.helpers import Utils


logger = logging.getLogger()


class Easel(Flask):
    """Returns a thinly wrapped Flask application instance with two bound
    attributes, Easel._site and it's accessor Easel.site which returns a
    Site object."""

    def __init__(
        self,
        root: Optional[Union[pathlib.Path, str]] = None,
        /,
        loglevel: Optional[str] = None,
        debug: Optional[bool] = None,
        testing: Optional[bool] = None,
    ):
        super().__init__(__name__)

        ENV_ROOT: Optional[str] = os.environ.get(Key.SITE_ROOT, None)
        ENV_DEBUG: str = os.environ.get(Key.SITE_DEBUG, "FALSE")
        ENV_TESTING: str = os.environ.get(Key.SITE_TESTING, "FALSE")

        root = root if root is not None else ENV_ROOT
        debug = debug if debug is not None else Utils.str_to_bool(ENV_DEBUG)
        testing = testing if testing is not None else Utils.str_to_bool(ENV_TESTING)

        if loglevel is not None:

            # Convert loglevel to an integer for setting numeric levels.
            loglevel_parsed: Union[str, int] = (
                int(loglevel) if loglevel.isnumeric() else loglevel
            )

            logger.setLevel(loglevel_parsed)

            # Also set Flask's 'werkzeug' to Easel's loglevel.
            logging.getLogger("werkzeug").setLevel(loglevel_parsed)

        if debug is True:
            os.environ["FLASK_ENV"] = "development"

        if testing is True:
            self.config["TESTING"] = True

        # Setup Globals object.
        Globals.debug = debug
        Globals.testing = testing
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

        # Inject site and theme into template context.
        self.context_processor(self._context)

        # Register custom url filters.
        self.jinja_env.filters["site_url"] = self._filter__site_url
        self.jinja_env.filters["theme_url"] = self._filter__theme_url

        """ Remove the root static URL rule. Leaving the following URL map:

        >>> self.url_map

            [
                <Rule '/' (OPTIONS, GET, HEAD) -> theme.index>,
                <Rule '/<page_url>' (OPTIONS, GET, HEAD) -> theme.render_page>
                <Rule '/theme/<filename>' (OPTIONS, GET, HEAD) -> theme.static>,
                <Rule '/site/<filename>' (OPTIONS, GET, HEAD) -> site.static>,
            ]

        https://stackoverflow.com/a/55909279
        https://www.pythonanywhere.com/forums/topic/12195/#id_post_46324
        """

        for rule in self.url_map.iter_rules("static"):
            self.url_map._rules.remove(rule)

        self.url_map._rules_by_endpoint["static"] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{Globals.site_paths.root}>"

    def _context(self) -> dict:
        # fmt:off
        return {
            "debug": Globals.debug,
            "config": {
                "site": Globals.site_config,
                "theme": Globals.theme_config,
            },
            "index": self.site.index,
            "menu": self.site.menu,
            "pages": self.site.pages,
        }
        # fmt:on

    @staticmethod
    def _filter__site_url(path: str) -> str:
        """Returns the path as absolute url to the site's static url '/site':

            path -> /site/path

        See Easel.__inti__() and Globals.site_paths.static_url_path."""

        return Utils.urlify(f"{Globals.site_paths.static_url_path}{os.sep}{path}")

    @staticmethod
    def _filter__theme_url(path: Union[pathlib.Path, str]) -> str:
        """Returns the path as absolute url to the themes's static url:

            path -> /theme/path

        See Easel.__inti__() and Globals.theme_paths.static_url_path."""

        # public/css/bundle.#.css
        path = pathlib.Path(path)

        # bundle.#.css
        filename = path.name

        if "#" in filename:

            # -> public/css/
            parent = path.parent

            # -> /absolute/path/to/parent
            path_absolute = Globals.theme_paths.root / parent

            # -> bundle.*.css
            filename_glob = re.sub(pattern=r"#+", repl="*", string=filename)

            try:
                latest_hashed_path = max(
                    path_absolute.glob(filename_glob),
                    key=os.path.getctime,
                )
                # NOTE: os.path.getctime returns the system’s ctime which, on
                # Unix-like systems, is the time of the last metadata change,
                # and, on others like Windows, is the creation time for path.
            except ValueError:
                # A ValueError is raised by max() if path_absolute.glob()
                # returns an empty iterator. Meaning there were no files that
                # matched the glob.
                raise ThemeConfigError(f"Hashed path '{path}' not found.")
            else:
                # Reassemble the path with the actual name of the hashed file.
                # -> public/css/bundle.###.css
                path = parent / latest_hashed_path.name

        return Utils.urlify(f"{Globals.theme_paths.static_url_path}{os.sep}{path}")

    @property
    def site(self) -> "Site":
        return self._site

    def run(self, watch: bool = False, **kwargs) -> None:

        extra_files = (
            [*Globals.site_paths.assets, *Globals.theme_paths.assets]
            if watch is True
            else []
        )

        if watch is True:  # pragma: no branch
            # TODO:LOW Once we're fully decoupled from Flask, re-assess how
            # watching/live-reloading will work along with what assets will be
            # watched. Both site and theme? Or just site?
            logger.info(
                f"Watching {Globals.site_paths.root} and "
                f"{Globals.theme_paths.root} for changes."
            )

        if Globals.testing is True:
            return

        super().run(
            debug=Globals.debug, extra_files=extra_files, **kwargs
        )  # pragma: no cover
