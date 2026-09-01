#!/usr/bin/env python3
"""Fetch verified covers and licensed project images for Rudolph and Stirling."""

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
ASSET_ROOT = ROOT / "assets" / "two-new-books-02"
USER_AGENT = "Codex-XHS-Book-Cards/1.0 (local editorial research)"


BOOKS = {
    "paul-rudolph-writings-on-architecture": {
        "cover_candidates": [
            "https://images.squarespace-cdn.com/content/v1/5a75ee0949fc2bc37b3ffb97/1568487823076-96MHK1NQ7SPVMFRYIUSC/writings+book+cover.jpg",
            "https://covers.openlibrary.org/b/olid/OL22552800M-L.jpg",
            "https://covers.openlibrary.org/b/isbn/9780300150926-L.jpg",
        ],
        "cover_source": "https://www.paulrudolph.institute/news/category/Writings",
        "cover_credit": "Paul Rudolph Institute for Modern Architecture / Yale School of Architecture",
        "images": [
            ("02-rudolph-hall.jpg", "鲁道夫楼（原耶鲁艺术与建筑大楼）", "Yale-Art-and-Architecture-Building-Rudolph-Hall-New-Haven-Connecticut-Apr-2014.jpg"),
            ("03-milam-house.jpg", "米拉姆住宅", "Arthur Milam House, Ponte Vedra, FL, US (02).jpg"),
            ("04-boston-gsc.jpg", "波士顿政府服务中心", "Paul Rudolph - Boston Government Services Center (14989170661).jpg"),
            ("05-umass-dartmouth.jpg", "马萨诸塞大学达特茅斯校区", "Paul Rudolph, 1960’s - Flickr - Seth Tisue.jpg"),
        ],
    },
    "james-stirling-early-unpublished-writings": {
        "cover_candidates": [
            "https://images.routledge.com/common/jackets/crclarge/978041555/9780415550598.jpg",
        ],
        "cover_source": "https://www.routledge.com/James-Stirling-Early-Unpublished-Writings-on-Architecture/Crinson/p/book/9780415550598",
        "cover_credit": "Routledge / Taylor & Francis",
        "images": [
            ("02-langham.jpg", "兰厄姆住宅区", "Ham Common, Langham House Close (1).jpg"),
            ("03-leicester.jpg", "莱斯特大学工程楼", "Leicester University Engineering Building 2.jpg"),
            ("04-cambridge-history.jpg", "剑桥大学历史系楼", "James stirling, cambridge university history faculty building, 1964-1967 (4928152576).jpg"),
            ("05-florey.jpg", "牛津大学弗洛里楼", "James stirling, florey building, oxford 1966-1971 (5122476997).jpg"),
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
        # Some publishers expose only a 180x270 official jacket. Accuracy takes
        # priority over replacing it with a cleaner but unverified marketplace scan.
        minimum = (160, 240) if cover else (700, 500)
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


def commons_info(filename: str, width: int = 1800) -> dict[str, str]:
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
            time.sleep(1.4)
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report[slug] = {item["filename"]: item["dimensions"] for item in manifest}
        print(f"Fetched {slug}: cover {cover_size}, 4 project images")
    (ASSET_ROOT / "download-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
