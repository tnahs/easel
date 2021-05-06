import logging
import os
import pathlib
import re
import unicodedata
from typing import Optional, Union

import yaml

from .enums import E_Directory, E_Mimetype
from .errors import ConfigLoadError


logger = logging.getLogger(__name__)


class Utils:
    @staticmethod
    def load_config(path: pathlib.Path) -> dict:

        logger.debug(f"Loading '{path.name}' from {path}.")

        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as error:
            raise ConfigLoadError(
                f"YAML Parsing Error while loading {path}."
            ) from error
        except FileNotFoundError as error:
            raise ConfigLoadError(
                f"Config '{path.name}' not found in {path.parent}."
            ) from error

        if data is None:
            return {}

        return data

    @staticmethod
    def get_mimetype(extension: str) -> Optional[str]:
        """Returns appropriate MIME Type for a file extension."""

        while extension.startswith("."):
            extension = extension[1:]

        try:
            mimetype = E_Mimetype[extension.upper()]
        except KeyError:
            logger.warning(f"Unsupported MIME Type '{extension}' detected.")
            return None

        return mimetype

    @staticmethod
    def slugify(string: str, delimiter: str = "-", allow_unicode: bool = False) -> str:
        """Convert to ASCII if 'allow_unicode' is False. Convert spaces to
        hyphens. Remove characters that aren't alphanumerics, underscores, or
        hyphens. Convert to lowercase. Also strip leading and trailing
        whitespace.

        via https://docs.djangoproject.com/en/2.1/_modules/django/utils/text/#slugify
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
        string = re.sub(r"[\s-]+", delimiter, string)

        return string

    @staticmethod
    def normalize_page_path(path: Union[str, pathlib.Path]) -> str:
        """Ensures path is relative to the 'Site().path_pages' directory.

            ./contents/pages/page-name --> /page-name
            /contents/pages/page-name  --> /page-name
            contents/pages/page-name   --> /page-name

            ./pages/page-name          --> /page-name
            /pages/page-name           --> /page-name
            pages/page-name            --> /page-name

            ./page-name                --> /page-name
            /page-name                 --> /page-name
            page-name                  --> /page-name

        This allows users to use paths relative to the site-name or or 'pages'
        directory."""

        # Starting with: ./contents/pages/page-name

        # Returns: contents/pages/page-name
        path = Utils.urlify(path, leading_slash=False)

        path = pathlib.Path(path)

        try:
            # Returns: pages/page-name
            path = path.relative_to(E_Directory.CONTENTS)
        except ValueError:
            # pathlib raises a ValueError if the path does not begin with the
            # value passed to Path.relative_to(). In this case 'contents'.
            pass

        try:
            # Returns: page-name
            path = path.relative_to(E_Directory.PAGES)
        except ValueError:
            # See above.
            pass

        # Returns: /page-name
        return Utils.urlify(path)

    @staticmethod
    def urlify(
        path: Union[str, pathlib.Path],
        leading_slash: bool = True,
        slugify: bool = False,
    ) -> str:

        # Normalize path with pathlib.
        path = pathlib.Path(path)

        # Slugify each part of the path...
        if slugify is True:

            # ...only if it isn't a slash-type i.e '\'...
            path_slugified = [
                Utils.slugify(part) for part in path.parts if part != os.sep
            ]

            # ...then re-join with the same slash-type
            path = os.sep.join(path_slugified)

        path = str(path)

        # Normalize leading slash.
        while path.startswith(os.sep):
            path = path[1:]

        if leading_slash is True:
            return f"{os.sep}{path}"

        return path
