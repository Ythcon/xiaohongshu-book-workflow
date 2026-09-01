#!/usr/bin/env python3
"""Fetch one verified cover and eight real Toyo Ito project photos."""

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
ASSETS = ROOT / "assets" / "toyo-ito-blurring-architecture"
USER_AGENT = "Codex-xhs-book-cards/1.0"
FILES = [
    ("02-sendai-exterior.jpg", "仙台媒体中心外观", "SendaiMediatheque.jpg"),
    ("03-sendai-interior.jpg", "仙台媒体中心室内", "Smt14.JPG - Flickr - scarletgreen.jpg"),
    ("04-tower-of-winds.jpg", "横滨风之塔夜景", "Tower of Winds.JPG"),
    ("05-tods.jpg", "TOD'S 表参道大楼", "TOD'S.jpg"),
    ("06-mikimoto.jpg", "Mikimoto 银座 2", "Mikimoto Ginza2.JPG"),
    ("07-serpentine.jpg", "蛇形画廊临时展亭", "Serpentine Pavillion 2002.jpg"),
    ("08-tama-exterior.jpg", "多摩美术大学图书馆外观", "Tama Art University Library.JPG"),
    ("09-tama-interior.jpg", "多摩美术大学图书馆室内", "Tama Art University Library2.JPG"),
]


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()


def get_bytes(url: str) -> bytes:
    error = None
    for i in range(6):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=100) as response:
                return response.read()
        except Exception as exc:
            error = exc
            time.sleep(2 + i)
    raise RuntimeError(f"Cannot download {url}: {error}")


def dimensions(data: bytes) -> tuple[int, int]:
    with Image.open(BytesIO(data)) as image:
        size = image.size
        image.verify()
    return size


def commons_records() -> dict[str, dict[str, str]]:
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "redirects": "1", "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "iiurlwidth": "1920",
        "titles": "|".join("File:" + filename for _, _, filename in FILES),
    })
    data = json.loads(get_bytes("https://commons.wikimedia.org/w/api.php?" + params))
    records: dict[str, dict[str, str]] = {}
    for page in data.get("query", {}).get("pages", {}).values():
        if "missing" in page:
            raise FileNotFoundError(page.get("title"))
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        value = lambda key: clean(meta.get(key, {}).get("value"))
        filename = page["title"].removeprefix("File:")
        records[filename] = {
            "download_url": info.get("thumburl") or info["url"],
            "source_url": info["descriptionurl"],
            "credit": value("Artist") or value("Credit") or "Wikimedia Commons contributor",
            "license": value("LicenseShortName") or value("UsageTerms") or "See source page",
            "license_url": value("LicenseUrl"),
        }
    return records


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    # CCA Islands catalogue record 21075 is the exhibition-book source itself;
    # Open Library returned a project photograph rather than this edition's cover.
    cover_url = "https://cca-islands.org/cms/wp-content/uploads/21075.jpg"
    cover_path = ASSETS / "cover.jpg"
    cover_path.write_bytes(get_bytes(cover_url))
    # The archive scan includes catalogue-form labels and a white scan margin.
    # Crop only those external margins; the printed book cover is untouched.
    with Image.open(cover_path) as raw_cover:
        raw_cover.convert("RGB").crop((30, 291, 1618, 2187)).save(cover_path, "JPEG", quality=95)
    cover_size = dimensions(cover_path.read_bytes())
    if min(cover_size) < 250:
        raise ValueError(f"Cover is too small or missing: {cover_size}")
    manifest = [{
        "filename": "cover.jpg",
        "content": "Charta 英德双语版真实书封",
        "credit": "Toyo Ito / Charta (book cover)",
        "source_url": "https://cca-islands.org/book/toyo-ito-blurring-architecture/",
        "download_url": cover_url,
        "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        "license_url": "",
        "modifications": "裁去档案扫描的外部字段与白边后等比缩放；未重绘或修改封面文字",
        "dimensions": list(cover_size),
    }]
    records = commons_records()
    for target, content, filename in FILES:
        record = records.get(filename)
        if not record:
            raise KeyError(filename)
        path = ASSETS / target
        path.write_bytes(get_bytes(record["download_url"]))
        size = dimensions(path.read_bytes())
        # Commons 的部分纪实照片分辨率有限；小图在成品中等比嵌入，
        # 不会被拉伸成伪高清，低于 300px 才视为不适用。
        if min(size) < 300:
            raise ValueError(f"Image too small: {target} {size}")
        manifest.append({"filename": target, "content": content, **record,
                         "modifications": "裁切、缩放、轻微调色与图文排版", "dimensions": list(size)})
        print(target, size, record["license"])
        time.sleep(1.4)
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("cover.jpg", cover_size)


if __name__ == "__main__":
    main()
