"""List Wikimedia Commons candidates for Kenzo Tange projects."""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

QUERIES = [
    "Hiroshima Peace Memorial Museum Kenzo Tange",
    "Yoyogi National Gymnasium Kenzo Tange",
    "Kagawa Prefectural Government Hall Kenzo Tange",
    "Shizuoka Press Broadcasting Center Kenzo Tange",
    "St Mary's Cathedral Tokyo Kenzo Tange",
    "Kurashiki City Hall Kenzo Tange",
    "Hiroshima Peace Memorial Park Kenzo Tange",
    "Tokyo Metropolitan Government Building Kenzo Tange",
]

def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Codex-xhs-book-cards/1.0"})
    with urllib.request.urlopen(req, timeout=60) as res:
        return json.loads(res.read().decode("utf-8"))

for query in QUERIES:
    params = urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search", "gsrsearch": query, "gsrnamespace": "6", "gsrlimit": "12", "prop": "imageinfo", "iiprop": "extmetadata|size", "iiurlwidth": "1800"})
    data = get("https://commons.wikimedia.org/w/api.php?" + params)
    print("\n###", query)
    for page in data.get("query", {}).get("pages", {}).values():
        info = page.get("imageinfo", [{}])[0]
        license_name = info.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "")
        print(page.get("title"), "|", info.get("width"), "x", info.get("height"), "|", license_name)
