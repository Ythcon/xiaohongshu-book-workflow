#!/usr/bin/env python3
"""Render ten Xiaohongshu cards for Ida van Zijl's Gerrit Rietveld."""
from __future__ import annotations
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import generate_three_unmentioned_masters as base

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "rietveld-furniture-to-architecture"
OUTPUT = ROOT / "output" / "rietveld-furniture-to-architecture"
W, H = 1242, 1660
P = {"paper": (247, 245, 238), "ink": (23, 25, 28), "red": (218, 48, 43), "blue": (0, 106, 178), "yellow": (247, 197, 55), "grey": (112, 114, 112), "white": (255, 255, 252)}
BOOK = {
    "designer": "赫里特·里特费尔德", "designer_en": "GERRIT RIETVELD",
    "book": "Gerrit Rietveld", "book_cn": "《Gerrit Rietveld》", "edition": "Ida van Zijl｜Phaidon｜ISBN 9780714873206",
    "question": "一把椅子，\n怎样推导出一座房子？",
    "thesis": "尺度、节点与色彩不是装饰；它们把坐、走、停留和视线组织成可以不断打开的空间。",
    "publish_title": "里特费尔德：家具如何变成建筑？",
    "publish_body": "《Gerrit Rietveld》值得重读的，不只是红蓝椅的配色，而是他如何从家具的尺度、构件与使用方式，推进到一座可以被重新组织的房子。对他而言，建筑不是被包起来的体量，更像一组让身体选择坐、走、转身和看出去的平面与节点。\n\n1924 年的施罗德住宅把窗、阳台、墙和楼梯拆成彼此错开的动作：外墙不必闭合成一个完整盒子，转角可以打开，室内也能通过可变隔断让生活在独处与共享之间切换。黑线负责定边界，红、蓝、黄只在关键处标记方向、重心和停留点。\n\n对设计师更实用的工作法是：先从一个具体动作开始，而不是先画整体形象；再让每一根线、每一块板只承担一种关系；最后检查这个节点是否同时改变了坐、走或看的方式。\n\n家具和建筑的距离，常常只差一次尺度的放大。方案卡住时，不妨先问：这个构件究竟让人怎样使用空间？本文为基于书籍与案例资料的编辑性阅读，不是原书逐字引语。",
    "tags": "#赫里特里特费尔德 #GerritRietveld #施罗德住宅 #DeStijl #建筑设计 #空间设计 #建筑书单 #设计方法",
}
CASES = [
    ("02-facade.jpg", "1924｜施罗德住宅", "不是盒子，\n而是一组可以错开的平面", "白墙、黑线与阳台不合成为一个封闭体量。每一块面都向外伸、向内退，先给出方向，房间才在它们之间出现。", "立面 / 关系先于体量", (0.50, 0.52)),
    ("03-side.jpg", "1924｜施罗德住宅", "色彩只在\n需要转向的地方出现", "红、蓝、黄并非给立面上色，而是让构件的前后、横竖和受力关系更容易被读到。颜色把视线推向下一块平面。", "颜色 / 标记空间重心", (0.48, 0.50)),
    ("04-stair.jpg", "1924｜施罗德住宅", "先画人的高度，\n再决定墙的高度", "楼梯把身体的上升、停顿和回望带进一个连续剖面。家具尺度的精确，在建筑里变成对步幅、扶手与视线高度的控制。", "尺度 / 从手到身体", (0.50, 0.50)),
    ("05-window.jpg", "1924｜施罗德住宅", "窗不是洞口，\n而是边界的开关", "开口的位置让室内与街道并非简单相望。它把墙、窗框与外部空间连成一套可调的界面，让看出去成为空间的一部分。", "开口 / 调整内外距离", (0.50, 0.44)),
    ("06-balcony.jpg", "1924｜施罗德住宅", "阳台把房间的边缘\n变成一次停留", "平面在阳台处向外延伸，生活不在门槛前结束。停留点让私密的室内与开放的城市之间，多出一段可以掌握的距离。", "停留 / 给边界加厚", (0.47, 0.50)),
    ("07-corner.jpg", "1924｜施罗德住宅", "转角不必用来封死，\n也可以把空间放出去", "悬挑、开窗和细柱使转角失去厚重的封闭感。边界被拆成轻而清晰的构件，室内外因而能够在同一节点彼此渗透。", "转角 / 释放两个方向", (0.50, 0.50)),
    ("08-opening.jpg", "1924｜施罗德住宅", "每一处开合，\n都在重排生活的关系", "构件不只定义形状，也定义谁能看见谁、哪里适合独处、何处可以共享。建筑的弹性来自这些关系可以被逐一调整。", "可变 / 让房间重新组合", (0.53, 0.50)),
]

def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0, optimize=True)

def photo(path: Path, size: tuple[int, int], focus: tuple[float, float]) -> Image.Image:
    im = Image.open(path).convert("RGB")
    im = ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.05)).enhance(0.90)
    return ImageOps.fit(im, size, Image.Resampling.LANCZOS, centering=focus)

def mark(d: ImageDraw.ImageDraw, page: int, light: bool = False) -> None:
    d.text((1060, 1578), f"{page:02d} / 10", font=base.get_font(18, bold=True), fill=P["paper"] if light else P["ink"])

def cropped_cover() -> Image.Image:
    # Official product image: only the surrounding white margin is trimmed.
    return Image.open(ASSETS / "cover.jpg").convert("RGB").crop((310, 150, 2530, 2780))

def cover_card() -> Image.Image:
    im = Image.new("RGB", (W, H), P["paper"]); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 92), fill=P["ink"])
    d.text((56, 29), "01 / SCALE INTO SPACE", font=base.get_font(22, bold=True), fill=P["white"])
    d.rectangle((66, 175, 500, 281), fill=P["red"])
    d.text((88, 195), "从椅子到房子", font=base.get_font(42, bold=True), fill=P["white"])
    d.rectangle((66, 307, 802, 442), fill=P["blue"])
    d.text((88, 330), "家具如何变成建筑？", font=base.get_font(58, bold=True), fill=P["white"])
    d.rectangle((66, 475, 332, 515), fill=P["yellow"])
    d.text((66, 545), BOOK["designer"], font=base.get_font(32, bold=True), fill=P["ink"])
    d.text((66, 592), "GERRIT RIETVELD / 1888–1964", font=base.get_font(20, bold=True), fill=P["grey"])
    y = base.text_block(d, (66, 690), BOOK["question"], base.get_font(53, bold=True), P["ink"], 510, 4)
    base.text_block(d, (66, y + 24), BOOK["thesis"], base.get_font(27), P["grey"], 488, 12)
    # A large verified cover, handled as a separate locked image object.
    book = ImageOps.contain(cropped_cover(), (590, 900), Image.Resampling.LANCZOS)
    bx, by = 588, 590
    im.paste(book, (bx, by))
    d.line((545, 573, 545, 1516), fill=P["ink"], width=9)
    d.rectangle((103, 1312, 507, 1397), fill=P["yellow"])
    d.text((126, 1332), "节点不是装饰", font=base.get_font(29, bold=True), fill=P["ink"])
    d.line((66, 1470, 510, 1470), fill=P["red"], width=16)
    d.text((66, 1514), BOOK["edition"], font=base.get_font(21), fill=P["ink"])
    mark(d, 1); return im

def mechanism_card() -> Image.Image:
    im = Image.new("RGB", (W, H), P["ink"]); d = ImageDraw.Draw(im)
    d.text((68, 70), "02 / READ THE HOUSE AS ACTIONS", font=base.get_font(22, bold=True), fill=P["yellow"])
    d.text((68, 142), "不是一栋房子，\n是四个动作", font=base.get_font(64, bold=True), fill=P["white"])
    steps = [("坐", "把尺度落到身体", P["yellow"]), ("走", "用线与墙安排方向", P["blue"]), ("开", "让边界可以调节", P["red"]), ("停", "把转角变成停留点", P["white"])]
    for i, (verb, desc, color) in enumerate(steps):
        x = 70 + (i % 2) * 570; y = 535 + (i // 2) * 350
        d.rectangle((x, y, x + 500, y + 278), fill=color)
        text_color = P["ink"] if color in (P["yellow"], P["white"]) else P["white"]
        d.text((x + 36, y + 34), f"0{i+1}", font=base.get_font(24, bold=True), fill=text_color)
        d.text((x + 36, y + 84), verb, font=base.get_font(88, bold=True), fill=text_color)
        d.text((x + 180, y + 160), desc, font=base.get_font(27, bold=True), fill=text_color)
    d.line((68, 1326, 1174, 1326), fill=P["white"], width=3)
    base.text_block(d, (68, 1370), "读里特费尔德时，先看构件怎样回应一个动作，再看这些动作如何拼成房间。", base.get_font(30), P["paper"], 690, 12)
    # The mechanism page retains one unaltered real project photograph as evidence.
    strip = photo(ASSETS / "09-open-corner.jpg", (350, 210), (0.50, 0.49))
    im.paste(strip, (824, 1340))
    d.rectangle((824, 1510, 1174, 1550), fill=P["red"])
    d.text((842, 1518), "施罗德住宅｜打开的转角", font=base.get_font(16, bold=True), fill=P["white"])
    mark(d, 2, True); return im

def case_card(case: tuple, page: int) -> Image.Image:
    asset, title, headline, body, tag, focus = case
    im = Image.new("RGB", (W, H), P["paper"]); d = ImageDraw.Draw(im)
    style = (page - 3) % 3
    if style == 0:
        im.paste(photo(ASSETS / asset, (W, 710), focus), (0, 0))
        d.rectangle((0, 710, W, H), fill=P["paper"])
        d.rectangle((68, 660, 434, 718), fill=P["red"])
        tx, ty, width = 68, 780, 1050
    elif style == 1:
        im.paste(photo(ASSETS / asset, (674, H), focus), (568, 0))
        d.rectangle((0, 0, 568, H), fill=P["blue"])
        d.rectangle((532, 0, 568, H), fill=P["yellow"])
        tx, ty, width = 66, 116, 430
    else:
        im.paste(photo(ASSETS / asset, (W, 820), focus), (0, 840))
        d.rectangle((0, 0, W, 840), fill=P["yellow"])
        d.rectangle((70, 736, 1060, 868), fill=P["ink"])
        tx, ty, width = 70, 92, 1010
    d.text((tx, ty), title, font=base.get_font(27, bold=True), fill=P["red"] if style != 1 else P["yellow"])
    y = base.text_block(d, (tx, ty + 58), headline, base.get_font(52, bold=True), P["ink"] if style != 1 else P["white"], width, 4)
    base.text_block(d, (tx, y + 25), body, base.get_font(27), P["grey"] if style != 1 else P["paper"], width, 12)
    if style == 0:
        d.rectangle((68, 1365, 638, 1424), fill=P["blue"]); d.text((91, 1380), tag, font=base.get_font(23, bold=True), fill=P["white"])
    elif style == 1:
        d.rectangle((66, 1376, 500, 1435), fill=P["red"]); d.text((89, 1391), tag, font=base.get_font(22, bold=True), fill=P["white"])
    else:
        d.text((74, 767), tag, font=base.get_font(25, bold=True), fill=P["white"])
    d.text((tx, 1510 if style != 2 else 1494), "RIETVELD SCHRÖDER HOUSE · UTRECHT", font=base.get_font(19, bold=True), fill=P["grey"] if style != 1 else P["white"])
    mark(d, page, light=style == 1); return im

def summary_card() -> Image.Image:
    im = Image.new("RGB", (W, H), P["paper"]); d = ImageDraw.Draw(im)
    d.text((68, 68), "10 / SCALE UP THE QUESTION", font=base.get_font(22, bold=True), fill=P["blue"])
    d.text((68, 142), "把家具的问题，\n放大成空间的问题", font=base.get_font(63, bold=True), fill=P["ink"])
    d.line((114, 570, 1040, 570), fill=P["ink"], width=10)
    nodes = [(154, 570, P["yellow"], "坐", "身体尺度"), (458, 570, P["blue"], "走", "方向关系"), (760, 570, P["red"], "开", "可变边界"), (1040, 570, P["ink"], "停", "共享节点")]
    for x, y, color, verb, note in nodes:
        d.ellipse((x - 72, y - 72, x + 72, y + 72), fill=color)
        d.text((x - 28, y - 31), verb, font=base.get_font(47, bold=True), fill=P["white"] if color in (P["blue"], P["red"], P["ink"]) else P["ink"])
        d.text((x - 55, y + 110), note, font=base.get_font(25, bold=True), fill=P["ink"])
    d.rectangle((68, 890, 1168, 1175), fill=P["ink"])
    base.text_block(d, (108, 938), "先问一个构件怎样改变使用；\n再问它是否也改变了下一步的视线、路径或停留。", base.get_font(40, bold=True), P["white"], 940, 8)
    notes = [("01", "先画动作", "先指定坐、走或看，再决定形式。"), ("02", "一件事一根线", "每个构件只承担清楚的空间关系。"), ("03", "让节点可用", "把转角、窗边和门槛变成停留点。")]
    for i, (number, head, body) in enumerate(notes):
        x = 68 + i * 373
        d.text((x, 1262), number, font=base.get_font(25, bold=True), fill=P["red"] if i == 1 else P["blue"])
        d.text((x, 1304), head, font=base.get_font(30, bold=True), fill=P["ink"])
        base.text_block(d, (x, 1354), body, base.get_font(23), P["grey"], 315, 10)
    d.text((68, 1534), "基于书籍与八张真实项目照片的编辑性总结", font=base.get_font(20), fill=P["grey"])
    mark(d, 10); return im

def preview(paths: list[Path]) -> None:
    canvas = Image.new("RGB", (1242, 654), P["ink"])
    for i, path in enumerate(paths):
        thumb = ImageOps.fit(Image.open(path).convert("RGB"), (210, 280), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (24 + (i % 5) * 234, 24 + (i // 5) * 304))
    save(canvas, OUTPUT / "preview.jpg")

def documents(paths: list[Path]) -> None:
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    copy = f"{BOOK['publish_title']}\n\n{BOOK['publish_body']}\n\n{BOOK['tags']}\n"
    (OUTPUT / "发布文案.md").write_text(copy, encoding="utf-8")
    lines = ["# 图片来源", "", "本套共 10 张：01 为问题封面，02 为阅读机制并使用一张真实项目照片，03–09 使用七张不同的施罗德住宅真实照片，10 为编辑性总结。", "书封为 Phaidon 官方产品图，只做外部留白裁切和等比缩放；项目图片均为真实照片，未使用 AI 生成图像。", ""]
    for item in manifest:
        lines += [f"## {item['filename']}｜{item['content']}", "", f"- 作者/机构：{item['credit']}", f"- 来源：{item['source_url']}", f"- 授权：{item['license']}", f"- 处理：{item['modifications']}", ""]
    (OUTPUT / "图片来源.md").write_text("\n".join(lines), encoding="utf-8")
    post = {"title": BOOK["publish_title"], "book": BOOK["book"], "edition": BOOK["edition"], "card_count": 10, "dimensions": [W, H], "format": "JPEG RGB quality 95", "visual_system": "moving-planes: body actions become planes, lines and open corners", "cover_policy": "publisher-verified official product cover; external margin crop and proportional scaling only", "cards": [{"page": 1, "file": "01.jpg", "role": "question_cover", "layout": "large verified cover intersecting coloured planes"}, {"page": 2, "file": "02.jpg", "role": "mechanism"}, *[{"page": i + 3, "file": f"{i+3:02d}.jpg", "role": "real_case_evidence", "project": "Rietveld Schröder House", "year": "1924", "image": c[0]} for i, c in enumerate(CASES)], {"page": 10, "file": "10.jpg", "role": "synthesis", "layout": "action path with spatial tests"}], "copy": copy, "source_manifest": str((ASSETS / "manifest.json").relative_to(ROOT))}
    (OUTPUT / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")

def validate(paths: list[Path]) -> None:
    cards = []
    for path in paths:
        with Image.open(path) as image:
            rgb = image.convert("RGB")
            cards.append({"file": path.name, "size": list(rgb.size), "mode": rgb.mode, "nonblank": any(lo != hi for lo, hi in rgb.getextrema())})
    required = all((OUTPUT / name).exists() for name in ("preview.jpg", "发布文案.md", "图片来源.md", "post.json"))
    report = {"pass": len(paths) == 10 and required and len(BOOK["publish_title"]) <= 20 and all(c["size"] == [W, H] and c["mode"] == "RGB" and c["nonblank"] for c in cards), "title_length": len(BOOK["publish_title"]), "body_length": len(BOOK["publish_body"].replace("\n", "")), "required_files": required, "cards": cards}
    (OUTPUT / "qa-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cards = [cover_card(), mechanism_card(), *[case_card(case, i + 3) for i, case in enumerate(CASES)], summary_card()]
    paths = []
    for i, image in enumerate(cards, 1):
        path = OUTPUT / f"{i:02d}.jpg"; save(image, path); paths.append(path)
    preview(paths); documents(paths); validate(paths)

if __name__ == "__main__":
    main()
