#!/usr/bin/env python3
"""Render a ten-card Xiaohongshu post for Conversations with I. M. Pei."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "im-pei-conversations-light-is-key"
OUTPUT = ROOT / "output" / "im-pei-conversations-light-is-key"
W, H = 1242, 1660

P = {
    "paper": (239, 235, 222),
    "ink": (11, 24, 38),
    "navy": (15, 43, 65),
    "blue": (67, 116, 145),
    "gold": (228, 178, 78),
    "red": (176, 64, 47),
    "white": (249, 247, 239),
    "muted": (103, 111, 111),
}

BOOK = {
    "designer": "贝聿铭",
    "designer_en": "I. M. PEI",
    "book": "Conversations With I. M. Pei: Light Is the Key",
    "book_cn": "《与贝聿铭对话：光是钥匙》",
    "edition": "Gero von Boehm 著｜Prestel, 2000｜ISBN 9783791321769",
    "question": "光，为什么是建筑的钥匙？",
    "thesis": "光不是最后添加的气氛；它把结构、路径、材料与场所组织成同一个判断。",
    "publish_title": "贝聿铭：光为什么是钥匙？",
    "publish_body": (
        "《Conversations With I. M. Pei: Light Is the Key》以访谈进入贝聿铭的工作判断：光不是完成造型后添加的气氛，而是结构、路径、材料与场所能否协调的共同尺度。\n\n"
        "路思义教堂让弯曲结构同时引导光线；NCAR 用体量缝隙把山地、入口与行走连起来；美国国家美术馆东馆借三角几何分配展厅、方向和天光；卢浮宫金字塔以透明入口把自然光带入地下大厅。\n\n"
        "香港中银大厦让斜撑既承担受力，也成为捕捉天空的城市图像；美秀美术馆用隧道后的明亮抵达制造时间感；苏州博物馆以深檐、白墙和取景窗口重新校准江南光线；多哈伊斯兰艺术博物馆则用厚墙、拱廊与阴影回应强烈日照。\n\n"
        "对设计师更实用的方法是：先画一天内光的方向，再决定入口与主要路径；让结构节点同时承担采光、遮阳或反射；用明暗转换设计抵达，而不是只追求通透。\n\n"
        "本文为基于书籍与案例资料的编辑性阅读，不是原书逐字引语。"
    ),
    "tags": "#贝聿铭 #IMPei #LightIsTheKey #建筑光影 #博物馆建筑 #建筑理论 #建筑书单 #设计方法",
}

CASES = [
    {
        "number": "1963",
        "title": "路思义教堂",
        "meta": "台中｜陈其宽、贝聿铭",
        "headline": "结构弯曲，光才获得方向",
        "body": "四片弯曲的钢筋混凝土面向屋脊汇拢，端部与接缝把光引入内部。结构和照明不是两层设计，而是同一个动作。",
        "asset": "02-luce-chapel.jpg",
        "focus": (0.50, 0.54),
    },
    {
        "number": "1967",
        "title": "美国国家大气研究中心",
        "meta": "科罗拉多｜Mesa Laboratory",
        "headline": "把体量切开，光会成为路径",
        "body": "阶梯状混凝土体量顺着台地展开，庭院、缝隙与阴影拆解巨大尺度，也让入口和行走方向被光线逐步说明。",
        "asset": "03-ncar.jpg",
        "focus": (0.48, 0.48),
    },
    {
        "number": "1978",
        "title": "美国国家美术馆东馆",
        "meta": "华盛顿｜East Building",
        "headline": "几何不是造型，而是分配光与方向",
        "body": "三角形基地被继续拆成展厅、流线与中庭；天窗把几何秩序变成可感知的方向，让参观者不靠标识也能判断位置。",
        "asset": "04-nga-east.jpg",
        "focus": (0.52, 0.47),
    },
    {
        "number": "1989",
        "title": "卢浮宫金字塔",
        "meta": "巴黎｜拿破仑庭院",
        "headline": "透明入口，让新旧同时被看见",
        "body": "玻璃金字塔把日光带入地下大厅，并用清晰的中心入口重新组织庞杂流线；新结构存在，却没有遮蔽宫殿轴线。",
        "asset": "05-louvre.jpg",
        "focus": (0.50, 0.50),
        "panorama": True,
    },
    {
        "number": "1990",
        "title": "香港中银大厦",
        "meta": "香港｜Bank of China Tower",
        "headline": "斜撑把受力变成城市图像",
        "body": "对角结构传递荷载，也把玻璃立面切成捕捉天空的明暗片段。工程逻辑、光的反射与城市轮廓在同一张图里完成。",
        "asset": "06-bank-china.jpg",
        "focus": (0.50, 0.47),
    },
    {
        "number": "1997",
        "title": "美秀美术馆",
        "meta": "滋贺｜MIHO MUSEUM",
        "headline": "先穿过黑暗，光才有抵达感",
        "body": "隧道与桥延长进入过程，主厅的格栅屋顶再把强光过滤成柔和背景。明暗转换让到达成为一段时间，而非一个门口。",
        "asset": "07-miho.jpg",
        "focus": (0.50, 0.42),
    },
    {
        "number": "2006",
        "title": "苏州博物馆",
        "meta": "苏州｜Suzhou Museum",
        "headline": "借来的不是形式，而是光的分寸",
        "body": "深檐、白墙、灰黑屋面与取景窗口重新组织庭院。现代结构没有复制传统样式，而是延续江南空间对明暗和远近的控制。",
        "asset": "08-suzhou.jpg",
        "focus": (0.50, 0.48),
    },
    {
        "number": "2008",
        "title": "多哈伊斯兰艺术博物馆",
        "meta": "多哈｜Museum of Islamic Art",
        "headline": "厚重体量，也能把光切成层次",
        "body": "石材体量、深窗与连续拱廊压低强烈日照，并把海湾景色框成明亮终点。阴影在这里不是缺光，而是光的尺度。",
        "asset": "09-mia-doha.jpg",
        "focus": (0.50, 0.45),
    },
]


def add_noise(image: Image.Image, strength: int = 3) -> Image.Image:
    """Add a very subtle deterministic paper grain."""
    px = image.load()
    for y in range(0, H, 3):
        for x in range(0, W, 3):
            delta = ((x * 13 + y * 7) % (strength * 2 + 1)) - strength
            old = px[x, y]
            px[x, y] = tuple(max(0, min(255, c + delta)) for c in old)
    return image


def photo_panel(source: Image.Image, size: tuple[int, int], focus=(0.5, 0.5), panorama=False) -> Image.Image:
    source = ImageEnhance.Contrast(source.convert("RGB")).enhance(1.03)
    source = ImageEnhance.Color(source).enhance(0.94)
    if panorama:
        panel = Image.new("RGB", size, P["ink"])
        fitted = ImageOps.contain(source, size, Image.Resampling.LANCZOS)
        y = (size[1] - fitted.height) // 2
        panel.paste(fitted, ((size[0] - fitted.width) // 2, y))
        return panel
    return ImageOps.fit(source, size, Image.Resampling.LANCZOS, centering=focus)


def cover_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["ink"])
    draw = ImageDraw.Draw(image)

    # A diagonal beam, structurally unique to this set.
    draw.polygon([(0, 270), (0, 610), (1242, 1200), (1242, 790)], fill=P["gold"])
    draw.polygon([(0, 610), (0, 690), (1242, 1265), (1242, 1200)], fill=P["red"])
    draw.line((66, 170, 1100, 1530), fill=P["blue"], width=3)
    for offset in (0, 46, 92):
        draw.line((82 + offset, 1010, 390 + offset, 1515), fill=P["white"], width=2)

    draw.text((78, 75), "ARCHITECTURE · CONVERSATION", font=base.get_font(24, bold=True), fill=P["blue"])
    draw.text((80, 135), BOOK["designer_en"], font=base.get_font(36, bold=True), fill=P["white"])

    # Large, accurate, unmodified cover: about 37% of the canvas area visually.
    cover = Image.open(ASSETS / "cover.jpg").convert("RGB")
    base.paste_cover(image, cover, (655, 155, 1160, 895), shadow=True)

    draw.rounded_rectangle((56, 785, 690, 1390), radius=8, fill=P["ink"], outline=P["gold"], width=3)
    draw.text((82, 830), "LIGHT IS THE KEY", font=base.get_font(26, bold=True), fill=P["gold"])
    y = base.text_block(draw, (78, 900), "光，为什么是\n建筑的钥匙？", base.get_font(72, bold=True), P["white"], 560, 5)
    base.text_block(draw, (82, y + 38), BOOK["thesis"], base.get_font(30), P["white"], 540, 12)

    draw.text((710, 1325), BOOK["book_cn"], font=base.get_font(29, bold=True), fill=P["white"])
    draw.text((710, 1380), "真实书封 · Prestel 2000", font=base.get_font(22), fill=P["blue"])
    base.draw_page_mark(draw, 1, P["ink"], light=True)
    return image


def case_card(case: dict, page: int) -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    even = page % 2 == 0

    if even:
        photo_y, photo_h = 0, 825
        text_y = 890
    else:
        photo_y, photo_h = 835, 825
        text_y = 95

    source = Image.open(ASSETS / case["asset"]).convert("RGB")
    panel = photo_panel(source, (W, photo_h), case.get("focus", (0.5, 0.5)), case.get("panorama", False))
    image.paste(panel, (0, photo_y))

    # Photo and typography remain separate; the thin beam only marks chronology.
    boundary = photo_y + photo_h if even else photo_y
    draw.rectangle((0, boundary - 9, W, boundary + 9), fill=P["gold"])
    beam_x = 70 if even else 1030
    draw.rectangle((beam_x, text_y - 20, beam_x + 18, text_y + 550), fill=P["gold"])

    tx = 118 if even else 82
    width = 980 if even else 895
    draw.text((tx, text_y), case["number"], font=base.get_font(30, bold=True), fill=P["red"])
    draw.text((tx + 155, text_y + 2), case["meta"], font=base.get_font(24), fill=P["muted"])
    draw.text((tx, text_y + 65), case["title"], font=base.get_font(40, bold=True), fill=P["navy"])
    y = base.text_block(draw, (tx, text_y + 145), case["headline"], base.get_font(56, bold=True), P["ink"], width, 6)
    base.text_block(draw, (tx, y + 34), case["body"], base.get_font(31), P["ink"], width - 50, 14)

    if case.get("panorama"):
        # Keep the full 1920×716 panorama visible and label the deliberate letterbox.
        draw.text((890, photo_y + photo_h - 45), "完整宽幅实景", font=base.get_font(19), fill=P["white"])

    base.draw_page_mark(draw, page, P["ink"], light=not even)
    return image


def summary_card() -> Image.Image:
    image = Image.new("RGB", (W, H), P["paper"])
    draw = ImageDraw.Draw(image)
    cx, cy = 621, 690

    draw.text((72, 70), "LIGHT AS A COMMON MEASURE", font=base.get_font(25, bold=True), fill=P["red"])
    y = base.text_block(draw, (72, 132), "光不是装饰，\n而是共同尺度", base.get_font(66, bold=True), P["ink"], 820, 4)
    base.text_block(draw, (76, y + 22), "结构、路径、材料与场所，最终都要在光里接受检验。", base.get_font(29), P["navy"], 850, 12)

    # A radial light compass: different from the diagonal cover and past stacked summaries.
    for radius, color, width in [(315, P["blue"], 3), (238, P["gold"], 5), (146, P["red"], 3)]:
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=color, width=width)

    concepts = ["方向", "路径", "结构", "材料", "场所", "时间"]
    for i, label in enumerate(concepts):
        angle = math.radians(-90 + i * 60)
        ex, ey = cx + math.cos(angle) * 325, cy + math.sin(angle) * 325
        draw.line((cx, cy, ex, ey), fill=P["blue"], width=3)
        bx, by = int(ex - 53), int(ey - 28)
        draw.rounded_rectangle((bx, by, bx + 106, by + 56), radius=28, fill=P["ink"])
        draw.text((bx + 19, by + 10), label, font=base.get_font(25, bold=True), fill=P["white"])

    draw.ellipse((cx - 105, cy - 105, cx + 105, cy + 105), fill=P["gold"])
    draw.text((cx - 62, cy - 44), "光", font=base.get_font(86, bold=True), fill=P["ink"])

    methods = [
        ("01", "先画一天内光的方向，\n再决定入口与主要路径"),
        ("02", "让结构节点同时承担\n采光、遮阳或反射"),
        ("03", "用明暗转换设计抵达，\n而不是只追求通透"),
    ]
    y0 = 1110
    for i, (num, text) in enumerate(methods):
        x = 66 + i * 392
        draw.rounded_rectangle((x, y0, x + 350, 1462), radius=10, fill=P["ink"] if i == 1 else P["navy"])
        draw.text((x + 26, y0 + 28), num, font=base.get_font(27, bold=True), fill=P["gold"])
        base.text_block(draw, (x + 26, y0 + 95), text, base.get_font(29, bold=True), P["white"], 292, 13)

    draw.text((70, 1525), "基于书籍与八个案例的编辑性总结", font=base.get_font(22), fill=P["muted"])
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
        x = 24 + col * (thumb_w + gap)
        y = 24 + row * (thumb_h + gap)
        canvas.paste(thumb, (x, y))
    save_jpg(canvas, OUTPUT / "preview.jpg")


def write_docs(card_paths: list[Path]) -> None:
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))

    publish = f"{BOOK['publish_title']}\n\n{BOOK['publish_body']}\n\n{BOOK['tags']}\n"
    (OUTPUT / "发布文案.md").write_text(publish, encoding="utf-8")

    source_lines = [
        "# 图片来源",
        "",
        "本套共 10 张：01 为问题封面，02–09 为八个真实建筑案例，10 为编辑性总结。",
        "路思义教堂为陈其宽与贝聿铭共同设计，卡片中已明确署名。",
        "书封保持原始封面内容，仅等比缩放并置于版面；建筑图均为对应项目的真实照片。",
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
        "visual_system": "light-cut cover + alternating case chronology + radial light compass",
        "cover_policy": "verified Open Library cover, proportional scaling only, no redraw",
        "cards": [
            {"page": 1, "file": card_paths[0].name, "role": "question_cover", "layout": "diagonal light cut with large verified cover"},
            *[
                {
                    "page": i + 2,
                    "file": card_paths[i + 1].name,
                    "role": "real_case_evidence",
                    "project": case["title"],
                    "year": case["number"],
                    "image": case["asset"],
                }
                for i, case in enumerate(CASES)
            ],
            {"page": 10, "file": card_paths[9].name, "role": "synthesis", "layout": "radial light compass"},
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
    result = {
        "pass": len(paths) == 10
        and all(x["size"] == [W, H] and x["mode"] == "RGB" and x["nonblank"] for x in checks)
        and len(BOOK["publish_title"]) <= 20,
        "title_length": len(BOOK["publish_title"]),
        "cards": checks,
        "required_files": all((OUTPUT / n).exists() for n in ("preview.jpg", "发布文案.md", "图片来源.md", "post.json")),
    }
    (OUTPUT / "qa-report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    images = [cover_card()]
    images.extend(case_card(case, i + 2) for i, case in enumerate(CASES))
    images.append(summary_card())

    paths = []
    for i, image in enumerate(images, start=1):
        path = OUTPUT / f"{i:02d}.jpg"
        save_jpg(image, path)
        paths.append(path)
    make_preview(paths)
    write_docs(paths)
    result = validate(paths)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
