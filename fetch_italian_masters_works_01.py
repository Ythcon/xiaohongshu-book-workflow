#!/usr/bin/env python3
"""Fetch verified covers and openly licensed documentation for three Italian architecture posts."""

from __future__ import annotations

import html
import io
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "italian-masters-works-01"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"

BOOKS = {
    "giuseppe-terragni-transformations": {
        "cover_candidates": [
            "https://covers.openlibrary.org/b/isbn/9781885254962-L.jpg",
            "https://images-na.ssl-images-amazon.com/images/P/1885254962.01.LZZZZZZZ.jpg",
        ],
        "cover_source": "https://www.indigo.ca/en-ca/giuseppe-terragni-transformations-decompositions-critiques/9781885254962.html",
        "cover_credit": "Peter Eisenman / Monacelli Press (book cover)",
        "images": [
            ("02-casa-del-fascio.jpg", "科莫法西斯之家（今 Palazzo Terragni）", "Como Casa del Fascio Terragni.jpg"),
            ("03-novocomum.jpg", "诺沃科穆姆公寓", "Novocomum Apartments, Como, 1980.jpg"),
            ("04-sant-elia.jpg", "圣埃利亚幼儿园", "AsiloSant'Elia02.JPG"),
            ("05-monumento-ai-caduti.jpg", "科莫阵亡将士纪念碑", "Monumento ai Caduti Architetto Giuseppe Terragni Como.jpg"),
        ],
    },
    "aldo-rossi-architecture-of-the-city": {
        "cover_candidates": [
            "https://covers.openlibrary.org/b/isbn/9780262680431-L.jpg",
            "https://books.google.com/books/content?id=1P1PAAAAMAAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api",
        ],
        "cover_source": "https://mitpress.mit.edu/9780262680431/the-architecture-of-the-city/",
        "cover_credit": "The MIT Press (book cover)",
        "images": [
            ("02-gallaratese.jpg", "加拉拉特斯住宅区", "Quartiere Gallaratese.2.jpg"),
            ("03-san-cataldo.jpg", "圣卡塔尔多公墓", "Cubo di Aldo Rossi del cimitero di San Cataldo.jpg"),
            ("04-teatro-del-mondo.jpg", "世界剧场", "Teatro del Mondo.1980.1, Aldo Rossi.jpg"),
            ("05-bonnefanten.jpg", "博纳方腾博物馆", "Bonnefanten2013-08.jpg"),
        ],
    },
    "superstudio-life-without-objects": {
        "cover_candidates": [
            "https://covers.openlibrary.org/b/olid/OL17118114M-L.jpg",
            "https://covers.openlibrary.org/b/isbn/9788884915696-L.jpg",
        ],
        "cover_source": "https://openlibrary.org/books/OL17118114M/Superstudio",
        "cover_credit": "Peter Lang & William Menking / Skira (book cover)",
        "images": [
            ("02-superarchitettura.jpg", "Superarchitettura 1966 展览的 2016 年复原", "Superarchitettura-SUPERSTUDIO 50-MAXXI-2016.jpg"),
            ("03-giovannetti.jpg", "Giovannetti 工厂，皮斯托亚", "Panoramica Azienda Giovannetti.jpg"),
            ("05-superronda.jpg", "Superstudio Superonda 沙发实物", "Superstudio Софа «суперронда». 1966.jpg"),
        ],
        "external_images": [{
            "filename": "04-continuous-monument.jpg",
            "content": "《连续纪念碑》（1969）原作的展览现场实拍",
            "credit": "diametrik",
            "source_url": "https://www.flickr.com/photos/58435577@N00/2730218752",
            "download_url": "https://live.staticflickr.com/3211/2730218752_f31f4a4ab8_c.jpg",
            "license": "CC BY 2.0",
            "license_url": "https://creativecommons.org/licenses/by/2.0/",
        }],
    },
}


def request_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=100) as response:
        return response.read()


def clean_html(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def image_size(data: bytes, *, cover: bool = False, small_ok: bool = False) -> tuple[int, int]:
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        minimum = (160, 200) if cover else ((480, 480) if small_ok else (700, 500))
        if image.width < minimum[0] or image.height < minimum[1]:
            raise ValueError(f"image too small: {image.width}x{image.height}")
        if cover and sum(ImageStat.Stat(image.convert("RGB").resize((64, 64))).stddev) < 5:
            raise ValueError("cover appears blank")
        return image.width, image.height


def download(url: str, path: Path, *, cover: bool = False, small_ok: bool = False) -> tuple[int, int]:
    if path.exists() and path.stat().st_size > 10_000:
        with Image.open(path) as image:
            return image.width, image.height
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            data = request_bytes(url)
            size = image_size(data, cover=cover, small_ok=small_ok)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return size
        except Exception as exc:
            last_error = exc
            time.sleep(1.7 * (attempt + 1))
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def download_cover(candidates: list[str], path: Path) -> tuple[str, tuple[int, int]]:
    errors: list[str] = []
    for url in candidates:
        try:
            return url, download(url, path, cover=True)
        except Exception as exc:
            errors.append(f"{url}: {exc}")
            path.unlink(missing_ok=True)
    raise RuntimeError("No valid cover candidate:\n" + "\n".join(errors))


def commons_info(filename: str, width: int = 2000) -> dict[str, str]:
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo", "iiprop": "url|extmetadata",
        "iiurlwidth": str(width), "titles": f"File:{filename}",
    })
    payload = json.loads(request_bytes(f"https://commons.wikimedia.org/w/api.php?{params}"))
    page = next(iter(payload["query"]["pages"].values()))
    if "missing" in page:
        raise FileNotFoundError(filename)
    info = page["imageinfo"][0]
    meta = info.get("extmetadata", {})
    get = lambda key: clean_html(meta.get(key, {}).get("value"))
    return {
        # Special:Redirect asks Commons for a scaled derivative; it avoids repeatedly
        # pulling multi-megabyte originals and is friendlier to the media CDN.
        "download_url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/" + urllib.parse.quote(filename.replace(" ", "_"), safe="_.()-',&«»") + f"?width={width}",
        "source_url": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(filename.replace(" ", "_"), safe="_.()-',&«»"),
        "credit": get("Artist") or get("Credit") or "Wikimedia Commons contributor",
        "license": get("LicenseShortName") or get("UsageTerms") or "See source page",
        "license_url": get("LicenseUrl"),
    }


def main() -> None:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    for slug, book in BOOKS.items():
        folder = ASSET_ROOT / slug
        folder.mkdir(parents=True, exist_ok=True)
        cover_url, cover_size = download_cover(book["cover_candidates"], folder / "cover.jpg")
        manifest: list[dict[str, object]] = [{
            "filename": "cover.jpg", "content": "经 ISBN 核对的真实书封", "credit": book["cover_credit"],
            "source_url": book["cover_source"], "download_url": cover_url,
            "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人", "license_url": "",
            "modifications": "等比缩放与外部留白；未重绘或修改封面文字", "dimensions": list(cover_size),
        }]
        for target, content, commons_name in book["images"]:
            info = commons_info(commons_name)
            size = download(info["download_url"], folder / target, small_ok=(target == "05-superronda.jpg"))
            manifest.append({
                "filename": target, "content": content, "credit": info["credit"], "source_url": info["source_url"],
                "download_url": info["download_url"], "license": info["license"], "license_url": info["license_url"],
                "modifications": "裁切、缩放、轻微调色与图文排版", "dimensions": list(size),
            })
            time.sleep(1.0)
        for item in book.get("external_images", []):
            size = download(item["download_url"], folder / item["filename"], small_ok=True)
            manifest.append({
                **item,
                "modifications": "裁切、缩放、轻微调色与图文排版",
                "dimensions": list(size),
            })
        (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Fetched {slug}: cover {cover_size}, {len(manifest) - 1} licensed images")


if __name__ == "__main__":
    main()
