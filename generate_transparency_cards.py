from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "colin-rowe-transparency"
OUT = ROOT / "output" / "colin-rowe-transparency"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
BLACK = "#171817"
WHITE = "#faf9f5"
PAPER = "#eeeae1"
GREY = "#858984"
BLUE = "#536f82"
OCHRE = "#bd9758"
OLIVE = "#74785c"
RUST = "#8e5c43"

FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rgba(color, alpha=255):
    value = color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def cover_crop(img, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, round(nw * focal[0] - tw / 2)))
    top = max(0, min(nh - th, round(nh * focal[1] - th / 2)))
    return img.crop((left, top, left + tw, top + th))


def fit_inside(img, box):
    bw, bh = box
    scale = min(bw / img.width, bh / img.height)
    return img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)


def wrap_text(draw, text, fnt, max_width):
    lines, current = [], ""
    no_line_start = "，。；：！？、）》】”’"
    for ch in text:
        test = current + ch
        if current and draw.textbbox((0, 0), test, font=fnt)[2] > max_width:
            if ch in no_line_start:
                current += ch
                lines.append(current)
                current = ""
            else:
                lines.append(current)
                current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return "\n".join(lines)


def layered_field(draw, box, seed=1, alpha=42, dark=False):
    random.seed(seed)
    x1, y1, x2, y2 = box
    colors = [BLUE, OCHRE, OLIVE, RUST]
    for i in range(9):
        x = random.randint(x1, max(x1, x2 - 160))
        y = random.randint(y1, max(y1, y2 - 130))
        ww = random.randint(150, 330)
        hh = random.randint(85, 220)
        draw.rectangle((x, y, min(x2, x + ww), min(y2, y + hh)),
                       fill=rgba(colors[i % len(colors)], alpha))
    line_color = WHITE if dark else BLACK
    for i in range(7):
        x = x1 + i * max(1, (x2 - x1) // 7)
        draw.line((x, y1, x, y2), fill=rgba(line_color, 28), width=2)
    for i in range(6):
        y = y1 + i * max(1, (y2 - y1) // 6)
        draw.line((x1, y, x2, y), fill=rgba(line_color, 28), width=2)


def page_mark(draw, number, light=False):
    draw.text((1168, 1585), f"0{number} / 06", font=font(FONT_SANS, 22),
              fill=WHITE if light else BLACK, anchor="ra")


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def authentic_cover():
    # Verified against Douban subject 2381804 (2008 Chinese edition).
    return Image.open(SRC / "book-cover-cn.jpg").convert("RGB")


def mount_book(canvas, position=(66, 1028), box=(345, 470)):
    cover = fit_inside(authentic_cover(), box)
    pad = 11
    mount = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), WHITE)
    mount.alpha_composite(cover.convert("RGBA"), (pad, pad))
    alpha = Image.new("L", mount.size, 0)
    ImageDraw.Draw(alpha).rounded_rectangle((6, 6, mount.width - 3, mount.height - 3), 5, fill=138)
    alpha = alpha.filter(ImageFilter.GaussianBlur(18))
    shadow = Image.new("RGBA", mount.size, (0, 0, 0, 0))
    shadow.putalpha(alpha)
    x, y = position
    canvas.alpha_composite(shadow, (x + 20, y + 24))
    canvas.alpha_composite(mount, (x, y))


def make_cover():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.5, 0.5))
    base = ImageEnhance.Contrast(base).enhance(1.04)
    canvas = base.convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 27, H), fill=BLACK)
    draw.rectangle((62, 58, 443, 112), fill=rgba(WHITE, 240))
    draw.text((82, 72), "BOOK × PERCEPTION / 06", font=font(FONT_BOLD, 23), fill=BLACK)

    draw.rounded_rectangle((54, 146, 795, 732), radius=8, fill=rgba(WHITE, 233))
    draw.text((82, 190), "柯林·罗 × 罗伯特·斯拉茨基", font=font(FONT_BOLD, 35), fill=BLACK)
    draw.text((78, 286), "透明性", font=font(FONT_SERIF, 139), fill=BLACK)
    draw.text((84, 462), "TRANSPARENCY", font=font(FONT_SANS, 43), fill=BLUE)
    draw.rectangle((82, 531, 703, 542), fill=OCHRE)
    draw.text((82, 588), "透明，不只是看得见", font=font(FONT_SERIF, 40), fill=BLACK)
    draw.text((82, 655), "LITERAL / PHENOMENAL", font=font(FONT_BOLD, 26), fill=GREY)
    layered_field(draw, (575, 518, 782, 718), 11, 45)

    mount_book(canvas, (64, 1052), (335, 462))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((470, 1038, 1175, 1508), radius=9, fill=rgba(WHITE, 238))
    draw.text((514, 1080), "SEE-THROUGH ≠ TRANSPARENCY", font=font(FONT_BOLD, 26), fill=BLUE)
    copy = "玻璃让视线穿过材料；\n现象的透明，则让多层空间\n同时进入我们的理解。"
    draw.multiline_text((514, 1162), copy, font=font(FONT_SERIF, 42), fill=BLACK, spacing=20)
    draw.text((514, 1425), "编辑性概括｜非书中原句", font=font(FONT_SANS, 23), fill=GREY)
    page_mark(draw, 1)

    path = save(canvas, "01.jpg")
    save(canvas, "book-cover-composite.jpg")
    return path


def make_case(number, source, title, meta, concept, headline, caption,
              focal=(0.5, 0.5), accent=BLUE, dark=False, art=False):
    source_img = Image.open(SRC / source).convert("RGB")
    photo_h = 1040
    if art:
        bg = Image.new("RGB", (W, photo_h), PAPER)
        fitted = fit_inside(source_img, (W - 120, photo_h - 100))
        bg.paste(fitted, ((W - fitted.width) // 2, (photo_h - fitted.height) // 2))
        image = bg
    else:
        image = cover_crop(source_img, (W, photo_h), focal)
    image = ImageEnhance.Contrast(image).enhance(1.06)
    image = ImageEnhance.Color(image).enhance(0.88)

    panel = BLACK if dark else PAPER
    text_color = WHITE if dark else BLACK
    canvas = Image.new("RGBA", (W, H), panel)
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 174), (0, 0, 0, 72)), (0, 0))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 27, H), fill=accent)
    draw.rectangle((64, 58, 246, 112), fill=accent)
    draw.text((82, 72), f"CASE 0{number - 1}", font=font(FONT_BOLD, 23), fill=WHITE)
    draw.text((1168, 71), meta, font=font(FONT_SANS, 24), fill=WHITE, anchor="ra")
    draw.rectangle((66, 916, 535, 984), fill=rgba(BLACK, 222))
    draw.text((88, 935), concept, font=font(FONT_BOLD, 24), fill=accent)

    draw.rectangle((0, photo_h, W, H), fill=panel)
    layered_field(draw, (700, 1050, 1215, 1584), number * 19, 28, dark)
    draw.rectangle((70, 1084, 82, 1519), fill=accent)
    draw.text((116, 1080), title, font=font(FONT_BOLD, 32), fill=text_color)
    body_font = font(FONT_SERIF, 43)
    draw.multiline_text((116, 1160), wrap_text(draw, headline, body_font, 970),
                        font=body_font, fill=text_color, spacing=17)
    cap_font = font(FONT_SANS, 24)
    draw.multiline_text((116, 1487), wrap_text(draw, caption, cap_font, 930),
                        font=cap_font, fill=rgba(WHITE, 160) if dark else GREY, spacing=8)
    page_mark(draw, number, light=dark)
    return save(canvas, f"{number:02d}.jpg")


def make_book_note():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.5, 0.52))
    base = ImageEnhance.Color(base).enhance(0.22)
    base = ImageEnhance.Brightness(base).enhance(0.34)
    base = base.filter(ImageFilter.GaussianBlur(1.4))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(BLACK, 191)))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 27, H), fill=OCHRE)
    draw.rectangle((70, 66, 1172, 1592), outline=rgba(WHITE, 140), width=2)
    draw.text((112, 112), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 27), fill=WHITE)
    draw.text((112, 200), "透明性", font=font(FONT_SERIF, 82), fill=WHITE)
    draw.text((412, 229), "TRANSPARENCY", font=font(FONT_SANS, 31), fill=OCHRE)
    draw.rectangle((112, 344, 1126, 357), fill=BLUE)

    statement = (
        "《透明性》把“透明”从玻璃的物理属性，推进为一种空间组织方法："
        "当多层位置、边界与关系能被同时感知，建筑即使不透明，也可以产生现象的透明性。"
    )
    body_font = font(FONT_SERIF, 48)
    draw.multiline_text((112, 438), wrap_text(draw, statement, body_font, 990),
                        font=body_font, fill=WHITE, spacing=30)

    draw.rounded_rectangle((112, 1140, 1127, 1420), radius=9, fill=rgba(WHITE, 239))
    draw.text((154, 1183), "SEEING THROUGH / READING THROUGH", font=font(FONT_BOLD, 26), fill=BLUE)
    detail = "一种透明让眼睛穿过材料；另一种透明让理解穿过层次。前者是物质事实，后者是组织关系。"
    detail_font = font(FONT_SERIF, 35)
    draw.multiline_text((154, 1250), wrap_text(draw, detail, detail_font, 900),
                        font=detail_font, fill=BLACK, spacing=15)
    draw.text((112, 1503), "编辑性概括｜非书中原句", font=font(FONT_SANS, 24), fill=rgba(WHITE, 190))
    page_mark(draw, 6, light=True)
    return save(canvas, "06.jpg")


def make_preview(paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), "#aaa9a4")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(image, (x, y))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def main():
    paths = [make_cover()]
    paths.append(make_case(
        2, "bauhaus-dessau.jpg", "包豪斯德绍校舍", "格罗皮乌斯｜1926",
        "LITERAL TRANSPARENCY",
        "整面玻璃让构造与内部活动直接进入视线：这里的透明首先是材料属性——光线与目光真的穿过表面。",
        "字面的透明性：空间可见，但前后关系相对明确。",
        (0.48, 0.48), BLUE, False, False,
    ))
    paths.append(make_case(
        3, "villa-stein-model.jpg", "加歇别墅", "勒·柯布西耶｜1927",
        "PHENOMENAL TRANSPARENCY",
        "墙面并不真正通透，却通过前后平面、开口与边界的重叠，让多个空间位置同时被感知。",
        "现象的透明性：不是穿透材料，而是读出层次。",
        (0.50, 0.48), OCHRE, True, False,
    ))
    paths.append(make_case(
        4, "delaunay-windows.jpg", "《城市上同时打开的窗》", "罗伯特·德劳内｜1912",
        "REFLECTION / REFRACTION",
        "德劳内把窗、光与城市化为反射和折射的色面；重叠产生看得见的透明，却仍保留自然主义的深度。",
        "看见重叠，不一定等于读出了空间的组织。",
        (0.5, 0.5), OLIVE, False, True,
    ))
    paths.append(make_case(
        5, "juan-gris-still-life.jpg", "《花卉静物》", "胡安·格里斯｜1912",
        "LAYER / AMBIGUITY",
        "格里斯用不透明色面和斜向网格压缩深度；物体彼此遮挡却不完全消失，观看在多种前后关系间摆动。",
        "复杂的透明，也可能来自不透明平面之间的组织。",
        (0.5, 0.5), RUST, False, True,
    ))
    paths.append(make_book_note())
    make_preview(paths)
    print("\n".join(str(path) for path in paths))


if __name__ == "__main__":
    main()
