#!/usr/bin/env python3
"""Fetch verified covers and Commons project images for three single-book posts."""

from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"

DIRECT_IMAGE_OVERRIDES = {
    "Lina_Bo_Bardi,_SESC_Pompéia_(5391718290).jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Lina_Bo_Bardi%2C_SESC_Pomp%C3%A9ia_%285391718290%29.jpg/1280px-Lina_Bo_Bardi%2C_SESC_Pomp%C3%A9ia_%285391718290%29.jpg",
}

METADATA_OVERRIDES = {
    "Fallingwater3.jpg": ("https://commons.wikimedia.org/wiki/File:Fallingwater3.jpg", "lachrimae72", "CC0"),
    "Jacobs_First_House_-_front.jpg": ("https://commons.wikimedia.org/wiki/File:Jacobs_First_House_-_front.jpg", "James Steakley", "CC BY-SA 3.0"),
    "Taliesin_West_Complex_DSCN2137.jpg": ("https://commons.wikimedia.org/wiki/File:Taliesin_West_Complex_DSCN2137.jpg", "Lar", "Public Domain"),
    "Rosenbaum_House_Rear_Pano.jpg": ("https://commons.wikimedia.org/wiki/File:Rosenbaum_House_Rear_Pano.jpg", "Mmdoogie", "CC BY-SA 3.0"),
    "Paimio_Sanatorium2.jpg": ("https://commons.wikimedia.org/wiki/File:Paimio_Sanatorium2.jpg", "Leon Liao", "CC BY 2.0"),
    "Vyborg_Library_Interior2_(cropped).jpg": ("https://commons.wikimedia.org/wiki/File:Vyborg_Library_Interior2_(cropped).jpg", "Ninaraas", "CC BY 4.0"),
    "Alvar_Aalto,_Villa_Mairea_08.jpg": ("https://commons.wikimedia.org/wiki/File:Alvar_Aalto,_Villa_Mairea_08.jpg", "Dieter Janssen", "CC BY-SA 3.0"),
    "Säynätsalo_town_hall_courtyard.jpg": ("https://commons.wikimedia.org/wiki/File:S%C3%A4yn%C3%A4tsalo_town_hall_courtyard.jpg", "Alexignat", "CC BY-SA 4.0"),
    "Casa_de_Vidro_-_Instituto_Bardi_01.jpg": ("https://commons.wikimedia.org/wiki/File:Casa_de_Vidro_-_Instituto_Bardi_01.jpg", "Monica Kaneko", "CC BY-SA 2.0"),
    "Escadaria_do_Museu_de_Arte_Moderna_da_Bahia.jpg": ("https://commons.wikimedia.org/wiki/File:Escadaria_do_Museu_de_Arte_Moderna_da_Bahia.jpg", "Boaventuravinicius", "CC BY-SA 4.0"),
    "Novo_MASP.jpg": ("https://commons.wikimedia.org/wiki/File:Novo_MASP.jpg", "Mauro Cateb", "CC BY-SA 2.0"),
    "Lina_Bo_Bardi,_SESC_Pompéia_(5391718290).jpg": (
        "https://commons.wikimedia.org/wiki/File:Lina_Bo_Bardi,_SESC_Pomp%C3%A9ia_(5391718290).jpg",
        "seier+seier",
        "CC BY 2.0",
    ),
}

BOOKS = {
    "frank-lloyd-wright-natural-house": {
        "cover": {
            "filename": "cover.jpg",
            "download_url": "https://covers.openlibrary.org/b/id/12187468-L.jpg",
            "source_url": "https://openlibrary.org/works/OL961857W/The_natural_house",
            "credit": "Open Library cover record / original publisher",
            "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        },
        "images": [
            ("02-fallingwater.jpg", "Fallingwater3.jpg", "流水别墅 / Fallingwater"),
            ("03-jacobs-house.jpg", "Jacobs_First_House_-_front.jpg", "赫伯特·雅各布斯第一住宅"),
            ("04-taliesin-west.jpg", "Taliesin_West_Complex_DSCN2137.jpg", "西塔里埃森 / Taliesin West"),
            ("05-rosenbaum-house.jpg", "Rosenbaum_House_Rear_Pano.jpg", "罗森鲍姆住宅"),
        ],
    },
    "alvar-aalto-in-his-own-words": {
        "cover": {
            "filename": "cover.jpg",
            "download_url": "https://covers.openlibrary.org/b/id/643564-L.jpg",
            "source_url": "https://openlibrary.org/books/OL684423M/Alvar_Aalto_in_his_own_words",
            "credit": "Open Library cover record / Rizzoli",
            "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        },
        "images": [
            ("02-paimio.jpg", "Paimio_Sanatorium2.jpg", "帕伊米奥疗养院"),
            ("03-vyborg-library.jpg", "Vyborg_Library_Interior2_(cropped).jpg", "维堡图书馆"),
            ("04-villa-mairea.jpg", "Alvar_Aalto,_Villa_Mairea_08.jpg", "玛利亚别墅"),
            ("05-saynatsalo.jpg", "Säynätsalo_town_hall_courtyard.jpg", "塞于奈察洛市政厅"),
        ],
    },
    "lina-bo-bardi-stones-against-diamonds": {
        "cover": {
            "filename": "cover.jpg",
            "download_url": "https://www.designersandbooks.com/sites/default/files/imagecache/large_book_jacket/stones-against-diamonds-300px.jpg",
            "source_url": "https://www.designersandbooks.com/book/architecture-words-12-stones-against-diamonds",
            "credit": "Designers & Books / Architectural Association Publications",
            "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        },
        "images": [
            ("02-casa-de-vidro.jpg", "Casa_de_Vidro_-_Instituto_Bardi_01.jpg", "玻璃之家 / Casa de Vidro"),
            ("03-solar-do-unhao.jpg", "Escadaria_do_Museu_de_Arte_Moderna_da_Bahia.jpg", "乌尼昂庄园改造 / Solar do Unhão"),
            ("04-masp.jpg", "Novo_MASP.jpg", "圣保罗艺术博物馆 / MASP"),
            ("05-sesc-pompeia.jpg", "Lina_Bo_Bardi,_SESC_Pompéia_(5391718290).jpg", "庞培亚文化体育中心 / SESC Pompéia"),
        ],
    },
}


def request(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 10_000:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            path.write_bytes(request(url))
            return
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(value).split())


def commons_metadata(filename: str) -> tuple[str, str, str]:
    if filename in METADATA_OVERRIDES:
        return METADATA_OVERRIDES[filename]
    encoded = urllib.parse.quote(filename.replace(" ", "_"), safe="(),_-.")
    page_url = f"https://commons.wikimedia.org/wiki/File:{encoded}"
    page = request(page_url).decode("utf-8", errors="replace")

    license_match = re.search(
        r'class="licensetpl_short"[^>]*>(.*?)</span>', page, flags=re.I | re.S
    )
    license_name = strip_tags(license_match.group(1)) if license_match else "见 Commons 文件页许可"

    author_match = re.search(
        r'id="fileinfotpl_aut".*?</td>\s*<td[^>]*>(.*?)</td>', page, flags=re.I | re.S
    )
    author = strip_tags(author_match.group(1)) if author_match else "Wikimedia Commons contributor"
    return page_url, author, license_name


def main() -> None:
    for slug, book in BOOKS.items():
        directory = ASSET_ROOT / slug
        directory.mkdir(parents=True, exist_ok=True)
        manifest: list[dict[str, str]] = []

        cover = book["cover"]
        cover_path = directory / cover["filename"]
        download(cover["download_url"], cover_path)
        manifest.append(
            {
                "filename": cover["filename"],
                "content": "正式书封",
                "credit": cover["credit"],
                "source_url": cover["source_url"],
                "license": cover["license"],
                "modifications": "等比缩放、裁切外部留白、排版；未修改封面文字",
            }
        )

        for local_name, commons_name, content in book["images"]:
            encoded = urllib.parse.quote(commons_name.replace(" ", "_"), safe="(),_-.äöåÄÖÅéÉèÈáÁíÍóÓúÚãÃõÕçÇ")
            image_url = DIRECT_IMAGE_OVERRIDES.get(
                commons_name,
                f"https://commons.wikimedia.org/wiki/Special:Redirect/file/{encoded}?width=1800",
            )
            path = directory / local_name
            download(image_url, path)
            page_url, author, license_name = commons_metadata(commons_name)
            manifest.append(
                {
                    "filename": local_name,
                    "content": content,
                    "credit": author,
                    "source_url": page_url,
                    "license": license_name,
                    "modifications": "裁切、缩放、轻微调色与图文排版",
                }
            )
            time.sleep(0.6)

        (directory / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Fetched {slug}: {len(manifest)} assets")


if __name__ == "__main__":
    main()
