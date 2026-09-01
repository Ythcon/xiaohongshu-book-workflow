#!/usr/bin/env python3
"""Fetch the verified book cover and eight real I. M. Pei project photographs."""

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
ASSET_ROOT = ROOT / "assets" / "im-pei-conversations-light-is-key"
USER_AGENT = "Codex-xhs-book-cards/1.0"

FILES = [
    ("02-luce-chapel.jpg", "路思义教堂建筑实景", "Luce Memorial Chapel - Tunghai University - DSC01491.JPG"),
    ("03-ncar.jpg", "美国国家大气研究中心 Mesa 实验室实景", "National Center for Atmospheric Research (NCAR) Mesa Laboratory in Boulder, Colorado, USA in 2014.jpg"),
    ("04-nga-east.jpg", "美国国家美术馆东馆实景", "National Gallery of Art, East Building.jpg"),
    ("05-louvre.jpg", "卢浮宫金字塔与拿破仑庭院实景", "Louvre Courtyard, Looking West.jpg"),
    ("06-bank-china.jpg", "香港中银大厦仰视实景", "Looking up to the Bank of China Tower in Hong Kong.jpg"),
    ("07-miho.jpg", "美秀美术馆主厅实景", "Main hall of the Miho museum, designed by I M Pei (of NCAR and the Louvre pyramid) (4157420538).jpg"),
    ("08-suzhou.jpg", "苏州博物馆室内望向庭院的实景", "Suzhou Museum garden view from inside.jpg"),
    ("09-mia-doha.jpg", "多哈伊斯兰艺术博物馆实景", "Museum of Islamic Art, Doha (54704206856).jpg"),
]


def clean_html(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()


def request_bytes(url: str) -> bytes:
    last_error = None
    for attempt in range(7):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=100) as response:
                return response.read()
        except Exception as error:
            last_error = error
            time.sleep(3.2 * (attempt + 1))
    raise RuntimeError(f"download failed: {url}: {last_error}")


def commons_records() -> dict[str, dict[str, str]]:
    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size",
        "iiurlwidth": "1920",
        "titles": "|".join("File:" + filename for _, _, filename in FILES),
    })
    payload = json.loads(request_bytes("https://commons.wikimedia.org/w/api.php?" + params))
    records = {}
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


def image_dimensions(data: bytes) -> tuple[int, int]:
    with Image.open(BytesIO(data)) as image:
        size = image.size
        image.verify()
    return size


def main() -> None:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    cover = ASSET_ROOT / "cover.jpg"
    if not cover.exists() or cover.stat().st_size < 10_000:
        cover.write_bytes(request_bytes("https://covers.openlibrary.org/b/id/1027009-L.jpg"))
    cover_size = image_dimensions(cover.read_bytes())
    manifest = [{
        "filename": "cover.jpg",
        "content": "2000 年 Prestel 英文版真实书封",
        "credit": "Gero von Boehm / I. M. Pei / Prestel (book cover)",
        "source_url": "https://openlibrary.org/books/OL9104394M/Conversations_With_I._M._Pei",
        "download_url": "https://covers.openlibrary.org/b/id/1027009-L.jpg",
        "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        "license_url": "",
        "modifications": "等比缩放与外部留白；未重绘或修改封面文字",
        "dimensions": list(cover_size),
    }]
    records = commons_records()
    for target, content, filename in FILES:
        record = records[filename]
        path = ASSET_ROOT / target
        if not path.exists() or path.stat().st_size < 10_000:
            path.write_bytes(request_bytes(record["download_url"]))
        size = image_dimensions(path.read_bytes())
        if min(size) < 700:
            raise ValueError(f"case image too small: {target} {size}")
        manifest.append({
            "filename": target,
            "content": content,
            **record,
            "modifications": "裁切、缩放、轻微调色与图文排版",
            "dimensions": list(size),
        })
        print(target, *size, record["license"])
        time.sleep(2.4)
    (ASSET_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("cover.jpg", *cover_size)


if __name__ == "__main__":
    main()
