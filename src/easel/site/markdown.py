import os
import pathlib
from typing import Optional, Union

import markdown as _markdown

from .globals import Globals
from .utils import Utils


class _Markdown:
    @staticmethod
    def _convert(
        string: str, base_path: Optional[Union[str, pathlib.Path]] = None
    ) -> str:
        """https://facelessuser.github.io/pymdown-extensions/"""

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
                "pymdownx.pathconverter": {
                    "absolute": True,
                    "base_path": base_path,
                }
            },
        )

        return md.convert(string)

    def from_file(self, path: pathlib.Path) -> str:
        """Render Markdown from a file."""

        """ 'base_path' is pre-pended to any 'path' or 'src' in <a>, <script>,
        <img>, and <link> tags, allowing the use of relative paths in markdown
        files. NOTE: This is emulating Easel._filter__site_url() with a
        slight variation.

        Transforms the original path:

            /site-name/pages/page-name/content.md

        ...to one relative to the static folder without the filename.

            pages/page-name

        ...then prepends the static url path.

            /sorolla-demo/pages/pages/page-name

        via https://facelessuser.github.io/pymdown-extensions/extensions/pathconverter/
        """

        path_relative = path.relative_to(Globals.site_root).parent
        base_path = Utils.urlify(f"{Globals.static_url_path}{os.sep}{path_relative}")

        with open(path, encoding="utf-8") as f:
            string = f.read()

        return self._convert(string=string, base_path=base_path)

    def from_string(self, string: Optional[str] = None) -> str:
        """Render Markdown from a string."""

        if string is None:
            return ""

        return self._convert(string)


Markdown = _Markdown()
