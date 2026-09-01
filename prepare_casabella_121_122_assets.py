from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance
import pypdfium2 as pdfium


ROOT = Path(__file__).resolve().parent
TMP = ROOT / "tmp" / "casabella-121-122"


RIDOLFI = {
    "02": (2465, 831, 10, 4, "03-ridolfi-sketch.jpg"),
    "03": (2629, 1287, 11, 6, "04-ridolfi-elevation.jpg"),
    "04": (2656, 1990, 11, 8, "05-ridolfi-front.jpg"),
    "05": (2745, 1990, 11, 8, "06-ridolfi-model.jpg"),
}


def stitch_zoomify() -> None:
    target = ROOT / "assets" / "casabella-122"
    target.mkdir(parents=True, exist_ok=True)
    for key, (width, height, cols, rows, name) in RIDOLFI.items():
        canvas = Image.new("RGB", (width, height), "white")
        tile_dir = TMP / f"tiles-{key}"
        for y in range(rows):
            for x in range(cols):
                tile = Image.open(tile_dir / f"4-{x}-{y}.jpg").convert("RGB")
                canvas.paste(tile, (x * 256, y * 256))
        canvas = ImageEnhance.Contrast(canvas).enhance(1.05)
        canvas = ImageEnhance.Sharpness(canvas).enhance(1.12)
        canvas.save(target / name, quality=95, subsampling=0, optimize=True)


def render_tessile_pages() -> None:
    target = ROOT / "assets" / "casabella-121"
    target.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(TMP / "mostra-tessile.pdf")
    for page_no in range(len(pdf)):
        page = pdf[page_no]
        image = page.render(scale=2.7).to_pil().convert("RGB")
        image.save(target / f"tessile-source-{page_no + 1:02d}.jpg", quality=94, subsampling=0)


def render_trieste_page() -> None:
    target = ROOT / "assets" / "casabella-121"
    pdf = pdfium.PdfDocument(TMP / "trieste-rationalism.pdf")
    image = pdf[82].render(scale=2.7).to_pil().convert("RGB")
    image.save(target / "trieste-source-83.jpg", quality=94, subsampling=0)


if __name__ == "__main__":
    stitch_zoomify()
    render_tessile_pages()
    render_trieste_page()
