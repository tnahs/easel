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


import pathlib
from typing import Optional, Union

from flask import Flask

from .site import Site
from .site.globals import site_globals


class Easel(Flask):
    """ Returns a thinly wrapped Flask application instance with two bound
    attributes, Easel._site and it's accessor Easel.site which returns a
    Site object.

    TEMP: Both 'theme' and 'custom_theme' are temporary ways of setting and
    customizing the theme. Future implementations will use the 'site.yaml' to
    do this. See src.easel.site.GlobalConfig for more info. """

    def __init__(
        self,
        root: Union[pathlib.Path, str],
        /,
        theme_name: Optional[str] = None,
        theme_root: Optional[Union[pathlib.Path, str]] = None,
        loglevel: Optional[Union[str, int]] = None,
        debug: bool = False,
    ):
        super().__init__(__name__)

        logger = logging.getLogger()

        if loglevel is not None:
            logger.setLevel(loglevel)

        if theme_name and theme_root:
            logger.warning(
                "Setting both 'theme_name' and 'theme_root' might result in unexpected behavior."
            )

        site_globals.paths.root = root
        site_globals.theme.name = theme_name
        site_globals.theme.root = theme_root

        site_globals.config.load()

        # Create and bind Site.
        self._site = Site()
        self._site.debug = debug
        self._site.build()

        # Load blueprints.
        from .main.views import blueprint_main
        from .site.views import blueprint_site

        # Register blueprints.
        self.register_blueprint(blueprint_site)
        self.register_blueprint(blueprint_main)

        @self.context_processor
        def inject_site() -> dict:
            return {"site": self._site}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{site_globals.paths.root}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{site_globals.paths.root}"

    @property
    def site(self) -> "Site":
        return self._site

    def run(self, **kwargs) -> None:
        super().run(debug=self._site.debug, extra_files=self._site.assets, **kwargs)
