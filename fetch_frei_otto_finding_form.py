#!/usr/bin/env python3
"""Fetch a verified Finding Form cover and eight real Frei Otto project photos."""

from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "frei-otto-finding-form"
USER_AGENT = "Codex-xhs-book-cards/1.0"

FILES = [
    ("02-expo67.jpg", "1967 年蒙特利尔世博会德国馆室内实景", "Expo 67 Montreal Canada (4).jpg"),
    ("03-il-stuttgart.jpg", "斯图加特轻型结构研究所（原世博德国馆试验建筑）实景", "0134-Stuttgart-Otto.jpg"),
    ("04-munich-wide.jpg", "慕尼黑奥林匹克公园张拉屋顶实景", "Munich - Frei Otto Tensed structures - 5406.jpg"),
    ("05-munich-detail.jpg", "慕尼黑奥林匹克屋顶膜结构细部实景", "Olympic Roof Munich, July 2018 -02.jpg"),
    ("06-multihalle-outside.jpg", "曼海姆多功能厅格栅壳外部实景", "Multihalle07.jpg"),
    ("07-multihalle-inside.jpg", "曼海姆多功能厅大空间内部实景", "Multihalle Mannheim, Innenraum große Halle.jpg"),
    ("08-multihalle-entry.jpg", "曼海姆多功能厅东入口实景", "Multihalle10.jpg"),
    ("09-munich-stadium.jpg", "慕尼黑奥林匹克体育场与张拉屋顶实景", "Munich - Frei Otto Tensed structures - 5293.jpg"),
]

# The two remaining Commons thumbnails intermittently time out on the CDN.
# Special:FilePath is still the original Commons file route and preserves the
# same attribution record queried below.
SPECIAL_DOWNLOADS = {}


def clean_html(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()


def request_bytes(url: str) -> bytes:
    last_error = None
    for attempt in range(6):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except Exception as error:
            last_error = error
            time.sleep(2.5 * (attempt + 1))
    raise RuntimeError(f"download failed: {url}: {last_error}")


def image_size(data: bytes) -> tuple[int, int]:
    with Image.open(BytesIO(data)) as image:
        size = image.size
        image.verify()
    return size


def commons_records() -> dict[str, dict[str, str]]:
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "redirects": "1",
        "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": "1920",
        "titles": "|".join("File:" + filename for _, _, filename in FILES),
    })
    payload = json.loads(request_bytes("https://commons.wikimedia.org/w/api.php?" + params))
    records: dict[str, dict[str, str]] = {}
    for page in payload["query"]["pages"].values():
        if "missing" in page:
            raise FileNotFoundError(page.get("title"))
        info = page["imageinfo"][0]
        metadata = info.get("extmetadata", {})
        get = lambda key: clean_html(metadata.get(key, {}).get("value"))
        filename = page["title"].removeprefix("File:")
        records[filename] = {
            "download_url": info.get("thumburl") or info["url"],
            "source_url": info["descriptionurl"],
            "credit": get("Artist") or get("Credit") or "Wikimedia Commons contributor",
            "license": get("LicenseShortName") or get("UsageTerms") or "See source page",
            "license_url": get("LicenseUrl"),
        }
    return records


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    # Official Simon & Schuster / Edition Axel Menges high-resolution cover asset.
    cover_url = "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9783930698660/finding-form-9783930698660_hr.jpg"
    cover_path = ASSETS / "cover.jpg"
    if not cover_path.exists() or cover_path.stat().st_size < 10_000:
        cover_path.write_bytes(request_bytes(cover_url))
    cover_size = image_size(cover_path.read_bytes())
    if min(cover_size) < 250:
        raise ValueError(f"cover is too small: {cover_size}")

    manifest = [{
        "filename": "cover.jpg",
        "content": "Edition Axel Menges 英文精装版真实书封",
        "credit": "Frei Otto / Bodo Rasch / Edition Axel Menges (book cover)",
        "source_url": "https://www.simonandschuster.com/books/Finding-Form/Frei-Otto/9783930698660",
        "download_url": cover_url,
        "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        "license_url": "",
        "modifications": "等比缩放与外部留白；未重绘或修改封面文字",
        "dimensions": list(cover_size),
    }]

    records = commons_records()
    for target, content, filename in FILES:
        record = records.get(filename)
        if not record:
            raise KeyError(f"Commons record not found: {filename}")
        if filename in SPECIAL_DOWNLOADS:
            record["download_url"] = SPECIAL_DOWNLOADS[filename]
        path = ASSETS / target
        if not path.exists() or path.stat().st_size < 10_000:
            path.write_bytes(request_bytes(record["download_url"]))
        size = image_size(path.read_bytes())
        if min(size) < 700:
            raise ValueError(f"case image too small: {target} {size}")
        manifest.append({
            "filename": target, "content": content, **record,
            "modifications": "裁切、缩放、轻微调色与图文排版",
            "dimensions": list(size),
        })
        print(target, *size, record["license"])
        time.sleep(1.6)

    (ASSETS / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("cover.jpg", *cover_size)


if __name__ == "__main__":
    main()
