from __future__ import annotations

import re

from io import BytesIO
from PIL import Image
from requests import Session

from .models import Option, PositionOfImage

_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"


def __get_page(ptimg: PositionOfImage, image: Image.Image) -> Image.Image:
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
        re.X,
    )
    for coord in view["coords"]:
        m = pattern.match(coord)
        if not m:
            raise ValueError(f"{coord!r} is not matched with expected pattern.")
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
            raise ValueError(f"'{base_url}/{page}.jpg' returns {image_res.status_code}")
        __get_page(
            ptimg_res.json(),
            Image.open(BytesIO(image_res.content)),
        ).save(
            chapter_dir / f"{page}.png",
        )
    return True


def __get_chapters(source: str) -> tuple[str, ...]:
    return tuple(
        str(chapter)
        for m in re.finditer(
            r'(?<=_epi)(\d+(?:_\d+)*)(?=")',
            source,
        )
        if isinstance(chapter := m.group(), str)
    )


def get_images(opt: Option) -> None:
    opt.save_dir /= opt.get_slug()
    opt.save_dir.mkdir(exist_ok=True, parents=True)

    with Session() as session:
        session.headers = {"user-agent": _UA}
        chapters = __get_chapters(session.get(opt.url.geturl()).text)
        chapters_len = len(chapters)
        print(f"[+] {chapters_len:04} chapter(s) found!")  # noqa: T201
        for idx, chapter in enumerate(chapters):
            print(f"[-] {idx + 1:04} / {chapters_len:04}...", end="", flush=True)  # noqa: T201
            print("..saved!" if __get_pages(opt, chapter, session) else "skipped!")  # noqa: T201


__all__ = ("get_images",)
