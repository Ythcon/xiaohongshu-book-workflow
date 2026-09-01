from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "learning-from-las-vegas"
OUT = ROOT / "output" / "learning-from-las-vegas"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
INK = "#111111"
CREAM = "#f3ead8"
WHITE = "#fffaf0"
YELLOW = "#ffd400"
PINK = "#f04f78"
BLUE = "#2aa7d8"

FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"


def font(size, serif=False):
    return ImageFont.truetype(FONT_SERIF if serif else FONT_SANS, size)


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


def wrap(draw, text, used_font, max_width):
    lines, current = [], ""
    for ch in text:
        trial = current + ch
        if draw.textbbox((0, 0), trial, font=used_font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return "\n".join(lines)


def save(canvas, number):
    path = OUT / f"{number:02d}.jpg"
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def page_number(draw, number, dark=True):
    color = rgba(WHITE if dark else INK, 190)
    draw.text((1158, 1590), f"0{number} / 06", font=font(24), fill=color, anchor="ra")


def source_photo(name, contrast=1.02, color=1.02):
    image = Image.open(SRC / name).convert("RGB")
    image = ImageEnhance.Contrast(image).enhance(contrast)
    return ImageEnhance.Color(image).enhance(color)


def book_cover():
    # Publisher artwork remains a locked layer: proportional resize only.
    return Image.open(SRC / "book-cover.jpg").convert("RGB")


def mount_book_cover(canvas, box=(855, 1035, 1160, 1510)):
    x1, y1, x2, y2 = box
    cover = fit_inside(book_cover(), (x2 - x1, y2 - y1))
    pad = 10
    shadow = Image.new("RGBA", (cover.width + 44, cover.height + 44), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((18, 18, cover.width + 30, cover.height + 30), 8, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(shadow, (x1 - 18, y1 - 12))
    mount = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), rgba(WHITE))
    mount.alpha_composite(cover.convert("RGBA"), (pad, pad))
    canvas.alpha_composite(mount, (x1, y1))


def make_cover():
    photo = cover_crop(source_photo("01-welcome-sign.jpg", 1.06, 1.05), (W, H), (0.5, 0.48))
    canvas = photo.convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, W, 370), fill=(8, 8, 8, 178))
    od.rectangle((0, 960, W, H), fill=(8, 8, 8, 205))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 24, H), fill=YELLOW)
    draw.rounded_rectangle((64, 62, 520, 120), 5, fill=INK)
    draw.text((86, 76), "建筑如何成为信息？", font=font(25), fill=YELLOW)
    draw.text((66, 165), "为什么建筑师", font=font(76, serif=True), fill=WHITE)
    draw.text((62, 254), "要向赌场招牌学习？", font=font(83, serif=True), fill=YELLOW)

    draw.text((68, 1038), "《向拉斯维加斯学习》", font=font(50, serif=True), fill=WHITE)
    draw.rectangle((68, 1114, 712, 1127), fill=PINK)
    body = "从高速公路、霓虹招牌到“鸭子”与“装饰棚”\n一套重新阅读日常城市的视觉方法"
    draw.multiline_text((68, 1162), body, font=font(31), fill=rgba(WHITE, 220), spacing=18)
    mount_book_cover(canvas)
    page_number(draw, 1)
    return save(canvas, 1)


def make_case(number, filename, eyebrow, title, body, concept, focal=(0.5, 0.5), accent=YELLOW,
              photo_height=1030, source_note="", contain=False):
    photo = source_photo(filename, 1.05, 1.03)
    if contain:
        fitted = fit_inside(photo, (W, photo_height))
        photo_frame = Image.new("RGB", (W, photo_height), INK)
        photo_frame.paste(fitted, ((W - fitted.width) // 2, (photo_height - fitted.height) // 2))
        photo = photo_frame
    else:
        photo = cover_crop(photo, (W, photo_height), focal)
    canvas = Image.new("RGBA", (W, H), rgba(INK))
    canvas.alpha_composite(photo.convert("RGBA"), (0, 0))

    # Legibility strips preserve the documentary image while keeping text separate.
    top = Image.new("RGBA", (W, 162), (0, 0, 0, 128))
    canvas.alpha_composite(top, (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=accent)
    draw.rounded_rectangle((64, 58, 680, 117), 5, fill=rgba(INK, 220))
    draw.text((86, 72), eyebrow, font=font(25), fill=accent)
    draw.rectangle((0, photo_height, W, H), fill=INK)
    draw.rectangle((66, photo_height + 54, 230, photo_height + 67), fill=accent)
    title_font = font(61, serif=True)
    title_text = wrap(draw, title, title_font, 1080)
    draw.multiline_text((66, photo_height + 106), title_text, font=title_font, fill=WHITE, spacing=11)
    title_bottom = draw.multiline_textbbox((66, photo_height + 106), title_text, font=title_font, spacing=11)[3]
    body_font = font(29)
    draw.multiline_text((68, title_bottom + 40), wrap(draw, body, body_font, 1070),
                        font=body_font, fill=rgba(WHITE, 205), spacing=12)
    page_number(draw, number)
    return save(canvas, number)


def make_summary():
    photo = cover_crop(source_photo("06-vanna-venturi-house.jpg", 1.07, 0.94), (W, 720), (0.5, 0.53))
    canvas = Image.new("RGBA", (W, H), rgba(INK))
    canvas.alpha_composite(photo.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 170), (0, 0, 0, 112)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=BLUE)

    # The author work remains visible and explicitly named; the rest of the
    # card synthesizes the book instead of introducing another case.
    draw.rounded_rectangle((64, 58, 735, 122), 5, fill=rgba(INK, 226))
    draw.text((86, 76), "作者作品｜文丘里母亲住宅 · 1962–1964", font=font(25), fill=BLUE)
    draw.rectangle((54, 640, 810, 704), fill=rgba(INK, 224))
    draw.text((76, 671), "VANNA VENTURI HOUSE · 宾夕法尼亚州", font=font(23), fill=WHITE, anchor="lm")

    draw.rounded_rectangle((52, 760, 1190, 1545), 16, fill="#0b0b0b")
    draw.rectangle((82, 804, 310, 866), fill=YELLOW)
    draw.text((196, 835), "本书总结", font=font(28), fill=INK, anchor="mm")
    draw.text((338, 835), "罗伯特·文丘里、丹尼斯·斯科特·布朗 ×《向拉斯维加斯学习》",
              font=font(25), fill=WHITE, anchor="lm")

    conclusion = "建筑不必沉默。\n它可以借符号、尺度与日常意象，\n主动和城市沟通。"
    draw.multiline_text((82, 925), conclusion, font=font(55, serif=True), fill=WHITE, spacing=14)
    draw.rectangle((82, 1162, 1156, 1172), fill=PINK)

    tags = [("DUCK", YELLOW), ("DECORATED SHED", PINK), ("COMMUNICATION", BLUE)]
    x = 84
    for label, color in tags:
        width = draw.textbbox((0, 0), label, font=font(21))[2] + 42
        draw.rounded_rectangle((x, 1208, x + width, 1258), 8, fill=color)
        draw.text((x + width / 2, 1233), label, font=font(21), fill=INK, anchor="mm")
        x += width + 16

    takeaways = [
        "先理解汽车速度、停车场和连续视野怎样改变城市阅读。",
        "“鸭子”让形体成为信息；“装饰棚”用符号赋予普通空间意义。",
        "接受复杂、矛盾与大众文化，建筑才能回应真实生活。",
    ]
    y = 1302
    for index, item in enumerate(takeaways, 1):
        color = (YELLOW, PINK, BLUE)[index - 1]
        draw.rounded_rectangle((84, y, 132, y + 48), 8, fill=color)
        draw.text((108, y + 24), str(index), font=font(23), fill=INK, anchor="mm")
        draw.text((158, y + 4), item, font=font(27), fill=rgba(WHITE, 224))
        y += 67

    page_number(draw, 6)
    return save(canvas, 6)


def make_preview(paths):
    tw, th, gap = 310, 414, 18
    preview = Image.new("RGB", (tw * 3 + gap * 4, th * 2 + gap * 3), "#d8d2c6")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        preview.paste(image, (x, y))
    preview.save(OUT / "preview.jpg", quality=94, optimize=True)


def main():
    paths = [
        make_cover(),
        make_case(
            2, "02-strip-aerial.jpg", "LAS VEGAS STRIP · 拉斯维加斯大道",
            "城市，是从车窗里被读懂的",
            "高速移动改变了建筑的尺度：街道不再只靠立面组织，而是靠道路、停车场、招牌和连续视野共同构成。",
            "汽车尺度 / 连续视野", (0.5, 0.57), BLUE,
            source_note="案例｜Las Vegas Strip · 航拍"
        ),
        make_case(
            3, "03-fremont-sign.jpg", "FREMONT STREET · 弗里蒙特街",
            "当招牌比建筑更先被看见",
            "在拉斯维加斯，信息不是附属物。巨型文字、箭头和霓虹承担了远距离识别，建筑反而退到符号之后。",
            "标识系统 / 沟通优先", (0.51, 0.48), PINK,
            source_note="案例｜Fremont Street · 霓虹标识"
        ),
        make_case(
            4, "04-big-duck.jpg", "THE BIG DUCK · 大鸭子",
            "“鸭子”：建筑本身就是符号",
            "当建筑的整体形状直接说明它是什么，空间、结构与图像被捆绑在一起。Big Duck 是这类建筑最直白的例子。",
            "Duck / 形体即信息", (0.56, 0.48), YELLOW,
            source_note="案例｜The Big Duck · Flanders, New York"
        ),
        make_case(
            5, "05-caesars-1970.jpg", "CAESARS PALACE · 凯撒宫",
            "普通盒子，也能靠符号制造意义",
            "凯撒宫用柱廊、字体与罗马意象包装常规体量。重要的不是结构炫技，而是让人立即读出一个明确主题。",
            "装饰棚 / 主题化", (0.52, 0.50), PINK,
            photo_height=900,
            source_note="案例｜Caesars Palace · 1970", contain=True
        ),
        make_summary(),
    ]
    make_preview(paths)
    print(f"Generated {len(paths)} cards in {OUT}")


if __name__ == "__main__":
    main()
