#!/usr/bin/env python3
"""Fetch an official Taschen cover and eight real Schindler project images."""
from __future__ import annotations
import html, json, re, time, urllib.parse, urllib.request
from io import BytesIO
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "schindler-exploration-space"
UA = "Codex-xhs-book-cards/1.0"
FILES = [
    ("02-kings-road-court.jpg", "辛德勒—切斯住宅庭院", "Schindler-Chase house (Rudolf Schindler), 1922.jpg"),
    ("03-kings-road-wall.jpg", "辛德勒—切斯住宅墙体与庭院", "Schindler-Chase house (Rudolf Schindler), 1922 b.jpg"),
    ("04-lovell-wide.jpg", "洛弗尔海滩住宅西南全景", "GENERAL VIEW FROM SOUTHWEST - Lovell Beach House, 1242 West Ocean Front, Newport Beach, Orange County, CA HABS CAL,30-NEWBE,1-1.tif"),
    ("05-lovell-living.jpg", "洛弗尔海滩住宅起居空间", "CLERESTORY, LIVING AREA - Lovell Beach House, 1242 West Ocean Front, Newport Beach, Orange County, CA HABS CAL,30-NEWBE,1-8.tif"),
    ("06-pueblo-corner.jpg", "普韦布洛里贝拉公寓转角", "Corner view, Gravilla Street unit - Pueblo Ribera Court, 230 Granvilla Street, La Jolla, San Diego County, CA HABS CAL,37-LAJOL,3-3.tif"),
    ("07-pueblo-terrace.jpg", "普韦布洛里贝拉公寓露台壁炉", "Fireplace, terrace - Pueblo Ribera Court, 230 Granvilla Street, La Jolla, San Diego County, CA HABS CAL,37-LAJOL,3-10.tif"),
]

def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()
def get_bytes(url: str) -> bytes:
    last = None
    for retry in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=100) as response: return response.read()
        except Exception as exc:
            last = exc; time.sleep(2 + retry)
    raise RuntimeError(f"Download failed: {url}: {last}")
def size(data: bytes) -> tuple[int, int]:
    with Image.open(BytesIO(data)) as image:
        value = image.size; image.verify()
    return value
def records() -> dict[str, dict[str, str]]:
    params = urllib.parse.urlencode({"action":"query", "format":"json", "redirects":"1", "prop":"imageinfo", "iiprop":"url|extmetadata|size", "iiurlwidth":"1920", "titles":"|".join("File:" + f for _, _, f in FILES)})
    data = json.loads(get_bytes("https://commons.wikimedia.org/w/api.php?" + params))
    result = {}
    for page in data.get("query", {}).get("pages", {}).values():
        if "missing" in page: raise FileNotFoundError(page.get("title"))
        info = page["imageinfo"][0]; meta = info.get("extmetadata", {})
        field = lambda name: clean(meta.get(name, {}).get("value"))
        result[page["title"].removeprefix("File:")] = {"download_url": info.get("thumburl") or info["url"], "source_url": info["descriptionurl"], "credit": field("Artist") or field("Credit") or "Wikimedia Commons contributor", "license": field("LicenseShortName") or field("UsageTerms") or "See source page", "license_url": field("LicenseUrl")}
    return result
def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    cover_url = "https://taschen.makaira.media/taschen/image/upload/v1745415961/products-live/b4212c028efb4c8361a99899793e4052.png"
    cover = ASSETS / "cover.png"
    if not cover.exists() or cover.stat().st_size < 10_000:
        cover.write_bytes(get_bytes(cover_url))
    cover_size = size(cover.read_bytes())
    if min(cover_size) < 500: raise ValueError(f"cover too small: {cover_size}")
    manifest = [{"filename":"cover.png", "content":"Taschen 英文精装《Schindler》真实书封", "credit":"TASCHEN (book cover)", "source_url":"https://www.taschen.com/en/books/architecture-design/43147/schindler/", "download_url":cover_url, "license":"书封仅用于书籍识别、介绍与评论；版权归原权利人", "license_url":"", "modifications":"等比缩放与外部留白；未重绘或修改封面文字", "dimensions":list(cover_size)}]
    source = records()
    for target, content, filename in FILES:
        record = source.get(filename)
        if not record: raise KeyError(filename)
        output = ASSETS / target
        if not output.exists() or output.stat().st_size < 10_000:
            output.write_bytes(get_bytes(record["download_url"]))
        dimensions = size(output.read_bytes())
        if min(dimensions) < 500: raise ValueError(f"image too small: {target} {dimensions}")
        manifest.append({"filename":target, "content":content, **record, "modifications":"裁切、缩放、轻微调色与图文排版", "dimensions":list(dimensions)})
        print(target, dimensions, record["license"]); time.sleep(1.2)
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("cover.png", cover_size)
if __name__ == "__main__": main()
