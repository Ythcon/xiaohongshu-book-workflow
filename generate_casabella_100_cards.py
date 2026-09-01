from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "casabella-100"
OUT = ROOT / "output" / "casabella-100"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
PAPER = "#eee9df"
LIGHT = "#f8f4eb"
INK = "#12161a"
BLUE = "#173b53"
ORANGE = "#ea6c36"
MUTED = "#77736c"
SAND = "#c9aa72"
GREEN = "#71816f"

FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rgba(color, alpha=255):
    value = color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def wrap(draw, text, used_font, max_width):
    lines = []
    for paragraph in str(text).splitlines():
        current = ""
        for char in paragraph:
            trial = current + char
            if current and draw.textbbox((0, 0), trial, font=used_font)[2] > max_width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
    return "\n".join(lines)


def draw_fit(draw, xy, text, width, height, start_size, fill, *, serif=False, bold=False, spacing=12):
    path = FONT_SERIF if serif else FONT_BOLD if bold else FONT_SANS
    for size in range(start_size, 19, -2):
        used = font(path, size)
        wrapped = wrap(draw, text, used, width)
        box = draw.multiline_textbbox(xy, wrapped, font=used, spacing=spacing)
        if box[3] - xy[1] <= height:
            draw.multiline_text(xy, wrapped, font=used, fill=fill, spacing=spacing)
            return box[3]
    raise ValueError(f"Text does not fit: {text[:30]}")


def fit_inside(image, size):
    scale = min(size[0] / image.width, size[1] / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


def cover_crop(image, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / image.width, th / image.height)
    nw, nh = round(image.width * scale), round(image.height * scale)
    image = image.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, round((nw - tw) * focal[0])))
    top = max(0, min(nh - th, round((nh - th) * focal[1])))
    return image.crop((left, top, left + tw, top + th))


def paper_canvas(seed=100):
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    random.seed(seed)
    for _ in range(150):
        y = random.randint(0, H - 1)
        x = random.randint(0, W - 60)
        draw.line((x, y, min(W, x + random.randint(35, 190)), y), fill=rgba(INK, random.randint(3, 9)), width=1)
    return canvas


def page_mark(draw, number, light=False):
    color = rgba(LIGHT if light else INK, 170)
    draw.text((1167, 1602), f"{number:02d} / 08", font=font(FONT_SANS, 21), fill=color, anchor="ra")


def header(draw, number, light=False):
    color = LIGHT if light else INK
    draw.text((68, 52), "CASABELLA 100", font=font(FONT_BOLD, 22), fill=color)
    draw.text((1170, 52), "APRILE 1936 · ANNO IX", font=font(FONT_SANS, 20), fill=rgba(color, 185), anchor="ra")
    draw.line((68, 96, 1170, 96), fill=rgba(color, 85), width=2)
    page_mark(draw, number, light)


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def mount(canvas, image, box, background=LIGHT, shadow=True):
    x, y, w, h = box
    fitted = fit_inside(image, (w, h))
    px = x + (w - fitted.width) // 2
    py = y + (h - fitted.height) // 2
    if shadow:
        alpha = Image.new("L", (fitted.width + 50, fitted.height + 50), 0)
        ImageDraw.Draw(alpha).rectangle((14, 12, fitted.width + 34, fitted.height + 34), fill=115)
        alpha = alpha.filter(ImageFilter.GaussianBlur(14))
        sh = Image.new("RGBA", alpha.size, (0, 0, 0, 0))
        sh.putalpha(alpha)
        canvas.alpha_composite(sh, (px - 14, py - 8))
    frame = Image.new("RGBA", (fitted.width + 16, fitted.height + 16), rgba(background))
    frame.alpha_composite(fitted.convert("RGBA"), (8, 8))
    canvas.alpha_composite(frame, (px, py))


def mount_issue_cover(canvas, x, y, box):
    cover = Image.open(SRC / "book-cover.jpg").convert("RGB")
    cover = ImageEnhance.Sharpness(cover).enhance(1.3)
    mount(canvas, cover, (x, y, box[0], box[1]), LIGHT, True)


def source_strip(draw, text, light=False):
    fill = rgba(LIGHT, 238) if light else rgba(BLUE, 238)
    text_color = INK if light else LIGHT
    draw.rounded_rectangle((68, 972, 1172, 1044), 5, fill=fill)
    draw_fit(draw, (94, 990), text, 1048, 40, 20, text_color, spacing=4)


def text_panel(canvas, number, eyebrow, title, body, *, dark=False, accent=ORANGE):
    panel_y = 1070
    panel = BLUE if dark else PAPER
    canvas.alpha_composite(Image.new("RGBA", (W, H - panel_y), rgba(panel)), (0, panel_y))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((68, 1127, 80, 1525), fill=accent)
    text = LIGHT if dark else INK
    draw.text((112, 1120), eyebrow, font=font(FONT_BOLD, 22), fill=accent)
    bottom = draw_fit(draw, (112, 1180), title, 1010, 175, 49, text, serif=True, spacing=12)
    draw_fit(draw, (112, bottom + 28), body, 990, 145, 27, rgba(text, 205), spacing=9)
    page_mark(draw, number, dark)


def make_cover():
    canvas = paper_canvas(1)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 28, H), fill=BLUE)
    draw.rectangle((0, 0, W, 24), fill=ORANGE)
    draw.text((1165, 655), "100", font=font(FONT_BOLD, 350), fill=rgba(ORANGE, 38), anchor="ra")
    for i in range(10):
        draw.line((550 - i * 14, 665 + i * 40, 1190, 590 + i * 30), fill=rgba(BLUE, 42), width=3)
    draw.text((76, 76), "CASABELLA 100 / 核心观点", font=font(FONT_BOLD, 23), fill=ORANGE)
    draw.text((76, 136), "GIUSEPPE PAGANO · EDITORE", font=font(FONT_SANS, 22), fill=MUTED)
    draw_fit(draw, (76, 228), "建筑形式应该\n从哪里长出来？", 675, 350, 79, INK, serif=True, spacing=10)
    draw.rectangle((76, 594, 588, 606), fill=ORANGE)
    draw.text((76, 644), "CASABELLA 100", font=font(FONT_BOLD, 37), fill=BLUE)
    draw.text((76, 700), "1936年4月 · 第IX年", font=font(FONT_SANS, 24), fill=MUTED)
    mount_issue_cover(canvas, 766, 698, (344, 400))
    draw.rounded_rectangle((72, 1280, 1170, 1516), 8, fill=rgba(BLUE, 246))
    draw.text((108, 1322), "场地 × 程序 × 生活", font=font(FONT_BOLD, 22), fill=ORANGE)
    draw_fit(draw, (108, 1370), "场地决定形体，程序组织空间，公共生活检验建筑是否真正成立。", 1010, 115, 34, LIGHT, serif=True, spacing=10)
    page_mark(draw, 1, False)
    return save(canvas, "01.jpg")


def make_portrait_article():
    background = Image.open(SRC / "04-tennis-plan.jpg").convert("RGB")
    background = cover_crop(background, (W, 1070), (0.5, 0.5)).filter(ImageFilter.GaussianBlur(2.5))
    background = ImageEnhance.Contrast(background).enhance(0.75)
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    canvas.alpha_composite(background.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 1070), rgba(BLUE, 178)), (0, 0))
    portrait = Image.open(SRC / "02-cosenza-portrait.jpg").convert("RGB")
    portrait = portrait.resize((720, 540), Image.Resampling.LANCZOS)
    mount(canvas, portrait, (250, 205, 740, 620), LIGHT, True)
    draw = ImageDraw.Draw(canvas)
    header(draw, 2, True)
    source_strip(draw, "Giuseppe Pagano｜Un architetto: Luigi Cosenza｜Casabella 100, pp. 6—17", False)
    text_panel(
        canvas, 2, "观点 01｜现代性不是样式",
        "现代建筑不是一种外观，而是解决具体生活的工具",
        "Cosenza面对住宅、运动与教育三种任务，没有复制同一种形式；每个方案都从场地条件和使用方式重新开始。",
        dark=False,
    )
    return save(canvas, "02.jpg")


def make_document_page(number, image_name, source, eyebrow, title, body, accent=ORANGE, background=BLUE):
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    canvas.alpha_composite(Image.new("RGBA", (W, 1070), rgba(background)), (0, 0))
    image = Image.open(SRC / image_name).convert("RGB")
    mount(canvas, image, (76, 140, 1090, 785), LIGHT, True)
    draw = ImageDraw.Draw(canvas)
    header(draw, number, True)
    source_strip(draw, source, False)
    text_panel(canvas, number, eyebrow, title, body, dark=False, accent=accent)
    return save(canvas, f"{number:02d}.jpg")


def make_villa_page():
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    canvas.alpha_composite(Image.new("RGBA", (W, 1070), rgba(LIGHT)), (0, 0))
    photo = Image.open(SRC / "03-villa-oro-photo.jpg").convert("RGB")
    plan = Image.open(SRC / "03-villa-oro-plan.jpg").convert("RGB")
    mount(canvas, photo, (66, 130, 1110, 405), LIGHT, True)
    mount(canvas, plan, (66, 540, 1110, 395), LIGHT, True)
    draw = ImageDraw.Draw(canvas)
    header(draw, 4, False)
    source_strip(draw, "Luigi Cosenza / Bernard Rudofsky｜Una Villa · Villa Oro｜Casabella 100, pp. 8—11", False)
    text_panel(
        canvas, 4, "观点 03｜地形生成住宅",
        "顺着坡地展开，比复制标准平面更重要",
        "狭窄的Posillipo凝灰岩坡地、海景与高差共同决定剖面和动线；房间沿地形展开，让居住空间获得方向。",
        dark=False,
    )
    return save(canvas, "04.jpg")


def make_photo_page(number, image_name, source, eyebrow, title, body, focal=(0.5, 0.5), dark=False):
    image = Image.open(SRC / image_name).convert("RGB")
    image = cover_crop(image, (W, 1070), focal)
    image = ImageEnhance.Contrast(image).enhance(1.04)
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 120), (0, 0, 0, 92)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    header(draw, number, True)
    source_strip(draw, source, False)
    text_panel(canvas, number, eyebrow, title, body, dark=dark, accent=ORANGE)
    return save(canvas, f"{number:02d}.jpg")


def make_summary():
    canvas = paper_canvas(8)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 28, H), fill=ORANGE)
    header(draw, 8, False)
    draw.text((74, 154), "建筑观点总结", font=font(FONT_BOLD, 23), fill=ORANGE)
    draw_fit(draw, (74, 238), "好的现代建筑，不靠统一外形证明自己；它让场地、程序与生活形成清楚的空间秩序。", 1080, 390, 61, INK, serif=True, spacing=20)

    concepts = [("场地条件", ORANGE), ("空间秩序", SAND), ("生活方式", GREEN)]
    x = 74
    for idx, (label, color) in enumerate(concepts):
        width = 292
        draw.rounded_rectangle((x, 750, x + width, 830), 7, fill=color)
        draw.text((x + width / 2, 790), label, font=font(FONT_BOLD, 27), fill=INK, anchor="mm")
        if idx < 2:
            draw.line((x + width + 12, 790, x + width + 56, 790), fill=BLUE, width=4)
            draw.polygon([(x + width + 56, 790), (x + width + 40, 779), (x + width + 40, 801)], fill=BLUE)
        x += 368

    draw.rounded_rectangle((74, 932, 1168, 1475), 10, fill=rgba(BLUE, 248))
    takeaways = [
        "先读地形、朝向与既有结构，再决定建筑的轮廓。",
        "让动线连接功能与公共空间，而不是只把房间排列整齐。",
        "不同生活程序需要不同空间秩序，不必共用一种形式。",
    ]
    y = 1000
    for idx, item in enumerate(takeaways, 1):
        draw.rounded_rectangle((112, y, 172, y + 60), 8, fill=ORANGE)
        draw.text((142, y + 30), str(idx), font=font(FONT_BOLD, 27), fill=LIGHT, anchor="mm")
        draw_fit(draw, (204, y + 2), item, 900, 92, 29, LIGHT, serif=True, spacing=8)
        y += 142
    page_mark(draw, 8, False)
    return save(canvas, "08.jpg")


def make_preview(paths):
    tw, th, gap = 250, 334, 18
    cols, rows = 4, 2
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * th + (rows + 1) * gap), "#c8c3b9")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % cols) * (tw + gap)
        y = gap + (i // cols) * (th + gap)
        sheet.paste(image, (x, y))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def main():
    paths = [
        make_cover(),
        make_portrait_article(),
        make_document_page(
            3,
            "04-tennis-plan.jpg",
            "Luigi Cosenza / Bernard Rudofsky｜Una Villa · Un Tennis · Una scuola｜Casabella 100, pp. 8—17",
            "观点 02｜程序改变空间",
            "住宅、运动与教育，需要三种不同的空间答案",
            "住宅从坡地与居住动线出发，网球俱乐部沿既有球场展开，学校则围绕庭院与集体活动组织空间。",
        ),
        make_villa_page(),
        make_document_page(
            5,
            "04-tennis-photo.jpg",
            "Luigi Cosenza / Bernard Rudofsky｜Un Tennis｜Casabella 100, pp. 12—15",
            "观点 04｜既有秩序生成布局",
            "既有球场不是限制，而是建筑秩序的起点",
            "低矮更衣体、柱廊、泳池与露台沿球场几何展开，让建筑延续Villa Comunale与海岸之间的开放关系。",
            background=LIGHT,
        ),
        make_document_page(
            6,
            "05-school-drawing.jpg",
            "Luigi Cosenza｜Una scuola · Ponte di Casanova｜Casabella 100, pp. 16—17",
            "观点 05｜庭院组织公共生活",
            "庭院不是空地，而是学校生活的中心",
            "教学空间、树木庭院、礼堂与运动场被编进连续框架；建筑用边界组织活动，同时保持内部空间开放。",
            accent=GREEN,
            background="#b49a70",
        ),
        make_photo_page(
            7,
            "07-de-la-warr.jpg",
            "Erich Mendelsohn / Serge Chermayeff｜Casino di Bexhill nel Sussex｜Casabella 100",
            "观点 06｜流线塑造公共建筑",
            "连续流线，让文化建筑成为海岸公共空间",
            "De La Warr Pavilion用露台、楼梯与水平长廊连接文化、娱乐和海滨活动，让建筑本身成为可游走的城市客厅。",
            focal=(0.54, 0.52),
            dark=False,
        ),
        make_summary(),
    ]
    make_preview(paths)
    print(f"Created {len(paths)} cards and preview in {OUT}")


if __name__ == "__main__":
    main()
