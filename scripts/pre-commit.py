import os
import argparse
import pathlib
import subprocess
from typing import List
import logging


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {name} {levelname}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)


logger = logging.getLogger()


THEME_NAMES: List[str] = [
    "sorolla",
    # "sargent"
]


def run__isort(verbose: bool = False):

    logger.info("Sorting Python imports with 'isort'...")

    isort_command = ["isort", "./src", "./tests"]

    if verbose is True:
        isort_command.append("--verbose")
    else:
        isort_command.append("--quiet")

    subprocess.run(isort_command)


def run__black(verbose: bool = False):

    logger.info("Formatting Python with 'Black'...")

    black_command = ["black", "./src", "./tests"]

    if verbose is True:
        black_command.append("--verbose")
    else:
        black_command.append("--quiet")

    subprocess.run(black_command)


def run__build_themes(verbose: bool = False):

    for theme_name in THEME_NAMES:

        theme_root = pathlib.Path(f"./src/easel/themes/{theme_name}").resolve()
        theme_src = theme_root / "src"
        theme_dist = theme_root / theme_name

        # Prettier

        logger.info(
            f"Theme '{theme_name}': Formatting SCSS and Typescript with 'Prettier'..."
        )

        prettier = theme_root / "node_modules/prettier/bin-prettier.js"
        prettierrc = theme_root / ".prettierrc"

        prettier_command = [
            str(prettier),
            str(theme_src / "scss/**/*.scss"),
            str(theme_src / "typescript/**/*.ts"),
            f"--config={prettierrc}",
            "--write",
        ]

        if verbose is True:
            prettier_command.append("--loglevel=debug")
        else:
            prettier_command.append("--loglevel=silent")

        subprocess.run(prettier_command)

        # Gulp

        logger.info(
            f"Theme '{theme_name}': Compiling CSS and Javascript with 'Gulp'..."
        )

        gulp = theme_root / "node_modules/gulp/bin/gulp.js"
        gulpfile = theme_root / "gulpfile.js"

        gulp_command = [
            str(gulp),
            f"--gulpfile={gulpfile}",
            f"--cwd={theme_root}",
            "build",
        ]

        if verbose is True:
            gulp_command.append("--loglevel=4")
        else:
            gulp_command.append("--silent")

        subprocess.run(gulp_command)

        # Trim

        logger.info(f"Theme '{theme_name}': Trimming unused CSS files...")

        theme_dist_css = theme_dist / "css"

        css = sorted(
            theme_dist_css.glob("*.css"),
            key=os.path.getctime,
        )
        css.pop()

        logger.info(f"Theme '{theme_name}': Trimming unused Javascript files...")

        theme_dist_javascript = theme_dist / "javascript"

        javascript = sorted(
            theme_dist_javascript.glob("*.js"),
            key=os.path.getctime,
        )
        javascript.pop()

        for path in [*css, *javascript]:
            path.unlink()


def run__pytest_coverage(verbose: bool = False):

    logger.info("Testing Python with 'pytest' and 'Coverage.py'...")

    coverage_pytest = ["coverage", "run", "-m", "pytest"]
    coverage_html = ["coverage", "html"]
    coverage_open = ["open", "./htmlcov/index.html"]

    subprocess.run(coverage_pytest)
    subprocess.run(coverage_html)
    subprocess.run(coverage_open)


def main(verbose: bool):
    run__isort(verbose=verbose)
    run__black(verbose=verbose)
    run__build_themes(verbose=verbose)
    run__pytest_coverage(verbose=verbose)


parser = argparse.ArgumentParser(add_help=False)

# fmt: off
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Verbose output."
)
parser.add_argument(
    "-h",
    "--help",
    action="help",
    default=argparse.SUPPRESS,
    help="Show this help message."
)
# fmt:on

args = parser.parse_args()

if __name__ == "__main__":

    main(verbose=args.verbose)
