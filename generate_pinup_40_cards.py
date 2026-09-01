from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-40"
OUT = ROOT / "output" / "pinup-40"
POST = ROOT / "posts" / "pinup-40" / "post.json"

W, H = 1242, 1660
BLACK = "#090909"
WHITE = "#f7f5ef"
YELLOW = "#ffd400"
CYAN = "#42c8ec"
PINK = "#ff3f8e"
BLUE = "#3156f5"

FONT_REG = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"


DIRECTORY = [
    ("01", "40 HOUSES", "100多位建筑师提名的21世纪住宅新谱系"),
    ("02", "40 OBJECTS", "定义新世纪前25年的40件物品"),
    ("03", "NYC ARCHITECTS", "60多位纽约建筑师的历史群像"),
    ("04", "SOLANGE / SAINT HERON", "音乐、表演、档案与设计共同体"),
    ("05", "YASMEEN LARI", "手艺、公共住宅与赤足社会建筑"),
    ("06", "DOZIE KANU", "从雕塑实践到首个Knoll量产系列"),
    ("07", "IAN SCHRAGER", "夜生活、精品酒店与空间颠覆"),
    ("08", "21ST-CENTURY REPORTS", "设计、建筑、室内、健康与身体"),
    ("09", "PIN–UP PARIS", "Michèle Lamy与Benjamin Paulin"),
    ("10", "BRANZI × TOYO ITO", "Continuous Present特别出版物"),
    ("11", "LIGHT / CHAIR / COMFORT", "Flos、Molteni&C、Poliform与Edra"),
    ("12", "AND MORE", "玻璃、餐厅、地毯、扶手椅与新工作室"),
]

ISSUE_URL = "https://www.pinupmagazine.org/issues/pinup-magazine-40-independence"
HOUSES_URL = "https://www.pinupmagazine.org/articles/pinup-40-40-houses"
LARI_URL = "https://www.pinupmagazine.org/articles/pinup-40-yasmeen-lari-interview"
KANU_URL = "https://www.pinupmagazine.org/articles/dozie-kanu-interview-pin-up-40"
SCHRAGER_URL = "https://www.pinupmagazine.org/articles/ian-schrager-interview-public-west-hollywood-pinup-40"
BRANZI_URL = "https://www.pinupmagazine.org/articles/toyo-ito-andrea-branzi-triennale-milano-continuous-present"
FLOS_URL = "https://www.pinupmagazine.org/articles/flos-lighting-21st-century-pin-up-magazine-40"
NYC_URL = "https://www.pinupmagazine.org/articles/nyc-architects-pin-up-40"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def cover_crop(image: Image.Image, size: tuple[int, int], focal=(0.5, 0.5)) -> Image.Image:
    tw, th = size
    scale = max(tw / image.width, th / image.height)
    nw, nh = round(image.width * scale), round(image.height * scale)
    image = image.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, round(nw * focal[0] - tw / 2)))
    top = max(0, min(nh - th, round(nh * focal[1] - th / 2)))
    return image.crop((left, top, left + tw, top + th))


def fit_inside(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = min(size[0] / image.width, size[1] / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


def grade(image: Image.Image, *, color=0.96, contrast=1.08, brightness=0.96) -> Image.Image:
    image = ImageEnhance.Color(image).enhance(color)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    return ImageEnhance.Brightness(image).enhance(brightness)


def wrap(draw: ImageDraw.ImageDraw, text: str, used_font, width: int) -> str:
    lines: list[str] = []
    for paragraph in text.splitlines():
        current = ""
        for char in paragraph:
            trial = current + char
            if current and draw.textbbox((0, 0), trial, font=used_font)[2] > width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
    return "\n".join(lines)


def draw_wrapped(draw, xy, text, width, size, fill, *, bold=False, spacing=8):
    used = font(size, bold)
    draw.multiline_text(xy, wrap(draw, text, used, width), font=used, fill=fill, spacing=spacing)


def image_panel(canvas: Image.Image, name: str, box: tuple[int, int, int, int], *,
                focal=(0.5, 0.5), border=0, border_color=WHITE, label: str | None = None,
                darken=1.0) -> None:
    x0, y0, x1, y1 = box
    source = Image.open(SRC / name).convert("RGB")
    source = grade(cover_crop(source, (x1 - x0, y1 - y0), focal), brightness=darken)
    canvas.alpha_composite(source.convert("RGBA"), (x0, y0))
    draw = ImageDraw.Draw(canvas)
    if border:
        draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=border_color, width=border)
    if label:
        used = font(15, True)
        tw = draw.textbbox((0, 0), label, font=used)[2]
        draw.rectangle((x0 + 12, y1 - 42, x0 + tw + 34, y1 - 12), fill=rgba(BLACK, 225))
        draw.text((x0 + 23, y1 - 27), label, font=used, fill=WHITE, anchor="lm")


def draw_meta(draw: ImageDraw.ImageDraw, number: int, accent=YELLOW) -> None:
    draw.rectangle((0, 0, W, 54), fill=BLACK)
    draw.text((34, 27), "PIN–UP 40 / INDEPENDENCE", font=font(18, True), fill=WHITE, anchor="lm")
    draw.rectangle((1030, 0, W, 54), fill=accent)
    draw.text((1136, 27), f"{number:02d} / 10", font=font(19, True), fill=BLACK, anchor="mm")


def draw_source(draw: ImageDraw.ImageDraw, text: str, *, light=True) -> None:
    bg = rgba(BLACK, 236) if light else rgba(WHITE, 242)
    fg = WHITE if light else BLACK
    draw.rectangle((0, 1601, W, H), fill=bg)
    draw.text((34, 1631), text, font=font(15), fill=fg, anchor="lm")


def impact_lines(draw: ImageDraw.ImageDraw, lines: list[str], x: int, y: int, size: int,
                 accent: str, *, max_width=1000, gap=5) -> int:
    used = font(size, True)
    for idx, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=used)
        tw = min(max_width, bbox[2] - bbox[0])
        th = bbox[3] - bbox[1]
        bg = accent if idx == 1 else BLACK
        fg = BLACK if idx == 1 else WHITE
        draw.rectangle((x, y, x + tw + 40, y + th + 28), fill=bg)
        draw.text((x + 18, y + 7), line, font=used, fill=fg)
        y += th + 28 + gap
    return y


def save(image: Image.Image, number: int) -> Path:
    path = OUT / f"{number:02d}.jpg"
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    cover = Image.open(SRC / "book-cover.jpg").convert("RGB")
    cover = fit_inside(cover, (1110, 1030))
    shadow = Image.new("RGBA", (cover.width + 70, cover.height + 70), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle((35, 35, cover.width + 35, cover.height + 35), fill=rgba(BLACK, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    canvas.alpha_composite(shadow, (40, 6))
    canvas.alpha_composite(cover.convert("RGBA"), ((W - cover.width) // 2, 38))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 28, 1075), fill=CYAN)
    draw.text((1180, 102), "40", font=font(170, True), fill=rgba(CYAN, 230), anchor="ra")
    draw.rectangle((0, 1072, W, H), fill=YELLOW)
    draw.text((42, 1122), "独立不是", font=font(124, True), fill=BLACK)
    draw.text((42, 1282), "一种风格", font=font(124, True), fill=BLACK)
    draw.rectangle((42, 1472, 1168, 1484), fill=PINK)
    draw.text((44, 1528), "PIN–UP 40 / INDEPENDENCE / S/S 2026", font=font(21, True), fill=BLACK)
    draw.text((1170, 1528), "01 / 10", font=font(21, True), fill=BLACK, anchor="ra")
    draw_source(draw, "PIN–UP 40 官方封面｜20周年收藏盒｜S/S 2026", light=False)
    return save(canvas, 1)


def make_directory() -> Path:
    bg = Image.open(SRC / "03-40-houses-detail.jpg").convert("RGB")
    bg = grade(cover_crop(bg, (W, H)), color=0.55, contrast=1.16, brightness=0.78)
    canvas = bg.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(BLUE, 214)))
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 2, YELLOW)
    draw.text((38, 80), "目录", font=font(126, True), fill=WHITE)
    draw.text((1164, 116), "CONTENTS", font=font(43, True), fill=YELLOW, anchor="ra")
    draw.text((1164, 170), "本期中文导览", font=font(23, True), fill=WHITE, anchor="ra")
    draw.line((40, 238, 1166, 238), fill=YELLOW, width=8)
    for idx, (num, title, desc) in enumerate(DIRECTORY):
        col = 0 if idx < 6 else 1
        row = idx if idx < 6 else idx - 6
        x = 40 if col == 0 else 640
        y = 284 + row * 194
        draw.text((x, y), num, font=font(26, True), fill=YELLOW)
        draw.text((x + 72, y), title, font=font(24, True), fill=WHITE)
        draw_wrapped(draw, (x + 72, y + 46), desc, 500, 21, WHITE, spacing=5)
        draw.line((x, y + 148, x + 540, y + 148), fill=rgba(WHITE, 92), width=2)
    draw.rectangle((40, 1484, 1166, 1570), fill=YELLOW)
    draw.text((66, 1527), "一盒十册：用房屋、物品、人物与文化重新盘点21世纪", font=font(27, True), fill=BLACK, anchor="lm")
    draw_source(draw, "PIN–UP 40 官方期号页｜中文编辑整理", light=True)
    return save(canvas, 2)


def make_houses() -> Path:
    canvas = Image.new("RGBA", (W, H), CYAN)
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 3, YELLOW)
    image_panel(canvas, "03-houses-canon-a.jpg", (36, 86, 826, 1028), border=4,
                label="VILLA VALS / CAPITAL HILL / WALL HOUSE / CASA VENTURA")
    image_panel(canvas, "03-houses-canon-b.jpg", (850, 86, 1206, 548), border=4,
                label="NAUTILUS / VAULT / INFINITE")
    image_panel(canvas, "03-houses-antivilla-ishigami.jpg", (850, 572, 1206, 1028), border=4,
                label="ANTIVILLA / HOUSE + RESTAURANT")
    draw.text((28, 1430), "40", font=font(505, True), fill=rgba(WHITE, 72), anchor="ls")
    impact_lines(draw, ["住宅不是", "宣言", "是协商"], 38, 1058, 70, YELLOW, max_width=600)
    draw.rectangle((690, 1080, 1206, 1554), fill=BLACK)
    draw_wrapped(draw, (724, 1118),
                 "100多位建筑师共同提名40座住宅。它们没有统一样式，却都在重新处理隐私、预算、气候、材料与日常生活。所谓‘新经典’，不是一种审美答案，而是一组仍可争论的选择。",
                 445, 25, WHITE, bold=True, spacing=10)
    draw.rectangle((724, 1460, 1128, 1514), fill=YELLOW)
    draw.text((744, 1487), "6座案例 / 3组官方出版图", font=font(20, True), fill=BLACK, anchor="lm")
    draw_source(draw, "Luke Libera Moore for PIN–UP｜40 HOUSES｜PIN–UP 40", light=True)
    return save(canvas, 3)


def make_lari() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    image_panel(canvas, "04-lari-zero-carbon.jpg", (0, 54, W, 770), focal=(0.5, 0.48), darken=0.91,
                label="ZERO CARBON CULTURAL CENTER / BAMBOO PAVILION")
    image_panel(canvas, "04-yasmeen-lari.jpg", (36, 806, 392, 1322), focal=(0.58, 0.50), border=4,
                label="YASMEEN LARI")
    image_panel(canvas, "04-lari-angoori-bagh.jpg", (416, 806, 792, 1322), focal=(0.52, 0.45), border=4,
                label="ANGOORI BAGH / 1973")
    image_panel(canvas, "04-lari-chulah.jpg", (816, 806, 1206, 1322), focal=(0.5, 0.48), border=4,
                label="PAKISTAN CHULAH")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 4, YELLOW)
    impact_lines(draw, ["建筑要", "回到", "社区"], 42, 170, 88, YELLOW, max_width=520)
    draw.rectangle((36, 1350, 1206, 1574), fill=YELLOW)
    draw_wrapped(draw, (70, 1380),
                 "从1973年的低成本公共住宅，到竹构零碳文化中心与可自行建造的无烟炉：Lari把建筑从‘作品’改写成知识、资源和尊严的分配方式。",
                 1100, 29, BLACK, bold=True, spacing=9)
    draw_source(draw, "Heritage Foundation of Pakistan｜肖像 Arif Mahmood｜PIN–UP 40", light=True)
    return save(canvas, 4)


def make_kanu() -> Path:
    canvas = Image.new("RGBA", (W, H), PINK)
    image_panel(canvas, "05-kanu-knoll-table.jpg", (0, 54, 760, 1090), focal=(0.50, 0.49), darken=0.93)
    image_panel(canvas, "05-kanu-chair-xi.jpg", (784, 86, 1206, 562), focal=(0.5, 0.50), border=4,
                label="CHAIR [XI] / STUDIO MUSEUM")
    image_panel(canvas, "05-kanu-knoll-pavilion.jpg", (784, 586, 1206, 1090), focal=(0.50, 0.48), border=4,
                label="KNOLL PAVILION / 2026")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 5, CYAN)
    impact_lines(draw, ["量产", "也能有", "个人历史"], 38, 772, 75, CYAN, max_width=660)
    draw.rectangle((36, 1130, 1206, 1570), fill=BLACK)
    draw.text((70, 1170), "从雕塑诱饵到家具系统", font=font(34, True), fill=PINK)
    draw_wrapped(draw, (70, 1232),
                 "Kanu把熟悉的桌椅当作‘概念诱饵’：Studio Museum的Chair [XI]让家具进入装置；首个Knoll量产系列则用钢管、皮革流苏与三种尺度，把休斯敦成长经验和非洲面具纤维意象压进工业结构。",
                 1090, 27, WHITE, bold=True, spacing=10)
    draw_source(draw, "Adam Reich / Cedric Mussano / Daniele Ansidei｜DOZIE KANU｜PIN–UP 40", light=True)
    return save(canvas, 5)


def make_schrager() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    image_panel(canvas, "06-schrager-delano.jpg", (0, 54, W, 796), focal=(0.5, 0.48), darken=0.87,
                label="DELANO MIAMI BEACH / PHILIPPE STARCK / 1994")
    image_panel(canvas, "06-schrager-palladium.jpg", (36, 834, 600, 1288), focal=(0.50, 0.49), border=4,
                label="PALLADIUM / KENNY SCHARF ROOM")
    image_panel(canvas, "06-schrager-st-martins.jpg", (624, 834, 1206, 1288), focal=(0.51, 0.48), border=4,
                label="ST MARTINS LANE / 1999")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 6, CYAN)
    impact_lines(draw, ["氛围", "先于", "房间"], 42, 190, 98, CYAN, max_width=500)
    draw.rectangle((36, 1318, 1206, 1572), fill=CYAN)
    draw_wrapped(draw, (70, 1350),
                 "从Palladium的艺术房间，到Delano的光幕大厅，再到可遥控彩光的St Martins Lane：Schrager把酒店从住宿容器变成一场被灯光、艺术与社交行为共同编排的事件。",
                 1090, 28, BLACK, bold=True, spacing=9)
    draw_source(draw, "Ian Schrager Company｜Palladium摄影 Tim Hursley｜PIN–UP 40", light=True)
    return save(canvas, 6)


def make_branzi() -> Path:
    canvas = Image.new("RGBA", (W, H), YELLOW)
    image_panel(canvas, "07-branzi-install-a.jpg", (0, 54, W, 788), focal=(0.51, 0.50), darken=0.89,
                label="CONTINUOUS PRESENT / TRIENNALE MILANO")
    image_panel(canvas, "07-branzi-install-b.jpg", (36, 826, 606, 1298), focal=(0.50, 0.50), border=4,
                label="INSTALLATION VIEW 01")
    image_panel(canvas, "07-branzi-install-c.jpg", (630, 826, 1206, 1298), focal=(0.52, 0.50), border=4,
                label="INSTALLATION VIEW 02")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 7, PINK)
    impact_lines(draw, ["过去", "不必", "排队"], 42, 165, 96, PINK, max_width=490)
    draw.rectangle((36, 1328, 1206, 1572), fill=BLACK)
    draw_wrapped(draw, (70, 1360),
                 "Toyo Ito没有把Andrea Branzi六十年的实践排成时间线，而是让理论、物件、模型与城市景观在流动空间里同时发生：档案不是终点，而是一种持续生成的现在。",
                 1090, 28, WHITE, bold=True, spacing=9)
    draw_source(draw, "Andrea Rossetti © Triennale Milano｜Andrea Branzi by Toyo Ito｜PIN–UP 40", light=True)
    return save(canvas, 7)


def make_flos() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 8, YELLOW)
    draw.text((38, 90), "光", font=font(154, True), fill=YELLOW)
    draw.text((244, 124), "是材料", font=font(76, True), fill=WHITE)
    draw.text((1168, 142), "FLOS / 21ST CENTURY", font=font(22, True), fill=CYAN, anchor="ra")
    image_panel(canvas, "08-flos-noctambule.jpg", (36, 266, 398, 1288), focal=(0.5, 0.48), border=4,
                label="NOCTAMBULE / GRCIC")
    image_panel(canvas, "08-flos-luce.jpg", (418, 266, 798, 1288), focal=(0.5, 0.48), border=4,
                label="LUCE / BOUROULLEC")
    image_panel(canvas, "08-flos-hooo.jpg", (818, 266, 1206, 1288), focal=(0.5, 0.48), border=4,
                label="HOOO!!! / STARCK + HOLZER")
    draw.rectangle((36, 1320, 1206, 1572), fill=YELLOW)
    draw_wrapped(draw, (70, 1350),
                 "从透明玻璃柱、可转动调光的模块系统，到Jenny Holzer文字穿过水晶灯体：技术只有在改变光的气氛、触感与使用方式时，才真正成为设计。",
                 1090, 29, BLACK, bold=True, spacing=9)
    draw_source(draw, "Nicolas Polli for PIN–UP 40｜FLOS: LIGHTING THE 21ST CENTURY", light=True)
    return save(canvas, 8)


def make_nyc() -> Path:
    canvas = Image.new("RGBA", (W, H), CYAN)
    image_panel(canvas, "09-nyc-architects-main.jpg", (0, 54, W, 738), focal=(0.50, 0.50), darken=0.90,
                label="60+ NYC ARCHITECTS / ABRONS ARTS CENTER")
    image_panel(canvas, "09-nyc-architects-a.jpg", (36, 776, 606, 1272), focal=(0.5, 0.50), border=4,
                label="THE OBSERVERS / PORTRAIT 01")
    image_panel(canvas, "09-nyc-architects-b.jpg", (630, 776, 1206, 1272), focal=(0.5, 0.50), border=4,
                label="THE OBSERVERS / PORTRAIT 02")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 9, YELLOW)
    impact_lines(draw, ["观察者", "坐进", "画面"], 42, 164, 84, YELLOW, max_width=600)
    draw.rectangle((36, 1306, 1206, 1572), fill=BLACK)
    draw_wrapped(draw, (70, 1338),
                 "PIN–UP把20年间出现过的60多位纽约建筑师聚到1915年落成的Abrons Arts Center，并让他们坐在观众席：惯于观察城市的人，这一次成为被观察的对象。",
                 1090, 28, WHITE, bold=True, spacing=9)
    draw_source(draw, "Lucas Creighton for PIN–UP 40｜与 The World Around 合作", light=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    image_panel(canvas, "book-cover.jpg", (0, 54, 510, 1601), focal=(0.50, 0.50), darken=0.82)
    image_panel(canvas, "03-houses-canon-a.jpg", (530, 54, 1242, 530), focal=(0.50, 0.50), darken=0.82,
                label="HOUSES")
    image_panel(canvas, "05-kanu-knoll-table.jpg", (530, 550, 874, 1120), focal=(0.50, 0.49), darken=0.82,
                label="OBJECTS")
    image_panel(canvas, "08-flos-noctambule.jpg", (894, 550, 1242, 1120), focal=(0.50, 0.48), darken=0.82,
                label="LIGHT")
    image_panel(canvas, "09-nyc-architects-main.jpg", (530, 1140, 1242, 1601), focal=(0.50, 0.50), darken=0.80,
                label="PEOPLE")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 10, PINK)
    draw.rectangle((80, 558, 1160, 994), fill=rgba(YELLOW, 242))
    draw.text((118, 606), "独立不是", font=font(92, True), fill=BLACK)
    draw.text((118, 732), "一种风格", font=font(92, True), fill=BLACK)
    draw.rectangle((118, 876, 1090, 888), fill=PINK)
    draw.text((118, 925), "而是一套选择机制", font=font(43, True), fill=BLACK)
    draw.rectangle((80, 1016, 1160, 1100), fill=BLACK)
    draw.text((620, 1058), "房屋 × 物品 × 人物 × 文化", font=font(28, True), fill=WHITE, anchor="mm")
    draw_source(draw, "PIN–UP 40 官方图像编辑｜HOUSES / OBJECTS / LIGHT / PEOPLE", light=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#b7b6b1")
    for idx, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (idx % 5) * (tw + gap), gap + (idx // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 40｜21世纪设计看什么？"
    body = (
        "当风格越来越碎片化，我们判断一件建筑或设计是否重要，不能只看它‘像什么’。\n\n"
        "PIN–UP 40《Independence》干脆把20周年做成一盒十册：主刊之外，还有40 Houses、40 Objects、NYC Architects，以及Andrea Branzi × Toyo Ito等特别出版物。它不急着给21世纪贴标签，而是把住宅、家具、酒店、灯具、展览和文化人物放在一起重新比较。\n\n"
        "100多位建筑师共同提名的40 Houses，让经典不再由单一权威决定。Yasmeen Lari从低成本公共住宅走向零碳竹构，让建筑变成社区能够自行掌握的建造方法。\n\n"
        "Dozie Kanu把个人成长经验藏进Knoll量产家具，证明工业生产不等于抹去身份。Ian Schrager则用Palladium、Delano和St Martins Lane说明，灯光、艺术与社交行为本身就是空间。\n\n"
        "Flos追踪光与技术的变化，NYC Architects把60多位城市观察者送进镜头。不同尺度、不同人物，却都在回答同一个问题：设计如何进入生活，并改变人与物、人与空间之间的关系。\n\n"
        "我最喜欢这期的一点，是它不急着给答案。判断作品是否重要，可以从三件事开始：它重新组织了哪些关系、改变了谁的生活、又留下了哪些争论。\n\n"
        "如果只能把一个案例放进你的21世纪设计清单，你会选哪一个？"
    )
    tags = "#PINUP #PINUP40 #建筑杂志 #建筑设计 #空间设计 #家具设计 #当代建筑 #独立出版"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")

    sources = f"""# PIN–UP 40 图片与内容来源

- 第01、02、10页：PIN–UP 40 官方期号页 {ISSUE_URL}
- 第03页 40 Houses：{HOUSES_URL}；摄影 Luke Libera Moore，封面摄影 Eric Staudenmaier
- 第04页 Yasmeen Lari：{LARI_URL}；项目图 Heritage Foundation of Pakistan，肖像 Arif Mahmood
- 第05页 Dozie Kanu：{KANU_URL}；摄影 Adam Reich、Cedric Mussano、Daniele Ansidei
- 第06页 Ian Schrager：{SCHRAGER_URL}；档案 Ian Schrager Company，Palladium 摄影 Tim Hursley
- 第07页 Andrea Branzi × Toyo Ito：{BRANZI_URL}；摄影 Andrea Rossetti © Triennale Milano
- 第08页 Flos：{FLOS_URL}；摄影 Nicolas Polli for PIN–UP 40
- 第09页 NYC Architects：{NYC_URL}；摄影 Lucas Creighton for PIN–UP 40

所有新增图像均来自 PIN–UP 官方第40期页面或官方文章，并按原文项目名称与摄影署名记录。
版权：图片版权归 PIN–UP、原摄影师及项目权利方所有；本文件仅作内容编辑与发布前来源记录。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")

    manifest = {
        "type": "magazine",
        "slug": "pinup-40",
        "issue": "PIN–UP 40 · INDEPENDENCE",
        "date": "2026春夏刊｜独立出版20周年",
        "core_question": "当一个时代没有统一风格，谁来决定什么值得被记住？",
        "core_thesis": "独立不是一种风格，而是一套选择、组织与争论的机制。",
        "pages": [
            "01 单期主线：独立不是一种风格",
            "02 中文目录：主刊与九册特别出版物",
            "03 40 Houses：六座案例进入新住宅谱系",
            "04 Yasmeen Lari：从公共住宅到零碳社会建筑",
            "05 Dozie Kanu：雕塑语言进入Knoll量产家具",
            "06 Ian Schrager：三组酒店与夜生活空间案例",
            "07 Andrea Branzi × Toyo Ito：展览现场与连续现在",
            "08 Flos：三件21世纪灯具案例",
            "09 NYC Architects：60多位建筑师历史群像",
            "10 总结：房屋、物品、人物与文化",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_directory(), make_houses(), make_lari(), make_kanu(),
        make_schrager(), make_branzi(), make_flos(), make_nyc(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP cards in {OUT}")


if __name__ == "__main__":
    main()
