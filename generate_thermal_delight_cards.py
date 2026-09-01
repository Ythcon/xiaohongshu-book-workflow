from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "thermal-delight"
OUT = ROOT / "output" / "thermal-delight-architecture"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
BLACK = "#0d0e0f"
PAPER = "#f2eee4"
WHITE = "#faf7ef"
COLD = "#567d9b"
COLD_DARK = "#173143"
EMBER = "#d66328"
GOLD = "#e7ad55"
GREEN = "#596d59"
GREY = "#9a9a91"

FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def rgba(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def cover_crop(image, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / image.width, th / image.height)
    nw, nh = round(image.width * scale), round(image.height * scale)
    image = image.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, round((nw - tw) * focal[0])))
    top = max(0, min(nh - th, round((nh - th) * focal[1])))
    return image.crop((left, top, left + tw, top + th))


def fit_inside(image, box):
    bw, bh = box
    scale = min(bw / image.width, bh / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


def wrap(draw, text, font, max_width):
    lines, current = [], ""
    for ch in text:
        trial = current + ch
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return "\n".join(lines)


def save(image, name):
    path = OUT / name
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def base_image():
    return Image.open(SRC / "ai-cover-base.png").convert("RGB")


def authentic_cover():
    # Publisher-supplied cover image. It is never sent through AI or restyled.
    cover = Image.open(SRC / "book-cover.jpg").convert("RGB")
    # Resolution enhancement only: proportional Lanczos resize plus very light sharpening.
    return cover.resize((cover.width * 3, cover.height * 3), Image.Resampling.LANCZOS).filter(
        ImageFilter.UnsharpMask(radius=0.8, percent=65, threshold=3)
    )


def mount_authentic_cover(canvas, position=(418, 1050), box=(345, 505)):
    cover = fit_inside(authentic_cover(), box)
    pad = 12
    mount = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), rgba(BLACK, 255))
    mount.alpha_composite(cover.convert("RGBA"), (pad, pad))
    alpha = Image.new("L", mount.size, 0)
    ImageDraw.Draw(alpha).rounded_rectangle((8, 8, mount.width - 3, mount.height - 3), 5, fill=160)
    alpha = alpha.filter(ImageFilter.GaussianBlur(22))
    shadow = Image.new("RGBA", mount.size, (0, 0, 0, 0))
    shadow.putalpha(alpha)
    x, y = position
    canvas.alpha_composite(shadow, (x + 20, y + 26))
    canvas.alpha_composite(mount, (x, y))


def page_mark(draw, number, light=True):
    ink = rgba(WHITE if light else BLACK, 205)
    draw.text((1110, 1578), f"0{number} / 06", font=fnt(FONT_SANS, 25), fill=ink, anchor="ra")


def make_cover():
    base = cover_crop(base_image(), (W, H), (0.5, 0.5))
    canvas = ImageEnhance.Contrast(base).enhance(1.04).convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 26, H), fill=GOLD)
    draw.rounded_rectangle((58, 58, 760, 617), radius=10, fill=rgba(BLACK, 222))
    draw.text((86, 86), "ARCHITECTURE × SENSES / 01", font=fnt(FONT_BOLD, 23), fill=GOLD)
    draw.text((84, 156), "莉萨·赫施翁", font=fnt(FONT_BOLD, 37), fill=WHITE)
    draw.text((80, 238), "建筑中的", font=fnt(FONT_SERIF, 74), fill=WHITE)
    draw.text((78, 334), "热愉悦", font=fnt(FONT_SERIF, 145), fill=GOLD)
    draw.rectangle((84, 506, 675, 518), fill=EMBER)
    draw.text((84, 550), "空调让建筑失去“温度”了吗？", font=fnt(FONT_SERIF, 34), fill=WHITE)

    # The verified cover is composited as an untouched, locked layer.
    mount_authentic_cover(canvas)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((68, 1496, 1172, 1570), radius=6, fill=rgba(BLACK, 214))
    draw.text((94, 1515), "HEARTH · SAUNA · BATH · GARDEN", font=fnt(FONT_BOLD, 24), fill=rgba(WHITE, 220))
    page_mark(draw, 1)
    path = save(canvas, "01.jpg")
    save(canvas, "book-cover-composite.jpg")
    return path


def image_page(number, focal, label, title, body, accent, overlay=120):
    bg = cover_crop(base_image(), (W, 1050), focal)
    bg = ImageEnhance.Contrast(bg).enhance(1.08)
    canvas = Image.new("RGBA", (W, H), rgba(BLACK, 255))
    canvas.alpha_composite(bg.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 1050), (4, 6, 8, overlay)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=accent)
    draw.rounded_rectangle((62, 58, 570, 114), radius=5, fill=rgba(BLACK, 205))
    draw.text((84, 73), label, font=fnt(FONT_BOLD, 23), fill=WHITE)
    draw.rectangle((0, 1050, W, H), fill=BLACK)
    draw.rectangle((70, 1090, 190, 1103), fill=accent)
    title_font = fnt(FONT_SERIF, 64)
    draw.multiline_text((72, 1140), wrap(draw, title, title_font, 1040), font=title_font, fill=WHITE, spacing=15)
    body_font = fnt(FONT_SANS, 30)
    draw.multiline_text((74, 1355), wrap(draw, body, body_font, 1040), font=body_font, fill=rgba(WHITE, 205), spacing=13)
    page_mark(draw, number)
    return save(canvas, f"{number:02d}.jpg")


def make_concept():
    canvas = Image.new("RGBA", (W, H), rgba(PAPER, 255))
    draw = ImageDraw.Draw(canvas)
    for x in range(W):
        t = x / (W - 1)
        c1 = rgba(COLD_DARK)
        c2 = rgba(EMBER)
        color = tuple(round(c1[i] * (1 - t) + c2[i] * t) for i in range(3)) + (255,)
        draw.line((x, 0, x, 890), fill=color)
    draw.rectangle((0, 0, 24, H), fill=GOLD)
    draw.text((72, 72), "01 / THERMAL THESIS", font=fnt(FONT_BOLD, 24), fill=WHITE)
    draw.text((70, 172), "舒适，", font=fnt(FONT_SERIF, 126), fill=WHITE)
    draw.text((70, 325), "不是恒温", font=fnt(FONT_SERIF, 145), fill=GOLD)
    draw.text((74, 545), "冷与热不是需要被消灭的误差，\n而是身体理解空间的语言。", font=fnt(FONT_SERIF, 41), fill=WHITE, spacing=18)

    draw.rectangle((0, 890, W, H), fill=PAPER)
    items = [
        ("NECESSITY", "生理需要", "温度首先保护身体"),
        ("DELIGHT", "感官愉悦", "变化让身体重新清醒"),
        ("AFFECTION", "共同记忆", "火炉与浴场组织关系"),
        ("SACREDNESS", "仪式意义", "冷热进入文化与精神生活"),
    ]
    for i, (en, cn, desc) in enumerate(items):
        y = 965 + i * 145
        draw.ellipse((72, y, 118, y + 46), fill=COLD if i < 2 else EMBER)
        draw.text((145, y - 3), en, font=fnt(FONT_BOLD, 23), fill=BLACK)
        draw.text((355, y - 7), cn, font=fnt(FONT_SERIF, 32), fill=BLACK)
        draw.text((625, y), desc, font=fnt(FONT_SANS, 25), fill=rgba(BLACK, 180))
    page_mark(draw, 2, light=False)
    return save(canvas, "02.jpg")


def make_summary():
    base = cover_crop(base_image(), (W, H), (0.48, 0.56)).filter(ImageFilter.GaussianBlur(4))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(BLACK, 175)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=GOLD)
    draw.text((78, 76), "THERMAL DELIGHT / EDITORIAL SUMMARY", font=fnt(FONT_BOLD, 23), fill=GOLD)
    draw.rounded_rectangle((62, 218, 1180, 1312), radius=12, fill=rgba(BLACK, 205), outline=rgba(GOLD, 150), width=2)
    quote = "建筑不该把温度抹平，\n而应让冷热、光、水、材料与身体，\n重新建立关系。"
    draw.multiline_text((105, 350), quote, font=fnt(FONT_SERIF, 65), fill=WHITE, spacing=35)
    draw.rectangle((106, 848, 918, 862), fill=EMBER)
    draw.text((105, 928), "基于全书内容的编辑性概括，非作者原话", font=fnt(FONT_SANS, 27), fill=rgba(WHITE, 185))
    draw.text((105, 1045), "温度不是设备后台里的数字。\n它是建筑最古老、也最容易被遗忘的材料。", font=fnt(FONT_SERIF, 38), fill=GOLD, spacing=18)
    page_mark(draw, 6)
    return save(canvas, "06.jpg")


def make_preview(paths):
    thumb_w, thumb_h = 310, 414
    preview = Image.new("RGB", (thumb_w * 3 + 72, thumb_h * 2 + 72), "#d9d4ca")
    for i, path in enumerate(paths):
        img = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = 18 + (i % 3) * (thumb_w + 18)
        y = 18 + (i // 3) * (thumb_h + 18)
        preview.paste(img, (x, y))
    preview.save(OUT / "preview.jpg", quality=93, optimize=True)


def main():
    paths = [
        make_cover(),
        make_concept(),
        image_page(3, (0.58, 0.66), "02 / HEARTH", "火炉不只是供暖设备", "它把温暖集中成一个可以靠近的中心。身体、交谈与仪式，因此围绕同一团火重新组织。", EMBER, 105),
        image_page(4, (0.83, 0.08), "03 / SAUNA & BATH", "冷热交替，让身体重新醒来", "桑拿与浴场通过蒸汽、热石、冷水和停留时间，把温度变成一段有节奏的空间序列。", GOLD, 90),
        image_page(5, (0.90, 0.66), "04 / GARDEN", "凉意，也可以被设计", "水面、阴影、风与植物共同降低身体感受到的热。庭院不是装饰，而是一台缓慢工作的气候装置。", GREEN, 90),
        make_summary(),
    ]
    make_preview(paths)
    print(f"Generated {len(paths)} cards in {OUT}")


if __name__ == "__main__":
    main()
