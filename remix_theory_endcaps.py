from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parent
RENDERER = ROOT / "skills/xhs-quick-book-cards/scripts/render_post.py"
SPEC = importlib.util.spec_from_file_location("xhs_renderer", RENDERER)
r = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(r)

W, H = r.W, r.H
PAPER = "#eee9dd"
INK = "#111111"
BLUE = "#173a73"
ORANGE = "#f27949"
GREEN = "#245b53"
MAGENTA = "#c81d58"
YELLOW = "#e1a429"
PLUM = "#38264f"
CREAM = "#f5ead3"


def cfg(slug: str) -> tuple[dict, Path, Path]:
    path = ROOT / "posts" / slug / "post.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data, (path.parent / data["asset_dir"]).resolve(), (path.parent / data["output_dir"]).resolve()


def save(im: Image.Image, output: Path, number: int) -> None:
    im.convert("RGB").save(output / f"{number:02d}.jpg", quality=95, subsampling=0, optimize=True)


def paste_book(canvas: Image.Image, path: Path, xy: tuple[int, int], size: tuple[int, int], border: int = 10) -> None:
    book = r.fit_inside(Image.open(path).convert("RGB"), size)
    x, y = xy
    shadow = Image.new("RGBA", (book.width + 60, book.height + 60), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle((24, 24, book.width + 42, book.height + 42), fill=(0, 0, 0, 145))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.alpha_composite(shadow, (x - 20, y - 18))
    mount = Image.new("RGBA", (book.width + border * 2, book.height + border * 2), r.rgba("#f7f1e4"))
    mount.alpha_composite(book.convert("RGBA"), (border, border))
    canvas.alpha_composite(mount, (x, y))


def bawa_cover(data: dict, assets: Path, output: Path) -> None:
    canvas = Image.new("RGBA", (W, H), r.rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((715, 0, W, H), fill=BLUE)
    draw.rectangle((0, 0, W, 28), fill=ORANGE)
    draw.rectangle((46, 0, 58, H), fill=INK)

    # A route-like archive trace: it carries the thesis instead of decorating a photo.
    route = [(750, 130), (1050, 130), (1050, 310), (835, 310), (835, 515), (1140, 515), (1140, 780)]
    draw.line(route, fill=r.rgba(ORANGE, 205), width=6, joint="curve")
    for x, y in route[1:]:
        draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=ORANGE)
    for i in range(8):
        y = 905 + i * 52
        draw.arc((730 + i * 20, y - 180, 1210 - i * 14, y + 220), 195, 338, fill=r.rgba(CREAM, 75), width=2)

    draw.text((92, 98), "ARCHIVE / DRAWING / PLACE", font=r.fnt(25, bold=True), fill=ORANGE)
    draw.text((92, 148), data["author"], font=r.fnt(28, bold=True), fill=INK)
    r.draw_fitted(draw, (92, 255), data["question"], 565, 430, 83, INK, serif=True, spacing=14)
    draw.multiline_text(
        (92, 750),
        "《Geoffrey Bawa:\nDrawing from the Archives》",
        font=r.fnt(28, serif=True),
        fill=BLUE,
        spacing=8,
    )
    paste_book(canvas, assets / data["book_cover"], (775, 610), (375, 605), 9)

    draw.rectangle((92, 1238, 650, 1248), fill=ORANGE)
    r.draw_fitted(draw, (92, 1285), data["thesis"], 1045, 220, 35, INK, serif=True, spacing=14)
    draw.text((1164, 1588), "01 / 06", font=r.fnt(21), fill=r.rgba(CREAM, 190), anchor="ra")
    save(canvas, output, 1)


def bawa_summary(data: dict, assets: Path, output: Path) -> None:
    photo = r.cover_crop(Image.open(assets / "cover-background.jpg").convert("RGB"), (470, H), (0.52, 0.48))
    photo = ImageEnhance.Contrast(photo).enhance(1.08)
    canvas = Image.new("RGBA", (W, H), r.rgba(PAPER))
    canvas.alpha_composite(photo.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (470, H), (0, 0, 0, 74)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((462, 0, 478, H), fill=ORANGE)
    draw.text((54, 76), "06 / FIELD NOTES", font=r.fnt(24, bold=True), fill=ORANGE)
    draw.text((54, 136), "建成之后，\n设计仍在继续。", font=r.fnt(47, serif=True), fill=CREAM, spacing=16)
    draw.text((540, 82), f"《{data['book']}》", font=r.fnt(28, serif=True), fill=BLUE)
    r.draw_fitted(draw, (540, 170), data["summary"]["statement"], 620, 430, 59, INK, serif=True, spacing=20)

    labels = data["summary"]["concepts"][:3]
    ys = [620, 820, 1020]
    draw.line((470, ys[0], 470, ys[-1]), fill=BLUE, width=5)
    for i, (label, y) in enumerate(zip(labels, ys), 1):
        draw.ellipse((431, y - 39, 509, y + 39), fill=[BLUE, YELLOW, ORANGE][i - 1])
        draw.text((470, y), str(i), font=r.fnt(25, bold=True), fill=CREAM if i == 1 else INK, anchor="mm")
        draw.text((540, y - 22), label, font=r.fnt(38, bold=True), fill=[BLUE, "#9a7d00", ORANGE][i - 1])

    y = 1160
    for i, item in enumerate(data["summary"]["takeaways"][:3], 1):
        draw.text((540, y), f"0{i}", font=r.fnt(24, bold=True), fill=ORANGE)
        r.draw_fitted(draw, (602, y - 4), item, 560, 86, 27, INK, serif=True, spacing=8)
        draw.line((540, y + 82, 1160, y + 82), fill=r.rgba(INK, 55), width=2)
        y += 112
    draw.text((540, 1532), "编辑性概括｜非书中原句", font=r.fnt(22), fill=r.rgba(INK, 145))
    draw.text((1164, 1588), "06 / 06", font=r.fnt(21), fill=r.rgba(INK, 150), anchor="ra")
    save(canvas, output, 6)


def barragan_cover(data: dict, assets: Path, output: Path) -> None:
    canvas = Image.new("RGBA", (W, H), r.rgba(MAGENTA))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 305, H), fill=YELLOW)
    draw.polygon([(305, 0), (760, 0), (645, 840), (305, 720)], fill="#a20d46")
    draw.polygon([(645, 840), (W, 620), (W, H), (520, H)], fill=PLUM)
    draw.polygon([(305, 0), (420, 0), (720, H), (600, H)], fill=r.rgba(CREAM, 38))
    draw.rectangle((0, 1125, W, 1142), fill=CREAM)

    draw.text((1145, 78), data["author"], font=r.fnt(27, bold=True), fill=CREAM, anchor="ra")
    draw.text((1145, 130), "WALL / LIGHT / COLOUR", font=r.fnt(22, bold=True), fill=r.rgba(CREAM, 180), anchor="ra")
    paste_book(canvas, assets / data["book_cover"], (62, 260), (390, 650), 9)
    r.draw_fitted(draw, (515, 250), data["question"], 645, 520, 83, CREAM, serif=True, spacing=16)
    draw.multiline_text(
        (515, 850),
        "《Barragán: Space and Shadow,\nWalls and Colour》",
        font=r.fnt(26, serif=True),
        fill=CREAM,
        spacing=7,
    )
    draw.rectangle((72, 1260, 1148, 1515), fill=r.rgba(INK, 225))
    draw.rectangle((72, 1260, 88, 1515), fill=YELLOW)
    r.draw_fitted(draw, (122, 1310), data["thesis"], 965, 150, 36, CREAM, serif=True, spacing=14)
    draw.text((1164, 1588), "01 / 06", font=r.fnt(21), fill=r.rgba(CREAM, 180), anchor="ra")
    save(canvas, output, 1)


def barragan_summary(data: dict, assets: Path, output: Path) -> None:
    photo = r.cover_crop(Image.open(assets / "02-gilardi.jpg").convert("RGB"), (430, H), (0.36, 0.5))
    photo = ImageEnhance.Color(photo).enhance(1.12)
    canvas = Image.new("RGBA", (W, H), r.rgba(CREAM))
    canvas.alpha_composite(photo.convert("RGBA"), (812, 0))
    canvas.alpha_composite(Image.new("RGBA", (430, H), (40, 8, 26, 58)), (812, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((798, 0, 812, H), fill=MAGENTA)
    draw.text((70, 72), "FOUR SPATIAL OPERATIONS", font=r.fnt(24, bold=True), fill=MAGENTA)
    draw.text((70, 124), f"《{data['book']}》", font=r.fnt(28, serif=True), fill=PLUM)
    r.draw_fitted(draw, (70, 220), data["summary"]["statement"], 650, 430, 57, INK, serif=True, spacing=19)

    concepts = ["墙", "阴影", "色彩", "尺度"]
    colors = [PLUM, "#6c5f72", MAGENTA, YELLOW]
    x0, y0 = 72, 735
    for i, (label, color) in enumerate(zip(concepts, colors)):
        x = x0 + i * 180
        draw.line((x + 62, y0 + 58, x + 180, y0 + 58), fill=r.rgba(INK, 70), width=3)
        draw.ellipse((x, y0, x + 116, y0 + 116), fill=color)
        draw.text((x + 58, y0 + 58), label, font=r.fnt(26, bold=True), fill=CREAM if i < 3 else INK, anchor="mm")
        if i < 3:
            draw.polygon([(x + 168, y0 + 49), (x + 184, y0 + 58), (x + 168, y0 + 67)], fill=INK)

    y = 950
    blocks = [(MAGENTA, 0), (YELLOW, 34), (PLUM, 0)]
    for i, (item, (color, shift)) in enumerate(zip(data["summary"]["takeaways"][:3], blocks), 1):
        x = 70 + shift
        draw.rectangle((x, y, 742, y + 138), fill=color)
        draw.text((x + 26, y + 25), f"0{i}", font=r.fnt(23, bold=True), fill=CREAM if color != YELLOW else INK)
        r.draw_fitted(draw, (x + 88, y + 21), item, 565 - shift, 98, 27, CREAM if color != YELLOW else INK, serif=True, spacing=8)
        y += 164

    draw.text((850, 118), "空间不是气氛，\n而是一组操作。", font=r.fnt(44, serif=True), fill=CREAM, spacing=15)
    draw.text((70, 1534), "编辑性概括｜非书中原句", font=r.fnt(22), fill=r.rgba(INK, 145))
    draw.text((1164, 1588), "06 / 06", font=r.fnt(21), fill=r.rgba(CREAM, 190), anchor="ra")
    save(canvas, output, 6)


def preview(output: Path) -> None:
    paths = [output / f"{i:02d}.jpg" for i in range(1, 7)]
    r.make_preview(paths, output)


def main() -> None:
    bawa, bawa_assets, bawa_output = cfg("geoffrey-bawa-drawing-archives")
    barragan, barragan_assets, barragan_output = cfg("luis-barragan-space-shadow")
    bawa_cover(bawa, bawa_assets, bawa_output)
    bawa_summary(bawa, bawa_assets, bawa_output)
    barragan_cover(barragan, barragan_assets, barragan_output)
    barragan_summary(barragan, barragan_assets, barragan_output)
    preview(bawa_output)
    preview(barragan_output)
    print("Rebuilt 01, 06 and previews for both theory-book sets.")


if __name__ == "__main__":
    main()
