from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    FONT_BOLD, FONT_SANS, H, INK, LIGHT, PAPER, ROOT, W,
    draw_fit, font, header, make_card, make_preview, mount, page_mark, rgba,
)


CFG = {
    "slug": "casabella-129",
    "issue": "CASABELLA-COSTRUZIONI 129",
    "date": "SETTEMBRE 1938 | ANNO X",
    "date_cn": "1938年9月",
    "cover": "book-cover.jpg",
    "accent": "#557c63",
    "dark": "#203c45",
    "question": "建筑不是把健康设备塞进平面；它先要让日照、通风、步行与停留各有位置。",
    "thesis": "第129期用 BBPR 的 Legnano 日光疗养院、Palanti 的住宅和 Aalto 专题，追问同一件事：当结构变轻、界面变薄，建筑能否把光、空气和集体生活带回身体尺度。",
    "summary": "129期的价值不在“疗愈风格”，而在于把健康拆成可以设计的空间条件：朝向决定日照，廊道调节步行，玻璃连接室内与树影，结构释放可用的公共空间。好的健康建筑，让身体在不同速度里都能靠近空气与光。",
    "concepts": ["把太阳当成程序", "让边界保持呼吸", "用轻结构留出空地"],
    "takeaways": [
        "先标记一天中需要日照、阴影与通风的位置，再安排体量与开口；采光不是事后补窗，而是平面的起点。",
        "把走廊、雨棚、露台做成室内外之间可停留的厚边界，让人可以慢下来、避风、看树或接近阳光。",
        "结构越轻，越要把释放出的空间交给使用：庭院、草地、外廊和公共厅应成为日常活动，而不只是建筑的背景。",
    ],
    "publish_title": "CASABELLA129｜建筑如何疗愈",
    "publish_body": "Casabella-Costruzioni 129 最动人的地方，是它没有把健康理解成医院设备或白色外墙。BBPR 的 Legnano 日光疗养院把疗养变成一套空间程序：孩子穿过有遮蔽的路径，到面向草地的餐厅、露台和日光区；玻璃、屋檐和柱子共同调节光、风与停留。\n\n同一期里，Aalto 的建筑被放进讨论，提醒我们：面向太阳的体量、可呼吸的外廊和对身体友好的细部，是现代建筑最具体的公共性。幼儿园案例则把这件事缩小到儿童尺度——庭院、光线和游戏不应排在教室之后。\n\n今天设计“健康空间”，不妨少问一点风格，多问三个问题：哪里能晒到太阳？哪里能躲雨、停下和看出去？释放出的结构空间，最后交给谁使用？你最想在建筑里多拥有哪一种身体感受？",
    "tags": "#Casabella #健康建筑 #疗愈空间 #BBPR #AlvarAalto #建筑历史 #空间设计 #现代建筑",
    "cards": [
        {"image":"02-bbpr-exterior.jpg","mode":"photo","accent":"#557c63","focal":(0.52,0.47),"source":"Pica｜Legnano 日光疗养院｜Casabella 129","eyebrow":"观点 01｜疗养从走到阳光里开始","title":"把主楼、露台与草地排成连续序列，让孩子从进入建筑起就能逐步接近空气、光和活动","body":"BBPR 没有把疗养院做成封闭盒子。不同功能分成清楚体量，由有遮蔽的路径连接；人能在室内、檐下和室外之间逐步切换，治疗因此成为一天的日常节奏。"},
        {"image":"03-bbpr-dining.jpg","mode":"photo","accent":"#d5a34c","focal":(0.50,0.50),"source":"Pica｜Legnano 日光疗养院｜Casabella 129","eyebrow":"观点 02｜集体空间要面向光","title":"餐厅不必只是一间大房：让用餐面向日照与远景，集体活动才能同时拥有方向、尺度和舒适感","body":"长桌、挑高和侧向开口把人群组织在同一视野里。健康空间的关键不是把人数压缩进最小面积，而是让光线、视线和声音在大集体中仍然可被身体辨认。"},
        {"image":"04-bbpr-light.jpg","mode":"photo","accent":"#557c63","focal":(0.50,0.54),"source":"Pica｜Legnano 日光疗养院｜Casabella 129","eyebrow":"观点 03｜用边界调节光而非隔绝光","title":"墙、格栅与窗带可以一起过滤阳光：既把室内打开给草地，也避免人被直接暴露在强光中","body":"真正有效的采光不是整面玻璃。把支撑、遮阳与开口组合成有厚度的边界，光线会被导入、反射和减弱；室内既明亮，也保有适合停留的阴影。"},
        {"image":"05-bbpr-glasshall.jpg","mode":"photo","accent":"#d5a34c","focal":(0.48,0.48),"source":"Pica｜Legnano 日光疗养院｜Casabella 129","eyebrow":"观点 04｜玻璃要让公共厅连到树影","title":"当整面开口对准庭院，室内活动会自然拥有外部参照；人不需要离开建筑，也能感觉到天气与时间","body":"公共厅的价值在于把集体生活与外部环境并置。透明界面延长视线，细柱释放边角，桌椅沿着光线排开；树、风和人的移动成为室内体验的一部分。"},
        {"image":"08-paimio.jpg","mode":"photo","accent":"#557c63","focal":(0.52,0.48),"source":"A. M. Mazzucchelli｜Alvar Aalto｜Casabella 129","eyebrow":"观点 05｜朝向是一种照护","title":"把病房翼朝向稳定日照，把休息露台交给空气和景观；治疗建筑首先要给身体一个可呼吸的方向","body":"Aalto 的 Paimio 疗养院将不同功能拆成相连的翼：病房、公共活动与服务各有位置。体量与开口不追求抽象纯粹，而是围绕日照、通风、安静与休息重新排列。"},
        {"image":"07-cattaneo-plan.jpg","mode":"document","accent":"#d5a34c","source":"Cattaneo、Origoni｜Garbagnati 幼儿园｜Casabella 129","eyebrow":"观点 06｜儿童空间要从庭院展开","title":"把教室、游戏与户外空地拉成可往返的日常路径，儿童才不是被安置在小房间里，而是在环境中学习","body":"幼儿园的平面不应只追求教室数量。入口、活动室、卫生与庭院要短距离相接；孩子能随时看见光、树与同伴，身体活动才会成为空间组织的核心。"},
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 129 原刊封面，1938年9月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/129-nz.jpg",
        "`02-bbpr-exterior.jpg`｜BBPR，Legnano 日光疗养院南立面，历史照片（研究论文第4页裁切）｜Proyecto, Progreso, Arquitectura｜https://revistascientificas.us.es/index.php/ppa/article/download/114/127/0｜许可待商业发布前复核｜裁切与文字排版",
        "`03-bbpr-dining.jpg`｜BBPR，Legnano 日光疗养院餐厅，历史照片（研究论文第5页裁切）｜Proyecto, Progreso, Arquitectura｜https://revistascientificas.us.es/index.php/ppa/article/download/114/127/0｜许可待商业发布前复核｜裁切与文字排版",
        "`04-bbpr-light.jpg`｜BBPR，Legnano 日光疗养院室内，历史照片（研究论文第5页裁切）｜Proyecto, Progreso, Arquitectura｜https://revistascientificas.us.es/index.php/ppa/article/download/114/127/0｜许可待商业发布前复核｜裁切与文字排版",
        "`05-bbpr-glasshall.jpg`｜BBPR，Legnano 日光疗养院面向草地的餐厅，历史照片（研究论文第5页裁切）｜Proyecto, Progreso, Arquitectura｜https://revistascientificas.us.es/index.php/ppa/article/download/114/127/0｜许可待商业发布前复核｜裁切与文字排版",
        "`08-paimio.jpg`｜Alvar Aalto，Paimio 疗养院，Leon Liao 摄影，CC BY 2.0｜Archweb｜https://www.archweb.it/dwg/arch_arredi_famosi/Alvar_aalto/sanatorio_paimio/photos/Paimio_Sanatorium_1.jpg｜裁切与文字排版",
        "`07-cattaneo-plan.jpg`｜Cesare Cattaneo、Mario Origoni，Giuseppe Garbagnati 幼儿园图纸｜Archivio Cattaneo｜https://www.cesarecattaneo.com/asilo-infantile-giuseppe-garbagnati-1935/｜许可待商业发布前复核｜裁切与文字排版",
        "目录核验｜第129期含 Pagano《Variazioni sull’autarchia architettonica》《Estetica delle strutture sottili》、Pica《Una colonia elioterapica》、Giolli《Una villa a Livorno》与 Mazzucchelli《Alvar Aalto》｜Casa dell’Architettura Latina｜https://www.casadellarchitettura.eu/collezioni/riviste/casabella-costruzioni/",
        "BBPR 期刊文章核验｜Agnoldomenico Pica《Una colonia elioterapica degli architetti Banfi, Belgioioso, Rogers e Peressutti》，Casabella-Costruzioni 129，1938年9月，pp.4–11｜Proyecto, Progreso, Arquitectura｜https://revistascientificas.us.es/index.php/ppa/article/download/114/127/0",
    ],
}


def save_rgb(image: Image.Image, path: Path) -> Path:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def source_line(draw: ImageDraw.ImageDraw, text: str, y: int, color: str = INK) -> None:
    draw.line((68, y - 18, 1174, y - 18), fill=rgba(color, 82), width=2)
    draw_fit(draw, (68, y), text, 1088, 44, 20, rgba(color, 175), spacing=5)


def make_cover(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#f1eadb"))
    draw = ImageDraw.Draw(canvas)
    dark, accent = cfg["dark"], cfg["accent"]
    draw.rectangle((0, 0, W, 34), fill=dark)
    draw.text((68, 76), cfg["issue"], font=font(FONT_BOLD, 24), fill=dark)
    draw.text((1170, 77), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(dark, 180), anchor="ra")
    draw.text((68, 159), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (68, 225), cfg["question"], 1025, 190, 57, dark, serif=True, spacing=16)
    draw.rectangle((68, 508, 1172, 524), fill=accent)
    for y in [610, 720, 830]:
        draw.line((68, y, 620, y), fill=rgba(accent, 110), width=3)
        draw.ellipse((608, y-9, 626, y+9), fill=accent)
    draw.text((68, 577), "光线 / 空气 / 行走 / 停留", font=font(FONT_BOLD, 26), fill=dark)
    draw_fit(draw, (68, 892), cfg["thesis"], 540, 300, 37, dark, serif=True, spacing=13)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.28)
    mount(canvas, cover, (696, 610, 398, 660), True)
    draw.rectangle((0, 1375, W, H), fill=dark)
    draw_fit(draw, (68, 1415), "健康不是风格；它来自可被身体感知的空间条件。", 1050, 90, 33, "#f1eadb", serif=True, spacing=10)
    source_line(draw, "Casabella-Costruzioni｜第129期原刊封面｜1938年9月", 1535, "#f1eadb")
    page_mark(draw, 1, True)
    return save_rgb(canvas, out / "01.jpg")


def make_summary(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(cfg["dark"]))
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, True)
    draw.rectangle((0, 130, W, 150), fill=cfg["accent"])
    draw.text((68, 206), "让身体在空间中得到方向", font=font(FONT_BOLD, 29), fill="#e9c86b")
    draw_fit(draw, (68, 282), cfg["summary"], 1060, 280, 48, "#f2eadc", serif=True, spacing=17)
    x, y, w, gap = 68, 655, 330, 42
    colors = [cfg["accent"], "#d5a34c", "#88a895"]
    for i, (label, body, color) in enumerate(zip(cfg["concepts"], cfg["takeaways"], colors), 1):
        left = x + (i - 1) * (w + gap)
        draw.rectangle((left, y, left + w, 712), fill=color)
        draw.text((left + 20, 744), f"0{i}", font=font(FONT_BOLD, 31), fill=color)
        draw_fit(draw, (left + 20, 800), label, w - 38, 130, 38, "#f2eadc", serif=True, spacing=12)
        draw.line((left + 20, 978, left + w - 20, 978), fill=rgba("#f2eadc", 90), width=2)
        draw_fit(draw, (left + 20, 1020), body, w - 38, 310, 29, rgba("#f2eadc", 220), serif=True, spacing=10)
    draw.line((68, 1434, 1174, 1434), fill=rgba("#f2eadc", 100), width=2)
    draw.text((68, 1464), "日照不是附加条件，而是空间的一部分。", font=font(FONT_BOLD, 30), fill="#e9c86b")
    source_line(draw, "Casabella-Costruzioni｜第129期健康与薄结构讨论｜1938年9月", 1530, "#f2eadc")
    page_mark(draw, 8, True)
    return save_rgb(canvas, out / "08.jpg")


def manifest(cfg: dict) -> dict:
    return {"type":"magazine","slug":cfg["slug"],"issue":cfg["issue"].title(),"date":cfg["date_cn"],"core_question":cfg["question"],"core_thesis":cfg["thesis"],"pages":[f"01 单期主线：{cfg['question']}", *[f"{i:02d} {c['source']}：{c['title']}" for i,c in enumerate(cfg["cards"],2)], f"08 总结：{'；'.join(cfg['concepts'])}"]}


def render() -> None:
    src, out = ROOT / "assets" / CFG["slug"], ROOT / "output" / CFG["slug"]
    out.mkdir(parents=True, exist_ok=True)
    paths = [make_cover(CFG, src, out)]
    paths += [make_card(CFG, src, out, i, card) for i, card in enumerate(CFG["cards"], 2)]
    paths.append(make_summary(CFG, out))
    make_preview(paths, out)
    (out / "发布文案.md").write_text(f"{CFG['publish_title']}\n\n{CFG['publish_body']}\n\n{CFG['tags']}\n", encoding="utf-8")
    (out / "图片来源.md").write_text(f"# {CFG['issue'].title()} 图片来源\n\n" + "\n".join(f"- {s}" for s in CFG["sources"]) + "\n", encoding="utf-8")
    post = ROOT / "posts" / CFG["slug"]
    post.mkdir(parents=True, exist_ok=True)
    (post / "post.json").write_text(json.dumps(manifest(CFG), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(paths)} cards in {out}")


if __name__ == "__main__":
    render()
