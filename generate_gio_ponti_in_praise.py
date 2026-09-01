#!/usr/bin/env python3
"""Render a six-card Xiaohongshu post for Gio Ponti's In Praise of Architecture."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "gio-ponti-in-praise-of-architecture"
OUTPUT = ROOT / "output" / "gio-ponti-in-praise-of-architecture"
W, H = 1242, 1660

BOOK = {
    "designer": "吉奥·庞蒂",
    "designer_en": "GIO PONTI",
    "book": "In Praise of Architecture",
    "book_cn": "《赞美建筑》",
    "edition": "F. W. Dodge Corporation, 1960｜Open Library OL6273922M",
    "question": "建筑为什么必须让人愉悦？",
    "thesis": "好建筑不靠沉重表达永恒，而让结构、表皮、尺度与使用共同获得轻盈、精确和愉悦。",
    "palette": {
        "paper": (243, 238, 228),
        "ink": (20, 40, 42),
        "teal": (43, 123, 122),
        "coral": (216, 92, 69),
        "yellow": (230, 200, 100),
        "gray": (140, 153, 148),
    },
    "cards": [
        {
            "name": "Montecatini 总部",
            "headline": "轻盈来自所有部件共同变薄",
            "body": "办公楼并不靠一个醒目姿态成立。曲面端部、连续开口与细致表皮一起削弱体量重量，让大型组织仍保持清楚、明快的城市轮廓。",
            "asset": "02-montecatini.jpg",
            "tag": "米兰 / 总部建筑群 / 1930—50年代",
            "centering": (0.50, 0.52),
        },
        {
            "name": "De Bijenkorf",
            "headline": "立面可以像织物，而不是包装",
            "body": "绿色陶瓷表面、窄窗与不规则几何把庞大的百货体量拆成可阅读的纹理。表皮既回应城市距离，也保留接近时的触觉尺度。",
            "asset": "03-bijenkorf.jpg",
            "tag": "埃因霍温 / 百货商店 / 1969",
            "centering": (0.52, 0.47),
        },
        {
            "name": "丹佛艺术博物馆",
            "headline": "封闭体量，也能让观看持续移动",
            "body": "窄长开口、切角轮廓与反光饰面让厚重体块随距离和光线改变。建筑不是一张正立面，而是一连串绕行中出现的片段。",
            "asset": "04-denver-art-museum.jpg",
            "tag": "丹佛 / 马丁大楼 / 1971",
            "centering": (0.50, 0.46),
        },
        {
            "name": "Superleggera",
            "headline": "删到最后，仍要留下身体的舒适",
            "body": "纤细木框与编织座面把重量减到最低，却没有牺牲坐姿与触感。轻盈不是视觉把戏，而是结构效率、手工尺度和日常使用的共同结果。",
            "asset": "05-superleggera.jpg",
            "tag": "Cassina / 家具实物 / 1957",
            "centering": (0.50, 0.43),
        },
    ],
    "summary": "轻盈不是少做，而是让每一部分都承担清楚的作用，并把精确转化成使用时的愉悦。",
    "chain": ["结构", "轮廓", "表皮", "尺度", "愉悦"],
    "methods": [
        "先找出体量最沉重的关系，再从轮廓与开口开始减重",
        "把表皮当作可在远近两种距离阅读的构造",
        "删减构件时，同时检查身体、触感与使用动作",
    ],
    "publish_title": "庞蒂：建筑为什么必须愉悦？",
    "publish_paragraphs": [
        "《In Praise of Architecture》不是一本教人复制意大利风格的图册，而是吉奥·庞蒂对建筑作为艺术、技术与生活经验的持续辩护。",
        "轻盈也不等于把结构做薄、把颜色调淡；真正的轻盈来自轮廓、开口、材料、尺度与使用互相校准，让复杂建筑看起来仍然清楚。",
        "Montecatini 总部用曲面端部与连续开口削弱办公体量；De Bijenkorf 让陶瓷表皮成为城市尺度的织物；丹佛艺术博物馆通过窄窗、切角和反光饰面，让观看在绕行中不断变化；Superleggera 则把椅子减到纤细木框与编织座面，仍保留身体的舒适。",
        "对设计师更实用的工作法是：先找出方案最沉重的关系，再从轮廓和开口开始减重；把表皮同时放到远景与近距离检查；删掉构件时，继续追问身体是否更自在。",
        "庞蒂真正赞美的不是某种造型，而是精确最终能够变成生活中的愉悦。你的方案里，哪一个部分还在用重量假装重要？",
    ],
    "tags": "#吉奥庞蒂  #GioPonti  #InPraiseOfArchitecture  #意大利建筑  #建筑理论  #轻盈设计  #建筑书单  #设计方法",
}


def toned(image: Image.Image, saturation: float = 0.82, contrast: float = 1.06) -> Image.Image:
    image = image.convert("RGB")
    return ImageEnhance.Contrast(ImageEnhance.Color(image).enhance(saturation)).enhance(contrast)


def fit_title(draw: ImageDraw.ImageDraw, xy, text: str, width: int, size: int, fill) -> int:
    font = base.get_font(size, bold=True, serif=True)
    lines = base.wrap(draw, text, font, width)
    while len(lines) > 3 and size > 38:
        size -= 2
        font = base.get_font(size, bold=True, serif=True)
        lines = base.wrap(draw, text, font, width)
    value = "\n".join(lines)
    draw.multiline_text(xy, value, font=font, fill=fill, spacing=9)
    return draw.multiline_textbbox(xy, value, font=font, spacing=9)[3]


def cover() -> Image.Image:
    p = BOOK["palette"]
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)

    # A faceted field occupies the right side; the verified book cover remains an untouched layer.
    facets = [
        ([(720, 0), (1242, 0), (1050, 390), (770, 310)], p["teal"]),
        ([(770, 310), (1050, 390), (920, 860), (650, 670)], p["yellow"]),
        ([(1050, 390), (1242, 0), (1242, 830), (920, 860)], p["coral"]),
        ([(650, 670), (920, 860), (800, 1320), (585, 1120)], p["teal"]),
        ([(920, 860), (1242, 830), (1242, 1660), (800, 1320)], p["paper"]),
    ]
    for points, color in facets:
        draw.polygon(points, fill=color)
        draw.line(points + [points[0]], fill=p["ink"], width=5, joint="curve")

    draw.text((66, 52), "GIO PONTI / IN PRAISE OF ARCHITECTURE / 01", font=base.get_font(20, bold=True), fill=p["paper"])
    draw.line((66, 101, 690, 101), fill=p["coral"], width=8)
    draw.text((70, 170), "建筑为什么", font=base.get_font(69, bold=True, serif=True), fill=p["paper"])
    draw.text((70, 257), "必须让人愉悦？", font=base.get_font(69, bold=True, serif=True), fill=p["paper"])
    base.text_block(draw, (72, 382), BOOK["thesis"], base.get_font(31), p["yellow"], 565, 13)

    base.paste_cover(image, base.open_image(ASSETS / "cover.jpg"), (86, 650, 610, 1450), shadow=True)
    draw = ImageDraw.Draw(image)
    draw.rectangle((86, 1465, 610, 1515), fill=p["coral"])
    draw.text((105, 1477), "VERIFIED 1960 F. W. DODGE EDITION", font=base.get_font(17, bold=True), fill=p["paper"])
    draw.text((712, 1410), BOOK["book_cn"], font=base.get_font(36, bold=True), fill=p["ink"])
    draw.text((712, 1465), "LIGHTNESS / PRECISION / JOY", font=base.get_font(18, bold=True), fill=p["teal"])
    base.draw_page_mark(draw, 1, p["ink"], light=True)
    return image


def interior(number: int) -> Image.Image:
    p = BOOK["palette"]
    card = BOOK["cards"][number - 2]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 108), fill=p["ink"])
    draw.text((62, 34), f"GIO PONTI / FACETED LIGHTNESS / 0{number}", font=base.get_font(20, bold=True), fill=p["paper"])

    source = toned(base.open_image(ASSETS / card["asset"]), 0.78 if number != 2 else 0.15, 1.08)
    photo = base.crop(source, (W, 810), card["centering"])
    image.paste(photo, (0, 108))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 824, W, 920), fill=p["ink"])
    draw.text((62, 847), card["name"], font=base.get_font(31, bold=True), fill=p["paper"])
    draw.text((1080, 838), f"0{number}", font=base.get_font(47, bold=True, serif=True), fill=p["coral"])
    draw.text((68, 950), card["tag"], font=base.get_font(19, bold=True), fill=p["teal"])
    y = fit_title(draw, (68, 1012), card["headline"], 1055, 49, p["ink"])
    draw.line((68, y + 22, 520, y + 22), fill=p["coral"], width=8)
    base.text_block(draw, (70, y + 62), card["body"], base.get_font(29), p["ink"], 1040, 12)
    draw.text((70, 1560), f"{BOOK['book_cn']} / REAL WORK IMAGE", font=base.get_font(18, bold=True), fill=p["gray"])
    base.draw_page_mark(draw, number, p["ink"])
    return image


def summary() -> Image.Image:
    p = BOOK["palette"]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((66, 65), "让精确变成愉悦", font=base.get_font(66, bold=True, serif=True), fill=p["ink"])
    base.text_block(draw, (70, 165), BOOK["summary"], base.get_font(31), p["teal"], 1020, 12)

    # Three tapered blades rise from the methods into one light central result.
    blades = [
        ([(92, 1340), (310, 1340), (530, 460), (430, 420)], p["coral"]),
        ([(455, 1450), (690, 1450), (670, 390), (570, 350)], p["yellow"]),
        ([(825, 1340), (1088, 1340), (825, 470), (725, 430)], p["teal"]),
    ]
    for points, color in blades:
        draw.polygon(points, fill=color)
        draw.line(points + [points[0]], fill=p["ink"], width=4)

    nodes = [(470, 540), (595, 675), (700, 835), (790, 1010), (865, 1200)]
    for i, (label, (x, y)) in enumerate(zip(BOOK["chain"], nodes), 1):
        draw.ellipse((x - 52, y - 52, x + 52, y + 52), fill=p["ink"], outline=p["paper"], width=4)
        draw.text((x - 28, y - 16), label, font=base.get_font(20, bold=True), fill=p["paper"])
        draw.text((x - 10, y + 60), f"0{i}", font=base.get_font(15, bold=True), fill=p["ink"])

    method_y = [610, 855, 1110]
    for i, (method, y) in enumerate(zip(BOOK["methods"], method_y), 1):
        x = 68 if i != 2 else 720
        width = 330 if i != 2 else 440
        draw.rectangle((x, y, x + width, y + 190), fill=p["paper"], outline=[p["coral"], p["yellow"], p["teal"]][i - 1], width=6)
        draw.text((x + 18, y + 18), f"METHOD 0{i}", font=base.get_font(17, bold=True), fill=[p["coral"], p["ink"], p["teal"]][i - 1])
        base.text_block(draw, (x + 18, y + 58), method, base.get_font(23, bold=True), p["ink"], width - 36, 8)

    draw.text((68, 1532), "STRUCTURE → SURFACE → SCALE → USE", font=base.get_font(19, bold=True), fill=p["ink"])
    base.draw_page_mark(draw, 6, p["ink"])
    return image


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0)


def make_preview(paths: list[Path]) -> None:
    tw, th, gap = 360, 481, 24
    sheet = Image.new("RGB", (tw * 3 + gap * 4, th * 2 + gap * 3), (221, 218, 211))
    for i, path in enumerate(paths):
        with Image.open(path) as source:
            thumb = source.convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 3) * (tw + gap), gap + (i // 3) * (th + gap)))
    save(sheet.resize((1242, 1108), Image.Resampling.LANCZOS), OUTPUT / "preview.jpg")


def write_docs() -> None:
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    lines = [
        "# 图片来源", "",
        "| 文件名 | 内容 | 作者 / 机构 | 来源 URL | 许可 / 版权 | 修改 |",
        "|---|---|---|---|---|---|",
    ]
    for item in manifest:
        lines.append(f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item['modifications']} |")
    lines += [
        "",
        "02—05 均使用可核验的真实建筑或家具实物图片；没有使用 AI 建筑图或自制示意图代替作品。",
        "书封仅用于书籍识别、介绍与评论；保持原始文字与比例，未重绘。",
        "卡片文字为基于书籍与项目资料的编辑性概括，不作为原书直接引语。",
    ]
    (OUTPUT / "图片来源.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    publication = BOOK["publish_title"] + "\n\n" + "\n\n".join(BOOK["publish_paragraphs"]) + "\n\n" + BOOK["tags"] + "\n"
    (OUTPUT / "发布文案.md").write_text(publication, encoding="utf-8")

    post = {
        "designer": BOOK["designer"],
        "book": BOOK["book"],
        "edition": BOOK["edition"],
        "thesis": BOOK["thesis"],
        "publish_title": BOOK["publish_title"],
        "title_length": len(BOOK["publish_title"]),
        "concept_chain": BOOK["chain"],
        "endcards": {
            "01": {
                "layout_rationale": "书封在深色左下形成大尺度档案物，标题悬于上部，右侧晶体切面把轻盈转译成方向性张力。",
                "changed_variables": ["左下大书封", "右侧晶体场", "上部横向问题", "深底高对比"],
            },
            "06": {
                "layout_rationale": "三条由方法向上收束的锥形路径托起概念链，结论从底部工作法逐步变成愉悦。",
                "changed_variables": ["三束锥形路径", "斜向概念节点", "分散方法框", "浅底收束"],
            },
        },
        "transferable_methods": BOOK["methods"],
        "sources": manifest,
        "cards": [
            {"number": "01", "role": "problem cover", "headline": BOOK["question"], "asset": "cover.jpg"},
            *[
                {"number": f"{i:02d}", "role": "mechanism" if i == 2 else "evidence", "headline": card["headline"], "evidence": card["name"], "asset": card["asset"]}
                for i, card in enumerate(BOOK["cards"], 2)
            ],
            {"number": "06", "role": "synthesis", "headline": BOOK["summary"], "asset": ""},
        ],
    }
    (OUTPUT / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if len(BOOK["publish_title"]) > 20:
        raise ValueError(f"title too long: {BOOK['publish_title']}")
    if not (ASSETS / "manifest.json").exists():
        raise FileNotFoundError("Run fetch_gio_ponti_in_praise.py first")
    cards = [cover(), *[interior(i) for i in range(2, 6)], summary()]
    paths = []
    for number, card in enumerate(cards, 1):
        path = OUTPUT / f"{number:02d}.jpg"
        save(card, path)
        paths.append(path)
    make_preview(paths)
    write_docs()
    print(f"Rendered {OUTPUT.name}; title length={len(BOOK['publish_title'])}")


if __name__ == "__main__":
    main()
