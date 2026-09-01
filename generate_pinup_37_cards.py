from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-37"
OUT = ROOT / "output" / "pinup-37"
POST = ROOT / "posts" / "pinup-37" / "post.json"

W, H = 1242, 1660
BLACK = "#12110e"
PAPER = "#f3efe4"
WARM = "#ded6c6"
RED = "#ed3f2e"
BLUE = "#2448b8"
YELLOW = "#ffe935"
GREEN = "#c8f146"

ISSUE_URL = "https://www.pinupmagazine.org/issues/pin-up-37-museum-issue"
WEEMS_URL = "https://www.pinupmagazine.org/articles/carrie-mae-weems-museums"
PHANTOM_URL = "https://www.pinupmagazine.org/articles/phantom-museums-museum-of-modern-art-warsaw-dasa-anosova"
LIVING_URL = "https://www.pinupmagazine.org/articles/living-museums-plimoth-patuxet/?preview=true"
HASEGAWA_URL = "https://www.pinupmagazine.org/articles/itsuko-hasegawa-interview"
RADIC_URL = "https://www.pinupmagazine.org/articles/smiljan-radic-interview"
SYMS_URL = "https://www.pinupmagazine.org/articles/martine-syms-interview-total-lafayette-anticipations-paris"
DREAM_URL = "https://www.pinupmagazine.org/articles/pin-up-2024-a-year-in-review"

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


def cover_fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return shared.fit_inside(image, size)


def save(image: Image.Image, number: int) -> Path:
    path = OUT / f"{number:02d}.jpg"
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def meta(draw: ImageDraw.ImageDraw, number: int, accent: str) -> None:
    draw.rectangle((0, 0, W, 54), fill=BLACK)
    draw.text((34, 27), "PIN–UP 37 / MUSEUM ISSUE", font=font(18, True), fill=PAPER, anchor="lm")
    draw.rectangle((1004, 0, W, 54), fill=accent)
    draw.text((1123, 27), f"{number:02d} / 10", font=font(19, True), fill=BLACK, anchor="mm")


def source(draw: ImageDraw.ImageDraw, text: str, *, light: bool = True) -> None:
    draw.rectangle((0, 1601, W, H), fill=rgba(BLACK if light else PAPER, 240))
    draw.text((34, 1631), text, font=font(15), fill=PAPER if light else BLACK, anchor="lm")


def label(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, fill: str = BLACK, fg: str = PAPER) -> None:
    used = font(18, True)
    width = draw.textbbox((0, 0), text, font=used)[2]
    draw.rectangle((x, y, x + width + 30, y + 39), fill=fill)
    draw.text((x + 15, y + 20), text, font=used, fill=fg, anchor="lm")


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    cover = cover_fit(Image.open(SRC / "book-cover.jpg").convert("RGB"), (690, 1370))
    shadow = Image.new("RGBA", (cover.width + 64, cover.height + 64), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((32, 32, cover.width + 32, cover.height + 32), fill=rgba(BLACK, 128))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(15)), (79, 110))
    canvas.alpha_composite(cover.convert("RGBA"), (111, 110))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((846, 0, W, H), fill=BLACK)
    draw.rectangle((808, 108, 846, 734), fill=RED)
    draw.text((890, 198), "博物馆", font=font(104, True), fill=PAPER, anchor="la")
    draw.text((890, 446), "该消失", font=font(94, True), fill=RED, anchor="la")
    draw.text((890, 558), "吗？", font=font(128, True), fill=YELLOW, anchor="la")
    draw.rectangle((890, 760, 1168, 772), fill=YELLOW)
    draw_wrapped(draw, (890, 812), "不是收藏物件的盒子，而是决定记忆、公共性与想象力如何发生的场所。", 258, 28, PAPER, bold=True, spacing=11)
    draw.text((890, 1324), "PIN–UP", font=font(37, True), fill=YELLOW)
    draw.text((890, 1378), "37", font=font(75, True), fill=PAPER)
    draw.text((890, 1476), "MUSEUM ISSUE", font=font(20, True), fill=PAPER)
    source(draw, "PIN–UP 37 官方封面｜Museum Issue", light=False)
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    draw = ImageDraw.Draw(canvas)
    draw.text((1180, 432), "37", font=font(600, True), fill=rgba(RED, 82), anchor="ra")
    draw.rectangle((0, 54, W, 306), fill=RED)
    draw.text((40, 84), "本期目录", font=font(112, True), fill=BLACK)
    draw.text((44, 246), "MUSEUM ISSUE / 中文导览", font=font(24, True), fill=BLACK)
    meta(draw, 2, YELLOW)
    items = [
        ("03", "CARRIE MAE WEEMS", "博物馆的外墙，也会说话"),
        ("04", "PHANTOM MUSEUM", "失去的，也能被展示"),
        ("05", "PLIMOTH PATUXET", "历史不能只隔着玻璃看"),
        ("06", "ITSUKO HASEGAWA", "文化空间，也可以像自然"),
        ("07", "SMILJAN RADIĆ", "博物馆，更像一座广场"),
        ("08", "MARTINE SYMS", "谁能在馆里开口"),
        ("09", "DREAM HOMES", "展览，也能收下生活"),
        ("10", "MUSEUM ISSUE", "给想象力留一把椅子"),
    ]
    for i, (number, name, text) in enumerate(items):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        x = 44 + col * 596
        y = 374 + row * 270
        draw.text((x, y), number, font=font(27, True), fill=YELLOW)
        draw.text((x, y + 42), name, font=font(20, True), fill=GREEN)
        draw_wrapped(draw, (x, y + 82), text, 490, 32, PAPER, bold=True, spacing=8)
        draw.line((x, y + 208, x + 522, y + 208), fill=rgba(PAPER, 80), width=2)
    draw.text((44, 1505), "博物馆，应当收藏什么？", font=font(33, True), fill=RED)
    source(draw, "PIN–UP 37｜中文目录", light=True)
    return save(canvas, 2)


def make_weems() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "03-weems-hero.jpg", (0, 54, W, 862), focal=(0.50, 0.43), darken=0.84,
                label="CARRIE MAE WEEMS / MUSEUMS SERIES")
    image_panel(canvas, "03-weems-a.jpg", (38, 912, 414, 1516), focal=(0.52, 0.50), border=4, border_color=BLACK)
    image_panel(canvas, "03-weems-b.jpg", (440, 912, 712, 1516), focal=(0.48, 0.50), border=4, border_color=BLACK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 3, RED)
    draw.rectangle((744, 912, 1204, 1516), fill=BLACK)
    draw.text((782, 950), "外墙", font=font(83, True), fill=PAPER)
    draw.text((782, 1052), "也会", font=font(83, True), fill=RED)
    draw.text((782, 1154), "说话", font=font(83, True), fill=PAPER)
    draw_wrapped(draw, (782, 1306), "Weems 把镜头对准机构外部：谁能进入、谁被排除，都写在门面上。", 370, 25, PAPER, bold=True, spacing=9)
    source(draw, "Carrie Mae Weems, Museums Series｜PIN–UP 37", light=True)
    return save(canvas, 3)


def make_phantom() -> Path:
    canvas = Image.new("RGBA", (W, H), WARM)
    image_panel(canvas, "04-phantom-a.jpg", (0, 54, 734, 922), focal=(0.50, 0.49), darken=0.96,
                label="PHANTOM MUSEUM / DASA ANOSOVA")
    image_panel(canvas, "04-phantom-b.jpg", (766, 54, W, 630), focal=(0.50, 0.50), border=4, border_color=BLACK)
    image_panel(canvas, "04-phantom-hero.jpg", (766, 662, W, 1116), focal=(0.50, 0.50), border=4, border_color=BLACK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 4, BLUE)
    draw.rectangle((0, 958, 734, 1548), fill=BLACK)
    draw.text((38, 996), "没有原件", font=font(77, True), fill=PAPER)
    draw.text((38, 1094), "也能", font=font(77, True), fill=YELLOW)
    draw.text((38, 1192), "记得", font=font(102, True), fill=RED)
    draw_wrapped(draw, (38, 1338), "失窃文物以记忆、手作和概念复制的方式，重新回到展厅。", 626, 27, PAPER, bold=True, spacing=10)
    draw.rectangle((766, 1148, 1204, 1548), fill=RED)
    draw_wrapped(draw, (804, 1188), "文化被掠夺时，展览也能成为一种抵抗遗忘的装置。", 354, 36, BLACK, bold=True, spacing=12)
    source(draw, "Dasa Anosova, Phantom Museum｜PIN–UP 37", light=True)
    return save(canvas, 4)


def make_living() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    image_panel(canvas, "05-living-hero.jpg", (0, 54, W, 802), focal=(0.50, 0.48), darken=0.88,
                label="PLIMOTH PATUXET / LIVING MUSEUM")
    image_panel(canvas, "05-living-a.jpg", (42, 848, 480, 1504), focal=(0.52, 0.50), border=4, border_color=PAPER)
    image_panel(canvas, "05-living-b.jpg", (514, 848, 832, 1504), focal=(0.50, 0.48), border=4, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 5, GREEN)
    draw.rectangle((866, 848, 1204, 1504), fill=RED)
    draw.text((900, 886), "历史", font=font(74, True), fill=BLACK)
    draw.text((900, 976), "不能", font=font(74, True), fill=BLACK)
    draw.text((900, 1066), "隔着看", font=font(74, True), fill=BLACK)
    draw_wrapped(draw, (900, 1204), "生活博物馆把历史放回身体、劳动和日常对话里。", 260, 26, BLACK, bold=True, spacing=9)
    draw.rectangle((42, 1528, 1204, 1548), fill=GREEN)
    source(draw, "Plimoth Patuxet Museums｜PIN–UP 37", light=True)
    return save(canvas, 5)


def make_hasegawa() -> Path:
    canvas = Image.new("RGBA", (W, H), BLUE)
    image_panel(canvas, "06-hasegawa-hero.jpg", (0, 54, 770, H), focal=(0.50, 0.50), darken=0.94,
                label="ITSUKO HASEGAWA / SHONANDAI CULTURAL CENTER")
    image_panel(canvas, "06-hasegawa-a.jpg", (804, 88, 1204, 572), focal=(0.50, 0.50), border=4, border_color=BLACK)
    image_panel(canvas, "06-hasegawa-b.jpg", (804, 604, 1204, 1014), focal=(0.50, 0.50), border=4, border_color=BLACK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 6, YELLOW)
    draw.rectangle((804, 1048, 1204, 1548), fill=YELLOW)
    draw.text((838, 1084), "文化空间", font=font(57, True), fill=BLACK)
    draw.text((838, 1156), "也能像", font=font(57, True), fill=BLACK)
    draw.text((838, 1228), "自然", font=font(91, True), fill=RED)
    draw_wrapped(draw, (838, 1364), "场地、社区与儿童活动，一起决定一座文化中心的形状。", 320, 25, BLACK, bold=True, spacing=9)
    source(draw, "Itsuko Hasegawa, Shonandai Cultural Center｜PIN–UP 37", light=True)
    return save(canvas, 6)


def make_radic() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "07-radic-a.jpg", (0, 54, W, 760), focal=(0.50, 0.50), darken=0.89,
                label="SMILJAN RADIĆ / MUSEUM AS PUBLIC SUPPORT")
    image_panel(canvas, "07-radic-b.jpg", (38, 806, 628, 1504), focal=(0.50, 0.50), border=4, border_color=BLACK)
    image_panel(canvas, "07-radic-hero.jpg", (666, 806, 900, 1504), focal=(0.50, 0.50), border=4, border_color=BLACK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 7, RED)
    draw.rectangle((938, 806, 1204, 1504), fill=BLACK)
    draw.text((968, 844), "更像", font=font(57, True), fill=PAPER)
    draw.text((968, 920), "一座", font=font(57, True), fill=RED)
    draw.text((968, 996), "广场", font=font(76, True), fill=PAPER)
    draw_wrapped(draw, (968, 1136), "活动、临时性与可变墙面，比纪念碑式的收藏更重要。", 204, 25, PAPER, bold=True, spacing=9)
    draw.line((968, 1424, 1168, 1424), fill=YELLOW, width=12)
    source(draw, "Smiljan Radić interview｜PIN–UP 37", light=True)
    return save(canvas, 7)


def make_syms() -> Path:
    canvas = Image.new("RGBA", (W, H), RED)
    image_panel(canvas, "08-syms-hero.jpg", (0, 54, W, 790), focal=(0.50, 0.48), darken=0.87,
                label="MARTINE SYMS / TOTAL LAFAYETTE")
    image_panel(canvas, "08-syms-a.jpg", (40, 834, 508, 1504), focal=(0.50, 0.50), border=4, border_color=BLACK)
    image_panel(canvas, "08-syms-b.jpg", (544, 834, 862, 1504), focal=(0.50, 0.50), border=4, border_color=BLACK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 8, GREEN)
    draw.rectangle((900, 834, 1204, 1504), fill=BLACK)
    draw.text((932, 872), "谁能", font=font(65, True), fill=PAPER)
    draw.text((932, 956), "在馆里", font=font(65, True), fill=GREEN)
    draw.text((932, 1040), "开口", font=font(82, True), fill=PAPER)
    draw_wrapped(draw, (932, 1192), "身份和叙事，不该只由机构单向决定。", 236, 28, PAPER, bold=True, spacing=10)
    source(draw, "Martine Syms, Total Lafayette｜PIN–UP 37", light=True)
    return save(canvas, 8)


def make_dream() -> Path:
    canvas = Image.new("RGBA", (W, H), GREEN)
    image_panel(canvas, "09-dream-hero.jpg", (0, 54, 724, H), focal=(0.50, 0.50), darken=0.93,
                label="DREAM HOMES / COOPER HEWITT")
    image_panel(canvas, "09-dream-a.jpg", (760, 88, 1204, 600), focal=(0.50, 0.50), border=4, border_color=BLACK)
    image_panel(canvas, "09-dream-b.jpg", (760, 632, 1204, 1080), focal=(0.50, 0.50), border=4, border_color=BLACK)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 9, RED)
    draw.rectangle((760, 1112, 1204, 1548), fill=BLACK)
    draw.text((796, 1148), "展览", font=font(74, True), fill=PAPER)
    draw.text((796, 1242), "也能收下", font=font(59, True), fill=RED)
    draw.text((796, 1320), "生活", font=font(87, True), fill=YELLOW)
    draw_wrapped(draw, (796, 1432), "酷儿共同居住，被当作现实而非旁注。", 350, 24, PAPER, bold=True, spacing=8)
    source(draw, "Michael Cukr, Dream Homes / Cooper Hewitt｜PIN–UP 37", light=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 10, RED)
    draw.ellipse((78, 132, 1164, 1218), fill=RED)
    draw.ellipse((228, 282, 1014, 1068), outline=BLACK, width=22)
    draw.text((621, 432), "MUSEUM?", font=font(114, True), fill=BLACK, anchor="mm")
    draw.text((621, 586), "不是封存", font=font(70, True), fill=PAPER, anchor="mm")
    draw.text((621, 676), "而是进入", font=font(70, True), fill=PAPER, anchor="mm")
    draw.rectangle((40, 1228, 1202, 1548), fill=BLACK)
    draw.text((74, 1264), "给想象力", font=font(78, True), fill=PAPER)
    draw.text((74, 1358), "留一把椅子", font=font(78, True), fill=YELLOW)
    draw_wrapped(draw, (78, 1472), "让更多记忆、身体与冲突，能进入同一段叙述。", 1070, 27, PAPER, bold=True, spacing=8)
    source(draw, "PIN–UP 37 / Museum Issue", light=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#bdb7ae")
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 37｜博物馆该消失吗？"
    body = (
        "博物馆最容易被想成一座存放珍品的建筑，但 PIN–UP 37 反过来追问：它究竟在保存什么，又在替谁讲述历史？\n\n"
        "Carrie Mae Weems 把镜头对准博物馆外墙，让制度本身成为被观看的对象；The Phantom Museum 以失窃文物的概念复制品抵抗文化抹除；Plimoth Patuxet 则把历史放回身体、劳动和日常对话中。它们都提醒我们，展示不是中立动作。\n\n"
        "长谷川逸子让文化中心像一种可参与的第二自然：场地、社区和儿童活动共同决定建筑。Smiljan Radić 设想的博物馆更接近公共广场，而不是被宝物塞满的纪念碑。Martine Syms 与 Cooper Hewitt 的 Dream Homes 又把声音、身份和共同居住带进机构内部。\n\n"
        "好博物馆不只收藏物件，也要容纳不同的记忆、身体与冲突。它必须允许历史被重新看见，也允许未来还没有名字。你最希望博物馆展示哪一种当下生活？当展柜、墙面和机构语言都被重新看见，博物馆才不只是结论的陈列室，而能成为让陌生经验相遇、争论和继续被书写的公共现场。"
    )
    tags = "#PINUP #PINUP37 #博物馆设计 #展览设计 #建筑杂志 #当代艺术 #公共空间 #建筑设计"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 37 图片与内容来源
- 第01页：PIN–UP 37 官方期号页 {ISSUE_URL}
- 第03页：Carrie Mae Weems, Museums Series {WEEMS_URL}
- 第04页：Daša Anosova, Phantom Museum {PHANTOM_URL}
- 第05页：Plimoth Patuxet living museums {LIVING_URL}
- 第06页：Itsuko Hasegawa interview / Shōnandai Cultural Center {HASEGAWA_URL}
- 第07页：Smiljan Radić interview {RADIC_URL}
- 第08页：Martine Syms, Total Lafayette {SYMS_URL}
- 第09页：Dream Homes / Cooper Hewitt {DREAM_URL}

图片均来自 PIN–UP 官方期号页或文章页。图片版权归 PIN–UP、原摄影师、艺术家和项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-37",
        "issue": "PIN–UP 37 · MUSEUM ISSUE",
        "date": "F/W 2024/25",
        "core_question": "博物馆该消失吗？",
        "core_thesis": "博物馆不是中性容器，而是记忆、公共性与想象力发生的场所。",
        "pages": [
            "01 封面：博物馆该消失吗？",
            "02 中文目录：本期内容导览",
            "03 Carrie Mae Weems：外墙也会说话",
            "04 Phantom Museum：没有原件也能记得",
            "05 Plimoth Patuxet：历史不能隔着看",
            "06 Itsuko Hasegawa：文化空间也能像自然",
            "07 Smiljan Radić：博物馆更像一座广场",
            "08 Martine Syms：谁能在馆里开口",
            "09 Dream Homes：展览也能收下生活",
            "10 收束：给想象力留一把椅子",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_weems(), make_phantom(), make_living(),
        make_hasegawa(), make_radic(), make_syms(), make_dream(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 37 cards in {OUT}")


if __name__ == "__main__":
    main()
