#!/usr/bin/env python3
"""Render a ten-card Xiaohongshu post for Otto Wagner's Modern Architecture."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "otto-wagner-modern-architecture"
OUTPUT = ROOT / "output" / "otto-wagner-modern-architecture"
W, H = 1242, 1660

P = {
    "paper": (244, 239, 219),
    "ink": (23, 31, 29),
    "green": (83, 116, 88),
    "deep_green": (31, 69, 56),
    "blue": (24, 91, 111),
    "cobalt": (24, 67, 112),
    "gold": (207, 158, 64),
    "coral": (193, 76, 53),
    "white": (252, 249, 237),
    "muted": (105, 103, 89),
}

BOOK = {
    "designer": "奥托·瓦格纳",
    "designer_en": "OTTO WAGNER",
    "book": "Modern Architecture: A Guidebook for His Students to This Field of Art",
    "book_cn": "《现代建筑：给学生的这一艺术领域指南》",
    "edition": "Harry Francis Mallgrave 英译及导论｜Getty Research Institute, 1988｜ISBN 9780226869391",
    "question": "现代建筑，\n为什么不能先从风格开始？",
    "thesis": "生活、交通、卫生、经济与新材料先改变条件，形式随后更新。",
    "publish_title": "瓦格纳：现代建筑为何不从风格开始？",
    "publish_body": (
        "《Modern Architecture》不是一本教人复制维也纳装饰的风格书。瓦格纳真正激进的判断是：当交通、卫生、材料、经济和现代生活都已改变，建筑就不能继续借历史样式假装一切未变。\n\n"
        "第一别墅仍保留对称柱廊与历史主义礼仪；努斯多夫水闸开始把工程设施转化为城市节点；希青宫廷车站在统一城铁系统中回应特殊抵达；卡尔广场亭则用金属骨架和板材建立可装配、可识别的公共入口。\n\n"
        "马约利卡住宅把易于维护的陶瓷变成连续城市表皮；邮政储蓄银行让金属固定点直接成为立面秩序；施泰因霍夫教堂以现代材料回应仪式与照护；多瑙运河控制室则把运行、临水位置和表皮分层压进一座基础设施。\n\n"
        "对设计师更实用的顺序是：先列出现代条件，再决定结构与连接怎样被看见，最后才用图案强化入口、分区和识别。现代不是删掉装饰，而是要求每个形式重新获得理由。\n\n"
        "本文为基于书籍与案例资料的编辑性阅读，不是原书逐字引语。"
    ),
    "tags": "#奥托瓦格纳 #ModernArchitecture #维也纳现代主义 #建筑表皮 #建筑构造 #建筑理论 #建筑书单 #设计方法",
}

CASES = [
    {
        "year": "1888",
        "title": "第一别墅",
        "meta": "维也纳｜Villa Wagner I",
        "headline": "现代不是突然断裂，\n而是先暴露旧规则",
        "body": "对称柱廊、纪念性台阶与丰富装饰仍属于历史主义。它是理解转变的起点：瓦格纳后来不是简单换风格，而是逐步让材料、建造与生活条件进入形式判断。",
        "asset": "02-villa-i.jpg",
        "focus": (0.50, 0.49),
    },
    {
        "year": "1894–99",
        "title": "努斯多夫水闸",
        "meta": "维也纳｜舍梅尔桥细部",
        "headline": "工程设施，也需要进入城市经验",
        "body": "水闸、桥梁与机械承担防洪和通行，石台、金属构件与灯具又把基础设施转化为可识别的公共节点。技术没有被藏在纪念性后面。",
        "asset": "03-nussdorf.jpg",
        "focus": (0.50, 0.43),
        "contain": True,
    },
    {
        "year": "1898",
        "title": "希青宫廷车站",
        "meta": "维也纳城铁｜Hofpavillon",
        "headline": "同一交通系统，\n可以回应不同使用者",
        "body": "它属于维也纳城铁，却为皇室抵达设置独立入口、候车空间与圆顶。标准交通网络与具体礼仪需求，在一个节点发生调整。",
        "asset": "04-hofpavillon.jpg",
        "focus": (0.50, 0.53),
    },
    {
        "year": "1898",
        "title": "卡尔广场城铁亭",
        "meta": "维也纳｜Karlsplatz",
        "headline": "模块化建造，\n也能形成城市识别",
        "body": "绿色金属骨架、白色板材与重复连接组织出可装配的车站界面；清晰入口和金色图案，让通勤设施在街道上被迅速认出。",
        "asset": "05-karlsplatz.jpg",
        "focus": (0.50, 0.48),
    },
    {
        "year": "1898–99",
        "title": "马约利卡住宅",
        "meta": "维也纳｜Majolica House",
        "headline": "装饰可以成为\n可维护的城市表皮",
        "body": "陶瓷板把花卉图案变成易于清洁、可重复的外墙系统；窗洞遵守住宅模数，图案则跨越模数，使维护、施工与城市表情同时成立。",
        "asset": "06-majolica.jpg",
        "focus": (0.50, 0.48),
    },
    {
        "year": "1904–06",
        "title": "奥地利邮政储蓄银行",
        "meta": "维也纳｜Postsparkasse",
        "headline": "构造连接，\n不必伪装成石砌传统",
        "body": "薄石板通过可见金属固定点安装在外墙，重复点阵让连接逻辑成为立面秩序；材料看起来轻，建筑仍保持公共机构的稳定感。",
        "asset": "07-postsparkasse.jpg",
        "focus": (0.50, 0.49),
    },
    {
        "year": "1904–07",
        "title": "施泰因霍夫教堂",
        "meta": "维也纳｜Kirche am Steinhof",
        "headline": "现代材料，\n也能服务仪式与照护",
        "body": "白色板材、金属节点和金色穹顶建立清晰整体；作为医院教堂，空间与细部还回应患者的可达、视线与使用安全。",
        "asset": "08-steinhof.jpg",
        "focus": (0.50, 0.48),
    },
    {
        "year": "1904–08",
        "title": "多瑙运河控制室",
        "meta": "维也纳｜Schützenhaus",
        "headline": "基础设施的表皮，\n应承认自己的系统",
        "body": "石材基座、白色板材与蓝色陶瓷带形成清楚分层；开口、楼梯和临水位置直接回应运行，图案只强化分区与识别。",
        "asset": "09-schuetzenhaus.jpg",
        "focus": (0.50, 0.48),
    },
]


def draw_track(draw: ImageDraw.ImageDraw, points, color, width=8, nodes=True) -> None:
    draw.line(points, fill=color, width=width, joint="curve")
    if nodes:
        for x, y in points:
            draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=P["paper"], outline=color, width=5)


def cover_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)

    # A city-track field unique to this set; all lines remain outside the cover itself.
    draw.rectangle((0, 0, W, 224), fill=P["deep_green"])
    draw.text((68, 54), "A GUIDEBOOK FOR A CHANGED CITY", font=base.get_font(23, bold=True), fill=P["gold"])
    draw.text((68, 112), BOOK["designer_en"], font=base.get_font(43, bold=True), fill=P["white"])
    draw.text((956, 73), "1896", font=base.get_font(35, bold=True), fill=P["gold"])

    draw_track(draw, [(30, 330), (316, 330), (515, 424), (1165, 424)], P["cobalt"], 8)
    draw_track(draw, [(1182, 270), (1182, 1120), (1110, 1210), (1110, 1510)], P["coral"], 7)
    draw_track(draw, [(360, 1440), (855, 1440), (1020, 1305)], P["gold"], 8)

    # Large verified cover: proportional scaling only, no crop and no redraw.
    cover = Image.open(ASSETS / "cover.jpg").convert("RGB")
    base.paste_cover(image, cover, (62, 428, 682, 1291), shadow=True)

    draw.text((725, 510), "MODERN", font=base.get_font(27, bold=True), fill=P["coral"])
    draw.text((725, 555), "IS A CONDITION", font=base.get_font(25, bold=True), fill=P["blue"])
    y = base.text_block(draw, (720, 635), BOOK["question"], base.get_font(63, bold=True), P["ink"], 455, 5)
    draw.rectangle((722, y + 22, 1125, y + 30), fill=P["gold"])
    base.text_block(draw, (722, y + 64), BOOK["thesis"], base.get_font(30), P["deep_green"], 445, 13)

    draw.rounded_rectangle((720, 1220, 1160, 1407), radius=8, fill=P["deep_green"])
    draw.text((746, 1248), "GETTY · 1988", font=base.get_font(22, bold=True), fill=P["gold"])
    base.text_block(draw, (746, 1294), "真实书封等比呈现\n英译：Harry F. Mallgrave", base.get_font(22), P["white"], 382, 8)
    base.draw_page_mark(draw, 1, P["ink"])
    return image


def photo_panel(source: Image.Image, size: tuple[int, int], focus=(0.5, 0.5), contain=False) -> Image.Image:
    source = ImageEnhance.Contrast(source.convert("RGB")).enhance(1.025)
    source = ImageEnhance.Color(source).enhance(0.95)
    if contain:
        panel = Image.new("RGB", size, P["deep_green"])
        fitted = ImageOps.contain(source, (size[0] - 130, size[1]), Image.Resampling.LANCZOS)
        panel.paste(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
        return panel
    return ImageOps.fit(source, size, Image.Resampling.LANCZOS, centering=focus)


def case_card(case: dict, page: int) -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    photo_top = page % 2 == 0
    photo_h = 840
    photo_y = 0 if photo_top else H - photo_h
    text_y = 905 if photo_top else 84

    source = Image.open(ASSETS / case["asset"]).convert("RGB")
    panel = photo_panel(source, (W, photo_h), case.get("focus", (0.5, 0.5)), case.get("contain", False))
    image.paste(panel, (0, photo_y))

    boundary = photo_h if photo_top else photo_y
    draw.rectangle((0, boundary - 11, W, boundary + 11), fill=P["deep_green"])
    draw.rectangle((0, boundary + (11 if photo_top else -20), W, boundary + (18 if photo_top else -13)), fill=P["gold"])

    # A small chronological rail is confined to the text field.
    rail_x = 64 if photo_top else 1125
    draw.line((rail_x, text_y - 8, rail_x, text_y + 590), fill=P["cobalt"], width=7)
    for node_y in (text_y + 22, text_y + 236, text_y + 505):
        draw.ellipse((rail_x - 10, node_y - 10, rail_x + 10, node_y + 10), fill=P["paper"], outline=P["cobalt"], width=4)

    tx = 105 if photo_top else 76
    max_width = 1000 if photo_top else 995
    draw.text((tx, text_y), case["year"], font=base.get_font(30, bold=True), fill=P["coral"])
    draw.text((tx + 185, text_y + 3), case["meta"], font=base.get_font(23), fill=P["muted"])
    draw.text((tx, text_y + 66), case["title"], font=base.get_font(39, bold=True), fill=P["deep_green"])
    y = base.text_block(draw, (tx, text_y + 143), case["headline"], base.get_font(54, bold=True), P["ink"], max_width, 4)
    base.text_block(draw, (tx, y + 28), case["body"], base.get_font(30), P["ink"], max_width - 28, 13)

    if case.get("contain"):
        draw.text((936, photo_y + photo_h - 43), "真实细部 · 完整竖幅", font=base.get_font(19), fill=P["white"])

    base.draw_page_mark(draw, page, P["ink"], light=not photo_top)
    return image


def summary_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["deep_green"])
    draw = ImageDraw.Draw(image)

    draw.text((68, 60), "FROM CONDITIONS TO FORM", font=base.get_font(24, bold=True), fill=P["gold"])
    y = base.text_block(draw, (68, 120), "现代不是删掉装饰，\n而是让形式重新获得理由", base.get_font(60, bold=True), P["white"], 1010, 5)
    base.text_block(draw, (72, y + 23), "条件先变，判断随后，形式最后出现。", base.get_font(29), P["gold"], 850, 10)

    # Transfer-station diagram: five present-day conditions converge on one judgement.
    labels = ["生活", "交通", "卫生", "经济", "材料"]
    colors = [P["gold"], P["coral"], P["blue"], (180, 200, 146), P["white"]]
    start_y = 555
    junction = (745, 760)
    for i, (label, color) in enumerate(zip(labels, colors)):
        yy = start_y + i * 105
        draw.rounded_rectangle((66, yy - 31, 224, yy + 31), radius=31, fill=color)
        label_fill = P["ink"] if color != P["coral"] else P["white"]
        box = draw.textbbox((0, 0), label, font=base.get_font(27, bold=True))
        draw.text((145 - (box[2] - box[0]) / 2, yy - 19), label, font=base.get_font(27, bold=True), fill=label_fill)
        elbow_x = 350 + i * 65
        draw.line([(224, yy), (elbow_x, yy), (junction[0] - 90, junction[1])], fill=color, width=8, joint="curve")

    draw.ellipse((junction[0] - 102, junction[1] - 102, junction[0] + 102, junction[1] + 102), fill=P["paper"], outline=P["gold"], width=8)
    draw.text((junction[0] - 59, junction[1] - 38), "判断", font=base.get_font(43, bold=True), fill=P["ink"])
    draw.line((junction[0] + 102, junction[1], 1040, junction[1]), fill=P["gold"], width=13)
    draw.polygon([(1040, junction[1] - 25), (1094, junction[1]), (1040, junction[1] + 25)], fill=P["gold"])
    draw.rounded_rectangle((1010, 675, 1175, 845), radius=12, fill=P["paper"])
    draw.text((1048, 729), "形式", font=base.get_font(43, bold=True), fill=P["ink"])

    methods = [
        ("01  先列条件", "人流、维护、卫生、施工与经济"),
        ("02  再显连接", "让结构与安装方式成为可读秩序"),
        ("03  最后识别", "图案只强化入口、分区和城市记忆"),
    ]
    y0 = 1120
    for i, (head, body) in enumerate(methods):
        x = 55 + i * 395
        fill = P["cobalt"] if i == 1 else P["ink"]
        draw.rounded_rectangle((x, y0, x + 355, 1478), radius=10, fill=fill, outline=P["gold"], width=2)
        draw.text((x + 24, y0 + 28), head, font=base.get_font(27, bold=True), fill=P["gold"])
        base.text_block(draw, (x + 24, y0 + 102), body, base.get_font(28), P["white"], 302, 13)

    draw.text((68, 1530), "基于书籍与八个真实案例的编辑性总结", font=base.get_font(21), fill=(189, 205, 188))
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
        "书封保持原始内容，仅等比缩放并置于版面；所有建筑图均为对应项目的真实照片，未使用 AI 生成图片。",
        "03 使用舍梅尔桥与努斯多夫水闸的真实细部竖幅；09 为多瑙运河控制室现状照片。",
        "",
    ]
    for item in manifest:
        source_lines += [
            f"## {item['filename']}｜{item['content']}",
            "",
            f"- 作者/机构：{item['credit']}",
            f"- 来源：{item['source_url']}",
            f"- 授权：{item['license']}",
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
        "visual_system": "large verified cover + city-track chronology + condition-transfer synthesis",
        "cover_policy": "verified Getty/Open Library cover, proportional scaling only, no redraw",
        "cards": [
            {"page": 1, "file": paths[0].name, "role": "question_cover", "layout": "large cover crossed by external city tracks"},
            *[
                {
                    "page": i + 2,
                    "file": paths[i + 1].name,
                    "role": "real_case_evidence",
                    "project": case["title"],
                    "year": case["year"],
                    "image": case["asset"],
                }
                for i, case in enumerate(CASES)
            ],
            {"page": 10, "file": paths[9].name, "role": "synthesis", "layout": "five-condition transfer station"},
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
            checks.append({
                "file": path.name,
                "size": list(rgb.size),
                "mode": rgb.mode,
                "nonblank": any(lo != hi for lo, hi in extrema),
            })
    required = all((OUTPUT / n).exists() for n in ("preview.jpg", "发布文案.md", "图片来源.md", "post.json"))
    passed = (
        len(paths) == 10
        and required
        and len(BOOK["publish_title"]) <= 20
        and 300 <= len(BOOK["publish_body"].replace("\n", "")) <= 500
        and all(x["size"] == [W, H] and x["mode"] == "RGB" and x["nonblank"] for x in checks)
    )
    result = {
        "pass": passed,
        "title_length": len(BOOK["publish_title"]),
        "body_length": len(BOOK["publish_body"].replace("\n", "")),
        "required_files": required,
        "cards": checks,
    }
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
