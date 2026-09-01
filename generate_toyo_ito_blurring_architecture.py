#!/usr/bin/env python3
"""Render a ten-card Xiaohongshu post for Toyo Ito's Blurring Architecture."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "toyo-ito-blurring-architecture"
OUTPUT = ROOT / "output" / "toyo-ito-blurring-architecture"
W, H = 1242, 1660
P = {
    "ink": (12, 19, 35), "night": (18, 37, 68), "paper": (241, 244, 240),
    "mist": (203, 222, 220), "cyan": (51, 211, 208), "violet": (129, 102, 210),
    "coral": (238, 106, 86), "white": (253, 254, 251), "muted": (89, 112, 126),
}
BOOK = {
    "designer": "伊东丰雄", "designer_en": "TOYO ITO", "book": "Toyo Ito: Blurring Architecture 1971–2005",
    "book_cn": "《模糊的建筑》", "edition": "Charta, 1999｜英德双语｜ISBN 9788881582310",
    "question": "墙，为什么\n不必是边界？",
    "thesis": "建筑不必用厚重边界分开内外；结构、媒介与光可以把空间变成连续的环境。",
    "publish_title": "伊东丰雄：墙为何不必是边界？",
    "publish_body": "《Blurring Architecture》收录伊东丰雄 1971—2005 年的展览与项目资料。它关心的不是把建筑做得更像流线形，而是如何让墙、楼板、结构和媒介不再各自封闭，把人、城市信息与自然条件接进同一套空间。\n\n仙台媒体中心以楼板和十三束不规则管状构件组织图书、展览与信息；横滨风之塔让通风设施在夜间成为接收城市信号的媒介；TOD’S 表参道大楼将树枝般的混凝土骨架推到外立面；Mikimoto 银座 2 则用不规则开口松动完整盒子。\n\n蛇形画廊展亭把网格同时变成结构与透视；多摩美术大学图书馆以连续拱廊串联地形、入口、书架和停留。边界变薄，并不等于取消秩序；相反，结构、洞口与路径要更精确地安排。\n\n对设计师可直接采用的顺序是：先列出真正需要连通的环境因素，再把承重、采光、设备或交通中的一种推到空间表面，最后用开口和路径校准停留的尺度。本文为基于书籍与案例资料的编辑性阅读，不是原书逐字引语。",
    "tags": "#伊东丰雄 #BlurringArchitecture #仙台媒体中心 #建筑表皮 #空间边界 #建筑理论 #建筑书单 #设计方法",
}
CASES = [
    ("2001", "仙台媒体中心｜外观", "楼板与管束，先成为城市立面", "七层平台被十三束不规则管状构件贯穿；它们同时承担结构、交通与服务，让玻璃外壳之后仍能读到空间正在流动。", "02-sendai-exterior.jpg", (0.50, 0.48)),
    ("2001", "仙台媒体中心｜室内", "开放，不等于没有方向", "管束在室内形成不同密度的光、视线与停留点。图书、展览和活动可共享楼层，但身体始终能借构件找到位置。", "03-sendai-interior.jpg", (0.48, 0.50)),
    ("1986", "横滨风之塔", "基础设施，也能读取城市的变化", "这座车站通风塔在夜间以光回应周围的声响、风与交通信息。设备没有被藏起，而被转译成可感知的公共界面。", "04-tower-of-winds.jpg", (0.50, 0.46)),
    ("2004", "TOD’S 表参道大楼", "把结构推到皮肤上，墙才会变薄", "树枝般的混凝土框架直接构成表皮。承重、开口与街道识别被合并，立面不再是一层独立的装饰幕布。", "05-tods.jpg", (0.50, 0.49)),
    ("2005", "Mikimoto 银座 2", "洞口不是减法，而是松动体量的工具", "不规则开口切入窄而高的白色体量，窗洞不服从整齐楼层节奏。完整盒子由此变成透光、可呼吸的城市表面。", "06-mikimoto.jpg", (0.50, 0.48)),
    ("2002", "蛇形画廊展亭", "网格既是结构，也是被身体穿过的视线", "旋转与扩张的方格生成轻质立体网。边界由单一道墙变成层层叠加的框景、阴影与行走体验。", "07-serpentine.jpg", (0.50, 0.50)),
    ("2007", "多摩美术大学图书馆｜外观", "把地形延续成可进入的立面", "连续拱廊沿坡地展开，入口并非一刀切开的门洞；行走、驻足和望向校园的视线先于封闭的建筑轮廓出现。", "08-tama-exterior.jpg", (0.50, 0.52)),
    ("2007", "多摩美术大学图书馆｜室内", "重复构件，通过差异制造空间深度", "薄钢板拱条在不同跨度中重复，串起书架、桌面与视线。规律没有消失，只是不再把使用切成僵硬的房间。", "09-tama-interior.jpg", (0.50, 0.50)),
]


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0, optimize=True)


def dots(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, step: int, alpha: int = 0) -> None:
    color = (80, 130, 151) if alpha == 0 else (38, 76, 101)
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=color)


def cover_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["night"])
    draw = ImageDraw.Draw(image)
    dots(draw, 46, 38, W - 45, H - 45, 46, 1)
    # Diaphragm rings frame, never alter, the accurate cover.
    for r in range(430, 94, -47):
        color = P["cyan"] if r % 94 else P["violet"]
        draw.rounded_rectangle((653 - r, 829 - r * 0.63, 653 + r, 829 + r * 0.63), radius=76, outline=color, width=3)
    draw.text((70, 70), "BOOK NOTE / 01", font=base.get_font(24, bold=True), fill=P["cyan"])
    draw.text((70, 115), BOOK["designer_en"], font=base.get_font(44, bold=True), fill=P["white"])
    y = base.text_block(draw, (68, 214), BOOK["question"], base.get_font(78, bold=True), P["white"], 500, 5)
    draw.rectangle((72, y + 34, 304, y + 42), fill=P["coral"])
    base.text_block(draw, (72, y + 77), BOOK["thesis"], base.get_font(30), P["mist"], 440, 14)
    cover = Image.open(ASSETS / "cover.jpg").convert("RGB")
    base.paste_cover(image, cover, (492, 351, 1085, 1286), shadow=True)
    draw.rounded_rectangle((68, 1310, 925, 1491), radius=16, fill=(8, 18, 33))
    draw.text((98, 1344), "TOYO ITO · BLURRING ARCHITECTURE", font=base.get_font(25, bold=True), fill=P["cyan"])
    base.text_block(draw, (98, 1394), BOOK["edition"], base.get_font(25), P["white"], 760, 10)
    draw.text((1010, 1445), "墙 = 环境？", font=base.get_font(25, bold=True), fill=P["coral"])
    base.draw_page_mark(draw, 1, P["white"], light=True)
    return image


def photo_panel(photo: Image.Image, size: tuple[int, int], focus: tuple[float, float]) -> Image.Image:
    photo = ImageEnhance.Contrast(photo.convert("RGB")).enhance(1.035)
    photo = ImageEnhance.Color(photo).enhance(0.92)
    if min(photo.size) < 500:
        panel = Image.new("RGB", size, P["night"])
        fitted = ImageOps.contain(photo, (photo.width, photo.height), Image.Resampling.LANCZOS)
        panel.paste(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
        return panel
    return ImageOps.fit(photo, size, Image.Resampling.LANCZOS, centering=focus)


def case_card(case: tuple, page: int) -> Image.Image:
    year, title, headline, body, asset, focus = case
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    photo_top = page % 2 == 0
    panel_h = 870
    panel_y = 0 if photo_top else H - panel_h
    photo = photo_panel(Image.open(ASSETS / asset), (W, panel_h), focus)
    image.paste(photo, (0, panel_y))
    # A thin cyan diaphragm always marks the transition, while information moves by page.
    draw.rectangle((0, panel_y + (panel_h - 24 if photo_top else 0), W, panel_y + (panel_h if photo_top else 24)), fill=P["cyan"])
    draw.line((0, panel_y + (panel_h - 48 if photo_top else 48), W, panel_y + (panel_h - 48 if photo_top else 48)), fill=P["ink"], width=3)
    ty = 945 if photo_top else 74
    accent_x = 72 if photo_top else 1060
    draw.line((accent_x, ty - 8, accent_x, ty + 590), fill=P["violet"], width=8)
    for n in (ty + 38, ty + 274, ty + 530):
        draw.ellipse((accent_x - 9, n - 9, accent_x + 9, n + 9), fill=P["cyan"])
    tx = 112 if photo_top else 68
    width = 1000 if photo_top else 920
    draw.text((tx, ty), year, font=base.get_font(29, bold=True), fill=P["coral"])
    draw.text((tx + 148, ty + 4), title, font=base.get_font(31, bold=True), fill=P["night"])
    y = base.text_block(draw, (tx, ty + 72), headline, base.get_font(54, bold=True), P["ink"], width, 4)
    base.text_block(draw, (tx, y + 24), body, base.get_font(29), P["ink"], width, 13)
    label_y = panel_y + (74 if not photo_top else panel_h - 67)
    draw.rounded_rectangle((60, label_y, 364, label_y + 42), radius=21, fill=P["night"])
    draw.text((83, label_y + 8), "真实建筑项目照片", font=base.get_font(20, bold=True), fill=P["white"])
    base.draw_page_mark(draw, page, P["ink"], light=not photo_top)
    return image


def summary_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((68, 62), "10 / MAKE THE BOUNDARY WORK", font=base.get_font(24, bold=True), fill=P["cyan"])
    y = base.text_block(draw, (68, 123), "边界变薄，\n判断反而要更精确", base.get_font(65, bold=True), P["white"], 960, 5)
    base.text_block(draw, (72, y + 24), "不是取消墙，而是让结构、开口、路径和环境共同定义空间。", base.get_font(29), P["mist"], 960, 12)
    # A porous field, rather than the earlier transfer-station conclusion layout.
    cells = [(110, 562, 274, 720, "环境"), (344, 510, 546, 694, "结构"), (642, 600, 846, 790, "开口"), (918, 510, 1130, 700, "路径")]
    for i, (x0, y0, x1, y1, label) in enumerate(cells):
        color = [P["cyan"], P["violet"], P["coral"], P["mist"]][i]
        draw.rounded_rectangle((x0, y0, x1, y1), radius=50, outline=color, width=8)
        draw.ellipse((x0 + 45, y0 + 45, x0 + 107, y0 + 107), fill=color)
        draw.text((x0 + 40, y0 + 119), label, font=base.get_font(32, bold=True), fill=P["white"])
        if i < 3:
            draw.line((x1 + 10, (y0 + y1) // 2, cells[i + 1][0] - 10, (cells[i + 1][1] + cells[i + 1][3]) // 2), fill=P["white"], width=5)
    draw.text((68, 862), "从“围合”转向“调节”", font=base.get_font(48, bold=True), fill=P["cyan"])
    methods = [
        ("01", "先连环境", "把风、光、人流与信息列成同一张关系表。"),
        ("02", "再选载体", "挑一种构件承担连接：管束、网格、框架或拱。"),
        ("03", "最后校准停留", "用洞口、视线和路径检查人是否真的能停下来。"),
    ]
    for i, (n, head, body) in enumerate(methods):
        x = 66 + i * 390
        color = [P["cyan"], P["violet"], P["coral"]][i]
        draw.line((x, 1020, x + 330, 1020), fill=color, width=9)
        draw.text((x, 1055), n, font=base.get_font(26, bold=True), fill=color)
        draw.text((x, 1102), head, font=base.get_font(37, bold=True), fill=P["white"])
        base.text_block(draw, (x, 1160), body, base.get_font(27), P["mist"], 330, 12)
    draw.text((68, 1530), "基于书籍与八张真实项目照片的编辑性总结", font=base.get_font(21), fill=P["muted"])
    base.draw_page_mark(draw, 10, P["white"], light=True)
    return image


def preview(paths: list[Path]) -> None:
    canvas = Image.new("RGB", (1242, 654), P["ink"])
    for i, path in enumerate(paths):
        thumb = ImageOps.fit(Image.open(path).convert("RGB"), (210, 280), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (24 + (i % 5) * 234, 24 + (i // 5) * 304))
    save(canvas, OUTPUT / "preview.jpg")


def docs(paths: list[Path]) -> None:
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    copy = f"{BOOK['publish_title']}\n\n{BOOK['publish_body']}\n\n{BOOK['tags']}\n"
    (OUTPUT / "发布文案.md").write_text(copy, encoding="utf-8")
    lines = ["# 图片来源", "", "本套共 10 张：01 为问题封面，02–09 为八张真实项目照片，10 为编辑性总结。", "书封保持原始内容，仅等比缩放；建筑图片均为真实照片，未使用 AI 生成图片。", ""]
    for item in manifest:
        lines += [f"## {item['filename']}｜{item['content']}", "", f"- 作者/机构：{item['credit']}", f"- 来源：{item['source_url']}", f"- 授权：{item['license']}", f"- 处理：{item['modifications']}", ""]
    (OUTPUT / "图片来源.md").write_text("\n".join(lines), encoding="utf-8")
    post = {"title": BOOK["publish_title"], "book": BOOK["book"], "edition": BOOK["edition"], "card_count": 10, "dimensions": [W, H], "format": "JPEG RGB quality 95", "visual_system": "porous-skin: cover inside a diaphragm field; case evidence; porous-field conclusion", "cover_policy": "verified Open Library cover, proportional scaling only, no redraw", "cards": [{"page": 1, "file": "01.jpg", "role": "question_cover", "layout": "large centered verified cover inside concentric diaphragm"}, *[{"page": i + 2, "file": f"{i + 2:02d}.jpg", "role": "real_case_evidence", "project": c[1], "year": c[0], "image": c[4]} for i, c in enumerate(CASES)], {"page": 10, "file": "10.jpg", "role": "synthesis", "layout": "porous relationship field"}], "copy": copy, "source_manifest": str((ASSETS / "manifest.json").relative_to(ROOT))}
    (OUTPUT / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")


def validate(paths: list[Path]) -> None:
    cards = []
    for path in paths:
        with Image.open(path) as im:
            rgb = im.convert("RGB")
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
    preview(paths)
    docs(paths)
    validate(paths)


if __name__ == "__main__":
    main()
