#!/usr/bin/env python3
"""Fetch verified covers and licensed project images for Siza/Siza/Niemeyer."""

from __future__ import annotations

import io
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "two-new-masters-three-books-01"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"

LICENSES = {
    "CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/",
    "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/",
    "CC BY-SA 2.5": "https://creativecommons.org/licenses/by-sa/2.5/",
    "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
}


def commons_file(filename: str, width: int = 1800) -> str:
    encoded = urllib.parse.quote(filename.replace(" ", "_"), safe="_.()-',&")
    return f"https://commons.wikimedia.org/wiki/Special:Redirect/file/{encoded}?width={width}"


def commons_api_file(filename: str, width: int = 1800) -> str:
    """Resolve the stable upload.wikimedia.org thumbnail URL through one API request."""
    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": str(width),
        "titles": f"File:{filename}",
    })
    data = json.loads(request_bytes(f"https://commons.wikimedia.org/w/api.php?{params}"))
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    info = page["imageinfo"][0]
    return info.get("thumburl") or info["url"]


BOOKS = {
    "alvaro-siza-imagining-the-evident": {
        "cover_candidates": [
            "https://covers.openlibrary.org/b/isbn/9789899948594-L.jpg",
            "https://books.google.com/books/content?id=jgGGzgEACAAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api",
        ],
        "cover_source": "https://www.monadebooks.com/products/imagining-the-evident",
        "cover_credit": "monade / Álvaro Siza",
        "images": [
            ("02-boa-nova.jpg", "Boa Nova 茶室", "Boa Nova Tea House Renovation.jpg", "Joaomorgado", "CC BY-SA 4.0"),
            ("03-leca-pools.jpg", "莱萨海水泳池", "Piscinas Leça.jpg", "Sara silva", "CC BY-SA 3.0"),
            ("04-malagueira.jpg", "马拉盖拉住宅区", "Evora seen from the Quinta da Malagueira Photo by Christian Gänshirt.JPG", "Christian Gänshirt", "CC BY-SA 4.0"),
            ("05-cgac.jpg", "加利西亚当代艺术中心", "Centro Galego de Arte Contemporánea, Santiago de Compostela, Galiza.jpg", "regueifeiro", "CC BY 2.0"),
        ],
    },
    "alvaro-siza-writings-on-architecture": {
        "cover_candidates": [
            "https://books.google.com/books/content?id=lzwzzgEACAAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api",
            "https://covers.openlibrary.org/b/isbn/9788881183159-L.jpg",
        ],
        "cover_source": "https://books.google.com/books/about/Writings_on_Architecture.html?id=lzwzzgEACAAJ",
        "cover_credit": "Google Books / Skira",
        "images": [
            ("02-serralves.jpg", "塞拉维斯当代艺术博物馆", "Museu Serralves I.jpg", "Sara silva", "CC BY-SA 3.0"),
            ("03-portugal-pavilion.jpg", "1998 葡萄牙国家馆", "Lisbon - Portuguese National Pavilion by Alvaro Siza 1998 World Expo (22588530074).jpg", "royckmeyer", "CC BY-SA 2.0"),
            ("04-santa-maria.jpg", "马尔科·德·卡纳维泽斯圣玛利亚教堂", "Marco Canavezes' Church - Alvaro Siza Vieira (1933) (197037227).jpg", "Pedro Ribeiro Simões", "CC BY 2.0"),
            ("05-ibere-camargo.jpg", "伊贝雷·卡马戈基金会", "Fundação Iberê Camargo 021.JPG", "Paulo rsmenezes", "CC BY-SA 4.0"),
        ],
    },
    "oscar-niemeyer-curves-of-time": {
        "cover_candidates": [
            "https://covers.openlibrary.org/b/isbn/9780714848570-L.jpg",
            "https://books.google.com/books/content?id=OrgHGQAACAAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api",
        ],
        "cover_source": "https://books.google.com/books/about/The_Curves_of_Time.html?id=OrgHGQAACAAJ",
        "cover_credit": "Google Books / Phaidon",
        "images": [
            ("02-pampulha.jpg", "潘普利亚圣方济各教堂", "Igreja de São Francisco de Assis (37555991674).jpg", "Nicolas de Camaret", "CC BY 2.0"),
            ("03-brasilia-cathedral.jpg", "巴西利亚大教堂", "Catedral de Brasília.JPG", "Acarlos01.sc", "CC BY-SA 3.0"),
            ("04-national-congress.jpg", "巴西国会大厦", "Brazilian National Congress.jpg", "Eurico Zimbres", "CC BY-SA 2.5"),
            ("05-niteroi.jpg", "尼泰罗伊当代艺术博物馆", "Museu Oscar Niemeyer em Niteroi.jpg", "RolandRaia", "CC BY-SA 4.0"),
        ],
    },
}


def request_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=100) as response:
        return response.read()


def valid_image(data: bytes, min_width: int = 240, min_height: int = 300) -> tuple[int, int]:
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        if image.width < min_width or image.height < min_height:
            raise ValueError(f"image too small: {image.width}x{image.height}")
        return image.width, image.height


def download(url: str, path: Path, *, is_cover: bool = False) -> tuple[int, int]:
    if path.exists() and path.stat().st_size > 10_000:
        with Image.open(path) as image:
            return image.width, image.height
    path.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            data = request_bytes(url)
            size = valid_image(data, 240 if is_cover else 700, 300 if is_cover else 500)
            path.write_bytes(data)
            return size
        except Exception as exc:
            last_error = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def download_cover(candidates: list[str], path: Path) -> tuple[str, tuple[int, int]]:
    errors = []
    for url in candidates:
        try:
            return url, download(url, path, is_cover=True)
        except Exception as exc:
            errors.append(f"{url}: {exc}")
            if path.exists():
                path.unlink()
    raise RuntimeError("No valid cover candidate:\n" + "\n".join(errors))


def main() -> None:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    batch_report: dict[str, object] = {}
    for slug, book in BOOKS.items():
        output = ASSET_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        cover_url, cover_size = download_cover(book["cover_candidates"], output / "cover.jpg")
        manifest = [{
            "filename": "cover.jpg",
            "content": "经书目页核对的真实书封",
            "credit": book["cover_credit"],
            "source_url": book["cover_source"],
            "download_url": cover_url,
            "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
            "license_url": "",
            "modifications": "等比缩放、裁切外部留白；未重绘或修改封面文字",
            "dimensions": list(cover_size),
        }]
        for filename, content, commons_name, author, license_name in book["images"]:
            target = output / filename
            image_url = commons_file(commons_name) if target.exists() else commons_api_file(commons_name)
            page = "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(commons_name.replace(" ", "_"), safe="_.()-',&")
            size = download(image_url, target)
            manifest.append({
                "filename": filename,
                "content": content,
                "credit": author,
                "source_url": page,
                "download_url": image_url,
                "license": license_name,
                "license_url": LICENSES[license_name],
                "modifications": "裁切、缩放、轻微调色与图文排版",
                "dimensions": list(size),
            })
            time.sleep(0.8)
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        batch_report[slug] = {item["filename"]: item["dimensions"] for item in manifest}
        print(f"Fetched {slug}: cover {cover_size}, 4 project images")
    (ASSET_ROOT / "download-report.json").write_text(json.dumps(batch_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
