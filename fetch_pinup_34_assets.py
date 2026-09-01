from __future__ import annotations

import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "pinup-34"

PAGES = [
    ("cover", "https://www.pinupmagazine.org/issues/pinup-34-body-issue-travis-scott", 14),
    ("travis", "https://www.pinupmagazine.org/articles/travis-scott-design-alphabet", 8),
    ("jonathan", "https://www.pinupmagazine.org/articles/jonathan-anderson-interview", 6),
    ("gamper", "https://www.pinupmagazine.org/articles/martino-gamper-and-max-lamb-interview", 6),
    ("cerri", "https://www.pinupmagazine.org/articles/leather-rebel-pierluigi-cerri-80s-showpiece-has-lost-none-of-its-edge", 6),
    ("cfgny", "https://www.pinupmagazine.org/articles/cfgny-emporium-marsell", 7),
    ("luna", "https://www.pinupmagazine.org/articles/lunar-eclipse-luna-luna-art-amusement-park", 6),
    ("barney", "https://www.pinupmagazine.org/articles/matthew-barney-interview", 6),
]

UA = "Mozilla/5.0 XiaohongshuArchitectureEditorial/1.0"


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def images_on(url: str) -> list[str]:
    content = get(url).decode("utf-8", "ignore")
    values = re.findall(r'https?[^"\'\s<>]+', content)
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
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


def make_contact_sheet() -> None:
    files = sorted(OUT.glob("*.jpg")) + sorted(OUT.glob("*.png")) + sorted(OUT.glob("*.webp"))
    tw, th, gap = 184, 220, 16
    cols = 6
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * th + (rows + 1) * gap), "#c3c7c4")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(files):
        image = Image.open(path).convert("RGB")
        image.thumbnail((tw, th - 28), Image.Resampling.LANCZOS)
        x = gap + (index % cols) * (tw + gap)
        y = gap + (index // cols) * (th + gap)
        sheet.paste(image, (x + (tw - image.width) // 2, y))
        draw.rectangle((x, y + th - 28, x + tw, y + th), fill="#111820")
        draw.text((x + 5, y + th - 14), path.name, fill="#ffffff", anchor="lm")
    sheet.save(OUT / "contact-sheet.jpg", quality=92, subsampling=0)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    requested = set(sys.argv[1:])
    pages = [item for item in PAGES if not requested or item[0] in requested]
    jobs: list[tuple[Path, str]] = []
    for key, page, maximum in pages:
        urls = images_on(page)[:maximum]
        for index, url in enumerate(urls, 1):
            path = urllib.parse.urlsplit(url).path
            suffix = Path(path).suffix.lower()
            if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
                suffix = ".jpg"
            target = OUT / f"{key}-{index:02d}{suffix}"
            jobs.append((target, url))

    def download(job: tuple[Path, str]) -> str:
        target, url = job
        if not target.exists():
            target.write_bytes(get(url))
        return target.name

    with ThreadPoolExecutor(max_workers=8) as executor:
        for name in executor.map(download, jobs):
            print(name, flush=True)
    make_contact_sheet()


if __name__ == "__main__":
    main()
