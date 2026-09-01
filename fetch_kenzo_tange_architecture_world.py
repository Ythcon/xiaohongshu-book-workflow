#!/usr/bin/env python3
"""Fetch publisher-verified cover and eight real Kenzo Tange project photos."""
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
ASSETS = ROOT / "assets" / "kenzo-tange-architecture-world"
UA = "Codex-xhs-book-cards/1.0"
FILES = [
    ("02-hiroshima-wide.jpg", "广岛和平纪念资料馆外观", "Hiroshima Peace Memorial Museum 2009.jpg"),
    ("03-hiroshima-perspective.jpg", "广岛和平纪念资料馆透视", "Hiroshima Peace Memorial Museum (7170064954) (3).jpg"),
    ("04-yoyogi-exterior.jpg", "代代木国立体育馆外观", "Le stade national de Yoyogi (Tokyo, Japon) (40937712410).jpg"),
    ("05-yoyogi-interior.jpg", "代代木国立体育馆游泳馆室内", "Yoyogi National Gymnasium - Swim.jpg"),
    ("06-shizuoka.jpg", "静冈新闻广播中心", "Shizuoka Press and Broadcasting Center. Ginza, Tokyo..jpg"),
    ("07-st-marys.jpg", "东京圣玛利亚大教堂外观", "2018 St. Mary's Cathedral, Tokyo 2.jpg"),
    ("08-kurashiki.jpg", "仓敷市政厅", "Kurashiki City Hall (Kenzo Tange) 2 - panoramio.jpg"),
    ("09-tokyo-metropolitan.jpg", "东京都厅舍", "Tokyo Metropolitan Government Building Morning1.jpg"),
]

def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()

def get_bytes(url: str) -> bytes:
    last = None
    for retry in range(6):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(request, timeout=100) as response:
                return response.read()
        except Exception as exc:
            last = exc
            time.sleep(2 + retry)
    raise RuntimeError(f"Download failed: {url}: {last}")

def dimensions(data: bytes) -> tuple[int, int]:
    with Image.open(BytesIO(data)) as image:
        size = image.size
        image.verify()
    return size

def commons_records() -> dict[str, dict[str, str]]:
    query = urllib.parse.urlencode({"action": "query", "format": "json", "redirects": "1", "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": "1920", "titles": "|".join("File:" + name for _, _, name in FILES)})
    data = json.loads(get_bytes("https://commons.wikimedia.org/w/api.php?" + query))
    records = {}
    for page in data.get("query", {}).get("pages", {}).values():
        if "missing" in page:
            raise FileNotFoundError(page.get("title"))
        info = page["imageinfo"][0]
        metadata = info.get("extmetadata", {})
        get = lambda key: clean(metadata.get(key, {}).get("value"))
        records[page["title"].removeprefix("File:")] = {"download_url": info.get("thumburl") or info["url"], "source_url": info["descriptionurl"], "credit": get("Artist") or get("Credit") or "Wikimedia Commons contributor", "license": get("LicenseShortName") or get("UsageTerms") or "See source page", "license_url": get("LicenseUrl")}
    return records

def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    cover_url = "https://www.lars-mueller-publishers.com/sites/default/files/styles/open_graph_image/public/2026-04/Kenzo-Tange_new_1600_2.png?itok=ZLfkipd7"
    cover = ASSETS / "cover.png"
    cover.write_bytes(get_bytes(cover_url))
    cover_size = dimensions(cover.read_bytes())
    if min(cover_size) < 500:
        raise ValueError(f"Book cover too small: {cover_size}")
    manifest = [{"filename": "cover.png", "content": "Lars Müller 2012 英文精装版真实书封", "credit": "Lars Müller Publishers (book cover)", "source_url": "https://www.lars-mueller-publishers.com/kenzo-tange-architecture-world", "download_url": cover_url, "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人", "license_url": "", "modifications": "等比缩放与外部留白；未重绘或修改封面文字", "dimensions": list(cover_size)}]
    records = commons_records()
    for target, content, filename in FILES:
        record = records.get(filename)
        if not record:
            raise KeyError(filename)
        output = ASSETS / target
        output.write_bytes(get_bytes(record["download_url"]))
        size = dimensions(output.read_bytes())
        if min(size) < 500:
            raise ValueError(f"Image too small: {target}: {size}")
        manifest.append({"filename": target, "content": content, **record, "modifications": "裁切、缩放、轻微调色与图文排版", "dimensions": list(size)})
        print(target, size, record["license"])
        time.sleep(1.3)
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("cover.png", cover_size)

if __name__ == "__main__":
    main()
