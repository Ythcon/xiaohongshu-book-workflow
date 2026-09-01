#!/usr/bin/env python3
"""Fetch the verified Getty edition cover and eight real Otto Wagner project photos."""

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
ASSET_ROOT = ROOT / "assets" / "otto-wagner-modern-architecture"
USER_AGENT = "Codex-xhs-book-cards/1.0"

FILES = [
    ("02-villa-i.jpg", "奥托·瓦格纳第一别墅建筑实景", "Wagner Villa.jpg"),
    ("03-nussdorf.jpg", "努斯多夫水闸与舍梅尔桥建筑实景", "Otto Wagner Schemerlbrücke Vienna - 04 (8677924964).jpg"),
    ("04-hofpavillon.jpg", "希青宫廷车站建筑实景", "Hietzing (Wien) - Hofpavillon.JPG"),
    ("05-karlsplatz.jpg", "卡尔广场城铁亭建筑实景", "Otto Wagner Pavillon - Karlsplatz.jpg"),
    ("06-majolica.jpg", "马约利卡住宅立面实景", "Majolica House facade.jpg"),
    ("07-postsparkasse.jpg", "奥地利邮政储蓄银行建筑实景", "Otto Wagner Postsparkasse Hauptfront.jpg"),
    ("08-steinhof.jpg", "施泰因霍夫教堂建筑实景", "Wien - Steinhof - Otto-Wagner-Kirche.jpg"),
    ("09-schuetzenhaus.jpg", "多瑙运河水闸控制室建筑实景", "Schuetzenhaus Donaukanal Wien DSC 9948w.jpg"),
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
            time.sleep(3.0 * (attempt + 1))
    raise RuntimeError(f"download failed: {url}: {last_error}")


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
    for item in payload.get("query", {}).get("normalized", []) + payload.get("query", {}).get("redirects", []):
        old = item["from"].removeprefix("File:")
        new = item["to"].removeprefix("File:")
        if new in records:
            records[old] = records[new]
    return records


def image_dimensions(data: bytes) -> tuple[int, int]:
    with Image.open(BytesIO(data)) as image:
        size = image.size
        image.verify()
    return size


def main() -> None:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    cover_url = "https://covers.openlibrary.org/b/isbn/0226869393-L.jpg"
    cover = ASSET_ROOT / "cover.jpg"
    if not cover.exists() or cover.stat().st_size < 8_000:
        cover.write_bytes(request_bytes(cover_url))
    cover_size = image_dimensions(cover.read_bytes())
    if min(cover_size) < 250:
        raise ValueError(f"book cover too small or missing: {cover_size}")

    manifest = [{
        "filename": "cover.jpg",
        "content": "1988 年 Getty 英文版真实书封",
        "credit": "Otto Wagner / Harry Francis Mallgrave / Getty Research Institute (book cover)",
        "source_url": "https://www.getty.edu/publications/virtuallibrary/0226869393.html",
        "download_url": cover_url,
        "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        "license_url": "",
        "modifications": "等比缩放与外部留白；未重绘或修改封面文字",
        "dimensions": list(cover_size),
    }]

    records = commons_records()
    for target, content, filename in FILES:
        if filename not in records:
            raise KeyError(f"Commons record not found: {filename}; available={list(records)}")
        path = ASSET_ROOT / target
        record = records[filename]
        if not path.exists() or path.stat().st_size < 10_000:
            path.write_bytes(request_bytes(record["download_url"]))
        size = image_dimensions(path.read_bytes())
        if min(size) < 700:
            raise ValueError(f"case image too small: {target} {size}")
        manifest.append({
            "filename": target, "content": content, **record,
            "modifications": "裁切、缩放、轻微调色与图文排版", "dimensions": list(size),
        })
        print(target, *size, record["license"])
        time.sleep(2.2)

    (ASSET_ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("cover.jpg", *cover_size)


if __name__ == "__main__":
    main()
