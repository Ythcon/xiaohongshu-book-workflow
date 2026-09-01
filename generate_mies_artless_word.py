#!/usr/bin/env python3
"""Render a six-card Xiaohongshu post for The Artless Word."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "mies-artless-word"
OUTPUT = ROOT / "output" / "mies-artless-word"
W, H = 1242, 1660

BOOK = {
    "designer": "密斯·凡·德·罗",
    "designer_en": "MIES VAN DER ROHE",
    "author": "Fritz Neumeyer",
    "book": "The Artless Word: Mies van der Rohe on the Building Art",
    "book_cn": "《The Artless Word》",
    "edition": "The MIT Press, 1994｜ISBN 9780262640329",
    "question": "少，为什么反而更难？",
    "thesis": "减法只有在结构、材料、尺度与细部彼此一致时才成立；否则只是空白。",
    "palette": {
        "paper": (241, 238, 230),
        "ink": (20, 23, 25),
        "bronze": (140, 91, 62),
        "red": (196, 79, 59),
        "bluegray": (98, 116, 122),
        "silver": (167, 172, 168),
    },
    "cards": [
        {
            "name": "巴塞罗那馆",
            "headline": "自由平面，不等于没有秩序",
            "body": "柱网独立支撑屋盖，石墙与玻璃墙沿轴线错动，空间因此连续却不失方向。所谓自由，建立在更严密的结构、材料与比例控制上。",
            "asset": "02-barcelona-pavilion.jpg",
            "tag": "巴塞罗那 / 1929｜1986年重建实景",
            "centering": (0.50, 0.53),
        },
        {
            "name": "图根哈特别墅",
            "headline": "结构退后，生活才得到连续背景",
            "body": "纤细钢柱、玻璃界面与自由分隔把承重和围护拆开。室内不再被房间逐格切断，而沿花园、家具与日常活动连续展开。",
            "asset": "03-villa-tugendhat.jpg",
            "tag": "布尔诺 / 1930",
            "centering": (0.50, 0.49),
        },
        {
            "name": "范斯沃斯住宅",
            "headline": "极少构件，会放大每一道边界",
            "body": "架空平台、屋顶与八根外露钢柱形成近乎不可隐藏的系统。构件越少，地面、水位、玻璃接缝与身体尺度之间的矛盾就越清楚。",
            "asset": "04-farnsworth-house.jpg",
            "tag": "伊利诺伊 / 1951",
            "centering": (0.50, 0.47),
        },
        {
            "name": "西格拉姆大厦",
            "headline": "细部重复，把高层变成城市秩序",
            "body": "青铜色竖向构件与深色玻璃把巨大立面压成稳定节奏；建筑向后退让出的广场，又把同一秩序从表皮扩展到街道。",
            "asset": "05-seagram-building.jpg",
            "tag": "纽约 / 1958",
            "centering": (0.50, 0.42),
        },
    ],
    "summary": "少不是删到空，而是把无法协调的关系逐一解决，直到结构、材料、空间与城市只说同一句话。",
    "chain": ["网格", "结构", "界面", "细部", "城市"],
    "methods": [
        "先锁定跨距、柱网和边界，再讨论空间自由",
        "每删一个构件，都检查另一部分是否接住它的工作",
        "把节点放大到材料相接处，检验比例是否仍然成立",
    ],
    "publish_title": "密斯：少，为什么反而更难？",
    "publish_paragraphs": [
        "《The Artless Word》把密斯的文字、思想来源与建筑实践重新放在一起。它提醒设计师：所谓“少”，从来不是把画面清空，也不是给方案套上一层冷静风格。",
        "构件越少，每个决定承担的责任反而越大。柱网、墙体、玻璃、材料接缝与人的尺度只要有一处失去协调，整个空间就会暴露问题。",
        "巴塞罗那馆把独立柱网与错动墙面组织成连续路径；图根哈特别墅让结构退后，使生活沿花园与自由分隔展开；范斯沃斯住宅用两片平台和外露钢柱放大场地、边界与身体的矛盾；西格拉姆大厦则用竖向细部的重复建立高层秩序，并通过退让广场把秩序延伸到街道。",
        "对设计师更实用的方法是：先锁定跨距、柱网和边界，再讨论自由；每删一个构件，都检查另一部分是否接住它的工作；最后把节点放大到材料相接处，确认比例依然成立。",
        "减法不是少做决定，而是让决定彼此不再冲突。你的方案里，哪一个被删掉的部分，其实还没有找到新的承担者？",
    ],
    "tags": "#密斯凡德罗  #MiesVanDerRohe  #TheArtlessWord  #现代主义建筑  #建筑细部  #建筑理论  #建筑书单  #设计方法",
}


def toned(image: Image.Image, saturation: float = 0.74, contrast: float = 1.08) -> Image.Image:
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
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)

    # Orthogonal planes organize the page like a precise joint; the cover is a large locked layer.
    draw.rectangle((0, 0, 126, H), fill=p["ink"])
    draw.rectangle((126, 0, 1242, 142), fill=p["bronze"])
    draw.rectangle((126, 142, 670, 950), fill=p["paper"])
    draw.rectangle((126, 950, 700, H), fill=p["bluegray"])
    draw.rectangle((700, 142, W, H), fill=p["ink"])
    draw.line((126, 142, 126, H), fill=p["red"], width=8)
    draw.line((126, 950, W, 950), fill=p["red"], width=8)

    draw.text((165, 50), "MIES VAN DER ROHE / THE ARTLESS WORD / 01", font=base.get_font(20, bold=True), fill=p["paper"])
    draw.text((175, 215), "少，为什么", font=base.get_font(76, bold=True, serif=True), fill=p["ink"])
    draw.text((175, 310), "反而更难？", font=base.get_font(76, bold=True, serif=True), fill=p["ink"])
    base.text_block(draw, (178, 445), BOOK["thesis"], base.get_font(32), p["bronze"], 430, 13)
    draw.text((180, 780), "ORDER / STRUCTURE / DETAIL", font=base.get_font(18, bold=True), fill=p["bluegray"])

    base.paste_cover(image, base.open_image(ASSETS / "cover.jpg"), (735, 215, 1168, 900), shadow=True)
    draw = ImageDraw.Draw(image)
    draw.rectangle((735, 908, 1168, 960), fill=p["red"])
    draw.text((752, 921), "VERIFIED MIT PRESS COVER", font=base.get_font(18, bold=True), fill=p["paper"])
    draw.text((180, 1030), BOOK["book_cn"], font=base.get_font(38, bold=True), fill=p["paper"])
    draw.text((180, 1090), "FRITZ NEUMEYER", font=base.get_font(23, bold=True), fill=p["ink"])
    base.text_block(draw, (180, 1190), "减法不是空白；它要求每一个留下的构件都承担更清楚的工作。", base.get_font(32), p["paper"], 465, 14)
    draw.text((760, 1510), BOOK["edition"], font=base.get_font(17, bold=True), fill=p["silver"])
    base.draw_page_mark(draw, 1, p["ink"], light=True)
    return image


def interior(number: int) -> Image.Image:
    p = BOOK["palette"]
    card = BOOK["cards"][number - 2]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 108), fill=p["ink"])
    draw.text((62, 34), f"MIES / PRECISION JOINT / 0{number}", font=base.get_font(20, bold=True), fill=p["paper"])

    source = toned(base.open_image(ASSETS / card["asset"]), 0.80, 1.07)
    photo = base.crop(source, (W, 810), card["centering"])
    image.paste(photo, (0, 108))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 824, W, 920), fill=p["ink"])
    draw.text((62, 847), card["name"], font=base.get_font(31, bold=True), fill=p["paper"])
    draw.text((1080, 838), f"0{number}", font=base.get_font(47, bold=True, serif=True), fill=p["red"])
    draw.text((68, 950), card["tag"], font=base.get_font(19, bold=True), fill=p["bronze"])
    y = fit_title(draw, (68, 1012), card["headline"], 1055, 49, p["ink"])
    draw.line((68, y + 22, 520, y + 22), fill=p["red"], width=8)
    base.text_block(draw, (70, y + 62), card["body"], base.get_font(29), p["ink"], 1040, 12)
    draw.text((70, 1560), f"{BOOK['book_cn']} / VERIFIED PROJECT PHOTO", font=base.get_font(18, bold=True), fill=p["silver"])
    base.draw_page_mark(draw, number, p["ink"])
    return image


def summary() -> Image.Image:
    p = BOOK["palette"]
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((66, 62), "少，是更严密的协调", font=base.get_font(64, bold=True, serif=True), fill=p["paper"])
    base.text_block(draw, (70, 165), BOOK["summary"], base.get_font(31), p["silver"], 1040, 12)

    # An exploded joint replaces the previous book's upward crystal paths.
    cx, cy = 620, 770
    layers = [
        ((180, 480, 1060, 565), p["bluegray"], "网格"),
        ((245, 605, 995, 695), p["bronze"], "结构"),
        ((310, 735, 930, 830), p["paper"], "界面"),
        ((375, 870, 865, 970), p["red"], "细部"),
        ((440, 1010, 800, 1120), p["silver"], "城市"),
    ]
    for i, (box, color, label) in enumerate(layers, 1):
        draw.rectangle(box, fill=color, outline=p["paper"], width=3)
        x0, y0, x1, y1 = box
        fill = p["ink"] if color in (p["paper"], p["silver"]) else p["paper"]
        draw.text(((x0 + x1) // 2, (y0 + y1) // 2), label, font=base.get_font(26, bold=True), fill=fill, anchor="mm")
        draw.text((x1 + 18, y0 + 25), f"0{i}", font=base.get_font(17, bold=True), fill=p["red"])
    draw.line((cx, 410, cx, 1185), fill=p["paper"], width=3)

    method_boxes = [(70, 1215, 405, 1510), (455, 1255, 790, 1550), (840, 1195, 1175, 1490)]
    colors = [p["red"], p["bronze"], p["bluegray"]]
    for i, (method, box, color) in enumerate(zip(BOOK["methods"], method_boxes, colors), 1):
        draw.rectangle(box, outline=color, width=7)
        draw.text((box[0] + 20, box[1] + 20), f"JOINT 0{i}", font=base.get_font(18, bold=True), fill=color)
        base.text_block(draw, (box[0] + 20, box[1] + 68), method, base.get_font(25, bold=True), p["paper"], box[2] - box[0] - 40, 9)
    base.draw_page_mark(draw, 6, p["ink"], light=True)
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
        "02—05 均使用可核验的真实建筑照片；巴塞罗那馆图片明确为重建后实景。没有使用 AI 建筑图或自制示意图代替项目。",
        "书封仅用于书籍识别、介绍与评论；保持原始文字与比例，未重绘。",
        "卡片文字为基于书籍与项目资料的编辑性概括，不作为密斯或作者的直接引语。",
    ]
    (OUTPUT / "图片来源.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    publication = BOOK["publish_title"] + "\n\n" + "\n\n".join(BOOK["publish_paragraphs"]) + "\n\n" + BOOK["tags"] + "\n"
    (OUTPUT / "发布文案.md").write_text(publication, encoding="utf-8")

    post = {
        "designer": BOOK["designer"],
        "author": BOOK["author"],
        "book": BOOK["book"],
        "edition": BOOK["edition"],
        "thesis": BOOK["thesis"],
        "publish_title": BOOK["publish_title"],
        "title_length": len(BOOK["publish_title"]),
        "concept_chain": BOOK["chain"],
        "endcards": {
            "01": {
                "layout_rationale": "用正交板片与红色节点线建立结构性入口，书封占据右上大区块，标题留在左侧浅底。",
                "changed_variables": ["右上大书封", "左侧问题标题", "正交板片", "底部理论面板"],
            },
            "06": {
                "layout_rationale": "以五层爆炸节点表示从网格到城市的协调，三条方法作为不同方向的节点检查。",
                "changed_variables": ["横向爆炸节点", "中心竖轴", "底部错位方法框", "深色总结底"],
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
        raise FileNotFoundError("Run fetch_mies_artless_word.py first")
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
