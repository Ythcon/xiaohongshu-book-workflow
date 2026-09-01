from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance
import pypdfium2 as pdfium


ROOT = Path(__file__).resolve().parent
TMP = ROOT / "tmp" / "casabella-123-124"


def render(pdf_path: Path, page_number: int, output: Path, scale: float = 3.4) -> None:
    document = pdfium.PdfDocument(pdf_path)
    image = document[page_number - 1].render(scale=scale).to_pil().convert("RGB")
    image = ImageEnhance.Contrast(image).enhance(1.05)
    image = ImageEnhance.Sharpness(image).enhance(1.10)
    image.save(output, quality=96, subsampling=0, optimize=True)


def main() -> None:
    issue_123 = ROOT / "assets" / "casabella-123"
    issue_124 = ROOT / "assets" / "casabella-124"
    issue_123.mkdir(parents=True, exist_ok=True)
    issue_124.mkdir(parents=True, exist_ok=True)

    case_fascio = TMP / "case-fascio-italia.pdf"
    render(case_fascio, 142, issue_123 / "07-sesto-calende-drawings.jpg")
    render(case_fascio, 143, issue_123 / "08-sesto-calende-photo.jpg")
    sesto = Image.open(issue_123 / "07-sesto-calende-drawings.jpg").convert("RGB")
    sesto.crop((80, 1030, 1160, 1680)).save(
        issue_123 / "04-sesto-calende-siteplan.jpg", quality=96, subsampling=0, optimize=True
    )
    sesto.crop((1100, 1770, 2200, 2560)).save(
        issue_123 / "07-sesto-calende-sections.jpg", quality=96, subsampling=0, optimize=True
    )

    nervi = TMP / "neri-capolavori.pdf"
    render(nervi, 10, issue_124 / "07-nervi-brief.jpg")
    render(nervi, 23, issue_124 / "08-nervi-prefab-model.jpg")
    render(nervi, 25, issue_124 / "09-nervi-wind-test.jpg")
    models = Image.open(issue_124 / "08-nervi-prefab-model.jpg").convert("RGB")
    models.crop((100, 140, 1860, 2240)).save(
        issue_124 / "06-nervi-models.jpg", quality=96, subsampling=0, optimize=True
    )


if __name__ == "__main__":
    main()
