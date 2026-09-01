#!/usr/bin/env python3
"""Render the second batch of three distinct six-card architecture-book posts."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters-02"
OUTPUT_ROOT = ROOT / "output" / "three-unmentioned-masters-02"
W, H = base.W, base.H

BOOKS = {
    "richard-neutra-survival-through-design": {
        "designer": "理查德·诺伊特拉", "designer_en": "RICHARD NEUTRA",
        "book": "Survival Through Design", "book_cn": "《生存·通过设计》",
        "edition": "Oxford University Press, 1954｜ISBN 9780195007909 版书目",
        "question": "建筑能照顾人的神经系统吗？",
        "thesis": "设计不只安排功能，还要调节光、温度、视线与身体压力，帮助人适应环境。",
        "system": "sensor-field",
        "palette": {"paper": "#E7ECE7", "ink": "#172526", "accent": "#E45B3D", "second": "#3C837A", "warm": "#BFCF9F"},
        "cards": [
            ("洛弗尔健康住宅", "健康从空气、日照和身体节律开始", "钢结构不是造型表演，而是为通风、露台、日光浴和新的健康生活提供框架。", "02-lovell-house.jpg"),
            ("考夫曼沙漠住宅", "气候边界必须可以精细调节", "深挑檐、可开启界面与水面共同缓冲沙漠热量，让室内外关系随时间变化。", "03-kaufmann-house.jpg"),
            ("VDL 研究住宅", "小空间靠视线与反射获得延伸", "庭院、水面、玻璃和屋顶花园把有限基地组织成多层环境反馈。", "04-vdl-house.jpg"),
            ("珀金斯住宅", "尺度应从具体身体而不是平均值出发", "紧凑平面、连续玻璃和内置家具围绕居住者的生活方式调整。", "05-perkins-house.jpg"),
        ],
        "summary": "生存性设计不是医疗化建筑，而是让空间持续读取身体与气候的反馈。",
        "chain": ["身体", "感官", "气候", "界面", "行为"],
        "methods": ["先记录光、热、噪声与视线的变化", "把门窗和遮阳设计成可调界面", "用家具、庭院和水面修正身体压力"],
        "endcards": {"01": {"layout_rationale": "以生命体征刻度穿过建筑照片，书封悬置在观察区，表现环境对身体的连续反馈。", "changed_variables": ["右上书封", "纵向体征轴", "整页冷色照片", "左下问题标题"]}, "06": {"layout_rationale": "把结论组织成五层感官阈值，读者从身体向行为逐层穿过，而非阅读普通列表。", "changed_variables": ["同心阈值", "中心身体节点", "环外方法标注", "浅色科学图谱"]}},
        "publish_title": "诺伊特拉：建筑能照顾人的神经系统吗？",
        "publish_body": "《Survival Through Design》最值得今天重新阅读的地方，是诺伊特拉把建筑放回身体与环境的连续反馈中。洛弗尔健康住宅用钢结构承载通风、露台与日照；考夫曼沙漠住宅借助深挑檐、可开启界面和水面缓冲热量；VDL 研究住宅用庭院、反射与屋顶花园延伸有限基地；珀金斯住宅则根据具体居住者调整尺度与家具。这里的“生存”不是把建筑变成医疗设备，而是提醒设计师：光、热、噪声、视线与空间压力都会作用于神经系统。透明与轻盈也不是风格终点，每一道玻璃、遮阳和水面都承担调节刺激的任务。面对更高密度、更强噪声与更极端气候，这套反馈思维依然有效。可带走的方法是先记录环境变化，再把门窗和遮阳做成可调界面，并用家具、庭院与水面修正身体体验。本文为基于书籍与案例的编辑性概括，不是原书直接引语。",
        "tags": "#理查德诺伊特拉 #SurvivalThroughDesign #住宅设计 #环境心理 #建筑理论 #建筑书单 #现代建筑 #空间体验",
    },
    "buckminster-fuller-spaceship-earth": {
        "designer": "巴克敏斯特·富勒", "designer_en": "R. BUCKMINSTER FULLER",
        "book": "Operating Manual for Spaceship Earth", "book_cn": "《地球号宇宙飞船操作手册》",
        "edition": "Southern Illinois University Press, 1969｜Open Library OL465813W",
        "question": "地球这艘飞船，为什么没有说明书？",
        "thesis": "设计的任务不是争夺有限资源，而是用系统知识让更少材料服务更多人。",
        "system": "resource-network",
        "palette": {"paper": "#E9EDF0", "ink": "#11171B", "accent": "#E6F04A", "second": "#2BA9C6", "warm": "#B8BFC5"},
        "cards": [
            ("Dymaxion 住宅", "住宅可以被当作轻量系统重算", "圆形平面、集中服务核与工业化构件尝试用更少材料完成居住功能。", "02-dymaxion-house.jpg"),
            ("Dymaxion 汽车", "效率必须跨越单一专业边界", "交通工具、流线、重量和空气动力学被放进同一套整体性能判断。", "03-dymaxion-car.jpg"),
            ("蒙特利尔生物圈", "几何能把局部构件变成整体强度", "三角网格分配受力，以较轻结构围合巨大的公共空间。", "04-montreal-biosphere.jpg"),
            ("Fly's Eye Dome", "构件需要同时承担结构与环境功能", "重复单元整合开口、采光和模块化制造，测试可扩展的居住外壳。", "05-fly-eye-dome.jpg"),
        ],
        "summary": "“做得更多、用得更少”不是口号，而是把资源、结构、制造与全球协作放进同一系统。",
        "chain": ["资源", "信息", "几何", "协作", "共享"],
        "methods": ["先统计性能与资源，而不是先画形象", "用重复单元建立可扩展的整体", "让不同专业共享同一张系统地图"],
        "endcards": {"01": {"layout_rationale": "以圆形地球舷窗和三角网格形成驾驶舱界面，书封作为操作手册插入右下。", "changed_variables": ["圆形主视觉", "弧形标题", "右下书封", "黑底高亮信息"]}, "06": {"layout_rationale": "用三角网架连接资源、信息、几何、协作与共享，三条方法落在不同结构边上。", "changed_variables": ["三角网络", "节点式概念链", "边缘方法", "无面板深底"]}},
        "publish_title": "富勒：地球号飞船为什么没有说明书？",
        "publish_body": "《Operating Manual for Spaceship Earth》不是一本造型手册，而是富勒对资源、知识和协作方式的系统提问。Dymaxion 住宅用圆形平面、服务核和工业构件重新计算居住；Dymaxion 汽车把重量、流线和空气动力学放在一起；蒙特利尔生物圈借三角网格用较轻结构围合巨大空间；Fly's Eye Dome 则让重复单元同时承担结构、开口与制造逻辑。富勒真正反对的是专业各自优化、整体继续浪费。局部节能也不等于系统高效：如果材料、运输、维护和更新彼此割裂，漂亮的单项指标仍可能只是转移成本。真正的设计对象，是资源在完整生命周期中的流动。对设计师而言，“更少材料服务更多人”需要三个动作：先统计性能和资源，再寻找可重复扩展的几何单元，最后让结构、制造、环境与使用共享同一张系统地图。本文为编辑性阅读，不是原书逐字引语。",
        "tags": "#巴克敏斯特富勒 #SpaceshipEarth #系统设计 #轻量结构 #建筑理论 #建筑书单 #可持续设计 #设计思维",
    },
    "charles-correa-place-in-the-shade": {
        "designer": "查尔斯·柯里亚", "designer_en": "CHARLES CORREA",
        "book": "A Place in the Shade", "book_cn": "《阴影中的场所》",
        "edition": "Penguin Books India, 2010｜ISBN 9780143068785",
        "question": "热带建筑为什么不能只靠空调？",
        "thesis": "热带空间的核心不是封闭室温，而是用阴影、庭院与天空组织可迁移的舒适边界。",
        "system": "climate-section",
        "palette": {"paper": "#EEE4CF", "ink": "#202637", "accent": "#C74C32", "second": "#315E64", "warm": "#E3B84B"},
        "cards": [
            ("甘地纪念馆", "屋顶与庭院先建立可呼吸的秩序", "低矮模块、廊道和开敞庭院让纪念空间依靠阴影与行走，而非封闭体量。", "02-gandhi-ashram.jpg"),
            ("巴拉特艺术中心", "建筑可以继续地形，而不是占据地形", "下沉庭院、屋顶平台与层层台阶把文化空间嵌入坡地。", "03-bharat-bhavan.jpg"),
            ("贾瓦哈尔艺术中心", "抽象秩序要转化成可穿行的院落", "九宫格不只是图形来源，而被拆成入口、庭院、展厅与城市路径。", "04-jawahar-kala-kendra.jpg"),
            ("IUCAA", "天空可以成为公共空间的共同尺度", "院落、门洞与天文意象把科研机构组织成可停留、可辨认的空间序列。", "05-iucaa.jpg"),
        ],
        "summary": "气候设计不是增加设备，而是创造从室内、廊下、庭院到天空的多层舒适选择。",
        "chain": ["室内", "廊下", "庭院", "屋顶", "天空"],
        "methods": ["先画太阳与季风，再决定体量开口", "用廊道和院落提供渐变的舒适区", "让屋顶与地面都成为可使用空间"],
        "endcards": {"01": {"layout_rationale": "以强烈日照剖面切出深色阴影区，书封位于阴影内，标题跨越明暗边界。", "changed_variables": ["对角光影剖面", "左下书封", "跨界标题", "上部日照留白"]}, "06": {"layout_rationale": "把结论画成从室内到天空的阶梯剖面，三条方法分别落在遮阴、庭院和屋顶层。", "changed_variables": ["阶梯概念链", "剖面阅读方向", "方法嵌入空间层", "暖色浅底"]}},
        "publish_title": "柯里亚：热带建筑为什么不能只靠空调？",
        "publish_body": "《A Place in the Shade》把查尔斯·柯里亚长期关心的问题集中到一起：在热带，舒适不应只等于密闭房间里的固定温度。甘地纪念馆用低矮模块、廊道和庭院建立可呼吸的秩序；巴拉特艺术中心把下沉院落与屋顶平台嵌进坡地；贾瓦哈尔艺术中心把九宫格转成可穿行的院落和城市路径；IUCAA 则让门洞、庭院与天空共同组织科研社区。这里的“阴影”不是消极避光，而是一层可居住的气候边界。被动式气候策略也不是回到传统形式，而是重新分配一天与不同季节中可使用的空间。高密度城市同样能借灰空间、通风路径和共享屋顶获得这种选择。对设计师最实用的提醒是：先画太阳与季风，再决定开口；用廊道和庭院提供渐变舒适区；让屋顶与地面都成为生活空间。本文为编辑性概括，不是原书直接引语。",
        "tags": "#查尔斯柯里亚 #APlaceInTheShade #热带建筑 #气候设计 #建筑理论 #建筑书单 #庭院设计 #公共空间",
    },
}


def palette(book):
    return {k: base.hex_rgb(v) for k, v in book["palette"].items()}


def cover_neutra(book, assets: Path) -> Image.Image:
    p = palette(book)
    image = base.crop(base.open_image(assets / "02-lovell-house.jpg"), (W, H), (0.52, 0.5))
    image = ImageEnhance.Color(image).enhance(0.28)
    overlay = Image.new("RGBA", (W, H), (*p["second"], 78))
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 510, H), fill=(*p["paper"],))
    for y in range(110, 1510, 78):
        length = 170 + int(90 * math.sin(y / 87))
        draw.line((470, y, 470 + length, y), fill=p["accent"] if y % 156 else p["warm"], width=5)
    draw.line((470, 70, 470, 1570), fill=p["ink"], width=3)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (760, 90, 1130, 650))
    draw.text((70, 95), book["designer_en"], font=base.get_font(27, bold=True), fill=p["second"])
    y = base.text_block(draw, (70, 760), "建筑能照顾\n人的神经系统吗？", base.get_font(50, bold=True), p["ink"], 400, 8)
    base.text_block(draw, (72, y + 34), book["thesis"], base.get_font(29), p["ink"], 385, 11)
    draw.text((72, 1510), book["book_cn"], font=base.get_font(28, bold=True), fill=p["accent"])
    base.draw_page_mark(draw, 1, p["ink"])
    return image


def cover_fuller(book, assets: Path) -> Image.Image:
    p = palette(book)
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    photo = base.crop(base.open_image(assets / "04-montreal-biosphere.jpg"), (940, 940), (0.5, 0.48))
    mask = Image.new("L", (940, 940), 0)
    ImageDraw.Draw(mask).ellipse((20, 20, 920, 920), fill=255)
    image.paste(photo, (180, 250), mask)
    for radius in (510, 565, 620):
        draw.arc((620-radius, 720-radius, 620+radius, 720+radius), 190, 350, fill=p["second"], width=4)
    for angle in range(0, 360, 30):
        x = 620 + int(450 * math.cos(math.radians(angle)))
        y = 720 + int(450 * math.sin(math.radians(angle)))
        draw.line((620, 720, x, y), fill=(*p["warm"],), width=2)
    draw.rectangle((0, 0, W, 220), fill=p["ink"])
    draw.text((70, 78), book["designer_en"], font=base.get_font(26, bold=True), fill=p["accent"])
    base.text_block(draw, (70, 1240), "地球这艘飞船，\n为什么没有说明书？", base.get_font(58, bold=True), p["paper"], 720, 8)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (865, 1125, 1155, 1575))
    base.draw_page_mark(draw, 1, p["ink"], light=True)
    return image


def cover_correa(book, assets: Path) -> Image.Image:
    p = palette(book)
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    photo = base.crop(base.open_image(assets / "02-gandhi-ashram.jpg"), (W, 690), (0.5, 0.5))
    image.paste(photo, (0, 970))
    draw.polygon([(0, 0), (W, 0), (W, 560), (0, 960)], fill=p["warm"])
    draw.polygon([(0, 680), (W, 320), (W, 1040), (0, 1040)], fill=p["ink"])
    draw.line((0, 680, W, 320), fill=p["accent"], width=16)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (80, 410, 390, 900), shadow=False)
    draw.text((80, 90), book["designer_en"], font=base.get_font(28, bold=True), fill=p["ink"])
    base.text_block(draw, (500, 500), "热带建筑为什么\n不能只靠空调？", base.get_font(62, bold=True), p["paper"], 650, 8)
    base.text_block(draw, (510, 735), book["thesis"], base.get_font(28), p["paper"], 620, 10)
    draw.text((82, 1510), book["book_cn"], font=base.get_font(29, bold=True), fill=p["paper"])
    base.draw_page_mark(draw, 1, p["ink"])
    return image


def interior(book, assets: Path, number: int) -> Image.Image:
    p = palette(book)
    title, headline, body, filename = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    source = base.open_image(assets / filename)
    if book["system"] == "sensor-field":
        photo = base.crop(source, (W, 960), (0.5, 0.48))
        image.paste(photo, (0, 0))
        draw.rectangle((0, 960, W, 1000), fill=p["second"])
        for x in range(80, 1180, 52):
            height = 16 + (x * number) % 54
            draw.line((x, 1000, x, 1000 + height), fill=p["accent"], width=4)
        draw.rectangle((70, 840, 560, 930), fill=p["ink"])
        draw.text((95, 858), title, font=base.get_font(33, bold=True), fill=p["paper"])
        y = base.text_block(draw, (75, 1090), headline, base.get_font(55, bold=True), p["ink"], 1060, 8)
        base.text_block(draw, (78, y + 30), body, base.get_font(31), p["ink"], 980, 12)
    elif book["system"] == "resource-network":
        photo = base.crop(source, (W, 980), (0.5, 0.48))
        image.paste(photo, (0, 0))
        draw.rectangle((0, 0, 120, 980), fill=p["ink"])
        for yline in range(80, 920, 95):
            draw.ellipse((44, yline, 76, yline + 32), fill=p["accent"] if (yline // 95) % 2 else p["second"])
        draw.rectangle((0, 980, W, H), fill=p["ink"])
        draw.text((80, 1035), title, font=base.get_font(30, bold=True), fill=p["accent"])
        y = base.text_block(draw, (80, 1110), headline, base.get_font(53, bold=True), p["paper"], 1060, 8)
        base.text_block(draw, (84, y + 28), body, base.get_font(30), p["paper"], 980, 12)
    else:
        photo = base.crop(source, (W, 920), (0.5, 0.48))
        image.paste(photo, (0, 0))
        draw.polygon([(0, 840), (W, 720), (W, 1040), (0, 1040)], fill=p["ink"])
        draw.line((0, 840, W, 720), fill=p["warm"], width=15)
        draw.text((80, 885), title, font=base.get_font(33, bold=True), fill=p["paper"])
        y = base.text_block(draw, (78, 1110), headline, base.get_font(54, bold=True), p["ink"], 1040, 8)
        base.text_block(draw, (82, y + 28), body, base.get_font(31), p["ink"], 970, 12)
    base.draw_page_mark(draw, number, p["ink"], light=book["system"] == "resource-network")
    draw.text((1010, 1570), book["designer_en"], font=base.get_font(18, bold=True), fill=p["accent"])
    return image


def summary_neutra(book) -> Image.Image:
    p = palette(book)
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((75, 90), "空间必须持续读取身体", font=base.get_font(64, bold=True), fill=p["ink"])
    center = (620, 780)
    radii = [115, 210, 310, 420, 520]
    for i, (radius, label) in enumerate(zip(radii, book["chain"])):
        draw.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), outline=p["second"] if i % 2 else p["accent"], width=10 if i == 0 else 4)
        draw.text((center[0]+radius-25, center[1]-35), label, font=base.get_font(27, bold=True), fill=p["ink"])
    draw.ellipse((center[0]-90, center[1]-90, center[0]+90, center[1]+90), fill=p["ink"])
    draw.text(center, "反馈", font=base.get_font(38, bold=True), fill=p["paper"], anchor="mm")
    for i, method in enumerate(book["methods"]):
        y = 1330 + i * 86
        draw.line((80, y, 240, y), fill=p["accent"] if i == 0 else p["second"], width=8)
        draw.text((270, y-25), f"0{i+1}  {method}", font=base.get_font(27), fill=p["ink"])
    base.draw_page_mark(draw, 6, p["ink"])
    return image


def summary_fuller(book) -> Image.Image:
    p = palette(book)
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((75, 90), "更少资源，服务更多人", font=base.get_font(67, bold=True), fill=p["paper"])
    nodes = [(620, 340), (1050, 720), (880, 1260), (360, 1260), (190, 720)]
    for i in range(5):
        a, b = nodes[i], nodes[(i + 1) % 5]
        draw.line((*a, *b), fill=p["second"], width=8)
        draw.line((*a, *nodes[(i + 2) % 5]), fill=p["warm"], width=2)
    for i, (label, node) in enumerate(zip(book["chain"], nodes)):
        draw.ellipse((node[0]-38, node[1]-38, node[0]+38, node[1]+38), fill=p["accent"] if i % 2 == 0 else p["second"])
        draw.text((node[0]-40, node[1]+58), label, font=base.get_font(30, bold=True), fill=p["paper"])
    methods_xy = [(90, 500), (760, 520), (430, 1410)]
    for i, (method, xy) in enumerate(zip(book["methods"], methods_xy)):
        draw.text(xy, f"0{i+1}", font=base.get_font(26, bold=True), fill=p["accent"])
        base.text_block(draw, (xy[0]+55, xy[1]), method, base.get_font(26), p["paper"], 360, 9)
    base.draw_page_mark(draw, 6, p["ink"], light=True)
    return image


def summary_correa(book) -> Image.Image:
    p = palette(book)
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((75, 90), "舒适是一组可以选择的边界", font=base.get_font(62, bold=True), fill=p["ink"])
    steps = [(70, 1210, 280, 1530), (280, 1040, 500, 1530), (500, 820, 730, 1530), (730, 570, 970, 1530), (970, 300, 1170, 1530)]
    colors = [p["ink"], p["second"], p["accent"], p["warm"], p["paper"]]
    for i, (box, label) in enumerate(zip(steps, book["chain"])):
        draw.rectangle(box, fill=colors[i], outline=p["ink"], width=4)
        fill = p["paper"] if i < 3 else p["ink"]
        draw.text((box[0]+20, box[1]+24), label, font=base.get_font(29, bold=True), fill=fill)
    for i, (method, xy) in enumerate(zip(book["methods"], [(90, 360), (90, 520), (90, 680)])):
        draw.text(xy, f"0{i+1}", font=base.get_font(25, bold=True), fill=p["accent"])
        base.text_block(draw, (xy[0]+48, xy[1]), method, base.get_font(25), p["ink"], 430, 8)
    draw.polygon([(1030, 250), (1100, 120), (1170, 250)], fill=p["warm"])
    base.draw_page_mark(draw, 6, p["ink"])
    return image


def write_docs(book, assets: Path, output: Path) -> None:
    manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    lines = ["# 图片来源", "", "| 文件名 | 内容 | 作者/机构 | 来源 URL | 许可/版权 | 修改 |", "|---|---|---|---|---|---|"]
    for item in manifest:
        lines.append(f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item['modifications']} |")
    lines += ["", "书封仅用于书籍识别、介绍与评论；商业投放前请重新核验平台规则。", "卡片文字为编辑性概括，未作为原书直接引语。"]
    (output / "图片来源.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output / "发布文案.md").write_text(f"# 标题\n\n{book['publish_title']}\n\n# 正文\n\n{book['publish_body']}\n\n# 标签\n\n{book['tags']}\n\n# 版本\n\n{book['book']}｜{book['edition']}\n", encoding="utf-8")
    post = {"designer": book["designer"], "book": book["book"], "edition": book["edition"], "thesis": book["thesis"], "concept_chain": book["chain"], "cards": [{"number": "01", "role": "problem cover", "headline": book["question"], "asset": "cover.jpg"}, *[{"number": f"{i:02d}", "role": "mechanism" if i == 2 else "evidence", "headline": c[1], "evidence": c[0], "asset": c[3]} for i, c in enumerate(book["cards"], 2)], {"number": "06", "role": "synthesis", "headline": book["summary"], "asset": ""}], "endcards": book["endcards"], "transferable_methods": book["methods"], "sources": manifest}
    (output / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    previews = []
    for slug, book in BOOKS.items():
        assets, output = ASSET_ROOT / slug, OUTPUT_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        if book["system"] == "sensor-field":
            first, last = cover_neutra(book, assets), summary_neutra(book)
        elif book["system"] == "resource-network":
            first, last = cover_fuller(book, assets), summary_fuller(book)
        else:
            first, last = cover_correa(book, assets), summary_correa(book)
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
