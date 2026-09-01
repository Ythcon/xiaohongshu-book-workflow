from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "kengo-kuma"
OUT = ROOT / "output" / "kengo-kuma-anti-object"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
PAPER = "#eee8dc"
PAPER_LIGHT = "#f7f3e9"
INK = "#20221f"
WOOD = "#9a6b43"
MOSS = "#66705e"
STONE = "#8b8980"
WHITE = "#f8f5ed"

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
    for ch in text:
        candidate = current + ch
        if current and draw.textbbox((0, 0), candidate, font=fnt)[2] > max_width:
            lines.append(current)
            current = ch
        else:
            current = candidate
    if current:
        lines.append(current)
    return "\n".join(lines)


def material_slats(draw, box, color=WOOD, alpha=90, gap=42, width=10):
    x1, y1, x2, y2 = box
    x = x1
    while x <= x2:
        draw.rounded_rectangle((x, y1, x + width, y2), radius=width // 2,
                               fill=rgba(color, alpha))
        x += gap


def page_mark(draw, number, light=False):
    color = WHITE if light else INK
    draw.text((1146, 1576), f"0{number} / 06", font=font(FONT_SANS, 24),
              fill=color, anchor="ra")


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def real_book_mount(canvas, position=(70, 880), box=(400, 560)):
    cover = Image.open(SRC / "book-cover-2018.jpg").convert("RGB")
    cover = fit_inside(cover, box)
    pad = 20
    mount = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), WHITE)
    mount.alpha_composite(cover.convert("RGBA"), (pad, pad))
    shadow_alpha = Image.new("L", mount.size, 0)
    ImageDraw.Draw(shadow_alpha).rounded_rectangle((8, 8, mount.width - 8, mount.height - 8),
                                                   radius=12, fill=150)
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(20))
    shadow = Image.new("RGBA", mount.size, (20, 18, 14, 0))
    shadow.putalpha(shadow_alpha)
    x, y = position
    canvas.alpha_composite(shadow, (x + 18, y + 24))
    canvas.alpha_composite(mount, (x, y))


def make_cover():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.51, 0.48))
    base = ImageEnhance.Contrast(base).enhance(1.04)
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (25, 24, 20, 68)))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 28, H), fill=WOOD)
    draw.rectangle((70, 68, 430, 116), fill=rgba(PAPER_LIGHT, 230))
    draw.text((90, 77), "BOOK × ARCHITECTURE / 03", font=font(FONT_BOLD, 24), fill=INK)
    draw.rounded_rectangle((52, 154, 708, 690), radius=12, fill=rgba(INK, 132))
    draw.text((72, 184), "隈研吾", font=font(FONT_BOLD, 40), fill=WHITE)
    draw.text((72, 270), "反", font=font(FONT_SERIF, 178), fill=WHITE)
    draw.text((252, 270), "造", font=font(FONT_SERIF, 178), fill=WHITE)
    draw.text((432, 270), "型", font=font(FONT_SERIF, 178), fill=WHITE)
    draw.rectangle((74, 486, 700, 500), fill=WOOD)
    draw.text((74, 530), "与自然连接的建筑", font=font(FONT_SERIF, 51), fill=WHITE)
    draw.text((74, 610), "让建筑从“物体”变回关系", font=font(FONT_SANS, 31), fill=rgba(WHITE, 215))

    # Use the generated collage for atmosphere, then lock the authentic cover on top.
    real_book_mount(canvas, (72, 870), (390, 570))

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((730, 1000, 1168, 1510), radius=14, fill=rgba(PAPER_LIGHT, 226))
    material_slats(draw, (760, 1032, 1132, 1138), WOOD, 130, 32, 8)
    summary = "把建筑拆成\n材料、光与缝隙，\n让它重新连接\n人、自然和场所。"
    draw.multiline_text((770, 1184), summary, font=font(FONT_SERIF, 42),
                        fill=INK, spacing=12)
    draw.text((770, 1460), "编辑性概括", font=font(FONT_SANS, 24), fill=MOSS)
    page_mark(draw, 1, light=True)

    path = save(canvas, "01.jpg")
    save(canvas, "book-cover-composite.jpg")
    return path


def make_project_page(number, source_name, project, meta, headline, caption,
                      focal=(0.5, 0.5), accent=WOOD):
    photo = Image.open(SRC / source_name).convert("RGB")
    photo_h = 1050
    image = cover_crop(photo, (W, photo_h), focal)
    image = ImageEnhance.Color(image).enhance(0.86)
    image = ImageEnhance.Contrast(image).enhance(1.07)

    canvas = Image.new("RGBA", (W, H), PAPER)
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 230), (0, 0, 0, 76)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 28, H), fill=accent)
    draw.rectangle((66, 64, 250, 112), fill=rgba(PAPER_LIGHT, 232))
    draw.text((84, 74), f"CASE 0{number - 1}", font=font(FONT_BOLD, 23), fill=INK)
    draw.text((1164, 72), meta, font=font(FONT_SANS, 24), fill=WHITE, anchor="ra")
    draw.line((76, 972, 560, 972), fill=accent, width=12)

    draw.rectangle((0, photo_h, W, H), fill=PAPER)
    material_slats(draw, (760, 1082, 1180, 1166), accent, 90, 34, 8)
    draw.text((80, 1090), project, font=font(FONT_BOLD, 32), fill=accent)
    headline_font = font(FONT_SERIF, 54)
    wrapped = wrap_text(draw, headline, headline_font, 1040)
    draw.multiline_text((80, 1180), wrapped, font=headline_font, fill=INK, spacing=15)
    draw.text((80, 1488), caption, font=font(FONT_SANS, 26), fill=rgba(MOSS, 225))
    page_mark(draw, number)
    return save(canvas, f"{number:02d}.jpg")


def make_book_note():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.48, 0.48))
    base = ImageEnhance.Color(base).enhance(0.35)
    base = ImageEnhance.Brightness(base).enhance(0.42)
    base = base.filter(ImageFilter.GaussianBlur(2.2))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(INK, 178)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 28, H), fill=WOOD)
    draw.rounded_rectangle((70, 68, 1170, 1588), radius=12, outline=rgba(PAPER_LIGHT, 130), width=2)
    draw.text((112, 112), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 27), fill=WHITE)
    draw.text((112, 202), "反造型", font=font(FONT_SERIF, 82), fill=WHITE)
    draw.line((112, 314, 1122, 314), fill=WOOD, width=12)

    statement = (
        "《反造型》不是拒绝形式，\n"
        "而是把封闭、突出的建筑物\n"
        "拆成材料、光、缝隙与关系，\n"
        "让建筑重新成为连接人、\n"
        "自然与场所的媒介。"
    )
    draw.multiline_text((112, 420), statement, font=font(FONT_SERIF, 58),
                        fill=WHITE, spacing=34)

    draw.rounded_rectangle((112, 1184, 1120, 1408), radius=12, fill=rgba(PAPER_LIGHT, 222))
    draw.text((154, 1222), "ANTI-OBJECT ≠ NO FORM", font=font(FONT_BOLD, 29), fill=WOOD)
    answer = "它反对的是把建筑当成孤立、封闭、\n只供观看的对象。"
    draw.multiline_text((154, 1285), answer, font=font(FONT_SERIF, 37), fill=INK, spacing=10)
    draw.text((112, 1496), "编辑性概括｜非书中原句", font=font(FONT_SANS, 25),
              fill=rgba(WHITE, 190))
    page_mark(draw, 6, light=True)
    return save(canvas, "06.jpg")


def make_preview(paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), "#d3cec2")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(image, (x, y))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def main():
    outputs = [make_cover()]
    outputs.append(make_project_page(
        2, "stone-plaza.jpg", "石之美术馆", "栃木｜2000",
        "当石头被切薄、穿孔、透光，厚重的材料也能变成一层关系。",
        "内外之间不再是边界，而是一段可以穿行的光与水。",
        (0.53, 0.58), STONE,
    ))
    outputs.append(make_project_page(
        3, "gc-prostho.jpg", "GC 口腔博物馆研究中心", "爱知｜2010",
        "把整体拆成可连接的微小单元，建筑就从一个物体变成可以生长的系统。",
        "木格栅既承重，也展示；结构与空间不再彼此分离。",
        (0.51, 0.47), WOOD,
    ))
    outputs.append(make_project_page(
        4, "asakusa.jpg", "浅草文化观光中心", "东京｜2012",
        "不是制造一个巨大的造型，而是把体量拆成一叠属于街区尺度的小屋顶。",
        "建筑以层叠回应雷门前的街道、屋檐与日常尺度。",
        (0.50, 0.52), MOSS,
    ))
    outputs.append(make_project_page(
        5, "va-dundee.jpg", "V&A Dundee", "苏格兰｜2018",
        "建筑可以像地层与海岸：边界被层层削弱，物体开始回应水、风与城市。",
        "后期作品延续“反造型”的思考，让建筑成为场所的一部分。",
        (0.47, 0.54), STONE,
    ))
    outputs.append(make_book_note())
    make_preview(outputs)
    print("\n".join(str(path) for path in outputs))


if __name__ == "__main__":
    main()
