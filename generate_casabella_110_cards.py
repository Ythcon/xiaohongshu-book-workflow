from __future__ import annotations

import json
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    BLUE,
    FONT_BOLD,
    FONT_SANS,
    FONT_SERIF,
    H,
    INK,
    LIGHT,
    MUTED,
    PAPER,
    ROOT,
    W,
    draw_fit,
    font,
    header,
    make_card,
    make_preview,
    mount,
    page_mark,
    paper_canvas,
    rgba,
)


CFG = {
    "slug": "casabella-110",
    "issue": "CASABELLA 110",
    "date": "FEBBRAIO 1937 · ANNO X",
    "date_cn": "1937年2月",
    "cover": "book-cover.jpg",
    "accent": "#3f7692",
    "question": "资源与技术，\n如何变成\n空间秩序？",
    "thesis_label": "材料 × 制度 × 技术",
    "thesis": "110期把材料开采、公共制度、城市基础设施、安全与尺度标准放在一起：现代建筑不是先有形式，而是把外部条件转成结构、流线和界面。",
    "summary": "从采石场到政府建筑，现代设计把自然资源、公共程序和技术约束逐层翻译，最后形成可建造、可使用的空间秩序。",
    "concepts": ["材料链条", "程序分区", "技术底线"],
    "takeaways": [
        "从块度、加工和运输反推构件尺度，让形式尊重材料的真实来源。",
        "先把公共、办公、安全与服务流线分清，再决定体量与入口表情。",
        "把避难、设备与人体尺度写进早期平面，技术条件才不会变成补丁。",
    ],
    "publish_title": "110期｜技术如何进入建筑",
    "publish_body": "Casabella 110 讨论的不是一种现代外观，而是建筑如何接住现实条件：石材从哪里来，公共机构怎样运作，城市基础设施如何进入立面，安全和尺度标准又怎样提前写进平面。\n\nPagano 从 Ravaccione 采石场出发，把大理石理解为一条从开采、切割到运输的材料链。Bollate 的 Casa del Fascio 用连续外楼梯组织公共进入，把纪念性放在人的移动中。博洛尼亚 Palazzo del Gas 则以高门廊、转角体量和连续浮雕，把能源生产与城市街道叠合。\n\nPalanti 讨论民用建筑防空，提醒安全空间不能只是剩余地下室；分散入口、连续通道和结构隔离必须预先进入设计。Pica 评介 Neufert 的《建筑设计资料集》，把人体动作、设备尺寸和相邻关系转成可比较的尺度。利沃诺政府宫进一步说明，三座庭院、办公走廊与安全空间的分区，会直接塑造体量和开口。\n\n你会先从材料链、程序分区，还是安全与尺度标准重新检查一个方案？",
    "tags": "#Casabella #建筑杂志 #GiuseppePagano #GiancarloPalanti #建筑设计 #公共建筑 #材料设计 #建筑史",
    "cards": [
        {
            "image": "02-ravaccione.jpg",
            "mode": "photo",
            "accent": "#3f7692",
            "focal": (0.52, 0.55),
            "source": "Giuseppe Pagano｜Potenza del marmo · La cava Ravaccione｜Casabella 110",
            "eyebrow": "观点 01｜设计从材料的来源开始",
            "title": "石材的块度与运输，早已在采石场规定建筑尺度",
            "body": "大理石进入建筑前，切缝、块度、吊运和运输路径已经限定可获得的构件。形式并非脱离生产条件后才被决定。",
        },
        {
            "image": "03-casa-del-fascio-crop.jpg",
            "mode": "photo",
            "accent": "#bd5b43",
            "focal": (0.58, 0.58),
            "source": "C. Magni / B. Opoczynski / A. Pasquali｜Casa del Fascio, Bollate｜Casabella 110",
            "eyebrow": "观点 02｜纪念性也可以来自流线",
            "title": "连续外楼梯把公共进入变成建筑最强的空间表情",
            "body": "底层容纳公共与集体活动，上层布置办公；外部大楼梯把两者连接成可见路径，纪念性来自进入过程，而不是附加装饰。",
        },
        {
            "image": "04-palazzo-gas.webp",
            "mode": "photo",
            "accent": "#6f816f",
            "focal": (0.50, 0.50),
            "source": "Alberto Legnani / Luciano Petrucci｜Palazzo del Gas, Bologna｜Casabella 110",
            "eyebrow": "观点 03｜基础设施也能塑造城市界面",
            "title": "门廊、转角体量与浮雕，把能源系统接入街道",
            "body": "建筑以高门廊承接行人，以退台顶层回应城市视野；连续浮雕把煤气的生产与日常使用写进公共立面。",
        },
        {
            "image": "05-air-raid-plan.png",
            "mode": "document",
            "accent": "#bd5b43",
            "source": "Giancarlo Palanti｜La protezione antiaerea negli edifici civili｜Casabella 110",
            "eyebrow": "观点 04｜安全空间必须预先进入平面",
            "title": "分散入口与连续通道，让避难不依赖单一路径",
            "body": "地下避难空间不能只是剩余地下室。入口位置、通道连续性、结构隔离与容纳人数，都应在建筑早期共同确定。",
        },
        {
            "image": "06-bauentwurfslehre-alt.jpg",
            "mode": "document",
            "accent": "#3f7692",
            "source": "Agnoldomenico Pica｜Bauentwurfslehre｜Casabella 110",
            "eyebrow": "观点 05｜标准化是可复用的判断工具",
            "title": "把身体动作与设备尺寸，翻译成可以比较的空间尺度",
            "body": "尺度图把动作范围、操作高度和相邻关系放在同一张图中。标准不是替代设计，而是减少基本尺寸的反复试算。",
        },
        {
            "image": "07-palazzo-governo.jpg",
            "mode": "photo",
            "accent": "#6f816f",
            "focal": (0.48, 0.47),
            "source": "Alberto Legnani / Armando Sabatini｜Palazzo del Governo, Livorno｜Casabella 110",
            "eyebrow": "观点 06｜制度程序决定体量差异",
            "title": "庭院、走廊与安全空间，先于正立面组织政府建筑",
            "body": "三座庭院和双侧办公走廊组织部门关系；面向安全空间的封闭体量与公共入口的开敞处理，对应不同程序需求。",
        },
    ],
}


def save_rgb(image: Image.Image, path: Path) -> None:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)


def render_frontispiece(source: Path, target: Path) -> None:
    if target.exists():
        return
    with fitz.open(source) as document:
        pixmap = document[0].get_pixmap(matrix=fitz.Matrix(3.2, 3.2), alpha=False)
        pixmap.save(target)


def crop_asset(source: Path, target: Path, box: tuple[int, int, int, int]) -> None:
    image = Image.open(source).convert("RGB").crop(box)
    image = ImageEnhance.Sharpness(image).enhance(1.18)
    image.save(target, quality=96, subsampling=0)


def prepare_assets(src: Path) -> None:
    frontispiece = src / "02-original-frontispiece.jpg"
    render_frontispiece(src / "original.pdf", frontispiece)
    with Image.open(frontispiece) as image:
        x_scale = image.width / 1498
        y_scale = image.height / 1659
    crop_asset(
        frontispiece,
        src / "02-ravaccione.jpg",
        tuple(round(value * scale) for value, scale in zip((340, 280, 1450, 1590), (x_scale, y_scale, x_scale, y_scale))),
    )
    with Image.open(src / "03-casa-del-fascio.jpg") as image:
        x_scale = image.width / 1536
        y_scale = image.height / 2089
    crop_asset(
        src / "03-casa-del-fascio.jpg",
        src / "03-casa-del-fascio-crop.jpg",
        tuple(round(value * scale) for value, scale in zip((330, 380, 1490, 1810), (x_scale, y_scale, x_scale, y_scale))),
    )


def make_cover(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(110)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]

    draw.rectangle((0, 0, 340, H), fill=rgba(BLUE))
    draw.text((54, 64), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(LIGHT, 190))
    draw.line((54, 112, 286, 112), fill=rgba(LIGHT, 80), width=2)
    draw.text((54, 176), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (54, 258), cfg["question"], 270, 500, 42, LIGHT, serif=True, spacing=14)

    draw.text((400, 58), cfg["issue"], font=font(FONT_BOLD, 31), fill=INK)
    draw.text((1166, 64), "GIUSEPPE PAGANO · DIRETTORE", font=font(FONT_SANS, 17), fill=MUTED, anchor="ra")
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (398, 126, 770, 850), True)

    draw.rectangle((340, 1055, W, 1065), fill=accent)
    draw.text((400, 1114), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (400, 1170), cfg["thesis"], 760, 270, 38, INK, serif=True, spacing=13)
    draw.text((400, 1510), "Giuseppe Pagano｜Casabella 110｜Febbraio 1937", font=font(FONT_SANS, 18), fill=MUTED)
    page_mark(draw, 1, False)

    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_summary(cfg: dict, out: Path) -> Path:
    canvas = paper_canvas(8110)
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, False)
    accent = cfg["accent"]

    draw.text((74, 158), "条件不是限制，而是空间的起点", font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (74, 225), cfg["summary"], 1080, 285, 48, INK, serif=True, spacing=16)

    blocks = [
        (74, 1140, "01", cfg["concepts"][0], cfg["takeaways"][0], "#3f7692", LIGHT),
        (260, 900, "02", cfg["concepts"][1], cfg["takeaways"][1], "#bd5b43", LIGHT),
        (446, 660, "03", cfg["concepts"][2], cfg["takeaways"][2], "#6f816f", LIGHT),
    ]
    for x, y, number, label, body, color, text_color in blocks:
        draw.rectangle((x, y, x + 720, y + 220), fill=rgba(color, 244))
        draw.text((x + 34, y + 31), number, font=font(FONT_BOLD, 24), fill=rgba(text_color, 175))
        draw.text((x + 112, y + 27), label, font=font(FONT_BOLD, 31), fill=text_color)
        draw_fit(draw, (x + 112, y + 84), body, 560, 105, 26, rgba(text_color, 225), spacing=9)

    draw.line((74, 1435, 1168, 1435), fill=rgba(INK, 58), width=2)
    draw.text((74, 1482), "外部条件  →  设计规则  →  空间秩序", font=font(FONT_BOLD, 25), fill=BLUE)
    page_mark(draw, 8, False)

    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def post_manifest(cfg: dict) -> dict:
    return {
        "type": "magazine",
        "slug": cfg["slug"],
        "issue": "Casabella 110",
        "date": cfg["date_cn"],
        "core_question": cfg["question"].replace("\n", ""),
        "core_thesis": cfg["thesis"],
        "pages": [
            "01 单期主线：资源与技术，如何变成空间秩序？",
            *[
                f"{number:02d} {card['source'].split('｜')[0]}：{card['title']}"
                for number, card in enumerate(cfg["cards"], 2)
            ],
            "08 总结：材料链条—程序分区—技术底线",
        ],
    }


def source_records() -> str:
    return """# Casabella 110 图片来源

- `book-cover.jpg`｜Casabella 110 官方历史封面｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/110-nz.jpg｜版权归原权利人；等比例放大，未改字。
- `02-original-frontispiece.jpg` / `02-ravaccione.jpg`｜Casabella 110 原刊 frontespizio，La cava Ravaccione｜Trento大学图书馆数字馆藏｜https://webapps.unitn.it/Biblioteca/it/Web/EngibankFile/1937%20Casabella%20%5Bperiodico%5D%20110.pdf｜原刊扫描渲染、裁切、缩放；版权归原权利人。
- `03-casa-del-fascio.jpg` / `03-casa-del-fascio-crop.jpg`｜C. Magni / B. Opoczynski / A. Pasquali，Casa del Fascio a Bollate，Casabella 原刊项目图｜Bollate Oggi，Archivio G. Minora｜https://bollateoggi.it/la-casa-del-fascio-e-poi-divenne-casa-del-popolo/｜裁切、缩放；版权归原权利人。
- `04-palazzo-gas.webp`｜Alberto Legnani / Luciano Petrucci，Palazzo del Gas，Bologna｜Bologna Online / Biblioteca Salaborsa｜https://www.bibliotecasalaborsa.it/bolognaonline/events/il_palazzo_del_gas_e_il_fregio_di_giorgio_giordani｜裁切、缩放；版权与使用条件以原来源页为准。
- `05-air-raid-plan.png`｜Piazza Risorgimento 公共防空避难所平面，1:1500｜Archivio Storico della Città di Torino / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Planimetria_rifugio_Piazza_Risorgimento.png｜CC BY-SA 4.0；缩放、排版。
- `06-bauentwurfslehre-alt.jpg`｜Ernst Neufert，《Bauentwurfslehre》1973版尺度图页｜Wasily / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Bladzijde_uit_Bauentwurfslehre.JPG｜CC BY-SA 4.0；裁切、缩放、排版。本图为同书后续版本图页，用于说明文章讨论的尺度标准方法。
- `07-palazzo-governo.jpg`｜Alberto Legnani / Armando Sabatini，Palazzo del Governo，Livorno｜Luca Aless / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Palazzo_del_governo_livorno.JPG｜CC BY-SA 3.0；裁切、缩放、排版。

本组用于建筑杂志内容整理与教育性发布；含 CC BY-SA 图像的衍生排版按兼容许可分享，商业投放前请逐张复核许可与平台规则。
"""


def write_text_files(cfg: dict, out: Path) -> None:
    publish = f"{cfg['publish_title']}\n\n{cfg['publish_body']}\n\n{cfg['tags']}\n"
    (out / "发布文案.md").write_text(publish, encoding="utf-8")
    (out / "图片来源.md").write_text(source_records(), encoding="utf-8")

    post_dir = ROOT / "posts" / cfg["slug"]
    post_dir.mkdir(parents=True, exist_ok=True)
    (post_dir / "post.json").write_text(
        json.dumps(post_manifest(cfg), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def render_issue(cfg: dict) -> None:
    src = ROOT / "assets" / cfg["slug"]
    out = ROOT / "output" / cfg["slug"]
    out.mkdir(parents=True, exist_ok=True)
    prepare_assets(src)

    paths = [make_cover(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(make_summary(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards, preview and publishing files in {out}")


if __name__ == "__main__":
    render_issue(CFG)
