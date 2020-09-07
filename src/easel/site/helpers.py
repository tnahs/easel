import logging
import pathlib
import re
import unicodedata
from typing import TYPE_CHECKING, Optional

import markdown as _markdown
import yaml

from . import errors
from .defaults import SiteDefaults
from .paths import site_paths__


if TYPE_CHECKING:
    from .pages import PageObj


logger = logging.getLogger(__name__)


class Key:
    ALIGN: str = "align"
    AUTHOR: str = "author"
    CAPTION: str = "caption"
    CONTENTS: str = "contents"
    COVER: str = "cover"
    COPYRIGHT: str = "copyright"
    DATE: str = "date"
    DESCRIPTION: str = "description"
    EXTRAS: str = "extras"
    FAVICON: str = "favicon"
    COLUMN_COUNT: str = "column-count"
    HEADER: str = "header"
    HTML: str = "html"
    ICON: str = "icon"
    IS_GALLERY: str = "is-gallery"
    IS_INDEX: str = "is-index"
    LABEL: str = "label"
    LINKS_TO: str = "links-to"
    MENU: str = "menu"
    NAME: str = "name"
    OPTIONS: str = "options"
    PATH: str = "path"
    SHOW_CAPTIONS: str = "show-captions"
    SIZE: str = "size"
    TEXT: str = "text"
    THEME: str = "theme"
    TITLE: str = "title"
    TYPE: str = "type"
    URL: str = "url"


class SafeDict(dict):
    """ Creates a dictionary that never raises a KeyError but rather returns a
    new dictionary of its own kind (i.e. a SafeDict) as the value of the
    missing key. This is primarily used for optional nested configurations
    where a missing key is okay.

    https://stackoverflow.com/a/25840834 """

    def __getitem__(self, key):

        if key not in self:
            return self.setdefault(key, type(self)())

        return super().__getitem__(key)


class Utils:
    @staticmethod
    def load_config(path: pathlib.Path) -> dict:

        logger.debug(f"Loading '{path.name}' from {path}.")

        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as error:
            raise errors.ConfigLoadError(
                f"YAML Parsing Error while loading {path}."
            ) from error
        except FileNotFoundError as error:
            raise errors.ConfigLoadError(
                f"Config '{path.name}' not found in {path.parent}."
            ) from error
        except Exception as error:
            raise errors.ConfigLoadError(
                f"Unexpected Error while loading {path}."
            ) from error

        if data is None:
            return {}

        return data

    @staticmethod
    def get_mimetype(extension: str) -> str:
        """ Returns appropriate MIME Type for a file extension. """

        if not extension.startswith("."):
            extension = f".{extension}"

        mimetype = SiteDefaults.MIMETYPES.get(extension, None)

        if mimetype is None:
            logger.warning(f"Unsupported MIME Type '{extension}' detected.")
            return ""

        return mimetype

    @staticmethod
    def slugify(string: str, delimiter: str = "-", allow_unicode: bool = False) -> str:
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

    def from_file(self, filepath: pathlib.Path, page: "PageObj") -> str:
        """ Render Markdown from a file. """

        # 'base_path' is pre-pended to any 'path' or 'src' in <a>, <script>,
        # <img>, and <link> tags, allowing the use of relative paths in
        # markdown files.
        #
        # via https://facelessuser.github.io/pymdown-extensions/extensions/pathconverter/
        base_path = pathlib.Path(f"{site_paths__.root.name}/{page.path_relative}")

        with open(filepath, encoding="utf-8") as f:
            string = f.read()

        return self._convert(string, base_path)

    def from_string(self, string: Optional[str] = None) -> str:
        """ Render Markdown from a string. """

        if string is not None:
            return self._convert(string)

        return ""


markdown = Markdown()
