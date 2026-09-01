from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-30"
OUT = ROOT / "output" / "pinup-30"
POST = ROOT / "posts" / "pinup-30" / "post.json"

W, H = 1242, 1660
INK = "#17141b"
PAPER = "#f8f0e2"
PINK = "#ec5ca6"
SUN = "#ffbd2f"
SKY = "#59a3eb"
MINT = "#6cd0b9"
RED = "#cf4e45"

ISSUE_URL = "https://www.pinupmagazine.org/issues/pinup-magazine-30-legacy"
FORMA_URL = "https://archive.pinupmagazine.org/articles/interview-formafantasma-hans-ulrich-obrist"
GEHRY_URL = "https://www.pinupmagazine.org/articles/frank-gehry-interview"
OBJECTS_URL = "https://archive.pinupmagazine.org/articles/article-30-objects-survey-show"
SHEILA_URL = "https://archive.pinupmagazine.org/articles/interview-sheila-levrant-de-bretteville-graphic-design-yale"
AAA_URL = "https://archive.pinupmagazine.org/articles/interview-a-a-a-andrea-chiney-arianna-deane-ashely-kuo"
AGENCY_URL = "https://archive.pinupmagazine.org/articles/interview-agency-agency-tei-carpenter"
CANTY_URL = "https://archive.pinupmagazine.org/articles/interview-studio-sean-canty"

shared.SRC = SRC
shared.OUT = OUT


def font(size: int, bold: bool = False):
    return shared.font(size, bold)


def rgba(value: str, alpha: int = 255):
    return shared.rgba(value, alpha)


def wrap(draw, xy, text, width, size, fill, *, bold=False, spacing=8):
    shared.draw_wrapped(draw, xy, text, width, size, fill, bold=bold, spacing=spacing)


def save(image: Image.Image, number: int) -> Path:
    path = OUT / f"{number:02d}.jpg"
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def crop_photo(name: str, size: tuple[int, int], *, focal=(0.5, 0.5), darken=1.0) -> Image.Image:
    image = Image.open(SRC / name).convert("RGB")
    image = shared.cover_crop(image, size, focal)
    return shared.grade(image, brightness=darken).convert("RGBA")


def rounded_photo(canvas: Image.Image, name: str, box: tuple[int, int, int, int], *, radius=36, focal=(0.5, 0.5), darken=1.0, border=0, border_color=PAPER) -> None:
    x0, y0, x1, y1 = box
    size = (x1 - x0, y1 - y0)
    image = crop_photo(name, size, focal=focal, darken=darken)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    canvas.paste(image, (x0, y0), mask)
    if border:
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((x0, y0, x1 - 1, y1 - 1), radius=radius, outline=border_color, width=border)


def stamp(draw: ImageDraw.ImageDraw, number: int, color: str, *, dark=False) -> None:
    fg = PAPER if dark else INK
    draw.rounded_rectangle((40, 42, 222, 94), radius=26, fill=color)
    draw.text((62, 68), "PIN–UP 30", font=font(18, True), fill=INK, anchor="lm")
    draw.text((1202, 68), f"{number:02d}/10", font=font(20, True), fill=fg, anchor="rm")


def cover_fit(name: str, size: tuple[int, int]) -> Image.Image:
    return shared.fit_inside(Image.open(SRC / name).convert("RGBA"), size)


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((-260, -310, 870, 780), fill=PINK)
    draw.rounded_rectangle((38, 500, 702, 1560), radius=68, fill=SUN)
    draw.rounded_rectangle((746, 80, 1206, 1480), radius=210, fill=SKY)
    cover = cover_fit("issue-cover.gif", (600, 1160))
    shadow = Image.new("RGBA", (cover.width + 50, cover.height + 50), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((25, 25, cover.width + 25, cover.height + 25), radius=12, fill=rgba(INK, 100))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(15)), (84, 420))
    canvas.alpha_composite(cover, (70, 400))
    draw = ImageDraw.Draw(canvas)
    draw.text((784, 142), "传承", font=font(112, True), fill=INK)
    draw.text((784, 266), "不是", font=font(82, True), fill=INK)
    draw.text((784, 358), "复刻", font=font(118, True), fill=PAPER)
    draw.rounded_rectangle((784, 528, 1158, 544), radius=8, fill=RED)
    wrap(draw, (784, 584), "留下来的，不只是名字和物件。", 350, 31, INK, bold=True, spacing=10)
    draw.text((784, 1228), "PIN–UP 30", font=font(26, True), fill=INK)
    draw.text((784, 1272), "LEGACY / S/S 2021", font=font(18, True), fill=INK)
    draw.text((1158, 1534), "01/10", font=font(20, True), fill=INK, anchor="ra")
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), SKY)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((636, -288, 1460, 538), fill=MINT)
    draw.rounded_rectangle((44, 116, 1198, 1520), radius=64, fill=PAPER)
    draw.text((84, 172), "目录", font=font(124, True), fill=INK)
    draw.text((88, 320), "LEGACY", font=font(54, True), fill=PINK)
    draw.text((1002, 196), "30", font=font(184, True), fill=SUN)
    stamp(draw, 2, PINK)
    items = [
        ("03", "FORMAFANTASMA", "传承不只靠收藏"),
        ("04", "FRANK GEHRY", "档案不等于回头"),
        ("05", "30 OBJECTS", "一件物也在记录时代"),
        ("06", "SHEILA DE BRETTEVILLE", "设计要让差异被看见"),
        ("07", "A+A+A", "建筑不只盖完就走"),
        ("08", "AGENCY—AGENCY", "修复不是做旧"),
        ("09", "SEAN CANTY", "小尺度也能改变日常"),
        ("10", "LEGACY", "把未来留出来"),
    ]
    for idx, (no, who, line) in enumerate(items):
        col, row = (0, idx) if idx < 4 else (1, idx - 4)
        x = 94 + col * 542
        y = 488 + row * 226
        draw.rounded_rectangle((x, y, x + 440, y + 160), radius=34, fill=SUN if (idx % 3 == 0) else MINT)
        draw.text((x + 22, y + 24), no, font=font(23, True), fill=RED)
        draw.text((x + 76, y + 28), who, font=font(17, True), fill=INK)
        wrap(draw, (x + 22, y + 74), line, 390, 29, INK, bold=True, spacing=6)
    return save(canvas, 2)


def make_forma() -> Path:
    canvas = Image.new("RGBA", (W, H), MINT)
    rounded_photo(canvas, "forma-04.jpg", (40, 110, 818, 1036), radius=74, focal=(0.5, 0.5), darken=0.95)
    rounded_photo(canvas, "forma-05.jpg", (856, 110, 1202, 534), radius=48, focal=(0.50, 0.5), border=7, border_color=PAPER)
    rounded_photo(canvas, "forma-08.jpg", (856, 586, 1202, 1006), radius=48, focal=(0.50, 0.50), border=7, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((40, 1090, 1202, 1512), radius=74, fill=INK)
    stamp(draw, 3, SUN, dark=True)
    draw.text((80, 1150), "传承不只靠收藏", font=font(76, True), fill=PAPER)
    draw.text((80, 1246), "思想也要继续生长", font=font(66, True), fill=SUN)
    draw.text((82, 1364), "FORMAFANTASMA", font=font(21, True), fill=PINK)
    wrap(draw, (82, 1412), "从森林、矿物到电子废料，设计的对象可以是一整套材料关系。", 1000, 26, PAPER, bold=True, spacing=8)
    return save(canvas, 3)


def make_gehry() -> Path:
    canvas = Image.new("RGBA", (W, H), SUN)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((590, -132, 1364, 652), fill=PINK)
    rounded_photo(canvas, "gehry-01.jpg", (56, 124, 784, 1032), radius=364, focal=(0.46, 0.50), darken=0.98)
    rounded_photo(canvas, "gehry-03.jpg", (834, 138, 1190, 540), radius=38, focal=(0.50, 0.5), border=6, border_color=INK)
    rounded_photo(canvas, "gehry-05.jpg", (834, 590, 1190, 950), radius=38, focal=(0.50, 0.5), border=6, border_color=INK)
    draw.rounded_rectangle((0, 1042, W, H), radius=0, fill=PAPER)
    stamp(draw, 4, SKY)
    draw.text((54, 1112), "档案", font=font(92, True), fill=INK)
    draw.text((306, 1112), "不等于回头", font=font(69, True), fill=INK)
    draw.rounded_rectangle((56, 1228, 704, 1246), radius=9, fill=PINK)
    draw.text((56, 1290), "FRANK GEHRY", font=font(21, True), fill=RED)
    wrap(draw, (56, 1342), "图纸和模型保存的，不是一次定稿，而是不断试错、继续往前的路径。", 680, 31, INK, bold=True, spacing=11)
    return save(canvas, 4)


def make_objects() -> Path:
    canvas = Image.new("RGBA", (W, H), PINK)
    rounded_photo(canvas, "objects-03.jpg", (44, 112, 1198, 760), radius=64, focal=(0.5, 0.5), darken=0.98)
    rounded_photo(canvas, "objects-04.jpg", (44, 808, 608, 1224), radius=54, focal=(0.50, 0.50), border=7, border_color=PAPER)
    rounded_photo(canvas, "objects-08.jpg", (648, 808, 1198, 1224), radius=54, focal=(0.50, 0.50), border=7, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((44, 1274, 1198, 1510), radius=58, fill=INK)
    stamp(draw, 5, MINT, dark=True)
    draw.text((78, 1320), "一件物，也在记录时代", font=font(60, True), fill=PAPER)
    draw.text((80, 1412), "30 OBJECTS", font=font(21, True), fill=SUN)
    draw.text((308, 1412), "把二十一世纪前二十年，装进三十件物。", font=font(23, True), fill=PAPER)
    return save(canvas, 5)


def make_sheila() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, W, 394), radius=0, fill=RED)
    rounded_photo(canvas, "sheila-03.jpg", (44, 92, 792, 758), radius=60, focal=(0.5, 0.48), border=7, border_color=PAPER)
    rounded_photo(canvas, "sheila-04.jpg", (834, 92, 1200, 512), radius=44, focal=(0.50, 0.50), border=7, border_color=PAPER)
    rounded_photo(canvas, "sheila-06.jpg", (834, 556, 1200, 972), radius=44, focal=(0.50, 0.50), border=7, border_color=INK)
    draw.rounded_rectangle((44, 818, 1200, 1510), radius=70, fill=SKY)
    stamp(draw, 6, SUN)
    draw.text((84, 878), "设计要让", font=font(75, True), fill=INK)
    draw.text((84, 968), "差异被看见", font=font(86, True), fill=PAPER)
    draw.text((86, 1100), "SHEILA LEVRANT DE BRETTEVILLE", font=font(20, True), fill=INK)
    wrap(draw, (86, 1160), "当设计认真面对观看者，它就不只传递信息，也为不同经验留下位置。", 940, 31, INK, bold=True, spacing=11)
    return save(canvas, 6)


def make_aaa() -> Path:
    canvas = Image.new("RGBA", (W, H), MINT)
    rounded_photo(canvas, "aaa-08.jpg", (40, 112, 1202, 866), radius=78, focal=(0.50, 0.52), darken=0.98)
    rounded_photo(canvas, "aaa-09.jpg", (40, 918, 572, 1510), radius=58, focal=(0.50, 0.50), border=7, border_color=INK)
    rounded_photo(canvas, "aaa-07.png", (622, 918, 1202, 1254), radius=58, focal=(0.50, 0.50), border=7, border_color=INK)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((622, 1304, 1202, 1510), radius=54, fill=INK)
    stamp(draw, 7, PINK)
    draw.rounded_rectangle((40, 556, 822, 866), radius=0, fill=rgba(INK, 218))
    draw.text((78, 586), "建筑不只", font=font(73, True), fill=PAPER)
    draw.text((78, 674), "盖完就走", font=font(85, True), fill=SUN)
    draw.text((80, 798), "A+A+A", font=font(22, True), fill=PINK)
    wrap(draw, (658, 1342), "一起建，也把技能、关系和停留的空间一起留下。", 492, 25, PAPER, bold=True, spacing=8)
    return save(canvas, 7)


def make_agency() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    rounded_photo(canvas, "agency-07.jpg", (42, 112, 622, 1508), radius=72, focal=(0.50, 0.50), border=7, border_color=MINT)
    rounded_photo(canvas, "agency-08.jpg", (674, 112, 1200, 690), radius=60, focal=(0.50, 0.50), border=7, border_color=MINT)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((674, 742, 1200, 1508), radius=70, fill=SUN)
    stamp(draw, 8, MINT, dark=True)
    draw.text((716, 798), "修复", font=font(88, True), fill=INK)
    draw.text((716, 902), "不是做旧", font=font(74, True), fill=RED)
    draw.rounded_rectangle((716, 1026, 1150, 1042), radius=8, fill=INK)
    draw.text((716, 1086), "AGENCY—AGENCY", font=font(21, True), fill=INK)
    wrap(draw, (716, 1146), "把旧厂房、废弃材料和已有结构重新接入公共生活，让修补成为新的起点。", 418, 29, INK, bold=True, spacing=10)
    return save(canvas, 8)


def make_canty() -> Path:
    canvas = Image.new("RGBA", (W, H), SKY)
    rounded_photo(canvas, "canty-07.jpg", (40, 114, 1202, 744), radius=78, focal=(0.50, 0.50), darken=0.98)
    rounded_photo(canvas, "canty-08.jpg", (40, 792, 610, 1246), radius=58, focal=(0.50, 0.50), border=7, border_color=PAPER)
    rounded_photo(canvas, "canty-10.jpg", (652, 792, 1202, 1246), radius=58, focal=(0.50, 0.50), border=7, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((40, 1292, 1202, 1510), radius=62, fill=PAPER)
    stamp(draw, 9, SUN)
    draw.text((78, 1334), "小尺度，也能改变日常", font=font(61, True), fill=INK)
    draw.text((80, 1422), "SEAN CANTY", font=font(21, True), fill=RED)
    draw.text((320, 1422), "亭子、住宅与公共空间，都可以是新的交谈开端。", font=font(23, True), fill=INK)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((-340, 962, 698, 2024), fill=MINT)
    draw.ellipse((742, -304, 1520, 496), fill=PINK)
    draw.rounded_rectangle((66, 100, 1176, 682), radius=136, fill=INK)
    draw.rounded_rectangle((66, 740, 1176, 1120), radius=120, fill=SUN)
    draw.rounded_rectangle((66, 1170, 1176, 1510), radius=110, fill=SKY)
    draw.text((122, 178), "传承", font=font(154, True), fill=PAPER)
    draw.text((122, 346), "是把未来留出来", font=font(72, True), fill=PINK)
    draw.text((122, 804), "保存", font=font(84, True), fill=INK)
    draw.text((458, 804), "改写", font=font(84, True), fill=RED)
    draw.text((794, 804), "交给更多人", font=font(62, True), fill=INK)
    wrap(draw, (122, 1242), "好的遗产，不会把后来者困在原地。它让材料、知识与公共经验拥有下一次使用的机会。", 930, 37, INK, bold=True, spacing=13)
    draw.text((122, 1458), "PIN–UP 30 / LEGACY / S/S 2021", font=font(20, True), fill=INK)
    draw.text((1144, 1538), "10/10", font=font(20, True), fill=INK, anchor="ra")
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#dad2c6")
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 30｜传承不是复刻"
    body = (
        "如果“传承”只是在复刻旧样式，那它很快就会变成博物馆里的标本。PIN–UP 30 在创刊十五周年回看设计时，真正追问的是：什么东西值得被带去下一代？\n\n"
        "Formafantasma 从森林、矿物与电子废料出发，把设计从单个物件推向材料系统。Frank Gehry 的图纸和模型则说明，档案留下的不是最终答案，而是一连串试错。30 Objects 用三十件物勾勒 2000 到 2020：家具、手机、建筑模型和一只包，都在记录技术、消费与审美如何改变生活。\n\n"
        "Sheila Levrant de Bretteville 让设计为不同经验腾出位置；A+A+A 把共建和技能一起留在社区；Agency—Agency 用修补与再利用重写既有建筑；Sean Canty 证明，一座小亭子也足以重新组织相遇、停留与玩耍。\n\n"
        "这期最有用的提醒是：遗产不是把过去封存，而是给未来留下能够继续使用、质疑和改写的资源。真正的传承，也必须允许后来者动手。你最希望哪一种设计经验被传下去？"
    )
    tags = "#PINUP #PINUP30 #建筑杂志 #设计史 #建筑设计 #空间设计 #建筑改造 #当代设计"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 30 图片与内容来源
- 第01–02、10页：PIN–UP 30《Legacy》官方期号 {ISSUE_URL}
- 第03页：Formafantasma / Cambio、Botanica 与材料研究图像 {FORMA_URL}
- 第04页：Frank Gehry / 访谈肖像、档案图纸与模型 {GEHRY_URL}
- 第05页：30 Objects / Rubén Gutiérrez-Martin 渲染图 {OBJECTS_URL}
- 第06页：Sheila Levrant de Bretteville / Central Market、At the Start... At Long Last...、Everywoman Newspaper {SHEILA_URL}
- 第07页：A+A+A / Rural Assembly、Healing Sanctuaries 与社区项目 {AAA_URL}
- 第08页：Agency—Agency / Hamilton Gears Reuse Park、Street Remodel {AGENCY_URL}
- 第09页：Sean Canty / Edgar’s Shed、Janus House 等项目 {CANTY_URL}

图片均来自 PIN–UP 官方期号、官方文章页或其官方档案。图片版权归 PIN–UP、原摄影师、建筑师、艺术家与项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-30",
        "issue": "PIN–UP 30 · Legacy",
        "date": "S/S 2021",
        "core_question": "传承是保存过去，还是把未来留出来？",
        "core_thesis": "设计的遗产不止是对象；它由材料、档案、教育、共建和修补持续被下一代改写。",
        "pages": [
            "01 封面：传承不是复刻",
            "02 中文目录：Legacy",
            "03 Formafantasma：传承不只靠收藏",
            "04 Frank Gehry：档案不等于回头",
            "05 30 Objects：一件物也在记录时代",
            "06 Sheila Levrant de Bretteville：设计让差异被看见",
            "07 A+A+A：建筑不只盖完就走",
            "08 Agency—Agency：修复不是做旧",
            "09 Sean Canty：小尺度也能改变日常",
            "10 收束：把未来留出来",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_forma(), make_gehry(), make_objects(),
        make_sheila(), make_aaa(), make_agency(), make_canty(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 30 cards in {OUT}")


if __name__ == "__main__":
    main()
