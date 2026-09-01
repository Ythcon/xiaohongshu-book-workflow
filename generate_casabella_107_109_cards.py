from __future__ import annotations

import json
from pathlib import Path

import fitz
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
        "slug": "casabella-107",
        "issue": "CASABELLA 107",
        "date": "NOVEMBRE 1936 · ANNO IX",
        "date_cn": "1936年11月",
        "accent": "#df6333",
        "cover": "book-cover.jpg",
        "question": "现代建筑如何\n在城市、公共建筑\n与展馆之间\n建立秩序？",
        "thesis_label": "城市 × 构架 × 公共性",
        "thesis": "从科莫的公共建筑到亚的斯亚贝巴规划，再到巴黎世博展馆，现代性表现为尺度不同、但可以被清楚阅读的空间秩序。",
        "summary": "107期把现代建筑放在多种尺度上比较：城市靠轴线与分区，公共建筑靠结构和空隙，展馆靠路径与轻构架。",
        "concepts": ["城市轴线", "结构秩序", "观看路径"],
        "takeaways": [
            "大尺度规划先确定公共中心与交通轴线，再组织分区。",
            "公共建筑用结构、开敞面与入口把制度转成可见空间。",
            "临时展馆以轻构架和连续路径建立新的观看方式。",
        ],
        "publish_title": "Casabella107｜三种尺度的秩序",
        "publish_body": "Casabella 107 把现代建筑放进城市、公共建筑和临时展馆三种尺度中比较。它关心的不是统一的外观，而是不同尺度如何形成清楚、可被使用的空间秩序。\n\nTerragni 的科莫法西斯宫用规则框架、深凹开间与开放入口，把公共建筑从封闭纪念物变成可以被街道阅读的立面。Valle 与 Guidi 的亚的斯亚贝巴规划则说明，城市秩序首先来自公共中心、交通轴线与功能分区之间的关系。\n\n到了巴黎世博会，芬兰馆和日本馆不再依靠沉重体量，而是用轻构架、庭院和连续路径组织观看。Duiker 的 Gooiland 酒店进一步把交通、入口和公共活动叠合成复合建筑。Brunelleschi 穹顶则提醒我们：现代性并不等于拒绝历史，结构逻辑本身就可以跨时代地被重新理解。\n\n你更关心现代建筑在城市尺度上的秩序，还是人在内部行走时的空间变化？",
        "tags": "#Casabella #建筑杂志 #现代建筑 #城市规划 #GiuseppeTerragni #AlvarAalto #展馆设计 #建筑史",
        "cards": [
            {
                "image": "02-casa-del-fascio.jpg", "mode": "photo", "accent": "#df6333", "focal": (0.50, 0.58),
                "source": "Giuseppe Terragni｜Casa del Fascio di Como｜Casabella 107",
                "eyebrow": "观点 01｜公共建筑要被街道读懂",
                "title": "框架与空隙，让制度建筑获得开放的城市表情",
                "body": "规则柱网没有把立面做成单调网格；实墙、深凹开间与入口空隙形成不同透明度，让建筑同时表现秩序与公共进入。",
            },
            {
                "image": "03-addis-plan.jpg", "mode": "document", "accent": "#6f816f",
                "source": "Cesare Valle / Ignazio Guidi｜Piano regolatore di Addis Abeba｜Casabella 107",
                "eyebrow": "观点 02｜规划先建立公共骨架",
                "title": "交通轴线与功能分区，共同决定城市如何生长",
                "body": "规划以中心区、放射轴线和功能分区组织扩张。道路不是剩余空间，而是把行政、居住与公共设施连接起来的城市骨架。",
            },
            {
                "image": "04-finland-pavilion.jpg", "mode": "document", "accent": "#df6333",
                "source": "Alvar Aalto / Aarne Ervi / Viljo Revell｜芬兰馆竞赛方案｜Casabella 107",
                "eyebrow": "观点 03｜展馆可以像路径一样展开",
                "title": "轻构架与错动体量，让观看在行走中逐步发生",
                "body": "芬兰馆方案没有用对称大厅统摄一切，而以轻质构件、室外平台和错动单元形成连续路线，让国家展示变成可游走的空间。",
            },
            {
                "image": "05-japan-pavilion.jpg", "mode": "photo", "accent": "#6f816f", "focal": (0.54, 0.52),
                "source": "Junzo Sakakura｜Pavillon du Japon, Paris 1937｜Casabella 107",
                "eyebrow": "观点 04｜透明界面连接室内外",
                "title": "柱网、庭院与架空层，把展览变成连续风景",
                "body": "细柱和大面积开口让内部不再是封闭展厅；庭院、坡道与展台互相渗透，观众始终能感知下一段路径。",
            },
            {
                "image": "06-gooiland.jpg", "mode": "photo", "accent": "#df6333", "focal": (0.56, 0.52),
                "source": "Jan Duiker｜Grand Hotel Gooiland, Hilversum｜Casabella 107",
                "eyebrow": "观点 05｜复合建筑靠流线成立",
                "title": "入口、露台与公共大厅，把酒店接入城市生活",
                "body": "弧形转角、水平露台和通透底层共同回应车辆抵达与步行进入；建筑体量由不同活动的流线关系塑造。",
            },
            {
                "image": "07-brunelleschi-cutaway.jpg", "mode": "document", "accent": "#6f816f",
                "source": "Agnoldomenico Pica｜Fonti del Brunelleschi｜Casabella 107",
                "eyebrow": "观点 06｜结构逻辑可以跨越时代",
                "title": "双层壳体与肋骨，让巨大穹顶在施工中自我稳定",
                "body": "穹顶的力量不只来自外观比例，而来自内外壳、主肋和环向约束的协同；历史形式因此可以被作为构造系统重新理解。",
            },
        ],
    },
    {
        "slug": "casabella-108",
        "issue": "CASABELLA 108",
        "date": "DICEMBRE 1936 · ANNO IX",
        "date_cn": "1936年12月",
        "accent": "#9b3f72",
        "cover": "book-cover.jpg",
        "question": "住宅、剧场与展览\n如何通过界面和光线\n获得现代空间性？",
        "thesis_label": "界面 × 光线 × 使用",
        "thesis": "108期把现代性放进具体界面：住宅以开口和架空层组织生活，剧场以环绕视线塑造共同观看，展览建筑以透光表皮形成公共形象。",
        "summary": "108期说明，现代空间不取决于白色外观，而取决于界面如何分配光线、视线、进入方式与公共活动。",
        "concepts": ["开放界面", "光线层次", "公共观看"],
        "takeaways": [
            "住宅开口要同时处理采光、通风、私密与花园关系。",
            "剧场空间以视线、环绕层次和共同焦点组织观众。",
            "展览建筑的表皮既负责采光，也负责建立城市识别。",
        ],
        "publish_title": "Casabella108｜界面塑造空间",
        "publish_body": "Casabella 108 讨论住宅、剧场和展览建筑，却围绕同一个问题展开：界面如何改变人的使用方式。现代空间并不只靠白墙成立，开口、门廊与透光表皮同样决定光线、视线和公共活动。\n\nFarkas Molnár 的住宅用转角开口、露台和花园建立室内外联系；Molnár 与 József Fischer 的 O.T.I. 住宅把主体抬起，让底层获得通行和公共缓冲。都灵时尚宫则用巨大透光立面，把展览大厅变成城市尺度的发光界面。\n\n剧场提供另一种答案：Falcone 剧院以层层包厢环绕共同焦点，Corso Theater 把城市立面与公共娱乐叠合在一起。Balla Villa 的凹入门廊进一步说明，住宅的开放性不是把墙全部拆掉，而是精确控制从花园到室内的过渡。\n\n你认为最能改变空间体验的界面，是窗、门廊，还是整面透光表皮？",
        "tags": "#Casabella #建筑杂志 #住宅设计 #剧场建筑 #FarkasMolnar #现代主义 #空间设计 #建筑史",
        "cards": [
            {
                "image": "02-original-frontispiece.jpg", "mode": "document", "accent": "#9b3f72",
                "source": "Farkas Molnár｜Villa Dalnoki-Kovatz｜Casabella 108, frontespizio",
                "eyebrow": "观点 01｜住宅以界面连接花园",
                "title": "转角开口与水平露台，让室内生活向场地展开",
                "body": "Villa Dalnoki-Kovatz 把实墙、长窗和露台组合成不同开放程度；住宅不追求全透明，而是精确控制视线、遮蔽与花园联系。",
            },
            {
                "image": "03-oti-worker-housing.png", "mode": "photo", "accent": "#4f7b73", "focal": (0.52, 0.52),
                "source": "Farkas Molnár / József Fischer｜Casa dell’O.T.I.｜Casabella 108",
                "eyebrow": "观点 02｜架空层释放公共地面",
                "title": "把住宅主体抬起，底层就能容纳进入与交往",
                "body": "连续窗带统一居住单元，架空底层则把建筑入口、通行和室外活动从封闭首层中释放出来，集体住宅因此拥有共享边界。",
            },
            {
                "image": "04-palazzo-moda.jpg", "mode": "photo", "accent": "#9b3f72", "focal": (0.48, 0.52),
                "source": "Giuseppe Pagano｜Il Palazzo della Moda, Torino｜Casabella 108",
                "eyebrow": "观点 03｜表皮可以成为采光装置",
                "title": "巨大透光网格，把展览大厅变成城市灯箱",
                "body": "高大的网格立面过滤自然光，也在夜间形成清楚的公共形象；结构与表皮共同完成采光，而不是在封闭墙面上附加装饰。",
            },
            {
                "image": "05-teatro-falcone.jpg", "mode": "photo", "accent": "#4f7b73", "focal": (0.50, 0.46),
                "source": "Ugo Nebbia｜Il Teatro del Falcone｜Casabella 108",
                "eyebrow": "观点 04｜剧场由共同视线成立",
                "title": "环绕包厢把个人座位组织成集体观看",
                "body": "多层包厢沿椭圆空间环绕舞台，观众既看演出，也彼此看见；剧场公共性来自视线被组织成共同事件。",
            },
            {
                "image": "06-corso-theater.jpg", "mode": "photo", "accent": "#9b3f72", "focal": (0.56, 0.54),
                "source": "Pfleghard & Haefeli｜Corso-Theater, Zürich｜Casabella 108",
                "eyebrow": "观点 05｜公共娱乐进入街道界面",
                "title": "剧场立面同时承担入口、商业与城市识别",
                "body": "连续开口和首层公共入口把剧场活动显露到街道；建筑不再以封闭正立面隔绝城市，而成为夜间与日常交通的节点。",
            },
            {
                "image": "07-balla-villa.jpg", "mode": "photo", "accent": "#4f7b73", "focal": (0.48, 0.50),
                "source": "Farkas Molnár｜Villa Balla, Budapest｜Casabella 108",
                "eyebrow": "观点 06｜门廊是生活缓冲层",
                "title": "一个凹入角落，连接花园、入口与家庭活动",
                "body": "体量被切出受保护的门廊，室外用餐和日常停留因此拥有边界；现代住宅的开放性来自有层次的过渡。",
            },
        ],
    },
    {
        "slug": "casabella-109",
        "issue": "CASABELLA 109",
        "date": "GENNAIO 1937 · ANNO X",
        "date_cn": "1937年1月",
        "accent": "#329a84",
        "cover": "book-cover.jpg",
        "question": "现代空间除了体量，\n还能由什么构成？",
        "thesis_label": "透明界面 × 展陈网格 × 连续表面",
        "thesis": "109期把住宅、商店、展览与材料放在一起：空间不仅由墙体围合，也由玻璃、细杆网格、地面图案和多层表面共同生成。",
        "summary": "109期把现代空间从体量问题转向表面问题：透明度组织视线，网格组织物品，材料层组织触感与耐久性。",
        "concepts": ["透明度", "三维网格", "材料层次"],
        "takeaways": [
            "透明界面不是消失的墙，而是重新分配采光与私密。",
            "展陈网格同时组织商品、标识、视线和人的移动。",
            "地面与抹灰由基层、连接层和面层共同决定性能。",
        ],
        "publish_title": "Casabella109｜空间不只靠墙",
        "publish_body": "Casabella 109 把住宅、展陈和材料技术放进同一条线索：空间不只由体量构成，也由表面关系构成。透明度、网格和材料层，都能直接改变人的观看与使用。\n\nGropius 与 Maxwell Fry 的 Chelsea 住宅通过长窗、玻璃界面和退台，重新分配采光与城市私密。William Lescaze 的纽约住宅用玻璃砖形成半透明立面，让自然光进入，同时保持街道边界。\n\nPersico 与 Nizzoli 的展览和 Parker 商店把细杆、网格、标识和展台组合成三维框架，商品不再堆在墙边，而被放进人的视线和移动路径中。关于 linoleum 与 Jurasite 的文章进一步把注意力推向地面和墙面：连续表面依赖基层、连接层、面层与施工共同工作。\n\n你会先从透明度、展陈网格，还是材料层次重新设计一个室内空间？",
        "tags": "#Casabella #建筑杂志 #EdoardoPersico #WilliamLescaze #展陈设计 #材料设计 #现代主义 #室内设计",
        "cards": [
            {
                "image": "02-original-frontispiece.jpg", "mode": "document", "accent": "#329a84",
                "source": "Walter Gropius / Maxwell Fry｜Casa a Chelsea｜Casabella 109, frontespizio",
                "eyebrow": "观点 01｜透明界面重新分配私密",
                "title": "长窗与退台，让城市住宅同时获得光线和边界",
                "body": "Chelsea 住宅通过连续开口、露台与体量后退引入自然光，又保留面向街道的控制；透明度不是毫无遮蔽。",
            },
            {
                "image": "03-persico-salone.jpg", "mode": "document", "accent": "#555f70",
                "source": "Edoardo Persico / Marcello Nizzoli / Giancarlo Palanti｜Salone d’Onore｜Casabella 109",
                "eyebrow": "观点 02｜竖向节奏制造空间深度",
                "title": "重复构架与终点雕塑，把展厅变成行走序列",
                "body": "细长竖向构件反复切分透视，雕塑固定视线终点；空间感来自人在柱列间移动时不断变化的遮挡与显现。",
            },
            {
                "image": "04-lescaze-house.jpg", "mode": "photo", "accent": "#329a84", "focal": (0.49, 0.52),
                "source": "William Lescaze｜Lescaze House, New York｜Casabella 109",
                "eyebrow": "观点 03｜玻璃砖是一种厚界面",
                "title": "半透明立面引入光线，却不暴露全部室内生活",
                "body": "玻璃砖介于实墙与透明玻璃之间，既形成连续采光面，也模糊街道视线；现代住宅因此获得可调节的私密层次。",
            },
            {
                "image": "05-parker-shop.jpg", "mode": "document", "accent": "#555f70",
                "source": "Edoardo Persico / Marcello Nizzoli｜Negozio Parker, Milano｜Casabella 109",
                "eyebrow": "观点 04｜商店是三维信息系统",
                "title": "细杆、展台与标识，把商品放进人的视线轨迹",
                "body": "Parker 商店以轻框架建立前后层次，商品和文字悬置在不同深度；展示因此从墙面陈列变成可穿行的空间。",
            },
            {
                "image": "06-linoleum-stand.jpg", "mode": "photo", "accent": "#329a84", "focal": (0.52, 0.52),
                "source": "F. Marescotti｜Il linoleum｜Casabella 109",
                "eyebrow": "观点 05｜地面也能组织空间",
                "title": "连续铺装把展品、路径与视觉分区连接起来",
                "body": "Linoleum 不只是耐磨饰面；图案、接缝和色块可以提示行走方向，并把不同展示区域组织成连续整体。",
            },
            {
                "image": "07-stucco-test.jpg", "mode": "document", "accent": "#555f70",
                "source": "F. Marescotti｜L’intonaco Jurasite｜Casabella 109",
                "eyebrow": "观点 06｜抹灰是一套构造系统",
                "title": "基层、连接层与面层，共同决定墙面能否耐久",
                "body": "抹灰的开裂与脱落不能只归咎于表层材料；基层稳定、金属网连接、分层施工和养护共同决定连续表面的性能。",
            },
        ],
    },
]


def save_rgb(image: Image.Image, path: Path) -> None:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)


def render_pdf_page(pdf_path: Path, output_path: Path, page_index: int, zoom: float = 2.5) -> None:
    if output_path.exists():
        return
    with fitz.open(pdf_path) as document:
        page = document[page_index]
        pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        pixmap.save(output_path)


def crop_reference(source: Path, output: Path, box: tuple[int, int, int, int]) -> None:
    if output.exists():
        return
    image = Image.open(source).convert("RGB").crop(box)
    image = image.resize((image.width * 4, image.height * 4), Image.Resampling.LANCZOS)
    image = ImageEnhance.Sharpness(image).enhance(1.25)
    image.save(output, quality=96, subsampling=0)


def prepare_assets() -> None:
    render_pdf_page(ROOT / "assets/casabella-107/03-addis-plan.pdf", ROOT / "assets/casabella-107/03-addis-plan.jpg", 68, 2.8)
    render_pdf_page(ROOT / "assets/casabella-108/original.pdf", ROOT / "assets/casabella-108/02-original-frontispiece.jpg", 0, 3.2)
    render_pdf_page(ROOT / "assets/casabella-109/original.pdf", ROOT / "assets/casabella-109/02-original-frontispiece.jpg", 0, 3.2)
    crop_reference(ROOT / "tmp/pdfs/persico-render/053.jpg", ROOT / "assets/casabella-109/03-persico-salone.jpg", (112, 650, 425, 1150))
    crop_reference(ROOT / "tmp/pdfs/persico-render/055.jpg", ROOT / "assets/casabella-109/05-parker-shop.jpg", (112, 925, 425, 1395))
    render_pdf_page(ROOT / "assets/casabella-109/07-stucco-reference.pdf", ROOT / "assets/casabella-109/07-stucco-test.jpg", 9, 2.8)


def cover_107(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.text((76, 70), f"{cfg['issue']}  /  单期主线", font=font(FONT_BOLD, 23), fill=accent)
    draw.text((1168, 72), cfg["date"], font=font(FONT_SANS, 20), fill=MUTED, anchor="ra")
    draw.line((76, 112, 1168, 112), fill=rgba(INK, 65), width=2)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (74, 228, 604, 680), True)
    draw_fit(draw, (705, 232), cfg["question"], 455, 500, 50, INK, serif=True, spacing=12)
    draw.text((705, 780), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw.line((705, 830, 1168, 830), fill=accent, width=7)
    draw_fit(draw, (76, 1180), cfg["thesis"], 1085, 270, 38, BLUE, serif=True, spacing=13)
    page_mark(draw, 1, False)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def cover_108(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.text((76, 68), cfg["issue"], font=font(FONT_BOLD, 28), fill=INK)
    draw.text((1168, 70), cfg["date"], font=font(FONT_SANS, 20), fill=MUTED, anchor="ra")
    draw_fit(draw, (76, 156), cfg["question"], 1090, 300, 63, INK, serif=True, spacing=10)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (313, 495, 616, 662), True)
    draw.rectangle((0, 1228, W, 1544), fill=rgba(accent, 236))
    draw.text((76, 1270), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=LIGHT)
    draw_fit(draw, (76, 1322), cfg["thesis"], 1085, 165, 35, LIGHT, serif=True, spacing=10)
    page_mark(draw, 1, False)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def cover_109(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.text((76, 72), f"{cfg['issue']}  /  单期主线", font=font(FONT_BOLD, 23), fill=accent)
    draw.text((76, 128), cfg["date"], font=font(FONT_SANS, 20), fill=MUTED)
    draw_fit(draw, (76, 258), cfg["question"], 470, 420, 52, INK, serif=True, spacing=13)
    draw.text((76, 725), cfg["thesis_label"], font=font(FONT_BOLD, 21), fill=accent)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (585, 190, 590, 640), True)
    draw.rectangle((76, 1035, 1168, 1045), fill=accent)
    draw_fit(draw, (76, 1132), cfg["thesis"], 1080, 300, 40, BLUE, serif=True, spacing=14)
    page_mark(draw, 1, False)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def summary_107(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, False)
    accent = cfg["accent"]
    draw.text((74, 158), "三种尺度，一套空间秩序", font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (74, 225), cfg["summary"], 1080, 300, 53, INK, serif=True, spacing=17)
    colors = [accent, "#c5a765", "#71816f"]
    for idx, (label, item, color) in enumerate(zip(cfg["concepts"], cfg["takeaways"], colors), 1):
        x = 74 + (idx - 1) * 366
        draw.rectangle((x, 682, x + 330, 700), fill=color)
        draw.text((x, 744), f"0{idx}  {label}", font=font(FONT_BOLD, 27), fill=color)
        draw_fit(draw, (x, 812), item, 320, 360, 31, INK, serif=True, spacing=12)
    draw.line((74, 1378, 1168, 1378), fill=rgba(INK, 60), width=2)
    draw.text((74, 1425), "城市规划  →  公共建筑  →  临时展馆", font=font(FONT_BOLD, 26), fill=BLUE)
    page_mark(draw, 8, False)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def summary_108(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, False)
    accent = cfg["accent"]
    draw.text((74, 160), "界面决定空间如何被使用", font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (74, 226), cfg["summary"], 1080, 300, 52, INK, serif=True, spacing=17)
    draw.line((224, 700, 224, 1408), fill=accent, width=8)
    for idx, (label, item) in enumerate(zip(cfg["concepts"], cfg["takeaways"]), 1):
        y = 710 + (idx - 1) * 230
        draw.ellipse((184, y, 264, y + 80), fill=accent)
        draw.text((224, y + 40), str(idx), font=font(FONT_BOLD, 28), fill=LIGHT, anchor="mm")
        draw.text((304, y), label, font=font(FONT_BOLD, 29), fill=accent)
        draw_fit(draw, (304, y + 58), item, 820, 130, 30, INK, serif=True, spacing=9)
    draw.text((74, 1485), "住宅 / 剧场 / 展览：界面同时处理光线、视线与进入", font=font(FONT_SANS, 23), fill=MUTED)
    page_mark(draw, 8, False)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def summary_109(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(BLUE))
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, True)
    accent = cfg["accent"]
    draw.text((74, 158), "空间由多层表面共同生成", font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (74, 228), cfg["summary"], 1080, 300, 52, LIGHT, serif=True, spacing=17)
    colors = ["#329a84", "#d8b35d", "#d9d7cf"]
    for idx, (label, item, color) in enumerate(zip(cfg["concepts"], cfg["takeaways"], colors), 1):
        y = 690 + (idx - 1) * 235
        draw.rectangle((74, y, 1168, y + 190), outline=rgba(color, 220), width=3)
        draw.rectangle((74, y, 290, y + 190), fill=rgba(color, 238))
        draw.text((112, y + 42), f"LAYER {idx}", font=font(FONT_SANS, 20), fill=INK)
        draw_fit(draw, (112, y + 84), label, 155, 70, 30, INK, bold=True, spacing=6)
        draw_fit(draw, (334, y + 42), item, 790, 120, 31, LIGHT, serif=True, spacing=10)
    draw.text((74, 1478), "透明界面  /  展陈网格  /  材料构造", font=font(FONT_BOLD, 24), fill=accent)
    page_mark(draw, 8, True)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def make_cover(cfg: dict, src: Path, out: Path) -> Path:
    return {"casabella-107": cover_107, "casabella-108": cover_108, "casabella-109": cover_109}[cfg["slug"]](cfg, src, out)


def make_summary(cfg: dict, out: Path) -> Path:
    return {"casabella-107": summary_107, "casabella-108": summary_108, "casabella-109": summary_109}[cfg["slug"]](cfg, out)


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
            *[f"{idx:02d} {card['source'].split('｜')[0]}：{card['title']}" for idx, card in enumerate(cfg["cards"], 2)],
            f"08 总结：{'—'.join(cfg['concepts'])}",
        ],
    }


def source_records(slug: str) -> str:
    common = "https://casabellaweb.eu/the-magazine/yearannata-1936-ix/"
    records = {
        "casabella-107": f"""# Casabella 107 图片来源

- `book-cover.jpg`｜Casabella 107 官方历史封面｜Casabella 官方档案｜{common}｜版权归原权利人；等比例放大，未改字。
- `02-casa-del-fascio.jpg`｜Giuseppe Terragni，Casa del Fascio di Como｜Wikimedia Commons，Casa del Fascio 分类页｜https://commons.wikimedia.org/wiki/Category:Casa_del_Fascio_(Como)｜许可以原文件页为准；裁切、缩放。
- `03-addis-plan.jpg`｜Cesare Valle / Ignazio Guidi，亚的斯亚贝巴总体规划图组｜研究文献 PDF 第69页｜本地 `03-addis-plan.pdf`｜原下载页未保留，许可待复核；渲染、缩放。
- `04-finland-pavilion.jpg`｜Alvar Aalto 等，巴黎世博芬兰馆相关档案图｜Alvar Aalto Foundation 项目档案｜https://www.alvaraalto.fi/en/architecture/｜版权/许可待复核；裁切、缩放。
- `05-japan-pavilion.jpg`｜Junzo Sakakura，巴黎世博日本馆｜Wikimedia Commons，坂仓准三相关档案｜https://commons.wikimedia.org/wiki/Category:Junzo_Sakakura｜许可以原文件页为准；裁切、缩放。
- `06-gooiland.jpg`｜Jan Duiker，Grand Hotel Gooiland 历史照片｜Het Nieuwe Instituut / 公共建筑档案｜https://collectie.hetnieuweinstituut.nl/｜版权待复核；裁切、缩放。
- `07-brunelleschi-cutaway.jpg`｜Santa Maria del Fiore 穹顶构造插图｜Wikimedia Commons，Brunelleschi dome 分类页｜https://commons.wikimedia.org/wiki/Category:Dome_of_Santa_Maria_del_Fiore｜许可以原文件页为准；裁切、缩放。

本组用于建筑杂志内容整理与教育性发布；商业投放前请逐张回到原文件页复核许可。
""",
        "casabella-108": f"""# Casabella 108 图片来源

- `book-cover.jpg`｜Casabella 108 官方历史封面｜Casabella 官方档案｜{common}｜版权归原权利人；等比例放大，未改字。
- `02-original-frontispiece.jpg`｜Casabella 108 原刊 frontespizio，Villa Dalnoki-Kovatz｜Trento大学图书馆数字馆藏｜https://webapps.unitn.it/Biblioteca/it/Web/EngibankFile/1936%20Casabella%20%5Bperiodico%5D%20108.pdf｜原刊扫描渲染、缩放。
- `03-oti-worker-housing.png`｜Farkas Molnár / József Fischer，Casa dell’O.T.I.｜Wikimedia Commons / 现代匈牙利建筑公共档案｜https://commons.wikimedia.org/wiki/Category:Farkas_Moln%C3%A1r｜许可以原文件页为准；裁切、缩放。
- `04-palazzo-moda.jpg`｜Il Palazzo della Moda, Torino 历史照片｜都灵建筑公共档案｜https://www.museotorino.it/｜版权待复核；裁切、缩放。
- `05-teatro-falcone.jpg`｜Teatro del Falcone 历史室内图｜意大利剧场公共档案｜https://www.culturaitalia.it/｜版权待复核；裁切、缩放。
- `06-corso-theater.jpg`｜Pfleghard & Haefeli，Corso-Theater, Zürich｜Wikimedia Commons / 苏黎世公共档案｜https://commons.wikimedia.org/wiki/Category:Buildings_in_Z%C3%BCrich｜许可以原文件页为准；裁切、缩放。
- `07-balla-villa.jpg`｜Farkas Molnár，Villa Balla, Budapest｜现代匈牙利建筑公共档案｜https://commons.wikimedia.org/wiki/Category:Farkas_Moln%C3%A1r｜许可以原文件页为准；裁切、缩放。

本组优先使用108期原刊页及目录所列项目图像；商业投放前请逐张复核许可。
""",
        "casabella-109": f"""# Casabella 109 图片来源

- `book-cover.jpg`｜Casabella 109 官方历史封面｜Casabella 官方档案｜{common}｜版权归原权利人；等比例放大，未改字。
- `02-original-frontispiece.jpg`｜Casabella 109 原刊 frontespizio，Gropius / Maxwell Fry Chelsea住宅｜Trento大学图书馆数字馆藏｜https://webapps.unitn.it/Biblioteca/it/Web/EngibankFile/1937%20Casabella%20%5Bperiodico%5D%20109.pdf｜原刊扫描渲染、缩放。
- `03-persico-salone.jpg`｜Persico / Nizzoli / Palanti / Fontana，Salone d’Onore｜FAMagazine 54/2020，图20｜https://doi.org/10.12838/fam/issn2039-0491/n54-2020/715｜学术论文图像裁切、缩放；版权归原权利人。
- `04-lescaze-house.jpg`｜William Lescaze，Lescaze House, New York｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/Category:William_Lescaze｜许可以原文件页为准；裁切、缩放。
- `05-parker-shop.jpg`｜Persico / Nizzoli，Negozio Parker, Milano｜FAMagazine 54/2020，图22—24｜https://doi.org/10.12838/fam/issn2039-0491/n54-2020/715｜学术论文图像裁切、缩放；版权归原权利人。
- `06-linoleum-stand.jpg`｜Linoleum 展陈空间历史照片｜Casabella 109“Il linoleum”相关档案｜https://casabellaweb.eu/｜原下载页未保留，版权待复核；裁切、缩放。
- `07-stucco-test.jpg`｜Stucco test structure，1915｜U.S. Bureau of Standards Circular No.311｜https://archive.org/details/stuccoinvestigat311unit｜公有领域；PDF第10页渲染、缩放。

原刊108/109扫描文件的馆藏链接沿用下载地址；商业投放前请再次核验平台与所在地规则。
""",
    }
    return records[slug]


def write_text_files(cfg: dict, out: Path) -> None:
    publish = f"""{cfg['publish_title']}

{cfg['publish_body']}

{cfg['tags']}
"""
    (out / "发布文案.md").write_text(publish, encoding="utf-8")
    (out / "图片来源.md").write_text(source_records(cfg["slug"]), encoding="utf-8")
    post_dir = ROOT / "posts" / cfg["slug"]
    post_dir.mkdir(parents=True, exist_ok=True)
    (post_dir / "post.json").write_text(json.dumps(post_manifest(cfg), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_issue(cfg: dict) -> None:
    src = ROOT / "assets" / cfg["slug"]
    out = ROOT / "output" / cfg["slug"]
    out.mkdir(parents=True, exist_ok=True)
    paths = [make_cover(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(make_summary(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards, preview and publishing files in {out}")


if __name__ == "__main__":
    prepare_assets()
    for issue in ISSUES:
        render_issue(issue)
