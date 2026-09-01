from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "rem-koolhaas"
OUT = ROOT / "output" / "rem-koolhaas-delirious-new-york"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
YELLOW = "#f1df00"
BLACK = "#141414"
PAPER = "#f2efe7"
WHITE = "#faf8f1"
BLUE = "#8fbac6"
PINK = "#d69a91"
GRAY = "#777b7a"

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


def fit_inside(img, box):
    bw, bh = box
    scale = min(bw / img.width, bh / img.height)
    return img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)


def wrap_text(draw, text, fnt, max_width):
    lines = []
    current = ""
    no_line_start = "，。；：！？、）》】”’"
    for ch in text:
        candidate = current + ch
        if current and draw.textbbox((0, 0), candidate, font=fnt)[2] > max_width:
            if ch in no_line_start:
                current += ch
                lines.append(current)
                current = ""
            else:
                lines.append(current)
                current = ch
        else:
            current = candidate
    if current:
        lines.append(current)
    return "\n".join(lines)


def manhattan_grid(draw, box, color=BLACK, alpha=36, step=64, heavy=5):
    x1, y1, x2, y2 = box
    i = 0
    x = x1
    while x <= x2:
        draw.line((x, y1, x, y2), fill=rgba(color, alpha * 2 if i % heavy == 0 else alpha),
                  width=3 if i % heavy == 0 else 1)
        x += step
        i += 1
    i = 0
    y = y1
    while y <= y2:
        draw.line((x1, y, x2, y), fill=rgba(color, alpha * 2 if i % heavy == 0 else alpha),
                  width=3 if i % heavy == 0 else 1)
        y += step
        i += 1


def program_stack(draw, box, colors=(YELLOW, BLUE, PINK)):
    x1, y1, x2, y2 = box
    h = max(12, (y2 - y1) // 9)
    y = y1
    i = 0
    while y < y2:
        fill = colors[i % len(colors)] if i % 3 == 0 else PAPER
        draw.rectangle((x1, y, x2, min(y + h, y2)), fill=fill, outline=BLACK, width=2)
        y += h
        i += 1


def page_mark(draw, number, light=False):
    color = WHITE if light else BLACK
    draw.text((1155, 1576), f"0{number} / 06", font=font(FONT_SANS, 24),
              fill=color, anchor="ra")


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def authentic_book_cover():
    cover = Image.open(SRC / "book-cover-cn.jpg").convert("RGB")
    # The source is a product image with grey margins; crop to the actual cover.
    w, h = cover.size
    return cover.crop((int(w * 0.22), int(h * 0.04), int(w * 0.78), int(h * 0.96)))


def real_book_mount(canvas, position=(62, 910), box=(350, 540)):
    cover = fit_inside(authentic_book_cover(), box)
    pad = 16
    mount = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), WHITE)
    mount.alpha_composite(cover.convert("RGBA"), (pad, pad))
    shadow_alpha = Image.new("L", mount.size, 0)
    ImageDraw.Draw(shadow_alpha).rectangle((8, 8, mount.width - 8, mount.height - 8), fill=145)
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(18))
    shadow = Image.new("RGBA", mount.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha)
    x, y = position
    canvas.alpha_composite(shadow, (x + 18, y + 20))
    canvas.alpha_composite(mount, (x, y))


def make_cover():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.50, 0.48))
    base = ImageEnhance.Contrast(base).enhance(1.06)
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (10, 10, 8, 35)))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 30, H), fill=YELLOW)
    draw.rectangle((62, 62, 480, 112), fill=YELLOW)
    draw.text((84, 72), "BOOK × ARCHITECTURE / 04", font=font(FONT_BOLD, 23), fill=BLACK)
    draw.rounded_rectangle((54, 146, 785, 710), radius=12, fill=rgba(BLACK, 215))
    draw.text((80, 188), "雷姆·库哈斯", font=font(FONT_BOLD, 39), fill=WHITE)
    draw.text((76, 282), "癫狂", font=font(FONT_SERIF, 158), fill=WHITE)
    draw.text((442, 282), "的", font=font(FONT_SERIF, 88), fill=YELLOW)
    draw.text((76, 450), "纽约", font=font(FONT_SERIF, 158), fill=WHITE)
    draw.rectangle((78, 625, 722, 639), fill=YELLOW)
    draw.text((80, 662), "给曼哈顿补写的宣言", font=font(FONT_SANS, 31), fill=WHITE)

    real_book_mount(canvas, (64, 942), (330, 510))

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((520, 1015, 1170, 1475), radius=12, fill=rgba(PAPER, 238))
    program_stack(draw, (552, 1048, 610, 1436))
    draw.text((650, 1052), "CULTURE OF", font=font(FONT_BOLD, 26), fill=GRAY)
    draw.text((650, 1090), "CONGESTION", font=font(FONT_BOLD, 42), fill=BLACK)
    summary = "拥挤不是混乱，\n而是把互不相干的生活\n压进同一座城市机器。"
    draw.multiline_text((650, 1180), summary, font=font(FONT_SERIF, 42),
                        fill=BLACK, spacing=16)
    draw.text((650, 1413), "编辑性概括", font=font(FONT_SANS, 23), fill=GRAY)
    page_mark(draw, 1, light=True)

    path = save(canvas, "01.jpg")
    save(canvas, "book-cover-composite.jpg")
    return path


def make_project_page(number, source_name, project, meta, concept, headline, caption,
                      focal=(0.5, 0.5), accent=YELLOW):
    photo = Image.open(SRC / source_name).convert("RGB")
    photo_h = 1050
    image = cover_crop(photo, (W, photo_h), focal)
    image = ImageEnhance.Color(image).enhance(0.82)
    image = ImageEnhance.Contrast(image).enhance(1.10)

    canvas = Image.new("RGBA", (W, H), PAPER)
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 210), (0, 0, 0, 78)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 30, H), fill=accent)
    draw.rectangle((66, 62, 242, 112), fill=accent)
    draw.text((84, 73), f"CASE 0{number - 1}", font=font(FONT_BOLD, 23), fill=BLACK)
    draw.text((1160, 72), meta, font=font(FONT_SANS, 24), fill=WHITE, anchor="ra")
    draw.rectangle((68, 950, 402, 1006), fill=rgba(BLACK, 218))
    draw.text((86, 961), concept, font=font(FONT_BOLD, 24), fill=accent)

    draw.rectangle((0, photo_h, W, H), fill=PAPER)
    manhattan_grid(draw, (0, photo_h, W, H), BLACK, 20, 72)
    draw.rectangle((70, 1094, 82, 1510), fill=accent)
    draw.text((116, 1090), project, font=font(FONT_BOLD, 32), fill=BLACK)
    headline_font = font(FONT_SERIF, 51)
    wrapped = wrap_text(draw, headline, headline_font, 1010)
    draw.multiline_text((116, 1180), wrapped, font=headline_font, fill=BLACK, spacing=16)
    draw.text((116, 1490), caption, font=font(FONT_SANS, 25), fill=GRAY)
    page_mark(draw, number)
    return save(canvas, f"{number:02d}.jpg")


def make_book_note():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.50, 0.54))
    base = ImageEnhance.Color(base).enhance(0.18)
    base = ImageEnhance.Brightness(base).enhance(0.32)
    base = base.filter(ImageFilter.GaussianBlur(2.0))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(BLACK, 185)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 30, H), fill=YELLOW)
    draw.rectangle((70, 66, 1170, 1590), outline=rgba(WHITE, 150), width=2)
    draw.text((112, 112), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 27), fill=WHITE)
    draw.text((112, 202), "癫狂的纽约", font=font(FONT_SERIF, 77), fill=WHITE)
    draw.rectangle((112, 310, 1122, 324), fill=YELLOW)

    statement = (
        "《癫狂的纽约》把曼哈顿读成\n"
        "一台由网格、摩天楼和欲望\n"
        "共同驱动的城市机器：\n"
        "真正的都市性，诞生于互不相干的\n"
        "程序被迫共处时产生的拥挤与冲突。"
    )
    draw.multiline_text((112, 424), statement, font=font(FONT_SERIF, 54),
                        fill=WHITE, spacing=30)

    draw.rounded_rectangle((112, 1180, 1120, 1415), radius=10, fill=rgba(PAPER, 235))
    draw.text((154, 1219), "GRID × LOBOTOMY × SCHISM", font=font(FONT_BOLD, 28), fill=BLACK)
    draw.text((154, 1284), "网格提供秩序，外壳隐藏差异，楼层容纳彼此冲突的世界。",
              font=font(FONT_SERIF, 35), fill=BLACK)
    draw.text((112, 1498), "编辑性概括｜非书中原句", font=font(FONT_SANS, 25),
              fill=rgba(WHITE, 190))
    page_mark(draw, 6, light=True)
    return save(canvas, "06.jpg")


def make_preview(paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), "#c9c8c2")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(image, (x, y))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def main():
    outputs = [make_cover()]
    outputs.append(make_project_page(
        2, "seattle-library.jpg", "西雅图中央图书馆", "西雅图｜2004", "PROGRAM STACK",
        "稳定的平台与流动空间被压进同一外壳，建筑成为一台组织知识与事件的城市机器。",
        "形状不是起点，而是程序叠加之后留下的结果。",
        (0.50, 0.47), YELLOW,
    ))
    outputs.append(make_project_page(
        3, "casa-da-musica.jpg", "Casa da Música", "波尔图｜2005", "LOBOTOMY",
        "外部像一块封闭岩石，内部却把演出、城市与公共路线并置在一起。",
        "内与外不必互相解释；表皮可以隐藏内部的差异与冲突。",
        (0.54, 0.48), BLUE,
    ))
    outputs.append(make_project_page(
        4, "cctv.jpg", "央视总部", "北京｜2012", "LOOP",
        "摩天楼不必只向上竞争；两座塔折叠成闭环，高度变成组织生产关系的三维线路。",
        "它把传统塔楼从垂直孤岛，改写为连续运转的城市回路。",
        (0.50, 0.52), YELLOW,
    ))
    outputs.append(make_project_page(
        5, "de-rotterdam.jpg", "De Rotterdam", "鹿特丹｜2013", "VERTICAL CITY",
        "住宅、酒店、办公与商业被压进一座垂直城市；密度不是结果，而是设计的发动机。",
        "互不相干的生活并置，正是“拥挤文化”的建筑版本。",
        (0.50, 0.48), PINK,
    ))
    outputs.append(make_book_note())
    make_preview(outputs)
    print("\n".join(str(path) for path in outputs))


if __name__ == "__main__":
    main()
