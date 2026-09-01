#!/usr/bin/env python3
"""Render a ten-card Xiaohongshu post for Louis Sullivan's Kindergarten Chats."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "louis-sullivan-kindergarten-chats"
OUTPUT = ROOT / "output" / "louis-sullivan-kindergarten-chats"
W, H = 1242, 1660

P = {
    "paper": (239, 228, 209),
    "ink": (30, 27, 25),
    "brick": (154, 59, 43),
    "clay": (197, 112, 80),
    "green": (48, 91, 81),
    "gold": (204, 154, 78),
    "white": (248, 243, 232),
    "muted": (112, 100, 88),
}

BOOK = {
    "designer": "路易斯·沙利文",
    "designer_en": "LOUIS H. SULLIVAN",
    "book": "Kindergarten Chats and Other Writings",
    "edition": "Dover Publications, 1979｜ISBN 9780486238128",
    "question": "形式追随功能，\n为什么装饰仍然重要？",
    "thesis": "功能不是造型的终点；它先建立秩序，装饰再让结构、尺度和入口获得可感知的生命。",
    "publish_title": "沙利文：装饰为何没有消失？",
    "publish_body": (
        "《Kindergarten Chats and Other Writings》最适合用来纠正一个误读：沙利文所说的“形式追随功能”，并不等于取消装饰。功能先规定建筑怎样站立、分层与被使用，装饰则让这种秩序能够被身体和城市感知。\n\n"
        "芝加哥礼堂大厦把剧院、酒店和办公压进同一体量；温莱特大厦以基座、连续竖向层和顶部收束表达高层办公；担保大厦让陶土纹样服从钢框架网格；贝亚德—康迪克特大厦把狭窄基地转化为清晰的垂直节奏。\n\n"
        "沙利文中心把大橱窗留给商业，并把浓密铸铁装饰集中在街角入口；奥瓦通纳国家农民银行用厚砖墙、彩窗和图案同时传达安全与公共性；格林内尔商人国家银行把装饰压缩到圆窗与门廊；克劳斯音乐商店则让一面小立面拥有完整身份。\n\n"
        "对设计师更实用的顺序是：先写清空间真正承担的动作，再让结构和开口形成可读节奏，最后只在入口、转角和收口处加深装饰。装饰不是覆盖秩序，而是让秩序被看见。\n\n"
        "本文为基于书籍与案例资料的编辑性阅读，不是原书逐字引语。"
    ),
    "tags": "#路易斯沙利文 #KindergartenChats #形式追随功能 #建筑装饰 #芝加哥学派 #建筑理论 #建筑书单 #设计方法",
}

CASES = [
    {"year": "1889", "title": "芝加哥礼堂大厦", "meta": "芝加哥｜Adler & Sullivan", "headline": "复杂功能，先被压成清晰层级", "body": "剧院、酒店与办公室共处一座大体量。外墙从厚重基座向重复开窗与顶部收束递进，让不同程序在城市立面上仍有整体秩序。", "asset": "02-auditorium.jpg", "focus": (0.50, 0.48)},
    {"year": "1891", "title": "温莱特大厦", "meta": "圣路易斯｜Adler & Sullivan", "headline": "高层建筑，应先承认自己的高度", "body": "基座对应街道商业，中段以连续竖向构件强调办公层重复，顶部负责收束。所谓功能，不只是房间用途，也是建筑作为高层的整体性格。", "asset": "03-wainwright.jpg", "focus": (0.49, 0.48)},
    {"year": "1896", "title": "担保大厦", "meta": "布法罗｜Adler & Sullivan", "headline": "装饰没有遮住网格，而是沿网格生长", "body": "钢框架建立窗与层的重复节奏，陶土纹样被嵌进窗间、边框与收口。细部变化很多，但始终服从立面的结构分格。", "asset": "04-guaranty.jpg", "focus": (0.50, 0.50)},
    {"year": "1899", "title": "贝亚德—康迪克特大厦", "meta": "纽约｜Bayard–Condict Building", "headline": "狭窄基地，也能把垂直节奏说清", "body": "纤细竖向构件跨越楼层，窗间墙后退，顶部拱窗结束上升。立面没有模仿历史宫殿，而是把高度与采光直接变成构图。", "asset": "05-bayard-condict.jpg", "focus": (0.53, 0.47)},
    {"year": "1904", "title": "沙利文中心", "meta": "芝加哥｜原卡森百货", "headline": "商业需要通透，入口需要被记住", "body": "宽大的展示窗服务零售，密集铸铁植物纹样则集中在街角与首层。装饰强化进入和转向，而没有平均铺满整座建筑。", "asset": "06-sullivan-center.jpg", "focus": (0.50, 0.58)},
    {"year": "1908", "title": "国家农民银行", "meta": "奥瓦通纳｜National Farmers’ Bank", "headline": "安全感与公共性，可以同时出现", "body": "厚重砖墙提供稳定，拱窗、彩色玻璃与金属细部把光和图案引入公共大厅。银行不只像保险箱，也成为小城的公共室内。", "asset": "07-owatonna.jpg", "focus": (0.50, 0.54)},
    {"year": "1914", "title": "商人国家银行", "meta": "格林内尔｜Merchants’ National Bank", "headline": "大面积克制，反而让入口更有力量", "body": "近乎完整的砖墙托住巨大的圆窗与装饰门廊。图案被压缩在最重要的接触点，证明丰富不等于到处填满。", "asset": "08-grinnell.jpg", "focus": (0.50, 0.53)},
    {"year": "1922", "title": "克劳斯音乐商店", "meta": "芝加哥｜Sullivan 与 William Presto", "headline": "一面小立面，也需要完整身份", "body": "商店与住宅的尺度很小，装饰却沿中央轴、窗框和檐口生长。有限预算没有取消表达，而是迫使表达更集中。", "asset": "09-krause.jpg", "focus": (0.50, 0.56)},
]


def leaf(draw: ImageDraw.ImageDraw, center: tuple[int, int], scale: float, color, width=4) -> None:
    """Draw a Sullivan-inspired abstract leaf with no copied historic ornament."""
    cx, cy = center
    pts = []
    for i in range(30):
        t = i / 29 * math.pi
        x = cx + math.cos(t) * 62 * scale
        y = cy + math.sin(t) * 26 * scale
        pts.append((x, y))
    for i in range(29, -1, -1):
        t = i / 29 * math.pi
        x = cx + math.cos(t) * 62 * scale
        y = cy - math.sin(t) * 26 * scale
        pts.append((x, y))
    draw.line(pts + [pts[0]], fill=color, width=width, joint="curve")
    draw.line((cx - 58 * scale, cy, cx + 58 * scale, cy), fill=color, width=max(2, width // 2))


def cover_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)

    # Vertical growth, unlike the diagonal Pei cover: a structural stem becomes ornament.
    draw.rectangle((0, 0, 236, H), fill=P["brick"])
    draw.rectangle((236, 0, 268, H), fill=P["ink"])
    for y in range(120, 1580, 150):
        leaf(draw, (118, y), 0.72, P["paper"], 4)
    draw.line((118, 65, 118, 1595), fill=P["gold"], width=7)

    draw.text((315, 70), "ARCHITECTURE / ORGANISM", font=base.get_font(21, bold=True), fill=P["green"])
    base.text_block(draw, (315, 116), "LOUIS H.\nSULLIVAN", base.get_font(32, bold=True), P["ink"], 275, 2)

    cover = Image.open(ASSETS / "cover.jpg").convert("RGB")
    base.paste_cover(image, cover, (620, 92, 1165, 865), shadow=True)

    draw.rounded_rectangle((300, 610, 820, 1360), radius=8, fill=P["ink"])
    draw.text((334, 652), "FORM / FUNCTION / LIFE", font=base.get_font(23, bold=True), fill=P["gold"])
    y = base.text_block(draw, (330, 726), BOOK["question"], base.get_font(65, bold=True), P["white"], 450, 5)
    base.text_block(draw, (334, y + 34), BOOK["thesis"], base.get_font(29), P["white"], 430, 12)

    draw.text((855, 1130), "Kindergarten Chats", font=base.get_font(34, bold=True, serif=True), fill=P["brick"])
    draw.text((855, 1180), "and Other Writings", font=base.get_font(26, serif=True), fill=P["ink"])
    base.text_block(draw, (855, 1270), "Dover 1979\n真实书封，等比呈现", base.get_font(23), P["muted"], 300, 9)
    base.draw_page_mark(draw, 1, P["ink"])
    return image


def photo_panel(source: Image.Image, size: tuple[int, int], focus: tuple[float, float]) -> Image.Image:
    source = ImageEnhance.Contrast(source.convert("RGB")).enhance(1.035)
    source = ImageEnhance.Color(source).enhance(0.93)
    return ImageOps.fit(source, size, Image.Resampling.LANCZOS, centering=focus)


def case_card(case: dict, page: int) -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    photo_top = page % 2 == 0
    photo_h = 900
    photo_y = 0 if photo_top else H - photo_h
    text_y = 965 if photo_top else 92

    source = Image.open(ASSETS / case["asset"]).convert("RGB")
    panel = photo_panel(source, (W, photo_h), case["focus"])
    image.paste(panel, (0, photo_y))

    border_y = photo_h if photo_top else photo_y
    draw.rectangle((0, border_y - 10, W, border_y + 10), fill=P["brick"])
    draw.rectangle((0, border_y + (10 if photo_top else -24), W, border_y + (18 if photo_top else -16)), fill=P["gold"])

    draw.text((74, text_y), case["year"], font=base.get_font(31, bold=True), fill=P["brick"])
    draw.text((218, text_y + 4), case["meta"], font=base.get_font(23), fill=P["muted"])
    draw.text((74, text_y + 66), case["title"], font=base.get_font(39, bold=True), fill=P["green"])
    y = base.text_block(draw, (74, text_y + 142), case["headline"], base.get_font(55, bold=True), P["ink"], 1010, 5)
    base.text_block(draw, (78, y + 28), case["body"], base.get_font(31), P["ink"], 1025, 13)

    # One restrained organic marker in the text area; never over the photo.
    leaf(draw, (1110, text_y + 400), 0.55, P["clay"], 3)
    draw.line((1110, text_y + 250, 1110, text_y + 550), fill=P["gold"], width=3)
    base.draw_page_mark(draw, page, P["ink"], light=not photo_top)
    return image


def summary_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["ink"])
    draw = ImageDraw.Draw(image)

    draw.text((70, 66), "FORM FOLLOWS LIFE", font=base.get_font(25, bold=True), fill=P["gold"])
    y = base.text_block(draw, (70, 126), "装饰不是覆盖秩序，\n而是让秩序被看见", base.get_font(62, bold=True), P["white"], 910, 4)
    base.text_block(draw, (74, y + 22), "从需要到结构，再从节奏抵达身份。", base.get_font(29), P["clay"], 800, 10)

    # A vertical organism section: roots, trunk and crown instead of a radial compass.
    trunk_x = 621
    draw.rectangle((trunk_x - 32, 520, trunk_x + 32, 1190), fill=P["brick"])
    stages = [("需要", 1110), ("结构", 920), ("节奏", 730), ("装饰", 540)]
    for i, (label, yy) in enumerate(stages):
        width = 210 + i * 95
        draw.rounded_rectangle((trunk_x - width // 2, yy - 42, trunk_x + width // 2, yy + 42), radius=42, fill=P["paper"] if i % 2 == 0 else P["green"])
        fill = P["ink"] if i % 2 == 0 else P["white"]
        bbox = draw.textbbox((0, 0), label, font=base.get_font(30, bold=True))
        draw.text((trunk_x - (bbox[2] - bbox[0]) // 2, yy - 20), label, font=base.get_font(30, bold=True), fill=fill)

    for side in (-1, 1):
        for index, yy in enumerate((660, 575, 505)):
            ex = trunk_x + side * (220 + index * 92)
            draw.line((trunk_x, yy + 100, ex, yy), fill=P["gold"], width=7)
            leaf(draw, (ex + side * 56, yy), 0.75, P["clay"], 4)

    methods = [
        ("先定动作", "写清空间真正承担的使用与公共动作"),
        ("再定节奏", "让结构、开口与楼层形成可读关系"),
        ("最后加深", "只在入口、转角和收口处集中装饰"),
    ]
    y0 = 1270
    for i, (head, body) in enumerate(methods):
        x = 55 + i * 395
        draw.rounded_rectangle((x, y0, x + 358, 1532), radius=8, outline=P["paper"], width=2)
        draw.text((x + 24, y0 + 25), f"0{i + 1}  {head}", font=base.get_font(27, bold=True), fill=P["gold"])
        base.text_block(draw, (x + 24, y0 + 92), body, base.get_font(27), P["white"], 305, 11)

    base.draw_page_mark(draw, 10, P["ink"], light=True)
    return image


def save_jpg(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0, optimize=True)


def make_preview(paths: list[Path]) -> None:
    thumb_w, thumb_h, gap = 210, 280, 24
    canvas = Image.new("RGB", (1242, 654), P["ink"])
    for index, path in enumerate(paths):
        thumb = ImageOps.fit(Image.open(path).convert("RGB"), (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        col, row = index % 5, index // 5
        canvas.paste(thumb, (24 + col * (thumb_w + gap), 24 + row * (thumb_h + gap)))
    save_jpg(canvas, OUTPUT / "preview.jpg")


def write_docs(paths: list[Path]) -> None:
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    publish = f"{BOOK['publish_title']}\n\n{BOOK['publish_body']}\n\n{BOOK['tags']}\n"
    (OUTPUT / "发布文案.md").write_text(publish, encoding="utf-8")

    source_lines = [
        "# 图片来源",
        "",
        "本套共 10 张：01 为问题封面，02–09 为八个真实建筑案例，10 为编辑性总结。",
        "书封保持原始内容，仅等比缩放；建筑图均为对应项目的真实照片。",
        "礼堂大厦、温莱特大厦与担保大厦均为 Adler & Sullivan 合作时期作品；克劳斯音乐商店由 William Presto 与 Louis Sullivan 共同参与。",
        "",
    ]
    for item in manifest:
        source_lines.extend([
            f"## {item['filename']}｜{item['content']}", "",
            f"- 作者/机构：{item['credit']}",
            f"- 来源：{item['source_url']}",
            f"- 授权：{item['license']}",
            f"- 处理：{item['modifications']}", "",
        ])
    (OUTPUT / "图片来源.md").write_text("\n".join(source_lines), encoding="utf-8")

    post = {
        "title": BOOK["publish_title"],
        "book": BOOK["book"],
        "edition": BOOK["edition"],
        "card_count": 10,
        "dimensions": [W, H],
        "format": "JPEG RGB quality 95",
        "visual_system": "vertical organic growth + alternating evidence panels + organism-section synthesis",
        "cover_policy": "verified Open Library/Dover cover, proportional scaling only, no redraw",
        "cards": [
            {"page": 1, "file": paths[0].name, "role": "question_cover", "layout": "large cover with vertical growth register"},
            *[{"page": i + 2, "file": paths[i + 1].name, "role": "real_case_evidence", "project": case["title"], "year": case["year"], "image": case["asset"]} for i, case in enumerate(CASES)],
            {"page": 10, "file": paths[9].name, "role": "synthesis", "layout": "roots-trunk-crown organism section"},
        ],
        "copy": publish,
        "source_manifest": str((ASSETS / "manifest.json").relative_to(ROOT)),
    }
    (OUTPUT / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")


def validate(paths: list[Path]) -> dict:
    checks = []
    for path in paths:
        with Image.open(path) as image:
            rgb = image.convert("RGB")
            extrema = rgb.getextrema()
            checks.append({"file": path.name, "size": list(rgb.size), "mode": rgb.mode, "nonblank": any(lo != hi for lo, hi in extrema)})
    required = all((OUTPUT / name).exists() for name in ("preview.jpg", "发布文案.md", "图片来源.md", "post.json"))
    passed = len(paths) == 10 and required and len(BOOK["publish_title"]) <= 20 and all(x["size"] == [W, H] and x["mode"] == "RGB" and x["nonblank"] for x in checks)
    result = {"pass": passed, "title_length": len(BOOK["publish_title"]), "body_length": len(BOOK["publish_body"].replace("\n", "")), "required_files": required, "cards": checks}
    (OUTPUT / "qa-report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    images = [cover_card(), *[case_card(case, i + 2) for i, case in enumerate(CASES)], summary_card()]
    paths = []
    for i, image in enumerate(images, start=1):
        path = OUTPUT / f"{i:02d}.jpg"
        save_jpg(image, path)
        paths.append(path)
    make_preview(paths)
    write_docs(paths)
    print(json.dumps(validate(paths), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
