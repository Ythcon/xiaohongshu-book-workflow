"""Download the two remaining verified Commons file paths without a bulk API query."""
from pathlib import Path
import urllib.request

root = Path(__file__).resolve().parent / "assets" / "schindler-exploration-space"
files = {
    "08-kings-road-archive.jpg": "https://commons.wikimedia.org/wiki/Special:FilePath/Schindler-Chase%20house%20%28Rudolf%20Schindler%29%2C%201922%20c.jpg?width=1200",
    "09-kings-road-light.jpg": "https://commons.wikimedia.org/wiki/Special:FilePath/Schindler-Chase%20house%20%28Rudolf%20Schindler%29%2C%201922%20d.jpg?width=1200",
}
for name, url in files.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Codex-xhs-book-cards/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read()
    (root / name).write_bytes(data)
    print(name, len(data))
