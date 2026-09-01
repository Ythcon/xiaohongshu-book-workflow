#!/usr/bin/env python3
"""Render three custom six-card Xiaohongshu posts about previously unused masters."""

from __future__ import annotations

import json
import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "three-unmentioned-masters"
OUTPUT_ROOT = ROOT / "output" / "three-unmentioned-masters"
W, H = 1242, 1660


BOOKS = {
    "frank-lloyd-wright-natural-house": {
        "designer": "弗兰克·劳埃德·赖特",
        "designer_en": "FRANK LLOYD WRIGHT",
        "book": "The Natural House",
        "book_cn": "《自然住宅》",
        "edition": "Bramhall House, 1954｜Open Library work OL961857W",
        "question": "房子怎样从场地里长出来？",
        "thesis": "自然住宅不模仿风景；场地、材料、网格与日常生活共同生成空间。",
        "system": "organic-grid",
        "palette": {"paper": "#EEE8DA", "ink": "#1E211D", "accent": "#A5442F", "second": "#50624D", "warm": "#C99D63"},
        "cards": [
            ("流水别墅", "地形先决定建筑的水平秩序", "岩石、溪流与悬挑不是背景和物体，而被组织成同一套层叠关系。", "02-fallingwater.jpg"),
            ("雅各布斯第一住宅", "网格把低成本变成生活秩序", "Usonian 住宅用模数、炉心和转角平面压缩造价，同时保留空间的伸展感。", "03-jacobs-house.jpg"),
            ("西塔里埃森", "材料不是贴面，而是场地的延续", "沙漠石砌体、低矮屋面与遮阳让建筑接受气候，而不是隔绝气候。", "04-taliesin-west.jpg"),
            ("罗森鲍姆住宅", "日常动线围绕炉心展开", "连续屋檐、花园界面与可扩展平面，让住宅随家庭生活继续生长。", "05-rosenbaum-house.jpg"),
        ],
        "summary": "有机建筑不是一种外观，而是一套从场地进入结构、材料与生活的连续推理。",
        "chain": ["场地", "模数", "炉心", "材料", "生活"],
        "methods": ["先画地形与气候关系，再画体量", "用一个秩序同时约束结构与家具", "让材料保留重量、尺度与产地感"],
        "endcards": {
            "01": {"layout_rationale": "用横向地层和悬挑式标题模拟建筑从地形中生长，书封偏置在地层断面上。", "changed_variables": ["横向主轴", "右下书封", "上部大留白", "地层式图像裁切"]},
            "06": {"layout_rationale": "以炉心为中心向场地、模数、材料和生活放射，回应赖特住宅的组织方式。", "changed_variables": ["放射概念链", "中心结论", "环形方法节点", "深色底"]},
        },
        "publish_title": "赖特的房子，为什么像从土地里长出来？",
        "publish_body": "如果把赖特理解成几座造型特别的住宅，就会错过《The Natural House》真正有用的部分：有机建筑不是给房子套上“自然风”，而是让场地、结构、材料与生活服从同一个秩序。流水别墅把岩层、溪流和悬挑压成连续的水平关系；雅各布斯第一住宅用模数与炉心，把低成本住宅组织得既紧凑又舒展；西塔里埃森让沙漠石、低屋面和遮阳直接回应气候；罗森鲍姆住宅则让平面随家庭生活继续生长。对设计师而言，最值得带走的不是赖特式线条，而是工作顺序：先确认场地关系，再建立可贯穿结构、家具和动线的秩序，最后让材料保留真实的重量与尺度。本文为基于书籍与案例资料的编辑性阅读，不是原书引语。",
        "tags": "#弗兰克劳埃德赖特 #TheNaturalHouse #有机建筑 #住宅设计 #建筑理论 #建筑书单 #空间设计 #建筑学生",
    },
    "alvar-aalto-in-his-own-words": {
        "designer": "阿尔瓦·阿尔托",
        "designer_en": "ALVAR AALTO",
        "book": "Alvar Aalto in His Own Words",
        "book_cn": "《阿尔瓦·阿尔托自述》",
        "edition": "Göran Schildt 编｜Rizzoli, 1998｜ISBN 9780847820801",
        "question": "现代主义怎样重新照顾人的感受？",
        "thesis": "阿尔托没有拒绝标准化，而是让标准在身体、光线、声学与自然面前发生柔性偏转。",
        "system": "human-wave",
        "palette": {"paper": "#F2EEE3", "ink": "#182C35", "accent": "#1D6B82", "second": "#9D3D32", "warm": "#D3B56D"},
        "cards": [
            ("帕伊米奥疗养院", "功能从人的身体尺度开始", "色彩、家具、采光与安静的环境被当作治疗经验的一部分，而不只是技术指标。", "02-paimio.jpg"),
            ("维堡图书馆", "曲线让标准空间回应声与光", "波浪形天花处理声学，圆形天窗分散自然光，理性系统因此获得感知层次。", "03-vyborg-library.jpg"),
            ("玛利亚别墅", "现代结构可以容纳自然的复杂性", "柱列、木材、石材与自由边界叠合，空间像穿过森林，而不是观看一套纯形式。", "04-villa-mairea.jpg"),
            ("塞于奈察洛市政厅", "公共建筑也需要亲密的尺度", "砖、庭院、草坡台阶与曲折入口，把行政建筑转化为可停留的日常场所。", "05-saynatsalo.jpg"),
        ],
        "summary": "人性化不是给理性系统加装饰，而是让规则主动回应身体、感官与具体环境。",
        "chain": ["标准", "身体", "感知", "自然", "公共生活"],
        "methods": ["把声、光、触感列入最初的功能表", "允许标准构件在关键处发生偏转", "用入口、庭院和家具校准人的尺度"],
        "endcards": {
            "01": {"layout_rationale": "以连续波形贯穿封面，书封像一个停顿点，表达阿尔托用柔性变化修正现代主义。", "changed_variables": ["纵向曲线路径", "左上书封", "中段标题", "暖白开放背景"]},
            "06": {"layout_rationale": "把结论组织成从标准到公共生活的弯曲感知路径，三条方法挂接在不同转折点。", "changed_variables": ["S形概念链", "分散方法标注", "大面积浅底", "非对称终点"]},
        },
        "publish_title": "阿尔托如何让现代主义重新照顾人？",
        "publish_body": "《Alvar Aalto in His Own Words》把阿尔托的文章、演讲与访谈放到一起，能看到他如何从现代主义内部修正规则。帕伊米奥疗养院把色彩、家具、光线和安静纳入治疗经验；维堡图书馆用波浪形天花与圆形天窗处理声音和漫射光；玛利亚别墅让柱列与多种材料形成近似森林的感知；塞于奈察洛市政厅则用砖、庭院和草坡台阶，把公共权力拉回人的尺度。他没有放弃标准化，而是不断追问：当规则碰到身体、感官和自然时，应该怎样弯曲？对设计师最实用的提醒是，把声、光、触感提前写进功能表；允许标准构件在关键位置发生变化；用入口、家具和可停留空间校准尺度。本文为编辑性概括，不是原书逐字引语。",
        "tags": "#阿尔瓦阿尔托 #AlvarAalto #现代主义 #人性化设计 #建筑理论 #建筑书单 #空间体验 #建筑学生",
    },
    "lina-bo-bardi-stones-against-diamonds": {
        "designer": "莉娜·博·巴尔迪",
        "designer_en": "LINA BO BARDI",
        "book": "Stones Against Diamonds",
        "book_cn": "《石头对抗钻石》",
        "edition": "Architectural Association Publications, 2012｜ISBN 9781907896200",
        "question": "建筑为什么要选择石头，而不是钻石？",
        "thesis": "建筑的价值不来自稀有与精致，而来自普通材料、旧结构和集体使用被重新组织。",
        "system": "rough-bridge",
        "palette": {"paper": "#E9E3D5", "ink": "#161716", "accent": "#D23A2E", "second": "#315A6A", "warm": "#A68C63"},
        "cards": [
            ("玻璃之家", "现代透明必须与真实地形相遇", "纤细结构面对茂密坡地，理性框架没有抹平热带环境，而是让两者保持张力。", "02-casa-de-vidro.jpg"),
            ("乌尼昂庄园", "改造先保留时间，再加入新动作", "旧建筑被继续使用，标志性的木楼梯把历史构造与当代公共文化连接起来。", "03-solar-do-unhao.jpg"),
            ("圣保罗艺术博物馆", "真正的纪念性来自让出地面", "巨大的悬空体量保留城市视线，也把建筑下方交给集会、市场与日常经过。", "04-masp.jpg"),
            ("庞培亚中心", "粗粝材料可以容纳丰富生活", "旧工厂、新混凝土塔、空中连桥与开放活动共同构成不被过度规定的公共场所。", "05-sesc-pompeia.jpg"),
        ],
        "summary": "“石头”不是反对美，而是拒绝把建筑价值压缩成稀有物；公共使用才是材料与结构被检验的现场。",
        "chain": ["已有之物", "最少干预", "让出空间", "集体占用", "持续变化"],
        "methods": ["先盘点可保留的结构与使用痕迹", "把首层和通道优先还给公共活动", "用粗粝材料承受变化，而非制造距离"],
        "endcards": {
            "01": {"layout_rationale": "用一块粗粝石形与锐利钻石网格正面对撞，窄书封嵌入裂缝，直接建立价值冲突。", "changed_variables": ["对角冲突", "左侧竖书封", "超大问题标题", "粗糙深底"]},
            "06": {"layout_rationale": "用一条跨越旧结构的公共桥串联五个概念，方法作为被使用的节点而非结论卡片。", "changed_variables": ["桥式概念链", "底部节点", "横跨式总结", "红蓝双重结构"]},
        },
        "publish_title": "建筑为什么要选择石头，而不是钻石？",
        "publish_body": "莉娜·博·巴尔迪在《Stones Against Diamonds》中讨论的并不是材料贵贱，而是建筑价值站在哪一边。“钻石”指向稀有、精致和与日常隔离的对象；“石头”则来自普通劳动、现成结构和真实使用。玻璃之家让现代框架与热带坡地保持张力；乌尼昂庄园在保留历史构造的同时加入新的公共文化；MASP 用巨大的悬空体量把地面让给城市；SESC 庞培亚则把旧工厂、粗混凝土塔、连桥和群众活动组织成持续变化的公共场所。对设计师而言，这不是一套粗野风格，而是一种价值判断：先盘点可保留的结构与痕迹，把首层和通道优先交给公共活动，再选择能承受使用与变化的材料。本文为编辑性阅读，不是原书直接引语。",
        "tags": "#莉娜博巴尔迪 #StonesAgainstDiamonds #建筑改造 #公共空间 #建筑理论 #建筑书单 #设计方法 #建筑学生",
    },
}


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def get_font(size: int, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if serif:
        candidates += [Path("C:/Windows/Fonts/simfang.ttf"), Path("C:/Windows/Fonts/simsun.ttc")]
    elif bold:
        candidates += [Path("C:/Windows/Fonts/msyhbd.ttc"), Path("C:/Windows/Fonts/simhei.ttf")]
    else:
        candidates += [Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/simhei.ttf")]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


def crop(image: Image.Image, box: tuple[int, int], centering=(0.5, 0.5)) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), box, method=Image.Resampling.LANCZOS, centering=centering)


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines():
        current = ""
        for char in paragraph:
            trial = current + char
            if current and draw.textbbox((0, 0), trial, font=font)[2] > width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
    return lines


def text_block(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.FreeTypeFont, fill, width: int, spacing=12) -> int:
    x, y = xy
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


def open_image(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return ImageEnhance.Contrast(image).enhance(1.03)


def paste_cover(canvas: Image.Image, cover: Image.Image, box: tuple[int, int, int, int], shadow=True) -> None:
    x0, y0, x1, y1 = box
    fitted = ImageOps.contain(cover.convert("RGB"), (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    x = x0 + (x1 - x0 - fitted.width) // 2
    y = y0 + (y1 - y0 - fitted.height) // 2
    if shadow:
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).rounded_rectangle((x + 14, y + 18, x + fitted.width + 14, y + fitted.height + 18), radius=4, fill=(0, 0, 0, 90))
        layer = layer.filter(ImageFilter.GaussianBlur(14))
        canvas.paste(layer, (0, 0), layer)
    canvas.paste(fitted, (x, y))


def draw_page_mark(draw: ImageDraw.ImageDraw, number: int, color, light=False) -> None:
    fill = (245, 243, 236) if light else color
    back = color if light else (245, 243, 236)
    draw.ellipse((1112, 52, 1192, 132), fill=back)
    draw.text((1127, 68), f"{number:02d}", font=get_font(28, bold=True), fill=fill)


def cover_wright(book, assets: Path) -> Image.Image:
    p = {k: hex_rgb(v) for k, v in book["palette"].items()}
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    photo = crop(open_image(assets / "02-fallingwater.jpg"), (W, 760), (0.48, 0.42))
    image.paste(photo, (0, 900))
    draw.rectangle((0, 900, W, 940), fill=p["accent"])
    for i, (y, h, color) in enumerate([(760, 170, p["warm"]), (835, 130, p["second"]), (905, 85, p["ink"])]):
        points = [(0, y + 45 * math.sin(i + 0.2)), (410, y - 25), (790, y + 20), (W, y - 42), (W, y + h), (0, y + h + 30)]
        draw.polygon(points, fill=color)
    draw.text((80, 82), book["designer_en"], font=get_font(28, bold=True), fill=p["second"])
    y = text_block(draw, (80, 170), book["question"], get_font(86, bold=True), p["ink"], 850, 6)
    text_block(draw, (84, y + 32), book["thesis"], get_font(34), p["ink"], 650, 14)
    paste_cover(image, open_image(assets / "cover.jpg"), (815, 320, 1150, 850))
    draw.text((82, 705), book["book_cn"], font=get_font(32, bold=True), fill=p["accent"])
    draw_page_mark(draw, 1, p["ink"])
    return image


def cover_aalto(book, assets: Path) -> Image.Image:
    p = {k: hex_rgb(v) for k, v in book["palette"].items()}
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    photo = crop(open_image(assets / "04-villa-mairea.jpg"), (520, H), (0.45, 0.5))
    photo = ImageEnhance.Color(photo).enhance(0.62)
    image.paste(photo, (722, 0))
    points = []
    for i in range(65):
        y = 40 + i * 25
        x = 650 + int(115 * math.sin(i / 5.3))
        points.append((x, y))
    draw.line(points, fill=p["accent"], width=22)
    draw.line([(x - 34, y) for x, y in points], fill=p["warm"], width=4)
    paste_cover(image, open_image(assets / "cover.jpg"), (72, 110, 430, 630))
    draw.text((76, 690), book["designer_en"], font=get_font(28, bold=True), fill=p["accent"])
    text_block(draw, (76, 770), "现代主义怎样\n重新照顾人的感受？", get_font(58, bold=True), p["ink"], 590, 10)
    text_block(draw, (76, 1100), book["thesis"], get_font(34), p["ink"], 560, 14)
    draw.text((76, 1510), book["book_cn"], font=get_font(30, bold=True), fill=p["second"])
    draw_page_mark(draw, 1, p["ink"])
    return image


def cover_lina(book, assets: Path) -> Image.Image:
    p = {k: hex_rgb(v) for k, v in book["palette"].items()}
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    photo = crop(open_image(assets / "05-sesc-pompeia.jpg"), (W, 610), (0.5, 0.45))
    photo = ImageEnhance.Color(photo).enhance(0.48)
    image.paste(photo, (0, 1050))
    draw.polygon([(0, 0), (825, 0), (620, 1020), (0, 1190)], fill=p["paper"])
    for offset in range(-160, 500, 95):
        draw.line((720 + offset, 0, 1030 + offset, 1060), fill=p["second"], width=3)
    stone = [(635, 360), (995, 250), (1155, 570), (1000, 930), (690, 870), (570, 610)]
    draw.polygon(stone, fill=p["warm"])
    draw.line(stone + [stone[0]], fill=p["accent"], width=14, joint="curve")
    paste_cover(image, open_image(assets / "cover.jpg"), (70, 135, 330, 660), shadow=False)
    draw.text((80, 700), book["designer_en"], font=get_font(26, bold=True), fill=p["accent"])
    y = text_block(draw, (80, 720), "建筑为什么\n要选择石头，\n而不是钻石？", get_font(62, bold=True), p["ink"], 520, 8)
    text_block(draw, (80, y + 18), book["thesis"], get_font(27), p["ink"], 500, 10)
    draw.text((78, 1520), book["book_cn"], font=get_font(30, bold=True), fill=p["paper"])
    draw_page_mark(draw, 1, p["ink"])
    return image


def interior(book, assets: Path, index: int) -> Image.Image:
    p = {k: hex_rgb(v) for k, v in book["palette"].items()}
    title, headline, body, asset_name = book["cards"][index - 2]
    system = book["system"]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    source = open_image(assets / asset_name)

    if system == "organic-grid":
        photo_h = 930 if index % 2 == 0 else 860
        photo = crop(source, (W, photo_h), (0.5, 0.48))
        image.paste(photo, (0, 0))
        draw.rectangle((0, photo_h - 22, W, photo_h + 18), fill=p["accent"])
        draw.rectangle((72, photo_h - 118, 520, photo_h - 42), fill=p["ink"])
        draw.text((95, photo_h - 102), title, font=get_font(34, bold=True), fill=p["paper"])
        y = text_block(draw, (78, photo_h + 92), headline, get_font(60, bold=True), p["ink"], 1060, 8)
        text_block(draw, (82, y + 32), body, get_font(34), p["ink"], 930, 14)
        for x in range(80, 1160, 108):
            draw.line((x, H - 90, x + 58, H - 90), fill=p["second"], width=5)
    elif system == "human-wave":
        photo = crop(source, (930, 940), (0.5, 0.48))
        image.paste(photo, (230, 100))
        draw.rectangle((0, 0, 160, H), fill=p["accent"] if index % 2 == 0 else p["second"])
        wave = [(160 + int(55 * math.sin(y / 95)), y) for y in range(0, H + 1, 14)]
        draw.line(wave, fill=p["warm"], width=18)
        draw.text((220, 54), title, font=get_font(32, bold=True), fill=p["ink"])
        y = text_block(draw, (220, 1115), headline, get_font(56, bold=True), p["ink"], 930, 8)
        text_block(draw, (224, y + 28), body, get_font(33), p["ink"], 880, 13)
    else:
        photo = crop(source, (870, 1000), (0.5, 0.48))
        x_photo = 0 if index % 2 == 0 else 372
        image.paste(photo, (x_photo, 0))
        panel_x = 820 if index % 2 == 0 else 0
        draw.rectangle((panel_x, 0, panel_x + 422, 1060), fill=p["ink"])
        for yline in range(90, 1000, 120):
            draw.line((panel_x + 55, yline, panel_x + 360, yline - 45), fill=p["accent"], width=5)
        draw.rectangle((70, 930, 1170, 1020), fill=p["accent"])
        draw.text((96, 948), title, font=get_font(35, bold=True), fill=p["paper"])
        y = text_block(draw, (74, 1110), headline, get_font(58, bold=True), p["ink"], 1050, 8)
        text_block(draw, (78, y + 30), body, get_font(33), p["ink"], 980, 13)

    draw_page_mark(draw, index, p["ink"], light=(system == "rough-bridge" and index % 2 == 0))
    draw.text((1040, 1570), book["designer_en"], font=get_font(19, bold=True), fill=p["accent"])
    return image


def summary_wright(book) -> Image.Image:
    p = {k: hex_rgb(v) for k, v in book["palette"].items()}
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    center = (620, 800)
    for radius, color, width in [(520, p["second"], 3), (390, p["warm"], 5), (250, p["accent"], 9)]:
        draw.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), outline=color, width=width)
    draw.ellipse((430, 610, 810, 990), fill=p["accent"])
    draw.multiline_text(center, "有机建筑\n是一条连续推理", font=get_font(42, bold=True), fill=p["paper"], anchor="mm", align="center", spacing=10)
    positions = [(160, 340), (500, 200), (875, 390), (900, 1040), (260, 1160)]
    for label, pos in zip(book["chain"], positions):
        draw.ellipse((pos[0]-16, pos[1]-16, pos[0]+16, pos[1]+16), fill=p["warm"])
        draw.text((pos[0]+28, pos[1]-24), label, font=get_font(34, bold=True), fill=p["paper"])
        draw.line((center[0], center[1], pos[0], pos[1]), fill=p["second"], width=3)
    draw.ellipse((430, 610, 810, 990), fill=p["accent"])
    draw.multiline_text(center, "有机建筑\n是一条连续推理", font=get_font(42, bold=True), fill=p["paper"], anchor="mm", align="center", spacing=10)
    for i, method in enumerate(book["methods"]):
        x = 80 + i * 390
        draw.text((x, 1450), f"0{i+1}", font=get_font(28, bold=True), fill=p["accent"])
        text_block(draw, (x, 1492), method, get_font(24), p["paper"], 320, 8)
    draw.text((80, 90), "从土地到生活", font=get_font(72, bold=True), fill=p["paper"])
    draw_page_mark(draw, 6, p["ink"], light=True)
    return image


def summary_aalto(book) -> Image.Image:
    p = {k: hex_rgb(v) for k, v in book["palette"].items()}
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((80, 100), "规则，要在人的感受前弯曲", font=get_font(64, bold=True), fill=p["ink"])
    points = []
    for i in range(101):
        x = 100 + i * 10.2
        y = 720 + 180 * math.sin(i / 16)
        points.append((int(x), int(y)))
    draw.line(points, fill=p["accent"], width=24)
    chain_positions = [points[i] for i in (3, 25, 50, 74, 97)]
    for index, (label, pos) in enumerate(zip(book["chain"], chain_positions)):
        draw.ellipse((pos[0]-28, pos[1]-28, pos[0]+28, pos[1]+28), fill=p["second"] if index % 2 else p["warm"])
        draw.text((pos[0]-35, pos[1]-88 if index % 2 == 0 else pos[1]+42), label, font=get_font(30, bold=True), fill=p["ink"])
    method_positions = [(95, 1080), (470, 1210), (810, 1010)]
    for i, (method, pos) in enumerate(zip(book["methods"], method_positions)):
        draw.line((pos[0], pos[1]-40, pos[0]+100, pos[1]-40), fill=p["accent"], width=8)
        draw.text(pos, f"0{i+1}", font=get_font(27, bold=True), fill=p["second"])
        text_block(draw, (pos[0]+58, pos[1]), method, get_font(27), p["ink"], 300, 10)
    text_block(draw, (80, 330), book["summary"], get_font(34), p["ink"], 880, 14)
    draw_page_mark(draw, 6, p["ink"])
    return image


def summary_lina(book) -> Image.Image:
    p = {k: hex_rgb(v) for k, v in book["palette"].items()}
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 470), fill=p["ink"])
    draw.text((82, 105), "建筑的价值，\n在被共同使用时成立", font=get_font(66, bold=True), fill=p["paper"], spacing=18)
    text_block(draw, (82, 520), book["summary"], get_font(34), p["ink"], 980, 14)
    bridge_y = 930
    draw.rectangle((80, bridge_y, 1160, bridge_y + 92), fill=p["second"])
    draw.line((80, bridge_y, 1160, bridge_y), fill=p["accent"], width=18)
    xs = [105, 345, 585, 825, 1065]
    for x, label in zip(xs, book["chain"]):
        draw.ellipse((x-21, bridge_y-21, x+21, bridge_y+21), fill=p["accent"])
        text_block(draw, (x-55, bridge_y+125), label, get_font(26, bold=True), p["ink"], 130, 5)
    for i, method in enumerate(book["methods"]):
        x = 75 + i * 390
        draw.polygon([(x, 1320), (x+350, 1280), (x+330, 1550), (x+15, 1580)], fill=p["ink"] if i != 1 else p["accent"])
        draw.text((x+22, 1342), f"0{i+1}", font=get_font(27, bold=True), fill=p["warm"])
        text_block(draw, (x+64, 1342), method, get_font(25), p["paper"], 250, 8)
    draw_page_mark(draw, 6, p["ink"], light=True)
    return image


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0)


def preview(paths: list[Path], output: Path) -> None:
    tw, th, gap = 360, 481, 24
    sheet = Image.new("RGB", (tw * 3 + gap * 4, th * 2 + gap * 3), (220, 218, 212))
    for i, path in enumerate(paths):
        with Image.open(path) as image:
            thumb = image.convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (gap + (i % 3) * (tw + gap), gap + (i // 3) * (th + gap)))
    save(sheet.resize((1242, 1108), Image.Resampling.LANCZOS), output)


def write_docs(book, assets: Path, output: Path) -> None:
    manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    source_lines = [
        "# 图片来源",
        "",
        "| 文件名 | 内容 | 作者/机构 | 来源 URL | 许可/版权 | 修改 |",
        "|---|---|---|---|---|---|",
    ]
    for item in manifest:
        source_lines.append(
            f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item['modifications']} |"
        )
    source_lines += [
        "",
        "书封仅用于书籍识别、介绍与评论；商业投放前请再次核验所在地与平台规则。",
        "卡片文字为基于书籍与案例资料的编辑性概括，未作为原书直接引语。",
    ]
    (output / "图片来源.md").write_text("\n".join(source_lines) + "\n", encoding="utf-8")

    publish = f"""# 标题

{book['publish_title']}

# 正文

{book['publish_body']}

# 标签

{book['tags']}

# 版本

{book['book']}｜{book['edition']}
"""
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
                {"number": f"{i:02d}", "role": "mechanism" if i == 2 else "evidence", "headline": card[1], "evidence": card[0], "asset": card[3]}
                for i, card in enumerate(book["cards"], start=2)
            ],
            {"number": "06", "role": "synthesis", "headline": book["summary"], "asset": ""},
        ],
        "endcards": book["endcards"],
        "transferable_methods": book["methods"],
        "sources": manifest,
    }
    (output / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    all_previews: list[Path] = []
    for slug, book in BOOKS.items():
        assets = ASSET_ROOT / slug
        output = OUTPUT_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        if not (assets / "manifest.json").exists():
            raise FileNotFoundError(f"Run fetch_three_unmentioned_masters.py first: {assets}")

        if book["system"] == "organic-grid":
            first = cover_wright(book, assets)
            last = summary_wright(book)
        elif book["system"] == "human-wave":
            first = cover_aalto(book, assets)
            last = summary_aalto(book)
        else:
            first = cover_lina(book, assets)
            last = summary_lina(book)

        paths: list[Path] = []
        for number, card in [(1, first), *[(i, interior(book, assets, i)) for i in range(2, 6)], (6, last)]:
            path = output / f"{number:02d}.jpg"
            save(card, path)
            paths.append(path)
        preview(paths, output / "preview.jpg")
        write_docs(book, assets, output)
        all_previews.append(output / "preview.jpg")
        print(f"Rendered {slug}")

    contact = Image.new("RGB", (1242, 3500), (232, 230, 224))
    y = 36
    for path in all_previews:
        with Image.open(path) as image:
            strip = image.convert("RGB").resize((1160, 1035), Image.Resampling.LANCZOS)
        contact.paste(strip, (41, y))
        y += 1140
    save(contact, OUTPUT_ROOT / "总预览.jpg")


if __name__ == "__main__":
    main()
