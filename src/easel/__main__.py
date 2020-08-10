import click

from . import __version__


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
def template(directory: str) -> None:
    """ Generate an Easel template inside a DIRECTORY. """
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--gallery", "is_gallery", is_flag=True, help="Generate as gallery.")
def layout_page(directory: str, is_gallery: bool) -> None:
    """ Auto-generate a page.yaml for a Layout page from a DIRECTORY. """
    pass


if __name__ == "__main__":

    cli()
