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


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
def cache(directory: str) -> None:
    """ Serve an site from an Easel DIRECTORY. """

    easel = Easel(directory, loglevel="DEBUG")
    easel.site.build_cache(force=True)


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
def new(directory: str) -> None:
    """ Generate an new Easel scaffold inside a DIRECTORY. """
    pass


if __name__ == "__main__":

    cli()
