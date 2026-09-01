from __future__ import annotations

import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "pinup-33"
UA = "Mozilla/5.0 XiaohongshuArchitectureEditorial/1.0"

PAGES = [
    ("cover", "https://www.pinupmagazine.org/issues/pinup-33-new-americana-usm-nyc-ben-ganz", 12),
    ("paige", "https://www.pinupmagazine.org/articles/robert-paige-interview", 7),
    ("olowu", "https://www.pinupmagazine.org/articles/duro-olowu-interview", 7),
    ("cape", "https://www.pinupmagazine.org/articles/cape-cod-essay-bauhaus-new-alchemy-institute-architecture", 10),
    ("barbie", "https://www.pinupmagazine.org/articles/barbie-dreamhouse-architectural-survey", 8),
    ("olivares", "https://www.pinupmagazine.org/articles/jonathan-olivares-interview", 7),
    ("newwave", "https://www.pinupmagazine.org/articles/new-wave-americana-alexander-may-sized", 10),
    ("bambole", "https://www.pinupmagazine.org/articles/beb-italia-bambole-grace-ahlbom", 10),
    ("sandiego", "https://www.pinupmagazine.org/articles/san-diego-a-bilateral-city-nicholas-alan-cope", 9),
]


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def images_on(page_url: str) -> list[str]:
    html = get(page_url).decode("utf-8", "ignore")
    seen: set[str] = set()
    output: list[str] = []
    for value in re.findall(r'https?[^"\'\s<>]+', html):
        value = value.replace("&amp;", "&")
        if "cdn.sanity.io/images/o4aog1mm/production/" not in value:
            continue
        parsed = urllib.parse.urlsplit(value)
        base = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
        if base in seen:
            continue
        seen.add(base)
        output.append(base + "?w=1400&auto=format")
    return output


def contact_sheet() -> None:
    files = [p for p in sorted(OUT.glob("*.*")) if p.name != "contact-sheet.jpg" and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    tw, th, gap, cols = 184, 220, 16, 6
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * th + (rows + 1) * gap), "#c6c8c4")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(files):
        image = Image.open(path).convert("RGB")
        image.thumbnail((tw, th - 28), Image.Resampling.LANCZOS)
        x = gap + (index % cols) * (tw + gap)
        y = gap + (index // cols) * (th + gap)
        sheet.paste(image, (x + (tw - image.width) // 2, y))
        draw.rectangle((x, y + th - 28, x + tw, y + th), fill="#151719")
        draw.text((x + 5, y + th - 14), path.name, fill="#ffffff", anchor="lm")
    sheet.save(OUT / "contact-sheet.jpg", quality=92, subsampling=0)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    requested = set(sys.argv[1:])
    pages = [item for item in PAGES if not requested or item[0] in requested]
    jobs: list[tuple[Path, str]] = []
    for key, page_url, maximum in pages:
        for index, url in enumerate(images_on(page_url)[:maximum], 1):
            suffix = Path(urllib.parse.urlsplit(url).path).suffix.lower()
            if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
                suffix = ".jpg"
            jobs.append((OUT / f"{key}-{index:02d}{suffix}", url))

    def download(job: tuple[Path, str]) -> str:
        target, url = job
        if not target.exists():
            target.write_bytes(get(url))
        return target.name

    with ThreadPoolExecutor(max_workers=8) as executor:
        for name in executor.map(download, jobs):
            print(name, flush=True)
    contact_sheet()


if __name__ == "__main__":
    main()
