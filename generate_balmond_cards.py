from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "cecil-balmond"
OUT = ROOT / "output" / "cecil-balmond-informal"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
BLUE = "#173f70"
RED = "#a93449"
YELLOW = "#ead34f"
BLACK = "#141414"
OLIVE = "#9d8b55"
GREEN = "#24593e"
PAPER = "#eee9df"
WHITE = "#faf8f1"
GREY = "#777873"

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


def network(draw, box, color=BLACK, alpha=55, seed=23):
    """A deterministic field: apparent irregularity built from connected points."""
    random.seed(seed)
    x1, y1, x2, y2 = box
    pts = []
    cols, rows = 6, 5
    for row in range(rows):
        for col in range(cols):
            x = x1 + (x2 - x1) * col / (cols - 1) + random.randint(-28, 28)
            y = y1 + (y2 - y1) * row / (rows - 1) + random.randint(-24, 24)
            pts.append((round(x), round(y)))
    for row in range(rows):
        for col in range(cols):
            i = row * cols + col
            if col + 1 < cols:
                draw.line((pts[i], pts[i + 1]), fill=rgba(color, alpha), width=2)
            if row + 1 < rows:
                draw.line((pts[i], pts[i + cols]), fill=rgba(color, alpha), width=2)
            if row + 1 < rows and col + (row % 2) < cols:
                j = i + cols + (row % 2)
                if j < len(pts):
                    draw.line((pts[i], pts[j]), fill=rgba(color, max(15, alpha - 16)), width=2)
    for x, y in pts[::3]:
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=rgba(color, alpha + 35))


def rotated_square(draw, center, radius, angle, color, width=3):
    cx, cy = center
    pts = []
    for i in range(4):
        a = angle + math.pi / 4 + i * math.pi / 2
        pts.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
    pts.append(pts[0])
    draw.line(pts, fill=color, width=width, joint="curve")


def page_mark(draw, number, light=False):
    color = WHITE if light else BLACK
    draw.text((1168, 1584), f"0{number} / 06", font=font(FONT_SANS, 22), fill=color, anchor="ra")


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def authentic_cover():
    image = Image.open(SRC / "book-cover-cn.png").convert("RGB")
    # Remove only the thin screenshot border; retain the cover's white bands.
    return image.crop((13, 4, image.width - 12, image.height - 14))


def mount_book(canvas, position=(66, 1038), box=(340, 470)):
    cover = fit_inside(authentic_cover(), box)
    pad = 12
    mount = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), WHITE)
    mount.alpha_composite(cover.convert("RGBA"), (pad, pad))
    alpha = Image.new("L", mount.size, 0)
    ImageDraw.Draw(alpha).rounded_rectangle((8, 8, mount.width - 4, mount.height - 4), 6, fill=145)
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
    canvas.alpha_composite(Image.new("RGBA", (W, H), (8, 9, 10, 20)))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 28, H), fill=RED)
    draw.rectangle((62, 60, 442, 112), fill=rgba(PAPER, 240))
    draw.text((82, 72), "BOOK × STRUCTURE / 06", font=font(FONT_BOLD, 23), fill=BLACK)

    draw.rounded_rectangle((54, 146, 760, 720), radius=10, fill=rgba(BLACK, 215))
    draw.text((82, 184), "塞西尔·巴尔蒙德", font=font(FONT_BOLD, 39), fill=WHITE)
    draw.text((78, 276), "异规", font=font(FONT_SERIF, 154), fill=WHITE)
    draw.text((422, 314), "informal", font=font(FONT_SANS, 54), fill=YELLOW)
    draw.rectangle((82, 486, 684, 499), fill=RED)
    draw.text((82, 544), "结构，不必长得整齐", font=font(FONT_SERIF, 43), fill=WHITE)
    draw.text((82, 616), "HIDDEN ORDER / OPEN SYSTEM", font=font(FONT_BOLD, 26), fill=rgba(WHITE, 205))
    for i, radius in enumerate((55, 89, 126)):
        rotated_square(draw, (650, 646), radius, i * 0.22, rgba(YELLOW, 105 - i * 18), 2)

    mount_book(canvas, (64, 1052), (332, 462))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((470, 1038, 1175, 1507), radius=10, fill=rgba(PAPER, 238))
    draw.text((514, 1080), "IRREGULAR ≠ RANDOM", font=font(FONT_BOLD, 28), fill=RED)
    line = "所谓“异规”，不是放弃规则，\n而是让结构从重复之外，\n生成建筑的节奏、力量与形式。"
    draw.multiline_text((514, 1162), line, font=font(FONT_SERIF, 39), fill=BLACK, spacing=18)
    draw.text((514, 1423), "编辑性概括｜非书中原句", font=font(FONT_SANS, 23), fill=GREY)
    page_mark(draw, 1, light=True)

    path = save(canvas, "01.jpg")
    save(canvas, "book-cover-composite.jpg")
    return path


def make_project_page(number, source, project, meta, concept, headline, caption,
                      focal=(0.5, 0.5), accent=RED, dark_panel=False):
    photo = Image.open(SRC / source).convert("RGB")
    photo_h = 1040
    image = cover_crop(photo, (W, photo_h), focal)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Color(image).enhance(0.88)

    panel = BLACK if dark_panel else PAPER
    text_color = WHITE if dark_panel else BLACK
    canvas = Image.new("RGBA", (W, H), panel)
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 174), (0, 0, 0, 76)), (0, 0))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 28, H), fill=accent)
    draw.rectangle((64, 58, 245, 112), fill=accent)
    draw.text((82, 72), f"CASE 0{number - 1}", font=font(FONT_BOLD, 23), fill=WHITE)
    draw.text((1168, 71), meta, font=font(FONT_SANS, 24), fill=WHITE, anchor="ra")
    draw.rectangle((66, 918, 510, 984), fill=rgba(BLACK, 222))
    draw.text((88, 936), concept, font=font(FONT_BOLD, 24), fill=accent)

    draw.rectangle((0, photo_h, W, H), fill=panel)
    network(draw, (710, 1054, 1218, 1588), accent, 34, seed=number * 17)
    draw.rectangle((70, 1085, 82, 1518), fill=accent)
    draw.text((116, 1080), project, font=font(FONT_BOLD, 32), fill=text_color)
    headline_font = font(FONT_SERIF, 44)
    wrapped = wrap_text(draw, headline, headline_font, 970)
    draw.multiline_text((116, 1160), wrapped, font=headline_font, fill=text_color, spacing=17)
    caption_font = font(FONT_SANS, 24)
    caption = wrap_text(draw, caption, caption_font, 950)
    draw.multiline_text((116, 1488), caption, font=caption_font,
                        fill=rgba(WHITE, 165) if dark_panel else GREY, spacing=8)
    page_mark(draw, number, light=dark_panel)
    return save(canvas, f"{number:02d}.jpg")


def make_book_note():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.50, 0.52))
    base = ImageEnhance.Color(base).enhance(0.26)
    base = ImageEnhance.Brightness(base).enhance(0.32)
    base = base.filter(ImageFilter.GaussianBlur(1.4))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(BLACK, 190)))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 28, H), fill=YELLOW)
    draw.rectangle((70, 66, 1172, 1592), outline=rgba(WHITE, 135), width=2)
    draw.text((112, 112), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 27), fill=WHITE)
    draw.text((112, 200), "异规", font=font(FONT_SERIF, 90), fill=WHITE)
    draw.text((340, 230), "INFORMAL", font=font(FONT_SANS, 34), fill=YELLOW)
    draw.rectangle((112, 344, 1125, 357), fill=RED)

    statement = (
        "《异规》把结构从建筑造型之后的技术补丁，改写为设计的第一推动力："
        "规则不必表现为整齐重复，也能藏在偏移、节奏、分形与受力关系之中。"
    )
    statement_font = font(FONT_SERIF, 49)
    draw.multiline_text((112, 442), wrap_text(draw, statement, statement_font, 990),
                        font=statement_font, fill=WHITE, spacing=30)

    draw.rounded_rectangle((112, 1142, 1127, 1418), radius=10, fill=rgba(PAPER, 239))
    draw.text((154, 1184), "ORDER CAN LOOK UNFAMILIAR", font=font(FONT_BOLD, 27), fill=RED)
    detail = "设计不是先画出一个形，再请结构把它撑住；结构关系本身就可以成为空间与形式的发生器。"
    detail_font = font(FONT_SERIF, 35)
    draw.multiline_text((154, 1250), wrap_text(draw, detail, detail_font, 900),
                        font=detail_font, fill=BLACK, spacing=15)
    draw.text((112, 1503), "编辑性概括｜非书中原句", font=font(FONT_SANS, 24), fill=rgba(WHITE, 190))
    page_mark(draw, 6, light=True)
    return save(canvas, "06.jpg")


def make_preview(paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), "#9e9d97")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(image, (x, y))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def main():
    outputs = [make_cover()]
    outputs.append(make_project_page(
        2, "serpentine-2002.jpg", "蛇形画廊展亭 2002", "伦敦｜2002",
        "ALGORITHM / PATTERN",
        "看似随机的交叉线来自一个可重复的方形算法：结构不再藏在表皮后面，而直接成为建筑的图案与空间。",
        "“非规则”不是无规则，而是让另一套秩序浮出表面。",
        (0.48, 0.52), BLUE, False,
    ))
    outputs.append(make_project_page(
        3, "cctv.jpg", "中央电视台总部", "北京｜2012",
        "LOOP / FORCE",
        "两座倾斜塔通过悬挑连成闭环，受力不再沿单一路径下落，而在连续网格中寻找多条传递路线。",
        "当结构成为回路，稳定来自整体协作，而非单个构件。",
        (0.53, 0.48), YELLOW, True,
    ))
    outputs.append(make_project_page(
        4, "orbit.jpg", "安赛乐米塔尔轨道塔", "伦敦｜2012",
        "INSTABILITY / EQUILIBRIUM",
        "红色钢管像一团失去重心的轨迹，却由多层三角网彼此约束；视觉上的不稳定，建立在计算后的平衡之上。",
        "秩序可以隐藏在运动、偏移和不断改变的视角中。",
        (0.50, 0.46), RED, False,
    ))
    outputs.append(make_project_page(
        5, "pedro-ines.jpg", "佩德罗与伊内斯人行桥", "科英布拉｜2006",
        "CUT / CONNECTION",
        "桥面在中央错开并切断惯常的直线，让“连接”本身变成停留、转向与结构张力共同发生的空间。",
        "偏移不是缺陷，而是生成体验与受力逻辑的起点。",
        (0.52, 0.48), GREEN, False,
    ))
    outputs.append(make_book_note())
    make_preview(outputs)
    print("\n".join(str(path) for path in outputs))


if __name__ == "__main__":
    main()
