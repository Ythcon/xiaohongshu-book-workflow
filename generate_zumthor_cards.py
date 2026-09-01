from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "peter-zumthor"
OUT = ROOT / "output" / "peter-zumthor-atmospheres"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
UMBER = "#6e4030"
DARK = "#1a1a18"
STONE = "#7b807a"
MIST = "#e9e5dc"
AMBER = "#d39a52"
GREEN = "#607167"
TIMBER = "#8b4436"
WHITE = "#f7f4ec"

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
    lines, current = [], ""
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


def atmospheric_lines(draw, box, color=STONE, alpha=55):
    x1, y1, x2, y2 = box
    for i in range(7):
        y = y1 + 42 + i * 62
        points = []
        for x in range(x1, x2 + 1, 36):
            bend = int(13 * ((x // 36 + i * 2) % 5 - 2))
            points.append((x, y + bend))
        draw.line(points, fill=rgba(color, max(10, alpha - i * 5)), width=2)


def page_mark(draw, number, light=False):
    color = WHITE if light else DARK
    draw.text((1150, 1580), f"0{number} / 06", font=font(FONT_SANS, 23), fill=color, anchor="ra")


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def authentic_cover():
    return Image.open(SRC / "book-cover-cn-v2.jpg").convert("RGB")


def mount_book(canvas, position=(65, 1030), box=(335, 450)):
    cover = fit_inside(authentic_cover(), box)
    pad = 15
    mount = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), WHITE)
    mount.alpha_composite(cover.convert("RGBA"), (pad, pad))
    shadow_alpha = Image.new("L", mount.size, 0)
    ImageDraw.Draw(shadow_alpha).rounded_rectangle(
        (7, 7, mount.width - 7, mount.height - 7), radius=5, fill=150
    )
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(20))
    shadow = Image.new("RGBA", mount.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha)
    x, y = position
    canvas.alpha_composite(shadow, (x + 18, y + 24))
    canvas.alpha_composite(mount, (x, y))


def make_cover():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.50, 0.49))
    base = ImageEnhance.Contrast(base).enhance(1.04)
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (10, 10, 8, 20)))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 27, H), fill=AMBER)
    draw.rectangle((64, 62, 468, 112), fill=rgba(MIST, 235))
    draw.text((84, 72), "BOOK × ARCHITECTURE / 06", font=font(FONT_BOLD, 23), fill=DARK)
    draw.rounded_rectangle((55, 145, 724, 700), radius=9, fill=rgba(DARK, 215))
    draw.text((82, 184), "彼得·卒姆托", font=font(FONT_BOLD, 42), fill=WHITE)
    draw.text((78, 282), "建筑", font=font(FONT_SERIF, 144), fill=WHITE)
    draw.text((400, 292), "氛围", font=font(FONT_SERIF, 88), fill=AMBER)
    draw.line((82, 468, 650, 468), fill=UMBER, width=12)
    draw.text((82, 514), "ATMOSPHERES", font=font(FONT_BOLD, 36), fill=WHITE)
    draw.text((82, 578), "空间，首先是一种感受", font=font(FONT_SANS, 31), fill=rgba(WHITE, 220))
    atmospheric_lines(draw, (78, 620, 655, 690), AMBER, 85)

    mount_book(canvas, (64, 1050), (330, 440))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((498, 1048, 1172, 1482), radius=9, fill=rgba(MIST, 238))
    draw.text((542, 1092), "LIGHT / SOUND / TEMPERATURE", font=font(FONT_BOLD, 27), fill=UMBER)
    draw.text((542, 1162), "氛围不是装饰，", font=font(FONT_SERIF, 43), fill=DARK)
    draw.text((542, 1224), "而是身体在空间中", font=font(FONT_SERIF, 43), fill=DARK)
    draw.text((542, 1286), "收到的全部信号。", font=font(FONT_SERIF, 43), fill=DARK)
    draw.text((542, 1400), "编辑性概括", font=font(FONT_SANS, 23), fill=STONE)
    page_mark(draw, 1, light=True)

    path = save(canvas, "01.jpg")
    save(canvas, "book-cover-composite.jpg")
    return path


def make_project_page(number, source_name, project, meta, concept, headline, caption,
                      focal=(0.5, 0.5), accent=AMBER, dark_panel=False):
    photo = Image.open(SRC / source_name).convert("RGB")
    photo_h = 1045
    image = cover_crop(photo, (W, photo_h), focal)
    image = ImageEnhance.Contrast(image).enhance(1.07)
    image = ImageEnhance.Color(image).enhance(0.82)

    panel = DARK if dark_panel else MIST
    panel_text = WHITE if dark_panel else DARK
    canvas = Image.new("RGBA", (W, H), panel)
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 190), (0, 0, 0, 68)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 27, H), fill=accent)
    draw.rectangle((66, 62, 246, 114), fill=accent)
    draw.text((84, 73), f"CASE 0{number - 1}", font=font(FONT_BOLD, 23), fill=WHITE)
    draw.text((1158, 72), meta, font=font(FONT_SANS, 24), fill=WHITE, anchor="ra")
    draw.rectangle((68, 927, 452, 988), fill=rgba(DARK, 224))
    draw.text((88, 942), concept, font=font(FONT_BOLD, 23), fill=accent)

    draw.rectangle((0, photo_h, W, H), fill=panel)
    atmospheric_lines(draw, (0, photo_h, W, H), accent, 42)
    draw.rectangle((70, 1090, 82, 1515), fill=accent)
    draw.text((116, 1085), project, font=font(FONT_BOLD, 32), fill=panel_text)
    headline_font = font(FONT_SERIF, 48)
    wrapped = wrap_text(draw, headline, headline_font, 980)
    draw.multiline_text((116, 1172), wrapped, font=headline_font, fill=panel_text, spacing=17)
    draw.text((116, 1492), caption, font=font(FONT_SANS, 24),
              fill=rgba(WHITE, 155) if dark_panel else STONE)
    page_mark(draw, number, light=dark_panel)
    return save(canvas, f"{number:02d}.jpg")


def make_book_note():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.50, 0.56))
    base = ImageEnhance.Color(base).enhance(0.15)
    base = ImageEnhance.Brightness(base).enhance(0.34)
    base = base.filter(ImageFilter.GaussianBlur(1.8))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(DARK, 192)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 27, H), fill=AMBER)
    draw.rectangle((70, 66, 1170, 1590), outline=rgba(WHITE, 145), width=2)
    draw.text((112, 110), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 27), fill=WHITE)
    draw.text((112, 198), "建筑氛围", font=font(FONT_SERIF, 76), fill=WHITE)
    draw.rectangle((112, 306, 1122, 320), fill=AMBER)

    statement = (
        "《建筑氛围》把设计从“看起来怎样”转向“置身其中是什么感觉”："
        "光、声音、温度、材料和距离共同决定空间是否真正打动人。"
    )
    statement_font = font(FONT_SERIF, 49)
    statement = wrap_text(draw, statement, statement_font, 980)
    draw.multiline_text((112, 420), statement, font=statement_font, fill=WHITE, spacing=30)

    draw.rounded_rectangle((112, 1115, 1124, 1405), radius=10, fill=rgba(MIST, 238))
    draw.text((154, 1160), "ATMOSPHERE IS FELT BEFORE IT IS NAMED",
              font=font(FONT_BOLD, 26), fill=UMBER)
    detail = "先问空间让人听见什么、触到什么、感到多冷或多暖，再问它应该长成什么样。"
    draw.multiline_text((154, 1230), wrap_text(draw, detail, font(FONT_SERIF, 35), 900),
                        font=font(FONT_SERIF, 35), fill=DARK, spacing=14)
    draw.text((112, 1498), "编辑性概括｜非书中原句", font=font(FONT_SANS, 25), fill=rgba(WHITE, 195))
    page_mark(draw, 6, light=True)
    return save(canvas, "06.jpg")


def make_preview(paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), "#aaa79f")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(image, (x, y))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def main():
    outputs = [make_cover()]
    outputs.append(make_project_page(
        2, "therme-vals.jpg", "瓦尔斯温泉", "瑞士瓦尔斯｜1996", "TEMPERATURE / MATERIAL",
        "氛围从身体开始：石材的重量、水汽的湿度与回声的距离，共同让温泉成为一段被皮肤理解的建筑。",
        "材料不只是被观看，它还改变触觉、声音和时间感。", (0.48, 0.54), GREEN, False,
    ))
    outputs.append(make_project_page(
        3, "bruder-klaus.jpg", "布鲁德·克劳斯礼拜堂", "德国梅谢尼希｜2007", "LIGHT / SOUND",
        "最深的黑暗让一束天光拥有重量；烧灼的墙面、脚步与沉默，把空间变成一次缓慢的内在感知。",
        "光不是照明配置，而是让黑暗产生尺度的材料。", (0.50, 0.50), AMBER, True,
    ))
    outputs.append(make_project_page(
        4, "kolumba.jpg", "科隆巴博物馆", "德国科隆｜2007", "INSIDE / OUTSIDE",
        "砖墙不是封闭表皮，而是一层会呼吸的滤镜：光线、遗址与城市声响在孔隙之间保持若即若离。",
        "室内与城市之间没有断开，只是被调低了音量。", (0.50, 0.50), STONE, False,
    ))
    outputs.append(make_project_page(
        5, "saint-benedict.jpg", "圣本笃礼拜堂", "瑞士苏姆维特｜1989", "SURROUNDINGS",
        "建筑没有站在山谷前展示自己，而是借木瓦、尺度与坡地把自己调到环境原有的音量。",
        "真正的场所感，是建筑与周围世界彼此成全。", (0.52, 0.56), TIMBER, False,
    ))
    outputs.append(make_book_note())
    make_preview(outputs)
    print("\n".join(str(path) for path in outputs))


if __name__ == "__main__":
    main()
