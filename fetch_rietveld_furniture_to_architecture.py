#!/usr/bin/env python3
"""Fetch publisher cover and eight verified Rietveld Schröder House photographs."""
from __future__ import annotations
import html, json, re, time, urllib.parse, urllib.request
from io import BytesIO
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "rietveld-furniture-to-architecture"
UA = "Codex-xhs-book-cards/1.0"
COVER_URL = "http://www.phaidon.com/cdn/shop/files/9780714873206-Gerrit-Rietveld-3D-standing-1to1_75a65aef-c0ad-47f2-814b-385b5450e015.jpg?v=1764656206"
FILES = [
    ("02-facade.jpg", "施罗德住宅｜外立面与阳台", "Casa Rietveld Schröder 01.jpg"),
    ("03-side.jpg", "施罗德住宅｜侧立面", "Casa Rietveld Schröder 02.jpg"),
    ("04-stair.jpg", "施罗德住宅｜楼梯与竖向动线", "Casa Rietveld Schröder 03.jpg"),
    ("05-window.jpg", "施罗德住宅｜窗与可变边界", "Casa Rietveld Schröder 05.jpg"),
    ("06-balcony.jpg", "施罗德住宅｜阳台与街道", "Casa Rietveld Schröder 06.jpg"),
    ("07-corner.jpg", "施罗德住宅｜转角与悬挑", "Casa Rietveld Schröder 07.jpg"),
    ("08-opening.jpg", "施罗德住宅｜开口与室内外关系", "Casa Rietveld Schröder 08.jpg"),
    ("09-open-corner.jpg", "施罗德住宅｜可打开转角", "Casa Rietveld Schröder 10 angolo a scomparsa.jpg"),
]

def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()

def get_bytes(url: str) -> bytes:
    last = None
    for retry in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=100) as response:
                return response.read()
        except Exception as exc:
            last = exc
            time.sleep(2 + retry)
    raise RuntimeError(f"Download failed: {url}: {last}")

def image_size(data: bytes) -> tuple[int, int]:
    with Image.open(BytesIO(data)) as image:
        value = image.size
        image.verify()
    return value

def records() -> dict[str, dict[str, str]]:
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "redirects": "1", "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "iiurlwidth": "1920",
        "titles": "|".join("File:" + filename for _, _, filename in FILES),
    })
    data = json.loads(get_bytes("https://commons.wikimedia.org/w/api.php?" + params))
    found = {}
    for page in data.get("query", {}).get("pages", {}).values():
        if "missing" in page:
            raise FileNotFoundError(page.get("title"))
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        field = lambda name: clean(meta.get(name, {}).get("value"))
        found[page["title"].removeprefix("File:")] = {
            "download_url": info.get("thumburl") or info["url"], "source_url": info["descriptionurl"],
            "credit": field("Artist") or field("Credit") or "Wikimedia Commons contributor",
            "license": field("LicenseShortName") or field("UsageTerms") or "See source page",
            "license_url": field("LicenseUrl"),
        }
    return found

def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    cover = ASSETS / "cover.jpg"
    if not cover.exists() or cover.stat().st_size < 10000:
        cover.write_bytes(get_bytes(COVER_URL))
    cover_dimensions = image_size(cover.read_bytes())
    if min(cover_dimensions) < 500:
        raise ValueError(f"cover too small: {cover_dimensions}")
    manifest = [{
        "filename": "cover.jpg", "content": "Phaidon 英文版《Gerrit Rietveld》真实书封（官方产品图）",
        "credit": "Phaidon (book cover)", "source_url": "https://www.phaidon.com/en-gb/products/gerrit-rietveld",
        "download_url": COVER_URL, "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人", "license_url": "",
        "modifications": "等比缩放与外部留白；未重绘或修改封面文字", "dimensions": list(cover_dimensions),
    }]
    source = records()
    for target, content, filename in FILES:
        record = source[filename]
        output = ASSETS / target
        if not output.exists() or output.stat().st_size < 10000:
            output.write_bytes(get_bytes(record["download_url"]))
        dimensions = image_size(output.read_bytes())
        if min(dimensions) < 500:
            raise ValueError(f"image too small: {target} {dimensions}")
        manifest.append({"filename": target, "content": content, **record, "modifications": "裁切、缩放、轻微调色与图文排版", "dimensions": list(dimensions)})
        print(target, dimensions, record["license"])
        time.sleep(0.8)
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("cover.jpg", cover_dimensions)

if __name__ == "__main__":
    main()
