#!/usr/bin/env python3
"""Render a six-card Xiaohongshu architecture-book post from post.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


W, H = 1242, 1660
WHITE = "#f6f2e9"
BLACK = "#101010"
PAPER = "#eee9dd"

THEMES = {
    "signage": {
        "accent": ["#ffd400", "#f04f78", "#2aa7d8", "#b8d72e"],
        "panel": BLACK,
        "text": WHITE,
    },
    "anchoring": {
        "accent": ["#3f7994", "#d8b82e", "#c6342b", "#708b58"],
        "panel": PAPER,
        "text": BLACK,
    },
    "event-grid": {
        "accent": ["#e51b23"] * 4,
        "panel": BLACK,
        "text": WHITE,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    return parser.parse_args()


def rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def font_path(serif: bool = False, bold: bool = False) -> str:
    candidates = []
    if serif:
        candidates += [r"C:\Windows\Fonts\NotoSerifSC-VF.ttf", r"C:\Windows\Fonts\simhei.ttf"]
    elif bold:
        candidates += [r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf", r"C:\Windows\Fonts\msyhbd.ttc"]
    else:
        candidates += [r"C:\Windows\Fonts\NotoSansSC-VF.ttf", r"C:\Windows\Fonts\msyh.ttc"]
    candidates += ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError("No usable CJK font found")


def fnt(size: int, serif: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(font_path(serif, bold), size)


def cover_crop(image: Image.Image, size: tuple[int, int], focal=(0.5, 0.5)) -> Image.Image:
    tw, th = size
    scale = max(tw / image.width, th / image.height)
    nw, nh = round(image.width * scale), round(image.height * scale)
    image = image.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, round((nw - tw) * float(focal[0]))))
    top = max(0, min(nh - th, round((nh - th) * float(focal[1]))))
    return image.crop((left, top, left + tw, top + th))


def fit_inside(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = min(size[0] / image.width, size[1] / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


def wrap(draw: ImageDraw.ImageDraw, text: str, used_font: ImageFont.FreeTypeFont, width: int) -> str:
    paragraphs = []
    for raw in str(text).splitlines() or [""]:
        lines, current = [], ""
        for char in raw:
            trial = current + char
            if current and draw.textbbox((0, 0), trial, font=used_font)[2] > width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
        paragraphs.append("\n".join(lines))
    return "\n".join(paragraphs)


def draw_fitted(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    width: int,
    height: int,
    start_size: int,
    fill: str | tuple,
    serif: bool = False,
    bold: bool = False,
    spacing: int = 12,
) -> int:
    for size in range(start_size, 21, -2):
        used = fnt(size, serif, bold)
        wrapped = wrap(draw, text, used, width)
        box = draw.multiline_textbbox(xy, wrapped, font=used, spacing=spacing)
        if box[3] - xy[1] <= height:
            draw.multiline_text(xy, wrapped, font=used, fill=fill, spacing=spacing)
            return box[3]
    raise ValueError(f"Text does not fit: {text[:40]}")


def grid(draw: ImageDraw.ImageDraw, box=(0, 0, W, H), step=104, alpha=38) -> None:
    x1, y1, x2, y2 = box
    for x in range(x1, x2 + 1, step):
        draw.line((x, y1, x, y2), fill=rgba(WHITE, alpha), width=1)
    for y in range(y1, y2 + 1, step):
        draw.line((x1, y, x2, y), fill=rgba(WHITE, alpha), width=1)


def contours(draw: ImageDraw.ImageDraw, box=(820, 1090, 1210, 1580), color=BLACK) -> None:
    x1, y1, x2, y2 = box
    for i in range(7):
        inset = i * 28
        draw.arc((x1 + inset, y1 + inset, x2 - inset, y2 - inset), 185, 342, fill=rgba(color, 45), width=2)


def page_mark(draw: ImageDraw.ImageDraw, number: int, total: int, light: bool) -> None:
    draw.text((1160, 1594), f"{number:02d} / {total:02d}", font=fnt(22), fill=rgba(WHITE if light else BLACK, 175), anchor="ra")


def save(canvas: Image.Image, output: Path, number: int) -> Path:
    path = output / f"{number:02d}.jpg"
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def mount_cover(canvas: Image.Image, cover_path: Path, box: tuple[int, int, int, int]) -> None:
    cover = fit_inside(Image.open(cover_path).convert("RGB"), (box[2], box[3]))
    x, y = box[0], box[1]
    shadow = Image.new("RGBA", (cover.width + 42, cover.height + 42), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((16, 16, cover.width + 28, cover.height + 28), 7, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(shadow, (x - 14, y - 10))
    mount = Image.new("RGBA", (cover.width + 16, cover.height + 16), rgba(WHITE))
    mount.alpha_composite(cover.convert("RGBA"), (8, 8))
    canvas.alpha_composite(mount, (x, y))


def load_image(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGB")


def make_cover(cfg: dict, assets: Path, output: Path) -> Path:
    system = cfg["system"]
    theme = THEMES[system]
    bg_name = cfg.get("cover_background") or cfg["cases"][0]["image"]
    bg = cover_crop(load_image(assets / bg_name), (W, H), cfg.get("cover_focal", [0.5, 0.5]))
    bg = ImageEnhance.Contrast(bg).enhance(1.05)
    canvas = bg.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 92)))
    draw = ImageDraw.Draw(canvas)
    accent = theme["accent"][0]

    if system == "signage":
        draw.rectangle((0, 0, 24, H), fill=accent)
        draw.rectangle((0, 0, W, 390), fill=rgba(BLACK, 182))
        draw.rectangle((0, 1010, W, H), fill=rgba(BLACK, 218))
        text_fill, box = WHITE, (66, 154)
        cover_box = (866, 1080, 275, 430)
    elif system == "anchoring":
        draw.rounded_rectangle((54, 55, 810, 620), 8, fill=rgba(WHITE, 238))
        draw.rectangle((0, 0, 24, H), fill=BLACK)
        contours(draw, (730, 500, 1220, 1080), BLACK)
        text_fill, box = BLACK, (82, 145)
        cover_box = (410, 1000, 410, 420)
    else:
        grid(draw, alpha=42)
        draw.rectangle((0, 0, 30, H), fill=accent)
        draw.rectangle((0, 1180, W, H), fill=rgba(BLACK, 236))
        draw.rounded_rectangle((54, 58, 540, 118), 4, fill=accent)
        draw.text((78, 74), "BOOK × URBANISM / 01", font=fnt(23, bold=True), fill=WHITE)
        text_fill, box = WHITE, (720, 300)
        cover_box = (68, 205, 560, 710)

    draw.text((box[0], box[1] - 64), cfg["author"], font=fnt(32, bold=True), fill=accent if system != "anchoring" else BLACK)
    draw_fitted(draw, box, cfg["question"], 490 if system == "event-grid" else 700, 265, 78, text_fill, serif=True, bold=False, spacing=10)
    mount_cover(canvas, assets / cfg["book_cover"], cover_box)

    if system == "event-grid":
        draw.rectangle((72, 1232, 86, 1535), fill=accent)
        draw_fitted(draw, (126, 1230), cfg["thesis"], 990, 220, 51, WHITE, serif=True, spacing=16)
        draw.text((126, 1492), f"《{cfg['book']}》", font=fnt(27), fill=rgba(WHITE, 185))
    elif system == "signage":
        draw.text((68, 1050), f"《{cfg['book']}》", font=fnt(45, serif=True), fill=WHITE)
        draw.rectangle((68, 1120, 700, 1132), fill=theme["accent"][1])
        draw_fitted(draw, (68, 1172), cfg["thesis"], 700, 250, 32, rgba(WHITE, 220), serif=True)
    else:
        draw.rounded_rectangle((74, 1402, 1168, 1542), 7, fill=rgba(BLACK, 222))
        draw_fitted(draw, (106, 1430), cfg["thesis"], 1025, 92, 31, WHITE, serif=True)
    page_mark(draw, 1, cfg["_total_pages"], light=system != "anchoring" or cover_box[1] > 900)
    return save(canvas, output, 1)


def make_case(cfg: dict, case: dict, number: int, assets: Path, output: Path) -> Path:
    system = cfg["system"]
    theme = THEMES[system]
    accent = theme["accent"][(number - 2) % len(theme["accent"])]
    photo_h = 1032 if system != "event-grid" else 1090
    photo = cover_crop(load_image(assets / case["image"]), (W, photo_h), case.get("focal", [0.5, 0.5]))
    photo = ImageEnhance.Contrast(photo).enhance(1.06)
    canvas = Image.new("RGBA", (W, H), theme["panel"])
    canvas.alpha_composite(photo.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 165), (0, 0, 0, 92)), (0, 0))
    draw = ImageDraw.Draw(canvas)

    if system == "event-grid":
        # Keep documentary images clean; the grid organizes only the text field.
        grid(draw, (0, photo_h, W, H), 104, 36)
        draw.rectangle((0, 0, 24, H), fill=accent)
        draw.line((82, photo_h - 76, 420, photo_h - 76), fill=accent, width=7)
        draw.line((420, photo_h - 76, 392, photo_h - 92), fill=accent, width=7)
        draw.line((420, photo_h - 76, 392, photo_h - 60), fill=accent, width=7)
    elif system == "signage":
        draw.rectangle((0, 0, 24, H), fill=accent)
        draw.rectangle((0, photo_h, W, H), fill=BLACK)
        draw.rectangle((68, photo_h + 56, 238, photo_h + 69), fill=accent)
    else:
        draw.rectangle((0, 0, 24, H), fill=accent)
        draw.rectangle((0, photo_h, W, H), fill=theme["panel"])
        draw.rectangle((70, photo_h + 52, 82, 1532), fill=accent)
        contours(draw, color=WHITE if theme["panel"] == BLACK else BLACK)

    draw.rounded_rectangle((64, 56, 580, 116), 5, fill=rgba(BLACK, 220))
    draw.text((86, 72), case.get("eyebrow", f"CASE 0{number - 1}"), font=fnt(24, bold=True), fill=accent)
    draw.text((1165, 72), case.get("meta", ""), font=fnt(23), fill=WHITE, anchor="ra")
    panel_text = theme["text"]
    x = 116 if system == "anchoring" else 68 if system == "signage" else 124
    draw.text((x, photo_h + 92), case.get("name", ""), font=fnt(30, bold=True), fill=accent)
    bottom = draw_fitted(draw, (x, photo_h + 160), case["headline"], 1020, 205, 55, panel_text, serif=True, spacing=12)
    draw_fitted(draw, (x, bottom + 30), case["body"], 1000, H - bottom - 90, 28, rgba(panel_text, 198), spacing=10)
    page_mark(draw, number, cfg["_total_pages"], light=theme["panel"] == BLACK)
    return save(canvas, output, number)


def make_summary(cfg: dict, output: Path) -> Path:
    system = cfg["system"]
    theme = THEMES[system]
    accent = theme["accent"][0]
    canvas = Image.new("RGBA", (W, H), rgba(BLACK if system != "anchoring" else PAPER))
    draw = ImageDraw.Draw(canvas)
    light = system != "anchoring"
    text = WHITE if light else BLACK
    if system == "event-grid":
        grid(draw, alpha=42)
    elif system == "anchoring":
        contours(draw, (650, 90, 1230, 920), BLACK)
    else:
        for color, y in zip(theme["accent"], (0, 18, 36, 54)):
            draw.rectangle((0, y, W, y + 18), fill=color)
    draw.rectangle((0, 0, 24, H), fill=accent)
    draw.text((72, 92), "ONE-SENTENCE BOOK NOTE", font=fnt(25, bold=True), fill=accent)
    draw.text((72, 160), f"《{cfg['book']}》", font=fnt(42, serif=True), fill=text)
    draw.rectangle((72, 245, 1168, 256), fill=accent)
    summary = cfg["summary"]
    draw_fitted(draw, (72, 340), summary["statement"], 1080, 470, 63, text, serif=True, spacing=22)
    concepts = summary.get("concepts", [])[:3]
    x = 74
    for i, label in enumerate(concepts):
        width = min(310, max(150, draw.textbbox((0, 0), label, font=fnt(23, bold=True))[2] + 44))
        color = theme["accent"][i % len(theme["accent"])]
        draw.rounded_rectangle((x, 850, x + width, 908), 7, fill=color)
        draw.text((x + width / 2, 879), label, font=fnt(23, bold=True), fill=BLACK, anchor="mm")
        x += width + 18
    panel_fill = "#1d1d1d" if light else "#dfd9cc"
    draw.rounded_rectangle((72, 990, 1170, 1485), 10, fill=panel_fill, outline=rgba(text, 90), width=2)
    y = 1050
    for i, item in enumerate(summary.get("takeaways", [])[:3], 1):
        color = theme["accent"][(i - 1) % len(theme["accent"])]
        draw.rounded_rectangle((108, y, 164, y + 56), 8, fill=color)
        draw.text((136, y + 28), str(i), font=fnt(25, bold=True), fill=BLACK, anchor="mm")
        draw_fitted(draw, (194, y + 3), item, 900, 90, 30, text, serif=True, spacing=8)
        y += 126
    draw.text((74, 1530), "编辑性概括｜非书中原句", font=fnt(23), fill=rgba(text, 165))
    number = cfg["_total_pages"]
    page_mark(draw, number, number, light=light)
    return save(canvas, output, number)


def make_preview(paths: list[Path], output: Path) -> None:
    tw, th, gap = 310, 414, 18
    rows = (len(paths) + 2) // 3
    sheet = Image.new("RGB", (tw * 3 + gap * 4, th * rows + gap * (rows + 1)), "#d4d0c7")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(image, (gap + (i % 3) * (tw + gap), gap + (i // 3) * (th + gap)))
    sheet.save(output / "preview.jpg", quality=94, subsampling=0)


def main() -> None:
    args = parse_args()
    cfg_path = args.config.resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    if cfg.get("system") not in THEMES:
        raise ValueError("system must be signage, anchoring, or event-grid")
    case_count = len(cfg.get("cases", []))
    kind = cfg.get("kind", "magazine" if case_count == 6 else "book")
    expected = 6 if kind == "magazine" else 4
    if case_count != expected:
        raise ValueError(f"{kind} requires exactly {expected} cases")
    cfg["_total_pages"] = case_count + 2
    assets = (cfg_path.parent / cfg["asset_dir"]).resolve()
    output = (cfg_path.parent / cfg["output_dir"]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    paths = [make_cover(cfg, assets, output)]
    paths.extend(make_case(cfg, case, i, assets, output) for i, case in enumerate(cfg["cases"], 2))
    paths.append(make_summary(cfg, output))
    make_preview(paths, output)
    print(f"Created {len(paths)} cards and preview in {output}")


if __name__ == "__main__":
    main()
