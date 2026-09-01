from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "sourced-eight-books"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "XiaohongshuArchitectureEditorial/1.0 (local research workflow)"


SETS = {
    "01-eyes-of-skin": [
        ("hero", "Villa Mairea through trees"),
        ("c1", "Villa Mairea interior"),
        ("c2", "Studio Aalto Helsinki"),
        ("02", "Saynatsalo Town Hall"),
        ("02b", "Paimio Sanatorium interior"),
        ("03", "Saynatsalo Town Hall interior"),
        ("04", "Paimio Sanatorium"),
        ("05", "Helsinki AaltoHouse 01"),
        ("summary", "Finlandia Hall interior"),
        ("06b", "Finlandia Hall Helsinki exterior"),
    ],
    "02-experiencing-architecture": [
        ("hero", "Pantheon oculus"),
        ("c1", "Pantheon exterior Rome"),
        ("c2", "Villa Rotonda interior"),
        ("02", "Pantheon Rome interior"),
        ("02b", "Bramante Tempietto exterior"),
        ("03", "Piazza del Campidoglio"),
        ("04", "Piazza San Marco Venice"),
        ("05", "Doge's Palace Venice arcade"),
        ("summary", "Santa Maria Maggiore interior"),
        ("06b", "Piazza San Marco colonnade Venice"),
    ],
    "03-genius-loci": [
        ("hero", "Prague skyline - panoramio"),
        ("c1", "Prague Mala Strana street"),
        ("c2", "Prague Old Town aerial"),
        ("02", "Old Town Square Prague"),
        ("02b", "Charles Bridge Prague panorama"),
        ("03", "Piazza Navona"),
        ("04", "Roman Forum"),
        ("05", "Trastevere street Rome Italy"),
        ("summary", "Charles Bridge Prague"),
        ("06b", "Piazza del Campo aerial Siena"),
    ],
    "04-death-and-life": [
        ("hero", "Greenwich Village street"),
        ("c1", "Greenwich Village pedestrians"),
        ("c2", "New York stoop Greenwich Village"),
        ("02", "Washington Square Arch, New York"),
        ("02b", "Washington Square Park daytime public life New York"),
        ("03", "Greenwich Village storefront"),
        ("04", "West 4th Street Greenwich Village 001"),
        ("05", "Greenwich Village cafe"),
        ("summary", "Washington Square Park - New York City - September 2025"),
        ("06b", "Bleecker Street Greenwich Village"),
    ],
    "05-architecture-city": [
        ("hero", "San Cataldo Cemetery Aldo Rossi"),
        ("c1", "Cubo di Aldo Rossi del cimitero di San Cataldo"),
        ("c2", "Teatro Carlo Felice exterior Genoa"),
        ("02", "San Cataldo Cemetery Modena"),
        ("02b", "Complesso abitativo gallaratese Monte Amiata 4"),
        ("03", "Gallaratese Aldo Rossi"),
        ("04", "Teatro del Mondo.1980.1, Aldo Rossi"),
        ("05", "Bonnefanten Museum"),
        ("summary", "Schutzenstrasse Aldo Rossi Berlin"),
        ("06b", "Schutzenstrasse Berlin Aldo Rossi"),
    ],
    "06-image-city": [
        ("hero", "Boston skyline"),
        ("c1", "Boston street map downtown"),
        ("c2", "Boston street network aerial"),
        ("02", "Boston downtown aerial"),
        ("02b", "Boston Marshall and Union intersection"),
        ("03", "Jersey City skyline"),
        ("04", "Los Angeles aerial"),
        ("05", "Los Angeles City Hall"),
        ("summary", "Boston Back Bay street"),
        ("06b", "Los Angeles freeway interchange aerial"),
    ],
    "07-pattern-language": [
        ("hero", "Paley Park New York"),
        ("c1", "Kresge College UC Santa Cruz"),
        ("c2", "courtyard arcade architecture"),
        ("02", "California Landmark No. 871 The Gamble House - panoramio"),
        ("02b", "Gamble House entrance Pasadena"),
        ("03", "Gamble House 2016-10"),
        ("04", "Spanish steps (5200572167)"),
        ("05", "Paley Park (54036)"),
        ("summary", "The Piazza Del Campo, Siena, Italy"),
        ("06b", "Spanish Steps people Rome"),
    ],
    "08-form-space-order": [
        ("hero", "Barcelona Pavilion interior"),
        ("c1", "Farnsworth House exterior"),
        ("c2", "Fallingwater exterior"),
        ("02", "Van der Rohe Pavillion overview"),
        ("02b", "Hagia Sophia interior dome Istanbul"),
        ("03", "Montreal - 26 - Vista de Habitat 67"),
        ("04", "Guggenheim Museum interior"),
        ("05", "Salk Institute Highsmith"),
        ("summary", "Villa La Rotonda"),
        ("06b", "Pantheon Rome exterior"),
    ],
}


DIRECT_TITLES = {
    ("01-eyes-of-skin", "05"): "File:Helsinki AaltoHouse 01.jpg",
    ("04-death-and-life", "02"): "File:Washington Square Arch, New York.jpg",
    ("03-genius-loci", "02b"): "File:Charles Bridge - panorama.jpg",
    ("04-death-and-life", "02b"): "File:Washington Square Park, New York.jpg",
    ("04-death-and-life", "04"): "File:West 4th Street Greenwich Village 001.jpg",
    ("04-death-and-life", "summary"): "File:Washington Square Park - New York City - September 2025.jpg",
    ("02-experiencing-architecture", "02b"): "File:01 Bramante Tempietto Exterior.jpg",
    ("05-architecture-city", "04"): "File:Teatro del Mondo.1980.1, Aldo Rossi.jpg",
    ("05-architecture-city", "c1"): "File:Cubo di Aldo Rossi del cimitero di San Cataldo.jpg",
    ("05-architecture-city", "c2"): "File:Teatro Carlo Felice (esterno) - Genova.jpg",
    ("05-architecture-city", "02b"): "File:Complesso abitativo gallaratese Monte Amiata 4.jpg",
    ("06-image-city", "02"): "File:Boston downtown aerial.jpg",
    ("06-image-city", "02b"): "File:Boston, Marshall and Union.jpg",
    ("07-pattern-language", "02"): "File:California Landmark No. 871 The Gamble House - panoramio.jpg",
    ("07-pattern-language", "03"): "File:Gamble House 2016-10.jpg",
    ("07-pattern-language", "04"): "File:Spanish steps (5200572167).jpg",
    ("07-pattern-language", "05"): "File:Paley Park (54036).jpg",
    ("07-pattern-language", "summary"): "File:The Piazza Del Campo, Siena, Italy.jpg",
    ("07-pattern-language", "06b"): "File:Spanish steps.jpg",
    ("08-form-space-order", "hero"): "File:Barcelona Pavilion interior.jpg",
    ("08-form-space-order", "02"): "File:Van der Rohe Pavillion overview.jpg",
    ("08-form-space-order", "03"): "File:Montreal - 26 - Vista de Habitat 67.jpg",
    ("08-form-space-order", "04"): "File:Guggenheim Museum interior.JPG",
    ("08-form-space-order", "05"): "File:Salk Institute Highsmith.jpg",
    ("08-form-space-order", "summary"): "File:Villa La Rotonda.JPG",
}


def clean(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def api_get(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 4:
                raise
            time.sleep(12 * (attempt + 1))
    raise RuntimeError("API retry exhausted")


def search(query: str) -> list[dict]:
    data = api_get({
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": 16,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 1800,
        "format": "json",
        "formatversion": 2,
    })
    return data.get("query", {}).get("pages", [])


def lookup_title(title: str) -> list[dict]:
    data = api_get({
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 1800,
        "format": "json",
        "formatversion": 2,
    })
    return data.get("query", {}).get("pages", [])


def choose(pages: list[dict], used: set[int]) -> dict:
    allowed = ("public domain", "cc0", "cc by", "cc-by", "cc by-sa", "cc-by-sa", "gfdl")
    for page in pages:
        if page.get("pageid") in used:
            continue
        info = (page.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        meta = info.get("extmetadata", {})
        license_name = clean(meta.get("LicenseShortName", {}).get("value")).lower()
        width, height = info.get("width", 0), info.get("height", 0)
        if mime not in {"image/jpeg", "image/png"}:
            continue
        if max(width, height) < 1400:
            continue
        if not any(token in license_name for token in allowed):
            continue
        return page
    raise RuntimeError("No suitable freely licensed image found")


def choose_direct(pages: list[dict], used: set[int]) -> dict:
    for page in pages:
        if page.get("missing") or page.get("pageid") in used:
            continue
        info = (page.get("imageinfo") or [{}])[0]
        if info.get("mime") in {"image/jpeg", "image/png"}:
            return page
    raise RuntimeError("Direct Commons file is missing or duplicated")


def download(url: str, path: Path):
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                path.write_bytes(response.read())
            return
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 4:
                raise
            time.sleep(15 * (attempt + 1))


def save_manifest(manifest: list[dict]):
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "manifest.json"
    manifest: list[dict] = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
    desired = {(set_name, slot): query for set_name, items in SETS.items() for slot, query in items}
    kept: list[dict] = []
    for item in manifest:
        key = (item["set"], item["slot"])
        if desired.get(key) == item.get("query"):
            kept.append(item)
            continue
        old_file = OUT / item["set"] / item["file"]
        if old_file.exists():
            old_file.unlink()
    manifest = kept
    save_manifest(manifest)
    completed = {(item["set"], item["slot"]) for item in manifest}
    used: set[int] = {item["pageid"] for item in manifest if item.get("pageid")}
    for set_name, requests in SETS.items():
        folder = OUT / set_name
        folder.mkdir(parents=True, exist_ok=True)
        for slot, query in requests:
            if (set_name, slot) in completed:
                print(f"Skipping completed {set_name}/{slot}", flush=True)
                continue
            print(f"Searching {set_name}/{slot}: {query}", flush=True)
            direct_title = DIRECT_TITLES.get((set_name, slot))
            pages = lookup_title(direct_title) if direct_title else search(query)
            page = choose_direct(pages, used) if direct_title else choose(pages, used)
            used.add(page["pageid"])
            info = page["imageinfo"][0]
            meta = info.get("extmetadata", {})
            mime = info.get("mime", "image/jpeg")
            ext = ".png" if mime == "image/png" else ".jpg"
            target = folder / f"{slot}{ext}"
            image_url = info.get("thumburl") or info["url"]
            download(image_url, target)
            record = {
                "set": set_name,
                "slot": slot,
                "query": query,
                "file": target.name,
                "commons_title": page["title"],
                "description": clean(meta.get("ImageDescription", {}).get("value")),
                "artist": clean(meta.get("Artist", {}).get("value")),
                "license": clean(meta.get("LicenseShortName", {}).get("value")),
                "license_url": clean(meta.get("LicenseUrl", {}).get("value")),
                "source_page": info.get("descriptionurl", ""),
                "download_url": image_url,
                "pageid": page["pageid"],
            }
            manifest.append(record)
            save_manifest(manifest)
            print(f"  -> {page['title']} [{record['license']}]", flush=True)
            time.sleep(2.0)

    save_manifest(manifest)
    lines = ["# 图片来源（内部记录）", ""]
    for set_name in SETS:
        lines.extend([f"## {set_name}", ""])
        for item in [x for x in manifest if x["set"] == set_name]:
            lines.append(f"- {item['slot']} — {item['commons_title']}；摄影/作者：{item['artist'] or '见原页面'}；许可：{item['license']}；{item['source_page']}")
        lines.append("")
    (OUT / "图片来源.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
