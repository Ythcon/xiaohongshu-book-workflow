#!/usr/bin/env python3
"""Render the third batch of three distinct architecture-book posts."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters-03"
OUTPUT_ROOT = ROOT / "output" / "three-unmentioned-masters-03"
W, H = base.W, base.H

BOOKS = {
    "herman-hertzberger-lessons-for-students": {
        "designer": "赫尔曼·赫兹伯格", "designer_en": "HERMAN HERTZBERGER",
        "book": "Lessons for Students in Architecture", "book_cn": "《给建筑学生的课》",
        "edition": "010 Publishers, 2005 reprint (first published 1991)｜Open Library OL4307478W",
        "question": "好建筑为什么要给人留余地？",
        "thesis": "建筑不应把使用方式全部写死，而要提供可占用的门槛、单元与共同空间。",
        "system": "threshold-cells",
        "palette": {"paper": "#ECE8DE", "ink": "#20272A", "accent": "#C94D36", "second": "#315F86", "warm": "#E0B84E"},
        "cards": [
            ("中央保险公司办公楼", "重复单元可以生成一座室内城市", "办公岛、街道和高差形成开放结构，使用者能在其中调整、停留和识别自己的位置。", "02-centraal-beheer.jpg"),
            ("Diagoon 住宅", "未完成的框架反而扩大居住自由", "建筑先提供结构与基本层级，房间边界和生活方式由住户继续定义。", "03-diagoon-houses.jpg"),
            ("De Drie Hoven", "住宅之间的空间同样需要被设计", "廊道、转角、庭院与共享节点把老年居住从孤立房间连接成邻里。", "04-drie-hoven.jpg"),
            ("Vredenburg 音乐中心", "公共性来自看见彼此的活动", "大厅、楼梯与观众席形成连续室内地形，让到达、等待和观看同时成为事件。", "05-vredenburg.jpg"),
        ],
        "summary": "真正开放的建筑不是没有秩序，而是秩序能被使用者解释、占用并继续完成。",
        "chain": ["结构", "门槛", "占用", "变化", "共同体"],
        "methods": ["把走廊转成可停留的门槛空间", "用明确骨架容纳多种房间划分", "让使用痕迹成为下一轮设计依据"],
        "endcards": {"01": {"layout_rationale": "以可被占用的方格单元构成封面，真实书封嵌入其中一个单元，问题标题跨越空白门槛。", "changed_variables": ["方格主视觉", "中央书封", "左下标题", "多方向留白"]}, "06": {"layout_rationale": "用单元从结构逐步扩展成共同体，三条方法放在被占用的边界，不使用普通列表。", "changed_variables": ["聚落式概念链", "尺度递增", "边界方法标注", "纯排版浅底"]}},
        "publish_title": "赫兹伯格：好建筑为什么要给人留余地？",
        "publish_body": "《Lessons for Students in Architecture》反复提醒设计师：空间一旦把使用方式规定得太完整，生活反而没有进入的余地。中央保险公司办公楼把重复办公岛、街道和高差组织成一座室内城市，员工可以调整并识别自己的位置；Diagoon 住宅只提供结构与基本层级，把房间边界交给住户继续完成；De Drie Hoven 用廊道、转角和庭院连接老年居住；Vredenburg 音乐中心则让大厅、楼梯与观众席成为彼此可见的公共地形。赫兹伯格所说的开放，并不是取消秩序，而是让秩序可以被解释和占用。面对今天标准化公寓、办公楼与学校，这个判断仍然尖锐：走廊能否停留？结构能否容纳变化？使用痕迹能否反馈到下一轮更新？本文为编辑性阅读，不是原书直接引语。",
        "tags": "#赫尔曼赫兹伯格 #建筑学生 #空间设计 #参与式设计 #建筑理论 #建筑书单 #公共空间 #住宅设计",
    },
    "renzo-piano-logbook": {
        "designer": "伦佐·皮亚诺", "designer_en": "RENZO PIANO",
        "book": "The Renzo Piano Logbook", "book_cn": "《伦佐·皮亚诺工作日志》",
        "edition": "Thames & Hudson, 1997｜ISBN 9780500279557",
        "question": "建筑的轻盈，是怎么造出来的？",
        "thesis": "轻盈不是把建筑画薄，而是让结构、设备、光线与制造过程彼此清楚。",
        "system": "assembly-light",
        "palette": {"paper": "#EDF1F0", "ink": "#1E2529", "accent": "#D84935", "second": "#2E86A4", "warm": "#C4C9C5"},
        "cards": [
            ("蓬皮杜艺术中心", "把设备移到外部，内部才获得自由", "结构、交通与管线成为可辨认构件，展厅因此保留连续、可变化的大空间。", "02-pompidou.jpg"),
            ("梅尼尔收藏馆", "自然光需要由精确构件慢慢过滤", "叶片形屋面、桁架与天窗共同控制漫射光，让技术退到安静的观看经验之后。", "03-menil.jpg"),
            ("关西国际机场", "连续大屋顶来自结构与气流一起工作", "长距离曲面、重复桁架和送风策略被统一，复杂航站楼因此保持清晰方向。", "04-kansai.jpg"),
            ("吉巴乌文化中心", "重复构件可以同时回应文化与气候", "木质壳体借风压与通风工作，传统聚落意象被转化为可制造的现代系统。", "05-tjibaou.jpg"),
        ],
        "summary": "皮亚诺的轻盈不是少用构件，而是让每个构件的受力、制造与环境任务都可读。",
        "chain": ["细部", "构件", "系统", "空间", "城市"],
        "methods": ["先画节点怎样装配，再决定整体表情", "让结构、设备与光共享同一秩序", "用重复构件管理尺度与施工误差"],
        "endcards": {"01": {"layout_rationale": "把照片拆成悬浮构件层，书封像施工日志夹在装配轴旁，标题沿竖向节点展开。", "changed_variables": ["竖向装配轴", "右中书封", "分层照片", "纵向标题"]}, "06": {"layout_rationale": "用爆炸轴从细部上升到城市，每层方法对应一类构件关系，表现轻盈由建造累积。", "changed_variables": ["爆炸轴概念链", "层间方法", "顶端总结", "钢灰底色"]}},
        "publish_title": "伦佐·皮亚诺：建筑的轻盈怎么造出来？",
        "publish_body": "《The Renzo Piano Logbook》让人看到，“轻盈”从来不是一张效果图里的薄与透明，而是漫长的构件推理。蓬皮杜中心把结构、交通与管线移到外部，让展厅保持自由；梅尼尔收藏馆用叶片形屋面和天窗精确过滤自然光；关西机场把曲面屋顶、重复桁架与送风策略统一起来；吉巴乌文化中心则让木质壳体同时承担通风、制造与文化表达。皮亚诺的项目尺度差异极大，但工作方法一致：先把节点怎样连接想清楚，再让构件形成系统，最后才出现整体形象。对设计师而言，轻盈不是少画几根线，而是让受力、设备、维护和光线彼此不打架。可以直接带走三件事：先画装配顺序，让多专业共享同一秩序，再用重复构件控制施工误差。本文为编辑性概括，不是原书逐字引语。",
        "tags": "#伦佐皮亚诺 #RenzoPiano #建筑细部 #结构设计 #建筑理论 #建筑书单 #博物馆设计 #建造逻辑",
    },
    "moshe-safdie-for-everyone-a-garden": {
        "designer": "摩西·萨夫迪", "designer_en": "MOSHE SAFDIE",
        "book": "For Everyone a Garden", "book_cn": "《每个人都应有一座花园》",
        "edition": "MIT Press, 1974｜ISBN 9780262191081",
        "question": "高密度住宅，也能让每户有花园吗？",
        "thesis": "密度不必牺牲户外生活；模块、错动与共享平台可以重新组合住宅和城市。",
        "system": "garden-cluster",
        "palette": {"paper": "#E9E5D9", "ink": "#25302D", "accent": "#D85A43", "second": "#3F7159", "warm": "#D2B05E"},
        "cards": [
            ("Habitat 67", "预制模块通过错动获得露台与方向", "重复混凝土盒子不是整齐堆叠，而被旋转、退台和连接，为住宅争取独立户外空间。", "02-habitat-67.jpg"),
            ("加拿大国家美术馆", "公共建筑也可以由花园组织路径", "玻璃厅、庭院与长廊把城市景观引入室内，让到达过程本身成为公共经验。", "03-national-gallery.jpg"),
            ("犹太大屠杀纪念馆", "建筑可以穿过地形，而不是压在地形上", "三角形混凝土棱体切入山体，光线、出口与地景共同组织记忆的路径。", "04-yad-vashem.jpg"),
            ("Sky Habitat", "空中连桥可以把高层住宅变成邻里", "错动塔楼、共享平台与空中花园尝试在垂直密度中恢复地面社区关系。", "05-sky-habitat.jpg"),
        ],
        "summary": "“每户一座花园”不是每户复制地面，而是把私密、共享与城市空间重新分层组合。",
        "chain": ["住宅单元", "私人露台", "共享平台", "邻里", "城市"],
        "methods": ["用错动而非齐平堆叠争取户外面", "把交通节点扩展成共享平台", "同时计算日照、视线、结构与隐私"],
        "endcards": {"01": {"layout_rationale": "以错动模块沿对角线生长，真实书封落在一块私人花园单元内，照片从下方托起聚落。", "changed_variables": ["对角模块", "左上书封", "下部照片", "中部问题标题"]}, "06": {"layout_rationale": "用层层退台的聚落从住宅单元上升到城市，每层承载一条空间关系与方法。", "changed_variables": ["退台概念链", "层级方法", "右上结论", "绿色聚落底图"]}},
        "publish_title": "萨夫迪：高密度住宅也能让每户有花园？",
        "publish_body": "《For Everyone a Garden》提出的不是一句浪漫口号，而是高密度住宅最难的矛盾：怎样在增加户数的同时保留日照、户外空间、方向感与邻里关系。Habitat 67 用预制混凝土模块的旋转、错动和退台，为住宅争取独立露台；加拿大国家美术馆用玻璃厅、庭院与长廊组织公共到达；犹太大屠杀纪念馆让混凝土棱体穿过山体，以光和出口建立记忆路径；Sky Habitat 则用空中连桥与共享花园测试垂直社区。萨夫迪后来做的并不都是住宅，但“单元如何组成共同体”始终存在。对今天的高层住区，真正可迁移的不是 Habitat 的外形，而是三种计算：用错动增加户外界面，把交通节点扩大为共享平台，同时校核日照、视线、结构与隐私。本文为编辑性阅读，不是原书直接引语。",
        "tags": "#摩西萨夫迪 #Habitat67 #集合住宅 #模块化建筑 #建筑理论 #建筑书单 #空中花园 #社区设计",
    },
}


def p(book):
    return {k: base.hex_rgb(v) for k, v in book["palette"].items()}


def cover_hertzberger(book, assets: Path) -> Image.Image:
    c = p(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    photo = base.crop(base.open_image(assets / "02-centraal-beheer.jpg"), (740, 900), (0.5, 0.5))
    image.paste(photo, (430, 140))
    for row in range(5):
        for col in range(4):
            x, y = 70 + col * 240, 90 + row * 240
            color = c["accent"] if (row, col) in ((1, 1), (3, 2)) else c["second"]
            draw.rectangle((x, y, x + 190, y + 190), outline=color, width=5)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (110, 350, 410, 830))
    draw.text((70, 45), book["designer_en"], font=base.get_font(27, bold=True), fill=c["ink"])
    base.text_block(draw, (70, 1160), "好建筑为什么\n要给人留余地？", base.get_font(61, bold=True), c["ink"], 700, 8)
    base.text_block(draw, (760, 1190), book["thesis"], base.get_font(29), c["ink"], 400, 11)
    draw.text((72, 1530), book["book_cn"], font=base.get_font(28, bold=True), fill=c["accent"])
    base.draw_page_mark(draw, 1, c["ink"])
    return image


def cover_piano(book, assets: Path) -> Image.Image:
    c = p(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    photo = base.crop(base.open_image(assets / "02-pompidou.jpg"), (820, 720), (0.5, 0.45))
    image.paste(photo, (330, 170))
    for i, y in enumerate((120, 900, 1010, 1120)):
        draw.line((80 + i * 45, y, 1160 - i * 60, y), fill=c["accent"] if i % 2 == 0 else c["second"], width=10)
        draw.ellipse((62 + i * 45, y - 18, 98 + i * 45, y + 18), fill=c["ink"])
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (850, 950, 1150, 1440))
    draw.text((75, 70), book["designer_en"], font=base.get_font(28, bold=True), fill=c["second"])
    base.text_block(draw, (75, 930), "建筑的轻盈，\n是怎么造出来的？", base.get_font(60, bold=True), c["ink"], 680, 8)
    base.text_block(draw, (78, 1220), book["thesis"], base.get_font(29), c["ink"], 620, 11)
    draw.text((78, 1530), book["book_cn"], font=base.get_font(27, bold=True), fill=c["accent"])
    base.draw_page_mark(draw, 1, c["ink"])
    return image


def cover_safdie(book, assets: Path) -> Image.Image:
    c = p(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    photo = base.crop(base.open_image(assets / "02-habitat-67.jpg"), (W, 760), (0.5, 0.42))
    image.paste(photo, (0, 900))
    modules = [(580, 100, 1080, 330), (390, 280, 910, 520), (690, 470, 1160, 700), (470, 650, 930, 880)]
    for i, box in enumerate(modules):
        draw.rectangle(box, fill=c["second"] if i % 2 == 0 else c["warm"], outline=c["ink"], width=5)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (80, 120, 390, 650), shadow=False)
    draw.text((80, 60), book["designer_en"], font=base.get_font(27, bold=True), fill=c["ink"])
    base.text_block(draw, (80, 690), "高密度住宅，\n也能让每户有花园吗？", base.get_font(55, bold=True), c["ink"], 620, 8)
    base.text_block(draw, (730, 730), book["thesis"], base.get_font(27), c["ink"], 420, 10)
    draw.text((78, 1530), book["book_cn"], font=base.get_font(28, bold=True), fill=c["paper"])
    base.draw_page_mark(draw, 1, c["ink"])
    return image


def interior(book, assets: Path, number: int) -> Image.Image:
    c = p(book)
    title, headline, body, filename = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    source = base.open_image(assets / filename)
    if book["system"] == "threshold-cells":
        photo = base.crop(source, (920, 980), (0.5, 0.5))
        image.paste(photo, (250, 0))
        draw.rectangle((0, 0, 180, 980), fill=c["second"] if number % 2 == 0 else c["accent"])
        for y in range(70, 920, 145):
            draw.rectangle((55, y, 125, y + 70), outline=c["warm"], width=5)
        draw.rectangle((70, 885, 600, 965), fill=c["ink"])
        draw.text((95, 902), title, font=base.get_font(31, bold=True), fill=c["paper"])
    elif book["system"] == "assembly-light":
        photo = base.crop(source, (W, 930), (0.5, 0.48))
        image.paste(photo, (0, 0))
        draw.rectangle((0, 930, W, 1000), fill=c["warm"])
        for x in range(70, 1170, 120):
            draw.line((x, 930, x + 45, 1000), fill=c["accent"] if x % 240 else c["second"], width=7)
        draw.rectangle((65, 820, 580, 905), fill=c["ink"])
        draw.text((90, 838), title, font=base.get_font(31, bold=True), fill=c["paper"])
    else:
        photo = base.crop(source, (W, 930), (0.5, 0.5))
        image.paste(photo, (0, 0))
        for i, x in enumerate((0, 250, 500, 750, 1000)):
            draw.rectangle((x, 900 - i * 25, x + 242, 960), fill=c["second"] if i % 2 == 0 else c["warm"])
        draw.rectangle((70, 825, 570, 905), fill=c["ink"])
        draw.text((95, 843), title, font=base.get_font(31, bold=True), fill=c["paper"])
    y = base.text_block(draw, (75, 1090), headline, base.get_font(53, bold=True), c["ink"], 1060, 8)
    base.text_block(draw, (78, y + 30), body, base.get_font(31), c["ink"], 980, 12)
    base.draw_page_mark(draw, number, c["ink"])
    draw.text((1010, 1570), book["designer_en"], font=base.get_font(18, bold=True), fill=c["accent"])
    return image


def summary_hertzberger(book) -> Image.Image:
    c = p(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((75, 85), "秩序，要允许生活继续完成", font=base.get_font(63, bold=True), fill=c["ink"])
    boxes = [(85, 420, 340, 675), (300, 570, 610, 880), (535, 750, 900, 1115), (815, 945, 1145, 1275), (320, 1120, 760, 1540)]
    for i, (box, label) in enumerate(zip(boxes, book["chain"])):
        fill = c["accent"] if i == 2 else c["second"] if i % 2 else c["warm"]
        draw.rectangle(box, fill=fill, outline=c["ink"], width=5)
        draw.text((box[0]+22, box[1]+22), label, font=base.get_font(30, bold=True), fill=c["paper"] if i in (1,2,3) else c["ink"])
    methods = [(95, 315), (700, 400), (790, 1370)]
    for i, (method, xy) in enumerate(zip(book["methods"], methods)):
        draw.text(xy, f"0{i+1}", font=base.get_font(25, bold=True), fill=c["accent"])
        base.text_block(draw, (xy[0]+50, xy[1]), method, base.get_font(25), c["ink"], 370, 8)
    base.draw_page_mark(draw, 6, c["ink"])
    return image


def summary_piano(book) -> Image.Image:
    c = p(book)
    image = Image.new("RGB", (W, H), c["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((75, 85), "轻盈，由清楚的连接累积", font=base.get_font(64, bold=True), fill=c["paper"])
    x = 620
    layers = [(250, "城市"), (500, "空间"), (760, "系统"), (1030, "构件"), (1320, "细部")]
    for i, (y, label) in enumerate(layers):
        width = 900 - i * 115
        draw.line((x-width//2, y, x+width//2, y), fill=c["accent"] if i % 2 else c["second"], width=12)
        draw.ellipse((x-23, y-23, x+23, y+23), fill=c["warm"])
        draw.text((x+40, y-28), label, font=base.get_font(30, bold=True), fill=c["paper"])
    for i, (method, y) in enumerate(zip(book["methods"], (390, 890, 1450))):
        draw.text((80, y), f"0{i+1}", font=base.get_font(26, bold=True), fill=c["accent"])
        base.text_block(draw, (135, y), method, base.get_font(26), c["paper"], 390, 9)
    base.draw_page_mark(draw, 6, c["ink"], light=True)
    return image


def summary_safdie(book) -> Image.Image:
    c = p(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((75, 85), "密度，也可以生成户外生活", font=base.get_font(61, bold=True), fill=c["ink"])
    terraces = [(75, 1280, 310, 1530), (260, 1040, 560, 1530), (510, 780, 840, 1530), (790, 500, 1110, 1530)]
    labels = book["chain"][:4]
    for i, (box, label) in enumerate(zip(terraces, labels)):
        fill = c["second"] if i % 2 == 0 else c["warm"]
        draw.rectangle(box, fill=fill, outline=c["ink"], width=5)
        draw.text((box[0]+20, box[1]+24), label, font=base.get_font(28, bold=True), fill=c["paper"] if i % 2 == 0 else c["ink"])
    draw.text((930, 395), "城市", font=base.get_font(34, bold=True), fill=c["accent"])
    for i, (method, xy) in enumerate(zip(book["methods"], ((80, 340), (80, 520), (80, 700)))):
        draw.text(xy, f"0{i+1}", font=base.get_font(25, bold=True), fill=c["accent"])
        base.text_block(draw, (xy[0]+50, xy[1]), method, base.get_font(25), c["ink"], 430, 8)
    base.draw_page_mark(draw, 6, c["ink"])
    return image


def write_docs(book, assets: Path, output: Path) -> None:
    manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    lines = ["# 图片来源", "", "| 文件名 | 内容 | 作者/机构 | 来源 URL | 许可/版权 | 修改 |", "|---|---|---|---|---|---|"]
    for item in manifest:
        lines.append(f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item['modifications']} |")
    lines += ["", "书封仅用于书籍识别、介绍与评论；商业投放前请重新核验平台规则。", "卡片文字为编辑性概括，未作为原书直接引语。"]
    (output / "图片来源.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output / "发布文案.md").write_text(f"# 标题\n\n{book['publish_title']}\n\n# 正文\n\n{book['publish_body']}\n\n# 标签\n\n{book['tags']}\n\n# 版本\n\n{book['book']}｜{book['edition']}\n", encoding="utf-8")
    post = {"designer": book["designer"], "book": book["book"], "edition": book["edition"], "thesis": book["thesis"], "concept_chain": book["chain"], "cards": [{"number": "01", "role": "problem cover", "headline": book["question"], "asset": "cover.jpg"}, *[{"number": f"{i:02d}", "role": "mechanism" if i == 2 else "evidence", "headline": card[1], "evidence": card[0], "asset": card[3]} for i, card in enumerate(book["cards"], 2)], {"number": "06", "role": "synthesis", "headline": book["summary"], "asset": ""}], "endcards": book["endcards"], "transferable_methods": book["methods"], "sources": manifest}
    (output / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    previews = []
    for slug, book in BOOKS.items():
        assets, output = ASSET_ROOT / slug, OUTPUT_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        if book["system"] == "threshold-cells":
            first, last = cover_hertzberger(book, assets), summary_hertzberger(book)
        elif book["system"] == "assembly-light":
            first, last = cover_piano(book, assets), summary_piano(book)
        else:
            first, last = cover_safdie(book, assets), summary_safdie(book)
        cards = [first, *[interior(book, assets, n) for n in range(2, 6)], last]
        paths = []
        for n, card in enumerate(cards, 1):
            path = output / f"{n:02d}.jpg"
            base.save(card, path)
            paths.append(path)
        base.preview(paths, output / "preview.jpg")
        write_docs(book, assets, output)
        previews.append(output / "preview.jpg")
        print(f"Rendered {slug}")
    contact = Image.new("RGB", (1242, 3500), (228, 227, 222))
    y = 36
    for path in previews:
        with Image.open(path) as source:
            strip = source.convert("RGB").resize((1160, 1035), Image.Resampling.LANCZOS)
        contact.paste(strip, (41, y))
        y += 1140
    base.save(contact, OUTPUT_ROOT / "总预览.jpg")


if __name__ == "__main__":
    main()
