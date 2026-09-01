from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-35"
OUT = ROOT / "output" / "pinup-35"
POST = ROOT / "posts" / "pinup-35" / "post.json"

W, H = 1242, 1660
INK = "#10222a"
PAPER = "#edf0eb"
CYAN = "#19bfd0"
LIME = "#c9ef25"
RUST = "#d97955"
CHARCOAL = "#16202a"

ISSUE_URL = "https://www.pinupmagazine.org/articles/pin-up-2024-a-year-in-review"
AMBASZ_URL = "https://www.pinupmagazine.org/articles/emilio-ambasz-interview"
JAQUE_URL = "https://www.pinupmagazine.org/articles/andres-jaque-interview"
STILLINGS_URL = "https://www.pinupmagazine.org/articles/contested-landscapes-mining-photography-jamey-stillings"
METZGER_URL = "https://www.pinupmagazine.org/articles/against-environment-gustav-metzger-damaged-nature-essay"
LAHORDE_URL = "https://www.pinupmagazine.org/articles/la-horde-interview"
UDDENBERG_URL = "https://www.pinupmagazine.org/articles/anna-uddenberg-bodyscapes-sculpture"
SNODGRASS_URL = "https://www.pinupmagazine.org/articles/cat-snodgrass-interview"

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
    base = PAPER if light else INK
    txt = INK if light else PAPER
    draw.rectangle((0, 0, W, 54), fill=base)
    draw.rectangle((0, 51, W, 54), fill=accent)
    draw.text((34, 25), "PIN–UP 35 / ENVIRONMENTS!", font=font(18, True), fill=txt, anchor="lm")
    draw.text((1204, 25), f"{number:02d} / 10", font=font(19, True), fill=txt, anchor="rm")


def source(draw: ImageDraw.ImageDraw, text: str, *, dark: bool = True) -> None:
    bg = rgba(INK if dark else PAPER, 242)
    fg = PAPER if dark else INK
    draw.rectangle((0, 1601, W, H), fill=bg)
    draw.text((34, 1631), text, font=font(15), fill=fg, anchor="lm")


def edge_tag(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, accent: str, *, dark: bool = False) -> None:
    x, y = xy
    fill = INK if dark else PAPER
    draw.rectangle((x, y, x + 14, y + 48), fill=accent)
    draw.text((x + 28, y + 24), text, font=font(18, True), fill=fill, anchor="lm")


def framed_cover(canvas: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    original = Image.open(SRC / name).convert("RGBA")
    fitted = shared.fit_inside(original, (x1 - x0, y1 - y0))
    shadow = Image.new("RGBA", fitted.size, rgba(INK, 110))
    canvas.alpha_composite(shadow, (x0 + (x1 - x0 - fitted.width) // 2 + 14, y0 + (y1 - y0 - fitted.height) // 2 + 16))
    canvas.alpha_composite(fitted, (x0 + (x1 - x0 - fitted.width) // 2, y0 + (y1 - y0 - fitted.height) // 2))


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, W, 338), fill=CYAN)
    draw.rectangle((0, 338, 228, 1600), fill=INK)
    draw.rectangle((228, 338, W, 416), fill=LIME)
    draw.text((46, 92), "环境", font=font(121, True), fill=INK)
    draw.text((44, 230), "不是背景", font=font(81, True), fill=PAPER)
    draw.text((58, 518), "PIN–UP", font=font(29, True), fill=LIME)
    draw.text((58, 558), "35", font=font(46, True), fill=PAPER)
    draw.text((58, 1488), "F/W 2023/24", font=font(18, True), fill=CYAN)
    framed_cover(canvas, "cover-a.jpg", (274, 456, 1170, 1538))
    draw.line((274, 430, 1170, 430), fill=INK, width=5)
    draw.text((1170, 390), "ENVIRONMENTS!", font=font(22, True), fill=INK, anchor="ra")
    source(draw, "PIN–UP 35 官方封面｜ENVIRONMENTS!", dark=True)
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(canvas)
    draw.text((1190, 112), "35", font=font(330, True), fill=rgba(CYAN, 64), anchor="ra")
    draw.rectangle((38, 208, 364, 228), fill=LIME)
    draw.text((40, 282), "本期目录", font=font(108, True), fill=PAPER)
    draw.text((44, 416), "ENVIRONMENTS! / 中文导览", font=font(24, True), fill=CYAN)
    meta(draw, 2, LIME)
    items = [
        ("03", "EMILIO AMBASZ", "绿色，要能被进入"),
        ("04", "ANDRES JAQUE", "水，不该躲在墙后"),
        ("05", "JAMEY STILLINGS", "矿场，也在你口袋里"),
        ("06", "GUSTAV METZGER", "受损自然，不能被美化"),
        ("07", "(LA)HORDE", "身体，也是一种环境"),
        ("08", "ANNA UDDENBERG", "家具，也会规训身体"),
        ("09", "CAT SNODGRASS", "光线，会改写空间"),
        ("10", "ENVIRONMENTS!", "环境，不在外面"),
    ]
    for i, (number, name, title) in enumerate(items):
        col, row = (0, i) if i < 4 else (1, i - 4)
        x = 44 + col * 602
        y = 510 + row * 236
        draw.text((x, y), number, font=font(28, True), fill=LIME)
        draw.text((x, y + 42), name, font=font(20, True), fill=CYAN)
        draw_wrapped(draw, (x, y + 82), title, 502, 33, PAPER, bold=True, spacing=8)
        draw.line((x, y + 188, x + 528, y + 188), fill=rgba(PAPER, 90), width=2)
    draw.text((44, 1490), "环境，是一套正在作用的关系。", font=font(31, True), fill=LIME)
    source(draw, "PIN–UP 35｜中文目录", dark=True)
    return save(canvas, 2)


def make_ambasz() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "03-ambasz-b.jpg", (0, 54, W, 942), focal=(0.52, 0.52), darken=0.98,
                label="EMILIO AMBASZ / ACROS FUKUOKA")
    image_panel(canvas, "03-ambasz-a.jpg", (40, 1000, 414, 1514), focal=(0.52, 0.48), border=4, border_color=INK)
    image_panel(canvas, "03-ambasz-hero.jpg", (452, 1000, 748, 1514), focal=(0.50, 0.48), border=4, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 3, LIME, light=True)
    draw.rectangle((786, 1000, 1204, 1514), fill=INK)
    edge_tag(draw, (820, 1036), "EMILIO AMBASZ", LIME, dark=False)
    draw.text((820, 1120), "绿色", font=font(80, True), fill=PAPER)
    draw.text((820, 1216), "要能被", font=font(55, True), fill=CYAN)
    draw.text((820, 1286), "进入", font=font(80, True), fill=LIME)
    draw_wrapped(draw, (820, 1402), "屋顶与公共坡地合并，植物成为城市可步入的地形。", 332, 24, PAPER, bold=True, spacing=8)
    source(draw, "Emilio Ambasz｜ACROS Fukuoka｜PIN–UP 35", dark=True)
    return save(canvas, 3)


def make_jaque() -> Path:
    canvas = Image.new("RGBA", (W, H), CYAN)
    image_panel(canvas, "04-jaque-a.jpg", (0, 54, 778, H), focal=(0.50, 0.50), darken=0.96,
                label="ANDRES JAQUE / COSMO")
    image_panel(canvas, "04-jaque-hero.jpg", (816, 92, 1204, 606), focal=(0.50, 0.46), border=5, border_color=INK)
    image_panel(canvas, "04-jaque-b.jpg", (816, 644, 1204, 990), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 4, LIME)
    draw.rectangle((816, 1028, 1204, 1516), fill=PAPER)
    edge_tag(draw, (850, 1062), "ANDRES JAQUE", CYAN, dark=True)
    draw.text((850, 1152), "水", font=font(100, True), fill=INK)
    draw.text((966, 1152), "不该", font=font(56, True), fill=INK)
    draw.text((850, 1270), "躲在墙后", font=font(68, True), fill=RUST)
    draw.text((850, 1390), "COSMO把水处理搬到", font=font(22, True), fill=INK)
    draw.text((850, 1424), "人眼前，让基础设施", font=font(22, True), fill=INK)
    draw.text((850, 1458), "成为公共空间。", font=font(22, True), fill=INK)
    source(draw, "Andres Jaque｜COSMO｜PIN–UP 35", dark=True)
    return save(canvas, 4)


def make_stillings() -> Path:
    canvas = Image.new("RGBA", (W, H), CHARCOAL)
    image_panel(canvas, "05-stillings-a.jpg", (0, 54, W, 850), focal=(0.50, 0.50), darken=0.93,
                label="JAMEY STILLINGS / CONTESTED LANDSCAPES")
    image_panel(canvas, "05-stillings-hero.jpg", (42, 900, 650, 1516), focal=(0.50, 0.50), border=5, border_color=PAPER)
    image_panel(canvas, "05-stillings-b.jpg", (694, 900, 894, 1516), focal=(0.50, 0.50), border=5, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 5, RUST)
    draw.rectangle((938, 900, 1204, 1516), fill=LIME)
    edge_tag(draw, (970, 936), "JAMEY STILLINGS", RUST, dark=True)
    draw.text((970, 1036), "矿场", font=font(62, True), fill=INK)
    draw.text((970, 1116), "也在", font=font(52, True), fill=INK)
    draw.text((970, 1184), "你口袋里", font=font(53, True), fill=RUST)
    draw.text((970, 1314), "铜、锂与能源设施", font=font(20, True), fill=INK)
    draw.text((970, 1348), "连接着每一件看似", font=font(20, True), fill=INK)
    draw.text((970, 1382), "轻巧的日常设备。", font=font(20, True), fill=INK)
    source(draw, "Jamey Stillings｜Contested Landscapes｜PIN–UP 35", dark=True)
    return save(canvas, 5)


def make_metzger() -> Path:
    canvas = Image.new("RGBA", (W, H), RUST)
    image_panel(canvas, "06-metzger-a.png", (0, 54, W, 904), focal=(0.50, 0.46), darken=0.98,
                label="GUSTAV METZGER / DAMAGED NATURE")
    image_panel(canvas, "06-metzger-hero.jpg", (42, 958, 592, 1516), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "06-metzger-b.jpg", (632, 958, 896, 1516), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 6, LIME)
    draw.rectangle((936, 958, 1204, 1516), fill=INK)
    edge_tag(draw, (968, 994), "GUSTAV METZGER", RUST, dark=False)
    draw.text((968, 1080), "受损", font=font(70, True), fill=PAPER)
    draw.text((968, 1168), "自然", font=font(78, True), fill=LIME)
    draw.text((968, 1264), "不能被美化", font=font(41, True), fill=PAPER)
    draw_wrapped(draw, (968, 1362), "面对破坏本身，比用温和的绿色语言遮住它更重要。", 194, 22, PAPER, bold=True, spacing=8)
    source(draw, "Gustav Metzger｜Damaged Nature｜PIN–UP 35", dark=True)
    return save(canvas, 6)


def make_lahorde() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "07-lahorde-hero.jpg", (0, 54, W, 938), focal=(0.50, 0.50), darken=0.94,
                label="(LA)HORDE / ROOM WITH A VIEW")
    image_panel(canvas, "07-lahorde-a.jpg", (44, 992, 606, 1516), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "07-lahorde-b.jpg", (650, 992, 910, 1516), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 7, CYAN, light=True)
    draw.rectangle((954, 992, 1204, 1516), fill=CYAN)
    edge_tag(draw, (982, 1028), "(LA)HORDE", LIME, dark=True)
    draw.text((982, 1122), "身体", font=font(69, True), fill=INK)
    draw.text((982, 1210), "也是", font=font(50, True), fill=INK)
    draw.text((982, 1276), "环境", font=font(69, True), fill=RUST)
    draw_wrapped(draw, (982, 1386), "动作穿过采石场、舞台与机构，重新测量空间的边界。", 182, 22, INK, bold=True, spacing=8)
    source(draw, "(LA)Horde｜Room With A View｜PIN–UP 35", dark=True)
    return save(canvas, 7)


def make_uddenberg() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    image_panel(canvas, "08-uddenberg-hero.jpg", (0, 54, 744, H), focal=(0.50, 0.50), darken=0.97,
                label="ANNA UDDENBERG / ECONOMY PLUS")
    image_panel(canvas, "08-uddenberg-a.jpg", (782, 92, 1204, 608), focal=(0.50, 0.50), border=5, border_color=PAPER)
    image_panel(canvas, "08-uddenberg-b.jpg", (782, 646, 1204, 1000), focal=(0.50, 0.50), border=5, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 8, RUST)
    draw.rectangle((782, 1038, 1204, 1516), fill=RUST)
    edge_tag(draw, (816, 1072), "ANNA UDDENBERG", CYAN, dark=True)
    draw.text((816, 1162), "家具", font=font(73, True), fill=INK)
    draw.text((816, 1254), "也会规训", font=font(51, True), fill=INK)
    draw.text((816, 1324), "身体", font=font(75, True), fill=PAPER)
    draw_wrapped(draw, (816, 1428), "座椅、设备与姿势一起规定：身体该如何停留、移动与被观看。", 338, 22, INK, bold=True, spacing=8)
    source(draw, "Anna Uddenberg｜Economy Plus｜PIN–UP 35", dark=True)
    return save(canvas, 8)


def make_snodgrass() -> Path:
    canvas = Image.new("RGBA", (W, H), LIME)
    image_panel(canvas, "09-snodgrass-hero.jpg", (0, 54, W, 868), focal=(0.50, 0.50), darken=0.97,
                label="CAT SNODGRASS / LIGHT AND SPACE")
    image_panel(canvas, "09-snodgrass-a.jpg", (42, 922, 614, 1516), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "09-snodgrass-b.jpg", (654, 922, 882, 1516), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 9, CYAN, light=True)
    draw.rectangle((922, 922, 1204, 1516), fill=PAPER)
    edge_tag(draw, (956, 958), "CAT SNODGRASS", LIME, dark=True)
    draw.text((956, 1058), "光线", font=font(70, True), fill=INK)
    draw.text((956, 1146), "会改写", font=font(50, True), fill=INK)
    draw.text((956, 1214), "空间", font=font(70, True), fill=CYAN)
    draw_wrapped(draw, (956, 1340), "颜色、尺度与光并不在后面，它们先决定身体如何停留。", 212, 23, INK, bold=True, spacing=8)
    source(draw, "Cat Snodgrass｜Light and Space｜PIN–UP 35", dark=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 10, LIME, light=True)
    draw.rectangle((0, 54, 286, 1600), fill=CYAN)
    draw.rectangle((286, 54, 440, 1600), fill=LIME)
    draw.rectangle((440, 54, 736, 1600), fill=INK)
    draw.rectangle((736, 54, W, 1600), fill=PAPER)
    draw.text((64, 146), "环境", font=font(111, True), fill=INK)
    draw.text((64, 274), "不在", font=font(74, True), fill=INK)
    draw.text((64, 362), "外面", font=font(92, True), fill=RUST)
    draw.text((482, 182), "水", font=font(106, True), fill=LIME)
    draw.text((482, 428), "材料", font=font(72, True), fill=PAPER)
    draw.text((482, 650), "身体", font=font(72, True), fill=CYAN)
    draw.text((482, 872), "权力", font=font(72, True), fill=LIME)
    draw.text((782, 236), "环境", font=font(118, True), fill=INK)
    draw.text((782, 382), "不是绿化", font=font(61, True), fill=INK)
    draw.text((782, 466), "的背景", font=font(69, True), fill=RUST)
    draw.line((784, 586, 1160, 586), fill=CYAN, width=14)
    draw_wrapped(draw, (782, 660), "它由资源如何流动、身体如何被安放，以及谁能决定空间的规则共同构成。", 356, 35, INK, bold=True, spacing=12)
    draw_wrapped(draw, (782, 1138), "设计真正要改变的，不只是表面看起来更绿，而是这套关系本身。", 356, 33, INK, bold=True, spacing=12)
    draw.text((782, 1476), "PIN–UP 35 / ENVIRONMENTS!", font=font(20, True), fill=RUST)
    source(draw, "PIN–UP 35｜环境不是背景", dark=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#8b9692")
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 35｜环境不是背景"
    body = (
        "环境常被理解成一片需要节能、绿化和美化的背景，但 PIN–UP 35 问得更彻底：谁在塑造环境，又是谁承担它的后果？\n\n"
        "Emilio Ambasz 让公共绿地成为建筑可进入的地形；Andres Jaque 把水处理管线搬到人们眼前；Jamey Stillings 从高空拍下矿场与能源设施，提醒我们手中的设备也有一片被改写的远方。它们都不把“环境”看作建筑外面的自然。\n\n"
        "Gustav Metzger 坚持面对受损自然，拒绝用温和的绿色语言遮住破坏；(LA)Horde 和 Anna Uddenberg 则把身体放回环境中心，让动作、姿势与制度共同构成空间。Cat Snodgrass 的光与色也说明，室内不是中性的容器。\n\n"
        "环境从来不是背景。它在水、材料、身体、劳动和权力关系里持续发生。设计若只追求看起来更绿，往往错过了真正需要被改变的系统。从一条被隐藏的管线到一块被开采的矿石，空间的边界比墙面更远，也比想象中更贴近每天的生活。你希望身边哪一处环境，先被重新设计？"
    )
    tags = "#PINUP #PINUP35 #环境设计 #生态建筑 #公共空间 #当代建筑 #建筑杂志 #设计思考"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 35 图片与内容来源
- 第01页：PIN–UP 35 ENVIRONMENTS! 官方期号回顾 {ISSUE_URL}
- 第03页：Emilio Ambasz / ACROS Fukuoka {AMBASZ_URL}
- 第04页：Andres Jaque / COSMO {JAQUE_URL}
- 第05页：Jamey Stillings / Contested Landscapes {STILLINGS_URL}
- 第06页：Gustav Metzger / Damaged Nature {METZGER_URL}
- 第07页：(LA)Horde / Room With A View {LAHORDE_URL}
- 第08页：Anna Uddenberg / Economy Plus {UDDENBERG_URL}
- 第09页：Cat Snodgrass / Light and Space {SNODGRASS_URL}

图片均来自 PIN–UP 官方文章或官方期号页。图片版权归 PIN–UP、原摄影师、建筑师、艺术家与项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-35",
        "issue": "PIN–UP 35 · ENVIRONMENTS!",
        "date": "F/W 2023/24",
        "core_question": "环境只是背景吗？",
        "core_thesis": "环境不是绿色外壳，而是水、资源、身体、权力与空间互相作用的现场。",
        "pages": [
            "01 封面：环境不是背景",
            "02 中文目录：本期内容导览",
            "03 Emilio Ambasz：绿色要能被进入",
            "04 Andres Jaque：水不该躲在墙后",
            "05 Jamey Stillings：矿场也在你口袋里",
            "06 Gustav Metzger：受损自然不能被美化",
            "07 (LA)Horde：身体也是一种环境",
            "08 Anna Uddenberg：家具也会规训身体",
            "09 Cat Snodgrass：光线会改写空间",
            "10 收束：环境不在外面",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_ambasz(), make_jaque(), make_stillings(),
        make_metzger(), make_lahorde(), make_uddenberg(), make_snodgrass(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 35 cards in {OUT}")


if __name__ == "__main__":
    main()
