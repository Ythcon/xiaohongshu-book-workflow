#!/usr/bin/env python3
"""Render two Casabella-inspired six-card posts for Paul Rudolph and James Stirling."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "two-new-books-02"
OUTPUT_ROOT = ROOT / "output" / "two-new-books-02"
W, H = 1242, 1660


BOOKS = {
    "paul-rudolph-writings-on-architecture": {
        "designer": "保罗·鲁道夫",
        "designer_en": "PAUL RUDOLPH",
        "book": "Writings on Architecture",
        "book_cn": "《建筑论述》",
        "edition": "Yale School of Architecture, 2008｜ISBN 9780300150926",
        "question": "复杂空间，为什么不能只靠平面解释？",
        "thesis": "鲁道夫把剖面、路径、结构与连续视点视为同一套空间系统：复杂不是元素更多，而是关系仍然可读。",
        "system": "sectional-depth",
        "palette": {"paper": "#F1EEE6", "ink": "#142434", "accent": "#E54D36", "second": "#657B83", "warm": "#E1BB56", "dark": "#242A2E"},
        "cards": [
            ("鲁道夫楼", "空间从剖面开始，而不是从房间列表开始", "工作室、评图空间、楼梯与平台被安排在连续变化的标高上。人在移动中不断获得新的俯视、仰视与对望关系，剖面因此成为组织教学活动和空间认知的核心工具。", "02-rudolph-hall.jpg"),
            ("米拉姆住宅", "立面不是表皮，而是气候与视线的深度装置", "面向海岸的混凝土框架形成深窗、遮阳与可停留的边界。开口大小并非图案，而是在日照、景观、私密与室内尺度之间建立层次。", "03-milam-house.jpg"),
            ("波士顿政府服务中心", "公共尺度，要靠路径与平台被身体理解", "巨大的公共机构没有被压成单一体量。坡道、庭院、露台与架空空间把庞大尺度拆成一段段可进入的城市动作，让公共性通过移动发生。", "04-boston-gsc.jpg"),
            ("马萨诸塞大学达特茅斯校区", "复杂总体需要一个能反复辨认的组织骨架", "校园以集中核心、放射路径与重复构件建立方向感。单体可以变化，但人在每一次转折中都能重新找到中心、路径和下一个目的地。", "05-umass-dartmouth.jpg"),
        ],
        "summary": "复杂不是把形式叠得更满，而是让剖面、路径、结构与视线在移动中仍能被同时阅读。",
        "chain": ["平面", "剖面", "路径", "视线", "整体"],
        "methods": ["先用剖面标出不同活动的高度关系", "把楼梯、平台和走廊当作空间主体", "用连续视点检查复杂是否仍可辨认"],
        "endcards": {
            "01": {"layout_rationale": "深色整页与竖向项目切片形成剖面背景，真实书封占据左侧约三分之一并成为最亮视觉块，问题标题沿右上展开。", "changed_variables": ["左侧大书封", "右侧剖面照片带", "阶梯式标题", "深色整页"]},
            "06": {"layout_rationale": "概念链沿一条垂直剖面路径逐层上升，三条方法分别落在不同平台，模拟身体穿过复杂空间的阅读过程。", "changed_variables": ["垂直剖面", "折线路径", "平台式方法注释", "中心空腔"]},
        },
        "publish_title": "鲁道夫：复杂空间，为什么不能只靠平面解释？",
        "publish_body": "《Writings on Architecture》把保罗·鲁道夫的文章、演讲与访谈放在一起，最值得设计师带走的并不是粗野主义的表面语言，而是一套阅读复杂空间的方法。鲁道夫楼用连续标高组织工作室、评图空间与交通，让人在移动中获得俯视、仰视和对望；米拉姆住宅把深立面变成遮阳、景观和私密之间的过滤器；波士顿政府服务中心用坡道、庭院与平台把庞大机构转化为可步行的公共动作；马萨诸塞大学达特茅斯校区则以中心、放射路径和重复构件维持总体方向感。复杂并不等于元素更多，而是剖面、路径、结构与视线仍能被同时辨认。可直接用于方案的三步：先用剖面标出活动高度，再把楼梯与平台当作空间主体，最后用连续视点检查每一次转折是否仍能读懂整体。本文为基于书籍与案例的编辑性概括，不是原书直接引语。",
        "tags": "#保罗鲁道夫 #WritingsOnArchitecture #建筑理论 #剖面设计 #空间组织 #建筑书单 #设计方法 #建筑案例",
    },
    "james-stirling-early-unpublished-writings": {
        "designer": "詹姆斯·斯特林",
        "designer_en": "JAMES STIRLING",
        "book": "Early Unpublished Writings on Architecture",
        "book_cn": "《早期未刊建筑论述》",
        "edition": "Routledge, 2010｜ISBN 9780415550598",
        "question": "建筑师如何从现代主义内部制造冲突？",
        "thesis": "斯特林的早期笔记不是寻找统一风格，而是把类型、程序、构造与历史引用拆开比较，再把矛盾重新组织成可辨认的建筑。",
        "system": "type-collision",
        "palette": {"paper": "#F3EFE5", "ink": "#172326", "accent": "#D84532", "second": "#28605A", "warm": "#E3B74A", "blue": "#366B93"},
        "cards": [
            ("兰厄姆住宅区", "普通住宅，也能从材料与构造中获得性格", "砖、混凝土梁和白色窗框没有被藏进抽象外皮。构造关系直接参与立面节奏，让集合住宅同时保有重复秩序与单元差异。", "02-langham.jpg"),
            ("莱斯特大学工程楼", "程序差异直接变成轮廓，而不是被统一外皮抹平", "塔楼、车间、玻璃幕墙与折板屋顶各自表达不同功能和构造。建筑的强烈形象来自并置，而不是先设定一个完整外形再把房间塞进去。", "03-leicester.jpg"),
            ("剑桥大学历史系楼", "结构、采光与阅读秩序，共同生成新的类型", "阅览空间围绕共享核心展开，玻璃、红砖与屋面结构把安静阅读和公共活动同时显露出来。类型在使用和建造逻辑中被重新解释。", "04-cambridge-history.jpg"),
            ("牛津大学弗洛里楼", "现代主义不断与场所记忆和集体生活协商", "弧形住宿体量围合却不封闭庭院，既回应学院传统，又把视线、交通与河岸方向引入日常生活。引用旧类型，不等于复制旧形式。", "05-florey.jpg"),
        ],
        "summary": "真正可迁移的不是红砖与玻璃，而是先辨认类型，再让程序、构造与公共路径彼此校正。",
        "chain": ["观察", "引用", "拆分", "碰撞", "再组织"],
        "methods": ["先记录已有类型和构造，不急于擦除", "把不同程序拆成可辨认的体块", "用共享路径把冲突片段重新串起来"],
        "endcards": {
            "01": {"layout_rationale": "暖白底上把项目照片切成斜向类型碎片，真实书封扩大后固定在右侧，标题占据左侧留白并以红色路径穿过版面。", "changed_variables": ["右侧大书封", "斜向照片碎片", "左侧留白标题", "红色路线"]},
            "06": {"layout_rationale": "黑色笔记本底上用五个不规则类型块围绕公共路径碰撞，方法写在三处转角，形成与封面完全不同的平面式总结。", "changed_variables": ["黑色笔记页", "不规则类型块", "环形公共路径", "转角方法批注"]},
        },
        "publish_title": "斯特林：建筑师如何从现代主义内部制造冲突？",
        "publish_body": "《James Stirling: Early Unpublished Writings on Architecture》收录黑色笔记本、讲稿、访谈和他对勒·柯布西耶影响的反思。它呈现的不是一套成熟风格，而是斯特林如何把现代主义内部的矛盾转化为设计工具。兰厄姆住宅区让砖、混凝土梁和窗框直接参与立面秩序；莱斯特大学工程楼把塔楼、车间、玻璃与折板屋顶按程序并置；剑桥历史系楼用结构、采光和阅读秩序重写图书馆类型；弗洛里楼则让学院庭院的记忆与开放河岸发生冲突。真正可迁移的不是红砖、玻璃或某种造型，而是先辨认已有类型和构造，再把不同程序拆成可读的片段，最后用共享路径把矛盾重新串成整体。引用历史不等于复制形式，冲突也不是混乱，它可以成为组织新关系的起点。本文为基于书籍与案例的编辑性概括，不是原书直接引语。",
        "tags": "#詹姆斯斯特林 #建筑理论 #现代主义 #建筑类型学 #建筑书单 #设计方法 #建筑案例 #建筑阅读",
    },
}


def rgb(book: dict) -> dict[str, tuple[int, int, int]]:
    return {key: tuple(int(value[i:i + 2], 16) for i in (1, 3, 5)) for key, value in book["palette"].items()}


def toned(image: Image.Image, saturation: float = 0.82, contrast: float = 1.04) -> Image.Image:
    image = ImageEnhance.Color(image.convert("RGB")).enhance(saturation)
    return ImageEnhance.Contrast(image).enhance(contrast)


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, bg, fg, width: int) -> None:
    x, y = xy
    draw.rectangle((x, y, x + width, y + 48), fill=bg)
    draw.text((x + 16, y + 10), text, font=base.get_font(18, bold=True), fill=fg)


def fit_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, max_width: int, start_size: int, fill, serif: bool = True, spacing: int = 8) -> int:
    size = start_size
    while size >= 26:
        font = base.get_font(size, bold=True, serif=serif)
        lines = base.wrap(draw, text, font, max_width)
        bbox = draw.multiline_textbbox(xy, "\n".join(lines), font=font, spacing=spacing)
        if bbox[2] - bbox[0] <= max_width:
            draw.multiline_text(xy, "\n".join(lines), font=font, fill=fill, spacing=spacing)
            return bbox[3]
        size -= 2
    return base.text_block(draw, xy, text, base.get_font(26, bold=True, serif=serif), fill, max_width, spacing)


def cover_rudolph(book: dict, assets: Path) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["ink"])
    photo = toned(base.crop(base.open_image(assets / "02-rudolph-hall.jpg"), (560, H), (0.57, 0.50)), 0.45, 1.08)
    image.paste(photo, (682, 0))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((682, 0, W, H), fill=(*p["ink"], 62))
    for y, run in [(170, 410), (430, 505), (720, 380), (1020, 480), (1320, 365)]:
        od.line((650, y, 650 + run, y), fill=(*p["warm"], 225), width=5)
        od.line((650 + run, y, 650 + run, y + 120), fill=(*p["warm"], 225), width=5)
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.text((70, 50), "PAUL RUDOLPH / WRITINGS / 01", font=base.get_font(22, bold=True), fill=p["warm"])
    draw.line((70, 103, 620, 103), fill=p["accent"], width=8)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (72, 205, 626, 1025), shadow=True)
    draw = ImageDraw.Draw(image)
    label(draw, (367, 1035), "VERIFIED BOOK COVER", p["accent"], p["paper"], 290)
    draw.rectangle((620, 176, 1170, 616), fill=(*p["ink"],))
    fit_text(draw, (660, 220), "复杂空间，\n为什么不能\n只靠平面解释？", 470, 61, p["paper"], spacing=10)
    draw.text((70, 1110), book["book_cn"], font=base.get_font(34, bold=True), fill=p["paper"])
    draw.text((70, 1165), book["designer"], font=base.get_font(24, bold=True), fill=p["second"])
    base.text_block(draw, (70, 1250), book["thesis"], base.get_font(29), p["paper"], 540, 11)
    draw.text((900, 1512), "SECTION / ROUTE / VIEW", font=base.get_font(18, bold=True), fill=p["warm"])
    base.draw_page_mark(draw, 1, p["ink"], light=True)
    return image


def cover_stirling(book: dict, assets: Path) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((64, 48), "EARLY NOTES / TYPE / CONSTRUCTION", font=base.get_font(21, bold=True), fill=p["second"])
    draw.line((64, 102, 1178, 102), fill=p["ink"], width=3)
    fit_text(draw, (68, 170), "建筑师如何从\n现代主义内部\n制造冲突？", 565, 62, p["ink"], spacing=10)
    draw.rectangle((66, 570, 530, 640), fill=p["accent"])
    draw.text((88, 590), "TYPE ≠ STYLE", font=base.get_font(26, bold=True), fill=p["paper"])
    photo = toned(base.crop(base.open_image(assets / "03-leicester.jpg"), (660, 660), (0.50, 0.48)), 0.68, 1.08)
    mask = Image.new("L", (660, 660), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(0, 120), (660, 0), (660, 530), (0, 660)], fill=255)
    image.paste(photo, (0, 930), mask)
    draw = ImageDraw.Draw(image)
    draw.line((0, 970, 648, 850), fill=p["accent"], width=16)
    draw.line((540, 640, 690, 915), fill=p["accent"], width=16)
    cover = base.open_image(assets / "cover.jpg").filter(ImageFilter.UnsharpMask(radius=1.2, percent=105, threshold=3))
    base.paste_cover(image, cover, (650, 205, 1176, 995), shadow=True)
    draw = ImageDraw.Draw(image)
    label(draw, (738, 1005), "OFFICIAL ROUTLEDGE COVER", p["second"], p["paper"], 355)
    base.text_block(draw, (694, 1080), book["thesis"], base.get_font(28), p["ink"], 455, 10)
    draw.text((694, 1452), book["book_cn"], font=base.get_font(31, bold=True), fill=p["accent"])
    draw.text((694, 1502), book["designer"], font=base.get_font(23, bold=True), fill=p["second"])
    base.draw_page_mark(draw, 1, p["ink"])
    return image


def interior_rudolph(book: dict, assets: Path, number: int) -> Image.Image:
    p = rgb(book)
    title, headline, body, filename = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 112), fill=p["ink"])
    draw.text((66, 34), f"PAUL RUDOLPH / SECTIONAL DEPTH / 0{number}", font=base.get_font(22, bold=True), fill=p["paper"])
    source = base.open_image(assets / filename)
    photo = toned(base.crop(source, (W, 850), (0.50, 0.50)), 0.72, 1.06)
    image.paste(photo, (0, 112))
    draw = ImageDraw.Draw(image)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i, y in enumerate((250, 390, 545, 700, 842)):
        x0 = 45 + (i % 2) * 130
        x1 = 1165 - (i % 3) * 95
        od.line((x0, y, x1, y), fill=(*p["warm"], 225), width=5)
        if i < 4:
            od.line((x1, y, x1, y + 130), fill=(*p["warm"], 225), width=5)
    od.rectangle((0, 840, W, 962), fill=(*p["ink"], 225))
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.text((68, 865), title, font=base.get_font(34, bold=True), fill=p["paper"])
    draw.text((1070, 856), f"0{number}", font=base.get_font(48, bold=True, serif=True), fill=p["accent"])
    y = fit_text(draw, (70, 1025), headline, 1070, 48, p["ink"], spacing=8)
    draw.line((70, y + 25, 440, y + 25), fill=p["accent"], width=9)
    base.text_block(draw, (72, y + 65), body, base.get_font(29), p["dark"], 1030, 12)
    draw.text((72, 1564), f"{book['book_cn']} / EDITORIAL READING", font=base.get_font(18, bold=True), fill=p["second"])
    base.draw_page_mark(draw, number, p["ink"])
    return image


def interior_stirling(book: dict, assets: Path, number: int) -> Image.Image:
    p = rgb(book)
    title, headline, body, filename = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 106), fill=p["ink"])
    draw.text((64, 32), f"JAMES STIRLING / BLACK NOTEBOOK / 0{number}", font=base.get_font(21, bold=True), fill=p["paper"])
    photo_w = 930
    x = 250 if number % 2 == 0 else 0
    photo = toned(base.crop(base.open_image(assets / filename), (photo_w, 835), (0.50, 0.50)), 0.83, 1.06)
    image.paste(photo, (x, 106))
    draw = ImageDraw.Draw(image)
    margin_x = 0 if number % 2 == 0 else 930
    draw.rectangle((margin_x, 106, margin_x + 312, 941), fill=p["second"])
    draw.text((margin_x + 48, 160), f"0{number}", font=base.get_font(74, bold=True, serif=True), fill=p["warm"])
    notes = ["TYPE", "PROGRAM", "MATERIAL", "ROUTE"]
    for i, note in enumerate(notes):
        yy = 360 + i * 112
        draw.text((margin_x + 48, yy), note, font=base.get_font(20, bold=True), fill=p["paper"])
        draw.line((margin_x + 48, yy + 38, margin_x + 250, yy + 38), fill=p["accent"], width=5)
    draw.rectangle((58, 860, 805, 946), fill=p["ink"])
    draw.text((82, 884), title, font=base.get_font(32, bold=True), fill=p["paper"])
    y = fit_text(draw, (68, 1015), headline, 1080, 47, p["ink"], spacing=8)
    draw.line((68, y + 24, 535, y + 24), fill=p["accent"], width=8)
    base.text_block(draw, (70, y + 62), body, base.get_font(29), p["ink"], 1040, 12)
    draw.text((70, 1562), f"{book['book_cn']} / TYPE AS EVIDENCE", font=base.get_font(18, bold=True), fill=p["second"])
    base.draw_page_mark(draw, number, p["ink"])
    return image


def summary_rudolph(book: dict) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((68, 64), "复杂，必须仍然可读", font=base.get_font(60, bold=True, serif=True), fill=p["paper"])
    base.text_block(draw, (72, 154), book["summary"], base.get_font(29), p["warm"], 990, 10)
    # A vertical sectional void with platforms at changing depths.
    draw.rectangle((460, 355, 820, 1495), outline=p["second"], width=5)
    platforms = [(120, 430, 700), (520, 610, 1110), (175, 805, 760), (540, 1000, 1160), (260, 1200, 890)]
    points = []
    for i, ((x0, y, x1), chain) in enumerate(zip(platforms, book["chain"]), 1):
        draw.line((x0, y, x1, y), fill=p["paper"], width=18)
        draw.line((x0, y + 19, x1, y + 19), fill=p["accent"], width=6)
        node_x = 520 if i % 2 else 760
        points.append((node_x, y - 8))
        draw.ellipse((node_x - 25, y - 33, node_x + 25, y + 17), fill=p["warm"], outline=p["paper"], width=4)
        text_x = x0 + 20 if i % 2 else x1 - 155
        draw.text((text_x, y - 68), f"0{i}  {chain}", font=base.get_font(26, bold=True), fill=p["paper"])
    draw.line(points, fill=p["warm"], width=7, joint="curve")
    method_positions = [(78, 525, 345), (835, 830, 330), (86, 1320, 360)]
    for i, (method, (x, y, mw)) in enumerate(zip(book["methods"], method_positions), 1):
        draw.text((x, y), f"METHOD 0{i}", font=base.get_font(18, bold=True), fill=p["accent"])
        base.text_block(draw, (x, y + 34), method, base.get_font(24, bold=True), p["paper"], mw, 8)
    draw.text((905, 1538), "SECTION → ROUTE → VIEW", font=base.get_font(17, bold=True), fill=p["second"])
    base.draw_page_mark(draw, 6, p["ink"], light=True)
    return image


def summary_stirling(book: dict) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((54, 58, 1188, 1602), outline=p["paper"], width=4)
    draw.text((82, 90), "类型不是答案，是可以重新组合的证据", font=base.get_font(51, bold=True, serif=True), fill=p["paper"])
    base.text_block(draw, (84, 180), book["summary"], base.get_font(28), p["warm"], 1010, 10)
    centers = [(250, 525), (515, 440), (785, 555), (930, 850), (590, 980)]
    colors = [p["accent"], p["second"], p["blue"], p["warm"], p["paper"]]
    sizes = [(250, 180), (265, 155), (255, 190), (280, 175), (310, 195)]
    polygons = []
    for i, ((cx, cy), (sw, sh), color, chain) in enumerate(zip(centers, sizes, colors, book["chain"]), 1):
        pts = [(cx - sw // 2, cy - sh // 3), (cx + sw // 3, cy - sh // 2), (cx + sw // 2, cy + sh // 4), (cx, cy + sh // 2), (cx - sw // 2, cy + sh // 3)]
        polygons.append(pts)
        draw.polygon(pts, fill=color, outline=p["paper"] if color != p["paper"] else p["accent"])
        fg = p["ink"] if color in (p["warm"], p["paper"]) else p["paper"]
        draw.text((cx - sw // 2 + 24, cy - 20), f"0{i} / {chain}", font=base.get_font(25, bold=True), fill=fg)
    route = [(170, 650), (390, 665), (610, 700), (840, 690), (1030, 800), (880, 1025), (620, 1115), (330, 1070), (170, 900), (170, 650)]
    draw.line(route, fill=p["accent"], width=18, joint="curve")
    for x, y in route[:-1]:
        draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill=p["paper"])
    method_boxes = [(88, 1240, 415, 1515), (456, 1180, 786, 1455), (825, 1250, 1152, 1525)]
    for i, (method, box) in enumerate(zip(book["methods"], method_boxes), 1):
        draw.rectangle(box, outline=colors[i - 1], width=7)
        draw.text((box[0] + 22, box[1] + 20), f"NOTE 0{i}", font=base.get_font(20, bold=True), fill=colors[i - 1])
        base.text_block(draw, (box[0] + 22, box[1] + 68), method, base.get_font(23, bold=True), p["paper"], box[2] - box[0] - 44, 8)
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
        "| 文件名 | 内容 | 作者/机构 | 来源 URL | 许可/版权 | 修改 |",
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
    publish = f"""# 标题

{book['publish_title']}

# 正文

{book['publish_body']}

# 标签

{book['tags']}

# 版本

{book['book']}｜{book['edition']}
"""
    (output / "发布文案.md").write_text(publish, encoding="utf-8")
    post = {
        "designer": book["designer"],
        "book": book["book"],
        "edition": book["edition"],
        "thesis": book["thesis"],
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
    previews: list[tuple[str, Path]] = []
    for slug, book in BOOKS.items():
        assets = ASSET_ROOT / slug
        output = OUTPUT_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        if not (assets / "manifest.json").exists():
            raise FileNotFoundError(f"Missing assets: {assets}")
        if book["system"] == "sectional-depth":
            cards = [cover_rudolph(book, assets)] + [interior_rudolph(book, assets, n) for n in range(2, 6)] + [summary_rudolph(book)]
        else:
            cards = [cover_stirling(book, assets)] + [interior_stirling(book, assets, n) for n in range(2, 6)] + [summary_stirling(book)]
        paths: list[Path] = []
        for number, card in enumerate(cards, 1):
            path = output / f"{number:02d}.jpg"
            save(card, path)
            paths.append(path)
        make_preview(paths, output / "preview.jpg")
        write_docs(book, assets, output)
        previews.append((book["book_cn"], output / "preview.jpg"))
        print(f"Rendered {slug}")

    total_h = 2650
    total = Image.new("RGB", (1242, total_h), (234, 231, 222))
    draw = ImageDraw.Draw(total)
    draw.rectangle((0, 0, 1242, 150), fill=(20, 36, 52))
    draw.text((58, 45), "两本新书 / 建筑大师方法论", font=base.get_font(44, bold=True, serif=True), fill=(245, 241, 232))
    y = 190
    for title, path in previews:
        draw.text((58, y), title, font=base.get_font(30, bold=True), fill=(20, 36, 52))
        with Image.open(path) as source:
            strip = source.convert("RGB").resize((1126, 1005), Image.Resampling.LANCZOS)
        total.paste(strip, (58, y + 55))
        y += 1160
    save(total, OUTPUT_ROOT / "总预览.jpg")


if __name__ == "__main__":
    main()
