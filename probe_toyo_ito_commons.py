"""List candidate real project photographs from Wikimedia Commons."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request


QUERIES = [
    "Sendai Mediatheque Toyo Ito",
    "TOD'S Omotesando Toyo Ito",
    "Tama Art University Library Toyo Ito",
    "Taichung Metropolitan Opera House Toyo Ito",
    "Serpentine Pavilion 2002 Toyo Ito",
    "Tower of Winds Yokohama Toyo Ito",
    "Mikimoto Ginza 2 Toyo Ito",
    "Todai-ji Museum Toyo Ito",
]


def request_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-xhs-book-cards/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


for query in QUERIES:
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrsearch": query,
        "gsrnamespace": "6", "gsrlimit": "10", "prop": "imageinfo",
        "iiprop": "extmetadata|size", "iiurlwidth": "1600",
    })
    data = request_json("https://commons.wikimedia.org/w/api.php?" + params)
    print("\n###", query)
    for page in data.get("query", {}).get("pages", {}).values():
        meta = page.get("imageinfo", [{}])[0].get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "")
        print(page.get("title", ""), "|", page.get("width"), "x", page.get("height"), "|", license_name)
