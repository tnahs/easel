import logging
import pathlib
import re
import unicodedata
from typing import TYPE_CHECKING, Optional

import markdown as _markdown
import yaml

from . import errors
from .config import config


if TYPE_CHECKING:
    from .pages import PageType


logger = logging.getLogger(__name__)


class ConfigLoader:
    @staticmethod
    def load(path: pathlib.Path) -> dict:

        logger.debug(f"Loading config file from {path}.")

        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as error:
            raise errors.ConfigError(
                f"YAML Parsing Error while loading {path}."
            ) from error
        except FileNotFoundError as error:
            raise errors.ConfigError(
                f"Config '{path.name}' not found in {path.parent}."
            ) from error
        except Exception as error:
            raise errors.ConfigError(
                f"Unexpected Error while loading {path}."
            ) from error

        return config


class Utils:
    def slugify(
        self, string: str, delimiter: str = "-", allow_unicode: bool = False
    ) -> str:
        """ Convert to ASCII if 'allow_unicode' is False. Convert spaces to
        hyphens. Remove characters that aren't alphanumerics, underscores, or
        hyphens. Convert to lowercase. Also strip leading and trailing
        whitespace.

        via. https://docs.djangoproject.com/en/2.1/_modules/django/utils/text/#slugify
        """

        string = str(string)

        if allow_unicode:
            string = unicodedata.normalize("NFKC", string)
        else:
            string = (
                unicodedata.normalize("NFKD", string)
                .encode("ascii", "ignore")
                .decode("ascii")
            )

        string = re.sub(r"[^\w\s-]", "", string).strip().lower()
        string = re.sub(r"[-\s]+", delimiter, string)

        return string


class Markdown:
    def _convert(self, string: str, base_path: Optional[pathlib.Path] = None) -> str:
        """ https://facelessuser.github.io/pymdown-extensions/ """

        md = _markdown.Markdown(
            extensions=[
                "nl2br",
                "sane_lists",
                "pymdownx.pathconverter",
                "pymdownx.smartsymbols",
                "pymdownx.magiclink",
                "pymdownx.tasklist",
                "pymdownx.extra",
                "pymdownx.caret",
                "pymdownx.tilde",
                "pymdownx.mark",
            ],
            extension_configs={
                "pymdownx.pathconverter": {"absolute": True, "base_path": base_path}
            },
        )

        return md.convert(string)

    def from_file(self, filepath: pathlib.Path, page: "PageType") -> str:
        """ Render Markdown from a file. """

        # 'base_path' is pre-pended to any 'path' or 'src' in <a>, <script>,
        # <img>, and <link> tags, allowing the use of relative paths in
        # markdown files.
        #
        # via https://facelessuser.github.io/pymdown-extensions/extensions/pathconverter/
        base_path = pathlib.Path(f"{config.path_site.name}/{page.path_relative}")

        with open(filepath, encoding="utf-8") as f:
            string = f.read()

        return self._convert(string, base_path)

    def from_string(self, string: Optional[str] = None) -> str:
        """ Render Markdown from a string. """

        if string is not None:
            return self._convert(string)

        return ""


config_loader = ConfigLoader()
utils = Utils()
markdown = Markdown()
