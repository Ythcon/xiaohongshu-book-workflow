#!/usr/bin/env python3
"""Fetch verified covers and sourced project images for batch 04."""

from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters-04"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"

LICENSES = {
    "CC0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "Public Domain": "https://creativecommons.org/publicdomain/mark/1.0/",
    "CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/",
    "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/",
    "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
}

BOOKS = {
    "hassan-fathy-architecture-for-the-poor": {
        "cover": (
            "https://covers.openlibrary.org/b/id/140666-L.jpg",
            "https://openlibrary.org/books/OL9411438M/Architecture_for_the_Poor",
            "Open Library / University of Chicago Press",
        ),
        "images": [
            (
                "02-new-gourna-mosque.jpg",
                "新古尔纳清真寺",
                "https://upload.wikimedia.org/wikipedia/commons/0/05/Gurna_Mosque_R01.jpg",
                "https://commons.wikimedia.org/wiki/File:Gurna_Mosque_R01.jpg",
                "Marc Ryckaert",
                "CC BY 3.0",
            ),
            (
                "03-new-gourna-section.jpg",
                "新古尔纳手工艺展馆剖面",
                "https://upload.wikimedia.org/wikipedia/commons/9/9a/New_Gourna_Village_-_Craft%27s_Exhibition-_Section.jpg",
                "https://commons.wikimedia.org/wiki/File:New_Gourna_Village_-_Craft%27s_Exhibition-_Section.jpg",
                "RBSCL",
                "CC BY-SA 4.0",
            ),
            (
                "04-new-baris.jpg",
                "新巴里斯村",
                "https://upload.wikimedia.org/wikipedia/commons/4/44/New_Baris%2C_Village_Kharga%2C_Egypt_28.jpg",
                "https://commons.wikimedia.org/wiki/File:New_Baris,_Village_Kharga,_Egypt_28.jpg",
                "Viktor Lazic",
                "CC BY-SA 4.0",
            ),
            (
                "05-dar-al-islam.jpg",
                "达尔伊斯兰清真寺",
                "https://upload.wikimedia.org/wikipedia/commons/f/fd/Hassan_Fathy_Dar-Ul-Islam_Mosque%2C_New_Mexico_%2812371058%29.jpg",
                "https://commons.wikimedia.org/wiki/File:Hassan_Fathy_Dar-Ul-Islam_Mosque,_New_Mexico_(12371058).jpg",
                "Omar Barcena",
                "CC BY 2.0",
            ),
        ],
    },
    "kisho-kurokawa-metabolism-in-architecture": {
        "cover": (
            "https://covers.openlibrary.org/b/id/12964998-L.jpg",
            "https://openlibrary.org/books/OL4604339M/Metabolism_in_architecture",
            "Open Library / Studio Vista",
        ),
        "images": [
            (
                "02-nakagin.jpg",
                "中银胶囊塔",
                "https://upload.wikimedia.org/wikipedia/commons/c/cb/Nakagin_Capsule_Tower_2017_dllu.jpg",
                "https://commons.wikimedia.org/wiki/File:Nakagin_Capsule_Tower_2017_dllu.jpg",
                "Dllu",
                "CC BY-SA 4.0",
            ),
            (
                "03-sagae-city-hall.jpg",
                "寒河江市政厅",
                "https://upload.wikimedia.org/wikipedia/commons/9/98/Sagae_City_Hall_2011.jpg",
                "https://commons.wikimedia.org/wiki/File:Sagae_City_Hall_2011.jpg",
                "Wiiii",
                "CC BY-SA 3.0",
            ),
            (
                "04-klia.jpg",
                "吉隆坡国际机场主航站楼",
                "https://upload.wikimedia.org/wikipedia/commons/2/24/KLIA_MTB%26Tower.jpg",
                "https://commons.wikimedia.org/wiki/File:KLIA_MTB%26Tower.jpg",
                "Craig / Pizzaboy1",
                "Public Domain",
            ),
            (
                "05-national-art-center.jpg",
                "东京国立新美术馆",
                "https://upload.wikimedia.org/wikipedia/commons/9/92/National_Art_Center%2C_Tokyo_-_DSC06720.JPG",
                "https://commons.wikimedia.org/wiki/File:National_Art_Center,_Tokyo_-_DSC06720.JPG",
                "Daderot",
                "CC0",
            ),
        ],
    },
    "fumihiko-maki-nurturing-dreams": {
        "cover": (
            "https://covers.openlibrary.org/b/id/9902745-L.jpg",
            "https://openlibrary.org/books/OL22670784M/Nurturing_dreams",
            "Open Library / MIT Press",
        ),
        "images": [
            (
                "02-hillside-terrace.jpg",
                "代官山 Hillside Terrace",
                "https://upload.wikimedia.org/wikipedia/commons/8/89/Hillside_Terrace_A_B_2010.jpg",
                "https://commons.wikimedia.org/wiki/File:Hillside_Terrace_A_B_2010.jpg",
                "Wiiii",
                "CC BY-SA 3.0",
            ),
            (
                "03-spiral.jpg",
                "东京 Spiral",
                "https://upload.wikimedia.org/wikipedia/commons/d/de/Spiral_Building.jpg",
                "https://commons.wikimedia.org/wiki/File:Spiral_Building.jpg",
                "Wiiii",
                "CC BY-SA 3.0",
            ),
            (
                "04-media-lab.jpg",
                "MIT Media Lab 新楼",
                "https://upload.wikimedia.org/wikipedia/commons/2/2c/MIT_Media_Lab_new_building.jpg",
                "https://commons.wikimedia.org/wiki/File:MIT_Media_Lab_new_building.jpg",
                "Unmadindu",
                "CC BY-SA 3.0",
            ),
            (
                "05-four-wtc.jpg",
                "纽约世贸中心四号楼",
                "https://upload.wikimedia.org/wikipedia/commons/3/37/Four_World_Trade_Center_2015.jpg",
                "https://commons.wikimedia.org/wiki/File:Four_World_Trade_Center_2015.jpg",
                "Choinowski",
                "CC BY-SA 4.0",
            ),
        ],
    },
}


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 10_000:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=60) as response:
                path.write_bytes(response.read())
            return
        except Exception as exc:
            last_error = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def thumbnail_url(url: str, width: int = 1280) -> str:
    directory, filename = url.rsplit("/", 1)
    directory = directory.replace("/wikipedia/commons/", "/wikipedia/commons/thumb/")
    return f"{directory}/{filename}/{width}px-{filename}"


def main() -> None:
    for slug, book in BOOKS.items():
        output = ASSET_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        cover_url, cover_source, cover_credit = book["cover"]
        download(cover_url, output / "cover.jpg")
        manifest = [
            {
                "filename": "cover.jpg",
                "content": "正式书封",
                "credit": cover_credit,
                "source_url": cover_source,
                "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
                "license_url": "",
                "modifications": "等比缩放、裁切外部留白、轻微清晰化；未修改封面文字",
            }
        ]
        for filename, content, original, page, author, license_name in book["images"]:
            try:
                download(thumbnail_url(original), output / filename)
            except RuntimeError:
                download(original, output / filename)
            manifest.append(
                {
                    "filename": filename,
                    "content": content,
                    "credit": author,
                    "source_url": page,
                    "license": license_name,
                    "license_url": LICENSES[license_name],
                    "modifications": "裁切、缩放、轻微调色与图文排版",
                }
            )
            time.sleep(0.9)
        (output / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Fetched {slug}: {len(manifest)} assets")


if __name__ == "__main__":
    main()
