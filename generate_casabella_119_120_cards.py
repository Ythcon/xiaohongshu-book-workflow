from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    BLUE,
    FONT_BOLD,
    FONT_SANS,
    FONT_SERIF,
    H,
    INK,
    LIGHT,
    MUTED,
    PAPER,
    ROOT,
    W,
    draw_fit,
    font,
    header,
    make_card,
    make_preview,
    mount,
    page_mark,
    paper_canvas,
    rgba,
)


ISSUES = [
    {
        "slug": "casabella-119",
        "issue": "CASABELLA 119",
        "date": "NOVEMBRE 1937 · ANNO X",
        "date_cn": "1937年11月",
        "cover": "book-cover.jpg",
        "accent": "#b84f3e",
        "question": "现代性不是样式，\n而是可以被使用的秩序",
        "thesis_label": "比例 · 材料 · 日常动作",
        "thesis": "119期把“意大利性”从历史样式中抽离出来：空间应先建立清楚的比例、材料触感和人的使用节奏，再谈它看起来属于哪里。Bega的室内、商店与展亭把这件事做得格外具体。",
        "summary": "地域性不是把旧元素贴回墙面，而是让空间的尺度、光线、材料和使用方式同时落在当地生活里。现代性由此获得位置感，而不是复制一套通用造型。",
        "concepts": ["尺度可被身体读取", "材料参与组织空间", "街道与室内连续"],
        "takeaways": [
            "先用行走、停留、就坐和观看确定尺度，再选择是否需要装饰。",
            "把地面、墙面、照明和陈列视为同一套空间构成，而不是彼此独立的饰面。",
            "商业与公共入口要把招牌、橱窗和人的动线编在一起，让室内主动回应街道。",
        ],
        "publish_title": "119期｜现代性不是样式",
        "publish_body": "Casabella 119最有力的提问，是怎样寻找一种不依赖历史样式的“意大利性”。Giuseppe Pagano的答案并不指向柱式或图案，而指向更难被复制的空间品质：比例的清晰、构造的逻辑、材料的真实，以及人与场所之间稳定的日常关系。\n\n同一期对Melchiorre Bega的关注，把这个判断落到商店、展亭、室内和住宅。米兰Motta商店用连续的陈列与细密灯光让商品成为空间深度的一部分；Perugina展亭把品牌字母、夜间照明和轻质框架合为一个街道界面；博尔扎诺Palazzo Reale的室内则不靠堆叠装饰，而用地面纹样、墙面肌理和家具位置组织停留。\n\n这些案例提示我们：风格并不等于地方性。真正可迁移的方法是先让身体读懂空间，再让材料参与空间，最后让室内把街道接进来。",
        "tags": "#Casabella #建筑杂志 #现代建筑 #室内设计 #商业空间 #建筑材料 #空间设计 #建筑历史",
        "cards": [
            {
                "image": "bega-4.png", "mode": "photo", "accent": "#b84f3e", "focal": (0.50, 0.52),
                "source": "Melchiorre Bega｜Motta商店，米兰｜Casabella 119",
                "eyebrow": "观点 01｜陈列必须形成空间深度",
                "title": "让商品沿视线连续展开，商店才不会只是堆满货架的房间",
                "body": "细密陈列、顶面照明与纵深通道共同延长了观看距离。人先被空间引导向前，再逐步接近商品；消费行为因此被编进一条清楚的行走序列。",
            },
            {
                "image": "bega-5.png", "mode": "photo", "accent": "#3f7894", "focal": (0.52, 0.48),
                "source": "Melchiorre Bega｜Perugina展亭，米兰｜Casabella 119",
                "eyebrow": "观点 02｜文字可以成为立面构件",
                "title": "招牌、灯光与轻质框架一起工作，让品牌从平面变成街道界面",
                "body": "体量并不靠厚重墙体建立存在感。悬置的字母、透明转角和水平屋架共同构成夜间可读的立面，让识别、进入和停留发生在同一个框架里。",
            },
            {
                "image": "bega-6.png", "mode": "photo", "accent": "#71816f", "focal": (0.50, 0.50),
                "source": "Melchiorre Bega｜Palazzo Reale，博尔扎诺｜Casabella 119",
                "eyebrow": "观点 03｜地面先规定停留方式",
                "title": "用地面图形、家具位置与吊灯中心对齐，让房间先获得可读的秩序",
                "body": "室内的重心不必来自堆叠摆设。中心图形给出停留位置，家具围绕边界布置，顶部灯具固定视线焦点；身体进入房间时，立刻能判断朝向和距离。",
            },
            {
                "image": "bega-7.png", "mode": "photo", "accent": "#b84f3e", "focal": (0.53, 0.53),
                "source": "Melchiorre Bega｜Palazzo Reale，博尔扎诺｜Casabella 119",
                "eyebrow": "观点 04｜墙面不是背景，而是尺度工具",
                "title": "重复纹理把大墙拆成可感知的节奏，也给床与座椅明确的靠背",
                "body": "墙面格纹不是附加花样。它把宽大的室内分成可阅读的段落，控制视觉密度，并让家具获得稳定的尺度参照；材料因此直接参与空间组织。",
            },
            {
                "image": "bega-8.png", "mode": "photo", "accent": "#3f7894", "focal": (0.50, 0.48),
                "source": "Melchiorre Bega｜Oceanarium展亭，博洛尼亚｜Casabella 119",
                "eyebrow": "观点 05｜展亭要把观看推向场地",
                "title": "轻体量贴近水面与树影布置，展览从封闭房间延伸到整片场地",
                "body": "临水的开口和水平边界让建筑不再只容纳展品，也把树影、倒影与步行路径纳入体验。临时建筑的强度，来自它如何放大周边环境。",
            },
            {
                "image": "bega-11.png", "mode": "photo", "accent": "#71816f", "focal": (0.51, 0.53),
                "source": "Melchiorre Bega｜私人公寓，博洛尼亚｜Casabella 119",
                "eyebrow": "观点 06｜日常动作决定室内线条",
                "title": "柜台、转角与照明围绕工作动作布置，功能可以直接生成室内表情",
                "body": "好的室内不需要另加一层“现代感”。把收纳、操作台、等候和照明沿着真实使用顺序安排，曲线与直线就会自然出现，并让空间保持清晰和易用。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella 119官方历史封面｜Casabella官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/119-nz.jpg",
            "`bega-4.png`｜Melchiorre Bega，Motta商店，米兰｜Domus历史档案｜https://www.domusweb.it/en/biographies/melchiorre-bega.html",
            "`bega-5.png`｜Melchiorre Bega，Perugina展亭，米兰｜Domus历史档案｜https://www.domusweb.it/en/biographies/melchiorre-bega.html",
            "`bega-6.png`｜Melchiorre Bega，Palazzo Reale，博尔扎诺｜Domus历史档案｜https://www.domusweb.it/en/biographies/melchiorre-bega.html",
            "`bega-7.png`｜Melchiorre Bega，Palazzo Reale，博尔扎诺｜Domus历史档案｜https://www.domusweb.it/en/biographies/melchiorre-bega.html",
            "`bega-8.png`｜Melchiorre Bega，Oceanarium展亭，博洛尼亚｜Domus历史档案｜https://www.domusweb.it/en/biographies/melchiorre-bega.html",
            "`bega-11.png`｜Melchiorre Bega，1930年代室内项目｜Domus历史档案｜https://www.domusweb.it/en/biographies/melchiorre-bega.html",
            "文章目录与页码｜Raffaello Giolli《L’opera di Melchiorre Bega》，Casabella 119，pp. 6–9｜Bologna Online｜https://www.bibliotecasalaborsa.it/bolognaonline/cronologia-di-bologna/1937/gli-arredamenti-della-ditta-bega",
            "文章信息｜Giuseppe Pagano《Alla ricerca dell’italianità》，Casabella 119｜Politecnico di Torino WebThesis｜https://webthesis.biblio.polito.it/2806/",
        ],
    },
    {
        "slug": "casabella-120",
        "issue": "CASABELLA 120",
        "date": "DICEMBRE 1937 · ANNO X",
        "date_cn": "1937年12月",
        "cover": "book-cover.jpg",
        "accent": "#3f7894",
        "question": "住宅不是物件，\n而是一套环境装置",
        "thesis_label": "视线 · 气候 · 可变生活",
        "thesis": "120期把美国住宅当作一种环境技术：平面从家庭动作与地形条件出发，玻璃、遮阳、露台与轻质构造共同控制视野、温度、隐私和未来变化。",
        "summary": "轻质住宅的关键不在“玻璃盒子”的外观，而在不断校准几组关系：开放面朝向什么景观，实体墙保护什么隐私，服务与睡眠如何退出公共空间，以及日常变化有没有预留余地。",
        "concepts": ["平面先回应生活", "开口同时处理气候", "结构支持未来变化"],
        "takeaways": [
            "从家庭成员、停留方式、眺望方向和服务需求开始画平面，不要先定立面。",
            "玻璃面必须与挑檐、实体墙、树影和窗高一起设计，开放不等于暴露。",
            "用轻质框架、集中服务和可变隔断预留调整空间，让住宅能跟着生活改变。",
        ],
        "publish_title": "120期｜住宅如何变成装置",
        "publish_body": "Casabella 120把目光投向美国，连续刊出Gropius、Neutra及多座加州住宅。它关心的不是“美国风格”，而是住宅怎样从一件固定物品变成能应对气候、地形、家庭关系和技术变化的环境装置。\n\nWestwood住宅用几组相互连通的起居空间争取小面积里的公共性；Grace Miller的棕榈泉住宅把工作、起居与室外休憩组织进紧凑平面；Barsha住宅则把实体北墙、玻璃侧墙、高窗与挑檐组合起来，同时处理景观、隐私与日晒。Ruben住宅顺着山坡悬挑，让视野成为平面的一部分；Kun住宅用连续桁架与轻质构造，把玻璃、阳台和陡坡连接成一套系统。\n\n这期给出的结论非常直接：平面先回应生活，开口同时处理气候，结构则为未来变化留出余地。",
        "tags": "#Casabella #建筑杂志 #RichardNeutra #现代住宅 #加州现代主义 #建筑设计 #住宅设计 #空间设计",
        "cards": [
            {
                "image": "02-westwood-photo.jpg", "mode": "photo", "accent": "#3f7894", "focal": (0.56, 0.48),
                "source": "Richard J. Neutra｜Westwood住宅｜Casabella 120",
                "eyebrow": "观点 01｜公共空间可以由几个起居湾组成",
                "title": "起居、就餐与阅读彼此连通，小面积也能获得连续而不单调的公共性",
                "body": "平面没有把日常活动塞进一个大房间，而是用相邻的活动湾形成层次。书架、壁炉和开口承担软分隔，让家庭成员可以同时停留又不互相干扰。",
            },
            {
                "image": "03-miller.png", "mode": "document", "accent": "#b84f3e",
                "source": "Richard J. Neutra｜Grace L. Miller住宅，棕榈泉｜Casabella 120",
                "eyebrow": "观点 02｜服务核心要释放可变房间",
                "title": "把设备与收纳集中起来，工作、休息和接待才能在紧凑住宅里切换",
                "body": "住宅把个人工作室、起居与室外空间拉到同一生活半径内。服务空间尽量收紧，活动区保持连续，必要时再用帘幕或轻隔断改变使用状态。",
            },
            {
                "image": "04-barsha-plan.png", "mode": "document", "accent": "#71816f",
                "source": "Richard J. Neutra｜Barsha住宅，北好莱坞｜Casabella 120",
                "eyebrow": "观点 03｜平面先分开睡眠、服务与起居",
                "title": "T形布局把车库、卧室与公共起居分成三翼，走廊成为安静的缓冲带",
                "body": "私密与服务功能各自占据一条翼部，中央留给起居和就餐。短走廊连接两端，也悄悄分开喧闹与安静；功能关系由平面本身完成，而不是靠门一层层封闭。",
            },
            {
                "image": "05-barsha-photo.png", "mode": "document", "accent": "#3f7894",
                "source": "Richard J. Neutra｜Barsha住宅，北好莱坞｜Casabella 120",
                "eyebrow": "观点 04｜玻璃与实体墙必须各司其职",
                "title": "向景观打开玻璃面，向邻里保留实体与高窗，让通透不牺牲私密",
                "body": "Barsha住宅把不同方向的墙当成不同性能层：有景观的一侧开大玻璃，受暴晒处设置挑檐，缺少视野或需要隐私的一侧改用实体墙和高窗。",
            },
            {
                "image": "06-ruben-photo.jpg", "mode": "photo", "accent": "#b84f3e", "focal": (0.56, 0.48),
                "source": "Richard J. Neutra｜Ruben住宅，圣莫尼卡｜Casabella 120",
                "eyebrow": "观点 05｜地形可以直接决定起居方向",
                "title": "房屋沿陡坡悬挑，露台与大开口把远景变成每天都被使用的房间边界",
                "body": "面对下落地形，建筑不退回封闭盒子，而是让起居面向山谷和海景展开。露台不是附加平台，它延续室内地面，也把结构、视野和停留方式绑在一起。",
            },
            {
                "image": "kun-01.jpg", "mode": "photo", "accent": "#71816f", "focal": (0.55, 0.55),
                "source": "Richard J. Neutra｜Kun住宅，好莱坞｜Casabella 120",
                "eyebrow": "观点 06｜轻质结构让建筑贴近陡坡",
                "title": "连续桁架、玻璃与长阳台协同工作，让入口高度、山坡与远景形成完整剖面",
                "body": "Kun住宅从街道高处进入，再顺着坡度向下展开。轻质框架减小对陡坡的干预，玻璃把远景引入室内，长阳台则把房间延伸为可以停留的气候缓冲层。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella 120官方历史封面｜Casabella官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/120-nz.jpg",
            "`02-westwood.png`｜Richard J. Neutra，Westwood住宅，1937｜The Modern House in America｜USModernist Archives｜https://www.usmodernist.org/1940modernhouseinamerica.pdf",
            "`03-miller.png`｜Richard J. Neutra，Grace L. Miller住宅，棕榈泉｜The Modern House in America｜USModernist Archives｜https://www.usmodernist.org/1940modernhouseinamerica.pdf",
            "`04-barsha-plan.png`｜Richard J. Neutra，Barsha住宅平面与总平面｜Architectural Record历史图版｜https://www.usmodernist.org/AR/AR-1938-07.pdf",
            "`05-barsha-photo.png`｜Richard J. Neutra，Barsha住宅外观与轴测｜Architectural Record历史图版｜https://www.usmodernist.org/AR/AR-1938-07.pdf",
            "`06-ruben.png`｜Richard J. Neutra，Ruben住宅，圣莫尼卡｜The Modern House in America｜USModernist Archives｜https://www.usmodernist.org/1940modernhouseinamerica.pdf",
            "`kun-01.jpg`｜Richard J. Neutra，Josef与Gertrud Kun住宅｜Neutra Institute / Shulman Photo Archive｜https://neutra.org/project/josef-and-gregory-kun-house-1/",
            "目录与文章信息｜Casabella 120，Impressioni d’America及Neutra案例目录｜Casa dell’Architettura Latina｜https://www.casadellarchitettura.eu/collezioni/riviste/casabella/",
        ],
    },
]


def save_rgb(image: Image.Image, path: Path) -> Path:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def prepare_assets(cfg: dict, src: Path) -> None:
    if cfg["slug"] == "casabella-120":
        page = Image.open(src / "02-westwood.png").convert("RGB")
        photo = page.crop((110, 120, 1215, 760))
        photo = ImageEnhance.Contrast(photo).enhance(1.08)
        photo = ImageEnhance.Sharpness(photo).enhance(1.18)
        photo.save(src / "02-westwood-photo.jpg", quality=96, subsampling=0)
        page = Image.open(src / "06-ruben.png").convert("RGB")
        photo = page.crop((18, 95, 1280, 625))
        photo = ImageEnhance.Contrast(photo).enhance(1.08)
        photo = ImageEnhance.Sharpness(photo).enhance(1.18)
        photo.save(src / "06-ruben-photo.jpg", quality=96, subsampling=0)


def make_cover_119(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(11901)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 32), fill=accent)
    draw.rectangle((0, 0, 190, H), fill="#dfd5c7")
    draw.text((68, 58), cfg["issue"], font=font(FONT_BOLD, 27), fill=INK)
    draw.text((1170, 60), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(INK, 175), anchor="ra")
    draw.text((232, 145), "单期主线", font=font(FONT_BOLD, 23), fill=accent)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
    mount(canvas, cover, (318, 206, 610, 805), True)
    draw.text((232, 1040), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (232, 1108), cfg["question"], 900, 175, 58, INK, serif=True, spacing=13)
    draw.line((232, 1333, 1168, 1333), fill=accent, width=7)
    draw_fit(draw, (232, 1385), cfg["thesis"], 900, 170, 30, rgba(INK, 215), serif=True, spacing=11)
    draw.text((94, 1388), "119", font=font(FONT_BOLD, 64), fill=accent, anchor="ma")
    page_mark(draw, 1, False)
    return save_rgb(canvas, out / "01.jpg")


def make_cover_120(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(LIGHT))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((808, 0, W, H), fill=BLUE)
    draw.rectangle((0, 1055, W, H), fill="#e4edf0")
    draw.text((68, 58), cfg["issue"], font=font(FONT_BOLD, 27), fill=INK)
    draw.text((1170, 60), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(LIGHT, 185), anchor="ra")
    draw.text((68, 155), "单期主线", font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (68, 230), cfg["question"], 610, 370, 65, INK, serif=True, spacing=14)
    draw.text((68, 700), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (68, 770), cfg["thesis"], 595, 260, 31, rgba(INK, 215), serif=True, spacing=12)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
    mount(canvas, cover, (670, 125, 500, 830), True)
    draw.text((68, 1150), "住宅如何成为环境装置？", font=font(FONT_BOLD, 39), fill=BLUE)
    draw_fit(draw, (68, 1235), "让平面、开口和轻质构造一起回应生活、气候与地形。", 1030, 155, 44, INK, serif=True, spacing=14)
    draw.rectangle((68, 1480, 1168, 1490), fill=accent)
    page_mark(draw, 1, False)
    return save_rgb(canvas, out / "01.jpg")


def make_summary_119(cfg: dict, out: Path) -> Path:
    canvas = paper_canvas(11908)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    header(draw, cfg, 8, False)
    draw.rectangle((68, 150, 80, 530), fill=accent)
    draw.text((112, 150), "把地方性做成空间品质", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (112, 220), cfg["summary"], 1010, 260, 50, INK, serif=True, spacing=17)
    colors = ["#b84f3e", "#3f7894", "#71816f"]
    xs = [68, 442, 816]
    for idx, (x, label, body, color) in enumerate(zip(xs, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.rounded_rectangle((x, 670, x + 330, 1428), 12, fill=color)
        draw.text((x + 38, 718), f"0{idx}", font=font(FONT_BOLD, 38), fill=rgba(LIGHT, 155))
        draw_fit(draw, (x + 38, 800), label, 254, 120, 35, LIGHT, serif=True, spacing=10)
        draw.line((x + 38, 955, x + 292, 955), fill=rgba(LIGHT, 115), width=2)
        draw_fit(draw, (x + 38, 1005), body, 254, 300, 31, LIGHT, serif=True, spacing=11)
    page_mark(draw, 8, False)
    return save_rgb(canvas, out / "08.jpg")


def make_summary_120(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#e6eef0"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    header(draw, cfg, 8, False)
    draw.text((72, 150), "现代住宅的三项校准", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (72, 220), cfg["summary"], 1080, 270, 48, INK, serif=True, spacing=17)
    colors = ["#3f7894", "#b84f3e", "#71816f"]
    ys = [650, 915, 1180]
    for idx, (y, label, body, color) in enumerate(zip(ys, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.rounded_rectangle((72, y, 1170, y + 198), 12, fill=rgba(LIGHT))
        draw.rectangle((72, y, 220, y + 198), fill=color)
        draw.text((146, y + 70), f"0{idx}", font=font(FONT_BOLD, 46), fill=rgba(LIGHT, 180), anchor="mm")
        draw.text((258, y + 43), label, font=font(FONT_BOLD, 35), fill=color)
        draw.line((258, y + 106, 1128, y + 106), fill=rgba(color, 80), width=2)
        draw_fit(draw, (258, y + 128), body, 835, 54, 28, rgba(INK, 215), serif=True, spacing=8)
    page_mark(draw, 8, False)
    return save_rgb(canvas, out / "08.jpg")


def post_manifest(cfg: dict) -> dict:
    return {
        "type": "magazine",
        "slug": cfg["slug"],
        "issue": cfg["issue"].title(),
        "date": cfg["date_cn"],
        "core_question": cfg["question"].replace("\n", ""),
        "core_thesis": cfg["thesis"],
        "pages": [
            f"01 单期主线：{cfg['question'].replace(chr(10), '')}",
            *[f"{n:02d} {card['source'].split('｜')[1]}：{card['title']}" for n, card in enumerate(cfg["cards"], 2)],
            f"08 总结：{'、'.join(cfg['concepts'])}",
        ],
    }


def write_text_files(cfg: dict, out: Path) -> None:
    (out / "发布文案.md").write_text(
        f"{cfg['publish_title']}\n\n{cfg['publish_body']}\n\n{cfg['tags']}\n", encoding="utf-8"
    )
    (out / "图片来源.md").write_text(
        f"# {cfg['issue'].title()} 图片来源\n\n" + "\n".join(f"- {line}" for line in cfg["sources"]) + "\n",
        encoding="utf-8",
    )
    post_dir = ROOT / "posts" / cfg["slug"]
    post_dir.mkdir(parents=True, exist_ok=True)
    (post_dir / "post.json").write_text(json.dumps(post_manifest(cfg), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_issue(cfg: dict) -> None:
    src = ROOT / "assets" / cfg["slug"]
    out = ROOT / "output" / cfg["slug"]
    out.mkdir(parents=True, exist_ok=True)
    prepare_assets(cfg, src)
    cover_maker = make_cover_119 if cfg["slug"] == "casabella-119" else make_cover_120
    summary_maker = make_summary_119 if cfg["slug"] == "casabella-119" else make_summary_120
    paths = [cover_maker(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(summary_maker(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards, preview and publishing files in {out}")


if __name__ == "__main__":
    for issue in ISSUES:
        render_issue(issue)
