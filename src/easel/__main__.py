import sys

import click

from . import Easel, __version__


@click.group()
@click.version_option(version=__version__)
@click.option("-s", "--site-root")
@click.option("-l", "--loglevel", default="INFO", show_default=True)
@click.option("--debug", is_flag=True)
@click.pass_context
def cli(context, site_root: str, loglevel: str, debug: bool) -> None:

    if "--help" in sys.argv:
        return

    context.obj = Easel(site_root, debug=debug, loglevel=loglevel)


@cli.command()
@click.option("-h", "--host")
@click.option("-p", "--port")
@click.option("--watch", is_flag=True)
@click.pass_obj
def serve(easel, watch: bool, host: str, port: str,) -> None:
    """ Serve the site. """

    easel.run(watch=watch, host=host, port=port)


@cli.command()
@click.pass_obj
def rebuild_site_cache(easel) -> None:
    """ Rebuild the site-cache. """

    easel.site.rebuild_cache()


if __name__ == "__main__":

    cli()
