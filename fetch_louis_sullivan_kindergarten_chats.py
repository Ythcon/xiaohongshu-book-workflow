#!/usr/bin/env python3
"""Fetch the verified Dover cover and eight real Louis Sullivan project photos."""

from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "louis-sullivan-kindergarten-chats"
USER_AGENT = "Codex-xhs-book-cards/1.0"

FILES = [
    ("02-auditorium.jpg", "芝加哥礼堂大厦建筑实景", "Auditorium Building, Michigan Avenue, Chicago, IL (54191615293).jpg"),
    ("03-wainwright.jpg", "圣路易斯温莱特大厦建筑实景", "Wainwright building st louis USA.jpg"),
    ("04-guaranty.jpg", "布法罗担保大厦建筑实景", "Guaranty (Prudential) Building, Church Street and Pearl Street, Buffalo, NY - 52674541052.jpg"),
    ("05-bayard-condict.jpg", "纽约贝亚德—康迪克特大厦建筑实景", "Louis H. Sullivan - Bayard-Condict Building (A), New York, NY.jpg"),
    ("06-sullivan-center.jpg", "芝加哥沙利文中心建筑实景", "Carson Prie Scott and Company Store Building (Sullivan Center), State Street and Madison Street, Chicago, IL - 52900635427.jpg"),
    ("07-owatonna.jpg", "奥瓦通纳国家农民银行建筑实景", "2017BankOwatonnaMN.jpg"),
    ("08-grinnell.jpg", "格林内尔商人国家银行建筑实景", "Louis Sullivan - Merchants' National Bank, Northwest corner of Fourth Avenue & Broad Street, Grinnell, Poweshiek County, IA.jpg"),
    ("09-krause.jpg", "芝加哥克劳斯音乐商店建筑实景", "Krause Music Store Building, Lincoln Avenue, Lincoln Square, Chicago, IL - 52522494677.jpg"),
]


def clean_html(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()


def request_bytes(url: str) -> bytes:
    last_error = None
    for attempt in range(7):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=100) as response:
                return response.read()
        except Exception as error:
            last_error = error
            time.sleep(3.0 * (attempt + 1))
    raise RuntimeError(f"download failed: {url}: {last_error}")


def commons_records() -> dict[str, dict[str, str]]:
    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "redirects": "1",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size",
        "iiurlwidth": "1920",
        "titles": "|".join("File:" + filename for _, _, filename in FILES),
    })
    payload = json.loads(request_bytes("https://commons.wikimedia.org/w/api.php?" + params))
    records = {}
    for page in payload["query"]["pages"].values():
        if "missing" in page:
            raise FileNotFoundError(page.get("title"))
        info = page["imageinfo"][0]
        metadata = info.get("extmetadata", {})
        get = lambda key: clean_html(metadata.get(key, {}).get("value"))
        filename = page["title"].removeprefix("File:")
        records[filename] = {
            "download_url": info.get("thumburl") or info["url"],
            "source_url": info["descriptionurl"],
            "credit": get("Artist") or get("Credit") or "Wikimedia Commons contributor",
            "license": get("LicenseShortName") or get("UsageTerms") or "See source page",
            "license_url": get("LicenseUrl"),
        }
    # Map normalized/redirected page titles back to requested titles.
    for normalized in payload.get("query", {}).get("normalized", []):
        old = normalized["from"].removeprefix("File:")
        new = normalized["to"].removeprefix("File:")
        if new in records:
            records[old] = records[new]
    for redirect in payload.get("query", {}).get("redirects", []):
        old = redirect["from"].removeprefix("File:")
        new = redirect["to"].removeprefix("File:")
        if new in records:
            records[old] = records[new]
    return records


def image_dimensions(data: bytes) -> tuple[int, int]:
    with Image.open(BytesIO(data)) as image:
        size = image.size
        image.verify()
    return size


def main() -> None:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    cover_url = "https://covers.openlibrary.org/b/isbn/0486238121-L.jpg"
    cover = ASSET_ROOT / "cover.jpg"
    if not cover.exists() or cover.stat().st_size < 8_000:
        cover.write_bytes(request_bytes(cover_url))
    cover_size = image_dimensions(cover.read_bytes())
    if min(cover_size) < 250:
        raise ValueError(f"book cover too small or missing: {cover_size}")

    manifest = [{
        "filename": "cover.jpg",
        "content": "1979 年 Dover 英文版真实书封",
        "credit": "Louis H. Sullivan / Dover Publications (book cover)",
        "source_url": "https://openlibrary.org/books/OL4427653M/Kindergarten_chats_and_other_writings",
        "download_url": cover_url,
        "license": "书封仅用于书籍识别、介绍与评论；版权归原权利人",
        "license_url": "",
        "modifications": "等比缩放与外部留白；未重绘或修改封面文字",
        "dimensions": list(cover_size),
    }]

    records = commons_records()
    for target, content, filename in FILES:
        if filename not in records:
            raise KeyError(f"Commons record not found: {filename}; available={list(records)}")
        record = records[filename]
        path = ASSET_ROOT / target
        if target == "07-owatonna.jpg" or not path.exists() or path.stat().st_size < 10_000:
            path.write_bytes(request_bytes(record["download_url"]))
        size = image_dimensions(path.read_bytes())
        if min(size) < 700:
            raise ValueError(f"case image too small: {target} {size}")
        manifest.append({
            "filename": target,
            "content": content,
            **record,
            "modifications": "裁切、缩放、轻微调色与图文排版",
            "dimensions": list(size),
        })
        print(target, *size, record["license"])
        time.sleep(2.2)

    (ASSET_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("cover.jpg", *cover_size)


if __name__ == "__main__":
    main()
