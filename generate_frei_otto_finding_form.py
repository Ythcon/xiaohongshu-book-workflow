#!/usr/bin/env python3
"""Render a ten-card Xiaohongshu post for Frei Otto and Bodo Rasch's Finding Form."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "frei-otto-finding-form"
OUTPUT = ROOT / "output" / "frei-otto-finding-form"
W, H = 1242, 1660

P = {
    "paper": (241, 237, 223),
    "ink": (15, 31, 44),
    "navy": (20, 43, 61),
    "steel": (72, 107, 132),
    "sky": (167, 194, 205),
    "coral": (195, 89, 61),
    "wood": (151, 102, 60),
    "gold": (214, 177, 95),
    "white": (252, 250, 243),
    "muted": (107, 107, 100),
}

BOOK = {
    "designer": "弗莱·奥托 / 博多·拉施",
    "designer_en": "FREI OTTO · BODO RASCH",
    "book": "Finding Form: Towards an Architecture of the Minimal",
    "book_cn": "《寻找形式：走向最少的建筑》",
    "edition": "Edition Axel Menges, 1996｜ISBN 9783930698660",
    "question": "最好的形状，\n为什么不是先画出来的？",
    "thesis": "先给出力、材料与边界，形状才会在试验与建造中出现。",
    "publish_title": "弗莱·奥托：形状为什么不能先画？",
    "publish_body": (
        "《Finding Form》最重要的提醒是：形式并非先被想象出来，再让结构替它背书。对弗莱·奥托而言，荷载、材料、边界与连接方式本身就是设计工具；先把条件设好，形状才会在模型、计算与建造中逐步出现。\n\n"
        "蒙特利尔德国馆用索网和膜面把展览空间从地面解放出来；斯图加特轻型结构研究所保留试验建筑，让模型直接进入长期研究；慕尼黑奥运屋顶以桅杆、索网和透明板连续覆盖场地，而节点细部把力的传递变得可读。\n\n"
        "曼海姆多功能厅把平直木条编成双曲网格壳：外部看是起伏屋面，内部才看见曲率如何换来跨度与空旷。不同入口、走道和大厅视角说明，轻型结构并不是一张好看的表皮，而是一套长期组织材料、维修和使用的系统。\n\n"
        "对设计师更实用的顺序是：先列出不可改变的受力与边界；用模型比较不同连接的变形；最后再决定哪些曲线值得被保留。不是先画一个姿态，再寻找理由，而是让理由慢慢长出姿态。\n\n"
        "本文为基于书籍与案例资料的编辑性阅读，不是原书逐字引语。"
    ),
    "tags": "#弗莱奥托 #FindingForm #轻型结构 #张拉结构 #建筑构造 #建筑理论 #建筑书单 #设计方法",
}

CASES = [
    {
        "year": "1967",
        "title": "蒙特利尔世博德国馆",
        "meta": "加拿大｜Frei Otto 与 Rolf Gutbrod",
        "headline": "先把受力交给结构，\n再把空间留给人",
        "body": "索网与膜面被抬离地面，下方成为可自由展开的展览空间。轻不是把材料单纯做薄，而是让材料只在真正需要它工作的地方出现。",
        "asset": "02-expo67.jpg",
        "focus": (0.50, 0.46),
    },
    {
        "year": "1965–68",
        "title": "轻型结构研究所",
        "meta": "斯图加特｜IL，原世博试验建筑",
        "headline": "模型不是展示品，\n是形状被发现的现场",
        "body": "这座建筑起初是德国馆的试验单元，后来成为研究所的一部分。试验不在纸外等待验证，而被保留为持续观察材料、曲率与支撑关系的工作现场。",
        "asset": "03-il-stuttgart.jpg",
        "focus": (0.50, 0.52),
    },
    {
        "year": "1972",
        "title": "慕尼黑奥林匹克屋顶",
        "meta": "德国｜Behnisch & Partner、Frei Otto 等",
        "headline": "一张连续的网，\n比一组独立屋顶更能组织场地",
        "body": "桅杆、索网与透明板连续跨过体育场、广场和步行空间。屋顶不再只是单体建筑的帽子，而成为让地形、运动与城市活动保持连通的基础设施。",
        "asset": "04-munich-wide.jpg",
        "focus": (0.48, 0.48),
    },
    {
        "year": "1972",
        "title": "慕尼黑奥林匹克屋顶细部",
        "meta": "德国｜Olympiapark",
        "headline": "节点决定屋顶能否\n既轻又可读",
        "body": "杆件、索、夹具和板材在一个节点相遇。复杂并没有被藏起来：连接方式让力的路径可被看见，也让维护、替换和局部调整有明确的落点。",
        "asset": "05-munich-detail.jpg",
        "focus": (0.50, 0.48),
    },
    {
        "year": "1975",
        "title": "曼海姆多功能厅",
        "meta": "德国｜Multihalle，外部",
        "headline": "平直木条，\n不必做成平直屋顶",
        "body": "小截面木条交织成网格壳，依靠双向曲率获得刚度。材料的常规尺度没有变，几何与连接方式改变后，却能覆盖一片起伏而连续的公共空间。",
        "asset": "06-multihalle-outside.jpg",
        "focus": (0.50, 0.46),
    },
    {
        "year": "1975",
        "title": "曼海姆多功能厅",
        "meta": "德国｜Multihalle，大厅",
        "headline": "曲率不是造型，\n是让大跨空间站住的方式",
        "body": "从内部看，木格栅连续弯曲，几乎没有厚重梁墙切断视线。形状来自结构工作后的结果，也反过来制造出可集会、可变化的无柱大空间。",
        "asset": "07-multihalle-inside.jpg",
        "focus": (0.50, 0.48),
    },
    {
        "year": "1975",
        "title": "曼海姆多功能厅",
        "meta": "德国｜Multihalle，入口与通道",
        "headline": "轻型结构，\n必须把长期使用一起设计",
        "body": "入口、坡道、边缘支撑和屋面曲线同时出现。省材料不等于省思考：结构越轻，排水、维护、通行与局部修补越要在一开始被纳入判断。",
        "asset": "08-multihalle-entry.jpg",
        "focus": (0.50, 0.50),
    },
    {
        "year": "1972",
        "title": "慕尼黑奥林匹克体育场",
        "meta": "德国｜体育场内部",
        "headline": "轻型屋顶不是消失，\n而是让使用环境继续可见",
        "body": "透明屋面过滤日光，索网的曲线在看台上方延续。遮蔽、采光、视线和现场氛围不必分成四套方案，它们可以在同一张结构网里被共同协调。",
        "asset": "09-munich-stadium.jpg",
        "focus": (0.50, 0.46),
    },
]


def catenary(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], sag: int, color, width: int = 5) -> None:
    """Draw a simple parabolic hanging line, used only as an explanatory force trace."""
    x0, y0 = start
    x1, y1 = end
    points = []
    for i in range(61):
        t = i / 60
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + 4 * sag * t * (1 - t)
        points.append((int(x), int(y)))
    draw.line(points, fill=color, width=width, joint="curve")


def anchor(draw: ImageDraw.ImageDraw, x: int, y: int, color) -> None:
    draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=P["navy"], outline=color, width=4)


def cover_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["navy"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 242), fill=P["ink"])
    draw.text((66, 58), "FORM IS NOT DRAWN FIRST", font=base.get_font(23, bold=True), fill=P["gold"])
    draw.text((66, 112), BOOK["designer_en"], font=base.get_font(37, bold=True), fill=P["white"])
    draw.text((920, 84), "1996", font=base.get_font(34, bold=True), fill=P["sky"])

    # Force traces stay below the type and outside the verified cover.
    catenary(draw, (60, 1030), (622, 1260), 190, P["sky"], 7)
    catenary(draw, (1180, 1040), (622, 1260), 175, P["coral"], 7)
    catenary(draw, (92, 1435), (622, 1260), 92, P["gold"], 5)
    catenary(draw, (1150, 1438), (622, 1260), 86, P["steel"], 5)
    for x, y, color in [(60, 1030, P["sky"]), (1180, 1040, P["coral"]), (92, 1435, P["gold"]), (1150, 1438, P["steel"]), (622, 1260, P["white"])]:
        anchor(draw, x, y, color)

    cover = Image.open(ASSETS / "cover.jpg").convert("RGB")
    base.paste_cover(image, cover, (690, 270, 1175, 828), shadow=True)

    draw.text((66, 336), "FINDING", font=base.get_font(26, bold=True), fill=P["gold"])
    draw.text((66, 382), "FORM", font=base.get_font(26, bold=True), fill=P["sky"])
    y = base.text_block(draw, (62, 456), BOOK["question"], base.get_font(65, bold=True), P["white"], 580, 5)
    draw.rectangle((66, y + 26, 555, y + 34), fill=P["coral"])
    base.text_block(draw, (66, y + 72), BOOK["thesis"], base.get_font(30), P["white"], 530, 13)

    draw.rounded_rectangle((68, 858, 620, 996), radius=10, outline=P["gold"], width=2)
    draw.text((94, 886), "EDITION AXEL MENGES · 1996", font=base.get_font(21, bold=True), fill=P["gold"])
    draw.text((94, 932), "真实书封 · 等比呈现 · 未重绘", font=base.get_font(23), fill=P["white"])

    draw.text((664, 1188), "荷载", font=base.get_font(31, bold=True), fill=P["white"])
    draw.text((664, 1243), "材料", font=base.get_font(31, bold=True), fill=P["white"])
    draw.text((664, 1298), "边界", font=base.get_font(31, bold=True), fill=P["white"])
    draw.text((664, 1353), "连接", font=base.get_font(31, bold=True), fill=P["white"])
    base.draw_page_mark(draw, 1, P["ink"], light=True)
    return image


def photo_panel(source: Image.Image, size: tuple[int, int], focus: tuple[float, float]) -> Image.Image:
    source = ImageEnhance.Contrast(source.convert("RGB")).enhance(1.025)
    source = ImageEnhance.Color(source).enhance(0.94)
    return ImageOps.fit(source, size, Image.Resampling.LANCZOS, centering=focus)


def case_card(case: dict, page: int) -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    photo_top = page % 2 == 0
    photo_h = 845
    photo_y = 0 if photo_top else H - photo_h
    text_y = 906 if photo_top else 78

    source = Image.open(ASSETS / case["asset"]).convert("RGB")
    image.paste(photo_panel(source, (W, photo_h), case["focus"]), (0, photo_y))
    boundary = photo_h if photo_top else photo_y
    draw.rectangle((0, boundary - 11, W, boundary + 11), fill=P["navy"])
    draw.rectangle((0, boundary + (11 if photo_top else -19), W, boundary + (18 if photo_top else -12)), fill=P["coral"])

    # Small force line remains in the type zone, never over the actual photograph.
    sx = 68 if photo_top else 1150
    catenary(draw, (sx, text_y + 52), (sx, text_y + 605), 74, P["steel"], 5)
    anchor(draw, sx, text_y + 52, P["steel"])
    anchor(draw, sx, text_y + 605, P["steel"])

    tx = 107 if photo_top else 76
    width = 1000 if photo_top else 1020
    draw.text((tx, text_y), case["year"], font=base.get_font(30, bold=True), fill=P["coral"])
    draw.text((tx + 185, text_y + 3), case["meta"], font=base.get_font(23), fill=P["muted"])
    draw.text((tx, text_y + 67), case["title"], font=base.get_font(39, bold=True), fill=P["navy"])
    y = base.text_block(draw, (tx, text_y + 145), case["headline"], base.get_font(54, bold=True), P["ink"], width, 4)
    base.text_block(draw, (tx, y + 27), case["body"], base.get_font(30), P["ink"], width - 30, 13)
    base.draw_page_mark(draw, page, P["ink"], light=not photo_top)
    return image


def summary_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 255), fill=P["navy"])
    draw.text((68, 58), "FORM FINDING / A PRACTICAL ORDER", font=base.get_font(23, bold=True), fill=P["gold"])
    base.text_block(draw, (68, 112), "不要先画姿态，\n让理由慢慢长出姿态", base.get_font(56, bold=True), P["white"], 900, 4)

    # Hanging-summary diagram: conditions are anchors, not a transfer station or radial chart.
    anchors = [(110, 490, "荷载", P["coral"]), (350, 490, "材料", P["wood"]), (610, 490, "边界", P["steel"]), (870, 490, "连接", P["navy"]), (1125, 490, "使用", P["gold"])]
    for x, y, label, color in anchors:
        draw.line((x, y - 80, x, y), fill=P["muted"], width=3)
        draw.ellipse((x - 44, y - 44, x + 44, y + 44), fill=color, outline=P["white"], width=3)
        bbox = draw.textbbox((0, 0), label, font=base.get_font(25, bold=True))
        draw.text((x - (bbox[2] - bbox[0]) / 2, y - 18), label, font=base.get_font(25, bold=True), fill=P["white"] if color != P["gold"] else P["ink"])

    lowest = (621, 940)
    for x, y, _label, color in anchors:
        catenary(draw, (x, y + 44), lowest, 118, color, 7)
    draw.ellipse((lowest[0] - 118, lowest[1] - 86, lowest[0] + 118, lowest[1] + 86), fill=P["navy"], outline=P["gold"], width=7)
    draw.text((lowest[0] - 70, lowest[1] - 35), "形式", font=base.get_font(48, bold=True), fill=P["white"])
    draw.text((400, 1060), "先给条件，再让形状出现", font=base.get_font(31, bold=True), fill=P["coral"])

    methods = [
        ("01  先列边界", "写出荷载、跨度、材料与不可移动的支点"),
        ("02  再做试验", "用模型比较连接方式与变形，不抢画最终曲线"),
        ("03  最后保留", "只保留那些能同时回应受力与使用的形状"),
    ]
    y0 = 1190
    for i, (head, body) in enumerate(methods):
        x = 55 + i * 395
        fill = P["navy"] if i != 1 else P["steel"]
        draw.rounded_rectangle((x, y0, x + 355, 1488), radius=10, fill=fill)
        draw.text((x + 24, y0 + 27), head, font=base.get_font(27, bold=True), fill=P["gold"])
        base.text_block(draw, (x + 24, y0 + 96), body, base.get_font(28), P["white"], 302, 12)

    draw.text((68, 1530), "基于书籍与八张真实项目照片的编辑性总结", font=base.get_font(21), fill=P["muted"])
    base.draw_page_mark(draw, 10, P["ink"])
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
        "本套共 10 张：01 为问题封面，02–09 为八张真实项目照片，10 为编辑性总结。",
        "书封保持原始内容，仅等比缩放；所有案例图均为对应建筑的实拍，不含 AI 生成或伪造建筑图。",
        "06–08 为曼海姆多功能厅的三张不同实拍视角；04、05、09 为慕尼黑奥运张拉屋顶的三张不同实拍视角，分别用于讲解场地、节点与使用体验。",
        "本文内容为编辑性阅读，不构成原书逐字引语。",
        "",
    ]
    for item in manifest:
        source_lines += [
            f"## {item['filename']}｜{item['content']}",
            "",
            f"- 作者/机构：{item['credit']}",
            f"- 来源：{item['source_url']}",
            f"- 授权：{item['license']}",
            f"- 许可链接：{item['license_url'] or '见来源页'}",
            f"- 处理：{item['modifications']}",
            "",
        ]
    (OUTPUT / "图片来源.md").write_text("\n".join(source_lines), encoding="utf-8")

    post = {
        "title": BOOK["publish_title"],
        "book": BOOK["book"],
        "edition": BOOK["edition"],
        "card_count": 10,
        "dimensions": [W, H],
        "format": "JPEG RGB quality 95",
        "visual_system": "catenary force traces + alternating real-photo evidence + hanging-condition conclusion",
        "cover_policy": "verified Edition Axel Menges cover, proportional scaling only, no redraw",
        "cards": [
            {"page": 1, "file": paths[0].name, "role": "question_cover", "layout": "large verified cover with catenary force field"},
            *[
                {"page": i + 2, "file": paths[i + 1].name, "role": "real_case_evidence", "project": case["title"], "year": case["year"], "image": case["asset"]}
                for i, case in enumerate(CASES)
            ],
            {"page": 10, "file": paths[9].name, "role": "synthesis", "layout": "five hanging conditions converge into form"},
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
    passed = (
        len(paths) == 10 and required and len(BOOK["publish_title"]) <= 20
        and 300 <= len(BOOK["publish_body"].replace("\n", "")) <= 500
        and all(item["size"] == [W, H] and item["mode"] == "RGB" and item["nonblank"] for item in checks)
    )
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
