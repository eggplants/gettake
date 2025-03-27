"""Models for gettake."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from pathlib import Path
    from urllib.parse import ParseResult


@dataclass
class Option:
    """CLI Options for gettake."""

    url: ParseResult
    save_dir: Path
    overwrite: bool
    quiet: bool

    def get_file_url(self, chapter: str) -> str:
        """Get file url.

        Args:
            chapter (str): chapter name.

        Returns:
                str: file url.
        """
        file_url = self.url._replace(
            path=f"/_files/{self.get_slug()}/{chapter}/data",
        )
        return file_url.geturl()

    def get_slug(self) -> str:
        """Get slug from url.

        Returns:
            str: slug.
        """
        return self.url.path.rstrip("/").split("/")[-1]


class ImageInfo(TypedDict):
    src: str
    width: int
    height: int


class Resources(TypedDict):
    i: ImageInfo


class View(TypedDict):
    width: int
    height: int
    coords: list[str]


PositionOfImage = TypedDict(
    "PositionOfImage",
    {
        "ptimg-version": Literal[1],
        "resources": Resources,
        "views": list[View],
    },
)


__all__ = ("Option", "PositionOfImage")
