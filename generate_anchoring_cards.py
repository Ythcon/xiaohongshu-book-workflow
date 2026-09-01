from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "steven-holl-anchoring"
OUT = ROOT / "output" / "steven-holl-anchoring"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
BLACK = "#171817"
WHITE = "#f8f7f1"
PAPER = "#ece9df"
GREY = "#73766f"
RED = "#a52b24"
BLUE = "#526f87"
YELLOW = "#cab35d"
GREEN = "#73806c"

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


def paper_lines(draw, box, color=BLACK, alpha=22, seed=7):
    random.seed(seed)
    x1, y1, x2, y2 = box
    for _ in range(18):
        y = random.randint(y1, y2)
        x = random.randint(x1, max(x1, x2 - 180))
        draw.line((x, y, min(x2, x + random.randint(140, 420)), y), fill=rgba(color, alpha), width=2)
    for i in range(4):
        inset = i * 28
        draw.arc((x1 + inset, y1 + inset, x2 - inset, y2 - inset), 198, 340,
                 fill=rgba(color, alpha + 8), width=2)


def page_mark(draw, number, light=False):
    color = rgba(WHITE, 190) if light else rgba(BLACK, 160)
    draw.text((1165, 1590), f"0{number} / 06", font=font(FONT_SANS, 22), fill=color, anchor="ra")


def save(canvas, name):
    path = OUT / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def authentic_cover():
    # Verified against Douban subject 5336555: 2010 Chinese edition, ISBN 9787561836125.
    return Image.open(SRC / "book-cover-cn.jpg").convert("RGB")


def mount_book(canvas, position, box):
    cover = fit_inside(authentic_cover(), box)
    x, y = position
    shadow_alpha = Image.new("L", (cover.width + 70, cover.height + 70), 0)
    ImageDraw.Draw(shadow_alpha).rounded_rectangle((20, 18, cover.width + 35, cover.height + 35), 6, fill=145)
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(22))
    shadow = Image.new("RGBA", shadow_alpha.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha)
    canvas.alpha_composite(shadow, (x - 8, y - 4))
    mount = Image.new("RGBA", (cover.width + 16, cover.height + 16), rgba(WHITE, 255))
    mount.alpha_composite(cover.convert("RGBA"), (8, 8))
    canvas.alpha_composite(mount, (x, y))


def make_cover():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.5, 0.5))
    base = ImageEnhance.Contrast(base).enhance(1.03)
    canvas = base.convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 24, H), fill=BLACK)
    draw.rounded_rectangle((54, 58, 812, 610), radius=8, fill=rgba(WHITE, 238))
    draw.text((82, 88), "ARCHITECT × BOOK / 09", font=font(FONT_BOLD, 24), fill=RED)
    draw.text((82, 153), "斯蒂文·霍尔", font=font(FONT_BOLD, 38), fill=BLACK)
    draw.text((78, 226), "锚", font=font(FONT_SERIF, 150), fill=BLACK)
    draw.text((290, 300), "ANCHORING", font=font(FONT_SANS, 39), fill=BLUE)
    draw.rectangle((82, 407, 728, 418), fill=RED)
    draw.text((82, 458), "形式不是漂浮的，", font=font(FONT_SERIF, 41), fill=BLACK)
    draw.text((82, 518), "它从场地里长出来。", font=font(FONT_SERIF, 41), fill=BLACK)

    # Always restore the verified real cover after AI compositing.
    mount_book(canvas, (396, 948), (430, 430))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((74, 1388, 1168, 1538), radius=7, fill=rgba(BLACK, 222))
    draw.text((106, 1422), "场地 · 程序 · 材料 · 光线 · 身体经验", font=font(FONT_BOLD, 31), fill=WHITE)
    draw.text((106, 1477), "五种关系，共同把建筑锚定在此时此地", font=font(FONT_SANS, 27), fill=rgba(WHITE, 205))
    page_mark(draw, 1, light=True)
    path = save(canvas, "01.jpg")
    save(canvas, "book-cover-composite.jpg")
    return path


def make_case(number, source, title, meta, keyword, headline, caption,
              focal=(0.5, 0.5), accent=RED, dark=False):
    source_img = Image.open(SRC / source).convert("RGB")
    image = cover_crop(source_img, (W, 1032), focal)
    image = ImageEnhance.Contrast(image).enhance(1.05)
    image = ImageEnhance.Color(image).enhance(0.88)
    panel = BLACK if dark else PAPER
    text_color = WHITE if dark else BLACK

    canvas = Image.new("RGBA", (W, H), panel)
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 168), (0, 0, 0, 80)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=accent)
    draw.rectangle((64, 56, 246, 111), fill=accent)
    draw.text((82, 70), f"CASE 0{number - 1}", font=font(FONT_BOLD, 23), fill=WHITE)
    draw.text((1166, 70), meta, font=font(FONT_SANS, 24), fill=WHITE, anchor="ra")
    draw.rounded_rectangle((66, 893, 594, 974), radius=5, fill=rgba(BLACK, 220))
    draw.text((92, 917), keyword, font=font(FONT_BOLD, 25), fill=accent)

    draw.rectangle((0, 1032, W, H), fill=panel)
    paper_lines(draw, (872, 1050, 1215, 1575), WHITE if dark else BLACK, 11, number * 17)
    draw.rectangle((70, 1084, 82, 1525), fill=accent)
    draw.text((116, 1080), title, font=font(FONT_BOLD, 33), fill=text_color)
    body_font = font(FONT_SERIF, 43)
    draw.multiline_text((116, 1162), wrap_text(draw, headline, body_font, 980),
                        font=body_font, fill=text_color, spacing=18)
    cap_font = font(FONT_SANS, 24)
    cap_color = rgba(WHITE, 165) if dark else GREY
    draw.multiline_text((116, 1482), wrap_text(draw, caption, cap_font, 950),
                        font=cap_font, fill=cap_color, spacing=8)
    page_mark(draw, number, light=dark)
    return save(canvas, f"{number:02d}.jpg")


def make_book_note():
    base = Image.open(SRC / "ai-cover-base.png").convert("RGB")
    base = cover_crop(base, (W, H), (0.5, 0.52))
    base = ImageEnhance.Color(base).enhance(0.28)
    base = ImageEnhance.Brightness(base).enhance(0.37)
    base = base.filter(ImageFilter.GaussianBlur(1.2))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(BLACK, 186)))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 24, H), fill=RED)
    draw.rectangle((70, 66, 1172, 1590), outline=rgba(WHITE, 115), width=2)
    draw.text((112, 112), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 27), fill=WHITE)
    draw.text((112, 190), "锚", font=font(FONT_SERIF, 100), fill=WHITE)
    draw.text((322, 240), "ANCHORING", font=font(FONT_SANS, 33), fill=YELLOW)
    draw.rectangle((112, 344, 1126, 356), fill=RED)

    statement = (
        "《锚》把建筑理解为一种“扎根”的关系：形式不是从风格中抽取，"
        "而是由场地、程序、材料、光线与身体经验共同生成。"
    )
    body_font = font(FONT_SERIF, 53)
    draw.multiline_text((112, 430), wrap_text(draw, statement, body_font, 994),
                        font=body_font, fill=WHITE, spacing=32)

    draw.rounded_rectangle((112, 1116, 1128, 1418), radius=9, fill=rgba(WHITE, 239))
    draw.text((154, 1162), "TO ANCHOR IS TO RELATE", font=font(FONT_BOLD, 28), fill=BLUE)
    detail = "场地不是背景，而是设计的起点；概念不是造型，而是把建筑与具体世界连接起来的方法。"
    detail_font = font(FONT_SERIF, 38)
    draw.multiline_text((154, 1230), wrap_text(draw, detail, detail_font, 900),
                        font=detail_font, fill=BLACK, spacing=18)
    draw.text((112, 1496), "编辑性概括｜非书中原句", font=font(FONT_SANS, 24), fill=rgba(WHITE, 190))
    page_mark(draw, 6, light=True)
    return save(canvas, "06.jpg")


def make_preview(paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), "#aaa9a4")
    for i, path in enumerate(paths):
        img = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(img, (x, y))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def main():
    paths = [make_cover()]
    paths.append(make_case(
        2, "kiasma.png", "奇亚斯玛当代艺术博物馆", "赫尔辛基｜1992–1998",
        "CITY × LANDSCAPE",
        "建筑的曲线同时回应城市几何、芬兰大厦与图奥洛湾；所谓“锚定”，是让多条场地关系在一个形体中交汇。",
        "Kiasma 的名字来自 chiasma：交叉。建筑不是落在城市里的物体，而是城市路径的结。",
        (0.43, 0.54), BLUE, False,
    ))
    paths.append(make_case(
        3, "chapel-st-ignatius.jpg", "圣依纳爵教堂", "西雅图｜1994–1997",
        "SEVEN BOTTLES OF LIGHT",
        "七个不同朝向的采光体对应礼拜程序；光不再是装饰，而是把空间、时间与仪式锚在一起的材料。",
        "彩色反射随云层移动而改变：概念最终要落到身体可以感知的现象上。",
        (0.58, 0.47), YELLOW, True,
    ))
    paths.append(make_case(
        4, "simmons-hall.jpg", "MIT 西蒙斯宿舍", "剑桥｜1999–2002",
        "POROSITY / SPONGE",
        "“海绵”不是表皮图案，而是一整套居住组织：大孔洞引入空气、光与公共活动，小窗则对应每个学生房间。",
        "当结构、采光和集体生活共享同一概念，造型就不再是孤立的结果。",
        (0.50, 0.48), RED, False,
    ))
    paths.append(make_case(
        5, "linked-hybrid.jpg", "北京当代 MOMA", "北京｜2003–2009",
        "OPEN CITY WITHIN A CITY",
        "地面通道与高空连桥把住宅、商业、教育和休闲编成三维公共循环，让封闭住区被重新锚定到城市生活。",
        "建筑群不是九座孤塔，而是一套制造相遇的城市关系。",
        (0.52, 0.45), GREEN, True,
    ))
    paths.append(make_book_note())
    make_preview(paths)
    print(f"Created {len(paths)} cards in {OUT}")


if __name__ == "__main__":
    main()
