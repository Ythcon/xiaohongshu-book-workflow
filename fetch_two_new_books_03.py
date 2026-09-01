#!/usr/bin/env python3
"""Download verified covers and licensed architecture photographs for two book posts."""

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
ASSET_ROOT = ROOT / "assets" / "two-new-books-03"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"


BOOKS = {
    "rafael-moneo-apuntes-sobre-21-obras": {
        "cover_candidates": [
            "https://rafaelmoneo.com/wp/wp-content/uploads/2016/10/image1web.jpg",
            "https://covers.openlibrary.org/b/isbn/9781580932165-L.jpg",
            "https://books.google.com/books/content?id=RaJNEAAAQBAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api",
        ],
        "cover_source": "https://rafaelmoneo.com/en/publicaciones/rafael-moneo-remarks-on-21-works/",
        "cover_credit": "Rafael Moneo Arquitecto / Gustavo Gili",
        "images": [
            ("02-merida.jpg", "梅里达罗马艺术博物馆室内", "Interior of the Museo Nacional de Arte Romano.jpg"),
            ("03-kursaal.jpg", "圣塞巴斯蒂安库萨尔会议中心", "Cubos Moneo Kursaal San Sebastian 06 2012 2588.jpg"),
            ("04-la-cathedral.jpg", "洛杉矶天使之后主教座堂", "Cathedral of Our Lady of the Angels-8.jpg"),
            ("05-prado.jpg", "普拉多博物馆扩建", "Ampliación del museo del Prado (2).jpg"),
        ],
    },
    "frei-otto-finding-form": {
        "cover_candidates": [
            "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9783930698660/finding-form-9783930698660_hr.jpg",
            "https://covers1.booksamillion.com/covers/bam/3/93/069/866/3930698668_b.jpg",
            "https://covers.openlibrary.org/b/isbn/9783930698660-L.jpg",
        ],
        "cover_source": "https://www.simonandschuster.com/books/Finding-Form/Frei-Otto/9783930698660",
        "cover_credit": "Edition Axel Menges / Simon & Schuster",
        "images": [
            ("02-ile-stuttgart.jpg", "斯图加特轻型结构研究所实验建筑", "0136-Stuttgart-Otto.jpg"),
            ("03-munich.jpg", "慕尼黑奥林匹克公园张拉屋顶", "Munich - Frei Otto Tensed structures - 5293.jpg"),
            ("04-multihalle.jpg", "曼海姆多功能厅木网壳", "Multihalle Mannheim, Innenraum große Halle.jpg"),
            ("05-japan-pavilion.jpg", "2000年汉诺威世博会日本馆", "Expo2000Japan.jpg"),
        ],
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


def image_size(data: bytes, *, cover: bool = False) -> tuple[int, int]:
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        minimum = (160, 200) if cover else (700, 500)
        if image.width < minimum[0] or image.height < minimum[1]:
            raise ValueError(f"image too small: {image.width}x{image.height}")
        if cover:
            sample = image.convert("RGB").resize((64, 64))
            if sum(ImageStat.Stat(sample).stddev) < 5:
                raise ValueError("cover appears blank")
        return image.width, image.height


def download(url: str, path: Path, *, cover: bool = False) -> tuple[int, int]:
    if path.exists() and path.stat().st_size > 10_000:
        with Image.open(path) as image:
            return image.width, image.height
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            data = request_bytes(url)
            size = image_size(data, cover=cover)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return size
        except Exception as exc:
            last_error = exc
            time.sleep(2.0 * (attempt + 1))
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
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": str(width),
        "titles": f"File:{filename}",
    })
    payload = json.loads(request_bytes(f"https://commons.wikimedia.org/w/api.php?{params}"))
    page = next(iter(payload["query"]["pages"].values()))
    if "missing" in page:
        raise FileNotFoundError(filename)
    info = page["imageinfo"][0]
    meta = info.get("extmetadata", {})
    get = lambda key: clean_html(meta.get(key, {}).get("value"))
    return {
        "download_url": info.get("thumburl") or info["url"],
        "source_url": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(filename.replace(" ", "_"), safe="_.()-',&"),
        "credit": get("Artist") or get("Credit") or "Wikimedia Commons contributor",
        "license": get("LicenseShortName") or get("UsageTerms") or "See source page",
        "license_url": get("LicenseUrl"),
    }


def main() -> None:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {}
    for slug, book in BOOKS.items():
        output = ASSET_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        cover_url, cover_size = download_cover(book["cover_candidates"], output / "cover.jpg")
        manifest: list[dict[str, object]] = [{
            "filename": "cover.jpg",
            "content": "经书目页与 ISBN 核对的真实书封",
            "credit": book["cover_credit"],
            "source_url": book["cover_source"],
            "download_url": cover_url,
            "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
            "license_url": "",
            "modifications": "等比缩放与外部留白；未重绘或修改封面文字",
            "dimensions": list(cover_size),
        }]
        for target_name, content, commons_name in book["images"]:
            info = commons_info(commons_name)
            size = download(info["download_url"], output / target_name)
            manifest.append({
                "filename": target_name,
                "content": content,
                "credit": info["credit"],
                "source_url": info["source_url"],
                "download_url": info["download_url"],
                "license": info["license"],
                "license_url": info["license_url"],
                "modifications": "裁切、缩放、轻微调色与图文排版",
                "dimensions": list(size),
            })
            time.sleep(1.2)
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report[slug] = {item["filename"]: item["dimensions"] for item in manifest}
        print(f"Fetched {slug}: cover {cover_size}, 4 project images")
    (ASSET_ROOT / "download-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
