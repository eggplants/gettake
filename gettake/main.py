"""Main module for gettake."""

from __future__ import annotations

import re
import sys
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    ArgumentTypeError,
    RawDescriptionHelpFormatter,
)
from pathlib import Path
from shutil import get_terminal_size
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from . import __version__
from .gettake import get_images
from .models import Option

if TYPE_CHECKING:
    from urllib.parse import ParseResult

VALID_HOSTS = ("webcomicgamma.takeshobo.co.jp",)


class CustomFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
    """Custom formatter for argparse."""


def available_list() -> str:
    """Return available urls.

    Returns:
        str: available urls.
    """
    return "available urls:\n  - https://" + "\n  - https://".join(VALID_HOSTS)


def check_url(s: str) -> ParseResult:
    """Check if s is a valid url.

    Args:
        s (str): url to check.

    Raises:
        argparse.ArgumentTypeError: if s is invalid.

    Returns:
        ParseResult: url object.
    """
    url = urlparse(s)
    if url.hostname in VALID_HOSTS and re.match("^/manga/[^/]+/?$", url.path):
        return url
    raise ArgumentTypeError(f"'{s}' is invalid.\n" + available_list())


def check_dir(s: str) -> Path:
    """Check if s is a valid directory.

    Args:
        s (str): path to check.

    Raises:
        argparse.ArgumentTypeError: if s is not a directory.

    Returns:
        Path: path object.
    """
    if s == ".":
        return Path().cwd()
    path = Path(s)
    if not path.is_dir():
        msg = f"{s!r} is not dir."
        raise ArgumentTypeError(msg)
    return path


def parse_args(test: list[str] | None = None) -> Option:
    """Parse arguments.

    Args:
        test (list[str] | None): test args. Defaults to None.

    Returns:
            Option: cli options.

    Raises:
            ArgumentTypeError: if url is invalid.
    """
    parser = ArgumentParser(
        formatter_class=(
            lambda prog: CustomFormatter(
                prog,
                width=get_terminal_size(fallback=(120, 50)).columns,
                max_help_position=25,
            )
        ),
        description="Get and save images from webcomicgamma.",
        epilog=available_list(),
    )

    parser.add_argument(
        "url",
        metavar="url",
        type=check_url,
        help="target url",
    )
    parser.add_argument(
        "-d",
        "--save-dir",
        type=check_dir,
        metavar="DIR",
        default=".",
        help="directory to save downloaded images",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="overwrite",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="keep stdout quiet",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)

    if test:
        args = parser.parse_args(test)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    else:
        args = parser.parse_args()
    return Option(
        url=args.url,
        save_dir=args.save_dir,
        overwrite=args.overwrite,
        quiet=args.quiet,
    )


def _main(test: list[str] | None = None) -> None:
    """Main function.

    Args:
        test (list[str] | None): test args. Defaults to None.
    """
    opt = parse_args(test)
    if not opt.quiet:
        print(f"[+] Target: {opt.url.geturl()}")
        print(f"[+] Host:   {opt.url.hostname}")
        print(f"[+] Slug:   {opt.get_slug()}")
    get_images(opt)
    if not opt.quiet:
        print("[+] Done!")


def main() -> None:
    """Main function."""
    try:
        _main()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
