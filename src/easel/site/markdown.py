import os
import pathlib
from typing import Optional, Union

import markdown as _markdown

from .globals import Globals
from .helpers import Utils


class Markdown:
    def _convert(
        self, string: str, base_path: Optional[Union[str, pathlib.Path]] = None
    ) -> str:
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

    def from_file(self, filepath: pathlib.Path) -> str:
        """ Render Markdown from a file. """

        """ 'base_path' is pre-pended to any 'path' or 'src' in <a>, <script>,
        <img>, and <link> tags, allowing the use of relative paths in markdown
        files. NOTE: This is emulating Easel._filter__site_url() with a
        slight variation.

        Transforms the original filepath:

            /site-name/pages/page-name/content.md

        ...to one relative to the static folder without the filename.

            pages/page-name

        ...then appends that to the static_url_path.

            /sorolla-demo/pages/pages/page-name

        via https://facelessuser.github.io/pymdown-extensions/extensions/pathconverter/
        """

        path = filepath.relative_to(Globals.site_paths.root).parent
        base_path = Utils.urlify(f"{Globals.site_paths.static_url_path}{os.sep}{path}")

        with open(filepath, encoding="utf-8") as f:
            string = f.read()

        return self._convert(string, base_path)

    def from_string(self, string: Optional[str] = None) -> str:
        """ Render Markdown from a string. """

        if string is not None:
            return self._convert(string)

        return ""


markdown = Markdown()
