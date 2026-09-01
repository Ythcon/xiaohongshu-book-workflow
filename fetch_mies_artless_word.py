#!/usr/bin/env python3
"""Fetch a verified The Artless Word cover and four real Mies project photos."""

from __future__ import annotations

import json
import time
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "mies-artless-word"
USER_AGENT = "Codex-xhs-book-cards/1.0"

ASSETS = [
    {
        "filename": "cover.jpg",
        "content": "1994 年 MIT Press 平装版真实书封",
        "credit": "Fritz Neumeyer / The MIT Press (book cover)",
        "source_url": "https://openlibrary.org/books/OL10238424M/The_Artless_Word",
        "download_url": "https://covers.openlibrary.org/b/id/2342731-L.jpg",
        "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        "license_url": "",
        "modifications": "等比缩放与外部留白；未重绘或修改封面文字",
    },
    {
        "filename": "02-barcelona-pavilion.jpg",
        "content": "重建后的巴塞罗那德国馆室内实景",
        "credit": "Christian Gänshirt",
        "source_url": "https://commons.wikimedia.org/wiki/File:Barcelona_Pavilion_photo_Christian_G%C3%A4nshirt_2012.JPG",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Barcelona_Pavilion_photo_Christian_G%C3%A4nshirt_2012.JPG/1920px-Barcelona_Pavilion_photo_Christian_G%C3%A4nshirt_2012.JPG",
        "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "modifications": "裁切、缩放、轻微调色与图文排版",
    },
    {
        "filename": "03-villa-tugendhat.jpg",
        "content": "图根哈特别墅花园立面实景",
        "credit": "Ben Skála",
        "source_url": "https://commons.wikimedia.org/wiki/File:Brno-vila-Tugendhat-ze-zahrady2023.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Brno-vila-Tugendhat-ze-zahrady2023.jpg/1920px-Brno-vila-Tugendhat-ze-zahrady2023.jpg",
        "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "modifications": "裁切、缩放、轻微调色与图文排版",
    },
    {
        "filename": "04-farnsworth-house.jpg",
        "content": "范斯沃斯住宅外部实景",
        "credit": "Victor Grigas",
        "source_url": "https://commons.wikimedia.org/wiki/File:Farnsworth_House_by_Mies_Van_Der_Rohe_-_exterior-6.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Farnsworth_House_by_Mies_Van_Der_Rohe_-_exterior-6.jpg/1920px-Farnsworth_House_by_Mies_Van_Der_Rohe_-_exterior-6.jpg",
        "license": "CC BY-SA 3.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/3.0/",
        "modifications": "裁切、缩放、轻微调色与图文排版",
    },
    {
        "filename": "05-seagram-building.jpg",
        "content": "纽约西格拉姆大厦实景",
        "credit": "Noroton",
        "source_url": "https://commons.wikimedia.org/wiki/File:NewYorkSeagram_04.30.2008.JPG",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/NewYorkSeagram_04.30.2008.JPG/1280px-NewYorkSeagram_04.30.2008.JPG",
        "license": "Public domain",
        "license_url": "",
        "modifications": "裁切、缩放、轻微调色与图文排版",
    },
]


def fetch(url: str) -> bytes:
    last_error = None
    for attempt in range(6):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read()
        except Exception as error:
            last_error = error
            time.sleep(3.5 * (attempt + 1))
    raise RuntimeError(f"download failed: {url}: {last_error}")


def main() -> None:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for item in ASSETS:
        path = ASSET_ROOT / item["filename"]
        if not path.exists() or path.stat().st_size < 10_000:
            path.write_bytes(fetch(item["download_url"]))
        with Image.open(BytesIO(path.read_bytes())) as image:
            width, height = image.size
            image.verify()
        if item["filename"] == "cover.jpg" and (width < 200 or height < 280):
            raise ValueError(f"cover too small: {width}x{height}")
        if item["filename"] != "cover.jpg" and min(width, height) < 700:
            raise ValueError(f"case image too small: {item['filename']} {width}x{height}")
        manifest.append({**item, "dimensions": [width, height]})
        print(item["filename"], width, height)
        time.sleep(2.5)
    (ASSET_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
