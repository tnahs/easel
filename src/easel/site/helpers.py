import collections
import copy
import logging
import os
import pathlib
import re
import unicodedata
from typing import Union

import yaml

from . import errors
from .defaults import Defaults


logger = logging.getLogger(__name__)


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
    def str_to_bool(value: str) -> bool:
        return value.upper() in ["TRUE", "ENABLED", "YES", "1"]

    @staticmethod
    def get_mimetype(extension: str) -> str:
        """ Returns appropriate MIME Type for a file extension. """

        if not extension.startswith("."):
            extension = f".{extension}"

        mimetype = Defaults.MIMETYPES.get(extension, None)

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
        string = re.sub(r"[-\s]+", delimiter, string)

        return string

    @staticmethod
    def urlify(
        path: Union[str, pathlib.Path], leading_slash: bool = True, slugify: bool = True
    ) -> str:

        # Normalize path with pathlib.
        path = pathlib.Path(path)

        # Slugify each part of the path.
        if slugify is True:
            for part in path.parts:
                if part == os.sep:
                    continue
                part = Utils.slugify(string=part)

        path = str(path)

        while path.startswith(os.sep):
            path = path[1:]

        if leading_slash is True:
            return f"{os.sep}{path}"

        return path

    @staticmethod
    def update_dict(original: dict, updates: collections.Mapping) -> dict:
        """ Returns a new dictionary with values from 'original' updated
        from the values from 'updates'.

        via https://stackoverflow.com/a/43228384
        via https://stackoverflow.com/a/38089879 """

        updated = copy.deepcopy(original)

        for key, value in updates.items():

            if isinstance(value, collections.Mapping):

                default = value.copy()  # type: ignore
                default.clear()

                updated[key] = Utils.update_dict(
                    original=updated.get(key, default), updates=value
                )

            else:
                updated[key] = copy.deepcopy(updates[key])

        return updated
