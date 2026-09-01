from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    FONT_BOLD, FONT_SANS, H, INK, LIGHT, PAPER, ROOT, W,
    draw_fit, font, header, make_card, make_preview, mount, page_mark, rgba,
)


ISSUES = [
    {
        "slug": "casabella-127",
        "issue": "CASABELLA-COSTRUZIONI 127",
        "date": "LUGLIO 1938 | ANNO X",
        "date_cn": "1938年7月",
        "cover": "book-cover.jpg",
        "accent": "#be3b32",
        "dark": "#151c24",
        "question": "钢的美感不在表面；在它能否把人流、展品、城市与结构组织成一套清晰秩序。",
        "thesis": "第127期把新居住区、米兰博览会与钢结构放在同一张问题纸上：现代建筑不是单独的造型，而是用构件、路径和节奏安排群体活动。",
        "summary": "127期最重要的提醒是：结构从来不只是受力计算。钢架、入口、道路、展台与标识一起规定了人如何抵达、停留、转向和看见。空间一旦能把规则说清，材料才会真正显出它的美。",
        "concepts": ["先显出路径", "再组织视线", "让构件说明规则"],
        "takeaways": [
            "先把人流、货流和服务流画出来，再决定柱网、入口和展台的位置；没有路径依据的结构，往往只剩形式。",
            "临时展览也需要城市尺度：用主街、门厅、节点和可识别的标志，让人群知道自己在何处、下一步往哪里走。",
            "钢结构的轻与薄应当转化为清晰跨度、可读节点与可变布置，而不是覆盖在立面上的工业表情。",
        ],
        "publish_title": "CASABELLA127｜钢如何组织空间",
        "publish_body": "第127期把城市居住区、米兰博览会与钢结构并列起来，真正讨论的是同一个问题：建筑怎样把大规模活动组织得清楚。钢的价值不在于显得“工业”，而在于它能用更少的支撑换来更连续的视线、更灵活的布置和更直接的路径。\n\n1938年的米兰博览会是一座短期存在的城市。入口、主街、展亭、广告塔和休息节点，都在引导人群前进、驻足与辨认方向。与此同时，住区方案把道路、绿地和住宅单元编排成更长时间尺度的日常秩序。\n\n把这期杂志放回今天，方法依然有效：先画出人流、货流和服务流；再让入口、柱网与转角回应这些路径；最后用结构把规则说出来，而不是把结构当成装饰。你在展览、商场或交通建筑里，最在意哪一个“容易迷路”的节点？",
        "tags": "#Casabella #钢结构 #展览建筑 #空间设计 #建筑历史 #米兰博览会 #建筑流线 #现代建筑",
        "cards": [
            {"image":"02-fiera.png","mode":"photo","accent":"#be3b32","focal":(0.50,0.49),"source":"Pagano｜十九届米兰博览会｜Casabella 127","eyebrow":"观点 01｜展会先是一座临时城市","title":"主街必须让人一眼读懂：展亭沿路展开，节点负责停留，方向感才不会被商品淹没","body":"博览会不是把展位并排塞满。主通道要提供连续视野，横向入口负责把人引入展亭；人群越多，越需要用道路宽度、树荫和转角建立可记住的节奏。"},
            {"image":"03-fiera.png","mode":"photo","accent":"#d69b37","focal":(0.50,0.45),"source":"Pagano 等｜米兰新住区方案｜Casabella 127","eyebrow":"观点 02｜公共空间不是余下的空地","title":"把道路、绿地和集中的活动点先排成层级，住宅单元才会从孤岛变成可使用的城市片段","body":"住区的密度问题要从公共空间开始回答。主路承担连续到达，支路减慢速度，绿地与广场成为共享节点；房子不是围住空地，而是把日常活动接进这套层级。"},
            {"image":"04-fiera.png","mode":"photo","accent":"#3e7790","focal":(0.52,0.42),"source":"Pagano、Albini 等｜十九届米兰博览会｜Casabella 127","eyebrow":"观点 03｜立面要同时承担识别与进入","title":"曲面玻璃、入口和大字标识共同构成第一道空间说明：人还没进门，已经知道这里展示什么","body":"展亭的外壳不是图像背景。可见的入口、通透的边界和远距离可读的文字，会把行业、展品与人流在街道上连接起来；建筑由此成为信息的接口。"},
            {"image":"05-fiera.png","mode":"photo","accent":"#be3b32","focal":(0.50,0.47),"source":"Pagano｜钢是否有美学？｜Casabella 127","eyebrow":"观点 04｜钢的表达来自跨度与节点","title":"当结构把入口撑成清楚的门槛，铁不需要被装饰；受力逻辑本身就能给人方向和尺度","body":"钢的轻盈应该让构件各司其职：柱子说明支撑，梁说明跨越，连接说明转折。看得懂的结构会让人自然判断入口、停留区与通过区，而不是只留下表面风格。"},
            {"image":"06-fiera.png","mode":"photo","accent":"#d69b37","focal":(0.52,0.45),"source":"Franco Albini｜INA 展亭｜Casabella 127","eyebrow":"观点 05｜临时建筑也要有稳定的秩序","title":"用清晰体量、屋顶标志和开口节奏抓住视线；展期结束后，仍能留下可记忆的空间逻辑","body":"短命并不等于随意。临时展亭尤其需要可读的体量与招牌位置，因为人们只会经过一次。越是短暂的建筑，越要把入口、视线与停留点安排得直接。"},
            {"image":"07-fiera.png","mode":"photo","accent":"#3e7790","focal":(0.50,0.51),"source":"Pagano｜十九届米兰博览会｜Casabella 127","eyebrow":"观点 06｜展品要成为空间的尺度","title":"设备、展台和行走距离一起决定展览；把真实尺度露出来，观众才会理解工业如何进入日常","body":"展示大型设备时，建筑不必抢走注意力。让机器沿明确路径排布，留出观看、绕行和比较的距离，再以简洁顶棚提供整体秩序，技术才会变成可被身体理解的知识。"},
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella-Costruzioni 127 原刊封面，1938年7月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/127-nz.jpg",
            "`02-fiera.png`｜1938米兰博览会工业大道历史照片｜Archivio Fondazione Fiera Milano｜https://backend.archiviofondazionefieramilano.archiui.it/cataloga/media/fieramilano/images/6/0/88267_ca_object_representations_media_6003_large.png｜许可待商业发布前复核｜裁切、调色与文字排版",
            "`03-fiera.png`｜1938米兰博览会 Italia 广场历史照片｜Archivio Fondazione Fiera Milano｜https://backend.archiviofondazionefieramilano.archiui.it/cataloga/media/fieramilano/images/5/9/60263_ca_object_representations_media_5922_large.png｜许可待商业发布前复核｜裁切、调色与文字排版",
            "`04-fiera.png`｜1938米兰博览会 Snia Viscosa 展亭入口｜Archivio Fondazione Fiera Milano｜https://backend.archiviofondazionefieramilano.archiui.it/cataloga/media/fieramilano/images/5/9/95581_ca_object_representations_media_5936_large.png｜许可待商业发布前复核｜裁切、调色与文字排版",
            "`05-fiera.png`｜1938米兰博览会 Domodossola 门入口钢拱｜Archivio Fondazione Fiera Milano｜https://backend.archiviofondazionefieramilano.archiui.it/cataloga/media/fieramilano/images/5/9/42142_ca_object_representations_media_5906_large.png｜许可待商业发布前复核｜裁切、调色与文字排版",
            "`06-fiera.png`｜Franco Albini，1938米兰博览会 INA 展亭｜Archivio Fondazione Fiera Milano｜https://backend.archiviofondazionefieramilano.archiui.it/cataloga/media/fieramilano/images/6/0/96690_ca_object_representations_media_6078_large.png｜许可待商业发布前复核｜裁切、调色与文字排版",
            "`07-fiera.png`｜1938米兰博览会建筑行业展区｜Archivio Fondazione Fiera Milano｜https://backend.archiviofondazionefieramilano.archiui.it/cataloga/media/fieramilano/images/5/9/18325_ca_object_representations_media_5971_large.png｜许可待商业发布前复核｜裁切、调色与文字排版",
            "目录核验｜第127期含 Pagano《I Littoriali dell’architettura》《Esiste un’estetica del ferro?》、Pagano/ Bianchetti/ Pea 住区方案与《La XIX Fiera di Milano》｜Casa dell’Architettura Latina｜https://www.casadellarchitettura.eu/collezioni/riviste/casabella-costruzioni/",
        ],
    },
    {
        "slug": "casabella-128",
        "issue": "CASABELLA-COSTRUZIONI 128",
        "date": "AGOSTO 1938 | ANNO X",
        "date_cn": "1938年8月",
        "cover": "book-cover.jpg",
        "accent": "#0d7180",
        "dark": "#142b33",
        "question": "商店不是摆满货物的房间；它要把街道、橱窗、展示、储藏与服务接成连续体验。",
        "thesis": "第128期用 Gardella 的诊所与 Bottoni、Nizzoli、Pucci 的 Olivetti 那不勒斯店铺说明：现代室内不是装饰，而是让看见、选择、交谈、存取与维护同时成立的空间装置。",
        "summary": "128期把现代性拉回身体尺度。玻璃把街道接入室内，长柜台组织停留与展示，墙面兼作储藏，灯光调节注意力；而诊所的采光、通风与路径则说明，室内秩序最终服务于人的使用与健康。",
        "concepts": ["把街道接进来", "让陈列变成动线", "把后勤藏进界面"],
        "takeaways": [
            "商店入口不应只是一扇门：橱窗、视线与人行道共同构成第一段体验，商品如何被看见要先于室内风格。",
            "把展柜做成可停留的长边，而不是散落的家具；人可以边走边看，也能在一个节点停下交谈与比较。",
            "储藏、照明、标识和补货应尽量嵌入墙面或柜体，前场保持连续，工作人员才不必反复穿越顾客路径。",
        ],
        "publish_title": "CASABELLA128｜商店是街道",
        "publish_body": "第128期最值得今天重读的案例，是 Piero Bottoni、Marcello Nizzoli 与 Mario Pucci 为 Olivetti 设计的那不勒斯店铺。它不是用装潢把商品包起来，而是把街道、橱窗、陈列、交谈、收纳和照明接成一条连续路径。\n\n店面用大玻璃把室内直接暴露给行人；近六米长的透明柜台把打字机排成可被比较的序列；背景墙兼作 96 个抽屉，储藏从视线中消失；金属网格、镜面与不同光源再把洽谈、展示和服务分开又连接。\n\n同期 Gardella 的防结核诊所提醒我们，这种空间观并不只适用于消费：采光、通风、可读路径和洁净界面，都在让人更有尊严地使用建筑。今天的零售空间，可以先从“街道如何进入室内”开始设计。你的体验里，哪一家店最能让你愿意停下来？",
        "tags": "#Casabella #零售空间 #室内设计 #Olivetti #建筑历史 #展陈设计 #空间动线 #现代建筑",
        "cards": [
            {"image":"02-bottoni.jpg","mode":"document","accent":"#0d7180","source":"Pagano｜那不勒斯商店｜Casabella 128","eyebrow":"观点 01｜街道从橱窗开始进入室内","title":"把中央大玻璃做成室内的延伸，商品与人的活动同时被街道看见，店面才有真正的公共性","body":"Olivetti 店没有把展示封在室内深处。中央橱窗让行人的视线直接穿进店里，左右小橱窗补充细节；玻璃不是边界，而是连接街道与陈列的第一层空间。"},
            {"image":"03-bottoni.jpg","mode":"photo","accent":"#d99a37","focal":(0.50,0.46),"source":"Bottoni、Nizzoli、Pucci｜Olivetti Napoli｜Casabella 128","eyebrow":"观点 02｜柜台是一条可停留的展示线","title":"把产品沿透明长柜台连续排开，顾客能边走边比较；展示由此成为动线，而不是一排孤立陈设","body":"近六米的柜台把打字机排列在同一条可读的水平线上。它既为街道橱窗提供画面，也给室内的人留下观看、比较与靠近工作人员的共同界面。"},
            {"image":"04-bottoni.jpg","mode":"photo","accent":"#0d7180","focal":(0.50,0.46),"source":"Bottoni、Nizzoli、Pucci｜Olivetti Napoli｜Casabella 128","eyebrow":"观点 03｜储藏应该长进墙面","title":"让背景墙同时成为抽屉与视觉秩序，前场就不用堆满柜体；小店也能把有限面积留给人","body":"店面深度不足五米，设计把 96 个抽屉嵌进背景墙，将配件、资料与零碎存取隐藏在整齐界面后。收纳不再抢占通道，展示空间保持完整。"},
            {"image":"05-bottoni.jpg","mode":"photo","accent":"#d99a37","focal":(0.48,0.48),"source":"Bottoni、Nizzoli、Pucci｜Olivetti Napoli｜Casabella 128","eyebrow":"观点 04｜用一件艺术品校准不对称","title":"当柜台和墙面必须为电梯让路，雕塑可以成为构图与视线的支点，而不是附加装饰","body":"柜台与背景墙无法等长，悬挂的雕塑因此承担了平衡重心的任务。它把橱窗、商品与室内深处的镜面串成一条视线，让不对称变成可被感知的秩序。"},
            {"image":"06-bottoni.jpg","mode":"photo","accent":"#0d7180","focal":(0.52,0.48),"source":"Bottoni、Nizzoli、Pucci｜Olivetti Napoli｜Casabella 128","eyebrow":"观点 05｜谈话区要可分而不断","title":"金属网格划出交流位置，却保留光线和视线；小空间不必靠实体隔墙来获得秩序","body":"一侧的金属网格承载可更换的宣传信息，也界定了与顾客交谈的区域。它没有切断商店整体，而是用透明边界让安静交流与公开展示同时发生。"},
            {"image":"07-gardella-page.jpg","mode":"document","accent":"#d99a37","source":"Giolli｜Alessandria 防结核诊所｜Casabella 128","eyebrow":"观点 06｜健康空间先让光与路可读","title":"诊所的平面要让入口、等候、检查与日照各有位置；洁净感来自流程清楚，而不是表面白色","body":"Gardella 的防结核诊所把现代空间原则放回使用：外部开口带来光与空气，平面把来访者和医疗活动梳理成清楚序列。功能、卫生与空间体验在这里是同一件事。"},
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella-Costruzioni 128 原刊封面，1938年8月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/128-nz.jpg",
            "`02-bottoni.jpg`｜Piero Bottoni 档案，Olivetti 那不勒斯店铺项目封面页｜Archivio Piero Bottoni, Politecnico di Milano｜https://www.archiviobottoni.polimi.it/wp-content/uploads/op168_copertina.jpg｜许可待商业发布前复核｜裁切与文字排版",
            "`03-bottoni.jpg`｜Piero Bottoni 档案，Olivetti 那不勒斯店铺设计图｜Archivio Piero Bottoni, Politecnico di Milano｜https://www.archiviobottoni.polimi.it/wp-content/uploads/op168_disfpb_013.jpg｜许可待商业发布前复核｜裁切与文字排版",
            "`04-bottoni.jpg`｜Piero Bottoni 档案，Olivetti 那不勒斯店铺历史照片｜Archivio Piero Bottoni, Politecnico di Milano｜https://www.archiviobottoni.polimi.it/wp-content/uploads/op168_fotoalbg_017.jpg｜许可待商业发布前复核｜裁切与文字排版",
            "`05-bottoni.jpg`｜Piero Bottoni 档案，Olivetti 那不勒斯店铺历史负片｜Archivio Piero Bottoni, Politecnico di Milano｜https://www.archiviobottoni.polimi.it/wp-content/uploads/op168_fotoneg_001.jpg｜许可待商业发布前复核｜裁切与文字排版",
            "`06-bottoni.jpg`｜Piero Bottoni 档案，Olivetti 那不勒斯店铺历史照片｜Archivio Piero Bottoni, Politecnico di Milano｜https://www.archiviobottoni.polimi.it/wp-content/uploads/op168_fotopos_061.jpg｜许可待商业发布前复核｜裁切与文字排版",
            "`07-gardella-page.jpg`｜Ignazio Gardella，Alessandria 防结核诊所，外观与平面转载页｜Antonino Saggio, Selected Writings｜https://www.nitrosaggio.net/iquaderni/PDFgratis/ANTONINOSAGGIO1929-39.pdf｜原资料标明出自 Casabella-Costruzioni 128，pp.6–7｜裁切与文字排版",
            "`Un negozio a Napoli` 核验｜Giuseppe Pagano，Casabella-Costruzioni 128，1938年8月，pp.26–31；项目为 1937–38 年 Olivetti via Sanfelice 53｜Archivio Piero Bottoni｜https://www.archiviobottoni.polimi.it/docs/archopere/architettura-urbanistica-e-design-1924-1973/op-168-sistemazione-di-un-edificio-a-negozio-e-uffici-e-relativi-arredamenti-per-la-sede-olivetti-in-via-sanfelice-53-a-napoli-1937-38-con-marcello-nizzoli-e-mario-pucci-scultura-di-jenni-wiegm",
            "`Il dispensario antitubercolare d’Alessandria` 核验｜Raffaello Giolli，Casabella-Costruzioni 128，1938年8月，pp.4–9｜La storia degli edifici, la memoria dei luoghi｜https://revistas.utadeo.edu.co/index.php/ltd/article/download/1760/1788",
        ],
    },
]


def save_rgb(image: Image.Image, path: Path) -> Path:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def source_line(draw: ImageDraw.ImageDraw, text: str, y: int, color: str = INK) -> None:
    draw.line((68, y - 18, 1174, y - 18), fill=rgba(color, 88), width=2)
    draw_fit(draw, (68, y), text, 1088, 48, 21, rgba(color, 180), spacing=5)


def make_cover(cfg: dict, src: Path, out: Path) -> Path:
    accent, dark = cfg["accent"], cfg["dark"]
    canvas = Image.new("RGBA", (W, H), rgba("#e8e1d2"))
    draw = ImageDraw.Draw(canvas)
    if cfg["slug"].endswith("127"):
        draw.rectangle((0, 0, W, H), fill=dark)
        for x in range(48, W, 146):
            draw.line((x, 0, x, H), fill=rgba("#d8dde0", 30), width=2)
        for y in range(0, H, 146):
            draw.line((0, y, W, y), fill=rgba("#d8dde0", 24), width=2)
        draw.rectangle((0, 0, W, 30), fill=accent)
        draw.text((68, 78), cfg["issue"], font=font(FONT_BOLD, 25), fill="#f1eee7")
        draw.text((1170, 80), cfg["date"], font=font(FONT_SANS, 19), fill=rgba("#f1eee7", 180), anchor="ra")
        draw.text((68, 188), "单期主线", font=font(FONT_BOLD, 23), fill="#f2ad45")
        draw_fit(draw, (68, 250), cfg["question"], 620, 375, 60, "#f1eee7", serif=True, spacing=18)
        cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
        mount(canvas, cover, (748, 160, 352, 618), True)
        draw.line((68, 730, 1170, 730), fill=rgba("#f1eee7", 110), width=2)
        draw.text((68, 794), "结构是活动的坐标", font=font(FONT_BOLD, 31), fill=accent)
        draw_fit(draw, (68, 866), cfg["thesis"], 1020, 300, 39, "#f1eee7", serif=True, spacing=14)
        source_line(draw, "Casabella-Costruzioni｜第127期原刊封面｜1938年7月", 1510, "#f1eee7")
        page_mark(draw, 1, True)
    else:
        draw.rectangle((0, 0, W, H), fill="#ebdfc7")
        draw.rectangle((0, 0, W, 240), fill=accent)
        draw.text((68, 69), cfg["issue"], font=font(FONT_BOLD, 25), fill="#f7f4ed")
        draw.text((1170, 71), cfg["date"], font=font(FONT_SANS, 19), fill=rgba("#f7f4ed", 190), anchor="ra")
        draw.text((68, 146), "单期主线", font=font(FONT_BOLD, 22), fill="#f7f4ed")
        cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
        mount(canvas, cover, (734, 298, 374, 676), True)
        draw.rectangle((68, 316, 646, 333), fill=accent)
        draw_fit(draw, (68, 390), cfg["question"], 570, 440, 61, dark, serif=True, spacing=18)
        draw.rectangle((0, 1110, W, H), fill=dark)
        draw.text((68, 1188), "商品如何成为空间事件", font=font(FONT_BOLD, 30), fill="#efc36e")
        draw_fit(draw, (68, 1258), cfg["thesis"], 1035, 190, 36, "#f7f4ed", serif=True, spacing=12)
        source_line(draw, "Casabella-Costruzioni｜第128期原刊封面｜1938年8月", 1510, "#f7f4ed")
        page_mark(draw, 1, True)
    return save_rgb(canvas, out / "01.jpg")


def make_summary(cfg: dict, out: Path) -> Path:
    accent, dark = cfg["accent"], cfg["dark"]
    canvas = Image.new("RGBA", (W, H), rgba("#f0e6d3" if cfg["slug"].endswith("127") else dark))
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, cfg["slug"].endswith("128"))
    if cfg["slug"].endswith("127"):
        draw.rectangle((0, 130, W, 150), fill=accent)
        draw.text((68, 206), "从结构到活动", font=font(FONT_BOLD, 26), fill=accent)
        draw_fit(draw, (68, 276), cfg["summary"], 1060, 250, 48, dark, serif=True, spacing=16)
        ys = [660, 910, 1160]
        for i, (y, label, detail) in enumerate(zip(ys, cfg["concepts"], cfg["takeaways"]), 1):
            draw.rectangle((68, y, 1174, y + 190), fill=dark)
            draw.rectangle((68, y, 220, y + 190), fill=accent if i != 2 else "#d69b37")
            draw.text((144, y + 70), f"0{i}", font=font(FONT_BOLD, 48), fill="#f0e6d3", anchor="mm")
            draw.text((265, y + 34), label, font=font(FONT_BOLD, 36), fill="#f0e6d3")
            draw_fit(draw, (265, y + 92), detail, 825, 75, 27, rgba("#f0e6d3", 225), serif=True, spacing=8)
        source_line(draw, "Casabella-Costruzioni｜第127期建筑与结构讨论｜1938年7月", 1505)
        page_mark(draw, 8, False)
    else:
        draw.rectangle((0, 130, W, 150), fill="#efc36e")
        draw.text((68, 206), "让室内保持连续", font=font(FONT_BOLD, 27), fill="#efc36e")
        draw_fit(draw, (68, 278), cfg["summary"], 1060, 260, 48, "#f7f4ed", serif=True, spacing=16)
        x_positions = [68, 430, 792]
        colors = [accent, "#d99a37", "#79a9a8"]
        for i, (x, label, detail, color) in enumerate(zip(x_positions, cfg["concepts"], cfg["takeaways"], colors), 1):
            draw.rectangle((x, 700, x + 314, 742), fill=color)
            draw.text((x + 18, 774), f"0{i}", font=font(FONT_BOLD, 29), fill=color)
            draw_fit(draw, (x + 18, 825), label, 278, 115, 38, "#f7f4ed", serif=True, spacing=12)
            draw.line((x + 18, 978, x + 294, 978), fill=rgba("#f7f4ed", 90), width=2)
            draw_fit(draw, (x + 18, 1018), detail, 278, 325, 29, rgba("#f7f4ed", 220), serif=True, spacing=10)
        source_line(draw, "Casabella-Costruzioni｜第128期室内与健康空间讨论｜1938年8月", 1505, "#f7f4ed")
        page_mark(draw, 8, True)
    return save_rgb(canvas, out / "08.jpg")


def post_manifest(cfg: dict) -> dict:
    return {"type":"magazine","slug":cfg["slug"],"issue":cfg["issue"].title(),"date":cfg["date_cn"],"core_question":cfg["question"],"core_thesis":cfg["thesis"],"pages":[f"01 单期主线：{cfg['question']}", *[f"{n:02d} {c['source']}：{c['title']}" for n,c in enumerate(cfg["cards"],2)], f"08 总结：{'；'.join(cfg['concepts'])}"]}


def write_text_files(cfg: dict, out: Path) -> None:
    (out / "发布文案.md").write_text(f"{cfg['publish_title']}\n\n{cfg['publish_body']}\n\n{cfg['tags']}\n", encoding="utf-8")
    (out / "图片来源.md").write_text(f"# {cfg['issue'].title()} 图片来源\n\n" + "\n".join(f"- {s}" for s in cfg["sources"]) + "\n", encoding="utf-8")
    post = ROOT / "posts" / cfg["slug"]
    post.mkdir(parents=True, exist_ok=True)
    (post / "post.json").write_text(json.dumps(post_manifest(cfg), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_issue(cfg: dict) -> None:
    src, out = ROOT / "assets" / cfg["slug"], ROOT / "output" / cfg["slug"]
    out.mkdir(parents=True, exist_ok=True)
    paths = [make_cover(cfg, src, out)]
    paths += [make_card(cfg, src, out, n, card) for n, card in enumerate(cfg["cards"], 2)]
    paths.append(make_summary(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards in {out}")


if __name__ == "__main__":
    for issue in ISSUES:
        render_issue(issue)
