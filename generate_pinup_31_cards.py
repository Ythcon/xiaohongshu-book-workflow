from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-31"
OUT = ROOT / "output" / "pinup-31"
POST = ROOT / "posts" / "pinup-31" / "post.json"

W, H = 1242, 1660
INK = "#171714"
PAPER = "#efe9dc"
GRASS = "#96cf39"
ORANGE = "#ff6d45"
COBALT = "#2855d6"
SOIL = "#9d5c38"

ISSUE_URL = "https://www.pinupmagazine.org/issues/pinup-31-mabel-o-wilson-cover"
MABEL_URL = "https://www.pinupmagazine.org/articles/mabel-o-wilson-on-radical-optimism"
PESCE_URL = "https://www.pinupmagazine.org/articles/gaetano-pesce-interview"
TSSUI_URL = "https://archive.pinupmagazine.org/articles/interview-eugene-tssui-architect"
ARGO_URL = "https://archive.pinupmagazine.org/articles/argo-museum-hope-factory-pejman-tehran-ahmadreza-schricker"
CARSON_URL = "https://www.pinupmagazine.org/articles/carson-chan-on-climate-crisis-and-the-challenge-of-the-architectural-canon"
BOND_URL = "https://archive.pinupmagazine.org/articles/special-bond-architects-interview"
MAX_URL = "https://www.pinupmagazine.org/articles/max-von-werz-about-designing-with-coherence-and-honesty-and-his-love-for-mexican-modernism"

shared.SRC = SRC
shared.OUT = OUT


def font(size: int, bold: bool = False):
    return shared.font(size, bold)


def rgba(value: str, alpha: int = 255):
    return shared.rgba(value, alpha)


def photo(canvas, name: str, box: tuple[int, int, int, int], *, focal=(0.5, 0.5), darken=1.0, border=0, border_color=PAPER):
    shared.image_panel(canvas, name, box, focal=focal, darken=darken, border=border, border_color=border_color)


def wrap(draw, xy, text, width, size, fill, *, bold=False, spacing=8):
    shared.draw_wrapped(draw, xy, text, width, size, fill, bold=bold, spacing=spacing)


def save(image: Image.Image, number: int) -> Path:
    path = OUT / f"{number:02d}.jpg"
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def folio(draw: ImageDraw.ImageDraw, number: int, color: str, *, light=False) -> None:
    fg = INK if light else PAPER
    draw.rectangle((0, 0, W, 18), fill=color)
    draw.text((36, 54), "PIN–UP 31", font=font(18, True), fill=fg)
    draw.text((1204, 54), f"{number:02d} / 10", font=font(18, True), fill=fg, anchor="ra")


def cut(draw: ImageDraw.ImageDraw, points, color: str) -> None:
    draw.polygon(points, fill=color)


def block_text(draw, x, y, lines, sizes, fills, *, gap=4) -> int:
    for line, size, fill in zip(lines, sizes, fills):
        draw.text((x, y), line, font=font(size, True), fill=fill)
        y += size + gap
    return y


def cover_fit(name: str, size: tuple[int, int]) -> Image.Image:
    image = Image.open(SRC / name).convert("RGBA")
    return shared.fit_inside(image, size)


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    cut(draw, [(0, 0), (674, 0), (494, H), (0, H)], INK)
    cut(draw, [(0, 1040), (676, 844), (640, 1015), (0, 1282)], GRASS)
    draw.rectangle((468, 110, 1182, 1498), fill=ORANGE)
    cover = cover_fit("issue-01.jpg", (650, 1200))
    shadow = Image.new("RGBA", (cover.width + 48, cover.height + 48), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((24, 24, cover.width + 24, cover.height + 24), fill=rgba(INK, 125))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(12)), (526, 162))
    canvas.alpha_composite(cover, (550, 138))
    draw = ImageDraw.Draw(canvas)
    draw.text((48, 72), "PIN–UP 31", font=font(24, True), fill=GRASS)
    draw.text((48, 172), "乐观", font=font(154, True), fill=PAPER)
    draw.text((48, 342), "不是", font=font(96, True), fill=PAPER)
    draw.text((48, 452), "好心情", font=font(104, True), fill=GRASS)
    draw.rectangle((48, 612, 394, 626), fill=ORANGE)
    wrap(draw, (48, 660), "在危机里继续设计，不是装作没事发生。", 360, 32, PAPER, bold=True, spacing=9)
    draw.text((48, 1450), "RADICAL OPTIMISM", font=font(20, True), fill=PAPER)
    draw.text((48, 1486), "F/W 2021/22", font=font(18, True), fill=GRASS)
    draw.text((1180, 1540), "01 / 10", font=font(19, True), fill=INK, anchor="ra")
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(canvas)
    cut(draw, [(700, 0), (W, 0), (W, H), (944, H)], COBALT)
    draw.text((42, 108), "目录", font=font(126, True), fill=PAPER)
    draw.text((40, 254), "31", font=font(360, True), fill=rgba(GRASS, 255))
    draw.text((88, 570), "RADICAL OPTIMISM", font=font(28, True), fill=ORANGE)
    folio(draw, 2, GRASS)
    items = [
        ("03", "MABEL O. WILSON", "先让隐形结构出现"),
        ("04", "GAETANO PESCE", "未来，得在今天做出来"),
        ("05", "EUGENE TSSUI", "建筑，也该替地球说话"),
        ("06", "ARGO FACTORY", "旧厂房接住新世界"),
        ("07", "BoND ARCHITECTS", "空间要像使用它的人"),
        ("08", "MAX VON WERZ", "材料不该只是背景"),
        ("09", "CARSON CHAN", "生态，是材料的后半生"),
        ("10", "RADICAL OPTIMISM", "一起把未来做出来"),
    ]
    for idx, (no, who, line) in enumerate(items):
        col, row = (0, idx) if idx < 4 else (1, idx - 4)
        x = 52 + col * 570
        y = 694 + row * 202
        draw.text((x, y), no, font=font(23, True), fill=ORANGE)
        draw.text((x + 56, y + 4), who, font=font(17, True), fill=GRASS if col == 0 else PAPER)
        draw.text((x, y + 48), line, font=font(29, True), fill=PAPER)
        draw.line((x, y + 126, x + 506, y + 126), fill=rgba(PAPER, 90), width=2)
    return save(canvas, 2)


def make_mabel() -> Path:
    canvas = Image.new("RGBA", (W, H), GRASS)
    photo(canvas, "mabel-06.jpg", (0, 18, 814, 1074), focal=(0.50, 0.54), darken=0.94)
    photo(canvas, "mabel-04.jpg", (860, 96, 1206, 580), focal=(0.50, 0.50), border=8, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    cut(draw, [(0, 1012), (814, 854), (814, 1600), (0, 1600)], PAPER)
    draw.rectangle((856, 632, 1206, 1498), fill=INK)
    folio(draw, 3, ORANGE, light=True)
    draw.text((42, 1132), "先把隐形的", font=font(64, True), fill=INK)
    draw.text((42, 1212), "东西变成空间", font=font(72, True), fill=COBALT)
    wrap(draw, (46, 1328), "墙以外，语言、规则和记忆，也会决定谁能站在这里。", 690, 28, INK, bold=True, spacing=10)
    draw.text((890, 702), "MABEL", font=font(26, True), fill=GRASS)
    draw.text((890, 758), "O.", font=font(65, True), fill=PAPER)
    draw.text((890, 830), "WILSON", font=font(53, True), fill=PAPER)
    draw.rectangle((890, 930, 1160, 944), fill=ORANGE)
    wrap(draw, (890, 984), "批判系统，也保留想象新秩序的能力。", 256, 24, PAPER, bold=True, spacing=8)
    return save(canvas, 3)


def make_pesce() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    photo(canvas, "pesce-02.jpg", (0, 18, W, 918), focal=(0.50, 0.50), darken=0.90)
    photo(canvas, "pesce-06.jpg", (44, 1014, 628, 1514), focal=(0.49, 0.52), border=7, border_color=ORANGE)
    photo(canvas, "pesce-05.jpg", (674, 1014, 1200, 1514), focal=(0.52, 0.50), border=7, border_color=ORANGE)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 600, W, 918), fill=rgba(INK, 220))
    folio(draw, 4, GRASS)
    block_text(draw, 42, 642, ["未来，得在", "今天做出来"], [76, 84], [PAPER, ORANGE])
    draw.text((44, 868), "GAETANO PESCE", font=font(21, True), fill=GRASS)
    cut(draw, [(838, 1014), (1200, 1014), (1200, 1514), (998, 1514)], ORANGE)
    wrap(draw, (708, 1100), "对他来说，设计不是复刻现在，而是把现在拧向尚未到来的地方。", 418, 29, INK, bold=True, spacing=10)
    return save(canvas, 4)


def make_tssui() -> Path:
    canvas = Image.new("RGBA", (W, H), COBALT)
    photo(canvas, "tssui-06.jpg", (0, 18, 770, H), focal=(0.53, 0.50), darken=0.94)
    photo(canvas, "tssui-02.jpg", (818, 84, 1204, 548), focal=(0.50, 0.50), border=7, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    cut(draw, [(738, 618), (W, 486), (W, H), (742, H)], PAPER)
    folio(draw, 5, ORANGE)
    draw.text((816, 674), "建筑", font=font(82, True), fill=INK)
    draw.text((816, 766), "也该替", font=font(53, True), fill=INK)
    draw.text((816, 832), "地球", font=font(88, True), fill=GRASS)
    draw.text((816, 934), "说话", font=font(88, True), fill=INK)
    draw.rectangle((818, 1048, 1162, 1062), fill=ORANGE)
    draw.text((818, 1098), "EUGENE TSSUI", font=font(21, True), fill=COBALT)
    wrap(draw, (818, 1150), "更轻、更强，先向自然学习，再把答案带回建筑。", 330, 28, INK, bold=True, spacing=10)
    return save(canvas, 5)


def make_argo() -> Path:
    canvas = Image.new("RGBA", (W, H), SOIL)
    photo(canvas, "argo-01.jpg", (0, 18, W, 874), focal=(0.50, 0.48), darken=0.93)
    photo(canvas, "argo-07.jpg", (42, 930, 640, 1510), focal=(0.48, 0.50), border=7, border_color=PAPER)
    photo(canvas, "argo-05.jpg", (684, 930, 1200, 1236), focal=(0.50, 0.50), border=7, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 578, W, 874), fill=rgba(SOIL, 224))
    folio(draw, 6, GRASS)
    draw.text((42, 614), "旧厂房", font=font(80, True), fill=PAPER)
    draw.text((42, 706), "接住新世界", font=font(78, True), fill=GRASS)
    draw.text((44, 848), "ARGO FACTORY / TEHRAN", font=font(21, True), fill=PAPER)
    draw.rectangle((684, 1280, 1200, 1510), fill=GRASS)
    wrap(draw, (720, 1320), "从停产啤酒厂到当代艺术馆，旧结构没有被抹去，它被接进新的公共生活。", 426, 27, INK, bold=True, spacing=9)
    return save(canvas, 6)


def make_bond() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    photo(canvas, "bond-05.jpg", (0, 18, W, 926), focal=(0.50, 0.50), darken=0.96)
    photo(canvas, "bond-06.jpg", (0, 974, 510, 1512), focal=(0.50, 0.50), border=7, border_color=INK)
    photo(canvas, "bond-07.jpg", (556, 974, 906, 1512), focal=(0.50, 0.50), border=7, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((950, 974, 1204, 1512), fill=COBALT)
    folio(draw, 7, ORANGE, light=True)
    draw.rectangle((0, 626, W, 926), fill=rgba(INK, 218))
    draw.text((40, 652), "空间要像", font=font(72, True), fill=PAPER)
    draw.text((40, 742), "使用它的人", font=font(83, True), fill=GRASS)
    draw.text((42, 870), "BoND ARCHITECTS", font=font(21, True), fill=ORANGE)
    wrap(draw, (980, 1030), "拒绝通用答案，让空间把人的身份、关系与欲望接进来。", 180, 25, PAPER, bold=True, spacing=9)
    return save(canvas, 7)


def make_max() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    photo(canvas, "max-04.jpg", (0, 18, 794, H), focal=(0.48, 0.50), darken=0.92)
    photo(canvas, "max-02.jpg", (844, 82, 1204, 474), focal=(0.50, 0.48), border=7, border_color=GRASS)
    photo(canvas, "max-06.jpg", (844, 526, 1204, 808), focal=(0.50, 0.50), border=7, border_color=GRASS)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((840, 858, 1204, 1510), fill=ORANGE)
    folio(draw, 8, GRASS)
    draw.text((872, 916), "材料", font=font(73, True), fill=INK)
    draw.text((872, 1004), "不该只是", font=font(46, True), fill=INK)
    draw.text((872, 1070), "背景", font=font(79, True), fill=PAPER)
    draw.rectangle((872, 1180, 1158, 1194), fill=INK)
    draw.text((872, 1232), "MAX VON WERZ", font=font(20, True), fill=INK)
    wrap(draw, (872, 1282), "木、混凝土和纹理不只服务气氛；它们决定空间如何保持清醒。", 276, 25, INK, bold=True, spacing=8)
    return save(canvas, 8)


def make_carson() -> Path:
    canvas = Image.new("RGBA", (W, H), GRASS)
    photo(canvas, "carson-01.jpg", (0, 18, 680, 900), focal=(0.50, 0.48), darken=0.94)
    photo(canvas, "carson-02.jpg", (728, 18, W, 592), focal=(0.50, 0.48), darken=0.95)
    photo(canvas, "carson-03.jpg", (728, 640, W, 1090), focal=(0.50, 0.48), darken=0.95)
    draw = ImageDraw.Draw(canvas)
    cut(draw, [(0, 876), (680, 774), (680, H), (0, H)], INK)
    draw.rectangle((728, 1138, 1204, 1510), fill=PAPER)
    folio(draw, 9, ORANGE, light=True)
    draw.text((40, 996), "生态", font=font(86, True), fill=GRASS)
    draw.text((40, 1096), "不是风格", font=font(82, True), fill=PAPER)
    draw.text((42, 1220), "CARSON CHAN", font=font(21, True), fill=ORANGE)
    wrap(draw, (42, 1280), "材料从哪里来，谁在加工，它被用完以后去了哪里——这些都属于建筑。", 580, 28, PAPER, bold=True, spacing=10)
    wrap(draw, (764, 1190), "气候问题从来不只发生在立面上。", 370, 33, INK, bold=True, spacing=11)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(canvas)
    cut(draw, [(0, 0), (W, 0), (W, 350), (0, 572)], COBALT)
    cut(draw, [(0, 1114), (W, 908), (W, H), (0, H)], GRASS)
    draw.text((40, 92), "RADICAL", font=font(42, True), fill=PAPER)
    draw.text((40, 152), "OPTIMISM", font=font(42, True), fill=PAPER)
    draw.text((40, 460), "乐观", font=font(160, True), fill=PAPER)
    draw.text((40, 636), "不是好心情", font=font(96, True), fill=ORANGE)
    draw.rectangle((42, 780, 768, 798), fill=GRASS)
    draw.text((40, 850), "是一起把未来", font=font(78, True), fill=PAPER)
    draw.text((40, 946), "做出来", font=font(106, True), fill=PAPER)
    draw.text((42, 1228), "不是“看起来没问题”。", font=font(34, True), fill=INK)
    draw.text((42, 1282), "而是在材料、关系、制度和想象里，持续动工。", font=font(34, True), fill=INK)
    draw.text((42, 1492), "PIN–UP 31 / F/W 2021/22", font=font(20, True), fill=INK)
    draw.text((1198, 1540), "10 / 10", font=font(19, True), fill=INK, anchor="ra")
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), INK)
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 31｜乐观不是好心情"
    body = (
        "如果乐观不是“事情总会变好”，它还能是什么？PIN–UP 31 给出的答案很直接：在危机里继续设计，把未来从一句口号变成可被使用的空间、材料和关系。\n\n"
        "Mabel O. Wilson 让建筑离开单纯的墙与屋顶，去看语言、制度与记忆如何决定可见性。Gaetano Pesce 把设计当成向未来施力的动作；Eugene Tssui 则把自然当作结构课本，重新思考建筑对地球应有的责任。\n\n"
        "Argo Factory 把德黑兰旧啤酒厂改成当代艺术馆，保留旧结构，也接住新的公共生活。BoND Architects 拒绝套用一种“正确”的空间模板，让使用者的身份和关系进入设计。Max von Werz 从木、混凝土和纹理出发，提醒我们材料不是氛围道具。Carson Chan 则把问题推进到材料的来处、劳动和去处：所谓生态，从不只在建筑完成的那一天发生。\n\n"
        "所以，这一期的“激进乐观”并不轻飘。它要求我们承认问题仍在，同时和更多人一起开工。你最想把哪一种未来落实进日常？"
    )
    tags = "#PINUP #PINUP31 #建筑杂志 #建筑设计 #空间设计 #当代建筑 #设计灵感 #建筑改造"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 31 图片与内容来源
- 第01–02、10页：PIN–UP 31《Radical Optimism》官方期号 {ISSUE_URL}
- 第03页：Mabel O. Wilson / Radical Optimism {MABEL_URL}
- 第04页：Gaetano Pesce / interview and works {PESCE_URL}
- 第05页：Eugene Tssui / Casa del Mar、Anquissa House 与创作资料 {TSSUI_URL}
- 第06页：Argo Factory, Tehran / ASA North、Pejman Foundation {ARGO_URL}
- 第07页：BoND Architects / Company Gallery and studio work {BOND_URL}
- 第08页：Max von Werz / Mexico City works and models {MAX_URL}
- 第09页：Carson Chan / climate crisis and architectural canon {CARSON_URL}

图片均来自 PIN–UP 官方期号、官方文章页或其官方档案。图片版权归 PIN–UP、原摄影师、建筑师、艺术家与项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-31",
        "issue": "PIN–UP 31 · Radical Optimism",
        "date": "F/W 2021/22",
        "core_question": "乐观是情绪，还是一种行动？",
        "core_thesis": "激进乐观不是回避危机，而是从材料、空间、社区与想象里共同做出未来。",
        "pages": [
            "01 封面：乐观不是好心情",
            "02 中文目录：Radical Optimism",
            "03 Mabel O. Wilson：让隐形结构出现",
            "04 Gaetano Pesce：今天做未来",
            "05 Eugene Tssui：建筑替地球说话",
            "06 Argo Factory：旧厂房接住新世界",
            "07 BoND Architects：空间像使用它的人",
            "08 Max von Werz：材料不只是背景",
            "09 Carson Chan：生态不是风格",
            "10 收束：一起把未来做出来",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_mabel(), make_pesce(), make_tssui(),
        make_argo(), make_bond(), make_max(), make_carson(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 31 cards in {OUT}")


if __name__ == "__main__":
    main()
