#!/usr/bin/env python3
"""Render two six-card Xiaohongshu architecture-book posts."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "two-new-books-03"
OUTPUT_ROOT = ROOT / "output" / "two-new-books-03"
W, H = 1242, 1660


BOOKS = {
    "rafael-moneo-apuntes-sobre-21-obras": {
        "designer": "拉斐尔·莫内欧",
        "designer_en": "RAFAEL MONEO",
        "book": "Apuntes sobre 21 obras",
        "book_cn": "《21部作品笔记》",
        "edition": "Gustavo Gili, 2010｜ISBN 9788425223624",
        "question": "场地怎样改写类型？",
        "thesis": "类型不是可复制的外形，而是一套会被地形、历史、程序与建造不断改写的关系。",
        "system": "context-fold",
        "palette": {"paper": "#F1EDE2", "ink": "#122A35", "red": "#D54F3C", "blue": "#315F72", "green": "#617A69", "warm": "#D8B66A", "brick": "#9B5A45"},
        "cards": [
            ("梅里达罗马艺术博物馆", "旧类型，不必复制旧形式", "砖拱把罗马建筑的厚度与秩序转译成新的承重节奏；新展厅的轴线同时回应地下遗址，让历史成为空间结构而不是表面引用。", "02-merida.jpg", "遗址 / 砖拱 / 轴线"),
            ("圣塞巴斯蒂安库萨尔", "城市边界，可以改变体量判断", "两个半透明体量没有延续街区轮廓，而像停在河口与海岸之间的岩体。类型服从城市、海岸和夜间公共性的共同压力。", "03-kursaal.jpg", "海岸 / 河口 / 城市"),
            ("洛杉矶天使之后主教座堂", "仪式类型，要由路径与光重新建立", "偏转的中殿、厚墙与漫射光共同组织进场次序；教堂的识别不依赖历史样式，而来自身体移动中逐步出现的仪式感。", "04-la-cathedral.jpg", "路径 / 厚墙 / 光"),
            ("普拉多博物馆扩建", "介入历史，不等于模仿历史", "新砖体、旧修道院与下沉入口被串成连续路线。扩建保持自身年代，同时把旧馆、花园和城市重新接合。", "05-prado.jpg", "旧馆 / 花园 / 新路线"),
        ],
        "summary": "类型提供可讨论的起点，场地压力负责把它变成只属于此处的建筑。",
        "chain": ["类型", "地形", "历史", "程序", "建造"],
        "methods": ["先写下场地最不能忽略的三种压力", "用同一类型画两种相反的落位关系", "最后检查材料与路径是否仍在回答场地"],
        "endcards": {
            "01": {"layout_rationale": "海岸照片横向压住上半页，大比例真实红色书封从场地折线中抬起；标题占据左侧负空间。", "changed_variables": ["右下大书封", "上部海岸照片", "折线式标题", "红蓝强对比"]},
            "06": {"layout_rationale": "把类型放在中心，地形、历史、程序与建造从四个方向推压边界，形成平面式判断图。", "changed_variables": ["中心类型块", "四向压力", "浅色总结页", "底部方法条"]},
        },
        "publish_title": "莫内欧：场地怎样改写类型？",
        "publish_paragraphs": [
            "《Apuntes sobre 21 obras》让莫内欧回看二十一个项目，把类型、场地与建造判断放回方案形成的过程。",
            "类型不是可以直接套用的外形，场地也不是建筑完成后才补上的说明；真正的设计发生在两者彼此修正的时候。",
            "梅里达罗马艺术博物馆用砖拱重写古罗马空间秩序；库萨尔会议中心让两个半透明体量回应河口、海岸与城市；洛杉矶主教座堂通过偏转路径、厚墙和漫射光重新建立仪式类型；普拉多扩建则把新砖体、旧修道院与下沉入口串成连续路线。",
            "对设计师更实用的工作法是：先写下场地最不能忽略的三种压力，再用同一类型画两个相反落位，并检查材料、入口和公共路径是否仍在回答这些条件。",
            "类型负责提供可讨论的起点，场地负责让答案保持具体；好的建筑不是消灭原型，而是让原型在限制中变得只属于此处。",
        ],
        "tags": "#拉斐尔莫内欧  #ApuntesSobre21Obras  #建筑类型  #场地设计  #建筑理论  #设计方法  #建筑书单  #建筑案例",
    },
    "frei-otto-finding-form": {
        "designer": "弗雷·奥托",
        "designer_en": "FREI OTTO",
        "book": "Finding Form",
        "book_cn": "《寻找形式》",
        "edition": "Edition Axel Menges, 1996｜ISBN 9783930698660",
        "question": "轻，怎样成为结构方法？",
        "thesis": "形式不是先画出的轮廓，而是支点、荷载、材料与实验共同找到的平衡状态。",
        "system": "force-membrane",
        "palette": {"paper": "#EEECE4", "ink": "#12283A", "cyan": "#65A8B4", "red": "#E05943", "yellow": "#E5C364", "gray": "#6C7478", "white": "#F7F5EE"},
        "cards": [
            ("斯图加特轻型结构研究所", "实验建筑，让研究本身成为空间", "这座由蒙特利尔德国馆试验结构发展而来的建筑，把膜面、支点和索网保持为可读系统；原型不是缩小版造型，而是受力关系的验证。", "02-ile-stuttgart.jpg", "原型 / 支点 / 膜面"),
            ("慕尼黑奥林匹克公园", "连续屋顶，来自连续的力", "索网随高点、低点和场地起伏展开，把体育场、步行空间与地形连接成一片轻屋面。形状来自力的传递，而不是轮廓偏好。", "03-munich.jpg", "索网 / 高低点 / 地形"),
            ("曼海姆多功能厅", "先让材料变形，再决定最后形状", "木格网在平面编织后被整体抬升，弹性变形生成双曲曲面。施工过程不是执行结果，而是寻找形式的组成部分。", "04-multihalle.jpg", "木格网 / 抬升 / 变形"),
            ("汉诺威世博会日本馆", "最少材料，也能形成完整空间", "坂茂与奥托用纸管网壳和可回收围护控制重量与废弃物；轻不仅是视觉感受，也是材料、运输和拆解的系统判断。", "05-japan-pavilion.jpg", "纸管 / 网壳 / 可回收"),
        ],
        "summary": "轻不是一种造型风格，而是让力、材料与建造过程少走弯路。",
        "chain": ["支点", "荷载", "模型", "变形", "构造"],
        "methods": ["先固定支点、荷载与材料边界", "用绳网或薄膜模型比较多个平衡状态", "把最清楚的受力路径转成可建造节点"],
        "endcards": {
            "01": {"layout_rationale": "慕尼黑索网照片形成上部弧面，大比例真实书封落在左下锚点；问题标题沿右侧张力方向展开。", "changed_variables": ["左下大书封", "上部索网照片", "右侧纵向标题", "节点与拉索"]},
            "06": {"layout_rationale": "用一张垂链式受力网络连接五个判断节点，方法分别落在三个锚点，形成结构图式总结。", "changed_variables": ["垂链网络", "五个受力节点", "三处锚点方法", "深色总结页"]},
        },
        "publish_title": "奥托：轻，怎样成为结构方法？",
        "publish_paragraphs": [
            "《Finding Form》把弗雷·奥托与博多·拉施的实验、模型和结构研究放在一起，讨论形式怎样从材料行为中被找到。",
            "轻不是把建筑画得纤细，模型也不是完成方案后的展示品；两者都在暴露受力路径、材料极限和不必要的重量。",
            "斯图加特轻型结构研究所让试验结构本身成为可使用空间；慕尼黑奥运屋顶用连续索网连接高点、低点与地形；曼海姆多功能厅把平面木格网整体抬升，让弹性变形生成曲面；汉诺威世博会日本馆则以纸管网壳和可回收围护同时控制重量与废弃物。",
            "对设计师更实用的工作法是：先固定支点、荷载和材料边界，再用绳网或薄膜模型比较多个平衡状态，并把最清楚的受力路径转成可制造、可安装的节点。",
            "形式负责让力变得可见，实验负责让判断接受材料检验；越早把建造过程放进设计，越可能用更少的材料得到更完整的空间。",
        ],
        "tags": "#弗雷奥托  #FindingForm  #轻型结构  #找形设计  #建筑结构  #设计方法  #建筑书单  #建筑案例",
    },
}


def rgb(book: dict) -> dict[str, tuple[int, int, int]]:
    return {key: tuple(int(value[i:i + 2], 16) for i in (1, 3, 5)) for key, value in book["palette"].items()}


def toned(image: Image.Image, saturation: float = 0.82, contrast: float = 1.05) -> Image.Image:
    image = ImageEnhance.Color(image.convert("RGB")).enhance(saturation)
    return ImageEnhance.Contrast(image).enhance(contrast)


def fit_title(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, width: int, size: int, fill, *, serif: bool = True, spacing: int = 8) -> int:
    font = base.get_font(size, bold=True, serif=serif)
    lines = base.wrap(draw, text, font, width)
    while len(lines) > 4 and size > 34:
        size -= 2
        font = base.get_font(size, bold=True, serif=serif)
        lines = base.wrap(draw, text, font, width)
    draw.multiline_text(xy, "\n".join(lines), font=font, fill=fill, spacing=spacing)
    box = draw.multiline_textbbox(xy, "\n".join(lines), font=font, spacing=spacing)
    return box[3]


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, bg, fg, width: int) -> None:
    x, y = xy
    draw.rectangle((x, y, x + width, y + 46), fill=bg)
    draw.text((x + 14, y + 9), text, font=base.get_font(18, bold=True), fill=fg)


def cover_moneo(book: dict, assets: Path) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["paper"])
    photo = toned(base.crop(base.open_image(assets / "03-kursaal.jpg"), (W, 700), (0.52, 0.49)), 0.62, 1.08)
    image.paste(photo, (0, 0))
    overlay = Image.new("RGBA", (W, 700), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, W, 700), fill=(*p["ink"], 72))
    od.polygon([(0, 515), (430, 465), (700, 560), (W, 470), (W, 700), (0, 700)], fill=(*p["blue"], 120))
    image.paste(Image.alpha_composite(image.crop((0, 0, W, 700)).convert("RGBA"), overlay).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((66, 48), "RAFAEL MONEO / 21 WORKS / 01", font=base.get_font(21, bold=True), fill=p["paper"])
    draw.line((66, 96, 1176, 96), fill=p["red"], width=7)
    draw.text((66, 156), "场地怎样", font=base.get_font(74, bold=True, serif=True), fill=p["paper"])
    draw.text((66, 252), "改写类型？", font=base.get_font(74, bold=True, serif=True), fill=p["paper"])
    draw.text((70, 374), "TYPE IS A STARTING POINT, NOT AN ANSWER", font=base.get_font(20, bold=True), fill=p["warm"])
    # The official Spanish edition is intentionally large and left unaltered.
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (640, 480, 1168, 1255), shadow=True)
    draw = ImageDraw.Draw(image)
    label(draw, (786, 1265), "VERIFIED OFFICIAL COVER", p["red"], p["paper"], 330)
    draw.text((70, 760), book["book_cn"], font=base.get_font(38, bold=True), fill=p["red"])
    draw.text((70, 818), book["designer"], font=base.get_font(26, bold=True), fill=p["blue"])
    base.text_block(draw, (70, 912), book["thesis"], base.get_font(31), p["ink"], 500, 12)
    # A site line bends around the cover without touching it.
    points = [(65, 1290), (250, 1290), (330, 1210), (530, 1210), (590, 1325), (760, 1325)]
    draw.line(points, fill=p["red"], width=10, joint="curve")
    for x, y in points[:-1]:
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=p["red"])
    base.text_block(draw, (70, 1370), "类型 × 地形 × 历史 × 程序 × 建造", base.get_font(25, bold=True), p["green"], 780, 8)
    draw.text((920, 1540), "CONTEXT / TYPE", font=base.get_font(18, bold=True), fill=p["blue"])
    base.draw_page_mark(draw, 1, p["ink"])
    return image


def cover_otto(book: dict, assets: Path) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["ink"])
    photo = toned(base.crop(base.open_image(assets / "03-munich.jpg"), (W, 770), (0.50, 0.45)), 0.35, 1.12)
    image.paste(photo, (0, 0))
    overlay = Image.new("RGBA", (W, 770), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, W, 770), fill=(*p["ink"], 55))
    image.paste(Image.alpha_composite(image.crop((0, 0, W, 770)).convert("RGBA"), overlay).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((62, 48), "FREI OTTO / FINDING FORM / 01", font=base.get_font(21, bold=True), fill=p["white"])
    draw.line((62, 96, 1180, 96), fill=p["yellow"], width=6)
    # Force paths belong to the editorial layer, never the real book cover.
    anchors = [(95, 680), (375, 365), (650, 565), (900, 250), (1160, 610)]
    draw.line(anchors, fill=p["yellow"], width=5, joint="curve")
    for x, y in anchors:
        draw.ellipse((x - 14, y - 14, x + 14, y + 14), fill=p["red"], outline=p["white"], width=3)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (64, 610, 602, 1248), shadow=True)
    draw = ImageDraw.Draw(image)
    label(draw, (118, 1260), "PUBLISHER COVER / ISBN VERIFIED", p["cyan"], p["ink"], 420)
    draw.text((652, 840), "轻，怎样成为", font=base.get_font(62, bold=True, serif=True), fill=p["white"])
    draw.text((652, 928), "结构方法？", font=base.get_font(62, bold=True, serif=True), fill=p["white"])
    draw.text((656, 1036), "FORM IS FOUND", font=base.get_font(22, bold=True), fill=p["yellow"])
    base.text_block(draw, (655, 1100), book["thesis"], base.get_font(29), p["white"], 500, 11)
    # Right-side catenary diagram makes this cover structurally unlike Moneo's.
    curve = []
    for i in range(101):
        x = 650 + i * 5.1
        y = 1420 - 0.0105 * (x - 905) ** 2
        curve.append((x, y))
    draw.line(curve, fill=p["cyan"], width=7)
    draw.line((650, 1420, 650, 1518), fill=p["red"], width=6)
    draw.line((1160, 1420, 1160, 1518), fill=p["red"], width=6)
    draw.text((650, 1533), "SUPPORT", font=base.get_font(17, bold=True), fill=p["gray"])
    draw.text((1065, 1533), "SUPPORT", font=base.get_font(17, bold=True), fill=p["gray"])
    base.draw_page_mark(draw, 1, p["ink"], light=True)
    return image


def interior_moneo(book: dict, assets: Path, number: int) -> Image.Image:
    p = rgb(book)
    title, headline, body, filename, pressures = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 110), fill=p["ink"])
    draw.text((64, 34), f"RAFAEL MONEO / CONTEXT FOLD / 0{number}", font=base.get_font(21, bold=True), fill=p["paper"])
    side = 250
    photo_x = side if number % 2 == 0 else 0
    band_x = 0 if number % 2 == 0 else W - side
    photo = toned(base.crop(base.open_image(assets / filename), (W - side, 840), (0.5, 0.50)), 0.72, 1.07)
    image.paste(photo, (photo_x, 110))
    draw = ImageDraw.Draw(image)
    draw.rectangle((band_x, 110, band_x + side, 950), fill=p["blue"] if number in (2, 5) else p["brick"])
    draw.text((band_x + 42, 155), f"0{number}", font=base.get_font(76, bold=True, serif=True), fill=p["warm"])
    for i, word in enumerate(pressures.split(" / "), 1):
        y = 390 + (i - 1) * 136
        draw.text((band_x + 42, y), f"0{i}", font=base.get_font(17, bold=True), fill=p["paper"])
        base.text_block(draw, (band_x + 42, y + 28), word, base.get_font(25, bold=True), p["paper"], 168, 6)
        draw.line((band_x + 42, y + 82, band_x + 198, y + 82), fill=p["warm"], width=5)
    draw.rectangle((58, 864, 830, 952), fill=p["ink"])
    draw.text((84, 888), title, font=base.get_font(31, bold=True), fill=p["paper"])
    y = fit_title(draw, (68, 1015), headline, 1080, 48, p["ink"], spacing=8)
    draw.line((68, y + 25, 420, y + 25), fill=p["red"], width=9)
    base.text_block(draw, (70, y + 66), body, base.get_font(29), p["ink"], 1040, 12)
    draw.text((70, 1560), f"{book['book_cn']} / TYPE UNDER PRESSURE", font=base.get_font(18, bold=True), fill=p["blue"])
    base.draw_page_mark(draw, number, p["ink"])
    return image


def interior_otto(book: dict, assets: Path, number: int) -> Image.Image:
    p = rgb(book)
    title, headline, body, filename, variables = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 108), fill=p["ink"])
    draw.text((64, 32), f"FREI OTTO / FORCE + MATERIAL / 0{number}", font=base.get_font(21, bold=True), fill=p["white"])
    photo = toned(base.crop(base.open_image(assets / filename), (W, 790), (0.50, 0.50)), 0.70, 1.08)
    image.paste(photo, (0, 108))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 818, W, 910), fill=p["ink"])
    draw.text((62, 842), title, font=base.get_font(31, bold=True), fill=p["white"])
    draw.text((1092, 829), f"0{number}", font=base.get_font(48, bold=True, serif=True), fill=p["red"])
    # Diagram remains outside the photo to keep the sourced image legible.
    nodes = [(80, 976), (315, 932), (560, 975), (810, 930), (1140, 980)]
    draw.line(nodes, fill=p["cyan"], width=6, joint="curve")
    for i, (x, y0) in enumerate(nodes):
        radius = 13 if i in (0, 4) else 10
        draw.ellipse((x - radius, y0 - radius, x + radius, y0 + radius), fill=p["red"] if i in (0, 4) else p["yellow"], outline=p["ink"], width=3)
    draw.text((70, 920), variables.upper(), font=base.get_font(18, bold=True), fill=p["gray"])
    y = fit_title(draw, (70, 1030), headline, 1060, 47, p["ink"], spacing=8)
    draw.line((70, y + 24, 520, y + 24), fill=p["red"], width=8)
    base.text_block(draw, (72, y + 62), body, base.get_font(29), p["ink"], 1035, 12)
    draw.text((72, 1560), f"{book['book_cn']} / FINDING, NOT IMPOSING", font=base.get_font(18, bold=True), fill=p["gray"])
    base.draw_page_mark(draw, number, p["ink"])
    return image


def summary_moneo(book: dict) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((66, 64), "类型不是答案，是起点", font=base.get_font(60, bold=True, serif=True), fill=p["ink"])
    base.text_block(draw, (70, 158), book["summary"], base.get_font(29), p["blue"], 1020, 10)
    # Four pressures deform the central type block from different directions.
    center = (418, 500, 824, 975)
    draw.rectangle(center, fill=p["red"], outline=p["ink"], width=5)
    draw.text((505, 650), "TYPE", font=base.get_font(63, bold=True, serif=True), fill=p["paper"])
    draw.text((492, 742), "可讨论的原型", font=base.get_font(28, bold=True), fill=p["paper"])
    pressures = [
        ("地形", (82, 480, 354, 664), p["green"], (354, 575, 418, 575)),
        ("历史", (888, 426, 1160, 610), p["brick"], (824, 520, 888, 520)),
        ("程序", (120, 810, 365, 994), p["blue"], (365, 900, 418, 900)),
        ("建造", (878, 826, 1125, 1010), p["warm"], (824, 920, 878, 920)),
    ]
    for i, (name, box, color, line) in enumerate(pressures, 1):
        draw.rectangle(box, fill=color, outline=p["ink"], width=4)
        fg = p["ink"] if color == p["warm"] else p["paper"]
        draw.text((box[0] + 30, box[1] + 35), f"0{i}", font=base.get_font(19, bold=True), fill=fg)
        draw.text((box[0] + 30, box[1] + 82), name, font=base.get_font(34, bold=True), fill=fg)
        draw.line(line, fill=p["ink"], width=9)
        arrow_x = line[2]
        draw.polygon([(arrow_x, line[3]), (arrow_x - 18 if arrow_x > 600 else arrow_x + 18, line[3] - 13), (arrow_x - 18 if arrow_x > 600 else arrow_x + 18, line[3] + 13)], fill=p["ink"])
    draw.text((70, 1105), "可迁移的三步", font=base.get_font(27, bold=True), fill=p["red"])
    for i, method in enumerate(book["methods"], 1):
        x = 70 + (i - 1) * 380
        draw.rectangle((x, 1170, x + 338, 1490), outline=[p["green"], p["blue"], p["brick"]][i - 1], width=7)
        draw.text((x + 24, 1200), f"METHOD 0{i}", font=base.get_font(19, bold=True), fill=p["red"])
        base.text_block(draw, (x + 24, 1252), method, base.get_font(25, bold=True), p["ink"], 285, 9)
    draw.text((910, 1545), "CONTEXT REWRITES TYPE", font=base.get_font(17, bold=True), fill=p["blue"])
    base.draw_page_mark(draw, 6, p["ink"])
    return image


def summary_otto(book: dict) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((66, 62), "形式，要从力里被找到", font=base.get_font(60, bold=True, serif=True), fill=p["white"])
    base.text_block(draw, (70, 156), book["summary"], base.get_font(29), p["yellow"], 1020, 10)
    # An actual catenary-like network, entirely different from Moneo's plan diagram.
    anchors = [(110, 445), (1132, 445), (110, 1065), (1132, 1065)]
    for x, y in anchors:
        draw.line((x, y, x, y + (72 if y < 700 else -72)), fill=p["red"], width=8)
        draw.ellipse((x - 15, y - 15, x + 15, y + 15), fill=p["red"], outline=p["white"], width=3)
    curves = []
    for offset in (0, 80, 160):
        points = []
        for i in range(101):
            x = 110 + i * 10.22
            y = 445 + offset + 0.0020 * (x - 621) ** 2
            points.append((x, y))
        curves.append(points)
        draw.line(points, fill=p["cyan"] if offset != 80 else p["yellow"], width=5)
    verticals = []
    for i in range(9):
        x = 170 + i * 112
        top = 445 + 0.0020 * (x - 621) ** 2
        bottom = 605 + 0.0020 * (x - 621) ** 2
        draw.line((x, top, x, bottom), fill=p["gray"], width=3)
        verticals.append((x, (top + bottom) / 2))
    chain_nodes = [(190, 625), (405, 725), (620, 770), (835, 725), (1050, 625)]
    for i, ((x, y), name) in enumerate(zip(chain_nodes, book["chain"]), 1):
        draw.ellipse((x - 48, y - 48, x + 48, y + 48), fill=p["paper"], outline=p["red"], width=6)
        draw.text((x - 28, y - 20), name, font=base.get_font(23, bold=True), fill=p["ink"])
        draw.text((x - 13, y + 54), f"0{i}", font=base.get_font(17, bold=True), fill=p["yellow"])
    method_boxes = [(72, 1120, 410, 1485), (452, 1045, 790, 1410), (832, 1120, 1170, 1485)]
    for i, (method, box) in enumerate(zip(book["methods"], method_boxes), 1):
        draw.rectangle(box, outline=[p["cyan"], p["yellow"], p["red"]][i - 1], width=7)
        draw.text((box[0] + 24, box[1] + 24), f"ANCHOR 0{i}", font=base.get_font(19, bold=True), fill=[p["cyan"], p["yellow"], p["red"]][i - 1])
        base.text_block(draw, (box[0] + 24, box[1] + 82), method, base.get_font(25, bold=True), p["white"], box[2] - box[0] - 48, 9)
    draw.text((862, 1540), "LOAD → MODEL → DETAIL", font=base.get_font(18, bold=True), fill=p["gray"])
    base.draw_page_mark(draw, 6, p["ink"], light=True)
    return image


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0)


def make_preview(paths: list[Path], output: Path) -> None:
    tw, th, gap = 360, 481, 24
    sheet = Image.new("RGB", (tw * 3 + gap * 4, th * 2 + gap * 3), (218, 216, 208))
    for i, path in enumerate(paths):
        with Image.open(path) as source:
            thumb = source.convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 3) * (tw + gap), gap + (i // 3) * (th + gap)))
    save(sheet.resize((1242, 1108), Image.Resampling.LANCZOS), output)


def write_docs(book: dict, assets: Path, output: Path) -> None:
    manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    source_lines = [
        "# 图片来源", "",
        "| 文件名 | 内容 | 作者 / 机构 | 来源 URL | 许可 / 版权 | 修改 |",
        "|---|---|---|---|---|---|",
    ]
    for item in manifest:
        source_lines.append(f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item['modifications']} |")
    source_lines += [
        "",
        "书封仅用于书籍识别、介绍与评论；封面文字和构图保持原样，未重绘。",
        "案例照片按来源许可进行裁切、缩放和轻微调色；图卡文字为编辑性概括，不作为原书直接引语。",
    ]
    (output / "图片来源.md").write_text("\n".join(source_lines) + "\n", encoding="utf-8")
    publication = book["publish_title"] + "\n\n" + "\n\n".join(book["publish_paragraphs"]) + "\n\n" + book["tags"] + "\n"
    (output / "发布文案.md").write_text(publication, encoding="utf-8")
    post = {
        "designer": book["designer"],
        "book": book["book"],
        "edition": book["edition"],
        "thesis": book["thesis"],
        "publish_title": book["publish_title"],
        "title_length": len(book["publish_title"]),
        "concept_chain": book["chain"],
        "cards": [
            {"number": "01", "role": "problem cover", "headline": book["question"], "asset": "cover.jpg"},
            *[{"number": f"{i:02d}", "role": "mechanism" if i == 2 else "evidence", "headline": card[1], "evidence": card[0], "asset": card[3]} for i, card in enumerate(book["cards"], start=2)],
            {"number": "06", "role": "synthesis", "headline": book["summary"], "asset": ""},
        ],
        "endcards": book["endcards"],
        "transferable_methods": book["methods"],
        "sources": manifest,
    }
    (output / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    previews: list[tuple[str, Path, tuple[int, int, int]]] = []
    for slug, book in BOOKS.items():
        if len(book["publish_title"]) > 20:
            raise ValueError(f"Title exceeds 20 characters: {book['publish_title']}")
        assets = ASSET_ROOT / slug
        output = OUTPUT_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        if not (assets / "manifest.json").exists():
            raise FileNotFoundError(f"Missing assets: {assets}")
        if book["system"] == "context-fold":
            cards = [cover_moneo(book, assets)] + [interior_moneo(book, assets, n) for n in range(2, 6)] + [summary_moneo(book)]
            title_color = rgb(book)["red"]
        else:
            cards = [cover_otto(book, assets)] + [interior_otto(book, assets, n) for n in range(2, 6)] + [summary_otto(book)]
            title_color = rgb(book)["cyan"]
        paths: list[Path] = []
        for number, card in enumerate(cards, 1):
            path = output / f"{number:02d}.jpg"
            save(card, path)
            paths.append(path)
        make_preview(paths, output / "preview.jpg")
        write_docs(book, assets, output)
        previews.append((f"{book['designer']} / {book['book']}", output / "preview.jpg", title_color))
        print(f"Rendered {slug}; title length={len(book['publish_title'])}")

    total = Image.new("RGB", (1242, 2580), (236, 233, 224))
    draw = ImageDraw.Draw(total)
    draw.rectangle((0, 0, 1242, 150), fill=(18, 40, 58))
    draw.text((58, 42), "两本新书 / 建筑判断的方法", font=base.get_font(44, bold=True, serif=True), fill=(247, 245, 238))
    y = 190
    for title, path, color in previews:
        draw.rectangle((58, y + 4, 76, y + 40), fill=color)
        draw.text((94, y), title, font=base.get_font(29, bold=True), fill=(18, 40, 58))
        with Image.open(path) as source:
            strip = source.convert("RGB").resize((1126, 1005), Image.Resampling.LANCZOS)
        total.paste(strip, (58, y + 58))
        y += 1160
    save(total, OUTPUT_ROOT / "总预览.jpg")


if __name__ == "__main__":
    main()
