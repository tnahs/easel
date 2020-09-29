import collections.abc
import copy
import datetime
import logging
import os
import pathlib
import re
import unicodedata
from typing import Optional, Union

import yaml

from .defaults import Defaults
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
    def str_to_bool(value: str) -> bool:
        return value.upper() in ["TRUE", "ENABLED", "YES", "1"]

    @staticmethod
    def get_mimetype(extension: str) -> Optional[str]:
        """ Returns appropriate MIME Type for a file extension. """

        if not extension.startswith("."):
            extension = f".{extension}"

        mimetype = Defaults.MIMETYPES.get(extension, None)

        if mimetype is None:
            logger.warning(f"Unsupported MIME Type '{extension}' detected.")

        return mimetype

    @staticmethod
    def str_to_datetime(date: str) -> datetime.datetime:

        for date_format in Defaults.DATE_FORMATS:
            try:
                datetime_date = datetime.datetime.strptime(date, date_format)
            except ValueError:
                """ValueError is raised if the date_string and format can’t be
                parsed by time.strptime() or if it returns a value which isn’t
                a time tuple.

                via https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
                """
                continue
            else:
                return datetime_date

        raise ValueError(
            f"Unsupported date format '{date}'. Supported formats are "
            f"{Defaults.DATE_FORMATS_PRETTY}."
        )

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
        """Ensures path is relative to the 'Globals.site_paths.pages' directory.

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
            path = path.relative_to(Defaults.DIRECTORY_NAME_CONTENTS)
        except ValueError:
            # pathlib raises a ValueError if the path does not begin with the
            # value passed to Path.relative_to(). In this case 'contents'.
            pass

        try:
            # Returns: page-name
            path = path.relative_to(Defaults.DIRECTORY_NAME_PAGES)
        except ValueError:
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

    @staticmethod
    def update_dict(original: dict, updates: collections.abc.Mapping) -> dict:
        """Returns a new dictionary with values from 'original' updated
        from the values from 'updates'.

        via https://stackoverflow.com/a/43228384
        via https://stackoverflow.com/a/38089879"""

        updated = copy.deepcopy(original)

        for key, value in updates.items():

            if isinstance(value, collections.abc.Mapping):

                default = value.copy()  # type: ignore
                default.clear()

                updated[key] = Utils.update_dict(
                    original=updated.get(key, default), updates=value
                )

            else:
                updated[key] = copy.deepcopy(updates[key])

        return updated


class SafeDict(dict):
    """Creates a dictionary that never raises a KeyError but rather returns a
    new dictionary of its own kind (i.e. a SafeDict) as the value of the
    missing key. This is primarily used for optional nested configurations
    where a missing key is okay.

    https://stackoverflow.com/a/25840834"""

    def __getitem__(self, key):

        if key not in self:
            return self.setdefault(key, type(self)())

        return super().__getitem__(key)

    def __getattr__(self, key):

        if key not in self:
            return self.setdefault(key, type(self)())

        return super().__getitem__(key)
