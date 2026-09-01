from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-36"
OUT = ROOT / "output" / "pinup-36"
POST = ROOT / "posts" / "pinup-36" / "post.json"

W, H = 1242, 1660
ASPHALT = "#141614"
PAPER = "#f0eee6"
ORANGE = "#ff5a1f"
LIME = "#d8ff2d"
STEEL = "#8faab3"
BLUE = "#155f7d"
YELLOW = "#ffe534"

ISSUE_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-36-editors-letter"
SHIGEMATSU_URL = "https://www.pinupmagazine.org/articles/shohei-shigematsu-interview"
KUNDOO_URL = "https://www.pinupmagazine.org/articles/anupama-kundoo-interview"
REYNOLDS_URL = "https://www.pinupmagazine.org/articles/michael-e-reynolds-interview"
BOCCI_URL = "https://www.pinupmagazine.org/articles/bocci-lighting-vancouver-architecture"
SCAFFOLD_URL = "https://www.pinupmagazine.org/articles/sidewalk-network-new-york-city-construction-sheds-scaffolding"
TOLAAS_URL = "https://www.pinupmagazine.org/articles/sissel-tolaas-re-searchlab"
SARGADELOS_URL = "https://www.pinupmagazine.org/articles/sargadelos-porcelain-factory-miguel-leiro"

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


def meta(draw: ImageDraw.ImageDraw, number: int, accent: str) -> None:
    draw.rectangle((0, 0, W, 54), fill=ASPHALT)
    draw.text((34, 27), "PIN–UP 36 / UNDER CONSTRUCTION", font=font(18, True), fill=PAPER, anchor="lm")
    draw.rectangle((994, 0, W, 54), fill=accent)
    draw.text((1118, 27), f"{number:02d} / 10", font=font(19, True), fill=ASPHALT, anchor="mm")


def source(draw: ImageDraw.ImageDraw, text: str, *, light: bool = True) -> None:
    draw.rectangle((0, 1601, W, H), fill=rgba(ASPHALT if light else PAPER, 240))
    draw.text((34, 1631), text, font=font(15), fill=PAPER if light else ASPHALT, anchor="lm")


def hazard_stripe(draw: ImageDraw.ImageDraw, y: int, height: int, color: str = ORANGE) -> None:
    draw.rectangle((0, y, W, y + height), fill=ASPHALT)
    for x in range(-160, W + 180, 152):
        draw.polygon([(x, y + height), (x + 56, y + height), (x + 206, y), (x + 150, y)], fill=color)


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), ORANGE)
    image_panel(canvas, "book-cover.jpg", (318, 54, W, H), focal=(0.55, 0.50), darken=0.90)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, 344, H), fill=ASPHALT)
    draw.polygon([(278, 54), (344, 54), (344, 1570), (230, 1570)], fill=ORANGE)
    draw.text((40, 156), "建筑", font=font(93, True), fill=PAPER)
    draw.text((40, 270), "必须", font=font(93, True), fill=PAPER)
    draw.text((40, 384), "完成", font=font(93, True), fill=LIME)
    draw.text((40, 498), "吗？", font=font(112, True), fill=ORANGE)
    draw.line((42, 654, 250, 654), fill=LIME, width=13)
    draw_wrapped(draw, (42, 704), "PIN–UP 36 把建造看成一种持续发生的状态：会被使用、修改、打断，也会重新开始。", 228, 28, PAPER, bold=True, spacing=11)
    draw.text((42, 1312), "UNDER", font=font(34, True), fill=LIME)
    draw.text((42, 1358), "CONSTRUCTION", font=font(25, True), fill=PAPER)
    draw.text((42, 1438), "PIN–UP 36", font=font(27, True), fill=PAPER)
    source(draw, "PIN–UP 36 官方封面｜Under Construction", light=True)
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    hazard_stripe(draw, 54, 134, ORANGE)
    draw.text((40, 252), "本期目录", font=font(110, True), fill=ASPHALT)
    draw.text((44, 390), "UNDER CONSTRUCTION / 中文导览", font=font(24, True), fill=BLUE)
    draw.text((1174, 346), "36", font=font(258, True), fill=rgba(ORANGE, 84), anchor="ra")
    meta(draw, 2, LIME)
    items = [
        ("03", "SHOHEI SHIGEMATSU", "设计要在现场被验证"),
        ("04", "ANUPAMA KUNDOO", "低技术，也能造好房"),
        ("05", "MICHAEL E. REYNOLDS", "废料，也能供养生活"),
        ("06", "OMER ARBEL / BOCCI", "材料不该太听话"),
        ("07", "SIDEWALK NETWORK", "围挡，也能成为城市"),
        ("08", "SISSEL TOLAAS", "空间，可以用鼻子建"),
        ("09", "SARGADELOS FACTORY", "工厂，也能造文化"),
        ("10", "UNDER CONSTRUCTION", "未完成，不是失败"),
    ]
    for i, (number, name, text) in enumerate(items):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        x = 44 + col * 592
        y = 500 + row * 238
        draw.text((x, y), number, font=font(27, True), fill=ORANGE)
        draw.text((x, y + 42), name, font=font(20, True), fill=BLUE)
        draw_wrapped(draw, (x, y + 82), text, 482, 32, ASPHALT, bold=True, spacing=8)
        draw.line((x, y + 186, x + 516, y + 186), fill=rgba(ASPHALT, 72), width=2)
    draw.text((44, 1492), "建造，不只发生在交工之前。", font=font(32, True), fill=ORANGE)
    source(draw, "PIN–UP 36｜中文目录", light=True)
    return save(canvas, 2)


def make_shigematsu() -> Path:
    canvas = Image.new("RGBA", (W, H), BLUE)
    image_panel(canvas, "03-shigematsu-a.jpg", (0, 54, W, 824), focal=(0.50, 0.50), darken=0.92,
                label="SHOHEI SHIGEMATSU / OMA")
    image_panel(canvas, "03-shigematsu-hero.jpg", (40, 868, 452, 1508), focal=(0.50, 0.47), border=4, border_color=ASPHALT)
    image_panel(canvas, "03-shigematsu-b.jpg", (488, 868, 784, 1508), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 3, YELLOW)
    draw.rectangle((820, 868, 1204, 1508), fill=ASPHALT)
    draw.text((854, 908), "设计", font=font(75, True), fill=PAPER)
    draw.text((854, 1002), "要在现场", font=font(54, True), fill=LIME)
    draw.text((854, 1074), "验证", font=font(89, True), fill=PAPER)
    draw_wrapped(draw, (854, 1218), "建筑不是模型的放大版；真实的使用、路径和时间，才会把概念推到下一步。", 308, 26, PAPER, bold=True, spacing=10)
    source(draw, "Shohei Shigematsu / OMA｜PIN–UP 36", light=True)
    return save(canvas, 3)


def make_kundoo() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "04-kundoo-a.jpg", (0, 54, 768, H), focal=(0.50, 0.50), darken=0.98,
                label="ANUPAMA KUNDOO / AUROVILLE")
    image_panel(canvas, "04-kundoo-hero.jpg", (804, 88, 1204, 602), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    image_panel(canvas, "04-kundoo-b.jpg", (804, 638, 1204, 994), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 4, ORANGE)
    draw.rectangle((804, 1030, 1204, 1548), fill=ORANGE)
    draw.text((838, 1068), "低技术", font=font(65, True), fill=ASPHALT)
    draw.text((838, 1150), "也能", font=font(65, True), fill=ASPHALT)
    draw.text((838, 1232), "造好房", font=font(82, True), fill=PAPER)
    draw_wrapped(draw, (838, 1374), "在地材料、轻量构件和现场手作，让墙、收纳与生活一起生长。", 320, 25, ASPHALT, bold=True, spacing=9)
    source(draw, "Anupama Kundoo｜PIN–UP 36", light=True)
    return save(canvas, 4)


def make_earthship() -> Path:
    canvas = Image.new("RGBA", (W, H), ASPHALT)
    image_panel(canvas, "05-earthship-b.jpg", (0, 54, W, 782), focal=(0.50, 0.50), darken=0.89,
                label="MICHAEL E. REYNOLDS / EARTHSHIP")
    image_panel(canvas, "05-earthship-hero.jpg", (42, 830, 506, 1506), focal=(0.50, 0.45), border=4, border_color=PAPER)
    image_panel(canvas, "05-earthship-a.jpg", (542, 830, 846, 1506), focal=(0.50, 0.50), border=4, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 5, LIME)
    draw.rectangle((882, 830, 1204, 1506), fill=LIME)
    draw.text((916, 868), "废料", font=font(74, True), fill=ASPHALT)
    draw.text((916, 960), "也能", font=font(74, True), fill=ASPHALT)
    draw.text((916, 1052), "供养", font=font(82, True), fill=ORANGE)
    draw.text((916, 1154), "生活", font=font(82, True), fill=ASPHALT)
    draw_wrapped(draw, (916, 1302), "轮胎、罐头与瓶子，不是装饰，而是自给建筑的热工与结构逻辑。", 250, 25, ASPHALT, bold=True, spacing=9)
    source(draw, "Michael E. Reynolds, Earthship｜PIN–UP 36", light=True)
    return save(canvas, 5)


def make_bocci() -> Path:
    canvas = Image.new("RGBA", (W, H), STEEL)
    image_panel(canvas, "06-bocci-hero.jpg", (0, 54, 610, H), focal=(0.52, 0.50), darken=0.92,
                label="OMER ARBEL / BOCCI")
    image_panel(canvas, "06-bocci-a.jpg", (650, 88, 1204, 704), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    image_panel(canvas, "06-bocci-b.jpg", (650, 738, 928, 1508), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 6, ORANGE)
    draw.rectangle((962, 738, 1204, 1508), fill=ASPHALT)
    draw.text((990, 778), "材料", font=font(58, True), fill=PAPER)
    draw.text((990, 852), "不该", font=font(58, True), fill=ORANGE)
    draw.text((990, 926), "太听话", font=font(58, True), fill=PAPER)
    draw_wrapped(draw, (990, 1068), "从布模混凝土到原型空间，工艺的偏差能打开新的建筑形式。", 178, 24, PAPER, bold=True, spacing=9)
    draw.line((990, 1404, 1170, 1404), fill=LIME, width=12)
    source(draw, "Omer Arbel / Bocci｜PIN–UP 36", light=True)
    return save(canvas, 6)


def make_scaffold() -> Path:
    canvas = Image.new("RGBA", (W, H), ORANGE)
    image_panel(canvas, "07-scaffold-hero.jpg", (0, 54, W, 894), focal=(0.50, 0.48), darken=0.92,
                label="SIDEWALK NETWORK / NEW YORK")
    image_panel(canvas, "07-scaffold-a.jpg", (38, 940, 486, 1510), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    image_panel(canvas, "07-scaffold-b.jpg", (522, 940, 820, 1510), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 7, YELLOW)
    draw.rectangle((858, 940, 1204, 1510), fill=ASPHALT)
    draw.text((890, 978), "围挡", font=font(77, True), fill=PAPER)
    draw.text((890, 1074), "也能成为", font=font(53, True), fill=LIME)
    draw.text((890, 1146), "城市", font=font(92, True), fill=PAPER)
    draw_wrapped(draw, (890, 1290), "当脚手架长期覆盖街道，它不再只是临时物，而是一套被身体重新使用的公共基础设施。", 270, 24, PAPER, bold=True, spacing=9)
    source(draw, "Nick Sethi, Sidewalk Network｜PIN–UP 36", light=True)
    return save(canvas, 7)


def make_tolaas() -> Path:
    canvas = Image.new("RGBA", (W, H), BLUE)
    image_panel(canvas, "08-tolaas-hero.jpg", (0, 54, 764, H), focal=(0.50, 0.50), darken=0.91,
                label="SISSEL TOLAAS / RE_SEARCHLAB")
    image_panel(canvas, "08-tolaas-a.jpg", (798, 88, 1204, 610), focal=(0.50, 0.50), border=4, border_color=PAPER)
    image_panel(canvas, "08-tolaas-b.jpg", (798, 644, 1204, 1054), focal=(0.50, 0.50), border=4, border_color=PAPER)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 8, LIME)
    draw.rectangle((798, 1088, 1204, 1548), fill=LIME)
    draw.text((832, 1124), "空间", font=font(71, True), fill=ASPHALT)
    draw.text((832, 1214), "可以用", font=font(55, True), fill=ASPHALT)
    draw.text((832, 1286), "鼻子建", font=font(84, True), fill=ORANGE)
    draw_wrapped(draw, (832, 1416), "气味、空气管与身体反应，让看不见的材料进入空间设计。", 326, 24, ASPHALT, bold=True, spacing=8)
    source(draw, "Sissel Tolaas, RE_searchLab｜PIN–UP 36", light=True)
    return save(canvas, 8)


def make_sargadelos() -> Path:
    canvas = Image.new("RGBA", (W, H), PAPER)
    image_panel(canvas, "09-sargadelos-hero.jpg", (0, 54, W, 796), focal=(0.50, 0.50), darken=0.90,
                label="SARGADELOS PORCELAIN FACTORY")
    image_panel(canvas, "09-sargadelos-a.jpg", (40, 840, 574, 1510), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    image_panel(canvas, "09-sargadelos-b.jpg", (610, 840, 902, 1510), focal=(0.50, 0.50), border=4, border_color=ASPHALT)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 9, ORANGE)
    draw.rectangle((938, 840, 1204, 1510), fill=ASPHALT)
    draw.text((968, 878), "工厂", font=font(69, True), fill=PAPER)
    draw.text((968, 964), "也能造", font=font(55, True), fill=YELLOW)
    draw.text((968, 1038), "文化", font=font(85, True), fill=PAPER)
    draw_wrapped(draw, (968, 1186), "空间、设备、标识与产品，被放进同一套可继续扩张的生产系统。", 202, 25, PAPER, bold=True, spacing=9)
    source(draw, "Sargadelos Porcelain Factory｜PIN–UP 36", light=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), ASPHALT)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 10, LIME)
    hazard_stripe(draw, 160, 228, ORANGE)
    hazard_stripe(draw, 1122, 228, LIME)
    draw.text((74, 474), "未完成", font=font(144, True), fill=PAPER)
    draw.text((74, 646), "不是失败", font=font(144, True), fill=ORANGE)
    draw.line((78, 844, 1160, 844), fill=STEEL, width=4)
    draw.text((78, 900), "可变", font=font(74, True), fill=LIME)
    draw.text((420, 900), "可学", font=font(74, True), fill=PAPER)
    draw.text((762, 900), "可继续", font=font(74, True), fill=ORANGE)
    draw_wrapped(draw, (78, 1420), "真正有生命力的建筑，会给修改、使用与下一次建造留下余地。", 1030, 39, PAPER, bold=True, spacing=12)
    source(draw, "PIN–UP 36 / Under Construction", light=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#a8aba5")
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 36｜建筑必须完成吗？"
    body = (
        "我们常把建筑理解成一项等待交工的成果，但 PIN–UP 36 的 Under Construction 反过来提醒：真正重要的，也许正是它还在变化的过程。\n\n"
        "Shohei Shigematsu 认为，概念必须进入现场、接受使用检验；Anupama Kundoo 用轻量构件与在地材料，让建造贴近日常资源；Michael E. Reynolds 把轮胎、瓶子和罐头变成自给建筑的一部分。它们都把“完成”从唯一目标，改成了可继续调整的起点。\n\n"
        "Omer Arbel 从材料的偶发性里寻找空间形式；纽约的施工围挡被身体重新使用，成了临时却真实的城市基础设施；Sissel Tolaas 甚至把气味视为可进入空间的材料。Sargadelos 工厂则说明，生产系统、建筑与文化可以被一并设计。\n\n"
        "未完成不是低质量的借口，而是为修改、学习和新的使用方式预留位置。这不是把变化浪漫化：材料、预算、法规和维护都是真实约束。好的设计不是回避它们，而是让调整的路径被看见，并且能被更多人参与。你希望身边哪一座建筑，能允许人们继续把它建下去？"
    )
    tags = "#PINUP #PINUP36 #建筑设计 #建筑施工 #公共空间 #材料设计 #可持续建筑 #建筑杂志"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 36 图片与内容来源
- 第01页：PIN–UP 36 Under Construction 官方期号文章 {ISSUE_URL}
- 第03页：Shohei Shigematsu / OMA {SHIGEMATSU_URL}
- 第04页：Anupama Kundoo {KUNDOO_URL}
- 第05页：Michael E. Reynolds / Earthship {REYNOLDS_URL}
- 第06页：Omer Arbel / Bocci {BOCCI_URL}
- 第07页：Nick Sethi, Sidewalk Network {SCAFFOLD_URL}
- 第08页：Sissel Tolaas / RE_searchLab {TOLAAS_URL}
- 第09页：Sargadelos Porcelain Factory {SARGADELOS_URL}

图片均来自 PIN–UP 官方文章或官方期号页。图片版权归 PIN–UP、原摄影师、建筑师、艺术家与项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-36",
        "issue": "PIN–UP 36 · UNDER CONSTRUCTION",
        "date": "S/S 2024",
        "core_question": "建筑必须完成吗？",
        "core_thesis": "建造不是交工前的短暂阶段，而是让空间持续被使用、修改与重写的能力。",
        "pages": [
            "01 封面：建筑必须完成吗？",
            "02 中文目录：本期内容导览",
            "03 Shohei Shigematsu：设计要在现场被验证",
            "04 Anupama Kundoo：低技术也能造好房",
            "05 Michael E. Reynolds：废料也能供养生活",
            "06 Omer Arbel：材料不该太听话",
            "07 Sidewalk Network：围挡也能成为城市",
            "08 Sissel Tolaas：空间可以用鼻子建",
            "09 Sargadelos：工厂也能造文化",
            "10 收束：未完成不是失败",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_shigematsu(), make_kundoo(), make_earthship(),
        make_bocci(), make_scaffold(), make_tolaas(), make_sargadelos(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 36 cards in {OUT}")


if __name__ == "__main__":
    main()
