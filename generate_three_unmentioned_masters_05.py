#!/usr/bin/env python3
"""Render batch 05: Loos, Breuer and Saarinen book-card posts."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters-05"
OUTPUT_ROOT = ROOT / "output" / "three-unmentioned-masters-05"
W, H = base.W, base.H


BOOKS = {
    "adolf-loos-ornament-and-crime": {
        "designer": "阿道夫·路斯",
        "designer_en": "ADOLF LOOS",
        "book": "Ornament and Crime",
        "book_cn": "《装饰与罪恶》",
        "edition": "Ariadne Press, 1997｜ISBN 9781572410466",
        "question": "去掉装饰，空间为什么反而更丰富？",
        "thesis": "路斯反对的不是美，而是把劳动浪费在附加表面；材料、比例与空间层级仍然可以极其丰厚。",
        "system": "raumplan-cut",
        "palette": {"paper": "#EEE9DE", "ink": "#17211D", "accent": "#E9482B", "second": "#426D62", "warm": "#D9B965"},
        "cards": [
            ("维也纳 Looshaus", "克制的外表，不等于贫乏的建筑", "上部住宅立面压低装饰存在感，首层商业空间则以石材明确城市尺度。价值从表面图案转向材料、开口和功能层级。", "02-looshaus-exterior.jpg"),
            ("American Bar", "材料本身，就能制造足够的密度", "镜面、木材、黄铜与格状天花把极小室内扩展成多层次场景。丰富感来自真实材料和精确比例，而非贴上去的纹样。", "03-american-bar.jpg"),
            ("Steiner House", "立面可以先回应条件，再决定表情", "临街一面保持克制，花园一侧则释放体量与开口。建筑不必用同一种风格包裹所有方向，而应让限制进入形式。", "04-steiner-house.jpg"),
            ("Villa Müller", "剖面关系，比统一楼层更接近生活", "Raumplan 以不同层高和错接平台组织房间，让视觉、动线与私密度在立体方向上连续变化。空间成为真正的主角。", "05-villa-muller.jpg"),
        ],
        "summary": "反装饰不是反对美，而是把价值从附加表面转回材料、比例与空间。",
        "chain": ["表面", "材料", "比例", "层高", "生活"],
        "methods": ["先判断哪些表面会快速过时", "用材料本身的纹理代替附加图案", "通过剖面和层高制造空间差异"],
        "endcards": {
            "01": {"layout_rationale": "Looshaus 暗化为整页背景，真实书封在右侧放大成为主角；左侧以切开的深色剖面容纳问题标题。", "changed_variables": ["右侧大书封", "深浅剖面切割", "左侧问题标题", "材料色块"]},
            "06": {"layout_rationale": "五个错层房间形成 Raumplan 剖面，概念链沿层高上升，三条方法分别落在不同房间。", "changed_variables": ["错层剖面", "房间式方法卡", "垂直概念链", "留白底色"]},
        },
        "publish_title": "去掉装饰，空间为什么反而更丰富？",
        "publish_body": "《Ornament and Crime》常被压缩成一句“反对装饰”，但路斯真正追问的是：设计价值应该放在哪里？Looshaus 让上部立面保持克制，却用石材把商业首层稳稳压在城市尺度上；American Bar 依靠镜面、木材、黄铜和天花比例，在极小面积里形成浓密体验；Steiner House 让临街与花园两侧分别回应不同条件；Villa Müller 更通过 Raumplan 把房间按层高、视线与私密度立体错接。对设计师最有用的不是复制光秃立面，而是改变投入顺序：先删掉会快速过时的附加表面，再让材料本身说话，最后用剖面和比例制造差异。反装饰并非反对美，而是把美从图案转回真实空间。本文为编辑性概括，不是原书逐字引语。你的项目里，哪些“装饰”其实可以被更好的空间关系替代？",
        "tags": "#阿道夫路斯 #OrnamentAndCrime #装饰与罪恶 #Raumplan #现代建筑 #建筑理论 #建筑书单 #设计方法",
    },
    "marcel-breuer-sun-and-shadow": {
        "designer": "马塞尔·布劳耶",
        "designer_en": "MARCEL BREUER",
        "book": "Sun and Shadow",
        "book_cn": "《阳光与阴影》",
        "edition": "Dodd, Mead, 1955",
        "question": "现代建筑，为什么需要同时容纳对立？",
        "thesis": "轻与重、开放与庇护、工业构件与粗粝材料，不必被统一成一种表情。",
        "system": "sun-shadow-balance",
        "palette": {"paper": "#F0E7D2", "ink": "#14263A", "accent": "#F0A929", "second": "#2B69A1", "warm": "#C95C42"},
        "cards": [
            ("Breuer House II", "轻结构与重基座，可以同时成立", "悬挑居住体量跨在石砌基座之上：开放视野与被保护的入口、工业构件与粗粝材料被安排在同一截面中。", "02-breuer-house-ii.jpg"),
            ("原 Whitney Museum", "厚重体量，也能靠悬挑获得方向", "倒置阶梯般的石质体量向街道伸出，深窗与架空入口控制光影。重量并未被隐藏，而是被结构转化为城市姿态。", "03-whitney.jpg"),
            ("Saint John's Abbey Church", "纪念性来自光与结构的共同工作", "巨大的混凝土旗帜、彩色玻璃与仪式性进深，把庇护和明亮同时推到极致。材料重量反而让光更可见。", "04-st-johns.jpg"),
            ("Atlanta Central Library", "阴影不是缺少光，而是组织公共界面", "深凹开口与厚重混凝土控制日照，也让公共建筑在城市中获得清楚轮廓。立面同时承担气候与象征任务。", "05-atlanta-library.jpg"),
        ],
        "summary": "成熟的现代主义，不是消除矛盾，而是让对立力量在结构与空间中保持平衡。",
        "chain": ["光 / 影", "轻 / 重", "开放 / 庇护", "工业 / 手工", "单体 / 城市"],
        "methods": ["用截面安排受光与遮阴", "让轻结构与重材料各自承担任务", "把矛盾转成明确的构造关系"],
        "endcards": {
            "01": {"layout_rationale": "对角线将整页切成阳光与阴影两场，真实书封纵向放大跨过分界，问题标题沿右侧亮区展开。", "changed_variables": ["对角明暗场", "跨界大书封", "右侧标题", "底部项目影像"]},
            "06": {"layout_rationale": "中央平衡梁连接五组对立概念，三条方法成为上下不同重量的构造块。", "changed_variables": ["平衡梁", "成对概念", "悬挂式方法卡", "深蓝背景"]},
        },
        "publish_title": "现代建筑，为什么需要同时容纳对立？",
        "publish_body": "《Sun and Shadow》不是让现代主义变得更统一，而是提醒我们：空间的力量常来自对立被同时保留。Breuer House II 把轻盈悬挑架在石砌基座上，让开放视野与庇护入口共存；原 Whitney Museum 用倒置阶梯般的石质体量、深窗与悬挑，把重量变成明确的城市方向；Saint John's Abbey Church 让混凝土旗帜、彩色玻璃和仪式性进深共同塑造光；Atlanta Central Library 则以厚重立面和深凹开口同时回应日照与公共形象。布劳耶的方法不是折中，而是分配任务：用截面决定光与影，让轻结构和重材料分别承担作用，再把矛盾落实成可读的构造关系。成熟的现代主义并不消除冲突，而是让冲突保持张力。本文为编辑性概括，不是原书逐字引语。你的设计里，哪一组对立值得被保留下来？",
        "tags": "#马塞尔布劳耶 #SunAndShadow #现代主义建筑 #粗野主义 #建筑构造 #建筑理论 #建筑书单 #设计方法",
    },
    "eero-saarinen-on-his-work": {
        "designer": "埃罗·沙里宁",
        "designer_en": "EERO SAARINEN",
        "book": "Eero Saarinen on His Work",
        "book_cn": "《埃罗·沙里宁谈自己的作品》",
        "edition": "Yale University Press, 1968｜ISBN 0300008775",
        "question": "每个项目，都应该拥有不同的建筑语言吗？",
        "thesis": "统一风格不重要；形式必须把机构、运动与公共象征压缩成清楚的整体。",
        "system": "singular-silhouette",
        "palette": {"paper": "#F3EEDC", "ink": "#152A45", "accent": "#E44735", "second": "#3B78A8", "warm": "#F0C64D"},
        "cards": [
            ("TWA Flight Center", "把移动写进轮廓，空间就会获得速度", "连续壳体、分叉流线与低伏入口把旅客从抵达推向登机。形式不是比喻装饰，而是对移动体验的压缩。", "02-twa.jpg"),
            ("Gateway Arch", "一个精确轮廓，可以承担公共记忆", "拱门把纪念物压缩成单一曲线，结构、尺度与城市识别合为一体。几乎没有次要语言，却拥有极强象征。", "03-gateway-arch.jpg"),
            ("Dulles International Airport", "屋顶结构可以直接组织抵达动作", "悬索屋面与倾斜柱列围出连续大厅，让车辆抵达、旅客进入和远处视线被同一条轮廓串联。", "04-dulles.jpg"),
            ("Kresge Auditorium", "薄壳不是造型，而是覆盖集体的方式", "三角球面薄壳以少量支点覆盖大跨公共内部。结构效率直接生成建筑最容易被记住的整体形象。", "05-kresge.jpg"),
        ],
        "summary": "一致性不必来自相同造型，而可以来自每次都为问题找到最清楚的整体形式。",
        "chain": ["任务", "运动", "结构", "轮廓", "象征"],
        "methods": ["先把项目最重要的动作压成一句话", "让结构直接参与主轮廓", "删除不能强化整体识别的次要形式"],
        "endcards": {
            "01": {"layout_rationale": "TWA 曲线铺满背景，真实书封放大占据左下，问题标题悬在右上并由一条连续轨迹连接。", "changed_variables": ["左下大书封", "满幅曲线影像", "右上问题标题", "连续运动轨迹"]},
            "06": {"layout_rationale": "五道不同轮廓的门沿连续路径展开，概念链逐级通过，三条方法像目的地落在路径转折处。", "changed_variables": ["轮廓门序列", "曲线路径", "转折式方法卡", "浅色场"]},
        },
        "publish_title": "每个项目，都应该拥有不同的建筑语言吗？",
        "publish_body": "《Eero Saarinen on His Work》让人重新思考“个人风格”是否必须表现为同一种造型。TWA Flight Center 用连续壳体和分叉流线，把旅客移动压成具有速度感的整体；Gateway Arch 以一条精确曲线统一结构、纪念与城市识别；Dulles International Airport 让悬索屋面和倾斜柱列直接组织抵达；Kresge Auditorium 则用三角球面薄壳覆盖集体空间，并由结构本身生成轮廓。这些作品外形并不相似，却共享同一工作方式：先把项目最重要的动作说清楚，让结构参与主轮廓，再删除不能强化整体识别的次要形式。一致性未必来自重复语言，也可以来自每次都把问题压缩得足够清楚。本文为编辑性概括，不是原书逐字引语。你的项目最值得被看见的那个“动作”是什么？",
        "tags": "#埃罗沙里宁 #EeroSaarinen #TWAFlightCenter #GatewayArch #薄壳结构 #建筑理论 #建筑书单 #设计方法",
    },
}


def colors(book):
    return {key: base.hex_rgb(value) for key, value in book["palette"].items()}


def toned(image: Image.Image, brightness: float = 1.0, saturation: float = 1.0) -> Image.Image:
    result = image.convert("RGB")
    result = ImageEnhance.Color(result).enhance(saturation)
    return ImageEnhance.Brightness(result).enhance(brightness)


def shadow_cover(canvas: Image.Image, cover: Image.Image, box: tuple[int, int, int, int]) -> None:
    base.paste_cover(canvas, cover, box, shadow=True)


def cover_loos(book, assets: Path) -> Image.Image:
    c = colors(book)
    photo = base.crop(base.open_image(assets / "02-looshaus-exterior.jpg"), (W, H), (0.5, 0.48))
    image = toned(photo, 0.43, 0.62)
    draw = ImageDraw.Draw(image)
    draw.polygon([(0, 0), (575, 0), (465, H), (0, H)], fill=c["ink"])
    draw.polygon([(0, 1125), (470, 1035), (445, 1445), (0, 1530)], fill=c["second"])
    draw.rectangle((0, 0, W, 34), fill=c["accent"])
    draw.text((64, 72), book["designer_en"], font=base.get_font(28, bold=True), fill=c["warm"])
    draw.text((64, 115), "01  /  THEORY BOOK", font=base.get_font(19, bold=True), fill=c["paper"])
    base.text_block(draw, (60, 245), "去掉装饰，\n空间为什么\n反而更丰富？", base.get_font(61, bold=True), c["paper"], 430, 7)
    base.text_block(draw, (62, 680), book["thesis"], base.get_font(27), c["paper"], 350, 10)
    draw.line((62, 1015, 355, 1015), fill=c["accent"], width=12)
    shadow_cover(image, base.open_image(assets / "cover.jpg"), (545, 250, 1170, 1265))
    draw.rectangle((610, 1315, 1135, 1372), fill=c["paper"])
    draw.text((634, 1328), "VERIFIED BOOK COVER · 1997", font=base.get_font(19, bold=True), fill=c["ink"])
    draw.text((64, 1512), book["book_cn"], font=base.get_font(28, bold=True), fill=c["warm"])
    base.draw_page_mark(draw, 1, c["ink"], light=True)
    return image


def cover_breuer(book, assets: Path) -> Image.Image:
    c = colors(book)
    image = Image.new("RGB", (W, H), c["ink"])
    draw = ImageDraw.Draw(image)
    draw.polygon([(0, 0), (W, 0), (W, 690), (0, 1265)], fill=c["accent"])
    draw.polygon([(690, 410), (W, 205), (W, H), (885, H)], fill=c["second"])
    photo = toned(base.crop(base.open_image(assets / "02-breuer-house-ii.jpg"), (640, 450), (0.52, 0.54)), 0.78, 0.65)
    image.paste(photo, (602, 1210))
    draw.line((0, 1265, W, 690), fill=c["paper"], width=10)
    shadow_cover(image, base.open_image(assets / "cover.jpg"), (80, 235, 690, 1265))
    draw.text((70, 66), book["designer_en"], font=base.get_font(28, bold=True), fill=c["paper"])
    draw.text((70, 110), "SUN / SHADOW · 01", font=base.get_font(20, bold=True), fill=c["ink"])
    base.text_block(draw, (735, 520), "现代建筑，\n为什么需要\n同时容纳对立？", base.get_font(57, bold=True), c["paper"], 430, 7)
    draw.rectangle((720, 810, 1190, 1005), fill=c["second"])
    base.text_block(draw, (744, 840), book["thesis"], base.get_font(27), c["paper"], 405, 10)
    draw.rectangle((80, 1315, 608, 1372), fill=c["paper"])
    draw.text((104, 1328), "VERIFIED BOOK COVER · 1955", font=base.get_font(19, bold=True), fill=c["ink"])
    draw.text((72, 1520), book["book_cn"], font=base.get_font(29, bold=True), fill=c["accent"])
    base.draw_page_mark(draw, 1, c["ink"], light=True)
    return image


def cover_saarinen(book, assets: Path) -> Image.Image:
    c = colors(book)
    photo = base.crop(base.open_image(assets / "02-twa.jpg"), (W, H), (0.5, 0.52))
    image = toned(photo, 0.62, 0.75)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 470), fill=c["ink"])
    draw.pieslice((-420, 250, 800, 1470), 205, 338, fill=c["paper"])
    draw.pieslice((-300, 365, 670, 1335), 205, 338, fill=c["accent"])
    draw.pieslice((-215, 445, 570, 1230), 205, 338, fill=c["paper"])
    shadow_cover(image, base.open_image(assets / "cover.jpg"), (78, 505, 650, 1450))
    draw.text((70, 64), book["designer_en"], font=base.get_font(28, bold=True), fill=c["warm"])
    draw.text((70, 108), "01  /  ONE PROBLEM · ONE FORM", font=base.get_font(19, bold=True), fill=c["paper"])
    base.text_block(draw, (555, 175), "每个项目，\n都应该拥有不同的\n建筑语言吗？", base.get_font(55, bold=True), c["paper"], 610, 6)
    draw.rectangle((700, 600, 1180, 825), fill=c["paper"])
    base.text_block(draw, (725, 635), book["thesis"], base.get_font(27), c["ink"], 420, 10)
    draw.line((730, 1010, 1145, 1010), fill=c["accent"], width=12)
    draw.rectangle((720, 1060, 1155, 1117), fill=c["paper"])
    draw.text((741, 1073), "VERIFIED COVER · 1968", font=base.get_font(19, bold=True), fill=c["ink"])
    draw.text((720, 1165), book["book_cn"], font=base.get_font(27, bold=True), fill=c["paper"])
    base.draw_page_mark(draw, 1, c["ink"], light=True)
    return image


def interior(book, assets: Path, number: int) -> Image.Image:
    c = colors(book)
    title, headline, body, filename = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    source = base.open_image(assets / filename)
    system = book["system"]
    if system == "raumplan-cut":
        photo = base.crop(source, (W - 170, 920), (0.5, 0.5))
        image.paste(photo, (170, 0))
        draw.rectangle((0, 0, 170, 920), fill=c["ink"])
        step = 220 + (number - 2) * 72
        draw.rectangle((35, 120, 135, step), fill=c["accent"])
        draw.rectangle((35, step + 36, 135, 820), outline=c["warm"], width=7)
        draw.line((170, 920, W, 920), fill=c["accent"], width=22)
    elif system == "sun-shadow-balance":
        photo = base.crop(source, (W, 930), (0.5, 0.5))
        image.paste(photo, (0, 0))
        draw.polygon([(0, 0), (260, 0), (610, 930), (0, 930)], fill=c["ink"])
        draw.polygon([(W, 0), (W, 930), (1030, 930), (790, 0)], fill=c["accent"])
        draw.line((0, 930, W, 930), fill=c["accent"], width=22)
    else:
        photo = base.crop(source, (W, 930), (0.5, 0.5))
        image.paste(photo, (0, 0))
        draw.arc((-190, 520, 1430, 1230), 186, 350, fill=c["paper"], width=36)
        draw.arc((-160, 555, 1400, 1195), 186, 350, fill=c["accent"], width=12)
        draw.rectangle((0, 915, W, 955), fill=c["ink"])
    draw.rectangle((70, 820, 650, 905), fill=c["ink"])
    draw.text((94, 838), title, font=base.get_font(29, bold=True), fill=c["paper"])
    draw.text((74, 1000), f"0{number}", font=base.get_font(28, bold=True), fill=c["accent"])
    y = base.text_block(draw, (74, 1055), headline, base.get_font(49, bold=True), c["ink"], 1075, 7)
    base.text_block(draw, (77, y + 32), body, base.get_font(30), c["ink"], 1015, 11)
    draw.text((78, 1550), book["designer_en"], font=base.get_font(18, bold=True), fill=c["second"])
    base.draw_page_mark(draw, number, c["ink"])
    return image


def summary_loos(book) -> Image.Image:
    c = colors(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((70, 72), "价值，要回到空间内部", font=base.get_font(62, bold=True), fill=c["ink"])
    base.text_block(draw, (74, 168), book["summary"], base.get_font(29), c["second"], 965, 10)
    rooms = [(75, 520, 400, 900), (400, 410, 735, 785), (735, 590, 1170, 980), (170, 900, 585, 1260), (585, 980, 1075, 1490)]
    fills = [c["second"], c["warm"], c["ink"], c["accent"], c["second"]]
    for i, (box, label, fill) in enumerate(zip(rooms, book["chain"], fills)):
        draw.rectangle(box, fill=fill, outline=c["paper"], width=10)
        draw.text((box[0] + 22, box[1] + 18), f"0{i+1}", font=base.get_font(20, bold=True), fill=c["paper"] if i != 1 else c["ink"])
        draw.text((box[0] + 22, box[3] - 58), label, font=base.get_font(28, bold=True), fill=c["paper"] if i != 1 else c["ink"])
    positions = [(95, 610, 270), (435, 500, 275), (760, 690, 350)]
    for i, (method, (x, y, width)) in enumerate(zip(book["methods"], positions), 1):
        draw.text((x, y), f"METHOD {i}", font=base.get_font(17, bold=True), fill=c["paper"] if i != 2 else c["ink"])
        base.text_block(draw, (x, y + 34), method, base.get_font(23, bold=True), c["paper"] if i != 2 else c["ink"], width, 7)
    draw.line((405, 410, 405, 1490), fill=c["paper"], width=6)
    base.draw_page_mark(draw, 6, c["ink"])
    return image


def summary_breuer(book) -> Image.Image:
    c = colors(book)
    image = Image.new("RGB", (W, H), c["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((70, 72), "矛盾，不必被消除", font=base.get_font(64, bold=True), fill=c["paper"])
    base.text_block(draw, (74, 170), book["summary"], base.get_font(29), c["warm"], 1000, 10)
    beam_y = 890
    draw.line((95, beam_y, 1145, beam_y), fill=c["accent"], width=22)
    draw.polygon([(570, beam_y + 10), (670, beam_y + 10), (620, 1030)], fill=c["paper"])
    pair_y = [450, 560, 675, 1140, 1290]
    for i, (label, y) in enumerate(zip(book["chain"], pair_y)):
        x = 95 if i % 2 == 0 else 735
        w = 410
        draw.rounded_rectangle((x, y, x + w, y + 88), radius=10, fill=c["second"] if i < 3 else c["accent"])
        draw.text((x + 25, y + 24), label, font=base.get_font(28, bold=True), fill=c["paper"] if i < 3 else c["ink"])
        anchor = x + w // 2
        draw.line((anchor, y + 88 if y < beam_y else y, anchor, beam_y), fill=c["paper"], width=5)
    method_boxes = [(80, 1000, 410, 1115), (455, 1035, 785, 1150), (830, 1000, 1160, 1115)]
    for i, (method, box) in enumerate(zip(book["methods"], method_boxes), 1):
        draw.rectangle(box, fill=c["paper"] if i == 2 else c["second"], outline=c["accent"], width=5)
        base.text_block(draw, (box[0] + 18, box[1] + 18), f"0{i}  {method}", base.get_font(21, bold=True), c["ink"] if i == 2 else c["paper"], box[2] - box[0] - 36, 6)
    draw.text((74, 1515), "SUN / SHADOW · LIGHT / WEIGHT", font=base.get_font(20, bold=True), fill=c["accent"])
    base.draw_page_mark(draw, 6, c["ink"], light=True)
    return image


def summary_saarinen(book) -> Image.Image:
    c = colors(book)
    image = Image.new("RGB", (W, H), c["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((70, 72), "每个问题，都有自己的轮廓", font=base.get_font(58, bold=True), fill=c["ink"])
    base.text_block(draw, (74, 165), book["summary"], base.get_font(27), c["second"], 1080, 9)
    gate_x = [105, 330, 555, 780, 1005]
    gate_y = [1000, 810, 930, 650, 840]
    for i, (x, y, label) in enumerate(zip(gate_x, gate_y, book["chain"])):
        width, height = 170, 280
        color = c["accent"] if i in (0, 4) else c["second"]
        draw.arc((x - width // 2, y - height, x + width // 2, y), 180, 360, fill=color, width=18)
        draw.line((x - width // 2, y - height // 2, x - width // 2, y + 80), fill=color, width=18)
        draw.line((x + width // 2, y - height // 2, x + width // 2, y + 80), fill=color, width=18)
        draw.text((x - 45, y + 105), label, font=base.get_font(25, bold=True), fill=c["ink"])
    route = [(50, 1260), (250, 1110), (455, 1210), (680, 1040), (915, 1180), (1190, 1010)]
    draw.line(route, fill=c["warm"], width=14, joint="curve")
    for x, y in route[1:-1]:
        draw.ellipse((x - 14, y - 14, x + 14, y + 14), fill=c["accent"])
    methods_xy = [(75, 410), (445, 470), (790, 385)]
    for i, (method, (x, y)) in enumerate(zip(book["methods"], methods_xy), 1):
        draw.text((x, y), f"0{i}", font=base.get_font(23, bold=True), fill=c["accent"])
        base.text_block(draw, (x + 45, y), method, base.get_font(23, bold=True), c["ink"], 315, 7)
    draw.text((74, 1515), "TASK → MOVEMENT → STRUCTURE → SILHOUETTE", font=base.get_font(19, bold=True), fill=c["second"])
    base.draw_page_mark(draw, 6, c["ink"])
    return image


def write_docs(book, assets: Path, output: Path) -> None:
    manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    source_lines = [
        "# 图片来源", "",
        "| 文件名 | 内容 | 作者 / 机构 | 来源 URL | 许可 | 许可链接 | 修改 |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in manifest:
        source_lines.append(f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item.get('license_url', '')} | {item['modifications']} |")
    source_lines += [
        "", "书封仅用于书籍识别、介绍与评论；版权归原权利人。商业投放前请重新核验所在地与平台规则。",
        "卡片文字为基于书籍与案例资料的编辑性概括，不作为原书直接引语。",
    ]
    (output / "图片来源.md").write_text("\n".join(source_lines) + "\n", encoding="utf-8")
    publish = f"# 标题\n\n{book['publish_title']}\n\n# 正文\n\n{book['publish_body']}\n\n# 标签\n\n{book['tags']}\n\n# 版本\n\n{book['book']}｜{book['edition']}\n"
    (output / "发布文案.md").write_text(publish, encoding="utf-8")
    post = {
        "designer": book["designer"], "book": book["book"], "edition": book["edition"],
        "thesis": book["thesis"], "concept_chain": book["chain"],
        "cards": [
            {"number": "01", "role": "problem cover", "headline": book["question"], "asset": "cover.jpg"},
            *[{"number": f"{i:02d}", "role": "mechanism" if i == 2 else "evidence", "headline": card[1], "evidence": card[0], "asset": card[3]} for i, card in enumerate(book["cards"], 2)],
            {"number": "06", "role": "synthesis", "headline": book["summary"], "asset": ""},
        ],
        "endcards": book["endcards"], "transferable_methods": book["methods"], "sources": manifest,
    }
    (output / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    previews: list[Path] = []
    for slug, book in BOOKS.items():
        assets = ASSET_ROOT / slug
        output = OUTPUT_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        if book["system"] == "raumplan-cut":
            first, last = cover_loos(book, assets), summary_loos(book)
        elif book["system"] == "sun-shadow-balance":
            first, last = cover_breuer(book, assets), summary_breuer(book)
        else:
            first, last = cover_saarinen(book, assets), summary_saarinen(book)
        cards = [first, *[interior(book, assets, n) for n in range(2, 6)], last]
        paths: list[Path] = []
        for number, card in enumerate(cards, 1):
            path = output / f"{number:02d}.jpg"
            base.save(card, path)
            paths.append(path)
        base.preview(paths, output / "preview.jpg")
        write_docs(book, assets, output)
        previews.append(output / "preview.jpg")
        print(f"Rendered {slug}")
    contact = Image.new("RGB", (1242, 3500), (226, 224, 216))
    y = 36
    for path in previews:
        with Image.open(path) as source:
            strip = source.convert("RGB").resize((1160, 1035), Image.Resampling.LANCZOS)
        contact.paste(strip, (41, y))
        y += 1140
    base.save(contact, OUTPUT_ROOT / "总预览.jpg")


if __name__ == "__main__":
    main()
