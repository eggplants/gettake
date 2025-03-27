"""Get and save images by chapters from specified work page."""

from __future__ import annotations

import re
from io import BytesIO
from typing import TYPE_CHECKING

from PIL import Image
from requests import Session

if TYPE_CHECKING:
    from .models import Option, PositionOfImage

_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)


def __get_page(ptimg: PositionOfImage, image: Image.Image) -> Image.Image:
    """Get a page image from ptimg and image.

    Args:
        ptimg (PositionOfImage): ptimg.json
        image (Image.Image): scrumbled image data.

    Returns:
        Image.Image: decoded image
    """
    view = ptimg["views"][0]
    decoded_image = Image.new("RGB", (view["width"], view["height"]))
    pattern = re.compile(
        r"""^
        i:(?P<sx>\d+),(?P<sy>\d+)
        \+
        (?P<sxoff>\d+),(?P<syoff>\d+)
        \>
        (?P<dx>\d+),(?P<dy>\d+)
        $""",
        re.VERBOSE,
    )
    for coord in view["coords"]:
        m = pattern.match(coord)
        if not m:
            msg = f"{coord!r} is not matched with expected pattern."
            raise ValueError(msg)
        (
            sx,
            sy,
            sxoff,
            syoff,
            dx,
            dy,
        ) = (
            int(m["sx"]),
            int(m["sy"]),
            int(m["sxoff"]),
            int(m["syoff"]),
            int(m["dx"]),
            int(m["dy"]),
        )
        decoded_image.paste(
            image.crop(
                (
                    sx,
                    sy,
                    sx + sxoff,
                    sy + syoff,
                ),
            ),
            (dx, dy),
        )
    return decoded_image


def __get_pages(opt: Option, chapter: str, session: Session) -> bool:
    """Get pages from specified chapter.

    Args:
        opt (Option): cli options.
        chapter (str): chapter name.
        session (Session): requests session.

    Raises:
        ValueError: if image response is not ok.

    Returns:
        bool: True if saved, False if skipped.
    """
    chapter_dir = opt.save_dir / chapter
    if chapter_dir.is_dir() and not opt.overwrite:
        return False
    chapter_dir.mkdir(exist_ok=True, parents=True)

    base_url = opt.get_file_url(chapter)
    for page_idx in range(1, 10000):
        page = f"{page_idx:04}"
        ptimg_res = session.get(f"{base_url}/{page}.ptimg.json")
        if not ptimg_res.ok:
            break
        image_res = session.get(f"{base_url}/{page}.jpg")
        if not image_res.ok:
            msg = f"{image_res.url!r} returns {image_res.status_code}"
            raise ValueError(msg)
        __get_page(
            ptimg_res.json(),
            Image.open(BytesIO(image_res.content)),
        ).save(
            chapter_dir / f"{page}.png",
        )
    return True


def __get_chapters(source: str) -> list[str]:
    """Get chapters from source.

    Args:
        source (str): source of the page.

    Returns:
        list[str]: chapters.
    """
    return sorted(
        {
            m.group()
            for m in re.finditer(
                r'(?<=_epi)(\d+(?:_\d+)*)(?=")',
                source,
            )
        },
    )


def get_images(opt: Option) -> None:
    """Get images from specified url.

    Args:
        opt (Option): cli options.
    """
    opt.save_dir /= opt.get_slug()
    opt.save_dir.mkdir(exist_ok=True, parents=True)

    session = Session()

    session.headers = {"user-agent": _UA}
    chapters = __get_chapters(session.get(opt.url.geturl()).text)
    chapters_len = len(chapters)
    print(f"[+] {chapters_len:04} chapter(s) found!")  # noqa: T201
    for idx, chapter in enumerate(chapters):
        if not opt.quiet:
            print(  # noqa: T201
                f"[-] Now: {chapter!r} [{idx + 1:04} / {chapters_len:04}] ...",
                end="",
                flush=True,
            )
        skipped = __get_pages(opt, chapter, session)
        if not opt.quiet:
            print("..saved!" if skipped else "skipped!")  # noqa: T201

    session.close()


__all__ = ("get_images",)
