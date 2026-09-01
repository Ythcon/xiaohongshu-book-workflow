from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-33"
OUT = ROOT / "output" / "pinup-33"
POST = ROOT / "posts" / "pinup-33" / "post.json"

W, H = 1242, 1660
INK = "#1b1715"
PAPER = "#f1e9dc"
BRICK = "#d9422b"
DENIM = "#29425e"
BUTTER = "#f3ce48"
MINT = "#7da286"
TAN = "#d6b18d"

ISSUE_URL = "https://www.pinupmagazine.org/issues/pinup-33-new-americana-usm-nyc-ben-ganz"
PAIGE_URL = "https://www.pinupmagazine.org/articles/robert-paige-interview"
OLOWU_URL = "https://www.pinupmagazine.org/articles/duro-olowu-interview"
CAPE_URL = "https://www.pinupmagazine.org/articles/cape-cod-essay-bauhaus-new-alchemy-institute-architecture"
BARBIE_URL = "https://www.pinupmagazine.org/articles/barbie-dreamhouse-architectural-survey"
NEWWAVE_URL = "https://www.pinupmagazine.org/articles/new-wave-americana-alexander-may-sized"
BAMBOLE_URL = "https://www.pinupmagazine.org/articles/beb-italia-bambole-grace-ahlbom"
SANDIEGO_URL = "https://www.pinupmagazine.org/articles/san-diego-a-bilateral-city-nicholas-alan-cope"

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
    draw.text((34, 26), "PIN–UP 33 / NEW AMERICANA", font=font(18, True), fill=fg, anchor="lm")
    draw.text((1204, 26), f"{number:02d} / 10", font=font(19, True), fill=fg, anchor="rm")


def source(draw: ImageDraw.ImageDraw, text: str, *, dark: bool = True) -> None:
    draw.rectangle((0, 1601, W, H), fill=rgba(INK if dark else PAPER, 245))
    draw.text((34, 1631), text, font=font(15), fill=PAPER if dark else INK, anchor="lm")


def sticker(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, color: str, *, dark: bool = False) -> None:
    draw.rectangle((x, y, x + 14, y + 46), fill=color)
    draw.text((x + 28, y + 23), text, font=font(18, True), fill=PAPER if dark else INK, anchor="lm")


def framed_cover(canvas: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    image = Image.open(SRC / name).convert("RGBA")
    fitted = shared.fit_inside(image, (x1 - x0, y1 - y0))
    dx = x0 + (x1 - x0 - fitted.width) // 2
    dy = y0 + (y1 - y0 - fitted.height) // 2
    shadow = Image.new("RGBA", fitted.size, rgba(INK, 95))
    canvas.alpha_composite(shadow, (dx + 16, dy + 18))
    canvas.alpha_composite(fitted, (dx, dy))


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, W, 310), fill=BRICK)
    draw.rectangle((0, 310, 276, 1600), fill=DENIM)
    draw.rectangle((276, 310, W, 400), fill=BUTTER)
    draw.text((42, 92), "新美式", font=font(111, True), fill=PAPER)
    draw.text((44, 220), "谁来定义？", font=font(66, True), fill=INK)
    draw.text((50, 488), "NEW", font=font(28, True), fill=BUTTER)
    draw.text((50, 528), "AMERICANA", font=font(20, True), fill=PAPER)
    draw.text((50, 1454), "F/W 2022/23", font=font(18, True), fill=TAN)
    framed_cover(canvas, "cover-01.jpg", (326, 454, 1160, 1538))
    draw.line((326, 424, 1160, 424), fill=INK, width=5)
    draw.text((1160, 388), "PIN–UP 33", font=font(22, True), fill=INK, anchor="ra")
    source(draw, "PIN–UP 33 官方封面｜NEW AMERICANA", dark=True)
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), DENIM)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, W, 294), fill=BUTTER)
    draw.text((42, 112), "本期目录", font=font(93, True), fill=INK)
    draw.text((44, 238), "NEW AMERICANA / 中文导览", font=font(23, True), fill=BRICK)
    draw.text((1208, 106), "33", font=font(168, True), fill=rgba(BRICK, 148), anchor="ra")
    meta(draw, 2, BRICK)
    items = [
        ("03", "ROBERT PAIGE", "图案，也能进入日常"),
        ("04", "DURO OLOWU", "拼接不是混搭，是立场"),
        ("05", "CAPE COD", "越普通的房子，越会发明生活"),
        ("06", "BARBIE DREAMHOUSE", "玩具屋，也在排练现实"),
        ("07", "NEW WAVE", "小物件，也能重写房间"),
        ("08", "LE BAMBOLE", "一把椅子，能占领公园"),
        ("09", "SAN DIEGO", "普通立面，也有美国西岸"),
        ("10", "NEW AMERICANA", "风格从来不是单数"),
    ]
    for i, (number, name, title) in enumerate(items):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        x = 44 + col * 602
        y = 394 + row * 258
        draw.text((x, y), number, font=font(30, True), fill=BUTTER)
        draw.text((x, y + 42), name, font=font(20, True), fill=TAN)
        draw_wrapped(draw, (x, y + 84), title, 498, 33, PAPER, bold=True, spacing=8)
        draw.line((x, y + 206, x + 530, y + 206), fill=rgba(PAPER, 105), width=2)
    draw.text((44, 1502), "谁能设计日常，谁就在重写美国想象。", font=font(28, True), fill=BUTTER)
    source(draw, "PIN–UP 33｜中文目录", dark=True)
    return save(canvas, 2)


def make_paige() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    image_panel(canvas, "paige-01.jpg", (0, 54, W, 890), focal=(0.50, 0.48), darken=0.96,
                label="ROBERT PAIGE / DAKKABAR")
    image_panel(canvas, "paige-02.jpg", (42, 940, 530, 1514), focal=(0.50, 0.50), border=5, border_color=BUTTER)
    image_panel(canvas, "paige-03.jpg", (572, 940, 814, 1514), focal=(0.50, 0.50), border=5, border_color=BUTTER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 3, BRICK)
    draw.rectangle((856, 940, 1204, 1514), fill=BRICK)
    sticker(draw, 890, 978, "ROBERT PAIGE", BUTTER)
    draw.text((890, 1072), "图案", font=font(70, True), fill=PAPER)
    draw.text((890, 1160), "也能进入", font=font(48, True), fill=INK)
    draw.text((890, 1226), "日常", font=font(76, True), fill=PAPER)
    draw.text((890, 1362), "枕头、窗帘与床罩，", font=font(21, True), fill=INK)
    draw.text((890, 1394), "把身份与记忆带进", font=font(21, True), fill=INK)
    draw.text((890, 1426), "每一个家庭房间。", font=font(21, True), fill=INK)
    source(draw, "Robert Paige｜Dakkabar Textiles｜PIN–UP 33", dark=True)
    return save(canvas, 3)


def make_olowu() -> Path:
    canvas = Image.new("RGBA", (W, H), TAN)
    image_panel(canvas, "olowu-02.jpg", (0, 54, W, 900), focal=(0.50, 0.50), darken=0.96,
                label="DURO OLOWU / PATTERN AS EQUALIZER")
    image_panel(canvas, "olowu-01.jpg", (44, 952, 634, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 4, DENIM, light=True)
    draw.rectangle((676, 952, 1204, 1514), fill=DENIM)
    sticker(draw, 712, 990, "DURO OLOWU", BRICK, dark=True)
    draw.text((712, 1084), "拼接", font=font(75, True), fill=PAPER)
    draw.text((712, 1178), "不是混搭", font=font(58, True), fill=BUTTER)
    draw.text((712, 1254), "是立场", font=font(74, True), fill=PAPER)
    draw.text((712, 1386), "不同文化的纹样并置，", font=font(22, True), fill=PAPER)
    draw.text((712, 1418), "不是抹平差异，而是", font=font(22, True), fill=PAPER)
    draw.text((712, 1450), "承认它们能共处。", font=font(22, True), fill=PAPER)
    source(draw, "Duro Olowu｜Pattern and Curation｜PIN–UP 33", dark=True)
    return save(canvas, 4)


def make_cape() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "cape-02.jpg", (0, 54, W, 822), focal=(0.50, 0.50), darken=0.96,
                label="CAPE COD / EXPERIMENTAL ARCHITECTURE")
    image_panel(canvas, "cape-05.jpg", (42, 874, 620, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "cape-08.jpg", (662, 874, 910, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 5, MINT, light=True)
    draw.rectangle((952, 874, 1204, 1514), fill=MINT)
    draw.text((982, 916), "越普通", font=font(53, True), fill=INK)
    draw.text((982, 988), "的房子", font=font(53, True), fill=INK)
    draw.text((982, 1068), "越会", font=font(48, True), fill=PAPER)
    draw.text((982, 1136), "发明", font=font(66, True), fill=INK)
    draw.text((982, 1218), "生活", font=font(66, True), fill=PAPER)
    draw.text((982, 1342), "从沙丘小屋到", font=font(20, True), fill=INK)
    draw.text((982, 1372), "现代主义实验，", font=font(20, True), fill=INK)
    draw.text((982, 1402), "轻装上地，也能", font=font(20, True), fill=INK)
    draw.text((982, 1432), "长出新想象。", font=font(20, True), fill=INK)
    source(draw, "Cape Cod｜Experimental Architecture｜PIN–UP 33", dark=True)
    return save(canvas, 5)


def make_barbie() -> Path:
    canvas = Image.new("RGBA", (W, H), BUTTER)
    image_panel(canvas, "barbie-01.jpg", (0, 54, 726, H), focal=(0.50, 0.50), darken=0.98,
                label="BARBIE DREAMHOUSE / ARCHITECTURAL SURVEY")
    image_panel(canvas, "barbie-04.jpg", (764, 92, 1204, 612), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "barbie-07.jpg", (764, 652, 1204, 1020), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 6, BRICK, light=True)
    draw.rectangle((764, 1060, 1204, 1514), fill=BRICK)
    sticker(draw, 798, 1096, "BARBIE DREAMHOUSE", DENIM)
    draw.text((798, 1188), "玩具屋", font=font(67, True), fill=PAPER)
    draw.text((798, 1274), "也在排练", font=font(49, True), fill=INK)
    draw.text((798, 1340), "现实", font=font(78, True), fill=PAPER)
    draw.text((798, 1440), "房间、角色与无障碍，", font=font(20, True), fill=INK)
    draw.text((798, 1468), "都被打包进一套", font=font(20, True), fill=INK)
    draw.text((798, 1496), "可出售的生活脚本。", font=font(20, True), fill=INK)
    source(draw, "Barbie Dreamhouse｜Architectural Survey｜PIN–UP 33", dark=True)
    return save(canvas, 6)


def make_newwave() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    image_panel(canvas, "newwave-03.jpg", (0, 54, W, 768), focal=(0.50, 0.50), darken=0.96,
                label="NEW WAVE / CONTEMPORARY AMERICAN PRACTICE")
    image_panel(canvas, "newwave-04.jpg", (42, 818, 504, 1514), focal=(0.50, 0.50), border=5, border_color=PAPER)
    image_panel(canvas, "newwave-05.jpg", (546, 818, 834, 1514), focal=(0.50, 0.50), border=5, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 7, TAN)
    draw.rectangle((876, 818, 1204, 1514), fill=PAPER)
    sticker(draw, 908, 856, "NEW WAVE", BRICK)
    draw.text((908, 950), "小物件", font=font(62, True), fill=INK)
    draw.text((908, 1030), "也能重写", font=font(48, True), fill=INK)
    draw.text((908, 1096), "房间", font=font(72, True), fill=BRICK)
    draw.text((908, 1238), "家具不是空间的附件。", font=font(20, True), fill=INK)
    draw.text((908, 1268), "它能决定视线、停留", font=font(20, True), fill=INK)
    draw.text((908, 1298), "与一个房间的情绪。", font=font(20, True), fill=INK)
    source(draw, "New Wave｜Contemporary American Practice｜PIN–UP 33", dark=True)
    return save(canvas, 7)


def make_bambole() -> Path:
    canvas = Image.new("RGBA", (W, H), BRICK)
    image_panel(canvas, "bambole-02.jpg", (0, 54, W, 896), focal=(0.50, 0.50), darken=0.97,
                label="MARIO BELLINI / LE BAMBOLE")
    image_panel(canvas, "bambole-01.jpg", (42, 946, 606, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "bambole-04.jpg", (648, 946, 902, 1514), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 8, BUTTER)
    draw.rectangle((944, 946, 1204, 1514), fill=BUTTER)
    draw.text((974, 986), "一把椅子", font=font(51, True), fill=INK)
    draw.text((974, 1054), "能占领", font=font(50, True), fill=INK)
    draw.text((974, 1122), "公园", font=font(73, True), fill=BRICK)
    draw.text((974, 1260), "当软椅被推到街上，", font=font(20, True), fill=INK)
    draw.text((974, 1290), "家具不再等待被摆放，", font=font(20, True), fill=INK)
    draw.text((974, 1320), "它会主动制造聚集。", font=font(20, True), fill=INK)
    source(draw, "Mario Bellini｜Le Bambole in Tompkins Square Park｜PIN–UP 33", dark=True)
    return save(canvas, 8)


def make_sandiego() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "sandiego-03.jpg", (0, 54, 740, H), focal=(0.50, 0.50), darken=0.96,
                label="SAN DIEGO / AN AMERICAN EDGE CASE")
    image_panel(canvas, "sandiego-06.jpg", (782, 92, 1204, 584), focal=(0.50, 0.50), border=5, border_color=INK)
    image_panel(canvas, "sandiego-09.jpg", (782, 626, 1204, 986), focal=(0.50, 0.50), border=5, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 9, DENIM, light=True)
    draw.rectangle((782, 1028, 1204, 1514), fill=DENIM)
    sticker(draw, 816, 1064, "SAN DIEGO", BUTTER, dark=True)
    draw.text((816, 1158), "普通", font=font(70, True), fill=PAPER)
    draw.text((816, 1244), "立面", font=font(70, True), fill=BUTTER)
    draw.text((816, 1330), "也有西岸", font=font(53, True), fill=PAPER)
    draw.text((816, 1422), "最常见的墙面、楼梯与", font=font(19, True), fill=PAPER)
    draw.text((816, 1450), "棕榈树，也会组成一种", font=font(19, True), fill=PAPER)
    draw.text((816, 1478), "无法复制的地方性。", font=font(19, True), fill=PAPER)
    source(draw, "Nicholas Alan Cope｜San Diego, an American Edge Case｜PIN–UP 33", dark=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 10, BRICK, light=True)
    draw.rectangle((0, 54, W, 440), fill=INK)
    draw.rectangle((0, 440, 446, 1600), fill=BRICK)
    draw.rectangle((446, 440, 728, 1600), fill=BUTTER)
    draw.rectangle((728, 440, W, 1600), fill=DENIM)
    draw.text((44, 116), "风格", font=font(122, True), fill=PAPER)
    draw.text((44, 260), "从来不是单数", font=font(72, True), fill=BUTTER)
    draw.text((74, 526), "人", font=font(99, True), fill=PAPER)
    draw.text((74, 760), "物", font=font(99, True), fill=INK)
    draw.text((74, 994), "地", font=font(99, True), fill=PAPER)
    draw.text((488, 530), "图案", font=font(66, True), fill=INK)
    draw.text((488, 770), "房间", font=font(66, True), fill=BRICK)
    draw.text((488, 1010), "街区", font=font(66, True), fill=INK)
    draw.text((770, 530), "美国风格", font=font(83, True), fill=PAPER)
    draw.text((770, 632), "不该只剩", font=font(53, True), fill=PAPER)
    draw.text((770, 704), "一种脸", font=font(83, True), fill=BUTTER)
    draw.line((772, 842, 1170, 842), fill=BRICK, width=14)
    draw_wrapped(draw, (770, 918), "当图案、地理、消费与人的经验都能进入设计，所谓“新美式”才有不断被改写的可能。", 368, 34, PAPER, bold=True, spacing=12)
    draw.text((770, 1478), "PIN–UP 33 / NEW AMERICANA", font=font(20, True), fill=TAN)
    source(draw, "PIN–UP 33｜美国风格，谁来定义？", dark=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#9c9c94")
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 33｜美国风格，谁来定义？"
    body = (
        "“美式”从来不该只是一套可被复制的符号。PIN–UP 33 的 New Americana 重新追问：谁在决定美国风格，又是谁的日常长期没有被放进设计史？\n\n"
        "Robert Paige 把西非灵感的图案带进美国人的枕头、床罩与窗帘，让身份不必停留在展厅；Duro Olowu 用跨文化纹样并置，证明拼接不是装饰，而是让差异共处的方式。它们都让家庭空间成为文化叙事的现场。\n\n"
        "从 Cape Cod 的沙丘小屋和现代主义实验，到 Barbie Dreamhouse 对房间、角色与无障碍的想象，住宅一直在排练一种生活方式。New Wave 的家具、Le Bambole 在公园里的软椅，以及 Nicholas Alan Cope 镜头下的圣地亚哥立面，也都说明：日常物件与普通街景同样能改写地方感。\n\n"
        "新美式不是统一审美，而是一张持续被补写的地图。设计要做的不是替文化贴标签，而是让更多人、物与土地拥有进入画面的机会。你最希望哪一种日常经验，被重新写进“美式风格”？"
    )
    tags = "#PINUP #PINUP33 #新美式 #美国设计 #家具设计 #建筑杂志 #当代设计 #设计思考"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 33 图片与内容来源
- 第01页：PIN–UP 33 NEW AMERICANA 官方期号页 {ISSUE_URL}
- 第03页：Robert Paige / Dakkabar Textiles {PAIGE_URL}
- 第04页：Duro Olowu / Pattern as an Equalizer {OLOWU_URL}
- 第05页：Cape Cod / Experimental Architecture {CAPE_URL}
- 第06页：Barbie Dreamhouse / Architectural Survey {BARBIE_URL}
- 第07页：New Wave / Contemporary American Practice {NEWWAVE_URL}
- 第08页：Mario Bellini / Le Bambole {BAMBOLE_URL}
- 第09页：Nicholas Alan Cope / San Diego, an American Edge Case {SANDIEGO_URL}

图片均来自 PIN–UP 官方期号页或官方文章页。图片版权归 PIN–UP、原摄影师、建筑师、艺术家与项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-33",
        "issue": "PIN–UP 33 · NEW AMERICANA",
        "date": "F/W 2022/23",
        "core_question": "美国风格，谁来定义？",
        "core_thesis": "新美式不是单一符号，而是图案、地方、商品与生活经验持续争夺和改写的设计地图。",
        "pages": [
            "01 封面：美国风格，谁来定义？",
            "02 中文目录：本期内容导览",
            "03 Robert Paige：图案也能进入日常",
            "04 Duro Olowu：拼接不是混搭，是立场",
            "05 Cape Cod：越普通的房子，越会发明生活",
            "06 Barbie Dreamhouse：玩具屋也在排练现实",
            "07 New Wave：小物件也能重写房间",
            "08 Le Bambole：一把椅子能占领公园",
            "09 San Diego：普通立面也有美国西岸",
            "10 收束：风格从来不是单数",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_paige(), make_olowu(), make_cape(),
        make_barbie(), make_newwave(), make_bambole(), make_sandiego(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 33 cards in {OUT}")


if __name__ == "__main__":
    main()
