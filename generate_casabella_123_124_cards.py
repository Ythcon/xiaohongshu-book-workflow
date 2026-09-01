from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    BLUE,
    FONT_BOLD,
    FONT_SANS,
    H,
    INK,
    LIGHT,
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
        "slug": "casabella-123",
        "issue": "CASABELLA-COSTRUZIONI 123",
        "date": "MARZO 1938 | ANNO XI",
        "date_cn": "1938年3月",
        "cover": "book-cover.jpg",
        "accent": "#bf4a36",
        "question": "纪念性不是把建筑做得更大或贴上更多符号；它来自结构、尺度与公共使用能否被一起读懂。",
        "thesis": "123期把纪念性、混凝土构件和玻璃采光放到同一张桌子上。它提醒我们：先让承重、开口、路径和人的尺度建立秩序，再审视这套秩序究竟服务谁。",
        "summary": "当建筑想显得“重要”时，最容易牺牲的是日常使用。123期留下的可迁移方法，是把纪念性拆回三个可检查的问题：结构是否解释了空间尺度，光线是否改善了真实体验，入口与公共层是否允许不同的人平等进入。",
        "concepts": ["结构先于姿态", "光线也是材料", "公共性必须可达"],
        "takeaways": [
            "先用跨距、柱距、开口和净高组织空间；不要把体量、台阶或装饰当成“重要性”的替代品。",
            "玻璃不只是透明边界。朝向、反射、眩光、散射和框架密度，会共同决定一个房间是否舒适可用。",
            "面对具有权力象征的公共建筑，要检查谁能进入、谁能停留、谁被迫只在远处观看。",
        ],
        "publish_title": "123期｜纪念性不靠装饰",
        "publish_body": "Casabella-Costruzioni 123讨论“纪念性”时，并没有把它只当成外形问题。真正值得带走的是一个更具体的判断：建筑的重量感应来自可读的受力、清晰的尺度和可使用的公共层，而不是把符号、台阶与巨大立面不断叠加。\n\n这一期同时把混凝土单元和 Termolux 玻璃的光线问题纳入讨论。构件的重复应当服务跨距、开口和施工；玻璃则不只是“透明”，它会反射、偏转、扩散，也会制造眩光。材料一旦进入空间，就必须同时接受结构、光环境和身体体验的检验。\n\n放在今天阅读，还要补上一层批判：任何借由“纪念性”塑造权力的建筑，都应追问它让谁进入、让谁停留、又让谁被排除。",
        "tags": "#Casabella #建筑杂志 #建筑设计 #空间设计 #建筑评论 #混凝土 #玻璃设计 #建筑历史",
        "cards": [
            {
                "image": "02-casa-fascio-como.jpg", "mode": "photo", "accent": "#bf4a36", "focal": (0.51, 0.48),
                "source": "Giuseppe Pagano｜Del monumentale nell’architettura｜Casabella-Costruzioni 123",
                "eyebrow": "观点 01｜先把纪念性从符号里拿出来",
                "title": "纪念性不靠堆砌装饰；让结构网格、开口尺度和公共入口共同说明建筑为何重要",
                "body": "规整的立面可以建立秩序，却不会自动产生公共性。面对这类带有法西斯政治语境的建筑，今天更应把它当作警示来读：形式越显得庄严，越要检查入口、首层和广场是否真的允许不同的人平等使用。",
            },
            {
                "image": "03-casa-fascio-interior.jpg", "mode": "photo", "accent": "#335f79", "focal": (0.50, 0.50),
                "source": "Giuseppe Pagano｜Del monumentale nell’architettura｜Casabella-Costruzioni 123",
                "eyebrow": "观点 02｜让内部秩序回应外部网格",
                "title": "外立面的网格若不能延续到采光、楼梯和视线，纪念性就只剩下一张正面照片",
                "body": "一个强烈的外壳，应该在室内继续解释路径、层高和停留位置。把中庭、楼梯、栏杆与自然光组织成连续关系，人才会在行走中理解建筑的尺度，而不是只在远处接受它的姿态。",
            },
            {
                "image": "04-sesto-calende-siteplan.jpg", "mode": "document", "accent": "#728056",
                "source": "Augusto Legnani｜Casa del Fascio di Sesto Calende｜Casabella-Costruzioni 123",
                "eyebrow": "观点 03｜先把建筑放回街道与入口",
                "title": "总平面先说明入口、道路和体量如何相遇；脱离城市位置的“纪念性”只是一张立面图",
                "body": "公共建筑的第一条尺度来自到达，而不是外形。先看人从哪里进、车辆如何避开行人、广场是否能穿行，再决定体量应该退让、转向还是形成门廊。总平面越清楚，权力姿态越难掩盖真实使用。",
            },
            {
                "image": "06-casa-fascio-archive.jpg", "mode": "photo", "accent": "#bf4a36", "focal": (0.52, 0.48),
                "source": "A. M. Mazzucchelli｜Struttura a elementi di cemento｜Casabella-Costruzioni 123",
                "eyebrow": "观点 04｜构件先决定空间单位",
                "title": "把柱距、跨距和开口做成可重复的空间单位，立面才不会只是覆盖在结构外的一层图案",
                "body": "混凝土构件的价值不在于“看起来现代”，而在于把承重、围护和分隔组织成可施工的规则。先确定哪些地方需要大跨、哪些地方需要密柱、哪些地方需要连续开口，再让立面从这些差异中长出来。",
            },
            {
                "image": "05-como-union.jpg", "mode": "photo", "accent": "#335f79", "focal": (0.50, 0.48),
                "source": "Franco Marescotti｜Riflessione e deviazione dei raggi nel Termolux｜Casabella-Costruzioni 123",
                "eyebrow": "观点 05｜玻璃会改变光线的方向",
                "title": "玻璃不是透明的缺席；反射、偏转与眩光必须和朝向、框架和人的视线一起被设计",
                "body": "相同面积的窗，可能带来完全不同的房间体验。把玻璃性能、遮阳、窗框分格和工作面的朝向一起推敲，才能让自然光真正进入使用，而不是只换来一张明亮的建筑照片。",
            },
            {
                "image": "07-sesto-calende-sections.jpg", "mode": "document", "accent": "#728056",
                "source": "Augusto Legnani｜Casa del Fascio di Sesto Calende｜Casabella-Costruzioni 123",
                "eyebrow": "观点 06｜剖面要让集会与日常分层",
                "title": "把礼堂的高度、入口门厅和日常办公画进同一条剖面，才能判断体量是否真的服务使用",
                "body": "剖面会让使用关系无处躲藏：礼堂是否独占首层，后勤和日常办公如何到达，结构高度是否压迫周边尺度。对于任何公共项目，这些问题都比“是否庄严”更接近建筑的真实价值。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella-Costruzioni 123 原刊封面，1938年3月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/123-nz.jpg",
            "`02-casa-fascio-como.jpg`｜Giuseppe Terragni，Casa del Fascio，Como，1932–1936，历史照片｜Architecture History｜https://architecture-history.org/schools/PIC/1932-1936%2C%20Casa%20del%20Fascio%2C%20Como%2C%20ITALY%20%2C%20GIUSEPPE%20TERRAGNI.jpg",
            "`03-casa-fascio-interior.jpg`｜Günther Förg，Casa del Fascio, Como 内部摄影，1995/96｜Janisch Fine Art｜https://janischfineart.com/wp-content/uploads/2017/05/P50103052.jpg",
            "`04-sesto-calende-siteplan.jpg`、`07-sesto-calende-sections.jpg`｜Augusto Legnani，Casa del Fascio di Sesto Calende，1937，总平面、立面与礼堂剖面细节；该项目在 Casabella-Costruzioni 123 的相关专题中出现｜意大利文化部《Le Case del Fascio in Italia e nelle terre d’Oltremare》｜https://dgagaeta.cultura.gov.it/public/uploads/documents/FuoriCollana/6486a31984e3c.pdf",
            "`05-como-union.jpg`｜Sede dell’unione fascista dei lavoratori dell’industria, Como，约1938–1949，历史照片；作为 Termolux 文章的同期玻璃/开口语境配图，并非原刊插图｜Lombardia Beni Culturali｜https://www.lombardiabeniculturali.it/assets/immagini/liv2/AF310RLSUP/SC/F/CO240/0000/F_SUP-CO240-0000413_IMG-0000222427.jpg",
            "`06-casa-fascio-archive.jpg`｜Giuseppe Terragni，Casa del Fascio, Como，历史照片｜Pinterest 原始图像页｜https://i.pinimg.com/originals/d5/55/2b/d5552befb7f1a1723841c95e287b33a5.jpg",
            "文章目录｜Giuseppe Pagano，《Del monumentale nell’architettura》，Casabella 123，1938年3月，pp.2–3｜TU Wien 研究论文｜https://repositum.tuwien.at/retrieve/27892",
            "文章目录｜Anna Maria Mazzucchelli，《Studi per l’applicazione razionale di una struttura a elementi di cemento》，Casabella-Costruzioni 123，1938年3月，p.20｜Università di Bologna 研究论文｜https://amsdottorato.unibo.it/id/eprint/1440/1/Cagneschi_Claudia_tesi.pdf",
            "文章目录｜Franco Marescotti，《Osservazioni sulla riflessione e deviazione dei raggi luminosi attraverso il complesso vitreo Termolux》，Casabella-Costruzioni 123，1938年3月，pp.41–42｜Politecnico di Torino WebThesis｜https://webthesis.biblio.polito.it/5916/",
        ],
    },
    {
        "slug": "casabella-124",
        "issue": "CASABELLA-COSTRUZIONI 124",
        "date": "APRILE 1938 | ANNO XI",
        "date_cn": "1938年4月",
        "cover": "book-cover.jpg",
        "accent": "#3e81a8",
        "question": "结构不是把空间撑起来的最后一步；重复构件、受力路径和施工顺序从一开始就决定了建筑形状。",
        "thesis": "124期以 Pier Luigi Nervi 的混凝土机库为核心：大跨度并非来自一个惊人的造型，而是来自清晰的荷载路径、可重复的几何单元、足够大的入口净空，以及用模型不断校验的施工判断。",
        "summary": "Nervi 的机库把结构变成可读的空间语言。它最有用的启发不是复制网格外观，而是把设计顺序倒过来：先画清净跨与荷载，再组织重复构件和拼装节奏，最后让光、行走和视线从受力逻辑里自然出现。",
        "concepts": ["先留出净跨", "再组织荷载路径", "最后校验施工"],
        "takeaways": [
            "先确定需要真正留空的区域：飞机、设备、人群或舞台都需要连续净高和无柱平面，结构再围绕它展开。",
            "重复不是装饰。每一次重复都要说明构件如何受力、如何相接、如何把集中荷载传到基础。",
            "当结构规则复杂到无法只靠计算直觉把握时，用模型和节点试验提前暴露变形、连接与施工风险。",
        ],
        "publish_title": "124期｜结构如何长成空间",
        "publish_body": "Casabella-Costruzioni 124的核心案例，是 Pier Luigi Nervi 的钢筋混凝土机库。它把一个最难的问题讲得很直接：大空间不是先画出一个漂亮屋顶，再去找结构支撑；恰恰相反，净跨、荷载路径、拱脚位置、构件重复与施工顺序，会共同生成屋顶的形状。\n\nOrvieto 机库最迷人的地方，是结构逻辑始终可见。拱、格、斜撑和边部支座不是被藏进吊顶后的技术；它们同时控制了入口净空、光线节奏、室内比例与建造方法。\n\n这也是今天做大跨度空间时最实用的顺序：先留出真正需要无柱的区域，再画清力往哪里走，接着把重复构件做成施工节奏，最后用模型和节点测试替代“看起来没问题”的判断。",
        "tags": "#Casabella #PierLuigiNervi #建筑结构 #混凝土建筑 #大跨度空间 #建筑设计 #工程美学 #建筑历史",
        "cards": [
            {
                "image": "02-nervi-hangar-interior.jpg", "mode": "photo", "accent": "#3e81a8", "focal": (0.52, 0.48),
                "source": "P. L. Nervi｜Un’aviorimessa in cemento armato｜Casabella-Costruzioni 124",
                "eyebrow": "观点 01｜先为真正的使用留出净跨",
                "title": "机库的第一张图不该是屋顶造型，而该是飞机需要怎样的净高、净宽和连续入口",
                "body": "大跨度空间的设计从“不能被柱子打断的区域”开始。先锁定飞机进出的开口、停放的净高和连续的操作带，再决定拱脚落在哪里、哪些力可以送到边部，形式才会有明确的任务。",
            },
            {
                "image": "03-nervi-plan.jpg", "mode": "document", "accent": "#bf7045",
                "source": "P. L. Nervi｜Un’aviorimessa in cemento armato｜Casabella-Costruzioni 124",
                "eyebrow": "观点 02｜平面先画清力如何落地",
                "title": "基础、拱跨和入口必须在同一张平面里对齐；空间越大，越不能把结构留到最后补画",
                "body": "这张图把基础位置、构件网格和横剖面放在一起。它提示我们：柱网不是独立的表格，必须同时回答谁进出、荷载怎么传、边部如何抵抗水平推力，以及维修和排水是否还有位置。",
            },
            {
                "image": "04-nervi-axonometric.jpg", "mode": "document", "accent": "#728056",
                "source": "P. L. Nervi｜Un’aviorimessa in cemento armato｜Casabella-Costruzioni 124",
                "eyebrow": "观点 03｜重复构件要形成连续受力",
                "title": "把一根梁做成一套可重复的受力规则：构件越多，越需要让连接、方向和节奏一眼可读",
                "body": "重复并不等于复制。真正有效的重复会建立构件方向、节点层级与安装顺序，让每一根梁都参与整体受力。人在室内看到的节奏，正是力被传递、被分散、再被送入基础的痕迹。",
            },
            {
                "image": "05-nervi-interior-archive.jpg", "mode": "photo", "accent": "#3e81a8", "focal": (0.50, 0.44),
                "source": "P. L. Nervi｜Un’aviorimessa in cemento armato｜Casabella-Costruzioni 124",
                "eyebrow": "观点 04｜让承重同时成为空间尺度",
                "title": "当拱、格和边部支座直接可见，结构不只撑住屋顶，也给出行走、停放与仰看的尺度",
                "body": "把结构完全藏起来，空间会失去方向感。机库的网格顶面将大尺度拆成可被身体感知的段落；边部构件既承担力，也建立侧向的节奏和采光边界，让巨大空间不至于变成无差别的空壳。",
            },
            {
                "image": "06-nervi-models.jpg", "mode": "document", "accent": "#bf7045",
                "source": "P. L. Nervi｜Un’aviorimessa in cemento armato｜Casabella-Costruzioni 124",
                "eyebrow": "观点 05｜模型是结构实验，不是展示品",
                "title": "先把构件、节点和支座放进模型，提前看见变形和连接问题，再把这套规则放大到真实跨度",
                "body": "复杂结构不能只凭“看起来合理”定案。模型能让设计团队同时检查局部节点和整体受力：哪里需要加密构件，哪里可以减轻重量，哪些连接会在施工时难以实现，都应该在图纸之前被看见。",
            },
            {
                "image": "07-nervi-brief.jpg", "mode": "document", "accent": "#728056",
                "source": "P. L. Nervi｜Un’aviorimessa in cemento armato｜Casabella-Costruzioni 124",
                "eyebrow": "观点 06｜用剖面让净跨与支座协商",
                "title": "入口要留出多高，拱脚就要承受多大推力；剖面先把空间愿望翻译成可传递的力",
                "body": "剖面不是平面的附图。它直接决定入口净高、拱的曲率、边部支座与屋顶网格如何配合。先用剖面校准空间和受力，再回到平面调整基础和构件间距，方案才不会在后期互相打架。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella-Costruzioni 124 原刊封面，1938年4月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/124-nz.jpg",
            "`02-nervi-hangar-interior.jpg`｜Pier Luigi Nervi，Orvieto 机库内部，1935｜Omrania｜https://omrania.com/wp-content/uploads/Nervi_Hangar-Orvieto-1935-1200x628-cover-768x402.jpg",
            "`03-nervi-plan.jpg`｜Pier Luigi Nervi，Orvieto 机库基础与钢筋混凝土结构平面｜Archimagazine｜https://www.archimagazine.com/amolecolare4_max.jpg",
            "`04-nervi-axonometric.jpg`｜Pier Luigi Nervi，Orvieto 机库轴测图｜Archilovers｜https://cdn.archilovers.com/projects/b_730_aba0e198-f3cc-4e84-91b4-1af5d2b44dee.jpg",
            "`05-nervi-interior-archive.jpg`｜Pier Luigi Nervi，Orvieto 机库内部历史图｜Pinterest 原始图像页｜https://i.pinimg.com/originals/3d/18/5e/3d185ebe2b8bce0a49ffaed508a989b3.jpg",
            "`06-nervi-models.jpg`｜Pier Luigi Nervi，预制机库平面、施工现场与 1:37.5 赛璐珞模型｜USI ARC《Capolavori in miniatura: Pier Luigi Nervi e la modellazione strutturale》，pp.42–43｜https://www.share.usi.ch/arc/neri_capolavori.pdf",
            "`07-nervi-brief.jpg`｜Pier Luigi Nervi，Aviorimesse in cemento armato，早期剖面与结构演变图｜USI ARC《Capolavori in miniatura: Pier Luigi Nervi e la modellazione strutturale》，pp.16–17｜https://www.share.usi.ch/arc/neri_capolavori.pdf",
            "文章目录｜Pier Luigi Nervi，《Un’aviorimessa in cemento armato》，Casabella-Costruzioni 124，1938年4月，pp.4–9｜USI ARC《Capolavori in miniatura》｜https://www.share.usi.ch/arc/neri_capolavori.pdf",
            "同期材料文章｜A. Rovelli，《Il Faesite extraduro nelle case d’oggi》，Casabella-Costruzioni 124，1938年4月，pp.36–39；Franco Marescotti，《L’isolamento acustico col vetro Termolux》，pp.34–35｜Politecnico di Torino WebThesis｜https://webthesis.biblio.polito.it/5916/",
        ],
    },
]


def save_rgb(image: Image.Image, path: Path) -> Path:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def source_line(draw: ImageDraw.ImageDraw, text: str, y: int, color: str = INK) -> None:
    draw.line((68, y - 18, 1174, y - 18), fill=rgba(color, 85), width=2)
    draw_fit(draw, (68, y), text, 1088, 48, 21, rgba(color, 180), spacing=5)


def make_cover_123(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#eee9dc"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 30), fill="#191b1c")
    draw.rectangle((0, 30, 458, H), fill="#1d2022")
    draw.text((68, 70), cfg["issue"], font=font(FONT_BOLD, 25), fill="#eee9dc")
    draw.text((68, 110), cfg["date"], font=font(FONT_SANS, 18), fill=rgba("#eee9dc", 185))
    for y in [230, 290, 350, 410, 470, 530]:
        draw.ellipse((68, y, 92, y + 24), fill=accent)
        draw.line((116, y + 12, 370, y + 12), fill=rgba("#eee9dc", 105), width=2)
    draw_fit(draw, (68, 680), cfg["question"], 325, 550, 48, "#eee9dc", serif=True, spacing=17)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.24)
    mount(canvas, cover, (530, 118, 610, 790), True)
    draw.rectangle((530, 970, 1140, 988), fill=accent)
    draw_fit(draw, (530, 1040), cfg["thesis"], 610, 340, 35, INK, serif=True, spacing=13)
    source_line(draw, "Casabella-Costruzioni｜第123期原刊封面｜1938年3月", 1510)
    page_mark(draw, 1, False)
    return save_rgb(canvas, out / "01.jpg")


def make_cover_124(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#15354c"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 28), fill=accent)
    draw.text((68, 68), cfg["issue"], font=font(FONT_BOLD, 25), fill="#f1ede3")
    draw.text((1170, 70), cfg["date"], font=font(FONT_SANS, 18), fill=rgba("#f1ede3", 185), anchor="ra")
    for offset in range(0, 7):
        x = 76 + offset * 158
        draw.arc((x, 180, x + 270, 760), 195, 345, fill=rgba(accent, 120), width=4)
    draw_fit(draw, (92, 204), cfg["question"], 470, 440, 50, "#f1ede3", serif=True, spacing=17)
    draw.line((92, 770, 550, 770), fill=accent, width=6)
    draw_fit(draw, (92, 830), cfg["thesis"], 470, 445, 34, rgba("#f1ede3", 230), serif=True, spacing=13)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.24)
    mount(canvas, cover, (650, 176, 480, 930), True)
    draw.rectangle((650, 1174, 1130, 1194), fill=accent)
    source_line(draw, "Casabella-Costruzioni｜第124期原刊封面｜1938年4月", 1510, "#f1ede3")
    page_mark(draw, 1, True)
    return save_rgb(canvas, out / "01.jpg")


def make_summary_123(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#eee9dc"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    header(draw, cfg, 8, False)
    draw.rectangle((0, 132, W, 475), fill="#1d2022")
    draw.text((68, 170), "重要性必须被使用证明", font=font(FONT_BOLD, 27), fill=accent)
    draw_fit(draw, (68, 236), cfg["summary"], 1060, 190, 47, "#f1ede3", serif=True, spacing=16)
    colors = ["#bf4a36", "#335f79", "#728056"]
    ys = [592, 872, 1152]
    for idx, (y, label, body, color) in enumerate(zip(ys, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.text((68, y), f"0{idx}", font=font(FONT_BOLD, 58), fill=color)
        draw.text((212, y + 13), label, font=font(FONT_BOLD, 34), fill=INK)
        draw.line((212, y + 68, 1142, y + 68), fill=rgba(INK, 75), width=2)
        draw_fit(draw, (212, y + 94), body, 900, 116, 31, rgba(INK, 220), serif=True, spacing=10)
    source_line(draw, "Casabella-Costruzioni｜第123期主要文章与案例｜1938年3月", 1508)
    page_mark(draw, 8, False)
    return save_rgb(canvas, out / "08.jpg")


def make_summary_124(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#dce8eb"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    header(draw, cfg, 8, False)
    draw.rectangle((0, 132, W, 152), fill=accent)
    for x in range(126, 1170, 145):
        draw.line((x, 210, x + 72, 535), fill=rgba(accent, 115), width=5)
        draw.line((x + 72, 535, x + 144, 210), fill=rgba(accent, 115), width=5)
    draw.text((68, 195), "让结构逻辑长成空间", font=font(FONT_BOLD, 27), fill="#15354c")
    draw_fit(draw, (68, 262), cfg["summary"], 1060, 235, 47, INK, serif=True, spacing=16)
    colors = ["#15354c", "#3e81a8", "#bf7045"]
    xs = [68, 444, 820]
    for idx, (x, label, body, color) in enumerate(zip(xs, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.rounded_rectangle((x, 700, x + 310, 1380), 10, fill=color)
        draw.text((x + 34, 740), f"0{idx}", font=font(FONT_BOLD, 42), fill=rgba("#f1ede3", 190))
        draw_fit(draw, (x + 34, 826), label, 238, 105, 33, "#f1ede3", serif=True, spacing=9)
        draw.line((x + 34, 960, x + 274, 960), fill=rgba("#f1ede3", 135), width=2)
        draw_fit(draw, (x + 34, 1002), body, 238, 292, 30, "#f1ede3", serif=True, spacing=11)
    source_line(draw, "Casabella-Costruzioni｜第124期主要文章与案例｜1938年4月", 1508)
    page_mark(draw, 8, False)
    return save_rgb(canvas, out / "08.jpg")


def post_manifest(cfg: dict) -> dict:
    return {
        "type": "magazine",
        "slug": cfg["slug"],
        "issue": cfg["issue"].title(),
        "date": cfg["date_cn"],
        "core_question": cfg["question"],
        "core_thesis": cfg["thesis"],
        "pages": [
            f"01 单期主线：{cfg['question']}",
            *[f"{n:02d} {card['source']}：{card['title']}" for n, card in enumerate(cfg["cards"], 2)],
            f"08 总结：{'；'.join(cfg['concepts'])}",
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
    cover_maker = make_cover_123 if cfg["slug"] == "casabella-123" else make_cover_124
    summary_maker = make_summary_123 if cfg["slug"] == "casabella-123" else make_summary_124
    paths = [cover_maker(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(summary_maker(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards, preview and publishing files in {out}")


if __name__ == "__main__":
    for issue in ISSUES:
        render_issue(issue)
