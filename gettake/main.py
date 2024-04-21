from __future__ import annotations

import re
import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse
from shutil import get_terminal_size

from . import __version__
from .gettake import get_images
from .models import Option

if TYPE_CHECKING:
    from urllib.parse import ParseResult

# https://webcomicgamma.takeshobo.co.jp/manga/madeinabyss/

VALID_HOSTS = ("webcomicgamma.takeshobo.co.jp",)


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def available_list() -> str:
    return "available urls:\n  - https://" + "\n  - https://".join(VALID_HOSTS)


def check_url(s: str) -> ParseResult:
    url = urlparse(s)
    if url.hostname in VALID_HOSTS and re.match("^/manga/[^/]+/?$", url.path):
        return url
    raise argparse.ArgumentTypeError(f"'{s}' is invalid.\n" + available_list())


def check_dir(s: str) -> Path:
    if s == ".":
        return Path().cwd()
    path = Path(s)
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"'{s}' is not dir.")
    return path


def parse_args(test: list[str] | None = None) -> Option:
    """Parse arguments."""
    parser = argparse.ArgumentParser(
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
    )


def main(test: list[str] | None = None) -> None:
    opt = parse_args(test)
    get_images(opt)


if __name__ == "__main__":
    main()
