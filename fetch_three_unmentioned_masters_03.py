#!/usr/bin/env python3
"""Fetch covers and sourced images for the third three-master batch."""

from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters-03"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"

BOOKS = {
    "herman-hertzberger-lessons-for-students": {
        "cover": ("https://covers.openlibrary.org/b/id/9800227-L.jpg", "https://openlibrary.org/works/OL4307478W/Lessons_for_students_in_architecture", "Open Library / 010 Publishers"),
        "images": [
            ("02-centraal-beheer.jpg", "中央保险公司办公楼", "https://upload.wikimedia.org/wikipedia/commons/7/7b/Centraal_Beheergebouw_van_Herman_Hertzberger%2C_interieur_%283%29.jpg", "https://commons.wikimedia.org/wiki/File:Centraal_Beheergebouw_van_Herman_Hertzberger,_interieur_(3).jpg", "Apdency", "CC0"),
            ("03-diagoon-houses.jpg", "Diagoon 住宅", "https://upload.wikimedia.org/wikipedia/commons/0/02/Diagoon_Delft_3b.Herman_Hertzberger.jpg", "https://commons.wikimedia.org/wiki/File:Diagoon_Delft_3b.Herman_Hertzberger.jpg", "Leuk2", "CC BY-SA 4.0"),
            ("04-drie-hoven.jpg", "De Drie Hoven 老年住宅", "https://upload.wikimedia.org/wikipedia/commons/c/c4/De_Drie_Hoven_1974_-_Hertzberger_%281%29.jpg", "https://commons.wikimedia.org/wiki/File:De_Drie_Hoven_1974_-_Hertzberger_(1).jpg", "Leuk2", "CC BY-SA 3.0"),
            ("05-vredenburg.jpg", "Vredenburg 音乐中心", "https://upload.wikimedia.org/wikipedia/commons/c/cc/Vredenburg_1978_-_Hertzberger.jpg", "https://commons.wikimedia.org/wiki/File:Vredenburg_1978_-_Hertzberger.jpg", "Leuk2", "CC BY-SA 3.0"),
        ],
    },
    "renzo-piano-logbook": {
        "cover": ("https://covers.openlibrary.org/b/id/12853074-L.jpg", "https://openlibrary.org/books/OL17489956M/The_Renzo_Piano_logbook", "Open Library / Thames & Hudson"),
        "images": [
            ("02-pompidou.jpg", "蓬皮杜艺术中心", "https://upload.wikimedia.org/wikipedia/commons/a/a5/0_Centre_Georges-Pompidou_-_1986_Paris.JPG", "https://commons.wikimedia.org/wiki/File:0_Centre_Georges-Pompidou_-_1986_Paris.JPG", "Jean-Pol GRANDMONT", "CC BY 4.0"),
            ("03-menil.jpg", "梅尼尔收藏馆", "https://upload.wikimedia.org/wikipedia/commons/6/63/MenilCollection.JPG", "https://commons.wikimedia.org/wiki/File:MenilCollection.JPG", "WhisperToMe", "Public Domain"),
            ("04-kansai.jpg", "关西国际机场航站楼", "https://upload.wikimedia.org/wikipedia/commons/1/16/KIX_airport.jpg", "https://commons.wikimedia.org/wiki/File:KIX_airport.jpg", "mackwo7", "CC0"),
            ("05-tjibaou.jpg", "吉巴乌文化中心", "https://upload.wikimedia.org/wikipedia/commons/c/ca/Jean-Marie_Tjibaou_Cultural_Centre%2C_filmed_in_June_2013.jpg", "https://commons.wikimedia.org/wiki/File:Jean-Marie_Tjibaou_Cultural_Centre,_filmed_in_June_2013.jpg", "gerard (Noumea)", "CC BY-SA 2.0"),
        ],
    },
    "moshe-safdie-for-everyone-a-garden": {
        "cover": ("https://covers.openlibrary.org/b/id/9814037-L.jpg", "https://openlibrary.org/works/OL6018549W/For_everyone_a_garden", "Open Library / MIT Press"),
        "images": [
            ("02-habitat-67.jpg", "Habitat 67", "https://upload.wikimedia.org/wikipedia/commons/f/fe/Habitat_67_2019_dllu_01.jpg", "https://commons.wikimedia.org/wiki/File:Habitat_67_2019_dllu_01.jpg", "Dllu", "CC BY-SA 4.0"),
            ("03-national-gallery.jpg", "加拿大国家美术馆", "https://upload.wikimedia.org/wikipedia/commons/4/43/National_Gallery_of_Canada%2C_Ottawa%2C_Ontario_%2830035252696%29.jpg", "https://commons.wikimedia.org/wiki/File:National_Gallery_of_Canada,_Ottawa,_Ontario_(30035252696).jpg", "Ken Lund", "CC BY-SA 2.0"),
            ("04-yad-vashem.jpg", "以色列犹太大屠杀纪念馆", "https://upload.wikimedia.org/wikipedia/commons/2/29/YadVashemMar042023_01.jpg", "https://commons.wikimedia.org/wiki/File:YadVashemMar042023_01.jpg", "Hagai Agmon-Snir", "CC BY-SA 4.0"),
            ("05-sky-habitat.jpg", "Sky Habitat", "https://upload.wikimedia.org/wikipedia/commons/f/f4/Sky_Habitat_at_Dawn.jpg", "https://commons.wikimedia.org/wiki/File:Sky_Habitat_at_Dawn.jpg", "MTCKSG", "CC BY-SA 4.0"),
        ],
    },
}


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 10_000:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
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
        cover_url, cover_source, cover_credit = book["cover"]
        download(cover_url, output / "cover.jpg")
        manifest = [{"filename": "cover.jpg", "content": "正式书封", "credit": cover_credit, "source_url": cover_source, "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人", "modifications": "等比缩放、裁切外部留白、排版；未修改封面文字"}]
        for filename, content, original, page, author, license_name in book["images"]:
            try:
                download(thumbnail_url(original), output / filename)
            except RuntimeError:
                download(original, output / filename)
            manifest.append({"filename": filename, "content": content, "credit": author, "source_url": page, "license": license_name, "modifications": "裁切、缩放、轻微调色与图文排版"})
            time.sleep(0.8)
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Fetched {slug}: {len(manifest)} assets")


if __name__ == "__main__":
    main()
