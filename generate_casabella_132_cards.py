from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    FONT_BOLD, FONT_SANS, H, INK, LIGHT, PAPER, ROOT, W,
    cover_crop, draw_fit, font, mount, rgba,
)


CFG = {
    "slug": "casabella-132",
    "issue": "CASABELLA-COSTRUZIONI 132",
    "date": "DICEMBRE 1938 | ANNO XI",
    "date_cn": "1938年12月",
    "cover": "book-cover.jpg",
    "accent": "#557b55",
    "dark": "#172a28",
    "paper2": "#e9e7da",
    "question": "绿地不是开发之后才塞进楼缝的边角料；它必须先和道路、日照、住宅一起成为街区的骨架。",
    "thesis": "第132期以《Milano Verde》为核心：Pagano、Albini、Gardella、Minoletti、Palanti、Predaval、Romano为 Sempione—Fiera 提出一套绿色街区。正交网格不是图纸上的秩序感，而是让道路分级、住宅朝向、连续绿地和私有开发能够共存的规则。",
    "summary": "132期真正讨论的不是“多种一点树”，而是城市怎样先把绿地变成结构。明确的道路层级把穿越交通与居住内部区分开；重复但可调整的住区单元保证日照与空隙；连续开放面让零散开发仍能成为一个可步行的街区。",
    "concepts": ["绿地先于地块", "网格服务日照", "道路按速度分层"],
    "takeaways": [
        "先画出连续绿地、步行方向和公共服务的位置，再确定每个地块能建多少。绿地一旦只剩补缝，就无法承担连接与停留。",
        "用规则而非一模一样的楼型控制住区：朝向、楼间距与开口共享底线，建筑可以在这套底线内变化。",
        "把区域通行、街区进入和步行游走分开处理。车流能到达，但不需要占据每一条生活路径。",
    ],
    "publish_title": "CASABELLA132｜绿地不是边角料",
    "publish_body": "Casabella-Costruzioni 132 的《Milano Verde》把一个今天依然棘手的问题摆到台面上：绿地到底是开发完成后的装饰，还是城市生长的规则？\n\n1938 年，Pagano、Albini、Gardella、Minoletti、Palanti、Predaval 与 Romano 为米兰 Sempione—Fiera 区域提出方案。它不靠一座地标解决城市，而是用正交网格把道路分级、住宅日照、楼间空隙和连续绿地放在同一张图里。网格在这里不是僵硬的形式，而是一种协商工具：不同开发单元可以变化，却不必破坏街区的空气、视线与步行连续性。\n\n今天看这个方案，最值得带走的不是复古的总平面，而是顺序：先决定哪些地面必须向所有人开放，哪些路只负责通过，哪些楼间距保证光和风；再讨论建筑可以长成什么样。把绿地画在最后，往往也会被压缩在最后。你所在的街区，绿地是骨架还是余量？",
    "tags": "#Casabella #MilanoVerde #城市设计 #绿地系统 #住区规划 #建筑历史 #FrancoAlbini #IgnazioGardella",
    "cards": [
        {"image":"02-fiera-1928-aerial.jpg", "focal":(0.50,0.46), "source":"Fiera Milano 档案｜Fiera 鸟瞰｜Casabella 132", "eyebrow":"观点 01｜先看清大地块如何切断城市", "title":"展馆、道路与围合空地一旦各自扩张，城市会变成一串孤岛；规划先要重新建立能穿行的整体", "body":"Fiera 区域的航拍显示了大型设施的双面性：它能带来规模，却也容易把街区切成封闭片段。Milano Verde 的起点，是把这些片段重新放回可步行、可连接的城市网格。"},
        {"image":"03-milano-verde-model.jpg", "focal":(0.50,0.48), "source":"Albini等｜Milano Verde 住区模型｜Casabella 132", "eyebrow":"观点 02｜用绿带给住宅留出距离", "title":"住宅不必围成封闭院子；让线性体量之间保持绿地与通风空隙，日照和视线才能进入每一户", "body":"模型把不同住区地块并置比较。关键不是复制同一种楼，而是让每一种组合都守住开敞地面、楼间距离与朝向的底线；绿地因此成为居住单元之间的共同基础。"},
        {"image":"04-fiera-1937.jpg", "focal":(0.52,0.45), "source":"Fiera Milano 档案｜Viale delle Nazioni｜Casabella 132", "eyebrow":"观点 03｜主路只负责把人带到这里", "title":"一条强势大道可以承担城市抵达，但生活不应全挤在大道边；内部还要有尺度更慢的街道与步行线", "body":"展会大道展示了大流量路径的效率，也提醒人们它不等于完整街区。Milano Verde 通过道路层级，把穿越交通留在外部，把住宅入口、散步与停留交给更细的内部网络。"},
        {"image":"05-fiera-1926.jpg", "focal":(0.50,0.47), "source":"Fiera Milano 档案｜Fiera 鸟瞰｜Casabella 132", "eyebrow":"观点 04｜网格不是把地块切得越小越好", "title":"正交网格的作用是给建筑、绿地和服务设施一套共同坐标，而不是把每一寸土地都拆成利润单位", "body":"面对可开发的大片土地，网格可以避免道路与建筑各走各路。只要先设定公共地面和通行层级，地块才会有边界；没有这一步，所谓灵活往往只是无序扩张。"},
        {"image":"06-fiera-1927.jpg", "focal":(0.50,0.48), "source":"Fiera Milano 档案｜Fiera 鸟瞰｜Casabella 132", "eyebrow":"观点 05｜开放面需要连续而非零碎", "title":"零散草坪只能点缀建筑；把绿地连成可走的带状网络，才能真正把住区、服务与公共生活接起来", "body":"开放空间的价值不只在面积，还在连续性。若人能沿着树荫、庭园和慢行路径穿过不同地块，绿地才会从“景观配额”变成街区的日常基础设施。"},
        {"image":"07-milano-verde-perspective.jpg", "focal":(0.50,0.47), "source":"Albini等｜Milano Verde 总体透视｜Casabella 132", "eyebrow":"观点 06｜让日照成为总平面条件", "title":"住宅朝向、楼间距与绿地不该各自决定；它们必须在总体布局里同时被校准，才有稳定的居住品质", "body":"Milano Verde 以正交组织街区，并把住宅日照、公共与私有建筑的层级、主次道路一并纳入方案。形式的整齐不是目的，稳定获得光、风和开敞面才是。"},
        {"image":"08-fiera-1928.jpg", "focal":(0.50,0.49), "source":"Fondazione Fiera Milano｜Fiera 总平面｜Casabella 132", "eyebrow":"观点 07｜服务设施也要进入街区骨架", "title":"展馆、商业和公共服务不能只靠一条主入口串联；把它们分布到步行网络中，日常使用才会均匀发生", "body":"总平面图里，功能被清楚编号与分区。对住区而言，这个方法同样重要：服务不应全部堆在边缘，而应借由可达的道路与绿地节点嵌入日常行走。"},
        {"image":"09-fiera-1936.jpg", "focal":(0.50,0.46), "source":"Argo 摄影社｜Fiera 工业大道｜Casabella 132", "eyebrow":"观点 08｜把高强度活动放在可承受的位置", "title":"展会、物流和车流可以很密集，但它们需要被放进明确的服务带，避免吞没住宅前的步行与停留空间", "body":"从高处看，密集展馆依靠清楚的主轴与后勤面维持运转。城市也应如此：让高强度交通拥有自己的路径，把安静、可停留的地面保留给邻里生活。"},
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 132 原刊封面，1938年12月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/132-nz.jpg",
        "`02-fiera-1928-aerial.jpg`｜Fiera Campionaria di Milano，1928年航拍｜Archivio Storico Fondazione Fiera Milano｜https://archiviostorico.fondazionefiera.it/oggetti/8741-veduta-aerea-della-fiera-campionaria-di-milano-del-1928｜许可待商业发布前复核｜裁切与文字排版",
        "`03-milano-verde-model.jpg`｜Milano Verde 住宅地块模型，原刊抽印本内页｜AbeBooks 书目图像｜https://www.abebooks.it/prima-edizione/MILANO-VERDE-Piano-regolatore-zona-Sempione-Fiera/30937125912/bd｜许可待商业发布前复核｜裁切与文字排版",
        "`04-fiera-1937.jpg`｜Fiera Campionaria，Viale delle Nazioni，1937年｜Lombardia Beni Culturali / Fondazione Fiera Milano｜https://www.lombardiabeniculturali.it/fotografie/schede/IMM-u3010-0003067/｜许可待商业发布前复核｜裁切与文字排版",
        "`05-fiera-1926.jpg`、`06-fiera-1927.jpg`｜Fiera Campionaria 航拍，1926/1927年｜Archivio Storico Fondazione Fiera Milano｜https://archiviostorico.fondazionefiera.it/oggetti/1928-veduta-aerea-della-fiera-campionaria-di-milano-del-1926；https://archiviostorico.fondazionefiera.it/oggetti/8713-veduta-aerea-della-fiera-campionaria-di-milano-del-1927｜许可待商业发布前复核｜裁切与文字排版",
        "`07-milano-verde-perspective.jpg`｜Franco Albini、Ignazio Gardella、Giulio Minoletti、Giuseppe Pagano、Giancarlo Palanti、Giangiacomo Predaval、Giovanni Romano，Milano Verde 透视，1938年｜MuseoCity｜https://www.museocity.it/opere/2020/progetto-milano-verde｜许可待商业发布前复核｜裁切与文字排版",
        "`08-fiera-1928.jpg`｜Fiera Esposizione di Milano 总平面，1928年｜Archivio Storico Fondazione Fiera Milano｜https://archiviostorico.fondazionefiera.it/oggetti/40875-planimetria-generale-della-fiera-esposizione-di-milano-del-1928｜许可待商业发布前复核｜裁切与文字排版",
        "`09-fiera-1936.jpg`｜Argo Agenzia Fotografica，Fiera Campionaria 工业大道航拍，1936年｜Archivio Storico Fondazione Fiera Milano｜https://archiviostorico.fondazionefiera.it/oggetti/4679-veduta-dallalto-dellarea-intorno-al-viale-dellindustria-alla-fiera-campionaria-di-milano-del-1936｜许可待商业发布前复核｜裁切与文字排版",
        "文章与方案核验｜Giuseppe Pagano《L’ordine contro il disordine》及《Milano Verde：Piano regolatore della zona Sempione-Fiera a Milano》，Casabella-Costruzioni 132，1938年12月，第4–24页；方案提出正交网格、住宅日照及主次道路层级｜Politecnico di Milano 书目｜https://opac.biblio.polimi.it/SebinaOpac/resource/PMI00138744；MuseoCity｜https://www.museocity.it/opere/2020/progetto-milano-verde",
        "同期文章核验｜Giuseppe Pagano《Un giovane progetta una borgata rurale in acciaio》，Casabella-Costruzioni 132，1938年12月｜Lombardia Beni Culturali｜https://www.lombardiabeniculturali.it/archivi/unita/MIUD02FC66/",
    ],
}


def save_rgb(image: Image.Image, path: Path) -> Path:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def mark(draw: ImageDraw.ImageDraw, number: int, light: bool = False) -> None:
    draw.text((1168, 1602), f"{number:02d} / 10", font=font(FONT_SANS, 21), fill=rgba(LIGHT if light else INK, 170), anchor="ra")


def header(draw: ImageDraw.ImageDraw, number: int, light: bool = False) -> None:
    color = LIGHT if light else INK
    draw.text((68, 52), CFG["issue"], font=font(FONT_BOLD, 22), fill=color)
    draw.text((1170, 52), CFG["date"], font=font(FONT_SANS, 20), fill=rgba(color, 185), anchor="ra")
    draw.line((68, 96, 1170, 96), fill=rgba(color, 85), width=2)
    mark(draw, number, light)


def source_strip(draw: ImageDraw.ImageDraw, text: str) -> None:
    draw.rounded_rectangle((68, 972, 1172, 1044), 5, fill=rgba(CFG["dark"], 240))
    draw_fit(draw, (94, 988), text, 1048, 34, 19, LIGHT, spacing=4)


def make_case(src: Path, out: Path, number: int, card: dict) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    image = Image.open(src / card["image"]).convert("RGB")
    image = cover_crop(image, (W, 1070), card["focal"])
    canvas.alpha_composite(ImageEnhance.Contrast(image).enhance(1.05).convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 120), (0, 0, 0, 102)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    header(draw, number, True)
    source_strip(draw, card["source"])
    canvas.alpha_composite(Image.new("RGBA", (W, H - 1070), rgba(CFG["paper2"])), (0, 1070))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((68, 1127, 80, 1525), fill=CFG["accent"])
    draw.text((112, 1120), card["eyebrow"], font=font(FONT_BOLD, 22), fill=CFG["accent"])
    bottom = draw_fit(draw, (112, 1180), card["title"], 1010, 175, 47, INK, serif=True, spacing=12)
    draw_fit(draw, (112, bottom + 28), card["body"], 990, 145, 26, rgba(INK, 205), spacing=9)
    mark(draw, number)
    return save_rgb(canvas, out / f"{number:02d}.jpg")


def make_cover(src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#dfe6d6"))
    draw = ImageDraw.Draw(canvas)
    dark, accent = CFG["dark"], CFG["accent"]
    draw.rectangle((0, 0, W, H), fill="#dfe6d6")
    for x in range(-80, W + 120, 108):
        draw.line((x, 0, x - 330, H), fill=rgba(accent, 40), width=2)
    draw.rectangle((0, 0, 362, H), fill=dark)
    draw.text((54, 56), CFG["issue"], font=font(FONT_BOLD, 19), fill=LIGHT)
    draw.text((54, 94), CFG["date"], font=font(FONT_SANS, 17), fill=rgba(LIGHT, 190))
    draw.text((54, 168), "单期主线", font=font(FONT_BOLD, 21), fill="#b7d48b")
    draw_fit(draw, (54, 232), "绿地不是\n边角料", 260, 290, 63, LIGHT, serif=True, spacing=16)
    draw_fit(draw, (54, 596), CFG["question"], 250, 480, 34, rgba(LIGHT, 220), serif=True, spacing=13)
    cover = ImageEnhance.Sharpness(Image.open(src / CFG["cover"]).convert("RGB")).enhance(1.30)
    mount(canvas, cover, (470, 180, 570, 612), True)
    draw.rectangle((470, 838, 1110, 848), fill=accent)
    draw.text((470, 895), "让绿地成为城市的第一层结构", font=font(FONT_BOLD, 31), fill=dark)
    draw_fit(draw, (470, 972), CFG["thesis"], 645, 370, 42, dark, serif=True, spacing=15)
    draw.text((470, 1510), "Casabella-Costruzioni｜第132期原刊封面｜1938年12月", font=font(FONT_SANS, 19), fill=rgba(dark, 195))
    mark(draw, 1)
    return save_rgb(canvas, out / "01.jpg")


def make_summary(src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#e0e7d7"))
    draw = ImageDraw.Draw(canvas)
    header(draw, 10)
    img = cover_crop(Image.open(src / "07-milano-verde-perspective.jpg").convert("RGB"), (590, 680), (0.50, 0.48))
    canvas.alpha_composite(ImageEnhance.Contrast(img).enhance(1.06).convert("RGBA"), (584, 150))
    draw.rectangle((584, 150, 1174, 830), outline=CFG["dark"], width=4)
    draw.text((68, 192), "绿地要先\n成为规则", font=font(FONT_BOLD, 63), fill=CFG["dark"], spacing=12)
    draw_fit(draw, (68, 396), CFG["summary"], 445, 355, 39, CFG["dark"], serif=True, spacing=15)
    y = 900
    for i, (label, body) in enumerate(zip(CFG["concepts"], CFG["takeaways"]), 1):
        draw.line((68, y, 1174, y), fill=rgba(CFG["dark"], 150), width=2)
        draw.text((68, y + 32), f"0{i}", font=font(FONT_BOLD, 34), fill=CFG["accent"])
        draw.text((186, y + 28), label, font=font(FONT_BOLD, 35), fill=CFG["dark"])
        draw_fit(draw, (186, y + 84), body, 915, 74, 27, rgba(CFG["dark"], 215), serif=True, spacing=9)
        y += 178
    draw.rectangle((68, 1465, 1174, 1528), fill=CFG["dark"])
    draw.text((96, 1481), "绿地不是最后的配额，而是第一张总平面。", font=font(FONT_BOLD, 29), fill=LIGHT)
    mark(draw, 10)
    return save_rgb(canvas, out / "10.jpg")


def make_preview(paths: list[Path], out: Path) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#c8c3b9")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(image, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(out / "preview.jpg", quality=94, subsampling=0)


def manifest() -> dict:
    return {"type":"magazine","slug":CFG["slug"],"issue":CFG["issue"].title(),"date":CFG["date_cn"],"core_question":CFG["question"],"core_thesis":CFG["thesis"],"pages":[f"01 单期主线：{CFG['question']}", *[f"{i:02d} {c['source']}：{c['title']}" for i,c in enumerate(CFG["cards"],2)], f"10 总结：{'；'.join(CFG['concepts'])}"]}


def render() -> None:
    src, out = ROOT / "assets" / CFG["slug"], ROOT / "output" / CFG["slug"]
    out.mkdir(parents=True, exist_ok=True)
    paths = [make_cover(src, out)]
    paths += [make_case(src, out, i, card) for i, card in enumerate(CFG["cards"], 2)]
    paths.append(make_summary(src, out))
    make_preview(paths, out)
    (out / "发布文案.md").write_text(f"{CFG['publish_title']}\n\n{CFG['publish_body']}\n\n{CFG['tags']}\n", encoding="utf-8")
    (out / "图片来源.md").write_text(f"# {CFG['issue'].title()} 图片来源\n\n" + "\n".join(f"- {s}" for s in CFG["sources"]) + "\n", encoding="utf-8")
    post = ROOT / "posts" / CFG["slug"]
    post.mkdir(parents=True, exist_ok=True)
    (post / "post.json").write_text(json.dumps(manifest(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(paths)} cards in {out}")


if __name__ == "__main__":
    render()
