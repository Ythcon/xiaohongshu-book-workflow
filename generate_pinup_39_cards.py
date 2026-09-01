from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-39"
OUT = ROOT / "output" / "pinup-39"
POST = ROOT / "posts" / "pinup-39" / "post.json"

W, H = 1242, 1660
BLACK = "#12110f"
WHITE = "#f5f1e8"
PAPER = "#e9e2d5"
RED = "#d83c2f"
ORANGE = "#f17632"
BLUE = "#2b65d9"
GREEN = "#1e6650"
PINK = "#ea7b98"

FONT_REG = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"

ISSUE_URL = "https://www.pinupmagazine.org/issues/pinup-magazine-39-frida-escobedo-domesticity-wolfgang-tillmans"
EDITOR_URL = "https://www.pinupmagazine.org/articles/pinup-39-domesticity-editors-letter-frida-escobedo"
FRIDA_SAM_URL = "https://www.pinupmagazine.org/articles/frida-escobedo-sam-chermayeff-interview"
SAM_URL = "https://www.pinupmagazine.org/articles/sam-chermayeff"
BILBAO_URL = "https://www.pinupmagazine.org/articles/tatiana-bilbao-interview"
LINA_URL = "https://www.pinupmagazine.org/articles/lina-ghotmeh-interview"
TOPHAT_URL = "https://www.pinupmagazine.org/articles/top-hat-blum-house-water-island-roger-ferri-charlie-porter"
JOSE_URL = "https://www.pinupmagazine.org/articles/jose-leon-cerrillo-mexico-city-pinup-magazine"
TERTULIA_URL = "https://www.pinupmagazine.org/articles/frida-escobedo-tertulia-pin-up-39"
PIET_URL = "https://www.pinupmagazine.org/articles/piet-oudolf-interview"
MET_URL = "https://www.pinupmagazine.org/articles/period-rooms-metropolitan-museum-of-art"

CONTENTS = [
    ("01", "FRIDA ESCOBEDO × SAM CHERMAYEFF", "隐私、童年与理想沙发"),
    ("02", "LINA GHOTMEH", "手艺、考古与建筑的记忆"),
    ("03", "TATIANA BILBAO", "住宅不是四面墙，而是照护"),
    ("04", "PIET OUDOLF", "四季种植与日常的花园"),
    ("05", "DOMESTIC LABOR", "谁做饭，谁清洁，谁被看见"),
    ("06", "SAM CHERMAYEFF", "挑战私密与舒适的默认设置"),
    ("07", "TOP-HAT HOUSE", "海岛上的后现代住宅修复"),
    ("08", "JOSÉ LEÓN CERRILLO", "墨西哥城联排住宅里的艺术生活"),
    ("09", "SHEILA HICKS / THE MET / STOREFRONT", "纺织、室内与公共文化"),
    ("10", "FRIDA'S TERTULIA", "墨西哥城的创作共同体"),
    ("11", "PETER SAVILLE / FIRE ISLAND", "图像、家与流行文化"),
    ("12", "AND MORE", "材料、花园、厨房、身体与共居"),
]


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


def grade(image: Image.Image, *, color=0.95, contrast=1.06, brightness=0.97) -> Image.Image:
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


def image_panel(canvas: Image.Image, name: str, box: tuple[int, int, int, int], *, focal=(0.5, 0.5),
                border=0, border_color=WHITE, label: str | None = None, darken=1.0) -> None:
    x0, y0, x1, y1 = box
    img = Image.open(SRC / name).convert("RGB")
    img = grade(cover_crop(img, (x1 - x0, y1 - y0), focal), brightness=darken)
    canvas.alpha_composite(img.convert("RGBA"), (x0, y0))
    draw = ImageDraw.Draw(canvas)
    if border:
        draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=border_color, width=border)
    if label:
        used = font(15, True)
        tw = draw.textbbox((0, 0), label, font=used)[2]
        draw.rectangle((x0 + 12, y1 - 42, x0 + tw + 34, y1 - 12), fill=rgba(BLACK, 226))
        draw.text((x0 + 23, y1 - 27), label, font=used, fill=WHITE, anchor="lm")


def draw_meta(draw: ImageDraw.ImageDraw, number: int, accent=RED) -> None:
    draw.rectangle((0, 0, W, 54), fill=BLACK)
    draw.text((34, 27), "PIN–UP 39 / DOMESTICITY", font=font(18, True), fill=WHITE, anchor="lm")
    draw.rectangle((1030, 0, W, 54), fill=accent)
    draw.text((1136, 27), f"{number:02d} / 10", font=font(19, True), fill=BLACK, anchor="mm")


def draw_source(draw: ImageDraw.ImageDraw, text: str, *, light=True) -> None:
    draw.rectangle((0, 1601, W, H), fill=rgba(BLACK if light else WHITE, 238))
    draw.text((34, 1631), text, font=font(15), fill=WHITE if light else BLACK, anchor="lm")


def impact(draw, lines: list[str], x: int, y: int, size: int, accent: str, *, max_width=900, gap=5) -> int:
    used = font(size, True)
    for idx, line in enumerate(lines):
        box = draw.textbbox((0, 0), line, font=used)
        tw, th = min(max_width, box[2] - box[0]), box[3] - box[1]
        bg = accent if idx == 1 else BLACK
        fg = BLACK if idx == 1 else WHITE
        draw.rectangle((x, y, x + tw + 40, y + th + 30), fill=bg)
        draw.text((x + 18, y + 8), line, font=used, fill=fg)
        y += th + 30 + gap
    return y


def save(image: Image.Image, number: int) -> Path:
    path = OUT / f"{number:02d}.jpg"
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    cover = fit_inside(Image.open(SRC / "book-cover.jpg").convert("RGB"), (730, 1120))
    shadow = Image.new("RGBA", (cover.width + 80, cover.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((40, 40, cover.width + 40, cover.height + 40), fill=rgba(BLACK, 155))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)), (442, 86))
    canvas.alpha_composite(cover.convert("RGBA"), (472, 86))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 52, H), fill=RED)
    draw.text((92, 132), "家", font=font(210, True), fill=RED)
    draw.text((94, 332), "不是", font=font(112, True), fill=BLACK)
    draw.text((94, 468), "私有容器", font=font(112, True), fill=BLACK)
    draw.rectangle((94, 646, 440, 660), fill=BLUE)
    draw_wrapped(draw, (96, 708), "它把照护、劳动、共居与安全，一起装进日常。", 340, 36, BLACK, bold=True, spacing=12)
    draw.text((94, 1450), "PIN–UP 39", font=font(30, True), fill=RED)
    draw.text((94, 1496), "DOMESTICITY / F/W 2025/26", font=font(20, True), fill=BLACK)
    draw.text((1174, 1545), "01 / 10", font=font(20, True), fill=BLACK, anchor="ra")
    draw_source(draw, "PIN–UP 39 官方封面｜Guest-edited by Frida Escobedo", light=False)
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), GREEN)
    image_panel(canvas, "02-piet-hummelo.jpg", (640, 54, W, H), focal=(0.50, 0.50), darken=0.76)
    canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, 680, H), fill=rgba(GREEN, 244))
    draw_meta(draw, 2, ORANGE)
    draw.text((38, 92), "目录", font=font(128, True), fill=WHITE)
    draw.text((38, 232), "DOMESTICITY", font=font(28, True), fill=ORANGE)
    for idx, (num, title, desc) in enumerate(CONTENTS):
        x = 40 if idx < 6 else 354
        y = 308 + (idx if idx < 6 else idx - 6) * 192
        draw.text((x, y), num, font=font(22, True), fill=ORANGE)
        draw.text((x, y + 32), title, font=font(17, True), fill=WHITE)
        draw_wrapped(draw, (x, y + 62), desc, 268, 18, WHITE, spacing=5)
        draw.line((x, y + 142, x + 270, y + 142), fill=rgba(WHITE, 95), width=2)
    draw.rectangle((38, 1490, 603, 1568), fill=ORANGE)
    draw.text((62, 1530), "Frida Escobedo 客座编辑", font=font(25, True), fill=BLACK, anchor="lm")
    draw_source(draw, "Wolfgang Tillmans｜Frida Escobedo｜PIN–UP 39", light=True)
    draw.rectangle((38, 1490, 603, 1568), fill=ORANGE)
    draw.text((62, 1530), "12 篇，从房间到花园", font=font(25, True), fill=BLACK, anchor="lm")
    draw_source(draw, "Piet Oudolf / Hummelo Garden｜PIN–UP 39", light=True)
    return save(canvas, 2)


def make_period_rooms() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    image_panel(canvas, "03-met-little-house.jpg", (0, 54, 742, 1018), focal=(0.50, 0.49), darken=0.90,
                label="FRANCIS W. LITTLE HOUSE / 1912–14")
    image_panel(canvas, "03-met-worsham.jpg", (776, 86, 1204, 594), focal=(0.50, 0.45), border=4,
                label="WORSHAM-ROCKEFELLER DRESSING ROOM")
    image_panel(canvas, "03-met-swiss.jpg", (776, 628, 1204, 1018), focal=(0.50, 0.50), border=4,
                label="SWISS ROOM / PERIOD ROOMS")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 3, ORANGE)
    draw.rectangle((0, 1052, W, 1601), fill=PAPER)
    impact(draw, ["室内", "不是", "标本"], 40, 1086, 90, ORANGE, max_width=440)
    draw.rectangle((636, 1086, 1204, 1558), fill=ORANGE)
    draw_wrapped(draw, (678, 1130), "大都会艺术博物馆的历史房间，不是把旧生活原封不动地搬进来。建筑被拆卸、运输、重组；家具被选择、放置，甚至暂时撤空。所谓保存，也是在为今天重新编排空间。", 470, 31, BLACK, bold=True, spacing=11)
    draw_source(draw, "The Metropolitan Museum of Art / Period Rooms｜PIN–UP 39", light=True)
    return save(canvas, 3)


def make_frida() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    image_panel(canvas, "03-frida-portrait-a.jpg", (0, 54, 730, H), focal=(0.54, 0.48), darken=0.88)
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 3, RED)
    draw.rectangle((762, 94, 1202, 484), fill=RED)
    draw.text((800, 134), "DOMESTICITY", font=font(27, True), fill=BLACK)
    draw_wrapped(draw, (800, 202), "当家的尺度被放大，它其实藏着劳动分配、照护网络、共居规则与安全感。", 348, 37, BLACK, bold=True, spacing=13)
    impact(draw, ["家里", "也有", "世界"], 760, 566, 94, ORANGE, max_width=420)
    draw.rectangle((760, 1012, 1204, 1452), fill=WHITE)
    draw_wrapped(draw, (798, 1056), "Escobedo以‘Domesticity’重看从独栋住宅到混合用途住宅塔楼的日常：厨房、客厅和度假屋都能暴露更大的社会关系。", 360, 27, BLACK, bold=True, spacing=10)
    draw_source(draw, "Wolfgang Tillmans｜Frida Escobedo｜PIN–UP 39", light=True)
    return save(canvas, 3)


def make_sam() -> Path:
    canvas = Image.new("RGBA", (W, H), BLUE)
    image_panel(canvas, "04-sam-baugruppe.jpg", (0, 54, W, 786), focal=(0.50, 0.50), darken=0.91,
                label="BAUGRUPPE KURFÜRSTENSTRASSE 142 / BERLIN")
    image_panel(canvas, "04-sam-triangle-kitchen.jpg", (38, 824, 620, 1296), focal=(0.52, 0.50), border=4,
                label="TRIANGLE KITCHEN / 2023")
    image_panel(canvas, "04-sam-portrait-a.jpg", (646, 824, 1204, 1296), focal=(0.50, 0.52), border=4,
                label="SAM AT HOME / BERLIN")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 4, ORANGE)
    impact(draw, ["隐私", "不是", "默认值"], 42, 176, 94, ORANGE, max_width=500)
    draw.rectangle((38, 1332, 1204, 1572), fill=BLACK)
    draw_wrapped(draw, (72, 1364), "Chermayeff住在自己设计的半公共住宅里，也把厨房压缩成一件三角装置：空间不必把人分开，反而可以用尺度与动线制造相遇。", 1090, 29, WHITE, bold=True, spacing=9)
    draw_source(draw, "Oliver Helbig｜Sam Chermayeff｜PIN–UP 39", light=True)
    return save(canvas, 4)


def make_bilbao() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "05-bilbao-casa-ajijic.jpg", (0, 54, W, 860), focal=(0.50, 0.48), darken=0.94,
                label="CASA AJIJIC / 2010 / EARTH WALLS")
    image_panel(canvas, "05-bilbao-xola.jpg", (38, 900, 604, 1302), focal=(0.50, 0.48), border=4,
                label="XOLA / AFFORDABLE HOUSING")
    image_panel(canvas, "05-bilbao-table.jpg", (630, 900, 1204, 1302), focal=(0.50, 0.50), border=4,
                label="¿MESA PARA CUÁNTOS?")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 5, GREEN)
    impact(draw, ["住宅", "是一种", "照护"], 40, 194, 92, GREEN, max_width=500)
    draw.rectangle((38, 1336, 1204, 1572), fill=GREEN)
    draw_wrapped(draw, (72, 1368), "从就地取材的Casa Ajijic，到把艺术馆引入可负担住房的Xola，Bilbao把住宅看作一套能容纳身体、家庭与公共生活的支持系统。", 1080, 29, WHITE, bold=True, spacing=9)
    draw_source(draw, "Iwan Baan / Tatiana Bilbao ESTUDIO｜PIN–UP 39", light=True)
    return save(canvas, 5)


def make_lina() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    image_panel(canvas, "06-lina-stone-garden.jpg", (0, 54, 694, H), focal=(0.50, 0.46), darken=0.84)
    image_panel(canvas, "06-lina-hermes.jpg", (724, 86, 1204, 620), focal=(0.50, 0.47), border=4,
                label="HERMÈS WORKSHOPS / NORMANDY")
    image_panel(canvas, "06-lina-serpentine.jpg", (724, 650, 1204, 1082), focal=(0.50, 0.50), border=4,
                label="À TABLE / SERPENTINE 2023")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 6, ORANGE)
    impact(draw, ["材料", "记得", "生活"], 722, 114, 83, ORANGE, max_width=430)
    draw.rectangle((724, 1116, 1204, 1532), fill=ORANGE)
    draw_wrapped(draw, (758, 1152), "Stone Garden的刻痕混凝土把贝鲁特的战后记忆带进住宅；低碳工坊与可拆卸的À Table，则把手艺、欢迎和共同进餐变成空间语言。", 400, 28, BLACK, bold=True, spacing=10)
    draw_source(draw, "Lina Ghotmeh — Architecture｜PIN–UP 39", light=True)
    return save(canvas, 6)


def make_tophat() -> Path:
    canvas = Image.new("RGBA", (W, H), PINK)
    image_panel(canvas, "07-top-hat-hero.jpg", (0, 54, W, 848), focal=(0.50, 0.46), darken=0.90,
                label="TOP-HAT HOUSE / WATER ISLAND")
    image_panel(canvas, "07-top-hat-living.jpg", (38, 888, 556, 1370), focal=(0.50, 0.50), border=4,
                label="LIVING + DINING")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 7, BLUE)
    impact(draw, ["修复", "不是", "复刻"], 610, 900, 88, BLUE, max_width=510)
    draw.rectangle((610, 1206, 1204, 1568), fill=BLACK)
    draw_wrapped(draw, (646, 1244), "1984年的Top-Hat House没有被抹平为‘新房’。修复保住它的红色细节、夸张屋顶和面向海的生活方式，也保存了Water Island的酷儿创作社区。", 500, 28, WHITE, bold=True, spacing=10)
    draw_source(draw, "Paul van der Grient｜Top-Hat House｜PIN–UP 39", light=True)
    return save(canvas, 7)


def make_jose() -> Path:
    canvas = Image.new("RGBA", (W, H), GREEN)
    image_panel(canvas, "08-jose-dining.jpg", (0, 54, W, 718), focal=(0.50, 0.49), darken=0.92,
                label="JOSÉ LEÓN CERRILLO'S TOWNHOUSE / CDMX")
    image_panel(canvas, "08-jose-rooftop.jpg", (38, 758, 596, 1264), focal=(0.50, 0.50), border=4,
                label="ROOFTOP GARDEN + PRIVACY")
    image_panel(canvas, "08-jose-bedroom.jpg", (620, 758, 1204, 1264), focal=(0.50, 0.50), border=4,
                label="BED / STORAGE / DIVIDER")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 8, ORANGE)
    impact(draw, ["收藏", "也能", "生活"], 42, 160, 92, ORANGE, max_width=500)
    draw.rectangle((38, 1302, 1204, 1572), fill=WHITE)
    draw_wrapped(draw, (72, 1338), "Cerrillo把作品、家具与建筑改造揉进同一个家：屋顶以格栅取得遮阳和隐私，床头兼作储物与隔断，生活与收藏不再互相让位。", 1080, 29, BLACK, bold=True, spacing=10)
    draw_source(draw, "Asger Carlsen｜José León Cerrillo's Mexico City Townhouse｜PIN–UP 39", light=True)
    return save(canvas, 8)


def make_tertulia() -> Path:
    canvas = Image.new("RGBA", (W, H), RED)
    image_panel(canvas, "09-tertulia-group.jpg", (0, 54, W, 776), focal=(0.50, 0.50), darken=0.88,
                label="FRIDA ESCOBEDO'S TERTULIA / MEXICO CITY")
    image_panel(canvas, "09-tertulia-a.jpg", (38, 816, 606, 1306), focal=(0.50, 0.45), border=4,
                label="ART / DESIGN / FOOD")
    image_panel(canvas, "09-tertulia-b.jpg", (630, 816, 1204, 1306), focal=(0.50, 0.45), border=4,
                label="A CITY-SCALE LIVING ROOM")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 9, PAPER)
    impact(draw, ["城市", "也要有", "客厅"], 42, 170, 90, PAPER, max_width=570)
    draw.rectangle((38, 1342, 1204, 1572), fill=PAPER)
    draw_wrapped(draw, (72, 1376), "Frida Escobedo把10位墨西哥城的创作者聚在Mario Pani设计的Reforma双塔。家不是封闭单元，也可以是由对话、食物与相互支持组成的文化基础设施。", 1080, 28, BLACK, bold=True, spacing=9)
    draw_source(draw, "Rodrigo Álvarez｜Frida Escobedo's Tertulia｜PIN–UP 39", light=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "03-frida-sam-a.jpg", (0, 54, 492, H), focal=(0.50, 0.48), darken=0.83)
    image_panel(canvas, "04-sam-portrait-b.jpg", (514, 54, 1242, 580), focal=(0.50, 0.48), darken=0.86, label="LIVING")
    image_panel(canvas, "08-jose-kitchen.jpg", (514, 602, 1242, 1601), focal=(0.50, 0.50), darken=0.86, label="EVERYDAY")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 10, RED)
    draw.rectangle((80, 706, 1162, 1198), fill=rgba(RED, 246))
    draw.text((116, 750), "家不是", font=font(92, True), fill=BLACK)
    draw.text((116, 870), "私有容器", font=font(92, True), fill=BLACK)
    draw.rectangle((116, 1024, 1098, 1038), fill=ORANGE)
    draw.text((116, 1074), "而是照护、劳动与共居的关系系统", font=font(36, True), fill=BLACK)
    draw.rectangle((80, 1218, 1162, 1290), fill=BLACK)
    draw.text((620, 1254), "空间 × 照护 × 材料 × 社群", font=font(27, True), fill=WHITE, anchor="mm")
    draw_source(draw, "Daniel Shea / Sam Chermayeff / Asger Carlsen｜PIN–UP 39", light=True)
    return save(canvas, 10)


def make_garden_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), GREEN)
    image_panel(canvas, "10-piet-detroit.jpg", (0, 54, W, 820), focal=(0.50, 0.50), darken=0.88,
                label="OUDOLF GARDEN / BELLE ISLE / DETROIT")
    image_panel(canvas, "10-piet-plan.jpg", (38, 866, 730, 1564), focal=(0.50, 0.50), border=4,
                label="PLANTING PLAN / BELLE ISLE")
    draw = ImageDraw.Draw(canvas)
    draw_meta(draw, 10, ORANGE)
    impact(draw, ["花园", "也是", "家"], 42, 156, 96, ORANGE, max_width=430)
    draw.rectangle((768, 866, 1204, 1564), fill=PAPER)
    draw.text((806, 914), "会生长的日常", font=font(34, True), fill=BLACK)
    draw.line((806, 970, 1160, 970), fill=ORANGE, width=12)
    draw_wrapped(draw, (806, 1020), "Piet Oudolf 用超过 160 种植物编写 Belle Isle 的种植计划。凋零、再生、维护与季节变化不再是背景，而是空间的一部分。舒适不必恒定，家的边界也可以一直生长。", 354, 30, BLACK, bold=True, spacing=11)
    draw_source(draw, "Piet Oudolf / Belle Isle, Detroit｜PIN–UP 39", light=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#c4bdb2")
    for idx, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (idx % 5) * (tw + gap), gap + (idx // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 39｜家到底是谁的？"
    body = (
        "我们总把家想成最私人的地方，但PIN–UP 39提醒我：一个家的布局，往往先暴露谁承担劳动、谁拥有隐私、谁能被照顾。\n\n"
        "Frida Escobedo客座编辑的《Domesticity》，没有把住宅只当成风格样板。Sam Chermayeff用半公共住宅和三角厨房，让日常互动重新发生；Tatiana Bilbao从土墙住宅、可负担住房到一张桌子，把建筑理解为照护；Lina Ghotmeh让材料承接战争记忆、手艺与欢迎。\n\n"
        "Top-Hat House的修复保住了一座后现代海岛住宅和它所属的创作社区；José León Cerrillo把收藏、储物、屋顶花园和起居空间揉进同一个家；Frida在墨西哥城的tertulia，则把朋友、食物与对话扩展成城市的客厅。\n\n"
        "所谓‘住得好’，也许不只是家具是否好看，而是空间能不能让关系变得更公平、更松弛，也更有共同生活的可能。\n\n"
        "如果重做自己的家，你最想先改变隐私、劳动，还是人与人相处的方式？"
    )
    tags = "#PINUP #PINUP39 #建筑杂志 #住宅设计 #空间设计 #室内设计 #当代建筑 #FridaEscobedo"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 39 图片与内容来源

- 第01页：PIN–UP 39 官方期号页 {ISSUE_URL}
- 第02、03页：Frida Escobedo 编辑信 {EDITOR_URL}；摄影 Wolfgang Tillmans
- 第04页 Sam Chermayeff：{SAM_URL}；摄影 Oliver Helbig、Nadine Fraczkowski
- 第10页 Frida Escobedo × Sam Chermayeff：{FRIDA_SAM_URL}；摄影 Daniel Shea
- 第05页 Tatiana Bilbao：{BILBAO_URL}；摄影 Iwan Baan，图像 Tatiana Bilbao ESTUDIO
- 第06页 Lina Ghotmeh：{LINA_URL}；图像 Lina Ghotmeh — Architecture
- 第07页 Top-Hat House：{TOPHAT_URL}；摄影 Paul van der Grient
- 第08页 José León Cerrillo：{JOSE_URL}；摄影 Asger Carlsen
- 第09页 Frida Escobedo's Tertulia：{TERTULIA_URL}；摄影 Rodrigo Álvarez

所有图片均来自 PIN–UP 官方第39期文章或官方期号页，并按原文项目名称与摄影署名记录。
版权：图片版权归 PIN–UP、原摄影师及项目权利方所有；本文件仅作内容编辑与发布前来源记录。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-39",
        "issue": "PIN–UP 39 · DOMESTICITY",
        "date": "F/W 2025/26",
        "core_question": "家到底是谁的？",
        "core_thesis": "家不是私有容器，而是照护、劳动、材料与共居关系的系统。",
        "pages": [
            "01 封面：家不是私有容器",
            "02 中文目录：本期内容导览",
            "03 Frida Escobedo：私密空间映照社会关系",
            "04 Sam Chermayeff：隐私不是默认值",
            "05 Tatiana Bilbao：住宅是一种照护",
            "06 Lina Ghotmeh：材料记得生活",
            "07 Top-Hat House：修复不是复刻",
            "08 José León Cerrillo：收藏也能生活",
            "09 Frida's Tertulia：城市也要有客厅",
            "10 总结：家的关系系统",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    revised_title = "PIN–UP 39｜家到底是谁的？"
    revised_body = (
        "家最容易被说成私事，但一套住宅的布局总会露出分工：谁能独处，谁方便相遇，谁承担维护，谁被照顾。\n\n"
        "PIN–UP 39 把这个问题摊开来看。大都会博物馆的历史房间提醒我们，保存从来不是把过去封存，而是一次次选择如何重组；Sam Chermayeff 把厨房压缩成三角装置，让相遇成为空间功能；Tatiana Bilbao 用土墙、住房与餐桌讨论照护；Lina Ghotmeh 让材料接住时间与记忆。\n\n"
        "修复后的 Top-Hat House 保住了一种海岛上的创作生活，José León Cerrillo 则让收藏、储物和屋顶花园共处在同一个屋檐下。Frida Escobedo 的 tertulia 把朋友、食物和对话延伸成城市客厅。最后，Piet Oudolf 的 Belle Isle 种植计划让我们看到：家也可以是一座不断凋零、再生、需要被照料的花园。\n\n"
        "真正值得重做的，也许不是某种装修风格，而是我们如何安排独处、相遇、劳动和共享。"
    )
    revised_body += "\n\n它不提供一套可以照抄的家，而是不断追问：一张餐桌、一面隔墙、一座屋顶花园，究竟能把谁带进来，又会把谁留在外面。"
    revised_body += "空间从不沉默，它总在塑造人与人的距离。"
    revised_tags = "#PINUP #PINUP39 #建筑杂志 #住宅设计 #空间设计 #室内设计 #当代建筑 #花园设计"
    (OUT / "发布文案.md").write_text(
        f"{revised_title}\n\n{revised_body}\n\n{revised_tags}\n", encoding="utf-8"
    )
    revised_sources = f"""# PIN–UP 39 图片与内容来源
- 第01页：PIN–UP 39 官方期号页 {ISSUE_URL}
- 第02、10页：Piet Oudolf 访谈与项目图片 {PIET_URL}
- 第03页：The Metropolitan Museum of Art 的 Period Rooms {MET_URL}
- 第04页：Sam Chermayeff {SAM_URL}
- 第05页：Tatiana Bilbao {BILBAO_URL}
- 第06页：Lina Ghotmeh {LINA_URL}
- 第07页：Top-Hat House {TOPHAT_URL}
- 第08页：José León Cerrillo {JOSE_URL}
- 第09页：Frida Escobedo's Tertulia {TERTULIA_URL}

图片均来自 PIN–UP 官方文章或官方期号页面；图片版权归原摄影师、项目方与 PIN–UP 所有。
"""
    (OUT / "图片来源.md").write_text(revised_sources, encoding="utf-8")
    revised_manifest = {
        "type": "magazine",
        "slug": "pinup-39",
        "issue": "PIN–UP 39 · DOMESTICITY",
        "date": "F/W 2025/26",
        "core_question": "家到底是谁的？",
        "core_thesis": "家的空间安排决定了独处、劳动、照护与共享如何发生。",
        "pages": [
            "01 封面：家不是私有容器",
            "02 中文目录：本期内容导览",
            "03 The Met Period Rooms：室内不是标本",
            "04 Sam Chermayeff：隐私不是默认值",
            "05 Tatiana Bilbao：住宅是一种照护",
            "06 Lina Ghotmeh：材料记得生活",
            "07 Top-Hat House：修复不是复刻",
            "08 José León Cerrillo：收藏也能生活",
            "09 Frida's Tertulia：城市也要有客厅",
            "10 Piet Oudolf：花园也是家",
        ],
    }
    POST.write_text(json.dumps(revised_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_period_rooms(), make_sam(), make_bilbao(),
        make_lina(), make_tophat(), make_jose(), make_tertulia(), make_garden_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 39 cards in {OUT}")


if __name__ == "__main__":
    main()
