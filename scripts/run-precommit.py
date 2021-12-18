import argparse
import logging
import subprocess


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {name} {levelname}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)


logger = logging.getLogger()


def run__isort(verbose: bool = False) -> None:

    logger.info("Running isort...")

    command = ["isort", "./src", "./tests"]
    command.append("--verbose") if verbose is True else command.append("--quiet")

    subprocess.run(command)


def run__black(verbose: bool = False) -> None:

    logger.info("Running black...")

    command = ["black", "./src", "./tests"]
    command.append("--verbose") if verbose is True else command.append("--quiet")

    subprocess.run(command)


def run__pytest_coverage() -> None:

    logger.info("Testing python with 'pytest' and 'Coverage.py'...")

    coverage_pytest = ["coverage", "run", "-m", "pytest"]
    coverage_html = ["coverage", "html"]
    coverage_open = ["open", "./htmlcov/index.html"]

    subprocess.run(coverage_pytest)
    subprocess.run(coverage_html)
    subprocess.run(coverage_open)


def main() -> int:

    parser = argparse.ArgumentParser(
        add_help=False,
        description="Run all pre-commit scripts.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output.",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message.",
    )

    args = parser.parse_args()

    run__isort(verbose=args.verbose)
    run__black(verbose=args.verbose)
    run__pytest_coverage()

    return 0


if __name__ == "__main__":
    exit(main())
