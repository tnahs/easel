import argparse
import pathlib
import sys
from typing import Optional, Sequence

from .site.enums import E_Content
from .site import Site
from .site.globals import Globals


def main(argv: Optional[Sequence[str]] = None) -> int:

    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        type=pathlib.Path,
    )
    args = parser.parse_args(argv)

    site_root = args.path.resolve()

    if not site_root.exists():
        parser.error(f"site path '{site_root}' does not exist")

    Globals.site_root = site_root

    site = Site()

    print(site)
    for page in site.pages:
        print(f"  {page}")
        for content in page.contents:
            print(f"    {content}")
            if content.type == E_Content.IMAGE.value:
                print(f"      {content.src}")
            if content.type == E_Content.VIDEO.value:
                print(f"      {content.src}")
                print(f"      {content.mimetype}")

    # print(site.json(indent=4))

    return 0


if __name__ == "__main__":
    sys.exit(main())
