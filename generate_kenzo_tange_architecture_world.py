#!/usr/bin/env python3
"""Render a ten-card Xiaohongshu post for Kenzo Tange's Architecture for the World."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import generate_three_unmentioned_masters as base

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "kenzo-tange-architecture-world"
OUTPUT = ROOT / "output" / "kenzo-tange-architecture-world"
W, H = 1242, 1660
P = {"paper": (239, 237, 229), "ink": (28, 30, 34), "red": (202, 49, 41), "blue": (46, 80, 101), "sand": (206, 193, 165), "white": (252, 251, 247), "muted": (96, 96, 90), "dark": (33, 42, 47)}
BOOK = {
    "designer": "丹下健三", "designer_en": "KENZŌ TANGE", "book": "Kenzō Tange: Architecture for the World", "book_cn": "《为世界而建的建筑》", "edition": "Seng Kuan、Yukio Lippit 编｜Lars Müller, 2012｜ISBN 9783037783108",
    "question": "大跨度结构，\n如何变成公共空间？", "thesis": "结构不是为大屋顶服务的技术附属；它可把纪念、集体活动与城市尺度同时组织起来。", "publish_title": "丹下健三：结构怎样放大公共性？",
    "publish_body": "《Kenzō Tange: Architecture for the World》把丹下健三放回战后日本的城市、技术与公共文化中阅读。书中最值得带走的，不是某一种混凝土造型，而是他如何把结构做成组织社会尺度的骨架。\n\n广岛和平纪念资料馆以架空体量、轴线与公园共同建立纪念的公共距离；代代木国立体育馆用悬索屋面覆盖万人活动，却让受力方向变成内部经验；静冈新闻广播中心则把可生长的核心筒变成紧凑城市中的垂直基础设施。\n\n东京圣玛利亚大教堂以折板屋面把光、仪式与聚集压缩进一个上升的剖面；仓敷市政厅让厚重构架处理行政秩序与市民尺度；东京都厅舍则把巨大公共机构拆解成可辨认的城市地标。\n\n可迁移的方法是：先确定公共行为需要被覆盖、连接或纪念什么；再选择一种清晰的结构逻辑承受它；最后用路径、视线与入口防止“大尺度”变成“无尺度”。本文为基于书籍与案例资料的编辑性阅读，不是原书逐字引语。",
    "tags": "#丹下健三 #KenzoTange #ArchitectureForTheWorld #结构设计 #公共建筑 #日本建筑 #建筑书单 #设计方法",
}
CASES = [
    ("1955", "广岛和平纪念资料馆｜全景", "纪念性，先让空间保持距离", "架空体量、轴线与公园共同组织观看。建筑不以封闭纪念碑占满场地，而是把穿行、停留和望向遗址的距离留给市民。", "02-hiroshima-wide.jpg", (0.50, 0.50)),
    ("1955", "广岛和平纪念资料馆｜透视", "结构抬起地面，公共性才有入口", "柱列将展馆抬离地面，底层成为连续的阴影与通行层。承重逻辑同时决定了纪念建筑面对城市的开放方式。", "03-hiroshima-perspective.jpg", (0.50, 0.47)),
    ("1964", "代代木国立体育馆｜外观", "大跨度，不必变成笨重的盒子", "悬索屋面由两座主塔牵引，屋顶的下垂与上扬直接显露受力方向。体量因此像被拉开的公共帐篷，而非封闭容器。", "04-yoyogi-exterior.jpg", (0.50, 0.50)),
    ("1964", "代代木国立体育馆｜室内", "看得见的受力，让人读懂集体尺度", "吊索、屋面和看台围绕中央活动场展开。结构不是背景，它让观众知道这片大空间如何被共同支撑。", "05-yoyogi-interior.jpg", (0.50, 0.51)),
    ("1967", "静冈新闻广播中心", "核心筒不是电梯井，而是生长的接口", "服务核心承受主要荷载，办公单元向外悬挑。小基地上的垂直组织被清晰分层，也为未来增添单元留下想象。", "06-shizuoka.jpg", (0.50, 0.48)),
    ("1964", "东京圣玛利亚大教堂", "剖面把光与仪式一起拉高", "折板屋面从低处向十字形高处汇聚。光线沿结构缝进入，行进、仰望与集体礼仪都在同一个剖面中被强化。", "07-st-marys.jpg", (0.50, 0.48)),
    ("1960", "仓敷市政厅", "行政建筑，也要给街道留下尺度", "粗壮构架表达公共机构的稳定，同时用入口、窗洞和架空层拆开巨大的体量。秩序不等于把市民拒在立面之外。", "08-kurashiki.jpg", (0.50, 0.49)),
    ("1991", "东京都厅舍", "地标不是高度，而是复杂系统的可读性", "双塔、公共广场与交通节点共同承担大都会行政系统。高层机构被拆成可识别的城市构件，尺度才有被进入的可能。", "09-tokyo-metropolitan.jpg", (0.50, 0.49)),
]

def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0, optimize=True)

def cable(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color, width=8, invert=False) -> None:
    x0, y0, x1, y1 = box
    points = []
    for i in range(81):
        t = i / 80
        x = x0 + (x1 - x0) * t
        dy = (4 * t * (1 - t)) * (y1 - y0)
        y = y0 + dy if not invert else y1 - dy
        points.append((int(x), int(y)))
    draw.line(points, fill=color, width=width, joint="curve")

def cover_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 186), fill=P["red"])
    draw.text((68, 58), "PUBLIC SCALE / 01", font=base.get_font(25, bold=True), fill=P["white"])
    draw.text((782, 58), "KENZŌ TANGE", font=base.get_font(30, bold=True), fill=P["white"])
    # Sloping structural field: intentionally unlike the prior concentric-cover layout.
    cable(draw, (56, 375, 1172, 1060), P["blue"], 10)
    cable(draw, (128, 470, 1118, 1180), P["sand"], 7, invert=True)
    for x in (156, 383, 609, 835, 1062):
        draw.line((x, 348, x, 1195), fill=P["sand"], width=3)
    y = base.text_block(draw, (68, 244), BOOK["question"], base.get_font(67, bold=True), P["ink"], 700, 4)
    base.text_block(draw, (72, y + 28), BOOK["thesis"], base.get_font(30), P["muted"], 530, 13)
    cover = Image.open(ASSETS / "cover.png").convert("RGB")
    base.paste_cover(image, cover, (528, 498, 1144, 1040), shadow=True)
    draw.rounded_rectangle((66, 1210, 1177, 1431), radius=14, fill=P["dark"])
    draw.text((100, 1250), "KENZŌ TANGE · ARCHITECTURE FOR THE WORLD", font=base.get_font(27, bold=True), fill=P["sand"])
    base.text_block(draw, (100, 1304), BOOK["edition"], base.get_font(25), P["white"], 940, 10)
    draw.text((72, 1510), "结构 / 集体 / 城市", font=base.get_font(31, bold=True), fill=P["red"])
    base.draw_page_mark(draw, 1, P["ink"])
    return image

def photo_panel(source: Image.Image, size: tuple[int, int], focus) -> Image.Image:
    source = ImageEnhance.Contrast(source.convert("RGB")).enhance(1.04)
    source = ImageEnhance.Color(source).enhance(0.92)
    return ImageOps.fit(source, size, Image.Resampling.LANCZOS, centering=focus)

def case_card(case, page: int) -> Image.Image:
    year, title, headline, body, asset, focus = case
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    photo_top = page % 2 == 0
    ph = 840
    py = 0 if photo_top else H - ph
    image.paste(photo_panel(Image.open(ASSETS / asset), (W, ph), focus), (0, py))
    draw.rectangle((0, py + (ph - 22 if photo_top else 0), W, py + (ph if photo_top else 22)), fill=P["red"])
    ty = 908 if photo_top else 74
    draw.text((70, ty), year, font=base.get_font(29, bold=True), fill=P["red"])
    draw.text((206, ty + 3), title, font=base.get_font(30, bold=True), fill=P["blue"])
    y = base.text_block(draw, (68, ty + 65), headline, base.get_font(52, bold=True), P["ink"], 1020, 4)
    base.text_block(draw, (68, y + 22), body, base.get_font(29), P["ink"], 995, 13)
    # The line translates load direction; it stays in the text field, never over photos.
    x = 1130 if photo_top else 82
    draw.line((x, ty - 8, x, ty + 555), fill=P["blue"], width=7)
    for yy in (ty + 20, ty + 270, ty + 523):
        draw.ellipse((x - 10, yy - 10, x + 10, yy + 10), fill=P["red"])
    tag_y = py + (ph - 58 if photo_top else 57)
    draw.rounded_rectangle((58, tag_y - 26, 350, tag_y + 18), radius=22, fill=P["dark"])
    draw.text((80, tag_y - 18), "真实建筑项目照片", font=base.get_font(19, bold=True), fill=P["white"])
    base.draw_page_mark(draw, page, P["ink"], light=not photo_top)
    return image

def summary_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["dark"])
    draw = ImageDraw.Draw(image)
    draw.text((68, 60), "10 / FROM LOAD TO PUBLIC LIFE", font=base.get_font(24, bold=True), fill=P["sand"])
    y = base.text_block(draw, (68, 120), "结构先承受，\n公共性才有尺度", base.get_font(67, bold=True), P["white"], 1020, 5)
    base.text_block(draw, (72, y + 22), "丹下健三的关键不是放大体量，而是让受力逻辑持续校准进入、观看与聚集", base.get_font(29), P["sand"], 980, 12)
    # Three stacked civic decks, unlike the previous set's linked icon row.
    decks = [(550, P["red"], "01  覆盖", "先确定要被共同保护的活动、记忆或天气。"), (775, P["blue"], "02  承受", "用一种明确结构承受跨度，并让受力方向可见。"), (1000, P["sand"], "03  进入", "以入口、路径与视线拆解巨型尺度，留下人的位置。")]
    for i, (yy, color, head, body) in enumerate(decks):
        skew = 65 if i == 1 else 0
        points = [(68 + skew, yy), (1128, yy), (1070 - skew, yy + 168), (68, yy + 168)]
        draw.polygon(points, fill=color)
        fill = P["white"] if i != 2 else P["ink"]
        draw.text((104 + skew, yy + 33), head, font=base.get_font(34, bold=True), fill=fill)
        base.text_block(draw, (398 + skew, yy + 34), body, base.get_font(27), fill, 630, 10)
    cable(draw, (84, 1306, 1150, 1500), P["red"], 8)
    draw.text((68, 1530), "基于书籍与八张真实项目照片的编辑性总结", font=base.get_font(21), fill=(159, 166, 166))
    base.draw_page_mark(draw, 10, P["white"], light=True)
    return image

def preview(paths: list[Path]) -> None:
    canvas = Image.new("RGB", (1242, 654), P["dark"])
    for i, path in enumerate(paths):
        thumb = ImageOps.fit(Image.open(path).convert("RGB"), (210, 280), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (24 + (i % 5) * 234, 24 + (i // 5) * 304))
    save(canvas, OUTPUT / "preview.jpg")

def docs(paths: list[Path]) -> None:
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    copy = f"{BOOK['publish_title']}\n\n{BOOK['publish_body']}\n\n{BOOK['tags']}\n"
    (OUTPUT / "发布文案.md").write_text(copy, encoding="utf-8")
    lines = ["# 图片来源", "", "本套共 10 张：01 为问题封面，02–09 为八张真实项目照片，10 为编辑性总结。", "书封使用 Lars Müller Publishers 对应版本图，等比缩放；建筑图片均为真实照片，未使用 AI 生成图片。", ""]
    for item in manifest:
        lines += [f"## {item['filename']}｜{item['content']}", "", f"- 作者/机构：{item['credit']}", f"- 来源：{item['source_url']}", f"- 授权：{item['license']}", f"- 处理：{item['modifications']}", ""]
    (OUTPUT / "图片来源.md").write_text("\n".join(lines), encoding="utf-8")
    post = {"title": BOOK["publish_title"], "book": BOOK["book"], "edition": BOOK["edition"], "card_count": 10, "dimensions": [W, H], "format": "JPEG RGB quality 95", "visual_system": "suspension-span: structural cables and civic decks", "cover_policy": "publisher-verified cover, proportional scaling only, no redraw", "cards": [{"page": 1, "file": "01.jpg", "role": "question_cover", "layout": "sloped structural field with large verified landscape cover"}, *[{"page": i + 2, "file": f"{i + 2:02d}.jpg", "role": "real_case_evidence", "project": c[1], "year": c[0], "image": c[4]} for i, c in enumerate(CASES)], {"page": 10, "file": "10.jpg", "role": "synthesis", "layout": "three stacked civic decks"}], "copy": copy, "source_manifest": str((ASSETS / "manifest.json").relative_to(ROOT))}
    (OUTPUT / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")

def validate(paths: list[Path]) -> None:
    cards = []
    for path in paths:
        with Image.open(path) as image:
            rgb = image.convert("RGB")
            cards.append({"file": path.name, "size": list(rgb.size), "mode": rgb.mode, "nonblank": any(a != b for a, b in rgb.getextrema())})
    required = all((OUTPUT / name).exists() for name in ("preview.jpg", "发布文案.md", "图片来源.md", "post.json"))
    report = {"pass": len(paths) == 10 and required and len(BOOK["publish_title"]) <= 20 and all(c["size"] == [W, H] and c["mode"] == "RGB" and c["nonblank"] for c in cards), "title_length": len(BOOK["publish_title"]), "body_length": len(BOOK["publish_body"].replace("\n", "")), "required_files": required, "cards": cards}
    (OUTPUT / "qa-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    images = [cover_card(), *[case_card(case, i + 2) for i, case in enumerate(CASES)], summary_card()]
    paths = []
    for i, image in enumerate(images, 1):
        path = OUTPUT / f"{i:02d}.jpg"
        save(image, path)
        paths.append(path)
    preview(paths); docs(paths); validate(paths)

if __name__ == "__main__":
    main()
