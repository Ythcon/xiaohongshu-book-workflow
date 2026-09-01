from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-32"
OUT = ROOT / "output" / "pinup-32"
POST = ROOT / "posts" / "pinup-32" / "post.json"

W, H = 1242, 1660
INK = "#121316"
PAPER = "#f5f2eb"
SILVER = "#d2d3d8"
CYAN = "#49bde7"
ORANGE = "#ff593e"
VIOLET = "#7a59e6"
LIME = "#d4f53e"
BLUE = "#123059"

ISSUE_URL = "https://www.pinupmagazine.org/issues/pinup-32-the-architecture-of-art"
TILLMANS_URL = "https://www.pinupmagazine.org/articles/wolfgang-tillmans-interview-emmanuel-olunkwa"
CARDINAL_URL = "https://www.pinupmagazine.org/articles/douglas-cardinal-interview"
NAUMANN_URL = "https://www.pinupmagazine.org/articles/henrike-naumann-interview"
MARCELIS_URL = "https://www.pinupmagazine.org/articles/sabine-marcelis-interview"
GOLDEN_URL = "https://www.pinupmagazine.org/articles/thelma-golden-interview"
HERZOG_URL = "https://www.pinupmagazine.org/articles/christine-binswanger-kathy-halbreich-herzog-and-de-meuron-interview"
WANGSHUI_URL = "https://www.pinupmagazine.org/articles/wangshui-interview"

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


def topbar(draw: ImageDraw.ImageDraw, number: int, accent: str, *, light: bool = False) -> None:
    bg = PAPER if light else INK
    fg = INK if light else PAPER
    draw.rectangle((0, 0, W, 54), fill=bg)
    draw.rectangle((0, 50, W, 54), fill=accent)
    draw.text((34, 25), "PIN–UP 32 / THE ARCHITECTURE OF ART", font=font(18, True), fill=fg, anchor="lm")
    draw.text((1204, 25), f"{number:02d} / 10", font=font(19, True), fill=fg, anchor="rm")


def source(draw: ImageDraw.ImageDraw, text: str, *, dark: bool = True) -> None:
    bg = rgba(INK if dark else PAPER, 245)
    fg = PAPER if dark else INK
    draw.rectangle((0, 1602, W, H), fill=bg)
    draw.text((34, 1631), text, font=font(15), fill=fg, anchor="lm")


def tag(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, accent: str, *, dark: bool = True) -> None:
    fg = PAPER if dark else INK
    draw.rectangle((x, y, x + 12, y + 44), fill=accent)
    draw.text((x + 24, y + 22), text, font=font(18, True), fill=fg, anchor="lm")


def framed_cover(canvas: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    original = Image.open(SRC / name).convert("RGBA")
    fitted = shared.fit_inside(original, (x1 - x0, y1 - y0))
    cx = x0 + (x1 - x0 - fitted.width) // 2
    cy = y0 + (y1 - y0 - fitted.height) // 2
    shadow = Image.new("RGBA", fitted.size, rgba(INK, 135))
    canvas.alpha_composite(shadow, (cx + 18, cy + 20))
    canvas.alpha_composite(fitted, (cx, cy))


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, W, 314), fill=CYAN)
    draw.rectangle((0, 314, 202, H), fill=ORANGE)
    draw.rectangle((202, 314, 246, H), fill=LIME)
    draw.text((42, 112), "艺术", font=font(122, True), fill=INK)
    draw.text((42, 242), "不只挂在墙上", font=font(54, True), fill=INK)
    draw.text((276, 374), "PIN–UP", font=font(28, True), fill=LIME)
    draw.text((276, 418), "32", font=font(50, True), fill=PAPER)
    draw.text((276, 1460), "S/S 2022", font=font(20, True), fill=CYAN)
    draw.rectangle((426, 352, 1186, 1438), outline=LIME, width=8)
    framed_cover(canvas, "issue-01.jpg", (454, 380, 1158, 1408))
    draw.text((1158, 1484), "THE ARCHITECTURE OF ART", font=font(19, True), fill=PAPER, anchor="ra")
    source(draw, "PIN–UP 32 官方封面｜The Architecture of Art", dark=True)
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, W, 386), fill=INK)
    draw.text((50, 136), "本期", font=font(95, True), fill=PAPER)
    draw.text((50, 238), "目录", font=font(118, True), fill=CYAN)
    draw.text((1190, 260), "32", font=font(290, True), fill=rgba(CYAN, 95), anchor="ra")
    topbar(draw, 2, ORANGE)
    items = [
        ("03", "WOLFGANG TILLMANS", "展览，先在模型里发生"),
        ("04", "DOUGLAS CARDINAL", "建筑，先把场地听进去"),
        ("05", "HENRIKE NAUMANN", "一套沙发，也有政治"),
        ("06", "SABINE MARCELIS", "光，能把物件变成空间"),
        ("07", "THELMA GOLDEN", "机构不是容器，是立场"),
        ("08", "HERZOG & DE MEURON", "美术馆，要让人发生关系"),
        ("09", "WANGSHUI", "屏幕，正在长出房间"),
        ("10", "THE ARCHITECTURE OF ART", "艺术不只在墙上发生"),
    ]
    for i, (no, name, title) in enumerate(items):
        col, row = (0, i) if i < 4 else (1, i - 4)
        x = 50 + col * 608
        y = 468 + row * 250
        draw.text((x, y), no, font=font(26, True), fill=ORANGE)
        draw.text((x, y + 42), name, font=font(18, True), fill=VIOLET)
        draw_wrapped(draw, (x, y + 78), title, 500, 34, INK, bold=True, spacing=7)
        draw.line((x, y + 198, x + 510, y + 198), fill=rgba(INK, 85), width=2)
    draw.text((50, 1490), "艺术发生在空间、材料、机构与人群之间。", font=font(30, True), fill=INK)
    source(draw, "PIN–UP 32｜中文目录", dark=False)
    return save(canvas, 2)


def make_tillmans() -> Path:
    canvas = Image.new("RGBA", (W, H), SILVER)
    draw = ImageDraw.Draw(canvas)
    image_panel(canvas, "tillmans-02.jpg", (0, 54, 786, H), focal=(0.47, 0.57), darken=0.96,
                label="WOLFGANG TILLMANS / 1:10 EXHIBITION MODEL")
    image_panel(canvas, "tillmans-05.jpg", (828, 92, 1204, 542), focal=(0.52, 0.50), border=5, border_color=INK)
    image_panel(canvas, "tillmans-06.jpg", (828, 582, 1204, 960), focal=(0.50, 0.50), border=5, border_color=INK)
    draw.rectangle((828, 1000, 1204, 1516), fill=ORANGE)
    topbar(draw, 3, CYAN)
    tag(draw, 860, 1038, "WOLFGANG TILLMANS", CYAN, dark=False)
    draw.text((860, 1138), "展览", font=font(79, True), fill=INK)
    draw.text((860, 1230), "先在模型", font=font(50, True), fill=INK)
    draw.text((860, 1296), "里发生", font=font(63, True), fill=PAPER)
    draw_wrapped(draw, (860, 1392), "他把墙、照片与动线缩到1:10，观看从布展那一刻就被设计。", 308, 22, INK, bold=True, spacing=7)
    source(draw, "Wolfgang Tillmans｜1:10 exhibition models｜PIN–UP 32", dark=True)
    return save(canvas, 3)


def make_cardinal() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    image_panel(canvas, "cardinal-09.png", (0, 54, W, 894), focal=(0.53, 0.54), darken=0.94,
                label="DOUGLAS CARDINAL / ST. MARY'S CHURCH")
    image_panel(canvas, "cardinal-11.jpg", (42, 946, 608, 1516), focal=(0.48, 0.53), border=6, border_color=INK)
    image_panel(canvas, "cardinal-10.jpg", (652, 946, 902, 1516), focal=(0.50, 0.50), border=6, border_color=INK)
    draw.rectangle((946, 946, 1204, 1516), fill=BLUE)
    topbar(draw, 4, LIME, light=True)
    tag(draw, 978, 982, "DOUGLAS CARDINAL", LIME, dark=True)
    draw.text((978, 1080), "建筑", font=font(68, True), fill=PAPER)
    draw.text((978, 1164), "先把", font=font(49, True), fill=PAPER)
    draw.text((978, 1226), "场地", font=font(69, True), fill=LIME)
    draw.text((978, 1308), "听进去", font=font(45, True), fill=PAPER)
    draw_wrapped(draw, (978, 1394), "从土地与共同体出发，曲线不只是造型，而是对环境的回应。", 194, 21, PAPER, bold=True, spacing=7)
    source(draw, "Douglas Cardinal｜St. Mary's Church / Canadian Museum of History｜PIN–UP 32", dark=True)
    return save(canvas, 4)


def make_naumann() -> Path:
    canvas = Image.new("RGBA", (W, H), VIOLET)
    draw = ImageDraw.Draw(canvas)
    image_panel(canvas, "naumann-04.jpg", (0, 54, 844, H), focal=(0.42, 0.49), darken=0.97,
                label="HENRIKE NAUMANN / RE:EDUCATION")
    image_panel(canvas, "naumann-06.jpg", (884, 92, 1204, 602), focal=(0.52, 0.52), border=5, border_color=PAPER)
    image_panel(canvas, "naumann-02.jpg", (884, 642, 1204, 992), focal=(0.50, 0.48), border=5, border_color=PAPER)
    draw.rectangle((884, 1032, 1204, 1516), fill=INK)
    topbar(draw, 5, ORANGE)
    tag(draw, 916, 1068, "HENRIKE NAUMANN", ORANGE, dark=True)
    draw.text((916, 1160), "一套", font=font(63, True), fill=PAPER)
    draw.text((916, 1240), "沙发", font=font(73, True), fill=ORANGE)
    draw.text((916, 1326), "也有政治", font=font(43, True), fill=PAPER)
    draw_wrapped(draw, (916, 1402), "家具、墙纸与陈设会把记忆和意识形态，悄悄摆进日常。", 250, 21, PAPER, bold=True, spacing=7)
    source(draw, "Henrike Naumann｜Re:Education｜PIN–UP 32", dark=True)
    return save(canvas, 5)


def make_marcelis() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(canvas)
    image_panel(canvas, "marcelis-05.png", (0, 54, 618, H), focal=(0.51, 0.50), darken=0.98,
                label="SABINE MARCELIS / RESIN OBJECT")
    image_panel(canvas, "marcelis-03.jpg", (660, 92, 1204, 684), focal=(0.45, 0.48), border=5, border_color=ORANGE)
    image_panel(canvas, "marcelis-07.jpg", (660, 726, 1204, 1050), focal=(0.50, 0.52), border=5, border_color=ORANGE)
    draw.rectangle((660, 1092, 1204, 1516), fill=LIME)
    topbar(draw, 6, ORANGE)
    tag(draw, 696, 1128, "SABINE MARCELIS", ORANGE, dark=False)
    draw.text((696, 1220), "光", font=font(82, True), fill=INK)
    draw.text((790, 1220), "能把", font=font(48, True), fill=INK)
    draw.text((696, 1310), "物件", font=font(70, True), fill=INK)
    draw.text((844, 1310), "变成", font=font(43, True), fill=INK)
    draw.text((696, 1370), "空间", font=font(70, True), fill=ORANGE)
    draw.text((696, 1448), "树脂、玻璃与反光，让一件家具", font=font(16, True), fill=INK)
    draw.text((696, 1476), "越过类别，开始改变房间的感受。", font=font(16, True), fill=INK)
    source(draw, "Sabine Marcelis｜resin, glass and light works｜PIN–UP 32", dark=True)
    return save(canvas, 6)


def make_golden() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(canvas)
    image_panel(canvas, "golden-01.png", (0, 54, W, 936), focal=(0.50, 0.52), darken=0.97,
                label="THELMA GOLDEN / BLACK SPACES")
    image_panel(canvas, "golden-02.png", (42, 990, 728, 1516), focal=(0.50, 0.52), border=5, border_color=PAPER)
    draw.rectangle((770, 990, 1204, 1516), fill=ORANGE)
    topbar(draw, 7, LIME)
    tag(draw, 804, 1026, "THELMA GOLDEN", LIME, dark=False)
    draw.text((804, 1124), "机构", font=font(72, True), fill=INK)
    draw.text((804, 1212), "不是容器", font=font(50, True), fill=INK)
    draw.text((804, 1280), "是立场", font=font(66, True), fill=PAPER)
    draw_wrapped(draw, (804, 1392), "艺术空间不只保存作品；它也创造语境、社区与被看见的方式。", 346, 23, INK, bold=True, spacing=8)
    source(draw, "Thelma Golden｜Black spaces and institutional context｜PIN–UP 32", dark=True)
    return save(canvas, 7)


def make_herzog() -> Path:
    canvas = Image.new("RGBA", (W, H), BLUE)
    draw = ImageDraw.Draw(canvas)
    image_panel(canvas, "herzog-02.jpg", (0, 54, W, 808), focal=(0.52, 0.56), darken=0.96,
                label="HERZOG & DE MEURON / WALKER ART CENTER")
    image_panel(canvas, "herzog-04.jpg", (42, 862, 606, 1516), focal=(0.52, 0.53), border=5, border_color=PAPER)
    image_panel(canvas, "herzog-03.jpg", (646, 862, 870, 1516), focal=(0.50, 0.52), border=5, border_color=PAPER)
    draw.rectangle((910, 862, 1204, 1516), fill=PAPER)
    topbar(draw, 8, CYAN)
    tag(draw, 942, 898, "HERZOG & DE MEURON", CYAN, dark=False)
    draw.text((942, 994), "美术馆", font=font(62, True), fill=INK)
    draw.text((942, 1074), "要让人", font=font(47, True), fill=INK)
    draw.text((942, 1138), "发生", font=font(69, True), fill=ORANGE)
    draw.text((942, 1220), "关系", font=font(69, True), fill=INK)
    draw_wrapped(draw, (942, 1332), "创作、聚集与观看不该被分开，艺术空间要让它们在这里相遇。", 222, 23, INK, bold=True, spacing=8)
    source(draw, "Herzog & de Meuron｜art spaces incl. Walker Art Center｜PIN–UP 32", dark=True)
    return save(canvas, 8)


def make_wangshui() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    image_panel(canvas, "wangshui-05.png", (0, 54, W, 924), focal=(0.50, 0.54), darken=0.95,
                label="WANGSHUI / HYALINE SEED")
    image_panel(canvas, "wangshui-06.jpg", (42, 978, 590, 1516), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "wangshui-02.jpg", (632, 978, 886, 1516), focal=(0.52, 0.50), border=5, border_color=INK)
    draw.rectangle((928, 978, 1204, 1516), fill=CYAN)
    topbar(draw, 9, VIOLET, light=True)
    tag(draw, 960, 1014, "WANGSHUI", VIOLET, dark=True)
    draw.text((960, 1106), "屏幕", font=font(69, True), fill=INK)
    draw.text((960, 1192), "正在", font=font(48, True), fill=INK)
    draw.text((960, 1256), "长出", font=font(69, True), fill=VIOLET)
    draw.text((960, 1338), "房间", font=font(69, True), fill=INK)
    draw.text((960, 1440), "绘画、LED 与装置叠在一起，", font=font(16, True), fill=INK)
    draw.text((960, 1468), "屏幕成了新的空间界面。", font=font(16, True), fill=INK)
    source(draw, "WangShui｜Hyaline Seed and LED installations｜PIN–UP 32", dark=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    topbar(draw, 10, ORANGE, light=True)
    draw.rectangle((0, 54, W, 340), fill=INK)
    draw.rectangle((0, 340, 232, 1602), fill=CYAN)
    draw.rectangle((232, 340, 500, 1602), fill=ORANGE)
    draw.rectangle((500, 340, 816, 1602), fill=INK)
    draw.rectangle((816, 340, W, 1602), fill=LIME)
    draw.text((44, 176), "艺术，不只挂在墙上", font=font(82, True), fill=PAPER)
    draw.text((44, 274), "它被模型、房间、材料、机构与屏幕共同塑形。", font=font(27, True), fill=CYAN)
    draw.text((52, 470), "模型", font=font(84, True), fill=INK)
    draw.text((52, 714), "房间", font=font(82, True), fill=INK)
    draw.text((282, 490), "材质", font=font(85, True), fill=INK)
    draw.text((282, 740), "光线", font=font(84, True), fill=INK)
    draw.text((540, 490), "机构", font=font(87, True), fill=LIME)
    draw.text((540, 740), "人群", font=font(84, True), fill=PAPER)
    draw.text((858, 490), "屏幕", font=font(85, True), fill=INK)
    draw.text((858, 740), "身体", font=font(85, True), fill=INK)
    draw.line((858, 920, 1148, 920), fill=INK, width=14)
    draw.text((858, 994), "设计改变的，不只是", font=font(31, True), fill=INK)
    draw.text((858, 1044), "展墙的位置，而是作品", font=font(31, True), fill=INK)
    draw.text((858, 1094), "如何被看见、被分享、", font=font(31, True), fill=INK)
    draw.text((858, 1144), "被感受。", font=font(31, True), fill=INK)
    draw.text((858, 1478), "PIN–UP 32 / THE ARCHITECTURE OF ART", font=font(17, True), fill=INK)
    source(draw, "PIN–UP 32｜艺术不只挂在墙上", dark=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#7a7c82")
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 32｜艺术不只挂墙上"
    body = (
        "艺术真的只发生在画廊的白墙上吗？PIN–UP 32 把问题推回更前面：作品从哪里开始被观看，谁决定它被怎样看见？\n\n"
        "Wolfgang Tillmans 用 1:10 模型推演墙、照片与动线，展览在开幕前就已经成立。Douglas Cardinal 从土地与共同体出发，让建筑把场地的曲线和记忆带进空间。Henrike Naumann 则用家具、墙纸和陈设揭开室内的意识形态：家的审美，从不只是私人的选择。\n\n"
        "Sabine Marcelis 让树脂、玻璃和光线越过家具的边界；Thelma Golden 提醒我们，机构并不是中性的容器，它塑造语境、社区与可见性。Herzog & de Meuron 的艺术空间把创作、聚集和观看拉回同一现场；WangShui 的绘画、LED 与装置则让屏幕长成新的房间。\n\n"
        "这期最值得带走的不是“艺术空间要更好看”，而是：模型、材料、制度与技术，都在提前安排我们的观看。它把每一次观看都还原为一种被设计的关系。下次走进一场展览，你会先注意哪一种空间规则？"
    )
    tags = "#PINUP #PINUP32 #艺术的建筑学 #展览设计 #美术馆建筑 #当代艺术 #建筑杂志 #空间设计"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 32 图片与内容来源
- 第01页：PIN–UP 32 The Architecture of Art 官方期号 {ISSUE_URL}
- 第03页：Wolfgang Tillmans / 1:10 Exhibition Models {TILLMANS_URL}
- 第04页：Douglas Cardinal / St. Mary's Church、Canadian Museum of History {CARDINAL_URL}
- 第05页：Henrike Naumann / Re:Education {NAUMANN_URL}
- 第06页：Sabine Marcelis / resin, glass and light works {MARCELIS_URL}
- 第07页：Thelma Golden / Black spaces and institutional context {GOLDEN_URL}
- 第08页：Herzog & de Meuron / Community Space {HERZOG_URL}
- 第09页：WangShui / Hyaline Seed and LED installations {WANGSHUI_URL}

图片均来自 PIN–UP 官方期号或官方文章页。图片版权归 PIN–UP、原摄影师、建筑师、艺术家与项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-32",
        "issue": "PIN–UP 32 · The Architecture of Art",
        "date": "S/S 2022",
        "core_question": "艺术只发生在墙上吗？",
        "core_thesis": "艺术的建筑学由模型、材料、室内、机构、屏幕与人群共同塑造。",
        "pages": [
            "01 封面：艺术不只挂在墙上",
            "02 中文目录：本期内容导览",
            "03 Wolfgang Tillmans：展览先在模型里发生",
            "04 Douglas Cardinal：建筑先把场地听进去",
            "05 Henrike Naumann：一套沙发也有政治",
            "06 Sabine Marcelis：光能把物件变成空间",
            "07 Thelma Golden：机构不是容器，是立场",
            "08 Herzog & de Meuron：美术馆要让人发生关系",
            "09 WangShui：屏幕正在长出房间",
            "10 收束：艺术不只在墙上发生",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_tillmans(), make_cardinal(), make_naumann(),
        make_marcelis(), make_golden(), make_herzog(), make_wangshui(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 32 cards in {OUT}")


if __name__ == "__main__":
    main()
