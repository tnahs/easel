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
    """ Re-build cache from an Easel DIRECTORY. """

    easel = Easel(directory, loglevel="DEBUG")
    easel.rebuild_cache()


@click.group()
def new() -> None:
    pass


@new.command()
@click.argument("directory", type=click.Path(exists=True))
@click.argument("name")
def site(directory: str, name: str) -> None:
    """ Create a new Easel DIRECTORY scaffold with NAME. """
    pass


if __name__ == "__main__":

    cli()
