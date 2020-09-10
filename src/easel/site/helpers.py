import copy
import collections
import logging
import pathlib
import re
import unicodedata
from typing import Any

import yaml

from . import errors
from .defaults import Defaults


logger = logging.getLogger(__name__)


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

    @staticmethod
    def update_dict(base: dict, updates: Any) -> dict:

        updated = copy.deepcopy(base)

        for key, value in updates.items():

            if isinstance(value, collections.Mapping):

                _updated = Utils.update_dict(base=updated.get(key, {}), updates=value)

                updated[key] = _updated

            elif isinstance(value, list):
                updated[key] = updated.get(key, []) + value

            else:
                updated[key] = updates[key]

        return updated
