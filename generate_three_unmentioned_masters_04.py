#!/usr/bin/env python3
"""Render batch 04: three distinct architecture-book Xiaohongshu posts."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters-04"
OUTPUT_ROOT = ROOT / "output" / "three-unmentioned-masters-04"
W, H = base.W, base.H


BOOKS = {
    "hassan-fathy-architecture-for-the-poor": {
        "designer": "哈桑·法赛",
        "designer_en": "HASSAN FATHY",
        "book": "Architecture for the Poor",
        "book_cn": "《为穷人建筑》",
        "edition": "University of Chicago Press, 2000｜ISBN 9780226239163",
        "question": "低成本建筑，为什么要先学会当地方法？",
        "thesis": "经济不是削减空间，而是让材料、气候、工匠和居民回到同一套建造逻辑。",
        "system": "earth-vault",
        "palette": {"paper": "#E9DFC9", "ink": "#20221D", "accent": "#C94E33", "second": "#315C55", "warm": "#D7A643"},
        "cards": [
            ("新古尔纳清真寺", "土坯拱券把材料限制变成空间秩序", "当地土料、厚墙与穹顶共同承担结构和遮热，不依赖昂贵木材也能形成清楚的公共中心。", "02-new-gourna-mosque.jpg"),
            ("手工艺展馆剖面", "真正的低成本，要先在剖面里解决气候", "拱顶、院落、高窗与墙体厚度在同一张剖面中工作，承重、采光和通风不再彼此分离。", "03-new-gourna-section.jpg"),
            ("新巴里斯村", "重复的券拱能够形成可学习的建造语法", "绿洲聚落用泥砖拱顶、遮阴路径与紧凑体量回应高温，也让施工方法能被当地工匠掌握。", "04-new-baris.jpg"),
            ("达尔伊斯兰清真寺", "传统不是外形，而是一套可迁移的环境技术", "法赛把土墙、拱顶与院落带到新墨西哥，证明地方方法可以在新气候与新社区中重新校准。", "05-dar-al-islam.jpg"),
        ],
        "summary": "真正节省的建筑，不是把质量删掉，而是让材料、气候与劳动彼此匹配。",
        "chain": ["土", "拱券", "微气候", "工匠", "共同建造"],
        "methods": ["从当地可得材料反推结构跨度", "用剖面同时解决承重、遮阳与通风", "把施工知识留给社区，而非设备依赖"],
        "endcards": {
            "01": {"layout_rationale": "以新古尔纳实景铺满背景，放大真实书封并嵌入拱形门洞，问题标题沿左侧竖向展开。", "changed_variables": ["右侧大书封", "满幅项目底图", "左上问题标题", "拱洞式信息面板"]},
            "06": {"layout_rationale": "用连续拱券截面组织材料到共同建造的递进关系，三条方法落在不同结构跨中。", "changed_variables": ["拱券概念链", "截面式阅读", "跨中方法标注", "暖色纯排版"]},
        },
        "publish_title": "低成本建筑，为什么更需要完整的方法？",
        "publish_body": "《Architecture for the Poor》讨论的并不是怎样把房子做得更便宜，而是怎样让建造重新适合当地。法赛在新古尔纳使用土坯厚墙、拱券和穹顶，让有限材料同时承担结构与遮热；手工艺展馆的剖面把承重、采光和通风放进同一套空间逻辑；新巴里斯以可重复的泥砖券拱形成工匠能够学习的建造语法；达尔伊斯兰清真寺则证明，这些方法并非只能停留在埃及，而能在新气候和新社区中重新校准。对设计师最有用的不是复制泥土外观，而是改变工作顺序：先从当地材料反推跨度，用剖面同时解决气候与结构，再让施工知识能够被社区掌握。真正的节省，不是删掉质量，而是减少材料、设备与劳动之间的冲突。本文为编辑性阅读，不是原书逐字引语。今天的低成本项目，是否也能把维护与建造能力留在当地？",
        "tags": "#哈桑法赛 #ArchitectureForThePoor #乡土建筑 #被动式设计 #低成本建筑 #建筑理论 #建筑书单 #建筑学生",
    },
    "kisho-kurokawa-metabolism-in-architecture": {
        "designer": "黑川纪章",
        "designer_en": "KISHO KUROKAWA",
        "book": "Metabolism in Architecture",
        "book_cn": "《新陈代谢建筑》",
        "edition": "Studio Vista, 1977｜ISBN 0289707331",
        "question": "建筑能像细胞一样替换和生长吗？",
        "thesis": "新陈代谢不是胶囊造型，而是把长期骨架与短期单元分开，让城市持续更新。",
        "system": "plug-in-capsules",
        "palette": {"paper": "#ECEBE5", "ink": "#15191A", "accent": "#F04B2B", "second": "#1C8190", "warm": "#E1C94F"},
        "cards": [
            ("中银胶囊塔", "长期核心与短期单元必须先被分开", "双核心承担交通与结构，胶囊通过接口挂接；虽然单元最终未按设想更换，逻辑仍揭示了寿命分层的关键。", "02-nakagin.jpg"),
            ("寒河江市政厅", "结构核心可以像树一样支撑开放空间", "分枝混凝土柱把办公层托起，固定支撑与可调整工作空间形成不同层级的秩序。", "03-sagae-city-hall.jpg"),
            ("吉隆坡国际机场", "大型基础设施需要为扩展预留组织规则", "重复屋顶模块、交通系统与“森林中的机场”概念，让航站楼在复杂流线中保持方向与生长余地。", "04-klia.jpg"),
            ("东京国立新美术馆", "可变性也可以来自没有固定收藏的空间框架", "展厅、设备与公共大厅被组织成可持续接纳不同展览的基础设施，变化发生在稳定结构之内。", "05-national-art-center.jpg"),
        ],
        "summary": "真正的新陈代谢，不是看起来像机器，而是把不同寿命的部件分开管理。",
        "chain": ["核心", "接口", "单元", "设备", "更新"],
        "methods": ["在设计初期标注不同构件的使用寿命", "让接口先于造型被标准化", "给扩展、维修与拆换保留可达路径"],
        "endcards": {
            "01": {"layout_rationale": "以中银胶囊塔照片形成城市底图，真实书封放大为左侧主物，问题标题与接口圆环集中在右下。", "changed_variables": ["左侧大书封", "上部城市实景", "右下问题标题", "圆形接口节点"]},
            "06": {"layout_rationale": "中央核心贯穿全页，五个寿命层级像胶囊从两侧插接，方法写在三块可拆换单元中。", "changed_variables": ["垂直核心链", "左右插接模块", "胶囊式方法", "深色结构底"]},
        },
        "publish_title": "建筑能更换部件，却不推倒重来吗？",
        "publish_body": "《Metabolism in Architecture》最容易被误读成一组胶囊和机器美学，但黑川纪章真正关心的是时间：城市里的核心、接口、房间与设备，本来就拥有不同寿命。中银胶囊塔用双核心承担结构和交通，让居住单元理论上能够拆换；寒河江市政厅用分枝柱支撑开放办公层，把固定支撑与可变使用分开；吉隆坡国际机场以重复屋顶模块和交通规则组织未来扩展；东京国立新美术馆则通过稳定基础设施接纳不断变化的展览。中银胶囊从未按计划更新，恰好说明可变建筑不能只画概念图：接口标准、维修路径、产权和运营必须同时成立。设计师可以直接带走三件事：标注构件寿命，先设计接口，再给维修和扩建留下可达路径。本文为编辑性概括，不是原书引语。你现在的项目里，哪一部分最应该先被允许替换？",
        "tags": "#黑川纪章 #MetabolismInArchitecture #新陈代谢建筑 #胶囊建筑 #建筑更新 #建筑理论 #建筑书单 #设计方法",
    },
    "fumihiko-maki-nurturing-dreams": {
        "designer": "槙文彦",
        "designer_en": "FUMIHIKO MAKI",
        "book": "Nurturing Dreams",
        "book_cn": "《培育梦想》",
        "edition": "MIT Press, 2008｜ISBN 9780262135009",
        "question": "一栋建筑，怎么成为一段城市关系？",
        "thesis": "城市品质来自建筑之间的时间、缝隙与连续关系，而不只来自单体造型。",
        "system": "collective-sequence",
        "palette": {"paper": "#F0F0EB", "ink": "#24282D", "accent": "#E24A42", "second": "#3D6F8D", "warm": "#DEB749"},
        "cards": [
            ("代官山 Hillside Terrace", "分期建造可以累积街区，而不是打断街区", "项目跨越二十多年逐段完成，以低层体量、通道和庭院保持尺度，让时间成为群体形式的一部分。", "02-hillside-terrace.jpg"),
            ("东京 Spiral", "公共路径能够把不同程序缝成室内城市", "展览、商业与文化活动围绕连续路径和中庭展开，复杂功能因清楚的空间序列而保持开放。", "03-spiral.jpg"),
            ("MIT Media Lab 新楼", "透明不是表皮，而是让知识交换可见", "实验空间、共享区域与中庭形成视线联系，研究活动不再被封闭房间完全隔开。", "04-media-lab.jpg"),
            ("纽约世贸中心四号楼", "克制的单体也可以通过反射进入城市整体", "玻璃表面随天空与周边变化，塔楼以简洁体量减少视觉竞争，把纪念性留给更大的场所关系。", "05-four-wtc.jpg"),
        ],
        "summary": "好城市不是把建筑排整齐，而是让不同时间完成的片段持续对话。",
        "chain": ["单体", "缝隙", "路径", "街区", "时间"],
        "methods": ["把项目分期当作设计变量", "先画建筑之间的公共路径", "让边界容纳未来项目继续接入"],
        "endcards": {
            "01": {"layout_rationale": "书封在上部居中放大，Hillside Terrace 作为底部城市带，问题标题沿两者之间的时间轴展开。", "changed_variables": ["上中大书封", "底部街景带", "横向时间轴标题", "中央留白"]},
            "06": {"layout_rationale": "五个城市片段沿折线路径跨越画面，三条方法分别挂接在缝隙、街区与时间节点。", "changed_variables": ["折线时间路径", "分期街区块", "节点式方法", "大面积浅底"]},
        },
        "publish_title": "好城市，为什么不能一次设计完成？",
        "publish_body": "《Nurturing Dreams》收集了槙文彦关于建筑与城市的长期思考。它反复提醒：城市品质不只来自优秀单体，更来自建筑之间的缝隙、路径与时间。代官山 Hillside Terrace 跨越二十多年分期完成，用低层体量、庭院和通道累积街区关系；Spiral 把展览、商业和文化活动缝进连续的室内路径；MIT Media Lab 新楼通过共享空间与视线联系，让研究交换被看见；世贸中心四号楼则以克制体量和反射表面进入更大的城市与纪念场所。对设计师而言，最值得借鉴的是把“未完成”纳入方法：将分期视为设计变量，先画建筑之间的公共路径，再让边界能接纳未来项目。好城市并非一次完成的总图，而是不同时间的片段仍能继续对话。本文为编辑性阅读，不是原书逐字引语。你的项目边界，是否给下一次建设留下了连接机会？",
        "tags": "#槙文彦 #NurturingDreams #群体形式 #城市设计 #公共空间 #建筑理论 #建筑书单 #建筑学生",
    },
}


def palette(book):
    return {key: base.hex_rgb(value) for key, value in book["palette"].items()}


def darken(image: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Brightness(image.convert("RGB")).enhance(factor)


def cover_fathy(book, assets: Path) -> Image.Image:
    c = palette(book)
    photo = base.crop(base.open_image(assets / "02-new-gourna-mosque.jpg"), (W, H), (0.48, 0.5))
    image = darken(photo, 0.58)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 620, H), fill=c["ink"])
    draw.pieslice((405, 160, 1095, 850), 180, 360, fill=c["accent"])
    draw.rectangle((405, 505, 1095, 1410), fill=c["accent"])
    draw.pieslice((470, 225, 1030, 785), 180, 360, fill=c["paper"])
    draw.rectangle((470, 505, 1030, 1345), fill=c["paper"])
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (525, 285, 985, 1175), shadow=True)
    draw.text((74, 66), book["designer_en"], font=base.get_font(28, bold=True), fill=c["warm"])
    base.text_block(draw, (70, 220), "低成本建筑，\n为什么要先学\n当地方法？", base.get_font(61, bold=True), c["paper"], 500, 8)
    base.text_block(draw, (72, 670), book["thesis"], base.get_font(28), c["paper"], 310, 11)
    draw.line((72, 1040, 365, 1040), fill=c["accent"], width=10)
    draw.text((72, 1080), book["book_cn"], font=base.get_font(31, bold=True), fill=c["warm"])
    draw.text((72, 1515), "土 / 气候 / 工匠", font=base.get_font(24, bold=True), fill=c["paper"])
    base.draw_page_mark(draw, 1, c["ink"], light=True)
    return image


def cover_kurokawa(book, assets: Path) -> Image.Image:
    c = palette(book)
    image = Image.new("RGB", (W, H), c["ink"])
    draw = ImageDraw.Draw(image)
    photo = base.crop(base.open_image(assets / "02-nakagin.jpg"), (W, 900), (0.52, 0.5))
    image.paste(photo, (0, 0))
    draw.rectangle((0, 865, W, 915), fill=c["accent"])
    for x, y, radius in ((875, 970, 115), (1080, 1140, 80), (790, 1380, 52)):
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline=c["second"], width=12)
        draw.ellipse((x-18, y-18, x+18, y+18), fill=c["warm"])
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (78, 305, 610, 1255), shadow=True)
    draw.rectangle((650, 955, 1165, 1008), fill=c["accent"])
    draw.text((72, 58), book["designer_en"], font=base.get_font(28, bold=True), fill=c["paper"])
    base.text_block(draw, (650, 1045), "建筑能像细胞一样\n替换和生长吗？", base.get_font(55, bold=True), c["paper"], 520, 9)
    base.text_block(draw, (650, 1310), book["thesis"], base.get_font(27), c["paper"], 470, 10)
    draw.text((72, 1515), book["book_cn"], font=base.get_font(30, bold=True), fill=c["accent"])
    base.draw_page_mark(draw, 1, c["ink"], light=True)
    return image


def cover_maki(book, assets: Path) -> Image.Image:
    c = palette(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    photo = base.crop(base.open_image(assets / "02-hillside-terrace.jpg"), (W, 600), (0.5, 0.58))
    image.paste(photo, (0, 1060))
    draw.rectangle((0, 1028, W, 1060), fill=c["accent"])
    draw.line((85, 875, 1135, 875), fill=c["second"], width=8)
    for x, color in ((120, c["accent"]), (520, c["warm"]), (930, c["second"])):
        draw.ellipse((x-18, 857, x+18, 893), fill=color)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (370, 95, 875, 805), shadow=True)
    draw.text((72, 58), book["designer_en"], font=base.get_font(28, bold=True), fill=c["second"])
    base.text_block(draw, (72, 900), "一栋建筑，怎么成为一段城市关系？", base.get_font(56, bold=True), c["ink"], 1080, 7)
    base.text_block(draw, (690, 760), book["thesis"], base.get_font(27), c["ink"], 440, 10)
    draw.rectangle((70, 1480, 420, 1540), fill=c["ink"])
    draw.text((88, 1492), book["book_cn"], font=base.get_font(27, bold=True), fill=c["paper"])
    base.draw_page_mark(draw, 1, c["ink"])
    return image


def interior(book, assets: Path, number: int) -> Image.Image:
    c = palette(book)
    title, headline, body, filename = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    source = base.open_image(assets / filename)
    if book["system"] == "earth-vault":
        photo = base.crop(source, (W, 960), (0.5, 0.5))
        image.paste(photo, (0, 0))
        draw.rectangle((0, 960, W, 1005), fill=c["accent"])
        draw.arc((70, 865, 240, 1035), 180, 360, fill=c["warm"], width=12)
        draw.rectangle((70, 885, 240, 1005), outline=c["warm"], width=0)
    elif book["system"] == "plug-in-capsules":
        photo = base.crop(source, (W - 145, 950), (0.5, 0.5))
        image.paste(photo, (145, 0))
        draw.rectangle((0, 0, 145, 950), fill=c["ink"])
        for y in range(85, 850, 155):
            draw.ellipse((45, y, 100, y + 55), outline=c["accent"] if (y // 155) % 2 else c["second"], width=7)
        draw.rectangle((0, 950, W, 1005), fill=c["accent"])
    else:
        photo = base.crop(source, (W, 900), (0.5, 0.5))
        image.paste(photo, (0, 0))
        draw.rectangle((0, 900, W, 1005), fill=c["ink"])
        draw.line((70, 952, 1170, 952), fill=c["paper"], width=4)
        for x in (130, 450, 780, 1100):
            draw.ellipse((x-13, 939, x+13, 965), fill=c["accent"] if x in (450, 1100) else c["warm"])
    draw.rectangle((72, 835, 610, 920), fill=c["ink"])
    draw.text((96, 852), title, font=base.get_font(30, bold=True), fill=c["paper"])
    y = base.text_block(draw, (75, 1080), headline, base.get_font(50, bold=True), c["ink"], 1080, 8)
    base.text_block(draw, (78, y + 32), body, base.get_font(30), c["ink"], 1010, 11)
    draw.text((78, 1550), book["designer_en"], font=base.get_font(18, bold=True), fill=c["accent"])
    base.draw_page_mark(draw, number, c["ink"])
    return image


def summary_fathy(book) -> Image.Image:
    c = palette(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((72, 78), "节省，不等于删掉质量", font=base.get_font(63, bold=True), fill=c["ink"])
    base.text_block(draw, (75, 175), book["summary"], base.get_font(29), c["second"], 980, 10)
    method_positions = ((75, 300), (430, 300), (790, 300))
    for i, (method, xy) in enumerate(zip(book["methods"], method_positions), 1):
        draw.text(xy, f"0{i}", font=base.get_font(24, bold=True), fill=c["accent"])
        base.text_block(draw, (xy[0] + 48, xy[1]), method, base.get_font(23), c["ink"], 285, 7)
    spans = [(70, 520, 280), (275, 650, 505), (500, 780, 750), (745, 910, 995), (990, 1040, 1170)]
    for i, ((x0, top, x1), label) in enumerate(zip(spans, book["chain"])):
        width = x1 - x0
        draw.arc((x0, top, x1, top + width), 180, 360, fill=c["accent"] if i % 2 else c["second"], width=18)
        draw.line((x0, top + width // 2, x0, 1480), fill=c["ink"], width=5)
        draw.line((x1, top + width // 2, x1, 1480), fill=c["ink"], width=5)
        draw.text((x0 + 15, top + width // 2 + 28), label, font=base.get_font(27, bold=True), fill=c["ink"])
    draw.rectangle((70, 1480, 1170, 1518), fill=c["warm"])
    base.draw_page_mark(draw, 6, c["ink"])
    return image


def summary_kurokawa(book) -> Image.Image:
    c = palette(book)
    image = Image.new("RGB", (W, H), c["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((72, 78), "变化，要先设计接口", font=base.get_font(64, bold=True), fill=c["paper"])
    base.text_block(draw, (76, 175), book["summary"], base.get_font(29), c["warm"], 970, 10)
    core_x0, core_x1 = 548, 692
    draw.rectangle((core_x0, 360, core_x1, 1510), fill=c["second"])
    for i, (label, y) in enumerate(zip(book["chain"], (420, 625, 830, 1035, 1240))):
        draw.ellipse((584, y, 656, y + 72), fill=c["warm"])
        label_font = base.get_font(27, bold=True)
        if i < 3:
            label_x = 710
        else:
            label_width = draw.textbbox((0, 0), label, font=label_font)[2]
            label_x = core_x0 - label_width - 22
        draw.text((label_x, y + 13), label, font=label_font, fill=c["paper"])
        if i < 3:
            box = (70, y - 45, 500, y + 130)
        else:
            box = (742, y - 45, 1170, y + 130)
        draw.rounded_rectangle(box, radius=6, fill=c["accent"] if i % 2 else c["paper"], outline=c["warm"], width=4)
        draw.line((box[2] if i < 3 else box[0], y + 36, core_x0 if i < 3 else core_x1, y + 36), fill=c["warm"], width=8)
        if i in (0, 2, 4):
            method = book["methods"][i // 2]
            base.text_block(draw, (box[0] + 24, box[1] + 25), method, base.get_font(24), c["ink"], box[2] - box[0] - 48, 7)
        else:
            draw.ellipse((box[0] + 28, box[1] + 45, box[0] + 98, box[1] + 115), outline=c["ink"], width=8)
    base.draw_page_mark(draw, 6, c["ink"], light=True)
    return image


def summary_maki(book) -> Image.Image:
    c = palette(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((72, 78), "城市，是被时间接续的关系", font=base.get_font(61, bold=True), fill=c["ink"])
    base.text_block(draw, (75, 175), book["summary"], base.get_font(29), c["second"], 920, 10)
    points = [(105, 1180), (330, 920), (570, 1060), (820, 690), (1100, 440)]
    draw.line(points, fill=c["accent"], width=14, joint="curve")
    block_sizes = [(180, 240), (210, 290), (235, 250), (220, 315), (155, 220)]
    for i, ((x, y), (bw, bh), label) in enumerate(zip(points, block_sizes, book["chain"])):
        box = (x - bw // 2, y - bh // 2, x + bw // 2, y + bh // 2)
        fill = c["second"] if i % 2 == 0 else c["warm"]
        draw.rectangle(box, fill=fill, outline=c["ink"], width=5)
        draw.text((box[0] + 18, box[1] + 18), f"{i + 1:02d}", font=base.get_font(22, bold=True), fill=c["paper"] if i % 2 == 0 else c["ink"])
        draw.text((box[0] + 18, box[3] - 58), label, font=base.get_font(27, bold=True), fill=c["paper"] if i % 2 == 0 else c["ink"])
    for i, (method, xy) in enumerate(zip(book["methods"], ((80, 350), (410, 480), (700, 1250))), 1):
        draw.text(xy, f"0{i}", font=base.get_font(24, bold=True), fill=c["accent"])
        base.text_block(draw, (xy[0] + 48, xy[1]), method, base.get_font(25), c["ink"], 360, 8)
    base.draw_page_mark(draw, 6, c["ink"])
    return image


def write_docs(book, assets: Path, output: Path) -> None:
    manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    source_lines = [
        "# 图片来源",
        "",
        "| 文件名 | 内容 | 作者/机构 | 来源 URL | 许可 | 许可链接 | 修改 |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in manifest:
        source_lines.append(
            f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item.get('license_url', '')} | {item['modifications']} |"
        )
    source_lines += [
        "",
        "书封仅用于书籍识别、介绍与评论；版权归原权利人。商业投放前请重新核验所在地与平台规则。",
        "卡片文字为基于书籍与案例资料的编辑性概括，不作为原书直接引语。",
    ]
    (output / "图片来源.md").write_text("\n".join(source_lines) + "\n", encoding="utf-8")
    publish = (
        f"# 标题\n\n{book['publish_title']}\n\n"
        f"# 正文\n\n{book['publish_body']}\n\n"
        f"# 标签\n\n{book['tags']}\n\n"
        f"# 版本\n\n{book['book']}｜{book['edition']}\n"
    )
    (output / "发布文案.md").write_text(publish, encoding="utf-8")
    post = {
        "designer": book["designer"],
        "book": book["book"],
        "edition": book["edition"],
        "thesis": book["thesis"],
        "concept_chain": book["chain"],
        "cards": [
            {"number": "01", "role": "problem cover", "headline": book["question"], "asset": "cover.jpg"},
            *[
                {
                    "number": f"{index:02d}",
                    "role": "mechanism" if index == 2 else "evidence",
                    "headline": card[1],
                    "evidence": card[0],
                    "asset": card[3],
                }
                for index, card in enumerate(book["cards"], 2)
            ],
            {"number": "06", "role": "synthesis", "headline": book["summary"], "asset": ""},
        ],
        "endcards": book["endcards"],
        "transferable_methods": book["methods"],
        "sources": manifest,
    }
    (output / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    previews: list[Path] = []
    for slug, book in BOOKS.items():
        assets = ASSET_ROOT / slug
        output = OUTPUT_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        if book["system"] == "earth-vault":
            first, last = cover_fathy(book, assets), summary_fathy(book)
        elif book["system"] == "plug-in-capsules":
            first, last = cover_kurokawa(book, assets), summary_kurokawa(book)
        else:
            first, last = cover_maki(book, assets), summary_maki(book)
        cards = [first, *[interior(book, assets, number) for number in range(2, 6)], last]
        paths: list[Path] = []
        for number, card in enumerate(cards, 1):
            path = output / f"{number:02d}.jpg"
            base.save(card, path)
            paths.append(path)
        base.preview(paths, output / "preview.jpg")
        write_docs(book, assets, output)
        previews.append(output / "preview.jpg")
        print(f"Rendered {slug}")
    contact = Image.new("RGB", (1242, 3500), (225, 225, 220))
    y = 36
    for path in previews:
        with Image.open(path) as source:
            strip = source.convert("RGB").resize((1160, 1035), Image.Resampling.LANCZOS)
        contact.paste(strip, (41, y))
        y += 1140
    base.save(contact, OUTPUT_ROOT / "总预览.jpg")


if __name__ == "__main__":
    main()
