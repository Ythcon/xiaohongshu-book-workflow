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
        "slug": "casabella-111",
        "issue": "CASABELLA 111",
        "date": "MARZO 1937 · ANNO X",
        "date_cn": "1937年3月",
        "cover": "book-cover.jpg",
        "accent": "#bb573f",
        "question": "现代建筑，\n怎样用克制\n获得清晰？",
        "thesis_label": "结构 × 路径 × 使用",
        "thesis": "111期把住宅、城市单元、商业表皮、展馆与工业设施并置：清晰不是压低野心，而是让结构、路径和使用关系先于造型表演。",
        "summary": "当结构回应生产、住宅保留独立生活、公共界面解释人的移动，现代性才不依赖风格姿态，而成为一套清楚的空间关系。",
        "concepts": ["生产流线", "独立生活", "公共可读性"],
        "takeaways": [
            "先把运输、储存与设备顺序画清，工业建筑的体量会从流程中自然长出。",
            "提高密度时保留独立入口、露台与室外空间，住宅才不会只剩重复单元。",
            "让立面、楼梯与展馆曲线解释人的移动，公共性就能被直接看见。",
        ],
        "publish_title": "111期｜克制如何生成现代性",
        "publish_body": "Casabella 111把“现代”从外观问题拉回空间关系：建筑是否忠实回应生产流程、居住单元、人的移动和城市尺度，比形式是否新奇更重要。\n\n原刊扉页的工业设施把筒仓、高塔与连桥连成连续工序，生产流程直接成为建筑轮廓。Levi-Montalcini的都灵住宅以退台、悬挑和露台把室内生活延伸到户外；Diotallevi与Marescotti研究叠层别墅，则试图在提高密度时继续保留独立入口与花园。\n\nKysela的布拉格Baťa商店用连续玻璃界面向街道公开楼层活动；巴黎航空馆以弧形表皮组织参观流线。都灵Torre Littoria的施工照片更直接暴露出轻型钢框架：高层体量的现代性来自结构效率，而不是厚重纪念性。\n\n这期可以带走三个判断：让流程生成体量，让密度保留独立生活，让公共界面解释人的移动。你会先用哪一条重新检查自己的方案？",
        "tags": "#Casabella #建筑杂志 #GiuseppePagano #现代建筑 #住宅设计 #工业建筑 #建筑结构 #建筑史",
        "cards": [
            {
                "image": "02-industrial-frontispiece.jpg",
                "mode": "photo",
                "accent": "#3f7591",
                "focal": (0.55, 0.53),
                "source": "Fausto Masi｜Fabbricati industriali (II)｜Casabella 111",
                "eyebrow": "观点 01｜流程可以直接生成体量",
                "title": "高塔、筒仓与连桥，把生产顺序变成建筑轮廓",
                "body": "垂直提升、集中储存与水平转运分别对应高塔、筒仓和连桥。工业建筑的形态来自设备与物流关系，而不是额外造型。",
            },
            {
                "image": "03-villa-lanfranco-gromo.jpg",
                "mode": "photo",
                "accent": "#bb573f",
                "focal": (0.52, 0.48),
                "source": "Gino Levi-Montalcini｜Villa Lanfranco-Gromo, Torino｜Casabella 111",
                "eyebrow": "观点 02｜小住宅也能拥有连续室外生活",
                "title": "退台、悬挑与露台，把室内空间逐层推向花园",
                "body": "体量没有被压成完整盒子，而是用阳台、雨棚和转折界面形成层层过渡；有限面积因此获得更多采光、遮蔽与停留位置。",
            },
            {
                "image": "04-citta-orizzontale.jpg",
                "mode": "document",
                "accent": "#6e816f",
                "source": "I. Diotallevi / F. Marescotti｜Un quartiere d’abitazione a ville sovrapposte｜Casabella 111",
                "eyebrow": "观点 03｜密度不必取消独立生活",
                "title": "把地面与花园抬到不同标高，让叠层住宅仍有独立入口",
                "body": "重复剖面把每户的室外空间错层布置，减少公共走廊依赖。密度通过垂直叠合提高，住宅仍保持接近独立别墅的进入与户外关系。",
            },
            {
                "image": "05-bata-prague.jpg",
                "mode": "photo",
                "accent": "#3f7591",
                "focal": (0.50, 0.48),
                "source": "Ludvík Kysela｜Obchodní dům Baťa, Praha｜Casabella 111",
                "eyebrow": "观点 04｜商业立面可以公开内部活动",
                "title": "连续玻璃带把楼层、商品与街道视线接在一起",
                "body": "规则柱网释放外墙，水平玻璃带让不同楼层保持可见。商店不再依赖厚重门面，而以内部活动本身形成城市识别。",
            },
            {
                "image": "06-pavillon-aeronautique.jpg",
                "mode": "document",
                "accent": "#bb573f",
                "source": "Raffaello Giolli｜I padiglioni francesi alla Mostra di Parigi｜Casabella 111",
                "eyebrow": "观点 05｜展馆外形应提示参观方式",
                "title": "连续弧面把转向、进入与观看压成一条可读路径",
                "body": "圆角体量、水平开口与入口退让共同引导人流。曲线不是装饰，它把快速通过的街道视线转成逐步靠近展品的参观过程。",
            },
            {
                "image": "07-torre-littoria.jpg",
                "mode": "photo",
                "accent": "#6e816f",
                "focal": (0.50, 0.44),
                "source": "Armando Melis / Giovanni Bernocco｜Torre Littoria, Torino｜Casabella 111",
                "eyebrow": "观点 06｜结构轻量化改变城市高层",
                "title": "钢框架先建立垂直秩序，再让薄围护完成城市界面",
                "body": "施工中的塔楼清楚分开承重骨架与外围护。高层不必依靠厚墙制造重量感，结构效率本身就能形成新的尺度与轮廓。",
            },
        ],
    },
    {
        "slug": "casabella-112",
        "issue": "CASABELLA 112",
        "date": "APRILE 1937 · ANNO X",
        "date_cn": "1937年4月",
        "cover": "book-cover.jpg",
        "accent": "#c45a3f",
        "question": "低成本，\n怎样不牺牲\n空间质量？",
        "thesis_label": "经济 × 结构 × 环境",
        "thesis": "112期把超低成本住宅、水晶宫、学校、工业建筑与环境技术放在一起：经济性不是削减空间，而是用重复构件、清楚流线和环境性能减少浪费。",
        "summary": "真正的经济性，不是把面积和材料一减再减，而是让构件可重复、服务可共享、围护连续有效，把有限资源转成稳定的日常空间。",
        "concepts": ["重复系统", "共享服务", "环境性能"],
        "takeaways": [
            "用标准构件和规则柱网降低制造复杂度，同时保留采光、通风与可变使用。",
            "把托育、洗衣和交通空间作为组团骨架，不能只计算单户面积与造价。",
            "让保温层跨过梁柱节点并连续闭合，运行成本才不会被热桥重新吞掉。",
        ],
        "publish_title": "112期｜低成本也能有空间质量",
        "publish_body": "Casabella 112追问的不是怎样把建筑做得更便宜，而是怎样把有限资源转成更稳定的空间质量。答案分布在住宅、展览、学校、工厂和环境技术之间。\n\nFIAT汽车仓库用大跨屋架、高侧窗和连续地坪容纳密集车辆，结构与流线同时工作。博洛尼亚“Popolarissime”住宅以重复街区和共享服务压低单户负担，却也暴露封闭组团、集中管理和城市隔离的问题：经济性不能只看造价。\n\n水晶宫用标准铁构件和玻璃模块快速装配出巨大公共空间；学校方案则把朝向、庭院和短走廊放在纪念性入口之前。Lingotto工厂进一步把生产线沿楼层推进，并在屋顶完成试车。保温文章提醒，建造阶段省下的材料，可能在梁柱热桥与长期能耗中加倍偿还。\n\n这期最值得保留的三条方法是：构件可重复、服务可共享、围护要连续。你认为低成本项目最容易忽略哪一项？",
        "tags": "#Casabella #建筑杂志 #低成本住宅 #公共建筑 #工业建筑 #学校设计 #建筑节能 #建筑史",
        "cards": [
            {
                "image": "02-fiat-depot.jpg",
                "mode": "photo",
                "accent": "#c45a3f",
                "focal": (0.56, 0.56),
                "source": "Fausto Masi｜Fabbricati industriali · Deposito auto FIAT｜Casabella 112",
                "eyebrow": "观点 01｜大空间先解决结构与流线",
                "title": "大跨屋架与高侧窗，让密集停车仍保持连续光线",
                "body": "细密屋架跨过无柱地坪，高侧窗把自然光送入深处；车辆可以成排进入、停放和转向，结构节奏直接服务物流效率。",
            },
            {
                "image": "03-case-popolarissime.webp",
                "mode": "photo",
                "accent": "#6e816f",
                "focal": (0.52, 0.54),
                "source": "Giuseppe Pagano｜Le case “popolarissime”｜Casabella 112",
                "eyebrow": "观点 02｜共享服务不能替代城市连接",
                "title": "封闭组团能集中托育与洗衣，也可能把低价住宅推向隔离",
                "body": "重复住宅围合内部空间，托育、洗衣与门房被集中管理。单位成本降低了，但封闭边界与远离主街的位置也放大了社会分隔。",
            },
            {
                "image": "04-crystal-palace-interior.jpg",
                "mode": "photo",
                "accent": "#3f7591",
                "focal": (0.52, 0.46),
                "source": "Giulia Veronesi｜Il Palazzo di Cristallo｜Casabella 112",
                "eyebrow": "观点 03｜标准化可以制造宏大公共空间",
                "title": "重复铁构件与玻璃模块，把巨大展厅变成装配系统",
                "body": "统一开间控制柱、梁与玻璃尺寸，构件可预制、运输和快速安装。宏大尺度不再依赖厚重材料，而来自小构件的连续重复。",
            },
            {
                "image": "05-asilo-santelia.jpg",
                "mode": "photo",
                "accent": "#c45a3f",
                "focal": (0.50, 0.50),
                "source": "F. Albini / A. Benko / P. Clausetti / G. Romano｜Tre progetti di scuole｜Casabella 112",
                "eyebrow": "观点 04｜学校从日常使用生成秩序",
                "title": "教室朝向、庭院与短走廊，比纪念性入口更重要",
                "body": "教室作为可重复单元优先获得采光和通风，再由庭院连接户外活动。缩短年级之间的路径，比制造正面轴线更接近真实学习生活。",
            },
            {
                "image": "06-lingotto-1928.jpg",
                "mode": "photo",
                "accent": "#6e816f",
                "focal": (0.52, 0.52),
                "source": "Fausto Masi｜Fabbricati industriali｜Casabella 112",
                "eyebrow": "观点 05｜生产顺序可以贯穿整座建筑",
                "title": "生产线沿楼层上升，屋顶试车道成为流程终点",
                "body": "原料从底层进入，车辆随装配过程逐层移动，最终在屋顶完成测试。建筑剖面不是容器，而是生产流程的立体展开。",
            },
            {
                "image": "07-thermal-section.png",
                "mode": "document",
                "accent": "#3f7591",
                "source": "Francesco Marescotti｜Il problema dell’isolamento termico nell’ambiente｜Casabella 112",
                "eyebrow": "观点 06｜节能取决于围护的连续性",
                "title": "保温连续跨过梁柱，室内表面温度才稳定",
                "body": "墙体中段的保温再厚，只要在梁柱处中断，热量仍会沿结构快速外泄。连续包覆能同时降低能耗、冷表面与结露风险。",
            },
        ],
    },
]


def save_rgb(image: Image.Image, path: Path) -> None:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)


def crop_frontispiece(source: Path, target: Path, issue: str) -> None:
    image = Image.open(source).convert("RGB")
    if issue == "CASABELLA 111":
        box = (round(image.width * 0.27), round(image.height * 0.20), round(image.width * 0.97), round(image.height * 0.98))
    else:
        box = (round(image.width * 0.27), round(image.height * 0.22), round(image.width * 0.98), round(image.height * 0.98))
    crop = ImageEnhance.Sharpness(image.crop(box)).enhance(1.18)
    crop.save(target, quality=96, subsampling=0)


def make_thermal_section(path: Path) -> None:
    image = Image.new("RGB", (1500, 980), LIGHT)
    draw = ImageDraw.Draw(image)
    blue = "#3f7591"
    red = "#c45a3f"
    gray = "#a9a49b"

    draw.rectangle((0, 0, 310, 980), fill=blue)
    draw.rectangle((1170, 0, 1500, 980), fill="#e8b765")
    draw.text((76, 76), "室外低温", font=font(FONT_BOLD, 44), fill=LIGHT)
    draw.text((1240, 76), "室内", font=font(FONT_BOLD, 44), fill=INK)

    draw.rectangle((430, 90, 520, 890), fill="#d7d2c8")
    draw.rectangle((520, 90, 610, 890), fill=red)
    draw.rectangle((610, 90, 965, 890), fill=gray)
    draw.rectangle((965, 90, 1018, 890), fill="#ded9cf")
    draw.rectangle((610, 426, 1170, 610), fill="#8e8a83")
    draw.rectangle((520, 426, 610, 610), fill=red)

    draw.line((565, 115, 565, 865), fill=LIGHT, width=5)
    draw.text((565, 830), "保温层", font=font(FONT_BOLD, 27), fill=LIGHT, anchor="ms")
    draw.text((740, 500), "梁板节点", font=font(FONT_BOLD, 34), fill=LIGHT)

    for y in (250, 705):
        draw.line((1100, y, 350, y), fill="#f08b55", width=12)
        draw.polygon([(350, y), (392, y - 26), (392, y + 26)], fill="#f08b55")
    draw.text((760, 190), "热量沿围护向外传递", font=font(FONT_BOLD, 34), fill=INK, anchor="mm")
    draw.text((760, 920), "节点不断开，热桥才不会穿透", font=font(FONT_BOLD, 34), fill=INK, anchor="mm")
    image.save(path)


def prepare_assets(cfg: dict, src: Path) -> None:
    if cfg["issue"] == "CASABELLA 111":
        crop_frontispiece(src / "02-original-frontispiece.jpg", src / "02-industrial-frontispiece.jpg", cfg["issue"])
    else:
        crop_frontispiece(src / "02-original-frontispiece.jpg", src / "02-fiat-depot.jpg", cfg["issue"])
        make_thermal_section(src / "07-thermal-section.png")


def make_cover_111(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(11101)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((840, 0, W, H), fill=rgba(BLUE))
    draw.text((62, 58), cfg["issue"], font=font(FONT_BOLD, 30), fill=INK)
    draw.text((790, 64), cfg["date"], font=font(FONT_SANS, 19), fill=MUTED, anchor="ra")

    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (62, 142, 730, 790), True)

    draw.text((894, 150), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (894, 230), cfg["question"], 286, 570, 52, LIGHT, serif=True, spacing=16)
    draw.line((894, 866, 1164, 866), fill=rgba(LIGHT, 80), width=2)
    draw.text((894, 906), "GIUSEPPE PAGANO", font=font(FONT_SANS, 18), fill=rgba(LIGHT, 180))

    draw.rectangle((62, 1010, 792, 1020), fill=accent)
    draw.text((62, 1066), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (62, 1125), cfg["thesis"], 730, 290, 34, INK, serif=True, spacing=14)
    draw.text((62, 1510), "Giuseppe Pagano｜Casabella 111｜Marzo 1937", font=font(FONT_SANS, 18), fill=MUTED)
    page_mark(draw, 1, True)

    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_cover_112(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(11201)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 470), fill=rgba(BLUE))
    draw.text((70, 52), cfg["issue"], font=font(FONT_BOLD, 28), fill=LIGHT)
    draw.text((1172, 58), cfg["date"], font=font(FONT_SANS, 19), fill=rgba(LIGHT, 185), anchor="ra")
    draw.text((70, 128), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (70, 186), cfg["question"], 950, 245, 68, LIGHT, serif=True, spacing=10)

    draw.text((70, 570), cfg["thesis_label"], font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (70, 640), cfg["thesis"], 410, 410, 37, INK, serif=True, spacing=14)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (540, 520, 640, 700), True)

    draw.line((70, 1304, 1172, 1304), fill=rgba(INK, 58), width=2)
    draw_fit(draw, (70, 1355), "经济性不是压缩体验，而是减少系统中的浪费。", 1060, 120, 38, BLUE, serif=True, spacing=10)
    draw.text((70, 1520), "Giuseppe Pagano｜Casabella 112｜Aprile 1937", font=font(FONT_SANS, 18), fill=MUTED)
    page_mark(draw, 1, False)

    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_summary_111(cfg: dict, out: Path) -> Path:
    canvas = paper_canvas(11108)
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, False)
    accent = cfg["accent"]

    draw.rectangle((74, 160, 86, 695), fill=accent)
    draw.text((122, 162), "清晰来自关系，不来自炫技", font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (122, 236), cfg["summary"], 1000, 390, 53, INK, serif=True, spacing=18)

    column_x = [74, 448, 822]
    colors = ["#3f7591", "#bb573f", "#6e816f"]
    for idx, (x, label, body, color) in enumerate(zip(column_x, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.line((x, 824, x, 1468), fill=color, width=8)
        draw.text((x + 28, 824), f"0{idx}", font=font(FONT_BOLD, 28), fill=color)
        draw.text((x + 28, 890), label, font=font(FONT_BOLD, 34), fill=INK)
        draw_fit(draw, (x + 28, 992), body, 310, 360, 29, rgba(INK, 215), serif=True, spacing=12)

    draw.text((74, 1518), "流程生成体量  ·  密度保留生活  ·  界面解释移动", font=font(FONT_BOLD, 24), fill=BLUE)
    page_mark(draw, 8, False)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def make_summary_112(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(BLUE))
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, True)
    accent = cfg["accent"]

    draw.text((72, 160), "经济性来自系统，不是删减", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (72, 232), cfg["summary"], 1080, 360, 51, LIGHT, serif=True, spacing=18)

    colors = ["#e4b359", "#c45a3f", "#80a099"]
    y_positions = [770, 1000, 1230]
    for idx, (y, label, body, color) in enumerate(zip(y_positions, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.line((72, y, 1170, y), fill=rgba(LIGHT, 55), width=2)
        draw.text((72, y + 48), f"0{idx}", font=font(FONT_BOLD, 48), fill=color)
        draw.text((188, y + 50), label, font=font(FONT_BOLD, 32), fill=LIGHT)
        draw_fit(draw, (440, y + 42), body, 700, 150, 27, rgba(LIGHT, 220), spacing=10)

    draw.line((72, 1495, 1170, 1495), fill=rgba(LIGHT, 65), width=2)
    draw.text((72, 1530), "构件可重复  →  服务可共享  →  围护要连续", font=font(FONT_BOLD, 25), fill=LIGHT)
    page_mark(draw, 8, True)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


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
            *[
                f"{number:02d} {card['source'].split('｜')[0]}：{card['title']}"
                for number, card in enumerate(cfg["cards"], 2)
            ],
            f"08 总结：{'—'.join(cfg['concepts'])}",
        ],
    }


def source_records(slug: str) -> str:
    if slug == "casabella-111":
        return """# Casabella 111 图片来源

- `book-cover.jpg`｜Casabella 111 官方历史封面｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/111-nz.jpg｜版权归原权利人；等比例放大，未改字。
- `02-original-frontispiece.jpg` / `02-industrial-frontispiece.jpg`｜Casabella 111 原刊 frontespizio，工业设施｜Trento大学图书馆数字馆藏｜https://webapps.unitn.it/Biblioteca/it/Web/EngibankFile/1937%20Casabella%20%5Bperiodico%5D%20111.pdf｜原刊扫描渲染、裁切、缩放；版权归原权利人。
- `03-villa-lanfranco-gromo.jpg`｜Gino Levi-Montalcini，Villa Lanfranco-Gromo，Torino，1936—1937｜Wright / Masterworks｜https://www.wright20.com/auctions/2017/11/masterworks/25｜裁切、缩放；版权与使用条件以原来源页为准。
- `04-citta-orizzontale.jpg`｜Irenio Diotallevi / Francesco Marescotti / Giuseppe Pagano，居住类型演化与水平城市研究图｜Vinicio Bonomètto / Flickr｜https://www.flickr.com/photos/viniciobonometto/4274543130/｜缩放、排版；该图为同一组作者后续居住研究，用于补充111期叠层住宅命题，版权与使用条件以原来源页为准。
- `05-bata-prague.jpg`｜Ludvík Kysela，Obchodní dům Baťa，Praha｜Modernism in Architecture｜https://modernism-in-architecture.org/buildings/department-store-obchodni-dum-bata/｜裁切、缩放；版权与使用条件以原来源页为准。
- `06-pavillon-aeronautique.jpg`｜1937巴黎国际博览会法国航空馆档案照片｜L’Art Nouveau｜https://lartnouveau.com/art_deco/expo_1937/pavillons_francais.htm｜缩放、排版；版权与使用条件以原来源页为准。
- `07-torre-littoria.jpg`｜Armando Melis de Villa / Giovanni Bernocco，Torre Littoria施工照片，1933—1934｜作者不详 / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:TorreLittoria_1934_costruzione.jpg｜Public Domain；裁切、缩放、排版。

本组用于建筑杂志内容整理与教育性发布；许可不明的图片不能默认用于商业投放，发布前请按所在地与平台规则复核。
"""
    return """# Casabella 112 图片来源

- `book-cover.jpg`｜Casabella 112 官方历史封面｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/112-nz.jpg｜版权归原权利人；等比例放大，未改字。
- `02-original-frontispiece.jpg` / `02-fiat-depot.jpg`｜Deposito auto della FIAT，Casabella 112 原刊 frontespizio｜Trento大学图书馆数字馆藏｜https://webapps.unitn.it/Biblioteca/it/Web/EngibankFile/1937%20Casabella%20%5Bperiodico%5D%20112.pdf｜原刊扫描渲染、裁切、缩放；版权归原权利人。
- `03-case-popolarissime.webp`｜Case popolarissime，via Pier Crescenzi，Bologna，1934｜Bologna rivista del Comune / Biblioteca Salaborsa｜https://www.bibliotecasalaborsa.it/bolognaonline/events/le_case_popolarissime｜裁切、缩放；版权与使用条件以原来源页为准。
- `04-crystal-palace-interior.jpg`｜J. McNeven，Crystal Palace interior，1851｜Victoria and Albert Museum / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Crystal_Palace_-_interior.jpg｜Public Domain Mark；裁切、缩放、排版。
- `05-asilo-santelia.jpg`｜Giuseppe Terragni，Asilo Sant’Elia，Como；摄影 Felice46｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Asilosantelia.jpg｜CC BY-SA 3.0 / GFDL；作为同期学校空间的案例参照，裁切、缩放、排版。
- `06-lingotto-1928.jpg`｜FIAT Lingotto工厂与屋顶试车道，1928；上传者 Dgtmedia - Simone｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Fiat_Lingotto_veduta-1928.jpg｜CC BY 3.0；裁切、缩放、排版。
- `07-thermal-section.png`｜连续外保温与梁板节点剖面｜依据 Francesco Marescotti《Il problema dell’isolamento termico nell’ambiente》整理｜Casabella 112｜自制技术插图；仅表达保温连续性与热桥原理。

本组用于建筑杂志内容整理与教育性发布；含CC许可图片的衍生排版按兼容许可分享，商业投放前请逐张复核许可与平台规则。
"""


def write_text_files(cfg: dict, out: Path) -> None:
    publish = f"{cfg['publish_title']}\n\n{cfg['publish_body']}\n\n{cfg['tags']}\n"
    (out / "发布文案.md").write_text(publish, encoding="utf-8")
    (out / "图片来源.md").write_text(source_records(cfg["slug"]), encoding="utf-8")

    post_dir = ROOT / "posts" / cfg["slug"]
    post_dir.mkdir(parents=True, exist_ok=True)
    (post_dir / "post.json").write_text(
        json.dumps(post_manifest(cfg), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def render_issue(cfg: dict) -> None:
    src = ROOT / "assets" / cfg["slug"]
    out = ROOT / "output" / cfg["slug"]
    out.mkdir(parents=True, exist_ok=True)
    prepare_assets(cfg, src)

    if cfg["slug"] == "casabella-111":
        paths = [make_cover_111(cfg, src, out)]
    else:
        paths = [make_cover_112(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(make_summary_111(cfg, out) if cfg["slug"] == "casabella-111" else make_summary_112(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards, preview and publishing files in {out}")


if __name__ == "__main__":
    for issue in ISSUES:
        render_issue(issue)
