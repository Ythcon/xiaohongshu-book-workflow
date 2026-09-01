from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent


def crop_bawa_cover() -> None:
    src = Image.open(ROOT / "assets/geoffrey-bawa-drawing-archives/book-cover.jpg").convert("RGB")
    # 官方商品照仅裁掉书体之外的留白与投影，不改动封面文字或图形。
    src.crop((365, 220, 835, 865)).save(
        ROOT / "assets/geoffrey-bawa-drawing-archives/book-cover-cropped.jpg",
        quality=95,
        subsampling=0,
    )


def bawa_background() -> None:
    w, h = 1242, 1660
    im = Image.new("RGB", (w, h), "#173A73")
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 0, w, 310), fill=(241, 235, 220, 255))
    d.rectangle((790, 0, w, h), fill=(15, 35, 61, 185))
    d.polygon([(0, 980), (470, 570), (900, 760), (1242, 520), (1242, 1660), (0, 1660)], fill=(36, 91, 83, 190))
    for i in range(16):
        y = 470 + i * 58
        pts = []
        for x in range(-80, 1320, 40):
            drift = 34 * ((x // 80 + i) % 3 - 1)
            pts.append((x, y + drift))
        d.line(pts, fill=(244, 121, 73, 150), width=3)
    d.ellipse((835, 1120, 1120, 1405), outline=(241, 235, 220, 180), width=8)
    im.filter(ImageFilter.GaussianBlur(0.25)).save(
        ROOT / "assets/geoffrey-bawa-drawing-archives/cover-system.jpg",
        quality=94,
        subsampling=0,
    )


def barragan_background() -> None:
    w, h = 1242, 1660
    im = Image.new("RGB", (w, h), "#C81D58")
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 0, 470, h), fill=(245, 153, 37, 255))
    d.polygon([(470, 0), (1242, 0), (1242, 690), (780, 820), (470, 690)], fill=(199, 24, 82, 255))
    d.polygon([(470, 690), (780, 820), (1242, 690), (1242, 1660), (470, 1660)], fill=(62, 54, 118, 255))
    d.rectangle((0, 1160, 1242, 1190), fill=(246, 226, 153, 230))
    d.polygon([(470, 0), (640, 0), (930, 1660), (760, 1660)], fill=(255, 239, 194, 55))
    im.save(
        ROOT / "assets/luis-barragan-space-shadow/cover-system.jpg",
        quality=95,
        subsampling=0,
    )


if __name__ == "__main__":
    crop_bawa_cover()
    bawa_background()
    barragan_background()
