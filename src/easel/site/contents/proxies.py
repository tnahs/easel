import abc
import json
import logging
import pathlib
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple

import PIL.Image
import PIL.ImageFilter

from ..defaults import Defaults
from ..globals import Globals


if TYPE_CHECKING:
    from .contents import Image


logger = logging.getLogger()


class BaseProxyManager(abc.ABC):
    """BUG:LOW It would be ideal to trigger Proxy image/color generation and
    loading i.e. the 'cache' method *after* the site has been built and
    validated. However it seems like proxy items become immutable after
    instantiation. In order for them to work properly, they must cached on
    instantiation. If 'cache' is run later in the build process, they show
    internal changes but these are undetectable from the Flask layer."""

    def __init__(self, image: "Image"):
        self._image = image

        self.root.mkdir(parents=True, exist_ok=True)

    @abc.abstractmethod
    def cache(self, force: bool) -> None:
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def proxies(self) -> list:
        pass  # pragma: no cover

    @property
    def image(self) -> "Image":
        return self._image

    @property
    def root(self) -> pathlib.Path:
        """Returns an absolute path to the proxy's root data directory.
        Transforms the original image path:

            /site-name/pages/page-name/image-name.ext

        ...to the site-cache path:

            /site-name/site-cache/pages/page-name/image-name
        """
        return (
            Globals.site_paths.cache
            / Defaults.DIRECTORY_NAME_PAGES
            / self.image.page.directory_name
            / self.image.name
        )


class ProxyImageManager(BaseProxyManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._small = ProxyImage(manager=self, config=Defaults.PROXY_IMAGE_SMALL)
        self._medium = ProxyImage(manager=self, config=Defaults.PROXY_IMAGE_MEDIUM)
        self._large = ProxyImage(manager=self, config=Defaults.PROXY_IMAGE_LARGE)

        self.cache()

    def cache(self, force: bool = False) -> None:

        if self.all_proxies_exist() and force is False:
            return

        with PIL.Image.open(self.image.path) as image:

            image = image.convert("RGB")

            # NOTE: The order of self.proxies here matters. Instead of loading
            # the image three times to create three resolutions, we load the
            # image once and resize it three times from largest to smallest.
            for image_proxy in self.proxies:

                if image_proxy.exists() and force is False:
                    continue

                logger.debug(
                    f"Generating {image_proxy.name}, {image_proxy.size[0]}px "
                    f"proxy image for '{self.image.filename}'."
                )

                image.thumbnail(image_proxy.size)

                image.save(
                    image_proxy.path,
                    format=Defaults.PROXY_IMAGE_FORMAT,
                    quality=Defaults.PROXY_IMAGE_QUALITY,
                )

    def all_proxies_exist(self) -> bool:
        return all(proxy.exists() for proxy in self.proxies)

    @property
    def proxies(self) -> List["ProxyImage"]:
        return [self.large, self.medium, self.small]

    @property
    def small(self) -> "ProxyImage":
        return self._small

    @property
    def medium(self) -> "ProxyImage":
        return self._medium

    @property
    def large(self) -> "ProxyImage":
        return self._large


class ProxyImage:
    def __init__(self, manager: "ProxyImageManager", config: dict):
        self._manager = manager

        # TODO:LOW Are we happy with the way these are being configured?
        self._name: str = config.get("name")  # type:ignore
        self._size: Tuple[int, int] = config.get("size")  # type:ignore

    def exists(self) -> bool:
        return self.path.exists()

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> Tuple[int, int]:
        return self._size

    @property
    def filename(self) -> str:
        return f"{self.name}{self._manager.image.extension}"

    @property
    def path(self) -> pathlib.Path:
        return self._manager.root / self.filename

    @property
    def src(self) -> pathlib.Path:
        return self.path.relative_to(Globals.site_paths.root)


class ProxyColorManager(BaseProxyManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._average = ProxyColor(
            manager=self, name="average", generate_color=self._generate_color__average
        )
        self._dominant = ProxyColor(
            manager=self, name="dominant", generate_color=self._generate_color__dominant
        )

        self.cache()

    def cache(self, force: bool = False) -> None:

        for proxy in self.proxies:
            proxy.load_or_generate(force=force)

    @property
    def proxies(self) -> List["ProxyColor"]:
        return [self.average, self.dominant]

    @property
    def average(self) -> "ProxyColor":
        return self._average

    def _generate_color__average(self) -> List[int]:

        with PIL.Image.open(self.image.path) as image:

            image = image.convert("RGB")
            image = image.resize((1, 1))
            color = image.getpixel((0, 0))

            return list(color)  # type:ignore

    @property
    def dominant(self) -> "ProxyColor":
        return self._dominant

    def _generate_color__dominant(self) -> List[int]:
        # TODO:LOW Need a better method for getting the dominant color.

        with PIL.Image.open(self.image.path) as image:

            image = image.convert("RGB")

            resolution = 32

            image.thumbnail((resolution, resolution), resample=0)

            """
                [
                    (frequency, (R, G, B)),
                    (frequency, (R, G, B)),
                    ...
                ]
            """
            pixel_data = image.getcolors(resolution * resolution)

            # Sort them by frequency.
            pixel_data_sorted = sorted(pixel_data, key=lambda i: i[0], reverse=True)

            # (frequency, (R, G, B))
            pixel_data_dominant = pixel_data_sorted[0]

            # (R, G, B)
            dominant_color = pixel_data_dominant[1]

            return list(dominant_color)  # type:ignore


class ProxyColor:
    def __init__(
        self, manager: "ProxyColorManager", name: str, generate_color: Callable
    ):
        self._manager = manager
        self._name = name
        self._generate_color = generate_color

        self._color: Optional[List[int]] = None

    # TODO:MED ProxyColor: load_or_generate, _load and _save need refactoring.

    def load_or_generate(self, force: bool = False) -> None:

        if self._color is not None and force is False:
            return

        if force is True:
            logger.debug(
                f"Generating '{self.name}' color data for '{self._manager.image.filename}'."
            )
            self.color = self._generate_color()
            self._save()
            return

        color = self._load()

        if color is None:
            logger.debug(
                f"Error/invalid color data in '{self.path.name}' for "
                f"'{self._manager.image.filename}'. Generating {self.name} "
                f"color data for '{self._manager.image.filename}'."
            )
            self.color = self._generate_color()
        else:
            self.color = color

        self._save()

    def _load(self) -> Optional[List[int]]:

        try:
            with open(self.path, "r") as f:
                color = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return

        if type(color) is not list:
            return

        return color

    def _save(self) -> None:

        with open(self.path, "w") as f:
            json.dump(self.color, f)

    def exists(self) -> bool:
        return self.path.exists()

    @property
    def color(self) -> List[int]:
        if self._color is None:
            return [0, 0, 0]
        return self._color

    @color.setter
    def color(self, value: List[int]) -> None:
        self._color = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def filename(self) -> str:
        return f"{self.name}.json"

    @property
    def path(self) -> pathlib.Path:
        return self._manager.root / self.filename

    @property
    def rgb(self) -> dict:
        """Returns the color as a dictionary. This is because this value needs
        to be passed to HTML then Javascript. It's easier to parse a dictionary
        in Javascript than a Tuple."""
        return {
            "R": self.color[0],
            "G": self.color[1],
            "B": self.color[2],
        }
