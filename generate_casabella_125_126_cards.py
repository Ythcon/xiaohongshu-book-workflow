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
    rgba,
)


CFG = {
    "slug": "casabella-125-126",
    "issue": "CASABELLA-COSTRUZIONI 125–126",
    "date": "MAGGIO–GIUGNO 1938 | ANNO XI",
    "date_cn": "1938年5–6月（合刊）",
    "cover": "book-cover.jpg",
    "accent": "#c56a3c",
    "question": "酒店不是一排客房的外壳；它是一套把抵达、停留、休息、服务与景观同时组织起来的空间系统。",
    "thesis": "125–126 合刊把酒店当成独立建筑类型来讨论。真正决定体验的不是大堂有多华丽，而是客人、行李、员工、餐饮、卫生与景观能否各走各的路、又在恰当之处相遇。",
    "summary": "这本合刊的价值，在于把酒店从“度假的背景”还原成运行中的建筑。先用到达与公共空间建立方向，再让客房重复形成效率，最后把服务流线和景观路径藏进同一套平面规则里，酒店才能在高峰期仍然从容。",
    "concepts": ["先分开四类流线", "再安排公共层级", "最后把房间接上景观"],
    "takeaways": [
        "把客人、行李、后勤和员工先画成四条独立路径；它们只在需要交接的地方相遇，前台才不会变成交通堵点。",
        "大堂、餐厅、露台和走廊需要递进，而不是同样开敞。每一次转折都应给人选择停留、观察或绕开的机会。",
        "客房标准化应服务采光、通风、视野与清洁维护；重复单元越多，越要让朝向、窗台和外廊回答场地条件。",
    ],
    "publish_title": "CASABELLA125-126｜住与行",
    "publish_body": "Casabella-Costruzioni 125–126 是一本完整的酒店专题。它最值得今天重读的地方，不是怀旧式的度假想象，而是把酒店当作一套精密运转的空间系统：客人怎样抵达，行李怎样进入，服务人员如何不打扰客房，公共空间怎样与景观相连。\n\n杂志选取海滨、城市、山地和疗养型酒店，反复证明同一件事：酒店的形式不应先于运营。客房可以高效重复，但入口、大堂、餐厅、露台、垂直交通和后勤必须形成不同速度的空间层级。\n\n今天做酒店也一样。先把客人、行李、后勤和员工的路线拆开；再让公共空间有停留而非只可通过；最后用朝向、外廊与露台把每个房间接回具体景观。真正好的酒店，让高峰期依然不显拥挤。",
    "tags": "#Casabella #酒店设计 #建筑设计 #空间设计 #度假酒店 #建筑历史 #公共空间 #建筑流线",
    "cards": [
        {
            "image": "02-gooiland-entrance.jpg", "mode": "photo", "accent": "#c56a3c", "focal": (0.50, 0.48),
            "source": "Giuseppe Pagano｜Disposizioni per l’attrezzamento dei nuovi alberghi｜Casabella-Costruzioni 125–126",
            "eyebrow": "观点 01｜酒店先是一台处理抵达的机器",
            "title": "把下车、进门、寄存、办理入住和上楼拆成连续节点，大堂才不会在高峰时变成一团人流",
            "body": "入口雨棚只是开始。真正有效的抵达系统要让车、人、行李和前台各有缓冲位置：门厅给方向，寄存与接待从主通道退开，垂直交通在视线可及却不阻塞的位置出现。",
        },
        {
            "image": "03-latitude43-landscape.jpg", "mode": "photo", "accent": "#3d7890", "focal": (0.50, 0.46),
            "source": "I. Diotallevi、F. Marescotti｜Alberghi di città e di soggiorno｜Casabella-Costruzioni 125–126",
            "eyebrow": "观点 02｜度假酒店要顺着场地分层",
            "title": "把公共层放在抵达与景观之间，让客房沿地形退开；每一次下行都应换来更安静的视野",
            "body": "海岸或山坡酒店不需要先造一个完整方盒再切窗。让入口接近道路，把餐厅、露台和泳池放在风景最好的中段，再把客房拉成长条或错层单元，私密性与景观才能同时成立。",
        },
        {
            "image": "04-latitude43-plan.jpg", "mode": "document", "accent": "#728056",
            "source": "Gio Ponti、Guglielmo Ulrich｜Alberghi per lido tirrenico e adriatico｜Casabella-Costruzioni 125–126",
            "eyebrow": "观点 03｜公共空间必须有层级",
            "title": "从门厅到露台不该只有一条走廊：用转角、外廊和半室外空间把经过变成停留",
            "body": "酒店最容易把所有人塞进同一条水平通道。更好的做法是让门厅负责分流，公共厅承担相遇，露台接住停留，外廊连接房间与景色；人在不同距离上都能找到合适的速度。",
        },
        {
            "image": "05-latitude43-exterior.jpg", "mode": "photo", "accent": "#c56a3c", "focal": (0.52, 0.42),
            "source": "BBPR｜Alberghi per Pila in Valle d’Aosta｜Casabella-Costruzioni 125–126",
            "eyebrow": "观点 04｜重复客房不等于单调立面",
            "title": "把客房做成稳定模块，再用阳台、窗洞和外廊回应朝向与气候；重复才能既高效又有差别",
            "body": "酒店客房需要重复，才能控制管线、清洁和施工，但重复不该抹掉场地。朝向好的房间可以获得更深的阳台，转角承担公共视野，服务端保持紧凑；一套模块便能适应不同的光、风与景观。",
        },
        {
            "image": "06-gooiland-historic.jpg", "mode": "photo", "accent": "#3d7890", "focal": (0.50, 0.46),
            "source": "Jan Duiker｜Grand Hotel Gooiland, Hilversum｜Casabella-Costruzioni 125–126",
            "eyebrow": "观点 05｜把城市界面做成可停留的前场",
            "title": "临街首层不只负责进入：雨棚、门廊和窗边座位要为等候、相遇与短暂停留留出厚度",
            "body": "城市酒店没有大片风景可借，就要把街道变成第一层公共空间。让门厅后退形成遮蔽，临街窗与餐饮空间保持可见，入口前留出短停和会面位置，酒店才会从孤立建筑变成城市日常的一部分。",
        },
        {
            "image": "07-latitude43-drawing.jpg", "mode": "document", "accent": "#728056",
            "source": "Georges-Henri Pingusson｜Hôtel Latitude 43｜Casabella-Costruzioni 125–126",
            "eyebrow": "观点 06｜把服务藏进与客人平行的系统",
            "title": "客房走廊、清洁补给和餐饮后勤可以并行，却不必互相穿过；酒店的从容来自后台的独立路线",
            "body": "客人看到的安静，来自看不见的组织。把布草、垃圾、送餐、设备和员工入口放进独立的竖向与水平路径，再在客房层设置简短交接点，公共空间就不会被服务车和后勤门不断打断。",
        },
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 125–126 原刊封面，1938年5–6月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/125_126-em.jpg",
        "`02-gooiland-entrance.jpg`｜Jan Duiker，Grand Hotel Gooiland，Hilversum，1936，历史入口照片；作为合刊酒店抵达系统的同期案例图｜Gooiland Events｜https://gooilandevents.nl/app/uploads/2021/03/Zwart-wit-foto-Gooiland-1-1.jpeg",
        "`03-latitude43-landscape.jpg`｜Georges-Henri Pingusson，Hôtel Latitude 43，Saint-Tropez，1930–1932｜Arquitectura y Empresa｜https://arquitecturayempresa.es/sites/default/files/content/arquitectura_pingusson_latitude_43_cite_11.jpg",
        "`04-latitude43-plan.jpg`｜Georges-Henri Pingusson，Hôtel Latitude 43，总平面、照片与图纸｜Institut für aktuelle Kunst｜https://institut-aktuelle-kunst.de/uploads/kuenstlerfotos/P/Pingusson_Georges_Henri/_large/pingusson030.jpg",
        "`05-latitude43-exterior.jpg`｜Georges-Henri Pingusson，Hôtel Latitude 43，历史照片｜Grande Masse des Beaux-Arts｜https://www.grandemasse.org/PREHISTOIRE/Multimedia/Public_documents/Blog/Filiation-Atelier-Libre-Architecture-Pingusson/PROJET_Latitude-43_3.jpg",
        "`06-gooiland-historic.jpg`｜Jan Duiker，Grand Hotel Gooiland，Hilversum，1936，历史街景照片｜Gooiland Events｜https://gooilandevents.nl/app/uploads/2021/04/1936-Geschiedenis-Gooiland-Evenementenlocatie-Hilversum.jpg",
        "`07-latitude43-drawing.jpg`｜Georges-Henri Pingusson，Hôtel Latitude 43，建筑透视图｜d’architectures｜https://www.darchitectures.com/images/Darchitectures/da-v1/03893_058_FFFFFFFF866E332A.jpg",
        "合刊目录与主题｜酒店专题合刊，Casabella-Costruzioni 125–126，1938年5–6月；含1张折页、插图、平面、立面与图纸｜AbeBooks｜https://www.abebooks.com/magazines-periodicals/Casabella-Costruzioni-125-126-Editoriale-Domus/31187230552/bd",
        "文章目录与案例｜G. Pagano《Disposizioni per l’attrezzamento dei nuovi alberghi》；I. Diotallevi、F. Marescotti《Alberghi di Città, Alberghi di Soggiorno e di Villeggiatura, Alberghi a piccoli Appartamenti, Alberghi di Cura》pp.58–61；合刊含 Ponti、Ulrich、BBPR、Daneri、Duiker、Pingusson 等酒店案例｜Università di Bologna 研究论文｜https://amsdottorato.unibo.it/id/eprint/6275/1/Ori_Eva_tesi.pdf",
    ],
}


def save_rgb(image: Image.Image, path: Path) -> Path:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def source_line(draw: ImageDraw.ImageDraw, text: str, y: int, color: str = INK) -> None:
    draw.line((68, y - 18, 1174, y - 18), fill=rgba(color, 88), width=2)
    draw_fit(draw, (68, y), text, 1088, 48, 21, rgba(color, 180), spacing=5)


def make_cover(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#f0e6d2"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 34), fill="#203b46")
    draw.rectangle((0, 1010, W, H), fill="#e4c995")
    for x in range(0, W + 160, 160):
        draw.arc((x - 210, 620, x + 260, 1080), 205, 335, fill=rgba("#3d7890", 128), width=4)
    draw.text((68, 72), cfg["issue"], font=font(FONT_BOLD, 25), fill=INK)
    draw.text((1170, 74), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(INK, 180), anchor="ra")
    draw.text((68, 154), "单期主线", font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (68, 225), cfg["question"], 460, 480, 52, INK, serif=True, spacing=17)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
    mount(canvas, cover, (665, 148, 450, 730), True)
    draw.rectangle((665, 924, 450 + 665, 944), fill=accent)
    draw_fit(draw, (68, 1090), cfg["thesis"], 1050, 290, 38, INK, serif=True, spacing=14)
    source_line(draw, "Casabella-Costruzioni｜第125–126期原刊封面｜1938年5–6月", 1510)
    page_mark(draw, 1, False)
    return save_rgb(canvas, out / "01.jpg")


def make_summary(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#203b46"))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    header(draw, cfg, 8, True)
    draw.rectangle((0, 132, W, 154), fill=accent)
    draw.text((68, 190), "酒店是一套空间运营系统", font=font(FONT_BOLD, 28), fill="#f3e9d7")
    draw_fit(draw, (68, 260), cfg["summary"], 1050, 255, 47, "#f3e9d7", serif=True, spacing=16)
    colors = ["#c56a3c", "#3d7890", "#728056"]
    ys = [690, 940, 1190]
    for idx, (y, label, body, color) in enumerate(zip(ys, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.rectangle((68, y, 1174, y + 190), fill=rgba("#f0e6d2", 248))
        draw.rectangle((68, y, 218, y + 190), fill=color)
        draw.text((143, y + 69), f"0{idx}", font=font(FONT_BOLD, 45), fill="#f3e9d7", anchor="mm")
        draw.text((260, y + 37), label, font=font(FONT_BOLD, 34), fill="#203b46")
        draw.line((260, y + 98, 1125, y + 98), fill=rgba("#203b46", 72), width=2)
        draw_fit(draw, (260, y + 120), body, 828, 53, 27, rgba(INK, 220), serif=True, spacing=8)
    source_line(draw, "Casabella-Costruzioni｜第125–126期酒店专题｜1938年5–6月", 1508, "#f3e9d7")
    page_mark(draw, 8, True)
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
    paths = [make_cover(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(make_summary(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards, preview and publishing files in {out}")


if __name__ == "__main__":
    render_issue(CFG)
