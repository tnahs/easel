import pathlib
from typing import Optional, Union

from . import errors
from .defaults import SiteDefaults


class SiteTheme:

    _root_custom: Optional[pathlib.Path] = None
    _name: Optional[str] = None

    @property
    def root(self) -> pathlib.Path:
        """ Returns the path to the current theme. """

        if self._root_custom is None:
            return (
                SiteDefaults.PATH_ROOT / SiteDefaults.DIRECTORY_NAME_THEMES / self.name
            )

        return self._root_custom

    @root.setter
    def root(self, value: Optional[Union[pathlib.Path, str]]) -> None:
        """ Sets the theme path to a custom location. """

        if not value:
            return

        path_theme = pathlib.Path(value)

        try:
            path_theme = path_theme.resolve(strict=True)
        except FileNotFoundError as error:
            raise errors.SiteConfigError(
                f"Theme directory {value} not found."
            ) from error

        self._root_custom = path_theme

    @property
    def name(self) -> str:
        """ Returns the name of the current theme. This method is accessed only
        if a path to a custom theme is not set. """

        if self._name is None:
            return SiteDefaults.DEFAULT_THEME_NAME

        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        """ Changes the current theme name. """

        if not value:
            return

        if value not in SiteDefaults.VALID_THEME_NAMES:
            raise errors.SiteConfigError(
                f"Invalid theme name '{value}'. Available themes are: "
                f"{SiteDefaults.VALID_THEME_NAMES}"
            )

        self._name = value

    @property
    def path_static(self) -> pathlib.Path:
        """ Returns the path to the current theme's static directory. """
        return self.root / SiteDefaults.DIRECTORY_NAME_STATIC

    @property
    def path_templates(self) -> pathlib.Path:
        """ Returns the path to the current theme's templates directory. """
        return self.root / SiteDefaults.DIRECTORY_NAME_TEMPLATES


site_theme__ = SiteTheme()
