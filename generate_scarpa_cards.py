from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "carlo-scarpa"
OUT = ROOT / "output" / "carlo-scarpa-the-complete-works"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
PARCHMENT = "#e8dfce"
LIGHT = "#f5f0e6"
CHARCOAL = "#20201e"
BRASS = "#b48a46"
TERRACOTTA = "#b64c3c"
CONCRETE = "#77736d"
MOSS = "#465b46"
BLUE = "#315b70"

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


def construction_field(draw, box, color=CHARCOAL, alpha=28):
    x1, y1, x2, y2 = box
    for x in range(x1, x2 + 1, 72):
        draw.line((x, y1, x, y2), fill=rgba(color, alpha), width=1)
    for y in range(y1, y2 + 1, 72):
        draw.line((x1, y, x2, y), fill=rgba(color, alpha), width=1)
    for offset in (0, 32):
        draw.arc((x2 - 250 + offset, y1 + 40 + offset, x2 - 70 - offset, y1 + 220 - offset),
                 198, 520, fill=rgba(BRASS, 90), width=3)
    draw.line((x2 - 205, y1 + 88, x2 - 115, y1 + 178), fill=rgba(BRASS, 110), width=3)
    draw.line((x2 - 115, y1 + 88, x2 - 205, y1 + 178), fill=rgba(BRASS, 110), width=3)


def scarpa_joint(draw, origin, scale=1.0):
    x, y = origin
    s = scale
    draw.rectangle((x, y, x + 94 * s, y + 94 * s), outline=BRASS, width=max(2, int(4 * s)))
    draw.rectangle((x + 26 * s, y + 26 * s, x + 120 * s, y + 120 * s),
                   outline=TERRACOTTA, width=max(2, int(4 * s)))
    draw.ellipse((x + 39 * s, y + 39 * s, x + 81 * s, y + 81 * s),
                 outline=CHARCOAL, width=max(2, int(3 * s)))


def page_mark(draw, number, light=False):
    color = LIGHT if light else CHARCOAL
    draw.text((1150, 1580), f"0{number} / 06", font=font(FONT_SANS, 23), fill=color, anchor="ra")


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def authentic_cover():
    return Image.open(SRC / "book-cover-v5.jpg").convert("RGB")


def mount_book(canvas, position=(72, 1020), box=(350, 430)):
    cover = fit_inside(authentic_cover(), box)
    pad = 14
    mount = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), LIGHT)
    mount.alpha_composite(cover.convert("RGBA"), (pad, pad))
    shadow_alpha = Image.new("L", mount.size, 0)
    ImageDraw.Draw(shadow_alpha).rectangle((8, 8, mount.width - 8, mount.height - 8), fill=150)
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(18))
    shadow = Image.new("RGBA", mount.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha)
    x, y = position
    canvas.alpha_composite(shadow, (x + 20, y + 22))
    canvas.alpha_composite(mount, (x, y))


def make_cover():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.50, 0.50))
    base = ImageEnhance.Contrast(base).enhance(1.05)
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (18, 15, 11, 22)))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 26, H), fill=TERRACOTTA)
    draw.rectangle((66, 62, 480, 112), fill=PARCHMENT)
    draw.text((84, 72), "BOOK × ARCHITECTURE / 05", font=font(FONT_BOLD, 23), fill=CHARCOAL)
    draw.rounded_rectangle((58, 146, 740, 700), radius=8, fill=rgba(CHARCOAL, 220))
    draw.text((82, 184), "卡洛·斯卡帕", font=font(FONT_BOLD, 42), fill=LIGHT)
    draw.text((78, 286), "完整", font=font(FONT_SERIF, 148), fill=LIGHT)
    draw.text((398, 292), "作品", font=font(FONT_SERIF, 88), fill=BRASS)
    draw.line((82, 468, 658, 468), fill=TERRACOTTA, width=12)
    draw.text((82, 510), "THE COMPLETE WORKS", font=font(FONT_BOLD, 34), fill=LIGHT)
    draw.text((82, 572), "建筑，从节点开始发生", font=font(FONT_SANS, 31), fill=rgba(LIGHT, 220))
    scarpa_joint(draw, (600, 555), 0.72)

    mount_book(canvas, (64, 1052), (338, 410))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((500, 1050, 1172, 1480), radius=9, fill=rgba(PARCHMENT, 240))
    draw.text((544, 1094), "JOINT / LAYER / THRESHOLD", font=font(FONT_BOLD, 27), fill=TERRACOTTA)
    draw.text((544, 1160), "一条缝不是空白，", font=font(FONT_SERIF, 43), fill=CHARCOAL)
    draw.text((544, 1222), "而是新旧、材料与时间", font=font(FONT_SERIF, 43), fill=CHARCOAL)
    draw.text((544, 1284), "开始对话的位置。", font=font(FONT_SERIF, 43), fill=CHARCOAL)
    draw.text((544, 1398), "编辑性概括", font=font(FONT_SANS, 23), fill=CONCRETE)
    page_mark(draw, 1, light=True)

    path = save(canvas, "01.jpg")
    save(canvas, "book-cover-composite.jpg")
    return path


def make_project_page(number, source_name, project, meta, concept, headline, caption,
                      focal=(0.5, 0.5), accent=BRASS, grayscale=False):
    photo = Image.open(SRC / source_name).convert("RGB")
    photo_h = 1030
    image = cover_crop(photo, (W, photo_h), focal)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Color(image).enhance(0.22 if grayscale else 0.80)

    canvas = Image.new("RGBA", (W, H), PARCHMENT)
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 180), (0, 0, 0, 70)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 26, H), fill=accent)
    draw.rectangle((66, 62, 246, 114), fill=accent)
    draw.text((84, 73), f"CASE 0{number - 1}", font=font(FONT_BOLD, 23), fill=LIGHT)
    draw.text((1158, 72), meta, font=font(FONT_SANS, 24), fill=LIGHT, anchor="ra")
    draw.rectangle((68, 922, 440, 982), fill=rgba(CHARCOAL, 224))
    draw.text((88, 937), concept, font=font(FONT_BOLD, 23), fill=accent)

    draw.rectangle((0, photo_h, W, H), fill=PARCHMENT)
    construction_field(draw, (0, photo_h, W, H))
    draw.rectangle((70, 1080, 82, 1515), fill=accent)
    draw.text((116, 1080), project, font=font(FONT_BOLD, 32), fill=CHARCOAL)
    headline_font = font(FONT_SERIF, 48)
    wrapped = wrap_text(draw, headline, headline_font, 970)
    draw.multiline_text((116, 1170), wrapped, font=headline_font, fill=CHARCOAL, spacing=17)
    draw.text((116, 1490), caption, font=font(FONT_SANS, 24), fill=CONCRETE)
    page_mark(draw, number)
    return save(canvas, f"{number:02d}.jpg")


def make_book_note():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.50, 0.48))
    base = ImageEnhance.Color(base).enhance(0.20)
    base = ImageEnhance.Brightness(base).enhance(0.38)
    base = base.filter(ImageFilter.GaussianBlur(1.6))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(CHARCOAL, 194)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 26, H), fill=TERRACOTTA)
    draw.rectangle((70, 66, 1170, 1590), outline=rgba(LIGHT, 145), width=2)
    draw.text((112, 110), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 27), fill=LIGHT)
    draw.text((112, 198), "完整作品", font=font(FONT_SERIF, 76), fill=LIGHT)
    draw.rectangle((112, 306, 1122, 320), fill=BRASS)

    statement = (
        "《The Complete Works》展示了斯卡帕如何把建筑从“造型”推进到“关系”："
        "每一道缝、每个节点和每次材料相遇，都在重新安排时间、身体与历史。"
    )
    statement_font = font(FONT_SERIF, 48)
    statement = wrap_text(draw, statement, statement_font, 980)
    draw.multiline_text((112, 420), statement, font=statement_font,
                        fill=LIGHT, spacing=29)

    draw.rounded_rectangle((112, 1115, 1124, 1405), radius=10, fill=rgba(PARCHMENT, 238))
    draw.text((154, 1160), "DETAIL IS A RELATIONSHIP", font=font(FONT_BOLD, 29), fill=TERRACOTTA)
    detail = "细部不是装饰，而是让石、金属、玻璃、水与人的动作彼此准确相遇。"
    draw.multiline_text((154, 1230), wrap_text(draw, detail, font(FONT_SERIF, 35), 900),
                        font=font(FONT_SERIF, 35), fill=CHARCOAL, spacing=14)
    draw.text((112, 1498), "编辑性概括｜非书中原句", font=font(FONT_SANS, 25), fill=rgba(LIGHT, 195))
    page_mark(draw, 6, light=True)
    return save(canvas, "06.jpg")


def make_preview(paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), "#bdb9af")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(image, (x, y))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def main():
    outputs = [make_cover()]
    outputs.append(make_project_page(
        2, "castelvecchio.jpg", "卡斯特维奇奥博物馆", "维罗纳｜1958—1974", "SEPARATION / GAP",
        "修复不是把新旧焊死，而是在它们之间留下一道清醒的缝，让历史被看见，也让当代介入保持诚实。",
        "新与旧保持距离，差异本身成为展陈的一部分。", (0.53, 0.50), BRASS, True,
    ))
    outputs.append(make_project_page(
        3, "olivetti.jpg", "奥利维蒂展厅", "威尼斯｜1957—1958", "CRAFT / DETAIL",
        "一段悬浮楼梯把石材、黄铜、光线和身体连接起来：节点不是收尾，而是空间真正发生的地方。",
        "每一级台阶既是结构，也是被精确安排的观看动作。", (0.50, 0.46), TERRACOTTA, True,
    ))
    outputs.append(make_project_page(
        4, "brion.jpg", "布里昂墓园", "圣维托｜1969—1978", "RITUAL / WATER",
        "圆、墙、水与路径把死亡转译成缓慢的行走；纪念性来自时间被材料轻轻托住。",
        "几何不是符号，而是身体进入记忆的仪式路线。", (0.50, 0.47), BLUE, False,
    ))
    outputs.append(make_project_page(
        5, "querini.jpg", "奎里尼·斯坦帕利亚基金会", "威尼斯｜1961—1963", "THRESHOLD / WATER",
        "斯卡帕不把水拒之门外，而是让潮汐进入建筑，成为连接城市、庭院与记忆的门槛。",
        "建筑不抵抗环境，而是把变化设计成日常经验。", (0.55, 0.52), MOSS, False,
    ))
    outputs.append(make_book_note())
    make_preview(outputs)
    print("\n".join(str(path) for path in outputs))


if __name__ == "__main__":
    main()
