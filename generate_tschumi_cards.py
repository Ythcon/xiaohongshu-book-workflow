from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "tschumi"
OUT = ROOT / "output" / "tschumi-red-is-not-a-color"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
RED = "#e51b23"
DEEP_RED = "#a90f17"
BLACK = "#101010"
WHITE = "#f4f2ed"
GRAY = "#a7a7a3"

FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rgba(hex_color, alpha=255):
    value = hex_color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def cover_crop(img, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, int(nw * focal[0] - tw / 2)))
    top = max(0, min(nh - th, int(nh * focal[1] - th / 2)))
    return img.crop((left, top, left + tw, top + th))


def technical_grid(draw, box=(0, 0, W, H), step=96, alpha=50, color=WHITE):
    x1, y1, x2, y2 = box
    fill = rgba(color, alpha)
    x = x1
    while x <= x2:
        draw.line((x, y1, x, y2), fill=fill, width=1)
        x += step
    y = y1
    while y <= y2:
        draw.line((x1, y, x2, y), fill=fill, width=1)
        y += step


def motion_vector(draw, start, end, color=RED, width=8):
    draw.line((*start, *end), fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    length = 24
    for delta in (2.55, -2.55):
        p = (x2 + length * math.cos(angle + delta), y2 + length * math.sin(angle + delta))
        draw.line((x2, y2, p[0], p[1]), fill=color, width=width)


def page_mark(draw, number, light=False):
    color = WHITE if light else BLACK
    draw.text((1140, 1570), f"0{number} / 06", font=font(FONT_SANS, 26), fill=color, anchor="ra")


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def make_cover(photos):
    canvas = Image.new("RGBA", (W, H), BLACK)
    bg = cover_crop(photos[1], (W, H), (0.55, 0.50))
    bg = ImageEnhance.Color(bg).enhance(0.60)
    bg = ImageEnhance.Contrast(bg).enhance(1.20)
    canvas.alpha_composite(bg.convert("RGBA"))
    canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 105)))
    draw = ImageDraw.Draw(canvas)
    technical_grid(draw, (0, 0, W, H), 92, 38)
    draw.rectangle((0, 0, 30, H), fill=RED)
    draw.rectangle((70, 62, 520, 112), fill=RED)
    draw.text((88, 71), "BOOK × ARCHITECTURE / 02", font=font(FONT_BOLD, 25), fill=WHITE)

    # Real Chinese edition book cover.
    cover = Image.open(SRC / "book-cover-cn.jpg").convert("RGB")
    target_h = 700
    target_w = int(target_h * cover.width / cover.height)
    cover = cover.resize((target_w, target_h), Image.Resampling.LANCZOS)
    mount = Image.new("RGBA", (target_w + 30, target_h + 30), WHITE)
    mount.alpha_composite(cover.convert("RGBA"), (15, 15))
    mount = mount.rotate(-2.2, resample=Image.Resampling.BICUBIC, expand=True, fillcolor=(0, 0, 0, 0))
    alpha = mount.getchannel("A").filter(ImageFilter.GaussianBlur(18))
    shadow = Image.new("RGBA", mount.size, (0, 0, 0, 120))
    shadow.putalpha(alpha.point(lambda p: int(p * 0.62)))
    canvas.alpha_composite(shadow, (80, 214))
    canvas.alpha_composite(mount, (56, 190))

    draw = ImageDraw.Draw(canvas)
    draw.text((742, 320), "伯纳德·屈米", font=font(FONT_BOLD, 34), fill=WHITE)
    draw.text((742, 405), "红", font=font(FONT_BOLD, 188), fill=RED)
    draw.text((930, 452), "不只是", font=font(FONT_SERIF, 54), fill=WHITE)
    draw.text((742, 620), "一种颜色", font=font(FONT_SERIF, 72), fill=WHITE)
    draw.line((742, 728, 1142, 728), fill=RED, width=8)
    draw.text((742, 770), "空间 × 事件 × 运动", font=font(FONT_SANS, 30), fill=WHITE)
    motion_vector(draw, (754, 868), (1090, 868), RED, 7)

    draw.rectangle((0, 1180, W, H), fill=rgba(BLACK, 235))
    draw.rectangle((76, 1240, 90, 1526), fill=RED)
    summary = "建筑不是一件静止的物体，\n而是一套让事件发生的关系。"
    draw.multiline_text((128, 1230), summary, font=font(FONT_SERIF, 58), fill=WHITE, spacing=18)
    draw.text((128, 1460), "《建筑概念：红不只是一种颜色》", font=font(FONT_SANS, 29), fill=rgba(WHITE, 185))
    page_mark(draw, 1, light=True)
    return save(canvas, "01.jpg")


def make_project_page(number, photo, project, meta, headline, caption, focal=(0.5, 0.5), redwash=False):
    canvas = Image.new("RGBA", (W, H), BLACK)
    photo_h = 1090
    image = cover_crop(photo, (W, photo_h), focal)
    image = ImageEnhance.Contrast(image).enhance(1.10)
    image = ImageEnhance.Color(image).enhance(0.78)
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    if redwash:
        canvas.alpha_composite(Image.new("RGBA", (W, photo_h), rgba(RED, 44)), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 210), (0, 0, 0, 90)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    technical_grid(draw, (0, 0, W, photo_h), 112, 34)
    draw.rectangle((0, 0, 24, H), fill=RED)
    draw.rectangle((66, 64, 214, 109), fill=RED)
    draw.text((84, 71), f"CASE 0{number - 1}", font=font(FONT_BOLD, 24), fill=WHITE)
    draw.text((1160, 74), meta, font=font(FONT_SANS, 24), fill=WHITE, anchor="ra")
    motion_vector(draw, (78, 1010), (420, 1010), RED, 7)

    draw.rectangle((0, photo_h, W, H), fill=BLACK)
    technical_grid(draw, (0, photo_h, W, H), 112, 28)
    draw.rectangle((72, 1145, 86, 1520), fill=RED)
    draw.text((124, 1142), project, font=font(FONT_BOLD, 32), fill=RED)
    draw.multiline_text((124, 1216), headline, font=font(FONT_SERIF, 55), fill=WHITE, spacing=14)
    draw.text((124, 1468), caption, font=font(FONT_SANS, 27), fill=rgba(WHITE, 165))
    page_mark(draw, number, light=True)
    return save(canvas, f"{number:02d}.jpg")


def make_book_note(photo):
    canvas = Image.new("RGBA", (W, H), BLACK)
    bg = cover_crop(photo, (W, H), (0.53, 0.50)).filter(ImageFilter.GaussianBlur(2.6))
    bg = ImageEnhance.Color(bg).enhance(0.20)
    bg = ImageEnhance.Brightness(bg).enhance(0.34)
    canvas.alpha_composite(bg.convert("RGBA"))
    canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 140)))
    draw = ImageDraw.Draw(canvas)
    technical_grid(draw, (0, 0, W, H), 100, 42)
    draw.rectangle((0, 0, 30, H), fill=RED)
    draw.rectangle((68, 70, 1174, 1590), outline=rgba(WHITE, 125), width=2)
    draw.text((112, 112), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 27), fill=WHITE)
    draw.text((112, 205), "红不只是一种颜色", font=font(FONT_SERIF, 64), fill=RED)
    draw.line((112, 302, 1120, 302), fill=rgba(WHITE, 90), width=2)

    summary = "建筑之所以区别于普通建筑物，\n不在于它更好看，\n而在于空间、程序、运动与事件，\n被一个清晰的概念组织起来。"
    draw.multiline_text((112, 430), summary, font=font(FONT_SERIF, 63), fill=WHITE, spacing=30)

    draw.rectangle((112, 1130, 1120, 1410), fill=RED)
    draw.text((158, 1170), "这里的“红”是什么？", font=font(FONT_BOLD, 30), fill=WHITE)
    answer = "不是装饰，而是向量、规则与事件的触发器。"
    draw.multiline_text((158, 1240), answer, font=font(FONT_SERIF, 41), fill=WHITE, spacing=14)
    draw.text((112, 1492), "编辑性概括｜非书中原句", font=font(FONT_SANS, 25), fill=rgba(WHITE, 160))
    page_mark(draw, 6, light=True)
    return save(canvas, "06.jpg")


def make_preview(paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), "#d8d5cf")
    for i, path in enumerate(paths):
        im = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(im, (x, y))
    sheet.save(OUT / "preview.jpg", quality=93, subsampling=0)


def main():
    photos = [
        Image.open(SRC / "01-villette-r4.jpg").convert("RGB"),
        Image.open(SRC / "02-villette-n8.jpg").convert("RGB"),
        Image.open(SRC / "03-le-fresnoy.jpg").convert("RGB"),
        Image.open(SRC / "04-acropolis-museum.jpg").convert("RGB"),
    ]
    outputs = [make_cover(photos)]
    outputs.append(make_project_page(
        2, photos[0], "拉·维莱特公园｜Folie R4", "PARIS · 1982—1998",
        "红色不是装饰，\n而是一套让事件发生的坐标。",
        "颜色成为概念的载体：标记点位，也触发行动。", (0.50, 0.48), True))
    outputs.append(make_project_page(
        3, photos[1], "拉·维莱特公园｜Folie N8", "PARIS · 1982—1998",
        "点、线、面同时存在，\n公园是一套可被使用的规则。",
        "建筑不规定唯一剧情，而是容纳不断变化的事件。", (0.55, 0.50), False))
    outputs.append(make_project_page(
        4, photos[2], "Le Fresnoy 当代艺术中心", "TOURCOING · 1997",
        "新屋顶覆盖旧建筑，\n两个时代之间的缝隙\n变成新的公共空间。",
        "并置并不抹去差异，它让差异产生新的程序。", (0.50, 0.49), False))
    outputs.append(make_project_page(
        5, photos[3], "雅典卫城博物馆", "ATHENS · 2009",
        "概念不是形状，\n而是场地、路径与内容\n交汇时形成的秩序。",
        "建筑把遗址、展品、城市与卫城重新组织为一段体验。", (0.50, 0.54), False))
    outputs.append(make_book_note(photos[1]))
    make_preview(outputs)
    print("\n".join(str(p) for p in outputs))


if __name__ == "__main__":
    main()
