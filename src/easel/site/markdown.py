import pathlib
from typing import TYPE_CHECKING, Optional

import markdown as _markdown

from .globals import site_globals


if TYPE_CHECKING:
    from .pages import PageObj


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
        base_path = pathlib.Path(f"{site_globals.paths.root.name}/{page.path_relative}")

        with open(filepath, encoding="utf-8") as f:
            string = f.read()

        return self._convert(string, base_path)

    def from_string(self, string: Optional[str] = None) -> str:
        """ Render Markdown from a string. """

        if string is not None:
            return self._convert(string)

        return ""


markdown = Markdown()
