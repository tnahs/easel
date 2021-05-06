import pathlib

from .utils import Utils


class _Globals:
    _site_root: pathlib.Path

    @property
    def site_root(self) -> pathlib.Path:
        return self._site_root

    @site_root.setter
    def site_root(self, value: pathlib.Path) -> None:
        self._site_root = value

    @property
    def static_url_path(self) -> str:
        """Returns an absolute url: /site"""
        return Utils.urlify("site")


Globals = _Globals()
