import click

from . import Easel, __version__


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    pass


@cli.command()
@click.option("-s", "--site-root")
@click.option("-l", "--loglevel", default="INFO", show_default=True)
@click.option("--debug/--no-debug", default=True)
@click.option("-h", "--host")
@click.option("-p", "--port")
def serve(site_root: str, loglevel: str, debug: bool, host: str, port: str) -> None:
    """ Serve an Easel site. """

    easel = Easel(site_root, debug=debug, loglevel=loglevel)
    easel.run(host=host, port=port)


if __name__ == "__main__":

    cli()
