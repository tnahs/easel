import click.testing
import pytest

from easel.__main__ import cli

from .test_configs import TestSites


@pytest.fixture
def runner() -> click.testing.CliRunner:
    return click.testing.CliRunner()


def test__help(runner):

    result_01 = runner.invoke(cli, [])
    result_02 = runner.invoke(cli, ["--help"])

    assert result_01.exit_code == 0
    assert result_02.exit_code == 0


TEST_SITE_VALID = ["--testing", f"--site-root={TestSites.valid}"]


def test__serve(runner):

    default = runner.invoke(
        cli,
        [*TEST_SITE_VALID, "serve"],
    )

    debug = runner.invoke(
        cli,
        [*TEST_SITE_VALID, "--debug", "serve"],
    )

    loglevel = runner.invoke(
        cli,
        [*TEST_SITE_VALID, "--loglevel=DEBUG", "serve"],
    )

    custom = runner.invoke(
        cli,
        [*TEST_SITE_VALID, "serve", "--host=0.0.0.0", "--port=5000"],
    )

    watch = runner.invoke(
        cli,
        [*TEST_SITE_VALID, "serve", "--watch"],
    )

    assert default.exit_code == 0
    assert debug.exit_code == 0
    assert loglevel.exit_code == 0
    assert custom.exit_code == 0
    assert watch.exit_code == 0


def test__rebuild_site_cache(runner):

    result = runner.invoke(
        cli,
        [*TEST_SITE_VALID, "rebuild-site-cache"],
    )

    assert result.exit_code == 0
