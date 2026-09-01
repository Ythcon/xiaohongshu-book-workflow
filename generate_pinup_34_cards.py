from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-34"
OUT = ROOT / "output" / "pinup-34"
POST = ROOT / "posts" / "pinup-34" / "post.json"

W, H = 1242, 1660
INK = "#17191d"
PAPER = "#f4f0e9"
COBALT = "#4b59ef"
PINK = "#e9b8ab"
RED = "#fa4b33"
SILVER = "#b8bab8"
YELLOW = "#f7d84a"

ISSUE_URL = "https://www.pinupmagazine.org/issues/pinup-34-body-issue-travis-scott"
TRAVIS_URL = "https://www.pinupmagazine.org/articles/travis-scott-design-alphabet"
JONATHAN_URL = "https://www.pinupmagazine.org/articles/jonathan-anderson-interview"
GAMPER_URL = "https://www.pinupmagazine.org/articles/martino-gamper-and-max-lamb-interview"
CERRI_URL = "https://www.pinupmagazine.org/articles/leather-rebel-pierluigi-cerri-80s-showpiece-has-lost-none-of-its-edge"
CFGNY_URL = "https://www.pinupmagazine.org/articles/cfgny-emporium-marsell"
LUNA_URL = "https://www.pinupmagazine.org/articles/lunar-eclipse-luna-luna-art-amusement-park"
BARNEY_URL = "https://www.pinupmagazine.org/articles/matthew-barney-interview"
BODY_URL = "https://www.pinupmagazine.org/articles/body-talk-drew-zeiba-essay"

shared.SRC = SRC
shared.OUT = OUT


def font(size: int, bold: bool = False):
    return shared.font(size, bold)


def rgba(value: str, alpha: int = 255):
    return shared.rgba(value, alpha)


def image_panel(canvas, name, box, **kwargs):
    return shared.image_panel(canvas, name, box, **kwargs)


def draw_wrapped(draw, xy, text, width, size, fill, **kwargs):
    return shared.draw_wrapped(draw, xy, text, width, size, fill, **kwargs)


def save(image: Image.Image, number: int) -> Path:
    path = OUT / f"{number:02d}.jpg"
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def meta(draw: ImageDraw.ImageDraw, number: int, accent: str, *, light: bool = False) -> None:
    bg = PAPER if light else INK
    fg = INK if light else PAPER
    draw.rectangle((0, 0, W, 54), fill=bg)
    draw.rectangle((0, 51, W, 54), fill=accent)
    draw.text((34, 26), "PIN–UP 34 / BODY ISSUE", font=font(18, True), fill=fg, anchor="lm")
    draw.text((1204, 26), f"{number:02d} / 10", font=font(19, True), fill=fg, anchor="rm")


def source(draw: ImageDraw.ImageDraw, text: str, *, dark: bool = True) -> None:
    draw.rectangle((0, 1601, W, H), fill=rgba(INK if dark else PAPER, 245))
    draw.text((34, 1631), text, font=font(15), fill=PAPER if dark else INK, anchor="lm")


def marker(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, color: str, *, dark: bool = False) -> None:
    draw.ellipse((x, y, x + 30, y + 30), fill=color)
    draw.text((x + 46, y + 15), text, font=font(18, True), fill=PAPER if dark else INK, anchor="lm")


def framed_cover(canvas: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    original = Image.open(SRC / name).convert("RGBA")
    fitted = shared.fit_inside(original, (x1 - x0, y1 - y0))
    dx = x0 + (x1 - x0 - fitted.width) // 2
    dy = y0 + (y1 - y0 - fitted.height) // 2
    shadow = Image.new("RGBA", fitted.size, rgba(INK, 85))
    canvas.alpha_composite(shadow, (dx + 14, dy + 16))
    canvas.alpha_composite(fitted, (dx, dy))


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, W, 358), fill=INK)
    draw.rectangle((0, 358, 346, 1600), fill=COBALT)
    draw.rectangle((346, 358, W, 498), fill=PINK)
    draw.text((44, 92), "身体", font=font(132, True), fill=PAPER)
    draw.text((44, 240), "会设计", font=font(77, True), fill=COBALT)
    draw.text((438, 392), "空间", font=font(82, True), fill=INK)
    draw.text((50, 500), "BODY", font=font(28, True), fill=PAPER)
    draw.text((50, 540), "ISSUE", font=font(28, True), fill=PAPER)
    draw.text((50, 1452), "S/S 2023", font=font(19, True), fill=PINK)
    framed_cover(canvas, "cover-01.png", (404, 546, 1160, 1538))
    draw.line((404, 516, 1160, 516), fill=INK, width=5)
    draw.text((1160, 486), "PIN–UP 34", font=font(22, True), fill=INK, anchor="ra")
    source(draw, "PIN–UP 34 官方封面｜BODY ISSUE / TRAVIS SCOTT", dark=True)
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, W, 308), fill=COBALT)
    draw.text((42, 118), "身体", font=font(98, True), fill=PAPER)
    draw.text((344, 118), "目录", font=font(98, True), fill=PINK)
    draw.text((42, 246), "BODY ISSUE / 中文导览", font=font(23, True), fill=INK)
    draw.text((1206, 118), "34", font=font(186, True), fill=rgba(PAPER, 142), anchor="ra")
    meta(draw, 2, RED, light=True)
    items = [
        ("03", "TRAVIS SCOTT", "身体，也能写字"),
        ("04", "JONATHAN ANDERSON", "衣服先重画身体"),
        ("05", "GAMPER & LAMB", "椅子，先听材料说话"),
        ("06", "PIERLUIGI CERRI", "沙发，也像基础设施"),
        ("07", "CFGNY", "衣服，也是一套建筑"),
        ("08", "LUNA LUNA", "游乐场，必须适合身体"),
        ("09", "MATTHEW BARNEY", "形式，要给即兴留空"),
        ("10", "BODY ISSUE", "身体不只占据空间"),
    ]
    for i, (number, name, title) in enumerate(items):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        x = 44 + col * 604
        y = 404 + row * 254
        draw.text((x, y), number, font=font(30, True), fill=RED)
        draw.text((x, y + 42), name, font=font(20, True), fill=COBALT)
        draw_wrapped(draw, (x, y + 84), title, 500, 34, INK, bold=True, spacing=8)
        draw.line((x, y + 204, x + 528, y + 204), fill=rgba(INK, 84), width=2)
    draw.text((44, 1504), "姿势、物件、尺度与规则，会一起生成空间。", font=font(28, True), fill=COBALT)
    source(draw, "PIN–UP 34｜中文目录", dark=True)
    return save(canvas, 2)


def make_travis() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "travis-03.jpg", (38, 112, 406, 980), focal=(0.50, 0.52), border=4, border_color=INK)
    image_panel(canvas, "travis-04.jpg", (426, 112, 798, 980), focal=(0.50, 0.52), border=4, border_color=INK)
    image_panel(canvas, "travis-05.jpg", (818, 112, 1204, 980), focal=(0.50, 0.52), border=4, border_color=INK)
    image_panel(canvas, "travis-06.jpg", (38, 1004, 604, 1516), focal=(0.50, 0.52), border=4, border_color=INK)
    image_panel(canvas, "travis-08.jpg", (630, 1004, 906, 1516), focal=(0.50, 0.52), border=4, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 3, COBALT, light=True)
    draw.rectangle((934, 1004, 1204, 1516), fill=COBALT)
    marker(draw, 966, 1042, "TRAVIS SCOTT", PINK, dark=True)
    draw.text((966, 1134), "身体", font=font(66, True), fill=PAPER)
    draw.text((966, 1218), "也能", font=font(52, True), fill=PINK)
    draw.text((966, 1286), "写字", font=font(78, True), fill=PAPER)
    draw.text((966, 1402), "姿势不是注释，", font=font(22, True), fill=INK)
    draw.text((966, 1434), "它本身就是", font=font(22, True), fill=INK)
    draw.text((966, 1466), "一套设计语言。", font=font(22, True), fill=INK)
    source(draw, "Travis Scott｜The Design Alphabet｜PIN–UP 34", dark=True)
    return save(canvas, 3)


def make_jonathan() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    image_panel(canvas, "jonathan-05.jpg", (0, 54, W, 826), focal=(0.50, 0.50), darken=0.95,
                label="JONATHAN ANDERSON / BODY + CRAFT")
    image_panel(canvas, "jonathan-02.jpg", (42, 876, 568, 1514), focal=(0.50, 0.50), border=5, border_color=PAPER)
    image_panel(canvas, "jonathan-04.jpg", (610, 876, 860, 1514), focal=(0.50, 0.50), border=5, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 4, PINK)
    draw.rectangle((902, 876, 1204, 1514), fill=PINK)
    marker(draw, 936, 914, "JONATHAN ANDERSON", COBALT)
    draw.text((936, 1008), "衣服", font=font(68, True), fill=INK)
    draw.text((936, 1094), "先重画", font=font(50, True), fill=INK)
    draw.text((936, 1160), "身体", font=font(76, True), fill=COBALT)
    draw.text((936, 1294), "轮廓、比例与空腔，", font=font(21, True), fill=INK)
    draw.text((936, 1326), "让服装不只覆盖人，", font=font(21, True), fill=INK)
    draw.text((936, 1358), "还改变人如何出现。", font=font(21, True), fill=INK)
    source(draw, "Jonathan Anderson｜Body, Craft, and Collecting｜PIN–UP 34", dark=True)
    return save(canvas, 4)


def make_gamper() -> Path:
    canvas = Image.new("RGBA", (W, H), SILVER)
    image_panel(canvas, "gamper-03.jpg", (0, 54, 700, H), focal=(0.50, 0.50), darken=0.96,
                label="MARTINO GAMPER / MAX LAMB")
    image_panel(canvas, "gamper-04.jpg", (742, 88, 1204, 646), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "gamper-05.jpg", (742, 688, 970, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 5, RED, light=True)
    draw.rectangle((1010, 688, 1204, 1514), fill=INK)
    draw.text((1038, 732), "椅子", font=font(64, True), fill=PAPER)
    draw.text((1038, 814), "先听", font=font(50, True), fill=PINK)
    draw.text((1038, 880), "材料", font=font(64, True), fill=RED)
    draw.text((1038, 1024), "拼接、切削与", font=font(20, True), fill=PAPER)
    draw.text((1038, 1054), "材料的阻力，", font=font(20, True), fill=PAPER)
    draw.text((1038, 1084), "会先给出形状。", font=font(20, True), fill=PAPER)
    draw.line((1038, 1338, 1170, 1338), fill=COBALT, width=14)
    source(draw, "Martino Gamper & Max Lamb｜Material and Making｜PIN–UP 34", dark=True)
    return save(canvas, 5)


def make_cerri() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    image_panel(canvas, "cerri-01.jpg", (38, 96, W - 38, 568), focal=(0.50, 0.50), border=4, border_color=PINK)
    image_panel(canvas, "cerri-02.jpg", (38, 610, 604, 1514), focal=(0.50, 0.50), border=4, border_color=PINK)
    image_panel(canvas, "cerri-03.jpg", (642, 610, 1020, 1514), focal=(0.50, 0.50), border=4, border_color=PINK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 6, YELLOW)
    draw.rectangle((1060, 610, 1204, 1514), fill=YELLOW)
    draw.text((1082, 656), "沙", font=font(52, True), fill=INK)
    draw.text((1082, 720), "发", font=font(52, True), fill=INK)
    draw.text((1082, 818), "也像", font=font(31, True), fill=RED)
    draw.text((1082, 864), "基", font=font(52, True), fill=INK)
    draw.text((1082, 928), "础", font=font(52, True), fill=INK)
    draw.text((1082, 992), "设", font=font(52, True), fill=INK)
    draw.text((1082, 1056), "施", font=font(52, True), fill=INK)
    draw.text((1082, 1180), "柔软坐垫", font=font(18, True), fill=INK)
    draw.text((1082, 1208), "嵌进钢结构，", font=font(18, True), fill=INK)
    draw.text((1082, 1236), "把工程语言", font=font(18, True), fill=INK)
    draw.text((1082, 1264), "带回客厅。", font=font(18, True), fill=INK)
    source(draw, "Pierluigi Cerri｜Ouverture Sofa｜PIN–UP 34", dark=True)
    return save(canvas, 6)


def make_cfgny() -> Path:
    canvas = Image.new("RGBA", (W, H), PINK)
    image_panel(canvas, "cfgny-02.jpg", (0, 54, W, 834), focal=(0.50, 0.52), darken=0.97,
                label="CFGNY / EMPORIUM MILANO")
    image_panel(canvas, "cfgny-03.jpg", (42, 884, 560, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "cfgny-04.jpg", (602, 884, 876, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 7, COBALT, light=True)
    draw.rectangle((918, 884, 1204, 1514), fill=COBALT)
    marker(draw, 950, 922, "CFGNY", YELLOW, dark=True)
    draw.text((950, 1018), "衣服", font=font(68, True), fill=PAPER)
    draw.text((950, 1104), "也是", font=font(48, True), fill=PAPER)
    draw.text((950, 1170), "建筑", font=font(74, True), fill=YELLOW)
    draw.text((950, 1306), "皮革、纸板与", font=font(21, True), fill=INK)
    draw.text((950, 1338), "商品流动，让", font=font(21, True), fill=INK)
    draw.text((950, 1370), "身体穿进制度。", font=font(21, True), fill=INK)
    source(draw, "CFGNY｜Emporium Milano｜PIN–UP 34", dark=True)
    return save(canvas, 7)


def make_luna() -> Path:
    canvas = Image.new("RGBA", (W, H), COBALT)
    image_panel(canvas, "luna-02.jpg", (0, 54, 714, H), focal=(0.50, 0.50), darken=0.94,
                label="LUNA LUNA / ART AMUSEMENT PARK")
    image_panel(canvas, "luna-03.jpg", (754, 96, 1204, 610), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "luna-04.jpg", (754, 650, 1204, 1008), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 8, YELLOW)
    draw.rectangle((754, 1048, 1204, 1514), fill=YELLOW)
    marker(draw, 788, 1084, "LUNA LUNA", RED)
    draw.text((788, 1178), "游乐场", font=font(63, True), fill=INK)
    draw.text((788, 1258), "必须适合", font=font(48, True), fill=INK)
    draw.text((788, 1324), "身体", font=font(72, True), fill=RED)
    draw.text((788, 1432), "当艺术变成可乘坐的装置，", font=font(20, True), fill=INK)
    draw.text((788, 1460), "安全与物理也成为创作条件。", font=font(20, True), fill=INK)
    source(draw, "Luna Luna｜Art Amusement Park｜PIN–UP 34", dark=True)
    return save(canvas, 8)


def make_barney() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "barney-04.jpg", (0, 54, W, 792), focal=(0.50, 0.50), darken=0.95,
                label="MATTHEW BARNEY / CREMASTER")
    image_panel(canvas, "barney-01.jpg", (42, 842, 576, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "barney-06.jpg", (618, 842, 884, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 9, RED, light=True)
    draw.rectangle((926, 842, 1204, 1514), fill=RED)
    marker(draw, 958, 878, "MATTHEW BARNEY", COBALT)
    draw.text((958, 980), "形式", font=font(68, True), fill=INK)
    draw.text((958, 1066), "要给", font=font(49, True), fill=INK)
    draw.text((958, 1130), "即兴", font=font(68, True), fill=PAPER)
    draw.text((958, 1216), "留空", font=font(68, True), fill=INK)
    draw.text((958, 1350), "先给身体一组规则，", font=font(20, True), fill=INK)
    draw.text((958, 1380), "再让行动把形式", font=font(20, True), fill=INK)
    draw.text((958, 1410), "一步步推出来。", font=font(20, True), fill=INK)
    source(draw, "Matthew Barney｜Cremaster and Improvisation｜PIN–UP 34", dark=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 10, COBALT)
    draw.rectangle((0, 54, 528, 1600), fill=PINK)
    draw.rectangle((528, 54, 774, 1600), fill=COBALT)
    draw.rectangle((774, 54, W, 1600), fill=INK)
    draw.text((56, 170), "身体", font=font(115, True), fill=INK)
    draw.text((56, 304), "不只", font=font(80, True), fill=INK)
    draw.text((56, 398), "占据", font=font(80, True), fill=RED)
    draw.text((56, 492), "空间", font=font(115, True), fill=INK)
    draw.text((568, 160), "姿", font=font(74, True), fill=PAPER)
    draw.text((568, 410), "物", font=font(74, True), fill=YELLOW)
    draw.text((568, 660), "尺", font=font(74, True), fill=PAPER)
    draw.text((568, 910), "规", font=font(74, True), fill=YELLOW)
    draw.text((818, 188), "身体", font=font(108, True), fill=PAPER)
    draw.text((818, 320), "也定义", font=font(65, True), fill=PAPER)
    draw.text((818, 402), "空间", font=font(104, True), fill=COBALT)
    draw.line((822, 556, 1168, 556), fill=RED, width=14)
    draw_wrapped(draw, (818, 638), "姿势改变路径，物件规定停留，尺度塑造感知，规则分配谁能参与。", 346, 34, PAPER, bold=True, spacing=12)
    draw_wrapped(draw, (818, 1126), "从来没有中性的身体，也没有与身体无关的空间。", 346, 34, YELLOW, bold=True, spacing=12)
    draw.text((818, 1480), "PIN–UP 34 / BODY ISSUE", font=font(20, True), fill=PINK)
    source(draw, "PIN–UP 34｜身体会设计空间", dark=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#959895")
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 34｜身体会设计空间"
    body = (
        "空间从来不是等着身体进入的空盒子。PIN–UP 34 把“身体”重新放回设计中心：姿势、比例、皮肤、动作，都会反过来决定物件如何成立、房间如何被体验。\n\n"
        "Travis Scott 用身体拼出字母，把姿势变成一套可以阅读的设计语言；Jonathan Anderson 通过服装与工艺切分轮廓，让身体同时像容器、雕塑和场景。Martino Gamper 与 Max Lamb 则从材料与制作出发，让椅子不再只服从标准坐姿。\n\n"
        "Pierluigi Cerri 把钢结构与柔软坐垫并置，让沙发借用基础设施的尺度。CFGNY 让衣服、纸板、展览和商品流动缠绕在一起；Luna Luna 证明，当艺术要被乘坐、穿越与使用，物理条件就是作品的一部分。Matthew Barney 进一步把身体的即兴当作形式的发动机。\n\n"
        "身体不是尺寸表上的一个数字，也不只是在空间里移动的人。它在制造尺度、测试材料、重写规则。设计若忽略身体，留下的往往只是看起来正确的形式。你最近在哪一处空间里，最明显地感到自己的身体被设计了？"
    )
    tags = "#PINUP #PINUP34 #身体与空间 #建筑设计 #家具设计 #当代艺术 #展览设计 #设计思考"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 34 图片与内容来源
- 第01页：PIN–UP 34 BODY ISSUE / Travis Scott 官方期号页 {ISSUE_URL}
- 第03页：Travis Scott / The Design Alphabet {TRAVIS_URL}
- 第04页：Jonathan Anderson / Body, Craft, and Collecting {JONATHAN_URL}
- 第05页：Martino Gamper & Max Lamb {GAMPER_URL}
- 第06页：Pierluigi Cerri / Ouverture Sofa {CERRI_URL}
- 第07页：CFGNY / Emporium Milano {CFGNY_URL}
- 第08页：Luna Luna / Art Amusement Park {LUNA_URL}
- 第09页：Matthew Barney {BARNEY_URL}
- 第10页：Body Talk / Architecture-Body Discourse {BODY_URL}

图片均来自 PIN–UP 官方期号页或官方文章页。图片版权归 PIN–UP、原摄影师、建筑师、艺术家与项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-34",
        "issue": "PIN–UP 34 · BODY ISSUE",
        "date": "S/S 2023",
        "core_question": "身体只是空间的使用者吗？",
        "core_thesis": "身体不只进入空间；姿势、材料、尺度与行动会反过来生成物件、场景与规则。",
        "pages": [
            "01 封面：身体会设计空间",
            "02 中文目录：本期内容导览",
            "03 Travis Scott：身体也能写字",
            "04 Jonathan Anderson：衣服先重画身体",
            "05 Martino Gamper & Max Lamb：椅子先听材料说话",
            "06 Pierluigi Cerri：沙发也像基础设施",
            "07 CFGNY：衣服也是一套建筑",
            "08 Luna Luna：游乐场必须适合身体",
            "09 Matthew Barney：形式要给即兴留空",
            "10 收束：身体不只占据空间",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_travis(), make_jonathan(), make_gamper(),
        make_cerri(), make_cfgny(), make_luna(), make_barney(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 34 cards in {OUT}")


if __name__ == "__main__":
    main()
