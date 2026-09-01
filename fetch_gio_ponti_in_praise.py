#!/usr/bin/env python3
"""Fetch the verified cover and four real Gio Ponti work images."""

from __future__ import annotations

import json
import time
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "gio-ponti-in-praise-of-architecture"
USER_AGENT = "Codex-xhs-book-cards/1.0"

ASSETS = [
    {
        "filename": "cover.jpg",
        "content": "1960 年 F. W. Dodge 英文版真实书封",
        "credit": "Gio Ponti / F. W. Dodge Corp. (book cover)",
        "source_url": "https://openlibrary.org/books/OL6273922M/In_praise_of_architecture",
        "download_url": "https://covers.openlibrary.org/b/id/14987823-L.jpg",
        "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        "license_url": "",
        "modifications": "等比缩放与外部留白；未重绘或修改封面文字",
    },
    {
        "filename": "02-montecatini.jpg",
        "content": "米兰 Montecatini 总部建筑实景",
        "credit": "Unknown author / Wikimedia Commons contributor",
        "source_url": "https://commons.wikimedia.org/wiki/File:Centro_direzionale_Montecatini_-_Milano.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Centro_direzionale_Montecatini_-_Milano.jpg/1920px-Centro_direzionale_Montecatini_-_Milano.jpg",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "modifications": "裁切、缩放、轻微调色与图文排版",
    },
    {
        "filename": "03-bijenkorf.jpg",
        "content": "埃因霍温 De Bijenkorf 百货建筑实景",
        "credit": "Choinowski",
        "source_url": "https://commons.wikimedia.org/wiki/File:Gebouw_van_De_Bijenkorf_in_Eindhoven.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Gebouw_van_De_Bijenkorf_in_Eindhoven.jpg/1920px-Gebouw_van_De_Bijenkorf_in_Eindhoven.jpg",
        "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "modifications": "裁切、缩放、轻微调色与图文排版",
    },
    {
        "filename": "04-denver-art-museum.jpg",
        "content": "丹佛艺术博物馆马丁大楼实景",
        "credit": "KM Newnham",
        "source_url": "https://commons.wikimedia.org/wiki/File:Denver_Art_Museum_Main_Building.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Denver_Art_Museum_Main_Building.jpg/1920px-Denver_Art_Museum_Main_Building.jpg",
        "license": "CC BY-SA 2.5",
        "license_url": "https://creativecommons.org/licenses/by-sa/2.5/",
        "modifications": "裁切、缩放、轻微调色与图文排版",
    },
    {
        "filename": "05-superleggera.jpg",
        "content": "Cassina Superleggera 椅实物照片",
        "credit": "Sailko",
        "source_url": "https://commons.wikimedia.org/wiki/File:Gio_ponti_per_cassina,_sedia_superleggera,_1957.JPG",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/9/9c/Gio_ponti_per_cassina%2C_sedia_superleggera%2C_1957.JPG",
        "license": "CC BY 3.0",
        "license_url": "https://creativecommons.org/licenses/by/3.0/",
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
