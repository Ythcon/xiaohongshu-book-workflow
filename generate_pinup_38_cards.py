from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import generate_pinup_39_cards as shared


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "pinup-38"
OUT = ROOT / "output" / "pinup-38"
POST = ROOT / "posts" / "pinup-38" / "post.json"

W, H = 1242, 1660
BLACK = "#12110f"
WHITE = "#f6f1e7"
INK = "#181b2f"
ORANGE = "#ff6a2a"
LIME = "#dfff38"
BLUE = "#1b4fb6"
PINK = "#ef9cc1"
TURQ = "#23c4c7"

ISSUE_URL = "https://www.pinupmagazine.org/issues/pinup-magazine-38-xxl-nyc11"
SOLAR_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-38-xxl-philippe-jarrigeon-tacchini-solar-sofa-faye-toogood"
SUPERWIRE_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-38-xxl-raymond-meier-flos-superwire"
TUFTY_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-38-xxl-philippe-jarrigeon-bbitalia-tufty-time-patricia-urquiola"
RUGS_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-38-xxl-francesco-nazardo-rop-van-meirlo-wild-animals-cctapis"
FROG_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-38-xxl-francesco-nazardo-living-divani-frog-piero-lissoni"
ROCKS_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-38-xxl-francesco-nazardo-francesco-binfare-on-the-rocks-outdoor-lounge-edra"
POLIFORM_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-38-xxl-poliform-jean-marie-massaud-ketch-sunbed-ernest-sofa-system-francesco-nazardo-philippe-jarrigeon"
CAMELOT_URL = "https://www.pinupmagazine.org/articles/pinup-magazine-38-xxl-philippe-jarrigeon-flexform-camelot-sofa"

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
    draw.rectangle((0, 0, W, 54), fill=BLACK)
    draw.text((34, 27), "PIN–UP 38 / XXL BIG DESIGN", font=font(18, True), fill=WHITE, anchor="lm")
    draw.rectangle((1020, 0, W, 54), fill=accent)
    draw.text((1131, 27), f"{number:02d} / 10", font=font(19, True), fill=BLACK, anchor="mm")


def source(draw: ImageDraw.ImageDraw, text: str, *, light: bool = True) -> None:
    bg = rgba(BLACK if light else WHITE, 238)
    fg = WHITE if light else BLACK
    draw.rectangle((0, 1601, W, H), fill=bg)
    draw.text((34, 1631), text, font=font(15), fill=fg, anchor="lm")


def crop(image: Image.Image, size: tuple[int, int], focal=(0.5, 0.5)) -> Image.Image:
    return shared.cover_crop(image, size, focal)


def cover_fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return shared.fit_inside(image, size)


def make_cover() -> Path:
    canvas = Image.new("RGBA", (W, H), WHITE)
    cover = cover_fit(Image.open(SRC / "book-cover.jpg").convert("RGB"), (672, 1336))
    shadow = Image.new("RGBA", (cover.width + 68, cover.height + 68), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((34, 34, cover.width + 34, cover.height + 34), fill=rgba(BLACK, 148))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(15)), (522, 112))
    canvas.alpha_composite(cover.convert("RGBA"), (556, 112))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 50, H), fill=ORANGE)
    draw.text((90, 160), "大设计", font=font(103, True), fill=BLACK)
    draw.text((90, 282), "不是", font=font(109, True), fill=ORANGE)
    draw.text((90, 410), "大尺寸", font=font(109, True), fill=BLACK)
    draw.rectangle((90, 570, 446, 584), fill=BLUE)
    draw_wrapped(draw, (90, 630), "真正占据空间的，是能被触摸、修复、重组和久用的物件。", 370, 34, BLACK, bold=True, spacing=12)
    draw.text((90, 1434), "PIN–UP 38", font=font(31, True), fill=ORANGE)
    draw.text((90, 1480), "XXL BIG DESIGN / S/S 2025", font=font(19, True), fill=BLACK)
    draw.text((1170, 1545), "01 / 10", font=font(20, True), fill=BLACK, anchor="ra")
    source(draw, "PIN–UP 38 官方封面｜XXL Big Design Issue", light=False)
    return save(canvas, 1)


def make_contents() -> Path:
    canvas = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 54, W, 278), fill=LIME)
    draw.text((38, 76), "本期目录", font=font(112, True), fill=BLACK)
    draw.text((44, 240), "XXL BIG DESIGN", font=font(24, True), fill=BLACK)
    draw.text((1180, 192), "38", font=font(246, True), fill=rgba(BLACK, 60), anchor="ra")
    meta(draw, 2, LIME)
    items = [
        ("03", "FAYE TOOGOOD", "把柔软做成一座可停靠的岛"),
        ("04", "FORMAFANTASMA", "可维修，才是面向未来的灯"),
        ("05", "PATRICIA URQUIOLA", "模块不必把生活固定下来"),
        ("06", "WILD ANIMALS × CC-TAPIS", "让图案失控，空间才会醒来"),
        ("07", "PIERO LISSONI", "一把椅子怎样活过三十年"),
        ("08", "FRANCESCO BINFARÉ", "沙发不是摆设，是身体的地形"),
        ("09", "JEAN-MARIE MASSAUD", "户外与室内之间，不必划线"),
        ("10", "FLEXFORM", "物件要为变化中的生活留余地"),
    ]
    for i, (num, name, text) in enumerate(items):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        x = 44 + col * 590
        y = 360 + row * 270
        draw.text((x, y), num, font=font(27, True), fill=LIME)
        draw.text((x, y + 42), name, font=font(21, True), fill=WHITE)
        draw_wrapped(draw, (x, y + 84), text, 500, 30, WHITE, bold=True, spacing=8)
        draw.line((x, y + 204, x + 518, y + 204), fill=rgba(WHITE, 70), width=2)
    draw.text((44, 1500), "不是更大，而是更能被生活使用。", font=font(30, True), fill=ORANGE)
    source(draw, "PIN–UP 38｜中文目录", light=True)
    return save(canvas, 2)


def make_solar() -> Path:
    canvas = Image.new("RGBA", (W, H), PINK)
    image_panel(canvas, "03-solar-hero.jpg", (0, 54, W, 918), focal=(0.50, 0.49), darken=0.94,
                label="FAYE TOOGOOD / SOLAR SOFA / TACCHINI")
    image_panel(canvas, "03-solar-a.jpg", (38, 960, 410, 1516), focal=(0.50, 0.45), border=4)
    image_panel(canvas, "03-solar-b.jpg", (438, 960, 810, 1516), focal=(0.50, 0.45), border=4)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 3, ORANGE)
    draw.rectangle((826, 960, 1204, 1516), fill=BLACK)
    draw.text((862, 1000), "软，", font=font(104, True), fill=WHITE)
    draw.text((862, 1126), "也能", font=font(104, True), fill=ORANGE)
    draw.text((862, 1252), "成形", font=font(104, True), fill=WHITE)
    draw_wrapped(draw, (862, 1400), "Solar 把坐垫叠成一件低矮、可陷入的软雕塑。", 300, 23, WHITE, bold=True, spacing=8)
    source(draw, "Philippe Jarrigeon｜Faye Toogood, Solar｜PIN–UP 38", light=True)
    return save(canvas, 3)


def make_superwire() -> Path:
    canvas = Image.new("RGBA", (W, H), TURQ)
    image_panel(canvas, "04-superwire-hero.jpg", (0, 54, W, 910), focal=(0.52, 0.50), darken=0.88,
                label="FORMAFANTASMA / SUPERWIRE / FLOS")
    image_panel(canvas, "04-superwire-a.jpg", (40, 954, 542, 1494), focal=(0.50, 0.50), border=4)
    image_panel(canvas, "04-superwire-b.webp", (570, 954, 850, 1494), focal=(0.50, 0.48), border=4)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 4, LIME)
    draw.rectangle((872, 954, 1204, 1494), fill=INK)
    draw.text((906, 998), "坏了", font=font(72, True), fill=WHITE)
    draw.text((906, 1096), "也能", font=font(72, True), fill=LIME)
    draw.text((906, 1194), "修", font=font(108, True), fill=WHITE)
    draw_wrapped(draw, (906, 1330), "12 条 LED 光源都能单独更换，构造不必被藏起来", 258, 23, WHITE, bold=True, spacing=9)
    source(draw, "Raymond Meier｜Formafantasma, SuperWire｜PIN–UP 38", light=True)
    return save(canvas, 4)


def make_tufty() -> Path:
    canvas = Image.new("RGBA", (W, H), WHITE)
    image_panel(canvas, "05-tufty-hero.jpg", (0, 54, W, 790), focal=(0.50, 0.50), darken=0.95,
                label="PATRICIA URQUIOLA / TUFTY-TIME 20 / B&B ITALIA")
    draw = ImageDraw.Draw(canvas)
    meta(draw, 5, BLUE)
    draw.text((40, 792), "14", font=font(260, True), fill=BLUE)
    draw.text((386, 878), "个模块", font=font(74, True), fill=BLACK)
    draw.text((386, 972), "不必固定", font=font(74, True), fill=BLACK)
    image_panel(canvas, "05-tufty-a.webp", (40, 1080, 562, 1510), focal=(0.50, 0.50), border=4)
    image_panel(canvas, "05-tufty-b.webp", (590, 1080, 1204, 1510), focal=(0.50, 0.50), border=4)
    draw.rectangle((40, 1008, 1204, 1050), fill=BLUE)
    draw.text((58, 1029), "可拆解、可重组，才配得上二十年的使用周期。", font=font(25, True), fill=WHITE, anchor="lm")
    source(draw, "Philippe Jarrigeon｜Patricia Urquiola, Tufty-Time 20｜PIN–UP 38", light=True)
    return save(canvas, 5)


def make_rugs() -> Path:
    canvas = Image.new("RGBA", (W, H), ORANGE)
    image_panel(canvas, "06-rugs-hero.jpg", (0, 54, 760, H), focal=(0.50, 0.48), darken=0.96,
                label="WILD ANIMALS / GRANDMA PATTERNS / CC-TAPIS")
    draw = ImageDraw.Draw(canvas)
    meta(draw, 6, TURQ)
    draw.rectangle((796, 94, 1204, 654), fill=TURQ)
    draw.text((830, 132), "图案", font=font(96, True), fill=BLACK)
    draw.text((830, 246), "可以", font=font(96, True), fill=BLACK)
    draw.text((830, 360), "失控", font=font(96, True), fill=BLACK)
    draw.rectangle((796, 692, 1204, 1548), fill=BLACK)
    draw_wrapped(draw, (832, 740), "Rop van Mierlo 把湿画法的偶然性带进手工地毯：格纹仍在，却不再服从笔直的边界。", 330, 31, WHITE, bold=True, spacing=12)
    draw.text((832, 1328), "秩序", font=font(72, True), fill=ORANGE)
    draw.text((832, 1416), "也该留一点缝隙", font=font(36, True), fill=WHITE)
    source(draw, "Francesco Nazardo｜Wild Animals, Grandma Patterns｜PIN–UP 38", light=True)
    return save(canvas, 6)


def make_frog() -> Path:
    canvas = Image.new("RGBA", (W, H), BLUE)
    image_panel(canvas, "07-frog-hero.jpg", (0, 54, W, 838), focal=(0.50, 0.50), darken=0.90,
                label="PIERO LISSONI / FROG / LIVING DIVANI")
    image_panel(canvas, "07-frog-a.jpg", (40, 878, 590, 1322), focal=(0.50, 0.50), border=4)
    image_panel(canvas, "07-frog-b.jpg", (628, 878, 932, 1322), focal=(0.50, 0.48), border=4)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 7, ORANGE)
    draw.rectangle((970, 878, 1204, 1518), fill=WHITE)
    draw.text((1002, 920), "30", font=font(96, True), fill=ORANGE)
    draw.text((1004, 1026), "年", font=font(66, True), fill=BLACK)
    draw_wrapped(draw, (1002, 1142), "Frog 的比例曾经太低、太宽；三十年后，它仍能用新材料继续跳跃。", 164, 26, BLACK, bold=True, spacing=10)
    draw.text((42, 1422), "经典，不是原地不动。", font=font(56, True), fill=WHITE)
    source(draw, "Francesco Nazardo｜Piero Lissoni, Frog｜PIN–UP 38", light=True)
    return save(canvas, 7)


def make_rocks() -> Path:
    canvas = Image.new("RGBA", (W, H), BLACK)
    image_panel(canvas, "08-rocks-hero.jpg", (0, 54, W, 774), focal=(0.50, 0.50), darken=0.88,
                label="FRANCESCO BINFARÉ / ON THE ROCKS / EDRA")
    image_panel(canvas, "08-rocks-a.jpg", (40, 816, 600, 1264), focal=(0.50, 0.50), border=4)
    image_panel(canvas, "08-rocks-b.jpg", (630, 816, 1204, 1264), focal=(0.50, 0.50), border=4)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 8, PINK)
    draw.rectangle((40, 1306, 1204, 1568), fill=PINK)
    draw.text((72, 1336), "沙发", font=font(82, True), fill=BLACK)
    draw.text((320, 1336), "是身体的地形", font=font(61, True), fill=BLACK)
    draw_wrapped(draw, (76, 1442), "四块手工塑形座面、两块可移动靠背，让每一种坐姿都能找到自己的坡度。", 1050, 27, BLACK, bold=True, spacing=8)
    source(draw, "Francesco Nazardo｜Francesco Binfaré, On the Rocks｜PIN–UP 38", light=True)
    return save(canvas, 8)


def make_poliform() -> Path:
    canvas = Image.new("RGBA", (W, H), TURQ)
    image_panel(canvas, "09-poliform-ketch.jpg", (0, 54, 600, H), focal=(0.50, 0.50), darken=0.90,
                label="JEAN-MARIE MASSAUD / KETCH / POLIFORM")
    image_panel(canvas, "09-poliform-ernest.jpg", (630, 54, 1242, 780), focal=(0.50, 0.50), darken=0.93,
                label="ERNEST SOFA SYSTEM / POLIFORM")
    image_panel(canvas, "09-poliform-a.jpg", (630, 816, 944, 1360), focal=(0.50, 0.48), border=4)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 9, ORANGE)
    draw.rectangle((976, 816, 1204, 1360), fill=WHITE)
    draw.text((1006, 862), "户外", font=font(51, True), fill=BLACK)
    draw.text((1006, 930), "不只", font=font(51, True), fill=ORANGE)
    draw.text((1006, 998), "在外", font=font(51, True), fill=BLACK)
    draw_wrapped(draw, (1006, 1100), "Ketch 与 Ernest 都把柔软的身体经验放到可变的场景里。", 158, 24, BLACK, bold=True, spacing=9)
    draw.rectangle((630, 1400, 1204, 1568), fill=BLACK)
    draw_wrapped(draw, (664, 1434), "形式必须允许人、天气和空间一起改变。", 500, 33, WHITE, bold=True, spacing=10)
    source(draw, "Francesco Nazardo / Philippe Jarrigeon｜Poliform｜PIN–UP 38", light=True)
    return save(canvas, 9)


def make_finale() -> Path:
    canvas = Image.new("RGBA", (W, H), LIME)
    image_panel(canvas, "10-camelot-hero.jpg", (0, 54, W, 884), focal=(0.50, 0.50), darken=0.92,
                label="ANTONIO CITTERIO / CAMELOT / FLEXFORM")
    image_panel(canvas, "10-camelot-a.webp", (40, 932, 720, 1528), focal=(0.50, 0.50), border=4)
    draw = ImageDraw.Draw(canvas)
    meta(draw, 10, ORANGE)
    draw.rectangle((758, 932, 1204, 1528), fill=BLACK)
    draw.text((798, 978), "物件", font=font(72, True), fill=WHITE)
    draw.text((798, 1064), "要为", font=font(72, True), fill=ORANGE)
    draw.text((798, 1150), "变化", font=font(72, True), fill=WHITE)
    draw.text((798, 1236), "留位", font=font(72, True), fill=WHITE)
    draw.line((798, 1338, 1162, 1338), fill=LIME, width=12)
    draw_wrapped(draw, (798, 1380), "能修、能变、能容纳身体，才是大设计真正的大。", 354, 28, WHITE, bold=True, spacing=10)
    source(draw, "Philippe Jarrigeon｜Antonio Citterio, Camelot｜PIN–UP 38", light=True)
    return save(canvas, 10)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#bdb7ae")
    for i, path in enumerate(paths):
        thumb = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(OUT / "preview.jpg", quality=94, subsampling=0)


def write_files() -> None:
    title = "PIN–UP 38｜大设计不等于大尺寸"
    body = (
        "设计一旦被放大，最先被看见的往往是价格、体积和造型。但 PIN–UP 38 的 XXL Big Design Issue 把问题问得更具体：一件物品凭什么值得占据我们的空间？\n\n"
        "Faye Toogood 把 Solar 沙发做成可陷入的软雕塑；Formafantasma 的 SuperWire 让灯具的光源和螺丝都能被替换；Patricia Urquiola 的 Tufty-Time 20 用 14 个模块延长一套沙发的变化周期。它们都不把“新”理解成换一件新的。\n\n"
        "Wild Animals 把湿画法的偶然带进手工地毯，让格纹松开边界；Piero Lissoni 的 Frog 用三十年证明，经典需要继续适应材料与身体；On the Rocks 则把沙发变成可调整的身体地形。Poliform 的 Ketch 和 Ernest 更把室内外、固定与流动之间的界线放松下来。\n\n"
        "好的大设计，不是往房间里塞进更大的物体，而是让物体能陪着生活改变：能修、能换、能重新组合，也能经得起被反复使用。你会为家里哪一件物品保留十年以上？"
    )
    body += "\n\n它们提醒我们，产品设计真正该争取的不是瞬间的视觉占有，而是一次次被坐下、拆开、挪动和修好的机会。当生活发生变化，能继续工作并让人愿意保留的物件，才会真正塑造空间的质量。"
    tags = "#PINUP #PINUP38 #家具设计 #意大利设计 #产品设计 #室内设计 #当代设计 #沙发设计"
    (OUT / "发布文案.md").write_text(f"{title}\n\n{body}\n\n{tags}\n", encoding="utf-8")
    sources = f"""# PIN–UP 38 图片与内容来源
- 第01页：PIN–UP 38 官方期号页 {ISSUE_URL}
- 第03页：Faye Toogood, Solar for Tacchini {SOLAR_URL}
- 第04页：Formafantasma, SuperWire for Flos {SUPERWIRE_URL}
- 第05页：Patricia Urquiola, Tufty-Time 20 for B&B Italia {TUFTY_URL}
- 第06页：Wild Animals, Grandma Patterns for cc-tapis {RUGS_URL}
- 第07页：Piero Lissoni, Frog for Living Divani {FROG_URL}
- 第08页：Francesco Binfaré, On the Rocks for Edra {ROCKS_URL}
- 第09页：Jean-Marie Massaud, Ketch and Ernest for Poliform {POLIFORM_URL}
- 第10页：Antonio Citterio, Camelot for Flexform {CAMELOT_URL}

图片均来自 PIN–UP 官方文章或官方期号页。图片版权归 PIN–UP、原摄影师、设计师与项目方所有；商业投放前请另行核验授权。
"""
    (OUT / "图片来源.md").write_text(sources, encoding="utf-8")
    manifest = {
        "type": "magazine",
        "slug": "pinup-38",
        "issue": "PIN–UP 38 · XXL BIG DESIGN",
        "date": "S/S 2025",
        "core_question": "大设计，凭什么值得占据空间？",
        "core_thesis": "好设计不靠体积取胜，而靠它如何被使用、修复、重组与长期共处。",
        "pages": [
            "01 封面：大设计不是大尺寸",
            "02 中文目录：本期内容导览",
            "03 Faye Toogood：软，也能成形",
            "04 Formafantasma：坏了也能修",
            "05 Patricia Urquiola：14个模块，不必固定",
            "06 Wild Animals：图案可以失控",
            "07 Piero Lissoni：经典，不是原地不动",
            "08 Francesco Binfaré：沙发是身体的地形",
            "09 Jean-Marie Massaud：户外不只在外",
            "10 Antonio Citterio：物件要为变化留位",
        ],
    }
    POST.parent.mkdir(parents=True, exist_ok=True)
    POST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        make_cover(), make_contents(), make_solar(), make_superwire(), make_tufty(),
        make_rugs(), make_frog(), make_rocks(), make_poliform(), make_finale(),
    ]
    make_preview(paths)
    write_files()
    print(f"Created {len(paths)} PIN–UP 38 cards in {OUT}")


if __name__ == "__main__":
    main()
