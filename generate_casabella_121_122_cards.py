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
        "slug": "casabella-121",
        "issue": "CASABELLA-COSTRUZIONI 121",
        "date": "GENNAIO 1938 | ANNO XI",
        "date_cn": "1938年1月",
        "cover": "book-cover.jpg",
        "accent": "#c55a43",
        "question": "展览不是陈列商品，\n而是把材料、文字与身体编成空间",
        "thesis_label": "材料 | 标识 | 动线 | 光",
        "thesis": "121期围绕罗马纺织展展开：纤维被拉成悬挂界面，字标承担导向，雕塑与灯光建立远距离识别，行走路线决定人如何接近材料。展览的力量不在装饰多少，而在信息、触感和移动能否被组织成一个连续场景。",
        "summary": "材料展陈最容易落入样品堆放。121期留下的图像提醒我们：先让材料决定边界、悬挂和透光方式；再让文字说明进入空间骨架；最后用可走、可停、可回看的路径，把看展变成一次身体经验。",
        "concepts": ["让材料生成边界", "让信息进入构造", "让动线决定记忆"],
        "takeaways": [
            "布料、网、纤维或薄板不必只贴在墙上。把它们拉伸、垂挂、折叠或围合，材料本身就能定义可进入与不可进入的空间。",
            "字标不应等到最后才贴上去。把尺寸、悬挂高度、照明和观看距离一起设定，信息才能成为可阅读的空间构件。",
            "每个展台都要给出接近、停留、回望三种距离。动线被写进平面，产品、叙事与人的记忆才会真正连起来。",
        ],
        "publish_title": "121期｜展览如何成为空间",
        "publish_body": "Casabella-Costruzioni 121把罗马纺织展当作一个完整的空间问题来讨论。纺织品不再只是被摆进玻璃柜的商品：它可以被悬挂成边界、拉成视觉深度、接住光线，也可以与文字、雕塑和行走路线一起决定展台的节奏。\n\nRayon-Fiocco馆用高大的字标和雕塑在远处建立识别；Nizzoli的染料馆以弧形顶面、竖向构件和连续灯光压缩并引导视线；Pica在纺织展台里把布料当作悬挂构件，而不是背景。它们共同回答了一个至今有效的问题：如何让材料本身参与空间组织。\n\n可迁移的方法很直接：先用材料生成边界，再让信息进入构造，最后用动线决定体验。这样做，展览才会从一组展品升级为可以被身体记住的场所。",
        "tags": "#Casabella #建筑杂志 #展览设计 #空间设计 #纺织设计 #材料设计 #平面设计 #建筑历史",
        "cards": [
            {
                "image": "02-rayon-fiocco.jpg", "mode": "photo", "accent": "#c55a43", "focal": (0.50, 0.44),
                "source": "Agnoldomenico Pica｜罗马纺织展 Rayon-Fiocco馆｜Casabella-Costruzioni 121",
                "eyebrow": "观点 01｜入口先给出远距离识别",
                "title": "把字标、雕塑和入口压成一条竖向界面，人在抵达前就知道展览从哪里开始",
                "body": "入口不是一块孤立的招牌。大尺度文字负责远看，人物尺度的雕塑建立近看，立面与遮棚再把视线带向门洞。识别、靠近与进入被放在同一条空间序列里，品牌才不会停留在平面上。",
            },
            {
                "image": "03-nizzoli-coloranti.jpg", "mode": "photo", "accent": "#355f7a", "focal": (0.48, 0.45),
                "source": "Marcello Nizzoli｜罗马纺织展 国染料馆｜Casabella-Costruzioni 121",
                "eyebrow": "观点 02｜曲面顶棚要引导视线",
                "title": "用弧形顶面、竖向肋条和连续灯光拉长视线，让展台从走廊变成有方向的空间",
                "body": "弧面不是为了制造造型。它把视线抬高并向前推送，竖向构件控制节奏，底部展柜维持可阅读的近距离尺度。观众一边移动，一边在不同高度接收产品、图像和文字。",
            },
            {
                "image": "04-pica-textile-ring.jpg", "mode": "photo", "accent": "#6f7b55", "focal": (0.48, 0.45),
                "source": "Agnoldomenico Pica｜VI Triennale纺织展台｜Casabella-Costruzioni 121",
                "eyebrow": "观点 03｜布料可以成为轻质隔断",
                "title": "把织物从圆形框架垂到地面，柔软材料也能围出中心、边界和观看距离",
                "body": "纺织品最有价值的不是图案，而是可悬挂、可透光、可摆动。将它与简单框架配合，展台便能获得轻量的围合，不必依赖厚重展墙，也保留了材料本身的质感和空气感。",
            },
            {
                "image": "05-pica-snia-stand.jpg", "mode": "photo", "accent": "#c55a43", "focal": (0.50, 0.46),
                "source": "Agnoldomenico Pica｜SNIA Viscosa纺织展台｜Casabella-Costruzioni 121",
                "eyebrow": "观点 04｜让材料成为空间的主角",
                "title": "把不同织物拉到柱、梁与框架之间，展品的长度、重量和垂坠感直接生成空间层次",
                "body": "展架不需要抢走材料的注意力。细框、柱网和悬挂点只提供秩序，织物的下垂、反光和重叠负责制造深度。观众看到的既是产品，也是一种由材料自己完成的空间构成。",
            },
            {
                "image": "06-marzotto-stand.png", "mode": "photo", "accent": "#355f7a", "focal": (0.52, 0.48),
                "source": "作者未详｜Marzotto羊毛纺织展台｜Casabella-Costruzioni 121",
                "eyebrow": "观点 05｜样品要有比较的尺度",
                "title": "把纱线与布样缠绕到连续柱面上，再用悬挂字标定位，材料比较才不会变成杂乱陈列",
                "body": "面对大量色彩与纹理，最有效的做法是先建立重复的承载单元。柱面给样品统一尺寸，字标帮助快速定位，外圈通道保证观看距离。信息密度增加时，秩序比装饰更重要。",
            },
            {
                "image": "07-de-micheli-stand.png", "mode": "photo", "accent": "#6f7b55", "focal": (0.50, 0.46),
                "source": "作者未详｜Carlo De Micheli纺织展台｜Casabella-Costruzioni 121",
                "eyebrow": "观点 06｜展柜应服务停留动作",
                "title": "把样衣放在低台、把图像放在视平线、把名称悬在上方，一次停留就能读完材料与用途",
                "body": "展陈的高度决定阅读顺序：低台适合近看细部，墙面承担图像与说明，悬挂文字负责远距离导航。三层信息同时出现，却不互相遮挡，观众也不必在展台前反复寻找重点。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella-Costruzioni 121原刊封面｜Casabella官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/121-nz.jpg",
            "`02-rayon-fiocco.jpg`｜Rayon-Fiocco馆入口，罗马纺织展，1937-38｜Roscini Vitali《Mostra del Tessile nazionale》｜https://www.edizionicaracol.it/wordpress/wp-content/uploads/2021/03/Studi-e-Ricerche-n.-8_4-Roscini-Vitali.pdf",
            "`03-nizzoli-coloranti.jpg`｜Marcello Nizzoli，国染料馆内部，罗马纺织展，1937-38｜同上",
            "`04-pica-textile-ring.jpg`｜Agnoldomenico Pica，VI Triennale纺织展台，1936｜Lombardia Beni Culturali｜https://www.lombardiabeniculturali.it/fotografie/schede/IMM-3u030-0002062/",
            "`05-pica-snia-stand.jpg`｜Agnoldomenico Pica，SNIA Viscosa展台，1936｜Lombardia Beni Culturali｜https://www.lombardiabeniculturali.it/fotografie/schede/IMM-3u030-0002065/",
            "`06-marzotto-stand.png`｜Marzotto羊毛纺织展台，米兰博览会，1937｜Fondazione Fiera Milano｜https://archiviostorico.fondazionefiera.it/oggetti/5423-stand-di-filati-e-tessuti-di-lana-della-marzotto-nel-padiglione-dei-tessili-e-dellabbigliamento-alla-fiera-campionaria-di-milano-del-1937",
            "`07-de-micheli-stand.png`｜Carlo De Micheli纺织展台，米兰博览会，1937｜Fondazione Fiera Milano｜https://archiviostorico.fondazionefiera.it/oggetti/5419-stand-di-confezioni-della-soc-an-carlo-de-micheli-nel-padiglione-dei-tessili-e-dellabbigliamento-alla-fiera-campionaria-di-milano-del-1937",
            "文章目录｜Agnoldomenico Pica《Discorso sulla mostra romana del Tessile》，Casabella-Costruzioni 121，pp.14-27｜Fondo Mario De Renzi｜https://www.fondoderenzi.org/p/bibliografia",
            "文章目录｜A. M. Mazzucchelli《Progetto di una Casa del Fascio a Trieste》，Casabella 121，pp.4-9｜CRS Trieste｜https://crsrv.org/PDF/Quaderni/29/Ferruccio-Canali-Avanguardie-artistiche-nella-Trieste-tra-le-due-guerre-futuristi-razionalisti-e-costruttivisti.pdf",
            "文章目录｜Franco Marescotti《Il vetro isolante Termolux》，Casabella-Costruzioni 121，pp.36-37｜Politecnico di Torino WebThesis｜https://webthesis.biblio.polito.it/5916/",
        ],
    },
    {
        "slug": "casabella-122",
        "issue": "CASABELLA-COSTRUZIONI 122",
        "date": "FEBBRAIO 1938 | ANNO XI",
        "date_cn": "1938年2月",
        "cover": "book-cover.jpg",
        "accent": "#8d3f3a",
        "question": "当建筑承担制度与仪式，\n平面、入口和立面都会成为权力的语言",
        "thesis_label": "城市界面 | 入口 | 分区 | 尺度",
        "thesis": "122期刊出 Casa Littoria竞赛文献。它们值得被批判性地阅读：高塔、对称轴线和宽阔台阶会如何塑造服从感；行政、集会与纪念功能又如何争夺平面。公共建筑不是中性的外壳，空间秩序会清楚规定谁被欢迎、谁被展示、谁被排除。",
        "summary": "公共性不是由大台阶、对称轴线或高塔自动产生。真正可被检验的公共建筑，要让入口平等可达、服务空间容易找到、集会空间能转换用途、外部场地不被单一仪式垄断。把这些问题画进平面，建筑才不会只剩权力的表情。",
        "concepts": ["先审视谁能进入", "把仪式与日常分开", "让城市界面可被使用"],
        "takeaways": [
            "从街道走到门厅的每一步都要可被不同人使用。入口不该只服务典礼照片，也要照顾日常到达、等候、无障碍和明确的方向。",
            "会议、办公、档案和纪念空间需要各自的流线与尺度。把它们混成一个巨大前厅，只会用形式掩盖真实的使用冲突。",
            "广场、台阶和首层界面应允许停留、穿行与临时活动。公共空间只有被多种身体占用，才不会沦为单向观看的背景。",
        ],
        "publish_title": "122期｜公共建筑如何被政治化",
        "publish_body": "Casabella-Costruzioni 122记录 Casa Littoria 竞赛的多种方案。这类项目需要带着批判阅读：建筑如何把行政办公、集会仪式、纪念符号和城市视线绑在一起，又如何通过高塔、台阶、轴线和大广场塑造服从感。\n\nRidolfi团队的草图、立面与模型把办公体量、集会空间、塔与入口广场拆开处理；Libera与Samona的前期方案则显示，同一个任务一旦改变场地、平面和交通组织，建筑表达会完全不同。值得看的不是哪一张立面更“宏伟”，而是谁拥有入口、空间如何分层、城市界面是否允许日常使用。\n\n今天做公共建筑时，这仍是最直接的检验：先审视谁能进入，再把仪式与日常分开，最后让广场与首层真正可以被使用。",
        "tags": "#Casabella #建筑杂志 #公共建筑 #建筑评论 #建筑历史 #城市设计 #建筑竞赛 #空间设计",
        "cards": [
            {
                "image": "03-ridolfi-sketch.jpg", "mode": "document", "accent": "#8d3f3a",
                "source": "Mario Ridolfi等｜Palazzo Littorio二阶段竞赛草图｜Casabella-Costruzioni 122",
                "eyebrow": "观点 01｜先把城市与体量放在一起看",
                "title": "公共建筑的第一张草图，应先说明道路、入口和主要体量如何相遇，而不是先追求纪念性的外形",
                "body": "草图把办公体量、演讲空间、塔与纪念区拉开，说明不同功能需要不同的城市位置。真正值得检验的是：从街道到门厅能否清晰抵达，广场是否可以穿行，体量是否压迫周边的日常尺度。",
            },
            {
                "image": "04-ridolfi-elevation.jpg", "mode": "document", "accent": "#355f7a",
                "source": "Mario Ridolfi等｜Palazzo Littorio二阶段竞赛立面图｜Casabella-Costruzioni 122",
                "eyebrow": "观点 02｜高度要对应真实功能",
                "title": "把办公、集会、纪念与交通分配到不同高度，建筑才不会用一个巨大体量掩盖功能冲突",
                "body": "立面并非只是对称或不对称的选择。每一段高度都应能回到具体使用：哪里需要安静办公，哪里需要大跨度集会，哪里承担竖向交通。功能关系被画清楚，形式才有可以讨论的基础。",
            },
            {
                "image": "05-ridolfi-front.jpg", "mode": "document", "accent": "#6f7b55",
                "source": "Mario Ridolfi等｜Palazzo Littorio二阶段竞赛主立面｜Casabella-Costruzioni 122",
                "eyebrow": "观点 03｜入口广场最需要被批判",
                "title": "宽台阶和正面入口会制造仪式感，但公共性要看谁能停留、谁能穿过、谁被拒在界面之外",
                "body": "大型入口天然具有聚集和观看的力量，因此更需要被仔细审视。首层是否有可达的服务空间，台阶是否只为典礼服务，立面是否把人缩成背景，决定了建筑是在接纳公众还是在要求公众仰视。",
            },
            {
                "image": "06-ridolfi-model.jpg", "mode": "photo", "accent": "#8d3f3a", "focal": (0.50, 0.55),
                "source": "Mario Ridolfi等｜Palazzo Littorio二阶段竞赛模型｜Casabella-Costruzioni 122",
                "eyebrow": "观点 04｜模型先检查身体尺度",
                "title": "在模型里检查塔、台阶和低层体量的距离，才能看出城市空间是在组织人，还是在压迫人",
                "body": "模型把图纸上的尺度关系变得可感知：高塔从哪里出现，低层建筑怎样围合，台阶与道路之间有没有缓冲。公共项目不能只看鸟瞰的完整性，更要从行走高度检验压迫感与可达性。",
            },
            {
                "image": "07-libera-competition.jpg", "mode": "document", "accent": "#355f7a",
                "source": "Adalberto Libera｜Palazzo Littorio前期竞赛方案｜Casabella-Costruzioni 122",
                "eyebrow": "观点 05｜形式变化必须回到平面",
                "title": "曲线体量或强烈轮廓并不等于开放，先看首层路径是否连续、公共厅是否真正连向城市",
                "body": "这类竞赛图最容易让人被外形吸引。更关键的问题是，弧形或围合的布局有没有留下可自由穿行的地面，入口是否只指向单一轴线，公共空间能否在没有仪式时仍被日常生活使用。",
            },
            {
                "image": "08-samona-competition.jpg", "mode": "document", "accent": "#6f7b55",
                "source": "Giuseppe Samona｜Palazzo Littorio前期竞赛方案｜Casabella-Costruzioni 122",
                "eyebrow": "观点 06｜总平面比渲染更诚实",
                "title": "先在总平面里读清会议、办公、服务与交通的边界，再判断一座公共建筑是否真的为人服务",
                "body": "一张透视图可以放大气势，却常常隐藏组织问题。总平面会直接暴露：不同人群从哪里进入，服务空间是否被挤到角落，集会高峰如何疏散，日常动线是否被纪念性轴线切断。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella-Costruzioni 122原刊封面｜Casabella官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/122-nz.jpg",
            "`03-ridolfi-sketch.jpg`、`04-ridolfi-elevation.jpg`、`05-ridolfi-front.jpg`、`06-ridolfi-model.jpg`｜Mario Ridolfi、Vittorio Cafiero、Ernesto La Padula、Ettore Rossi，Palazzo Littorio二阶段竞赛，1937｜Fondo Ridolfi-Frankl-Malagricci｜https://www.fondoridolfi.org/FondoRidolfi/52_5/periodo/progetto-di-concorso-di-secondo-grado-per-il-palazzo-littorio-a-roma.htm",
            "`07-libera-competition.jpg`｜Adalberto Libera，Palazzo Littorio前期竞赛方案，1934｜+ACNE+｜https://plusacne.wordpress.com/2014/01/02/palazzo-del-littorio/",
            "`08-samona-competition.jpg`｜Giuseppe Samona，Palazzo Littorio前期竞赛方案，1934｜+ACNE+｜https://plusacne.wordpress.com/2014/01/02/palazzo-del-littorio/",
            "文章目录｜Giuseppe Pagano《Documenti del concorso per la Casa Littoria di Roma》，Casabella 122，pp.20-21｜Fondo Ridolfi-Frankl-Malagricci｜https://www.fondoridolfi.org/bibliografia.htm",
            "原刊专题｜《Documenti del concorso per la Casa Littoria di Roma: sei progetti segnalati + cinque progetti riprovati》，Casabella 122，pp.22-29｜Fondo Mario De Renzi｜https://www.fondoderenzi.org/p/bibliografia",
        ],
    },
]


def save_rgb(image: Image.Image, path: Path) -> Path:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def prepare_assets(cfg: dict, src: Path) -> None:
    if cfg["slug"] != "casabella-121":
        return
    crops = {
        "02-rayon-fiocco.jpg": ("tessile-source-08.jpg", (130, 95, 930, 1120)),
        "03-nizzoli-coloranti.jpg": ("tessile-source-12.jpg", (125, 70, 930, 1120)),
    }
    for output, (name, box) in crops.items():
        image = Image.open(src / name).convert("RGB").crop(box)
        image = ImageEnhance.Contrast(image).enhance(1.08)
        image = ImageEnhance.Sharpness(image).enhance(1.15)
        image.save(src / output, quality=96, subsampling=0)


def source_line(draw: ImageDraw.ImageDraw, text: str, y: int, color: str = INK) -> None:
    draw.line((68, y - 18, 1174, y - 18), fill=rgba(color, 80), width=2)
    draw_fit(draw, (68, y), text, 1090, 46, 21, rgba(color, 175), spacing=5)


def make_cover_121(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#eef0e7"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 38), fill=BLUE)
    draw.rectangle((0, 38, 420, H), fill="#dbe0cf")
    draw.text((68, 68), cfg["issue"], font=font(FONT_BOLD, 26), fill=INK)
    draw.text((1170, 70), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(INK, 175), anchor="ra")
    draw.text((68, 200), "单期主线", font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (68, 278), cfg["question"], 340, 510, 50, INK, serif=True, spacing=16)
    draw.text((68, 850), cfg["thesis_label"], font=font(FONT_BOLD, 22), fill=accent)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
    mount(canvas, cover, (490, 155, 650, 710), True)
    draw.rectangle((490, 890, 1140, 914), fill=accent)
    draw_fit(draw, (490, 970), cfg["thesis"], 650, 425, 38, INK, serif=True, spacing=14)
    source_line(draw, "Casabella-Costruzioni｜第121期原刊封面｜1938年1月", 1512)
    page_mark(draw, 1, False)
    return save_rgb(canvas, out / "01.jpg")


def make_cover_122(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(12201)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 38), fill=accent)
    draw.rectangle((0, 1030, W, H), fill=BLUE)
    draw.text((68, 68), cfg["issue"], font=font(FONT_BOLD, 26), fill=INK)
    draw.text((1170, 70), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(INK, 175), anchor="ra")
    draw.text((68, 155), "单期主线", font=font(FONT_BOLD, 24), fill=accent)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
    mount(canvas, cover, (68, 224, 600, 700), True)
    draw.rectangle((742, 224, 760, 924), fill=accent)
    draw_fit(draw, (808, 240), cfg["question"], 330, 640, 51, INK, serif=True, spacing=16)
    draw.text((68, 1105), cfg["thesis_label"], font=font(FONT_BOLD, 22), fill="#f0e8db")
    draw_fit(draw, (68, 1178), cfg["thesis"], 1080, 260, 35, "#f0e8db", serif=True, spacing=13)
    source_line(draw, "Casabella-Costruzioni｜第122期原刊封面｜1938年2月", 1512, "#f0e8db")
    page_mark(draw, 1, True)
    return save_rgb(canvas, out / "01.jpg")


def make_summary_121(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#eef0e7"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    header(draw, cfg, 8, False)
    for x in range(82, 1160, 42):
        draw.line((x, 150, x, 510), fill=rgba(accent, 110), width=4)
    draw.text((68, 175), "把材料做成空间", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (68, 245), cfg["summary"], 1060, 225, 48, INK, serif=True, spacing=17)
    colors = [accent, "#355f7a", "#6f7b55"]
    xs = [68, 444, 820]
    for idx, (x, label, body, color) in enumerate(zip(xs, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.rectangle((x, 690, x + 310, 1370), fill=rgba(color, 245))
        draw.text((x + 34, 730), f"0{idx}", font=font(FONT_BOLD, 38), fill=rgba(LIGHT, 170))
        draw_fit(draw, (x + 34, 815), label, 242, 110, 34, LIGHT, serif=True, spacing=10)
        draw.line((x + 34, 950, x + 275, 950), fill=rgba(LIGHT, 130), width=2)
        draw_fit(draw, (x + 34, 1000), body, 242, 300, 30, LIGHT, serif=True, spacing=11)
    source_line(draw, "Casabella-Costruzioni｜第121期主要文章与案例｜1938年1月", 1475)
    page_mark(draw, 8, False)
    return save_rgb(canvas, out / "08.jpg")


def make_summary_122(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(BLUE))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    header(draw, cfg, 8, True)
    draw.rectangle((68, 148, 86, 570), fill=accent)
    draw.text((120, 150), "让公共性可以被检验", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (120, 220), cfg["summary"], 1000, 300, 48, "#f0e8db", serif=True, spacing=17)
    colors = ["#f0e8db", "#dac7a7", "#d48a71"]
    ys = [690, 935, 1180]
    for idx, (y, label, body, color) in enumerate(zip(ys, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.rectangle((68, y, 1174, y + 185), fill=rgba(color, 245))
        draw.rectangle((68, y, 218, y + 185), fill=accent)
        draw.text((143, y + 67), f"0{idx}", font=font(FONT_BOLD, 44), fill=rgba(LIGHT, 190), anchor="mm")
        draw.text((258, y + 36), label, font=font(FONT_BOLD, 34), fill=BLUE)
        draw.line((258, y + 98, 1128, y + 98), fill=rgba(BLUE, 80), width=2)
        draw_fit(draw, (258, y + 120), body, 835, 52, 27, rgba(INK, 220), serif=True, spacing=8)
    source_line(draw, "Casabella-Costruzioni｜第122期竞赛文献｜1938年2月", 1475, "#f0e8db")
    page_mark(draw, 8, True)
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
            *[f"{n:02d} {card['source']}：{card['title']}" for n, card in enumerate(cfg["cards"], 2)],
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
    cover_maker = make_cover_121 if cfg["slug"] == "casabella-121" else make_cover_122
    summary_maker = make_summary_121 if cfg["slug"] == "casabella-121" else make_summary_122
    paths = [cover_maker(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(summary_maker(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards, preview and publishing files in {out}")


if __name__ == "__main__":
    for issue in ISSUES:
        render_issue(issue)
