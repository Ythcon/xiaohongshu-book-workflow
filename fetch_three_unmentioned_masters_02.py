#!/usr/bin/env python3
"""Fetch covers and sourced images for the second three-master batch."""

from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters-02"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"

BOOKS = {
    "richard-neutra-survival-through-design": {
        "cover": (
            "https://covers.openlibrary.org/b/id/8231531-L.jpg",
            "https://openlibrary.org/works/OL5791354W/Survival_through_design",
            "Open Library / Oxford University Press",
        ),
        "images": [
            ("02-lovell-house.jpg", "洛弗尔健康住宅", "https://upload.wikimedia.org/wikipedia/commons/4/4d/Lovell_House%2C_Los_Angeles%2C_California.JPG", "https://commons.wikimedia.org/wiki/File:Lovell_House,_Los_Angeles,_California.JPG", "Los Angeles", "CC BY-SA 3.0"),
            ("03-kaufmann-house.jpg", "考夫曼沙漠住宅", "https://upload.wikimedia.org/wikipedia/commons/8/8a/Kaufman_Desert_Home.jpg", "https://commons.wikimedia.org/wiki/File:Kaufman_Desert_Home.jpg", "Pmeulbroek", "CC BY-SA 4.0"),
            ("04-vdl-house.jpg", "诺伊特拉 VDL 研究住宅", "https://upload.wikimedia.org/wikipedia/commons/f/f5/Neutra_front_gardens.jpg", "https://commons.wikimedia.org/wiki/File:Neutra_front_gardens.jpg", "Caterpillar84", "CC BY-SA 4.0"),
            ("05-perkins-house.jpg", "康斯坦斯·珀金斯住宅", "https://upload.wikimedia.org/wikipedia/commons/e/ea/Constance_Perkins_House.jpg", "https://commons.wikimedia.org/wiki/File:Constance_Perkins_House.jpg", "Barte", "CC BY-SA 4.0"),
        ],
    },
    "buckminster-fuller-spaceship-earth": {
        "cover": (
            "https://covers.openlibrary.org/b/id/689663-L.jpg",
            "https://openlibrary.org/works/OL465813W/Operating_manual_for_spaceship_earth",
            "Open Library / original publisher record",
        ),
        "images": [
            ("02-dymaxion-house.jpg", "Dymaxion 住宅", "https://upload.wikimedia.org/wikipedia/commons/b/b4/Dymaxion_house.jpg", "https://commons.wikimedia.org/wiki/File:Dymaxion_house.jpg", "Rmhermen", "CC BY-SA 3.0"),
            ("03-dymaxion-car.jpg", "Dymaxion 汽车", "https://upload.wikimedia.org/wikipedia/commons/5/52/Dymaxion_car_photo.jpg", "https://commons.wikimedia.org/wiki/File:Dymaxion_car_photo.jpg", "Sascha Pohflepp", "CC BY 2.0"),
            ("04-montreal-biosphere.jpg", "蒙特利尔生物圈", "https://upload.wikimedia.org/wikipedia/commons/4/4b/17-08-islcanus-RalfR-DSC_3883.jpg", "https://commons.wikimedia.org/wiki/File:17-08-islcanus-RalfR-DSC_3883.jpg", "Ralf Roletschek", "GFDL 1.2"),
            ("05-fly-eye-dome.jpg", "Fly's Eye Dome", "https://upload.wikimedia.org/wikipedia/commons/3/3c/Fly%27s_Eye_Dome_by_Buckminster_Fuller%2C_Crystal_Bridges_Museum.JPG", "https://commons.wikimedia.org/wiki/File:Fly%27s_Eye_Dome_by_Buckminster_Fuller,_Crystal_Bridges_Museum.JPG", "Wmpearl", "CC0"),
        ],
    },
    "charles-correa-place-in-the-shade": {
        "cover": (
            "https://covers.openlibrary.org/b/id/14047995-L.jpg",
            "https://openlibrary.org/books/OL24903848M/A_place_in_the_shade",
            "Open Library / Penguin Books India",
        ),
        "images": [
            ("02-gandhi-ashram.jpg", "甘地纪念馆", "https://upload.wikimedia.org/wikipedia/commons/9/9a/GANDHI_ASHRAM_03.jpg", "https://commons.wikimedia.org/wiki/File:GANDHI_ASHRAM_03.jpg", "Umar", "CC BY-SA 3.0"),
            ("03-bharat-bhavan.jpg", "巴拉特艺术中心", "https://upload.wikimedia.org/wikipedia/commons/5/56/Bharat_Bhavan_Bhopal.JPG", "https://commons.wikimedia.org/wiki/File:Bharat_Bhavan_Bhopal.JPG", "Suyash Dwivedi", "CC BY-SA 4.0"),
            ("04-jawahar-kala-kendra.jpg", "贾瓦哈尔艺术中心", "https://upload.wikimedia.org/wikipedia/commons/4/41/2022_July_-_JawaharKalaKendra_Jaipur_13.jpg", "https://commons.wikimedia.org/wiki/File:2022_July_-_JawaharKalaKendra_Jaipur_13.jpg", "Chainwit", "CC BY-SA 4.0"),
            ("05-iucaa.jpg", "IUCAA 天文与天体物理中心", "https://upload.wikimedia.org/wikipedia/commons/5/5a/Architecture_of_IUCAA_01.jpg", "https://commons.wikimedia.org/wiki/File:Architecture_of_IUCAA_01.jpg", "DesiBoy101", "CC BY 4.0"),
        ],
    },
}


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 10_000:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                path.write_bytes(response.read())
            return
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def thumbnail_url(url: str, width: int = 1280) -> str:
    directory, filename = url.rsplit("/", 1)
    directory = directory.replace("/wikipedia/commons/", "/wikipedia/commons/thumb/")
    return f"{directory}/{filename}/{width}px-{filename}"


def main() -> None:
    for slug, book in BOOKS.items():
        output = ASSET_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        cover_url, source_url, credit = book["cover"]
        download(cover_url, output / "cover.jpg")
        manifest = [{
            "filename": "cover.jpg",
            "content": "正式书封",
            "credit": credit,
            "source_url": source_url,
            "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
            "modifications": "等比缩放、裁切外部留白、排版；未修改封面文字",
        }]
        for filename, content, image_url, page_url, author, license_name in book["images"]:
            download(thumbnail_url(image_url), output / filename)
            manifest.append({
                "filename": filename,
                "content": content,
                "credit": author,
                "source_url": page_url,
                "license": license_name,
                "modifications": "裁切、缩放、轻微调色与图文排版",
            })
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Fetched {slug}: {len(manifest)} assets")


if __name__ == "__main__":
    main()
