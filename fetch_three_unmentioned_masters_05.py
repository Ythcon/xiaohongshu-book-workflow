#!/usr/bin/env python3
"""Fetch verified covers and sourced project images for batch 05."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters-05"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"

LICENSES = {
    "Public Domain": "https://creativecommons.org/publicdomain/mark/1.0/",
    "No known restrictions": "https://www.loc.gov/pictures/collection/krb/rights.html",
    "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/",
    "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
}


def commons_file(filename: str, width: int = 1600) -> str:
    encoded = urllib.parse.quote(filename.replace(" ", "_"), safe="_.()-")
    return f"https://commons.wikimedia.org/wiki/Special:Redirect/file/{encoded}?width={width}"


BOOKS = {
    "adolf-loos-ornament-and-crime": {
        "cover": (
            "https://covers.openlibrary.org/b/id/822494-L.jpg",
            "https://openlibrary.org/books/OL8734863M/Ornament_and_Crime",
            "Open Library / Ariadne Press",
        ),
        "images": [
            ("02-looshaus-exterior.jpg", "维也纳 Looshaus", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Looshaus_Michaelerplatz.JPG/1280px-Looshaus_Michaelerplatz.JPG", "https://commons.wikimedia.org/wiki/File:Looshaus_Michaelerplatz.JPG", "Thomas Ledl", "CC BY-SA 4.0"),
            ("03-american-bar.jpg", "American Bar 室内", commons_file("American Bar Interior.jpg"), "https://commons.wikimedia.org/wiki/File:American_Bar_Interior.jpg", "SullyWatts", "CC BY-SA 4.0"),
            ("04-steiner-house.jpg", "Steiner House", commons_file("Steiner1.jpg"), "https://commons.wikimedia.org/wiki/File:Steiner1.jpg", "Castellónenred", "CC BY-SA 4.0"),
            ("05-villa-muller.jpg", "Villa Müller", commons_file("Müller villa.jpg"), "https://commons.wikimedia.org/wiki/File:M%C3%BCller_villa.jpg", "Martin2035", "CC BY-SA 4.0"),
        ],
    },
    "marcel-breuer-sun-and-shadow": {
        "cover": (
            "https://covers.openlibrary.org/b/id/15072961-L.jpg",
            "https://openlibrary.org/books/OL50558833M/Sun_and_shadow",
            "Open Library / Dodd, Mead",
        ),
        "images": [
            ("02-breuer-house-ii.jpg", "Breuer House II", commons_file("NewCanaanCT MarcelBreuerHouseII.jpg"), "https://commons.wikimedia.org/wiki/File:NewCanaanCT_MarcelBreuerHouseII.jpg", "Magicpiano", "CC BY-SA 3.0"),
            ("03-whitney.jpg", "原 Whitney Museum（现 The Met Breuer）", commons_file("2003-03-ehemaliges-Whitney-Museum-new-York-Manhattan-Marcel-Breuer.jpg"), "https://commons.wikimedia.org/wiki/File:2003-03-ehemaliges-Whitney-Museum-new-York-Manhattan-Marcel-Breuer.jpg", "Gunnar Klack", "CC BY-SA 4.0"),
            ("04-st-johns.jpg", "Saint John's Abbey Church", commons_file("2009-0522-MN-SJU-abbeychurch.jpg"), "https://commons.wikimedia.org/wiki/File:2009-0522-MN-SJU-abbeychurch.jpg", "Bobak Ha'Eri", "CC BY 3.0"),
            ("05-atlanta-library.jpg", "Atlanta Central Library", commons_file("Atlanta Central Library, ATL.jpg"), "https://commons.wikimedia.org/wiki/File:Atlanta_Central_Library,_ATL.jpg", "JJonahJackalope", "CC BY-SA 4.0"),
        ],
    },
    "eero-saarinen-on-his-work": {
        "cover": (
            "https://covers.openlibrary.org/b/id/10180042-L.jpg",
            "https://openlibrary.org/books/OL19144132M/Eero_Saarinen_on_his_work",
            "Open Library / Yale University Press",
        ),
        "images": [
            ("02-twa.jpg", "TWA Flight Center", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/TWA_Flight_Center_Dec_2025_101.jpg/1280px-TWA_Flight_Center_Dec_2025_101.jpg", "https://commons.wikimedia.org/wiki/File:TWA_Flight_Center_Dec_2025_101.jpg", "Epicgenius", "CC BY-SA 4.0"),
            ("03-gateway-arch.jpg", "Gateway Arch", "https://upload.wikimedia.org/wikipedia/commons/d/de/Gateway_Arch%2C_St._Louis.jpg", "https://commons.wikimedia.org/wiki/File:Gateway_Arch,_St._Louis.jpg", "Lewis Hulbert", "CC BY-SA 4.0"),
            ("04-dulles.jpg", "Washington Dulles International Airport", "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Washington_Dulles_International_Airport.jpg/1280px-Washington_Dulles_International_Airport.jpg", "https://commons.wikimedia.org/wiki/File:Washington_Dulles_International_Airport.jpg", "Joe Ravi", "CC BY-SA 3.0"),
            ("05-kresge.jpg", "Kresge Auditorium", "https://cdn.loc.gov/service/pnp/krb/00200/00242v.jpg", "https://www.loc.gov/pictures/item/2018673066/", "Balthazar Korab / Library of Congress", "No known restrictions"),
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
            with urllib.request.urlopen(request, timeout=90) as response:
                path.write_bytes(response.read())
            return
        except Exception as exc:
            last_error = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def main() -> None:
    for slug, book in BOOKS.items():
        output = ASSET_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        cover_url, cover_source, cover_credit = book["cover"]
        download(cover_url, output / "cover.jpg")
        manifest = [{
            "filename": "cover.jpg",
            "content": "正式书封",
            "credit": cover_credit,
            "source_url": cover_source,
            "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
            "license_url": "",
            "modifications": "等比缩放、裁切外部留白、轻微清晰化；未修改封面文字",
        }]
        for filename, content, image_url, page, author, license_name in book["images"]:
            download(image_url, output / filename)
            manifest.append({
                "filename": filename,
                "content": content,
                "credit": author,
                "source_url": page,
                "license": license_name,
                "license_url": LICENSES[license_name],
                "modifications": "裁切、缩放、轻微调色与图文排版",
            })
            time.sleep(0.8)
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Fetched {slug}: {len(manifest)} assets")


if __name__ == "__main__":
    main()
