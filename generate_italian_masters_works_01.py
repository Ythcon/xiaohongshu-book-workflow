#!/usr/bin/env python3
"""Render three six-card Xiaohongshu posts on Italian architecture masters."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

import generate_three_unmentioned_masters as base

ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "italian-masters-works-01"
OUTPUT_ROOT = ROOT / "output" / "italian-masters-works-01"
W, H = 1242, 1660

BOOKS = {
    "giuseppe-terragni-transformations": {
        "designer": "朱塞佩·特拉尼", "designer_en": "GIUSEPPE TERRAGNI",
        "book": "Giuseppe Terragni: Transformations, Decompositions, Critiques",
        "book_cn": "《特拉尼：变形、分解与批评》",
        "edition": "The Monacelli Press, 2003｜ISBN 9781885254962",
        "question": "立面，怎样成为空间的推理？",
        "thesis": "特拉尼把网格、开口、楼板与路径当作同一套推理：理性不是把建筑压平，而是让复杂关系保持可读。",
        "system": "rational-frame",
        "palette": {"paper": "#F0EEE5", "ink": "#122433", "red": "#D54135", "gray": "#85939A", "blue": "#276273", "warm": "#DAB35D"},
        "cards": [
            ("科莫法西斯之家", "网格不是立面图案，而是空间秩序", "正方形体量被柱网、楼板和不同深度的开口切开；立面让内部的集会、楼梯与平台关系保持可读。", "02-casa-del-fascio.jpg", "网格 / 楼板 / 透明度"),
            ("诺沃科穆姆公寓", "新住宅，先把体量拆成不同的观看距离", "转角阳台、水平窗带与后退体量让公寓不再是一堵完整外墙；街道、居住与光线由不同层次同时组织。", "03-novocomum.jpg", "转角 / 水平线 / 层次"),
            ("圣埃利亚幼儿园", "儿童空间，也能用结构给出自由", "屋顶、采光和活动空间不靠装饰区分，而由连续构件和尺度变化建立；规则成为活动可以占用的框架。", "04-sant-elia.jpg", "尺度 / 采光 / 活动"),
            ("科莫阵亡将士纪念碑", "纪念性，来自比例与城市轴线", "垂直塔体与湖岸、城市视线形成明确的公共坐标；几何的克制让纪念碑从对象转为城市中的方向装置。", "05-monumento-ai-caduti.jpg", "比例 / 轴线 / 城市"),
        ],
        "summary": "理性主义不是简化关系，而是把每一层关系都放进能被阅读、检验与修改的结构里。",
        "chain": ["网格", "楼板", "开口", "路径", "城市"],
        "methods": ["先用结构网格确定可变与不可变", "让开口对应内部真实的层高与移动", "从城市远景和近景各检查一次比例"],
        "endcards": {"01": {"layout_rationale": "以法西斯之家立面作为整页结构框架，真实书封被置于网格内的偏下单元，标题沿网格的空格展开。", "changed_variables": ["整页立面", "中下书封", "网格式标题", "白底红线"]}, "06": {"layout_rationale": "把五个判断做成可推演的正方形矩阵，从网格到城市逐层外扩，三条方法贴在不同边界上。", "changed_variables": ["正方形矩阵", "由内向外概念链", "边界式方法", "深色结尾"]}},
        "publish_title": "特拉尼：立面怎样推理空间？",
        "publish_paragraphs": [
            "《Giuseppe Terragni》把特拉尼的建筑放进一套变形与分解的阅读里：建筑不靠造型先成立，而是让网格、开口、楼板和路径互相说明。",
            "理性主义不等于把建筑做成冷静方盒子，立面也不是完成平面后的表皮；它们都可以把内部关系推到城市尺度上被看见。",
            "科莫法西斯之家用正方形柱网和不同深度的开口暴露内部层次；诺沃科穆姆公寓靠转角、窗带和后退体量拆开街道尺度；圣埃利亚幼儿园把采光、活动和儿童尺度放进连续构件；科莫阵亡将士纪念碑则用塔体比例与湖岸轴线建立公共方向。",
            "对设计师更实用的工作法是：先用结构网格区分可变与不可变，再让开口对应真实层高和移动，最后从街道远景与近景各检查一次比例。",
            "规则不是限制复杂性的笼子，而是让复杂性能够被推理和校正的坐标；当立面说得清内部，建筑才不必依赖额外的形式姿态。",
        ],
        "tags": "#朱塞佩特拉尼  #GiuseppeTerragni  #意大利理性主义  #建筑立面  #建筑理论  #设计方法  #建筑书单  #建筑案例",
    },
    "aldo-rossi-architecture-of-the-city": {
        "designer": "阿尔多·罗西", "designer_en": "ALDO ROSSI",
        "book": "The Architecture of the City", "book_cn": "《城市建筑学》",
        "edition": "The MIT Press, 1984｜ISBN 9780262680431",
        "question": "城市，为什么会记住建筑？",
        "thesis": "罗西把城市看作集体记忆的容器：类型、纪念物与日常生活不断重叠，才让一个地点在时间中保持可辨认。",
        "system": "memory-artefacts",
        "palette": {"paper": "#F3EEE2", "ink": "#27313A", "red": "#CB4936", "blue": "#57768B", "yellow": "#D7B766", "gray": "#B7AEA2"},
        "cards": [
            ("加拉拉特斯住宅区", "住宅的重复，也能成为城市记忆", "长廊、重复墙片和楼梯把普通住区变成可辨认的公共序列；类型不靠新奇，而靠持续出现的尺度与路径。", "02-gallaratese.jpg", "重复 / 长廊 / 共同生活"),
            ("圣卡塔尔多公墓", "纪念物让城市记住时间", "红色空心立方体、锥体和骨灰廊被组织成一座死者之城；抽象几何不是装饰，而是让哀悼获得稳定的城市尺度。", "03-san-cataldo.jpg", "纪念物 / 时间 / 城市"),
            ("世界剧场", "短暂建筑，也能进入集体记忆", "漂浮在威尼斯水面上的木制剧场借用塔、剧院和驳船的熟悉类型；它存在时间很短，却让城市旧有的水上记忆重新显形。", "04-teatro-del-mondo.jpg", "类型 / 水面 / 暂时性"),
            ("博纳方腾博物馆", "新地标，不必伪装成旧城", "塔、圆顶和长体量让博物馆在马斯特里赫特河岸建立新的辨认点；新建筑通过清晰类型参与城市，而非复制历史细节。", "05-bonnefanten.jpg", "地标 / 河岸 / 新旧"),
        ],
        "summary": "城市不是建筑物的总和，而是一些能抵抗时间的类型、路径与纪念物持续被生活重新使用。",
        "chain": ["类型", "地点", "纪念物", "时间", "集体生活"],
        "methods": ["找出场地中反复出现的一种空间类型", "把纪念性放到路径与尺度，不放到符号堆砌", "为新建筑预留一个可被日常反复经过的地点"],
        "endcards": {"01": {"layout_rationale": "红色公墓立方体压在下方，MIT 书封像城市档案卡插入上方留白，标题沿一条城市记忆时间线排开。", "changed_variables": ["下部纪念物", "上部书封", "时间线标题", "暖纸色"]}, "06": {"layout_rationale": "用城市地图式的时间环把类型、地点、纪念物和生活串起，结论在中心，方法沿四个街区分布。", "changed_variables": ["时间环", "中心结论", "街区式方法", "浅色结尾"]}},
        "publish_title": "罗西：城市为何会记住建筑？",
        "publish_paragraphs": [
            "《The Architecture of the City》把城市理解为集体记忆的容器：真正留下来的，不只是功能，而是能够被不断使用、辨认和重写的类型。",
            "城市不是建筑物的清单，纪念性也不是加一座显眼雕塑；它们都来自地点、路径与时间被反复叠加后的稳定关系。",
            "加拉拉特斯住宅区用长廊、墙片和楼梯把重复住宅组织成公共序列；圣卡塔尔多公墓把红色空心立方体和骨灰廊变成死者之城；世界剧场借塔、剧院和驳船的类型让威尼斯水上记忆再次显形；博纳方腾博物馆则以塔与圆顶在河岸建立新的辨认点。",
            "对设计师更实用的工作法是：先找出场地中反复出现的一种空间类型，再把纪念性放进路径和尺度，并为新建筑预留一个能够被日常反复经过的地点。",
            "类型不是复古的形式库，而是城市用来保存经验的结构；当建筑愿意承接这种结构，它才可能在时间里比流行更久。",
        ],
        "tags": "#阿尔多罗西  #TheArchitectureOfTheCity  #城市建筑学  #建筑类型  #城市记忆  #建筑理论  #建筑书单  #建筑案例",
    },
    "superstudio-life-without-objects": {
        "designer": "超级工作室", "designer_en": "SUPERSTUDIO",
        "book": "Superstudio: Life Without Objects", "book_cn": "《没有物的生活》",
        "edition": "Skira, 2003｜ISBN 9788884915696",
        "question": "不再造物，建筑还能做什么？",
        "thesis": "超级工作室把建筑从建造对象转成批判工具：用网格、拼贴、家具和仪式，追问消费如何塑造空间与生活。",
        "system": "critical-grid",
        "palette": {"paper": "#F5F1E8", "ink": "#101417", "red": "#E34A38", "yellow": "#F4CF4C", "blue": "#2D6D82", "gray": "#969B98"},
        "cards": [
            ("Superarchitettura", "先把设计变成一场过量的提问", "1966 年的展览以夸张色彩、家具与环境挑战好品味和功能主义。它不是提供新风格，而是让设计的消费逻辑无处躲藏。", "02-superarchitettura.jpg", "展览复原 / 1966"),
            ("Giovannetti 工厂", "真正建成，也可以拒绝中性", "这座 1969 年工厂把强烈图案、外壳与日常生产放在同一个视野里。即使面对普通委托，建筑仍能把物的文化变成问题。", "03-giovannetti.jpg", "建成项目 / 1969"),
            ("连续纪念碑", "一张无限网格，暴露全球化想象", "《连续纪念碑》是未建的拼贴方案：同一张网格跨越城市、山脉与海岸。它把‘统一世界’的欲望推到极端，反而显出其暴力。", "04-continuous-monument.jpg", "原作展陈实拍 / 1969"),
            ("Superonda", "一件沙发，也能拒绝固定姿态", "Superonda 用两块可自由组合的波浪形泡沫取代固定骨架，让坐、躺、聚集不断变化。家具不再规定唯一动作，而成为身体试验生活方式的接口。", "05-superronda.jpg", "家具实物 / 1966"),
        ],
        "summary": "当建筑不急着生产对象，它可以先暴露：谁在规定需求、尺度、图像与生活方式。",
        "chain": ["对象", "图像", "网格", "身体", "生活方式"],
        "methods": ["把项目里默认的需求写成可以质疑的问题", "用一个极端图像测试规则会把生活推向哪里", "让材料和对象承担观点，而不只承担风格"],
        "endcards": {"01": {"layout_rationale": "用一张黑色无限网格占满下半页，真实书封像被网格吸附的档案物，标题留在纯白区域形成强烈断裂。", "changed_variables": ["下半无限网格", "上部留白标题", "居中书封", "黑白红黄对比"]}, "06": {"layout_rationale": "以一条不断扩张的网格带穿过五个批判节点，三条方法像脚注散落在带外，避免做成建筑案例总结板。", "changed_variables": ["扩张网格带", "非线性节点", "脚注式方法", "明亮结尾"]}},
        "publish_title": "超级工作室：不造物还能做什么？",
        "publish_paragraphs": [
            "《Superstudio: Life Without Objects》把超级工作室的拼贴、展览、家具、脚本和批评文字放在一起，提醒设计师：建筑不只是在生产更多对象。",
            "激进设计不是做一张更酷的未来图，网格也不是视觉装饰；它们可以把消费、标准化和生活方式中默认的规则推到无法回避的位置。",
            "Superarchitettura 用过量色彩和环境挑衅好品味；Giovannetti 工厂把普通生产建筑变成物的文化现场；未建的《连续纪念碑》让一张网格跨过山海，暴露统一世界的暴力；Superonda 则用可重组的波浪形泡沫，拒绝家具对身体姿态的固定。",
            "对设计师更实用的工作法是：先把项目里默认的需求写成可以质疑的问题，再用一个极端图像测试规则会把生活推向哪里，并让材料或对象承担明确的观点。",
            "不急着提出新形式，并不等于停止设计；有时先让既有形式的代价被看见，才是重新发明空间的开始。",
        ],
        "tags": "#超级工作室  #Superstudio  #LifeWithoutObjects  #激进设计  #意大利建筑  #设计批评  #建筑书单  #建筑理论",
    },
}


def rgb(book: dict) -> dict[str, tuple[int, int, int]]:
    return {k: tuple(int(v[i:i+2], 16) for i in (1, 3, 5)) for k, v in book["palette"].items()}


def toned(image: Image.Image, sat: float = .72, contrast: float = 1.05) -> Image.Image:
    return ImageEnhance.Contrast(ImageEnhance.Color(image.convert("RGB")).enhance(sat)).enhance(contrast)


def fit_title(draw, xy, text, width, size, fill, spacing=8):
    font = base.get_font(size, bold=True, serif=True)
    lines = base.wrap(draw, text, font, width)
    while len(lines) > 4 and size > 34:
        size -= 2; font = base.get_font(size, bold=True, serif=True); lines = base.wrap(draw, text, font, width)
    draw.multiline_text(xy, "\n".join(lines), font=font, fill=fill, spacing=spacing)
    return draw.multiline_textbbox(xy, "\n".join(lines), font=font, spacing=spacing)[3]


def label(draw, x, y, text, bg, fg, width):
    draw.rectangle((x, y, x + width, y + 46), fill=bg)
    draw.text((x + 14, y + 10), text, font=base.get_font(18, bold=True), fill=fg)


def cover_terragni(book, assets):
    p = rgb(book); img = Image.new("RGB", (W,H), p["paper"])
    photo = toned(base.crop(base.open_image(assets / "02-casa-del-fascio.jpg"),(W,960),(.5,.45)), .38, 1.10); img.paste(photo,(0,0))
    d=ImageDraw.Draw(img); d.rectangle((0,0,W,960), outline=p["paper"], width=14)
    for x in range(60,W,190): d.line((x,0,x,960), fill=(*p["paper"],), width=3)
    for y in range(120,960,170): d.line((0,y,W,y), fill=p["paper"], width=3)
    d.rectangle((0,0,W,960), fill=(*p["ink"],))
    # Re-paste photo softly through selected grid cells.
    img.paste(photo, (0,0)); d=ImageDraw.Draw(img)
    overlay=Image.new("RGBA",(W,960),(18,36,51,88)); img.paste(Image.alpha_composite(img.crop((0,0,W,960)).convert("RGBA"),overlay).convert("RGB"),(0,0)); d=ImageDraw.Draw(img)
    for x in range(60,W,190): d.line((x,0,x,960), fill=p["paper"], width=3)
    for y in range(120,960,170): d.line((0,y,W,y), fill=p["paper"], width=3)
    d.text((60,44),"GIUSEPPE TERRAGNI / 01",font=base.get_font(21,bold=True),fill=p["paper"]); d.line((60,94,1180,94),fill=p["red"],width=7)
    d.text((60,160),"立面怎样",font=base.get_font(72,bold=True,serif=True),fill=p["paper"]); d.text((60,250),"推理空间？",font=base.get_font(72,bold=True,serif=True),fill=p["paper"])
    base.paste_cover(img,base.open_image(assets/"cover.jpg"),(712,670,1168,1320),shadow=True); d=ImageDraw.Draw(img); label(d,748,1332,"VERIFIED BOOK COVER",p["red"],p["paper"],330)
    d.text((62,1025),book["book_cn"],font=base.get_font(36,bold=True),fill=p["red"]); d.text((62,1080),book["designer"],font=base.get_font(25,bold=True),fill=p["blue"])
    base.text_block(d,(62,1150),book["thesis"],base.get_font(30),p["ink"],570,11)
    d.text((62,1488),"GRID / SLAB / OPENING / ROUTE",font=base.get_font(18,bold=True),fill=p["gray"]); base.draw_page_mark(d,1,p["ink"])
    return img


def cover_rossi(book, assets):
    p=rgb(book); img=Image.new("RGB",(W,H),p["paper"]); d=ImageDraw.Draw(img)
    # Central memory line and a red urban artefact, deliberately unlike Terragni's grid.
    d.line((70,264,1170,264),fill=p["gray"],width=4); d.text((70,58),"ALDO ROSSI / THE ARCHITECTURE OF THE CITY / 01",font=base.get_font(20,bold=True),fill=p["ink"])
    d.text((70,115),"城市为何会",font=base.get_font(70,bold=True,serif=True),fill=p["ink"]); d.text((70,200),"记住建筑？",font=base.get_font(70,bold=True,serif=True),fill=p["ink"])
    photo=toned(base.crop(base.open_image(assets/"03-san-cataldo.jpg"),(W,650),(.5,.45)),.72,1.08); img.paste(photo,(0,330)); d=ImageDraw.Draw(img); d.rectangle((0,330,W,980),fill=(*p["ink"],55))
    d.rectangle((70,842,505,1320),fill=p["red"]); d.rectangle((102,875,473,1288),outline=p["paper"],width=8); d.text((125,980),"MEMORY\nARTEFACT",font=base.get_font(35,bold=True,serif=True),fill=p["paper"],spacing=8)
    base.paste_cover(img,base.open_image(assets/"cover.jpg"),(690,660,1124,1260),shadow=True); d=ImageDraw.Draw(img); label(d,710,1274,"MIT PRESS COVER",p["blue"],p["paper"],300)
    base.text_block(d,(70,1375),book["thesis"],base.get_font(31),p["ink"],1050,12); d.text((860,1540),"TYPE / TIME / CITY",font=base.get_font(18,bold=True),fill=p["blue"]); base.draw_page_mark(d,1,p["ink"])
    return img


def cover_superstudio(book, assets):
    p=rgb(book); img=Image.new("RGB",(W,H),p["paper"]); d=ImageDraw.Draw(img)
    d.text((64,50),"SUPERSTUDIO / LIFE WITHOUT OBJECTS / 01",font=base.get_font(20,bold=True),fill=p["ink"]); d.line((64,96,1175,96),fill=p["red"],width=8)
    d.text((66,164),"不再造物，",font=base.get_font(71,bold=True,serif=True),fill=p["ink"]); d.text((66,252),"建筑还能做什么？",font=base.get_font(62,bold=True,serif=True),fill=p["ink"])
    # A critical grid expands from the lower frame, no invented building or text.
    d.rectangle((0,520,W,H),fill=p["ink"])
    for x in range(-200,W+200,86): d.line((x,520,x+530,H),fill=p["gray"],width=2)
    for y in range(600,H,86): d.line((0,y,W,y),fill=p["gray"],width=2)
    base.paste_cover(img,base.open_image(assets/"cover.jpg"),(390,510,838,1170),shadow=True); d=ImageDraw.Draw(img); label(d,438,1185,"VERIFIED SKIRA COVER",p["yellow"],p["ink"],350)
    d.text((66,1286),"OBJECT → IMAGE → GRID → LIFE",font=base.get_font(25,bold=True),fill=p["yellow"])
    base.text_block(d,(66,1355),book["thesis"],base.get_font(31),p["paper"],1050,12); base.draw_page_mark(d,1,p["ink"],light=True)
    return img


def interior_photo(book, assets, number, style):
    p=rgb(book); title,headline,body,filename,tag=book["cards"][number-2]
    img=Image.new("RGB",(W,H),p["paper"]); d=ImageDraw.Draw(img)
    d.rectangle((0,0,W,108),fill=p["ink"]); d.text((62,32),f"{book['designer_en']} / {style.upper()} / 0{number}",font=base.get_font(20,bold=True),fill=p["paper"])
    photo=toned(base.crop(base.open_image(assets/filename),(W,795),(.5,.5)),.72,1.07); img.paste(photo,(0,108)); d=ImageDraw.Draw(img)
    d.rectangle((0,822,W,918),fill=p["ink"]); d.text((62,846),title,font=base.get_font(31,bold=True),fill=p["paper"]); d.text((1080,834),f"0{number}",font=base.get_font(48,bold=True,serif=True),fill=p.get("red",p.get("yellow")))
    d.text((68,940),tag,font=base.get_font(19,bold=True),fill=p.get("blue",p.get("yellow")))
    y=fit_title(d,(68,1010),headline,1065,47,p["ink"]); d.line((68,y+24,510,y+24),fill=p.get("red",p.get("yellow")),width=8); base.text_block(d,(70,y+62),body,base.get_font(29),p["ink"],1040,12)
    d.text((70,1562),f"{book['book_cn']} / {style.upper()}",font=base.get_font(18,bold=True),fill=p.get("gray",p.get("blue"))); base.draw_page_mark(d,number,p["ink"])
    return img


def interior_super_custom(book, number):
    p=rgb(book); title,headline,body,filename,tag=book["cards"][number-2]
    img=Image.new("RGB",(W,H),p["paper"]); d=ImageDraw.Draw(img); d.rectangle((0,0,W,108),fill=p["ink"]); d.text((62,32),f"SUPERSTUDIO / CRITICAL GRID / 0{number}",font=base.get_font(20,bold=True),fill=p["paper"])
    if number == 4:
        d.rectangle((0,108,W,900),fill=p["ink"])
        # A borderless grid crosses simple terrain lines: it is a critical diagram, not an image of a built work.
        for x in range(-250,W+300,90): d.line((x,108,x+850,900),fill=p["gray"],width=3)
        for y in range(190,900,90): d.line((0,y,W,y),fill=p["gray"],width=3)
        d.line((0,530,220,420,430,560,665,365,900,520,1242,390),fill=p["red"],width=12,joint="curve")
        d.text((66,165),"CONTINUOUS\nMONUMENT",font=base.get_font(57,bold=True,serif=True),fill=p["paper"],spacing=5)
        d.text((66,760),"UNBUILT CRITICAL PROJECT / 1969",font=base.get_font(20,bold=True),fill=p["yellow"])
    else:
        d.rectangle((0,108,W,900),fill=p["yellow"])
        for x in range(80,1210,74): d.line((x,150,x,850),fill=p["ink"],width=3)
        for y in range(150,850,74): d.line((80,y,1160,y),fill=p["ink"],width=3)
        d.rectangle((280,265,815,655),fill=p["paper"],outline=p["ink"],width=10)
        d.rectangle((822,355,1020,655),fill=p["paper"],outline=p["ink"],width=10)
        d.text((98,172),"QUADERNA / 1970",font=base.get_font(23,bold=True),fill=p["ink"])
        d.text((98,760),"GRID BECOMES AN OBJECT",font=base.get_font(20,bold=True),fill=p["red"])
    d=ImageDraw.Draw(img); d.rectangle((0,822,W,918),fill=p["ink"]); d.text((62,846),title,font=base.get_font(31,bold=True),fill=p["paper"]); d.text((1080,834),f"0{number}",font=base.get_font(48,bold=True,serif=True),fill=p["red"])
    d.text((68,940),tag,font=base.get_font(19,bold=True),fill=p["blue"]); y=fit_title(d,(68,1010),headline,1065,47,p["ink"]); d.line((68,y+24,510,y+24),fill=p["red"],width=8); base.text_block(d,(70,y+62),body,base.get_font(29),p["ink"],1040,12); base.draw_page_mark(d,number,p["ink"])
    return img


def summary_terragni(book):
    p=rgb(book); img=Image.new("RGB",(W,H),p["ink"]); d=ImageDraw.Draw(img); d.text((64,60),"把关系放进可读的框架",font=base.get_font(58,bold=True,serif=True),fill=p["paper"]); base.text_block(d,(68,152),book["summary"],base.get_font(29),p["warm"],1040,10)
    # Matrix grows from a structural grid to urban field.
    x0,y0=230,390; cells=[(2,2,"网格"),(1,3,"楼板"),(3,3,"开口"),(2,4,"路径"),(2,5,"城市")]
    for r in range(6):
        for c in range(5): d.rectangle((x0+c*150,y0+r*125,x0+c*150+150,y0+r*125+125),outline=p["gray"],width=2)
    for c,r,text in cells:
        x=x0+c*150+8;y=y0+r*125+10; d.rectangle((x,y,x+134,y+105),fill=p["red"] if text=="网格" else p["blue"]); d.text((x+18,y+35),text,font=base.get_font(27,bold=True),fill=p["paper"])
    for i,m in enumerate(book["methods"],1):
        x=72+(i-1)*382; d.rectangle((x,1190,x+338,1495),outline=[p["warm"],p["blue"],p["red"]][i-1],width=7); d.text((x+22,1218),f"METHOD 0{i}",font=base.get_font(18,bold=True),fill=[p["warm"],p["blue"],p["red"]][i-1]); base.text_block(d,(x+22,1265),m,base.get_font(25,bold=True),p["paper"],290,9)
    base.draw_page_mark(d,6,p["ink"],light=True); return img


def summary_rossi(book):
    p=rgb(book); img=Image.new("RGB",(W,H),p["paper"]); d=ImageDraw.Draw(img); d.text((66,62),"城市由重复的记忆组成",font=base.get_font(58,bold=True,serif=True),fill=p["ink"]); base.text_block(d,(70,152),book["summary"],base.get_font(29),p["blue"],1040,10)
    cx,cy=620,735; radii=[120,215,310]
    for r,col in zip(radii,[p["red"],p["yellow"],p["blue"]]): d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=col,width=9)
    for i,(name,angle) in enumerate(zip(book["chain"],[250,315,20,85,150]),1):
        import math
        x=cx+int(310*math.cos(math.radians(angle))); y=cy+int(310*math.sin(math.radians(angle))); d.ellipse((x-55,y-55,x+55,y+55),fill=p["ink"],outline=p["red"],width=5); d.text((x-31,y-16),name,font=base.get_font(21,bold=True),fill=p["paper"]); d.text((x-11,y+62),f"0{i}",font=base.get_font(16,bold=True),fill=p["red"])
    d.ellipse((cx-120,cy-120,cx+120,cy+120),fill=p["red"]); d.multiline_text((cx-72,cy-40),"集体\n记忆",font=base.get_font(31,bold=True),fill=p["paper"],spacing=4)
    for i,m in enumerate(book["methods"],1):
        x=72+(i-1)*382; d.rectangle((x,1190,x+338,1495),outline=[p["red"],p["yellow"],p["blue"]][i-1],width=7); d.text((x+22,1218),f"CITY NOTE 0{i}",font=base.get_font(18,bold=True),fill=[p["red"],p["yellow"],p["blue"]][i-1]); base.text_block(d,(x+22,1265),m,base.get_font(25,bold=True),p["ink"],290,9)
    base.draw_page_mark(d,6,p["ink"]); return img


def summary_super(book):
    p=rgb(book); img=Image.new("RGB",(W,H),p["paper"]); d=ImageDraw.Draw(img); d.text((64,62),"先暴露规则，再谈新形式",font=base.get_font(58,bold=True,serif=True),fill=p["ink"]); base.text_block(d,(68,152),book["summary"],base.get_font(29),p["red"],1040,10)
    # A network that keeps expanding outside the page logic.
    d.rectangle((0,380,W,1060),fill=p["ink"])
    for x in range(-300,W+300,92): d.line((x,380,x+500,1060),fill=p["gray"],width=3)
    for y in range(470,1060,92): d.line((0,y,W,y),fill=p["gray"],width=3)
    nodes=[(150,520),(390,640),(630,550),(860,710),(1080,580)]
    d.line(nodes,fill=p["yellow"],width=8,joint="curve")
    for i,((x,y),name) in enumerate(zip(nodes,book["chain"]),1): d.ellipse((x-48,y-48,x+48,y+48),fill=p["red"],outline=p["paper"],width=4); d.text((x-28,y-15),name,font=base.get_font(20,bold=True),fill=p["paper"]); d.text((x-9,y+54),f"0{i}",font=base.get_font(15,bold=True),fill=p["yellow"])
    for i,m in enumerate(book["methods"],1):
        x=72+(i-1)*382; d.rectangle((x,1190,x+338,1495),outline=[p["red"],p["yellow"],p["blue"]][i-1],width=7); d.text((x+22,1218),f"FOOTNOTE 0{i}",font=base.get_font(18,bold=True),fill=[p["red"],p["yellow"],p["blue"]][i-1]); base.text_block(d,(x+22,1265),m,base.get_font(25,bold=True),p["ink"],290,9)
    base.draw_page_mark(d,6,p["ink"]); return img


def save(image,path): path.parent.mkdir(parents=True,exist_ok=True); image.convert("RGB").save(path,"JPEG",quality=95,subsampling=0)

def preview(paths,out):
    tw,th,g=360,481,24; sheet=Image.new("RGB",(tw*3+g*4,th*2+g*3),(220,218,210))
    for i,path in enumerate(paths):
        with Image.open(path) as src: thumb=src.convert("RGB").resize((tw,th),Image.Resampling.LANCZOS)
        sheet.paste(thumb,(g+(i%3)*(tw+g),g+(i//3)*(th+g)))
    save(sheet.resize((1242,1108),Image.Resampling.LANCZOS),out)

def docs(book,assets,out):
    manifest=json.loads((assets/"manifest.json").read_text(encoding="utf-8")); lines=["# 图片来源","","| 文件名 | 内容 | 作者 / 机构 | 来源 URL | 许可 / 版权 | 修改 |","|---|---|---|---|---|---|"]
    for item in manifest: lines.append(f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item['modifications']} |")
    if book["designer"] == "超级工作室": lines += ["","02—05 均使用可核验的真实图像：展览复原现场、建成项目实景、原作展陈实拍和家具实物照片；未用自制示意图代替作品。"]
    lines += ["","书封仅用于书籍识别、介绍与评论；封面文字和构图保持原样，未重绘。","案例照片按来源许可进行裁切、缩放和轻微调色；图卡文字为编辑性概括。"]
    (out/"图片来源.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    publication=book["publish_title"]+"\n\n"+"\n\n".join(book["publish_paragraphs"])+"\n\n"+book["tags"]+"\n"; (out/"发布文案.md").write_text(publication,encoding="utf-8")
    post={"designer":book["designer"],"book":book["book"],"edition":book["edition"],"thesis":book["thesis"],"publish_title":book["publish_title"],"title_length":len(book["publish_title"]),"concept_chain":book["chain"],"endcards":book["endcards"],"transferable_methods":book["methods"],"sources":manifest,"cards":[{"number":"01","role":"problem cover","headline":book["question"],"asset":"cover.jpg"},*[{"number":f"{i:02d}","role":"mechanism" if i==2 else "evidence","headline":v[1],"evidence":v[0],"asset":v[3]} for i,v in enumerate(book["cards"],2)],{"number":"06","role":"synthesis","headline":book["summary"],"asset":""}]}
    (out/"post.json").write_text(json.dumps(post,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main():
    overview=[]
    for slug,book in BOOKS.items():
        if len(book["publish_title"])>20: raise ValueError(book["publish_title"])
        assets=ASSET_ROOT/slug; out=OUTPUT_ROOT/slug; out.mkdir(parents=True,exist_ok=True)
        if not (assets/"manifest.json").exists(): raise FileNotFoundError(assets)
        if book["system"]=="rational-frame": cards=[cover_terragni(book,assets)]+[interior_photo(book,assets,n,"rational frame") for n in range(2,6)]+[summary_terragni(book)]
        elif book["system"]=="memory-artefacts": cards=[cover_rossi(book,assets)]+[interior_photo(book,assets,n,"memory artefacts") for n in range(2,6)]+[summary_rossi(book)]
        else: cards=[cover_superstudio(book,assets)]+[interior_photo(book,assets,n,"critical grid") for n in range(2,6)]+[summary_super(book)]
        paths=[]
        for i,card in enumerate(cards,1): path=out/f"{i:02d}.jpg";save(card,path);paths.append(path)
        preview(paths,out/"preview.jpg");docs(book,assets,out);overview.append((book["designer"],out/"preview.jpg",rgb(book).get("red")))
        print(f"Rendered {slug}; title length={len(book['publish_title'])}")
    total=Image.new("RGB",(1242,3740),(236,233,224));d=ImageDraw.Draw(total);d.rectangle((0,0,W,148),fill=(16,28,35));d.text((58,42),"意大利建筑 / 三组代表作",font=base.get_font(43,bold=True,serif=True),fill=(246,243,234));y=185
    for title,path,color in overview:
        d.rectangle((58,y+4,76,y+42),fill=color);d.text((94,y),title,font=base.get_font(31,bold=True),fill=(16,28,35))
        with Image.open(path) as src: strip=src.convert("RGB").resize((1126,1005),Image.Resampling.LANCZOS)
        total.paste(strip,(58,y+58));y+=1170
    save(total,OUTPUT_ROOT/"总预览.jpg")

if __name__=="__main__": main()
