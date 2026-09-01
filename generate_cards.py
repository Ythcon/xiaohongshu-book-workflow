from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "source"
OUT = ROOT / "output" / "wang-shu-design-begins"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
PAPER = "#eee9df"
INK = "#171816"
BRICK = "#9b3f2d"
MOSS = "#5c6251"

FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"
FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_SANS_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def hex_rgba(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def add_paper_texture(image, strength=9, seed=21):
    random.seed(seed)
    noise = Image.new("L", image.size, 128)
    px = noise.load()
    for y in range(0, image.height, 4):
        for x in range(0, image.width, 4):
            v = 128 + random.randint(-strength, strength)
            for yy in range(y, min(y + 4, image.height)):
                for xx in range(x, min(x + 4, image.width)):
                    px[xx, yy] = v
    noise = noise.filter(ImageFilter.GaussianBlur(0.6))
    texture = Image.merge("RGBA", (noise, noise, noise, Image.new("L", image.size, 22)))
    image.alpha_composite(texture)


def cover_crop(img, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    fx, fy = focal
    left = max(0, min(nw - tw, int(nw * fx - tw / 2)))
    top = max(0, min(nh - th, int(nh * fy - th / 2)))
    return img.crop((left, top, left + tw, top + th))


def fit_text(draw, text, box_width, start_size, min_size, path=FONT_SERIF, spacing=15):
    for size in range(start_size, min_size - 1, -2):
        f = font(path, size)
        bbox = draw.multiline_textbbox((0, 0), text, font=f, spacing=spacing)
        if bbox[2] - bbox[0] <= box_width:
            return f
    return font(path, min_size)


def page_number(draw, number, dark=False):
    color = PAPER if dark else INK
    f = font(FONT_SANS, 27)
    draw.text((1080, 1540), f"0{number} / 06", font=f, fill=color, anchor="ra")


def label(draw, text, xy, light=False):
    color = PAPER if light else INK
    f = font(FONT_SANS_BOLD, 27)
    draw.text(xy, text, font=f, fill=color)


def save(img, number):
    path = OUT / f"{number:02d}.jpg"
    img.convert("RGB").save(path, quality=94, subsampling=0, optimize=True)
    return path


def make_cover(images):
    canvas = Image.new("RGBA", (W, H), PAPER)
    add_paper_texture(canvas, seed=1)
    draw = ImageDraw.Draw(canvas)

    strip_h = 935
    widths = [304, 304, 304, 330]
    x = 0
    focals = [(0.49, 0.50), (0.55, 0.52), (0.58, 0.50), (0.52, 0.45)]
    for im, sw, fp in zip(images, widths, focals):
        part = cover_crop(im, (sw, strip_h), fp)
        part = ImageEnhance.Color(part).enhance(0.72)
        part = ImageEnhance.Contrast(part).enhance(1.08)
        canvas.alpha_composite(part.convert("RGBA"), (x, 0))
        x += sw

    overlay = Image.new("RGBA", (W, strip_h), (15, 15, 12, 42))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 25, H), fill=BRICK)
    draw.rectangle((74, 880, 1168, 1005), fill=hex_rgba(PAPER, 245))
    label(draw, "ARCHITECT / BOOK / 01", (92, 916))

    draw.text((86, 1062), "王 澍", font=font(FONT_SERIF, 154), fill=INK)
    draw.text((91, 1260), "设计的开始", font=font(FONT_SERIF, 84), fill=BRICK)
    draw.line((92, 1400, 1138, 1400), fill=hex_rgba(INK, 100), width=2)
    draw.text((92, 1440), "从建造一座房子，开始辨认自己的语言", font=font(FONT_SANS, 36), fill=INK)
    page_number(draw, 1)
    return save(canvas, 1)


def make_work_page(number, image, project, city_year, headline, body, focal, accent=BRICK):
    canvas = Image.new("RGBA", (W, H), PAPER)
    photo_h = 1060
    photo = cover_crop(image, (W, photo_h), focal)
    photo = ImageEnhance.Color(photo).enhance(0.82)
    photo = ImageEnhance.Contrast(photo).enhance(1.07)
    canvas.alpha_composite(photo.convert("RGBA"), (0, 0))

    shade = Image.new("RGBA", (W, photo_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(260):
        alpha = int(125 * (1 - y / 260))
        sd.line((0, y, W, y), fill=(0, 0, 0, alpha))
    canvas.alpha_composite(shade)

    draw = ImageDraw.Draw(canvas)
    label(draw, f"WORK 0{number - 1}", (76, 66), light=True)
    draw.text((1166, 65), city_year, font=font(FONT_SANS, 25), fill=PAPER, anchor="ra")

    draw.rectangle((0, 1060, W, H), fill=PAPER)
    add_paper_texture(canvas, seed=number)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((76, 1118, 90, 1526), fill=accent)
    draw.text((126, 1114), project, font=font(FONT_SANS_BOLD, 34), fill=accent)

    f_head = fit_text(draw, headline, 1000, 62, 48, FONT_SERIF, spacing=18)
    draw.multiline_text((126, 1188), headline, font=f_head, fill=INK, spacing=18)
    draw.text((126, 1458), body, font=font(FONT_SANS, 28), fill=hex_rgba(INK, 178))
    page_number(draw, number)
    return save(canvas, number)


def make_book_page(image):
    canvas = Image.new("RGBA", (W, H), INK)
    bg = cover_crop(image, (W, H), (0.54, 0.46)).filter(ImageFilter.GaussianBlur(3.2))
    bg = ImageEnhance.Color(bg).enhance(0.28)
    bg = ImageEnhance.Brightness(bg).enhance(0.46)
    canvas.alpha_composite(bg.convert("RGBA"))
    canvas.alpha_composite(Image.new("RGBA", (W, H), (8, 10, 8, 115)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((70, 70, 1172, 1590), outline=hex_rgba(PAPER, 100), width=2)
    draw.rectangle((70, 70, 95, 390), fill=BRICK)
    label(draw, "ONE-SENTENCE BOOK NOTE", (126, 114), light=True)
    draw.text((126, 240), "《设计的开始》", font=font(FONT_SERIF, 58), fill=PAPER)
    draw.line((126, 344, 1110, 344), fill=hex_rgba(PAPER, 90), width=2)

    summary = "设计的开始，\n不是先画出一个漂亮形式，\n而是在真实的建造与生活中，\n逐渐自觉自己正在使用的语言。"
    draw.multiline_text((126, 470), summary, font=font(FONT_SERIF, 65), fill=PAPER, spacing=32)

    draw.rectangle((126, 1128, 1102, 1392), fill=hex_rgba(PAPER, 232))
    draw.text((174, 1172), "读完留下的问题", font=font(FONT_SANS_BOLD, 30), fill=BRICK)
    question = "当我们设计一座房子，\n是否也在设计一种生活与记忆？"
    draw.multiline_text((174, 1235), question, font=font(FONT_SERIF, 42), fill=INK, spacing=16)
    draw.text((126, 1476), "编辑性概括｜非书中原句", font=font(FONT_SANS, 25), fill=hex_rgba(PAPER, 170))
    page_number(draw, 6, dark=True)
    return save(canvas, 6)


def make_contact_sheet(paths):
    thumb_w, thumb_h = 372, 498
    gap = 28
    sheet = Image.new("RGB", (3 * thumb_w + 4 * gap, 2 * thumb_h + 3 * gap), "#d8d2c8")
    for idx, path in enumerate(paths):
        im = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = gap + (idx % 3) * (thumb_w + gap)
        y = gap + (idx // 3) * (thumb_h + gap)
        sheet.paste(im, (x, y))
    sheet.save(OUT / "preview.jpg", quality=92, subsampling=0)


def make_book_work_composite(photos):
    """Create a standalone cover that combines the actual book cover with built works."""
    canvas = Image.new("RGBA", (W, H), PAPER)
    add_paper_texture(canvas, seed=17)

    # Main architectural background.
    hero = cover_crop(photos[0], (W, 1110), (0.49, 0.50))
    hero = ImageEnhance.Color(hero).enhance(0.58)
    hero = ImageEnhance.Contrast(hero).enhance(1.16)
    canvas.alpha_composite(hero.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 1110), (8, 9, 7, 88)), (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=BRICK)
    label(draw, "BOOK × ARCHITECTURE", (72, 64), light=True)
    draw.text((1168, 62), "WANG SHU / 01", font=font(FONT_SANS, 25), fill=PAPER, anchor="ra")

    # Two architectural detail windows to make the montage explicit.
    inset_specs = [
        (photos[1], (786, 160, 1158, 402), (0.52, 0.52)),
        (photos[2], (850, 438, 1158, 642), (0.57, 0.50)),
    ]
    for im, box, focal in inset_specs:
        x1, y1, x2, y2 = box
        detail = cover_crop(im, (x2 - x1, y2 - y1), focal)
        detail = ImageEnhance.Color(detail).enhance(0.68)
        canvas.alpha_composite(detail.convert("RGBA"), (x1, y1))
        draw.rectangle(box, outline=hex_rgba(PAPER, 170), width=3)

    # Book cover with a light mount, subtle tilt and real shadow.
    cover = Image.open(SRC / "lac-cover-2.jpg").convert("RGB")
    target_w = 500
    target_h = int(target_w * cover.height / cover.width)
    cover = cover.resize((target_w, target_h), Image.Resampling.LANCZOS)
    mount = Image.new("RGBA", (target_w + 34, target_h + 34), PAPER)
    mount.alpha_composite(cover.convert("RGBA"), (17, 17))
    mount = mount.rotate(2.2, resample=Image.Resampling.BICUBIC, expand=True, fillcolor=(0, 0, 0, 0))
    shadow = Image.new("RGBA", mount.size, (0, 0, 0, 0))
    shadow.alpha_composite(mount, (0, 0))
    alpha = shadow.getchannel("A").filter(ImageFilter.GaussianBlur(18))
    shadow = Image.new("RGBA", mount.size, (0, 0, 0, 125))
    shadow.putalpha(alpha.point(lambda p: int(p * 0.55)))
    canvas.alpha_composite(shadow, (105, 216))
    canvas.alpha_composite(mount, (87, 193))

    # Editorial question beside the cover.
    draw = ImageDraw.Draw(canvas)
    draw.text((680, 718), "设计", font=font(FONT_SERIF, 76), fill=PAPER)
    draw.text((680, 816), "从哪里开始？", font=font(FONT_SERIF, 76), fill=PAPER)
    draw.line((680, 930, 1148, 930), fill=hex_rgba(PAPER, 120), width=2)
    draw.text((680, 966), "一本书，读懂王澍的建造语言", font=font(FONT_SANS, 31), fill=PAPER)

    # Paper caption area.
    draw.rectangle((0, 1110, W, H), fill=PAPER)
    add_paper_texture(canvas, seed=18)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((74, 1180, 88, 1514), fill=BRICK)
    draw.text((126, 1174), "王澍｜《设计的开始》", font=font(FONT_SANS_BOLD, 34), fill=BRICK)
    summary = "设计的开始，不是先画出一个漂亮形式，\n而是在真实的建造与生活中，\n逐渐自觉自己正在使用的语言。"
    draw.multiline_text((126, 1252), summary, font=font(FONT_SERIF, 48), fill=INK, spacing=18)
    draw.text((126, 1486), "书籍封面 × 宁波博物馆 × 宁波美术馆 × 临安博物馆", font=font(FONT_SANS, 25), fill=hex_rgba(INK, 170))
    draw.text((1140, 1555), "COVER / 3:4", font=font(FONT_SANS, 25), fill=INK, anchor="ra")

    path = OUT / "book-cover-composite.jpg"
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def main():
    photos = [
        Image.open(SRC / "01-ningbo-museum.jpg").convert("RGB"),
        Image.open(SRC / "02-ningbo-art-museum.jpg").convert("RGB"),
        Image.open(SRC / "03-linan-museum.jpg").convert("RGB"),
        Image.open(SRC / "04-ningbo-rooftop-corridor.jpg").convert("RGB"),
    ]
    outputs = [make_cover(photos)]
    outputs.append(make_work_page(
        2, photos[0], "宁波博物馆", "NINGBO · 2008",
        "旧材料不是怀旧，\n它让一座被更新的城市\n重新拥有记忆。",
        "旧砖、旧瓦与新结构并置，时间成为建筑材料。", (0.50, 0.51), BRICK))
    outputs.append(make_work_page(
        3, photos[3], "宁波博物馆·屋顶走廊", "NINGBO · 2008",
        "建筑不是孤立的物件，\n而是一段可以行走、\n停留与回望的关系。",
        "路径、院落与屋顶，共同组织人与空间的相遇。", (0.52, 0.50), MOSS))
    outputs.append(make_work_page(
        4, photos[1], "宁波美术馆", "NINGBO · 2005",
        "建筑先回应场所，\n再表达自己。",
        "港口、码头与城市生活，共同决定了空间的气质。", (0.52, 0.52), BRICK))
    outputs.append(make_work_page(
        5, photos[2], "临安博物馆", "HANGZHOU · 2019",
        "传统不是复制古代，\n而是让材料、手艺与时间\n在今天继续生长。",
        "真正的当代性，也可以从地方经验中发生。", (0.56, 0.50), MOSS))
    outputs.append(make_book_page(photos[0]))
    make_contact_sheet(outputs)
    composite = make_book_work_composite(photos)
    print(composite)
    print("\n".join(str(p) for p in outputs))


if __name__ == "__main__":
    main()
