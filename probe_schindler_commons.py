"""List usable Wikimedia Commons candidates for R. M. Schindler projects."""
from __future__ import annotations
import json
import urllib.parse
import urllib.request

QUERIES = [
    "Schindler House Kings Road R. M. Schindler",
    "Lovell Beach House R. M. Schindler",
    "Pueblo Ribera Court Schindler",
    "Falk Apartments Schindler",
    "How House R. M. Schindler",
    "Schindler Chace House California",
    "Mackey Apartments Schindler",
    "Scherer House R. M. Schindler",
]

def query(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-xhs-book-cards/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))

for term in QUERIES:
    params = urllib.parse.urlencode({"action":"query", "format":"json", "generator":"search", "gsrsearch":term, "gsrnamespace":"6", "gsrlimit":"12", "prop":"imageinfo", "iiprop":"extmetadata|size", "iiurlwidth":"1800"})
    data = query("https://commons.wikimedia.org/w/api.php?" + params)
    print("\n###", term)
    for page in data.get("query", {}).get("pages", {}).values():
        info = page.get("imageinfo", [{}])[0]
        license_name = info.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "")
        print(page.get("title"), "|", info.get("width"), "x", info.get("height"), "|", license_name)
