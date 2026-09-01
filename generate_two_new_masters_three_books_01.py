#!/usr/bin/env python3
"""Render three Casabella-inspired six-card posts for Siza, Siza and Niemeyer."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

import generate_three_unmentioned_masters as base


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets" / "two-new-masters-three-books-01"
OUTPUT_ROOT = ROOT / "output" / "two-new-masters-three-books-01"
W, H = 1242, 1660


BOOKS = {
    "alvaro-siza-imagining-the-evident": {
        "designer": "阿尔瓦罗·西扎",
        "designer_en": "ÁLVARO SIZA",
        "book": "Imagining the Evident",
        "book_cn": "《想象显而易见》",
        "edition": "monade, 2021｜ISBN 9789899948594",
        "question": "设计，为什么不是从发明新形式开始？",
        "thesis": "想象不是制造奇观，而是让场地、记忆、建造与既有关系逐步显现。",
        "system": "evident-trace",
        "palette": {"paper": "#EEE9DD", "ink": "#102438", "accent": "#D84B33", "second": "#5E7B80", "warm": "#D3B76C"},
        "cards": [
            ("Boa Nova 茶室", "形式先服从岩石、海岸与抵达路径", "屋面、墙体和台阶沿岩层展开。建筑没有替换海岸，而是把原本分散的边界组织成一段可进入、可停留的路径。", "02-boa-nova.jpg"),
            ("莱萨海水泳池", "少量墙体，也能把自然条件变成空间", "混凝土墙补足礁石之间的缺口，潮水、风与水平线仍是主体。设计的力量来自判断哪里需要介入，哪里必须保持开放。", "03-leca-pools.jpg"),
            ("马拉盖拉住宅区", "集体秩序不必抹掉个体差异", "低层住宅、连续基础设施与庭院建立稳定框架，住户仍能在其中调整生活。城市形态由长期使用逐步完成。", "04-malagueira.jpg"),
            ("加利西亚当代艺术中心", "新建筑可以接续城市，而不复制历史", "克制的石材体量回应修道院、街巷与坡地。几何并非孤立物体，而是把旧城关系重新校准的工具。", "05-cgac.jpg"),
        ],
        "summary": "好的形式不是突然被发明，而是在限制、记忆与建造之间被反复看见。",
        "chain": ["观察", "删减", "连接", "校准", "显现"],
        "methods": ["先标出不能被删除的既有条件", "用少量几何关系连接场地矛盾", "让形式在反复校准后再显现"],
        "endcards": {
            "01": {"layout_rationale": "竖向档案切片把场地照片、问题标题与放大的真实书封错位叠合；书封占据页面约三分之一。", "changed_variables": ["竖向切片", "左中大书封", "右侧场地窗口", "超大竖排问题"]},
            "06": {"layout_rationale": "五张错位描图纸从观察推进到显现，方法写在纸层边缘，模拟设计在痕迹中逐步变清楚。", "changed_variables": ["错位描图纸", "斜向概念链", "边缘方法注释", "浅色档案底"]},
        },
        "publish_title": "西扎：设计为什么不是从发明新形式开始？",
        "publish_body": "《Imagining the Evident》最值得设计师反复看的，不是西扎的白色体量，而是他如何让形式从既有条件里慢慢显现。Boa Nova 茶室沿岩石、海岸和抵达路径展开；莱萨海水泳池只用少量墙体补足礁石，把潮水与水平线留在空间中心；马拉盖拉住宅区用低层单元和基础设施建立集体秩序，同时允许住户继续改变生活；加利西亚当代艺术中心则以克制几何回应修道院、街巷与坡地。这里的“想象”并非无中生有，而是观察、删减、连接与校准。可带走的三步是：先标出不能删除的条件，再用最少关系解决矛盾，最后让形式在反复调整后出现。所谓原创往往不是抛开现场，而是发现其中尚未被组织的关系。本文为基于书籍与案例的编辑性概括，不是原书直接引语。",
        "tags": "#阿尔瓦罗西扎 #ImaginingTheEvident #建筑理论 #场地设计 #建筑书单 #设计方法 #建筑案例 #设计师必读",
    },
    "alvaro-siza-writings-on-architecture": {
        "designer": "阿尔瓦罗·西扎",
        "designer_en": "ÁLVARO SIZA",
        "book": "Writings on Architecture",
        "book_cn": "《建筑写作》",
        "edition": "Skira, 1997｜ISBN 9788881183159",
        "question": "写字和画草图，怎样改变建筑判断？",
        "thesis": "文字澄清矛盾，草图保留可能；它们不是作品完成后的说明，而是设计工具。",
        "system": "margin-notes",
        "palette": {"paper": "#F2EBDD", "ink": "#11283B", "accent": "#C83E35", "second": "#3D6E83", "warm": "#D7B75D"},
        "cards": [
            ("塞拉维斯当代艺术博物馆", "画下的不是物体，而是建筑与花园的距离", "展厅体量、路径和树木被放在同一张关系图里。草图先测试靠近、转折与留白，再决定建筑的轮廓。", "02-serralves.jpg"),
            ("1998 葡萄牙国家馆", "一个公共动作，来自持续删减", "薄而下垂的混凝土顶棚把广场压缩成清楚手势。方案的力量不在元素数量，而在每次比较后留下的那一个关系。", "03-portugal-pavilion.jpg"),
            ("圣玛利亚教堂", "草图可以同时测试光、尺度与仪式", "不对称开口、厚墙与行进序列共同组织礼拜体验。快速小图让尚未确定的空间关系保持可比较。", "04-santa-maria.jpg"),
            ("伊贝雷·卡马戈基金会", "剖面上的一条线，也会重写观看方式", "外置坡道、实体墙面与河岸构成连续运动。绘图在路径、结构与景观之间反复往返，避免造型先于判断。", "05-ibere-camargo.jpg"),
        ],
        "summary": "设计思考不只发生在模型里：文字把问题说清，草图让尚未决定的关系继续工作。",
        "chain": ["记录", "比较", "推迟", "取舍", "落定"],
        "methods": ["用一句话写出当前最难的矛盾", "连续画小草图，只比较空间关系", "决定前保留至少一个相反方案"],
        "endcards": {
            "01": {"layout_rationale": "深蓝编辑台面上放大真实书封，左侧以手稿边注和大标题形成文章首页；底部横向照片像折入的图版。", "changed_variables": ["横向编辑台", "右上大书封", "左侧边注", "底部折页照片"]},
            "06": {"layout_rationale": "总结页做成展开的双页手稿，中缝贯穿，概念链游走于页边，三条方法成为红色校订批注。", "changed_variables": ["双页中缝", "页边概念链", "红色校订", "文本手稿感"]},
        },
        "publish_title": "西扎：写字和画草图，怎样改变建筑判断？",
        "publish_body": "《Writings on Architecture》把西扎的文章、讲稿与设计思考放回工作过程。写字不是为完成的建筑补说明，草图也不是漂亮纪念品；两者都在延迟结论、保存矛盾。塞拉维斯博物馆通过小图比较展厅、路径与花园的距离；葡萄牙国家馆把复杂公共空间删减成一片下垂顶棚；圣玛利亚教堂在草图中同时测试光、厚墙、尺度与仪式；伊贝雷·卡马戈基金会则让坡道、实体和河岸在剖面里反复校准。对设计师更实用的工作法是：先用一句话写清最难的矛盾，再连续画小图比较关系而不是造型，并在决定前保留至少一个相反方案。文字负责聚焦，草图负责让可能性继续存在；方案卡住时，记录还能保留判断依据，让修改不必从零开始。本文为编辑性概括，不是原书直接引语。",
        "tags": "#阿尔瓦罗西扎 #WritingsOnArchitecture #建筑草图 #建筑写作 #设计方法 #建筑理论 #建筑书单 #建筑案例",
    },
    "oscar-niemeyer-curves-of-time": {
        "designer": "奥斯卡·尼迈耶",
        "designer_en": "OSCAR NIEMEYER",
        "book": "The Curves of Time",
        "book_cn": "《时间的曲线》",
        "edition": "Phaidon, 2007｜ISBN 9780714848570",
        "question": "曲线，怎样同时承载自由与公共性？",
        "thesis": "曲线不是任性的造型，它把身体、地景、结构想象与公共象征压缩成一个清楚动作。",
        "system": "public-curves",
        "palette": {"paper": "#F0E8D9", "ink": "#10283A", "accent": "#BF2E2A", "second": "#217687", "warm": "#E4C45C"},
        "cards": [
            ("潘普利亚圣方济各教堂", "拱壳把结构、屋面与轮廓合成一条曲线", "连续薄壳没有把技术藏在造型背后。结构本身制造起伏的内部，也把湖岸景观转译成新的宗教形象。", "02-pampulha.jpg"),
            ("巴西利亚大教堂", "重复构件可以围出开放而集体的中心", "十六根混凝土柱向上张开，结构、采光与象征同时发生。纪念性不靠封闭厚重，而来自共享天空的姿态。", "03-brasilia-cathedral.jpg"),
            ("巴西国会大厦", "简单几何也能表达制度关系", "塔楼、平台与相反曲率的碗形体量被压缩成可辨认的城市图像。公共权力通过轴线、尺度和空场被组织。", "04-national-congress.jpg"),
            ("尼泰罗伊当代艺术博物馆", "一条坡道，把建筑、身体与海湾串成连续镜头", "碟形体量被抬离地面，红色坡道延长抵达。曲线引导人的移动，也把观看城市变成展览的一部分。", "05-niteroi.jpg"),
        ],
        "summary": "曲线的价值不在奇特，而在它能否把结构、运动、地景与公共想象组织成同一个动作。",
        "chain": ["地景", "身体", "结构", "公共", "记忆"],
        "methods": ["先画出项目最重要的一次公共动作", "让结构逻辑参与主轮廓而非藏在背后", "用连续路径检验曲线是否真正可被体验"],
        "endcards": {
            "01": {"layout_rationale": "整页以尼迈耶书封的红色为主场，真实书封在左侧大比例出现，右侧白色曲线和项目照片构成强识别海报。", "changed_variables": ["满版红场", "左侧大书封", "右侧连续曲线", "底部城市图像"]},
            "06": {"layout_rationale": "一条巨大的连续曲线贯穿五个概念节点，三条方法悬挂在曲线内外，形成公共路径而非卡片网格。", "changed_variables": ["单笔连续曲线", "五个轨迹节点", "悬挂式方法", "深色公共场"]},
        },
        "publish_title": "尼迈耶：曲线怎样同时承载自由与公共性？",
        "publish_body": "《The Curves of Time》把尼迈耶的建筑与人生放在同一条流动叙事里。曲线对他而言并非任性造型，而是身体、地景、结构想象和公共象征的共同语言。潘普利亚圣方济各教堂用连续拱壳把结构与湖岸轮廓合在一起；巴西利亚大教堂让十六根混凝土柱向天空张开，纪念性因此变得明亮而共享；国会大厦以塔楼、平台和相反曲率的碗形体量压缩制度关系；尼泰罗伊当代艺术博物馆则用碟形体量与红色坡道，把抵达、展览和海湾景观串成连续镜头。对今天的设计师，关键不是复制曲线，而是先确定最重要的公共动作，让结构参与主轮廓，再用真实行走检验它是否成立。曲线只有进入结构、路径和集体经验，才不只是视觉符号。本文为基于回忆录与案例的编辑性概括，不是原书直接引语。",
        "tags": "#奥斯卡尼迈耶 #TheCurvesOfTime #现代建筑 #曲线建筑 #公共建筑 #建筑理论 #建筑书单 #巴西利亚",
    },
}


def rgb(book):
    return {key: base.hex_rgb(value) for key, value in book["palette"].items()}


def toned(image: Image.Image, brightness=1.0, saturation=0.85, contrast=1.03) -> Image.Image:
    out = image.convert("RGB")
    out = ImageEnhance.Color(out).enhance(saturation)
    out = ImageEnhance.Contrast(out).enhance(contrast)
    return ImageEnhance.Brightness(out).enhance(brightness)


def editorial_rule(draw: ImageDraw.ImageDraw, y: int, color, x0=70, x1=1172, width=3) -> None:
    draw.line((x0, y, x1, y), fill=color, width=width)


def small_label(draw, xy, text, foreground, background, width=None):
    x, y = xy
    font = base.get_font(19, bold=True)
    if width is None:
        width = draw.textbbox((0, 0), text, font=font)[2] + 34
    draw.rectangle((x, y, x + width, y + 48), fill=background)
    draw.text((x + 17, y + 11), text, font=font, fill=foreground)


def cover_evident(book, assets: Path) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["paper"])
    photo = toned(base.crop(base.open_image(assets / "02-boa-nova.jpg"), (470, 1160), (0.52, 0.48)), 0.68, 0.55)
    image.paste(photo, (772, 250))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 126), fill=p["ink"])
    draw.rectangle((742, 126, 772, H), fill=p["accent"])
    draw.text((70, 43), "CASABELLA / BOOK NOTE 01", font=base.get_font(22, bold=True), fill=p["warm"])
    draw.text((780, 44), book["designer_en"], font=base.get_font(25, bold=True), fill=p["paper"])
    base.text_block(draw, (70, 190), "设计，为什么\n不是从发明\n新形式开始？", base.get_font(70, bold=True, serif=True), p["ink"], 650, 7)
    editorial_rule(draw, 500, p["accent"], 70, 650, 10)
    base.text_block(draw, (72, 540), book["thesis"], base.get_font(29), p["second"], 560, 11)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (105, 780, 665, 1535), shadow=True)
    draw = ImageDraw.Draw(image)
    small_label(draw, (420, 1460), "VERIFIED COVER", p["paper"], p["accent"], 260)
    draw.text((790, 1445), "场地不是背景\n而是形式的证据", font=base.get_font(34, bold=True, serif=True), fill=p["paper"], spacing=12)
    draw.text((70, 1586), book["book_cn"], font=base.get_font(26, bold=True), fill=p["ink"])
    base.draw_page_mark(draw, 1, p["ink"], light=True)
    return image


def cover_writings(book, assets: Path) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 112), fill=p["accent"])
    draw.text((72, 35), "ARCHITECTURE / WRITINGS / 01", font=base.get_font(23, bold=True), fill=p["paper"])
    base.text_block(draw, (72, 182), "写字和画草图，\n怎样改变\n建筑判断？", base.get_font(67, bold=True, serif=True), p["paper"], 530, 7)
    for y in (540, 603, 666, 729):
        draw.line((72, y, 545 + (y % 90), y - 22), fill=p["second"], width=3)
    base.text_block(draw, (76, 770), book["thesis"], base.get_font(28), p["warm"], 475, 10)
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (610, 165, 1168, 1025), shadow=True)
    photo = toned(base.crop(base.open_image(assets / "03-portugal-pavilion.jpg"), (W, 510), (0.5, 0.55)), 0.72, 0.55)
    image.paste(photo, (0, 1150))
    draw = ImageDraw.Draw(image)
    draw.polygon([(0, 1060), (W, 980), (W, 1215), (0, 1280)], fill=p["paper"])
    draw.line((0, 1060, W, 980), fill=p["accent"], width=12)
    small_label(draw, (845, 1030), "VERIFIED BOOK COVER", p["paper"], p["accent"], 310)
    draw.text((76, 1094), book["book_cn"], font=base.get_font(31, bold=True), fill=p["ink"])
    draw.text((790, 1430), "文字聚焦 / 草图延迟", font=base.get_font(28, bold=True), fill=p["paper"])
    base.draw_page_mark(draw, 1, p["ink"], light=True)
    return image


def cover_niemeyer(book, assets: Path) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["accent"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 118), fill=p["paper"])
    draw.text((70, 35), "MEMOIR / STRUCTURE / PUBLIC LIFE", font=base.get_font(22, bold=True), fill=p["ink"])
    draw.text((925, 35), "01 / 06", font=base.get_font(24, bold=True), fill=p["accent"])
    base.paste_cover(image, base.open_image(assets / "cover.jpg"), (64, 200, 675, 1115), shadow=True)
    draw = ImageDraw.Draw(image)
    base.text_block(draw, (700, 190), "曲线，怎样\n同时承载\n自由与公共性？", base.get_font(66, bold=True, serif=True), p["paper"], 470, 7)
    for off in (0, 38, 76):
        pts = []
        for i in range(80):
            x = 675 + i * 7
            y = 700 + off + 105 * math.sin(i / 12)
            pts.append((int(x), int(y)))
        draw.line(pts, fill=p["paper"] if off == 0 else p["warm"], width=7 if off == 0 else 3)
    base.text_block(draw, (712, 905), book["thesis"], base.get_font(28), p["paper"], 420, 10)
    photo = toned(base.crop(base.open_image(assets / "05-niteroi.jpg"), (W, 440), (0.50, 0.52)), 0.76, 0.68)
    image.paste(photo, (0, 1220))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 1184, W, 1230), fill=p["ink"])
    small_label(draw, (390, 1100), "VERIFIED COVER", p["ink"], p["paper"], 255)
    draw.text((70, 1520), book["book_cn"], font=base.get_font(31, bold=True), fill=p["paper"])
    base.draw_page_mark(draw, 1, p["accent"])
    return image


def interior(book, assets: Path, number: int) -> Image.Image:
    p = rgb(book)
    title, headline, body, filename = book["cards"][number - 2]
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 112), fill=p["ink"])
    draw.text((70, 34), book["designer_en"], font=base.get_font(23, bold=True), fill=p["paper"])
    draw.text((785, 36), f"CASE STUDY / 0{number}", font=base.get_font(20, bold=True), fill=p["warm"])
    source = base.open_image(assets / filename)
    if book["system"] == "evident-trace":
        photo_w = 1040 if number % 2 == 0 else 990
        x = 0 if number % 2 == 0 else W - photo_w
        photo = toned(base.crop(source, (photo_w, 820), (0.5, 0.5)), 0.93, 0.78)
        image.paste(photo, (x, 112))
        draw = ImageDraw.Draw(image)
        side_x = 1040 if number % 2 == 0 else 0
        draw.rectangle((side_x, 112, side_x + 202, 932), fill=p["second"])
        for i in range(6):
            y = 170 + i * 118
            draw.line((side_x + 35, y, side_x + 166, y + (i % 2) * 26), fill=p["warm"], width=4)
        draw.rectangle((70, 850, 745, 930), fill=p["ink"])
    elif book["system"] == "margin-notes":
        photo = toned(base.crop(source, (1010, 820), (0.5, 0.5)), 0.92, 0.72)
        image.paste(photo, (232, 112))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 112, 232, 932), fill=p["paper"])
        draw.line((205, 112, 205, 932), fill=p["accent"], width=7)
        draw.text((55, 180), f"0{number}", font=base.get_font(82, bold=True, serif=True), fill=p["accent"])
        note = "记录\n关系\n比较\n尺度" if number % 2 == 0 else "保留\n矛盾\n推迟\n结论"
        draw.multiline_text((62, 355), note, font=base.get_font(29, bold=True), fill=p["second"], spacing=24)
        draw.rectangle((232, 850, 985, 930), fill=p["ink"])
    else:
        photo = toned(base.crop(source, (W, 850), (0.5, 0.52)), 0.90, 0.78)
        image.paste(photo, (0, 112))
        draw = ImageDraw.Draw(image)
        draw.arc((-180, 510, 1420, 1190), 190, 345, fill=p["accent"], width=28)
        draw.arc((-140, 540, 1380, 1160), 190, 345, fill=p["warm"], width=8)
        draw.rectangle((70, 872, 720, 952), fill=p["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((95 if book["system"] != "margin-notes" else 260, 873), title, font=base.get_font(31, bold=True), fill=p["paper"])
    draw.text((72, 1010), f"0{number}", font=base.get_font(26, bold=True), fill=p["accent"])
    y = base.text_block(draw, (72, 1060), headline, base.get_font(50, bold=True, serif=True), p["ink"], 1050, 8)
    editorial_rule(draw, y + 22, p["accent"], 74, 360, 8)
    base.text_block(draw, (76, y + 58), body, base.get_font(29), p["ink"], 1010, 12)
    draw.text((76, 1568), f"{book['book_cn']}  /  EDITORIAL READING", font=base.get_font(18, bold=True), fill=p["second"])
    base.draw_page_mark(draw, number, p["ink"], light=True)
    return image


def summary_evident(book) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["paper"])
    draw = ImageDraw.Draw(image)
    draw.text((70, 72), "形式，是被逐步看见的", font=base.get_font(62, bold=True, serif=True), fill=p["ink"])
    base.text_block(draw, (74, 165), book["summary"], base.get_font(29), p["second"], 940, 10)
    sheets = [(80, 430, 820, 810), (155, 585, 945, 975), (250, 745, 1080, 1135), (340, 905, 1160, 1305), (430, 1070, 1168, 1515)]
    for i, (box, label) in enumerate(zip(sheets, book["chain"])):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rectangle(box, fill=(*p["paper"], 230), outline=(*p["second"], 210), width=4)
        ld.text((box[0] + 28, box[1] + 24), f"0{i+1} / {label}", font=base.get_font(28, bold=True), fill=(*p["ink"], 255))
        ld.line((box[0] + 30, box[1] + 92, box[2] - 30, box[1] + 92), fill=(*p["accent"], 220), width=6)
        image = Image.alpha_composite(image.convert("RGBA"), layer).convert("RGB")
        draw = ImageDraw.Draw(image)
    method_xy = [(110, 530), (370, 860), (655, 1190)]
    for i, (method, (x, y)) in enumerate(zip(book["methods"], method_xy), 1):
        draw.text((x, y), f"METHOD {i}", font=base.get_font(17, bold=True), fill=p["accent"])
        base.text_block(draw, (x, y + 32), method, base.get_font(23, bold=True), p["ink"], 350, 7)
    base.draw_page_mark(draw, 6, p["ink"])
    return image


def summary_writings(book) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((60, 70, 610, 1590), fill=p["paper"])
    draw.rectangle((632, 70, 1182, 1590), fill=(236, 226, 208))
    draw.rectangle((610, 70, 632, 1590), fill=p["second"])
    draw.text((100, 112), "写清问题", font=base.get_font(55, bold=True, serif=True), fill=p["ink"])
    draw.text((675, 112), "保留可能", font=base.get_font(55, bold=True, serif=True), fill=p["ink"])
    base.text_block(draw, (102, 230), book["summary"], base.get_font(28), p["second"], 445, 10)
    chain_y = [560, 705, 850, 995, 1110]
    for i, (label, y) in enumerate(zip(book["chain"], chain_y)):
        x = 105 if i % 2 == 0 else 680
        draw.text((x, y), f"0{i+1}", font=base.get_font(24, bold=True), fill=p["accent"])
        draw.text((x + 55, y - 4), label, font=base.get_font(31, bold=True), fill=p["ink"])
        draw.line((x + 55, y + 46, x + 405, y + 18), fill=p["second"], width=3)
    method_y = [1225, 1355, 1470]
    for i, (method, y) in enumerate(zip(book["methods"], method_y), 1):
        x = 95 if i != 2 else 655
        draw.rectangle((x, y, x + 500, y + 104), outline=p["accent"], width=5)
        draw.text((x + 18, y + 15), f"批注 {i}", font=base.get_font(19, bold=True), fill=p["accent"])
        base.text_block(draw, (x + 105, y + 14), method, base.get_font(23, bold=True), p["ink"], 360, 6)
    base.draw_page_mark(draw, 6, p["ink"], light=True)
    return image


def summary_niemeyer(book) -> Image.Image:
    p = rgb(book)
    image = Image.new("RGB", (W, H), p["ink"])
    draw = ImageDraw.Draw(image)
    draw.text((70, 74), "曲线不是答案，公共动作才是", font=base.get_font(58, bold=True, serif=True), fill=p["paper"])
    base.text_block(draw, (75, 170), book["summary"], base.get_font(29), p["warm"], 990, 10)
    points = []
    for i in range(121):
        x = 40 + i * 9.7
        y = 770 + 260 * math.sin(i / 18) + 55 * math.sin(i / 5.8)
        points.append((int(x), int(y)))
    draw.line(points, fill=p["accent"], width=28, joint="curve")
    draw.line([(x, y - 20) for x, y in points], fill=p["paper"], width=5, joint="curve")
    indexes = [8, 34, 60, 88, 112]
    for i, (idx, label) in enumerate(zip(indexes, book["chain"])):
        x, y = points[idx]
        draw.ellipse((x - 30, y - 30, x + 30, y + 30), fill=p["warm"], outline=p["paper"], width=5)
        draw.text((x - 28, y - 105 if i % 2 == 0 else y + 42), label, font=base.get_font(29, bold=True), fill=p["paper"])
    method_boxes = [(70, 1250, 390, 1530), (455, 1110, 785, 1390), (850, 1260, 1172, 1540)]
    for i, (method, box) in enumerate(zip(book["methods"], method_boxes), 1):
        draw.rounded_rectangle(box, radius=90, fill=p["second"] if i != 2 else p["accent"])
        draw.text((box[0] + 30, box[1] + 28), f"0{i}", font=base.get_font(27, bold=True), fill=p["warm"])
        base.text_block(draw, (box[0] + 30, box[1] + 84), method, base.get_font(24, bold=True), p["paper"], box[2] - box[0] - 60, 8)
    base.draw_page_mark(draw, 6, p["ink"], light=True)
    return image


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0)


def make_preview(paths: list[Path], output: Path) -> None:
    tw, th, gap = 360, 481, 24
    sheet = Image.new("RGB", (tw * 3 + gap * 4, th * 2 + gap * 3), (218, 216, 208))
    for i, path in enumerate(paths):
        with Image.open(path) as source:
            thumb = source.convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
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
        source_lines.append(f"| {item['filename']} | {item['content']} | {item['credit']} | {item['source_url']} | {item['license']} | {item['modifications']} |")
    source_lines += [
        "",
        "书封仅用于书籍识别、介绍与评论；书封未重绘，封面文字与构图均保持原样。",
        "案例照片按来源许可裁切、缩放和轻微调色；图卡文字为编辑性概括，不作为原书直接引语。",
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
            *[{"number": f"{i:02d}", "role": "mechanism" if i == 2 else "evidence", "headline": card[1], "evidence": card[0], "asset": card[3]} for i, card in enumerate(book["cards"], start=2)],
            {"number": "06", "role": "synthesis", "headline": book["summary"], "asset": ""},
        ],
        "endcards": book["endcards"],
        "transferable_methods": book["methods"],
        "sources": manifest,
    }
    (output / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    previews: list[tuple[str, Path]] = []
    for slug, book in BOOKS.items():
        assets = ASSET_ROOT / slug
        output = OUTPUT_ROOT / slug
        output.mkdir(parents=True, exist_ok=True)
        if not (assets / "manifest.json").exists():
            raise FileNotFoundError(f"Missing assets: {assets}")
        if book["system"] == "evident-trace":
            first, last = cover_evident(book, assets), summary_evident(book)
        elif book["system"] == "margin-notes":
            first, last = cover_writings(book, assets), summary_writings(book)
        else:
            first, last = cover_niemeyer(book, assets), summary_niemeyer(book)
        cards = [first] + [interior(book, assets, number) for number in range(2, 6)] + [last]
        paths = []
        for number, card in enumerate(cards, 1):
            path = output / f"{number:02d}.jpg"
            save(card, path)
            paths.append(path)
        make_preview(paths, output / "preview.jpg")
        write_docs(book, assets, output)
        previews.append((book["book_cn"], output / "preview.jpg"))
        print(f"Rendered {slug}")

    total = Image.new("RGB", (1242, 3560), (233, 229, 219))
    d = ImageDraw.Draw(total)
    d.rectangle((0, 0, 1242, 150), fill=(16, 36, 56))
    d.text((58, 45), "两位新大师 / 三本建筑书", font=base.get_font(46, bold=True, serif=True), fill=(245, 240, 229))
    y = 190
    for title, path in previews:
        d.text((58, y), title, font=base.get_font(30, bold=True), fill=(16, 36, 56))
        with Image.open(path) as source:
            strip = source.convert("RGB").resize((1126, 1005), Image.Resampling.LANCZOS)
        total.paste(strip, (58, y + 55))
        y += 1110
    save(total, OUTPUT_ROOT / "总预览.jpg")


if __name__ == "__main__":
    main()
