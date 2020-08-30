import click

from . import __version__
from . import Easel


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
def serve(directory: str) -> None:
    """ Serve an site from an Easel DIRECTORY. """

    easel = Easel(directory, loglevel="DEBUG")
    easel.run()


@cli.command("rebuild-cache")
@click.argument("directory", type=click.Path(exists=True))
def rebuild_cache(directory: str) -> None:
    """ Re-build Easel DIRECTORY cache. """

    easel = Easel(directory, loglevel="DEBUG")
    easel.rebuild_cache()


if __name__ == "__main__":

    cli()
