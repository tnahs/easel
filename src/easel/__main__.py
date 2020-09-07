import logging

import click

from . import Easel, __version__


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
def serve(directory: str) -> None:
    """ Serve an site from an Easel DIRECTORY. """

    easel = Easel(directory, loglevel=logging.DEBUG)
    easel.run()


@cli.command("rebuild-cache")
@click.argument("directory", type=click.Path(exists=True))
def rebuild_cache(directory: str) -> None:
    """ Re-build cache from an Easel DIRECTORY. """

    easel = Easel(directory, loglevel=logging.INFO)
    easel.site.rebuild_cache()


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
