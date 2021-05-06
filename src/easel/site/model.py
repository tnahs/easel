import re

from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    class Config:
        underscore_attrs_are_private = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            return re.sub(r"[_-]", "_", string)
