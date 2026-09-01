from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    FONT_BOLD, FONT_SANS, H, INK, LIGHT, PAPER, ROOT, W,
    cover_crop, draw_fit, font, mount, rgba,
)


CFG = {
    "slug": "casabella-130",
    "issue": "CASABELLA-COSTRUZIONI 130",
    "date": "OTTOBRE 1938 | ANNO XI",
    "date_cn": "1938年10月",
    "cover": "book-cover.jpg",
    "accent": "#16818a",
    "dark": "#16333d",
    "question": "面对海岸，建筑不该是一堵挡风墙；它要用抬升、遮阳、通风和长廊把气候变成日常。",
    "thesis": "第130期以 Vaccaro 的 Cesenatico AGIP 海滨疗养院为核心，同时讨论系列住宅与别墅：海风、日照与季节性使用不是立面之后的技术问题，它们决定了建筑如何贴近地面、拉开体量并组织集体生活。",
    "summary": "130期说明，气候不是风格滤镜，而是一套空间规则。建筑沿海岸展开，架空层让沙地和人流继续穿过；遮阳、开口与长廊把强光、海风和停留调到合适的程度。面向季节与身体的设计，才会让形式变得必要。",
    "concepts": ["顺着风向展开", "把首层让给空气", "让阴影成为活动场"],
    "takeaways": [
        "先看太阳、海风和到达方向，再决定建筑的长边与开口。朝向不是造型选择，而是每个房间如何获得空气和光。",
        "把首层适度架空，连续地面就能容纳进入、等待、游戏与穿行；建筑不占满场地，场地才会继续工作。",
        "檐下、连廊和阳台是气候缓冲器。它们让人不必在室内与暴晒之间二选一，而能拥有可停留的中间地带。",
    ],
    "publish_title": "CASABELLA130｜海风如何造建筑",
    "publish_body": "Casabella-Costruzioni 130 让人看到，海边建筑最重要的不是“看起来像度假”，而是能否把风、太阳、沙地和集体生活真正组织起来。Giuseppe Vaccaro 的 AGIP 海滨疗养院沿 Cesenatico 海岸平行展开：五层宿舍抬在柱子上，连续首层保持通透；两端较低的服务体量承担餐厅、厨房等功能；人、空气和视线都能从建筑下方穿过。\n\n这个项目的逻辑很简单，却很有用。长边面向气候，重复房间获得稳定的光与风；架空层把沙地还给活动；深檐和连廊提供阴影与过渡。建筑不是把自然挡在外面，而是把环境过滤成可使用的日常。\n\n今天做海边、校园、社区甚至南方住宅，也可以先问：风从哪里来？阳光最强在哪里？人能在哪一段停下来，而不用躲进空调房？你最喜欢哪一种“半室外”的空间？",
    "tags": "#Casabella #海岸建筑 #气候设计 #建筑历史 #GiuseppeVaccaro #空间设计 #现代建筑 #公共空间",
    "cards": [
        {"image":"extra-3.jpg","accent":"#16818a","focal":(0.50,0.48),"source":"Giolli｜AGIP 海滨疗养院｜Casabella 130","eyebrow":"观点 01｜长边先向海岸校准","title":"把宿舍楼平行于海岸拉开，房间才能获得稳定的光与风；体量的方向先由气候决定","body":"AGIP 疗养院的主楼顺着海岸线展开。长条体量不是为了显得水平，而是让重复房间共享一致的朝向；建筑先读懂风和太阳，立面节奏才有意义。"},
        {"image":"extra-4.jpg","accent":"#d49b45","focal":(0.54,0.45),"source":"Vaccaro｜AGIP 海滨疗养院｜Casabella 130","eyebrow":"观点 02｜把地面还给空气与人","title":"五层宿舍被柱子抬起后，首层不再是封闭基座；风、视线和集体活动能继续穿过建筑","body":"架空不是一条形式原则。它在海岸创造了阴影与通风，也给进入、集合和临时停留留下连续地面。建筑抬得越清楚，场地就越不被切碎。"},
        {"image":"03-agip.jpg","accent":"#16818a","focal":(0.50,0.42),"source":"Vaccaro｜AGIP 海滨疗养院｜Casabella 130","eyebrow":"观点 03｜重复房间需要同一气候条件","title":"把卧室排成均质带状立面，不是为了机械整齐；它保证每个单元都能得到近似的日照与通风","body":"集体居住最怕把好朝向留给少数房间。连续窗带与规则模块让房间共享海风和光线；标准化在这里首先是一种环境公平。"},
        {"image":"04-agip.jpg","accent":"#d49b45","focal":(0.51,0.45),"source":"Vaccaro｜AGIP 海滨疗养院｜Casabella 130","eyebrow":"观点 04｜低体量负责服务与停留","title":"把餐厅、厨房等服务空间压低放在长楼两端，让宿舍保持安静，也让集体活动有自己的尺度","body":"不同程序不需要塞进同一座块状建筑。高的长楼承担休息，低的端部承接用餐、后勤与聚集；体量差让功能关系从外部就能读懂。"},
        {"image":"05-agip.jpg","accent":"#16818a","focal":(0.50,0.48),"source":"Giolli｜AGIP 海滨疗养院｜Casabella 130","eyebrow":"观点 05｜海滩是建筑的延伸地面","title":"面向沙地的首层不应封死：把视线、路径和活动留给海岸，建筑才不会变成一条拒绝环境的边界","body":"站在海滩看，疗养院的地面层仍可被穿越。建筑没有把海岸切成前后两半，而是让户外活动、入口与阴影连续发生，海滩也成为日常空间的一部分。"},
        {"image":"07-agip.jpg","accent":"#d49b45","focal":(0.50,0.49),"source":"Vaccaro｜AGIP 海滨疗养院｜Casabella 130","eyebrow":"观点 06｜场地要给建筑留出呼吸距离","title":"主楼与周边体量不必贴紧；保留草地、沙地与通行空隙，风和人的路线才有地方转弯、会合与停下","body":"建筑群的密度不只用建筑面积判断。沿海项目需要让风穿过，也要让人看见远处。留出的空地不是剩余，而是连接不同活动与气候条件的公共基础设施。"},
        {"image":"08-agip.jpg","accent":"#16818a","focal":(0.50,0.44),"source":"Vaccaro｜AGIP 海滨疗养院｜Casabella 130","eyebrow":"观点 07｜阴影要被设计成一层空间","title":"深檐、柱列和退进的首层共同制造阴影，让人在暴晒与室内之间拥有能走、能等、能看的中间地带","body":"气候设计的关键不只是避开太阳。更重要的是提供不同亮度与温度的选择：檐下可以通过，靠边可以停留，向外又能看见海岸；身体因此不被迫只剩两个选项。"},
        {"image":"09-agip.jpg","accent":"#d49b45","focal":(0.52,0.46),"source":"Giolli｜AGIP 海滨疗养院｜Casabella 130","eyebrow":"观点 08｜形式来自一套可重复的规则","title":"柱距、窗带、阳台和屋檐反复出现，建筑因此既能容纳大规模集体生活，也能保持清楚的人的尺度","body":"尺度大的建筑不必变成巨物。让结构、房间与遮阳遵循同一套节奏，远看是稳定的整体，近看仍然能读到门、窗、阴影和可抵达的位置。"},
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 130 原刊封面，1938年10月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/130-nz.jpg",
        "`extra-3.jpg`｜Giuseppe Vaccaro，AGIP 海滨疗养院，Cesenatico，历史远景｜Engramma｜https://www.engramma.it/eOS/resources/images/169/e169_demaio_%20%281%29%281%29.jpg｜许可待商业发布前复核｜裁切与文字排版",
        "`extra-4.jpg`｜Giuseppe Vaccaro，AGIP 海滨疗养院，Cesenatico，历史架空层照片｜Engramma｜https://www.engramma.it/eOS/resources/images/169/e169_demaio_%20%286%29.jpg｜许可待商业发布前复核｜裁切与文字排版",
        "`03-agip.jpg`—`09-agip.jpg`｜Giuseppe Vaccaro，AGIP 海滨疗养院，Cesenatico，建筑现状照片｜Biblioteca Salaborsa｜https://www.bibliotecasalaborsa.it/bolognaonline/cronologia-di-bologna/1938/la-colonia-sandro-mussolini-agip-a-cesenatico｜许可待商业发布前复核｜裁切与文字排版",
        "文章与项目核验｜Raffaello Giolli《La colonia marina dell’A.G.I.P. a Cesenatico》，Casabella-Costruzioni 130，1938年10月；项目为 Giuseppe Vaccaro，1937–38，主楼五层、架空且平行海岸，两端低体量为服务空间｜Biblioteca Salaborsa｜https://www.bibliotecasalaborsa.it/bolognaonline/cronologia-di-bologna/1938/la-colonia-sandro-mussolini-agip-a-cesenatico",
        "目录核验｜第130期含 Pagano《Variazioni sull’autarchia II》、Ragghianti《L’architettura italiana del ‘200 e del ‘300》、Giolli《La colonia marina dell’A.G.I.P. a Cesenatico》、Schio 系列住宅与别墅方案｜Casa dell’Architettura Latina｜https://www.casadellarchitettura.eu/collezioni/riviste/casabella-costruzioni/",
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
    draw.rounded_rectangle((68, 972, 1172, 1044), 5, fill=rgba(CFG["dark"], 238))
    draw_fit(draw, (94, 988), text, 1048, 34, 19, LIGHT, spacing=4)


def make_case(src: Path, out: Path, number: int, card: dict) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    image = Image.open(src / card["image"]).convert("RGB")
    image = cover_crop(image, (W, 1070), card["focal"])
    canvas.alpha_composite(ImageEnhance.Contrast(image).enhance(1.04).convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 120), (0, 0, 0, 92)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    header(draw, number, True)
    source_strip(draw, card["source"])
    canvas.alpha_composite(Image.new("RGBA", (W, H - 1070), rgba(PAPER)), (0, 1070))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((68, 1127, 80, 1525), fill=card["accent"])
    draw.text((112, 1120), card["eyebrow"], font=font(FONT_BOLD, 22), fill=card["accent"])
    bottom = draw_fit(draw, (112, 1180), card["title"], 1010, 175, 48, INK, serif=True, spacing=12)
    draw_fit(draw, (112, bottom + 28), card["body"], 990, 145, 27, rgba(INK, 205), spacing=9)
    mark(draw, number)
    path = out / f"{number:02d}.jpg"
    return save_rgb(canvas, path)


def make_cover(src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#e5edf0"))
    draw = ImageDraw.Draw(canvas)
    dark, accent = CFG["dark"], CFG["accent"]
    draw.rectangle((0, 0, W, 46), fill=dark)
    for y in (422, 485, 548, 611):
        draw.line((0, y, W, y), fill=rgba(accent, 75), width=2)
    draw.text((68, 85), CFG["issue"], font=font(FONT_BOLD, 25), fill=dark)
    draw.text((1170, 87), CFG["date"], font=font(FONT_SANS, 19), fill=rgba(dark, 180), anchor="ra")
    draw.text((68, 174), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (68, 238), CFG["question"], 1080, 225, 58, dark, serif=True, spacing=17)
    cover = ImageEnhance.Sharpness(Image.open(src / CFG["cover"]).convert("RGB")).enhance(1.28)
    mount(canvas, cover, (78, 710, 372, 630), True)
    draw.rectangle((508, 710, 1142, 1340), fill=dark)
    draw.text((550, 760), "海岸不是背景", font=font(FONT_BOLD, 28), fill="#e7c06a")
    draw_fit(draw, (550, 828), CFG["thesis"], 540, 390, 40, "#f1f6f6", serif=True, spacing=15)
    draw.line((550, 1260, 1098, 1260), fill=rgba("#f1f6f6", 100), width=2)
    draw.text((550, 1282), "风 / 光 / 阴影 / 共同生活", font=font(FONT_BOLD, 23), fill="#e7c06a")
    draw.rectangle((0, 1422, W, H), fill=accent)
    draw_fit(draw, (68, 1465), "建筑不是把自然挡在外面，而是把环境变成可用的日常。", 1050, 80, 33, "#f1f6f6", serif=True, spacing=9)
    draw.text((68, 1560), "Casabella-Costruzioni｜第130期原刊封面｜1938年10月", font=font(FONT_SANS, 19), fill=rgba("#f1f6f6", 200))
    mark(draw, 1, True)
    return save_rgb(canvas, out / "01.jpg")


def make_summary(out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#e7c06a"))
    draw = ImageDraw.Draw(canvas)
    header(draw, 10, False)
    draw.rectangle((0, 130, W, 150), fill=CFG["accent"])
    draw.text((68, 208), "把气候设计成空间秩序", font=font(FONT_BOLD, 28), fill=CFG["dark"])
    draw_fit(draw, (68, 282), CFG["summary"], 1050, 300, 49, CFG["dark"], serif=True, spacing=17)
    y = 700
    for i, (label, body, color) in enumerate(zip(CFG["concepts"], CFG["takeaways"], [CFG["accent"], CFG["dark"], "#557c63"]), 1):
        draw.rectangle((68, y, 1174, y + 178), fill=color)
        draw.text((108, y + 44), f"0{i}", font=font(FONT_BOLD, 36), fill="#e7c06a")
        draw.text((228, y + 38), label, font=font(FONT_BOLD, 36), fill="#f5f1e7")
        draw_fit(draw, (228, y + 95), body, 875, 58, 27, rgba("#f5f1e7", 220), serif=True, spacing=8)
        y += 210
    draw.rectangle((68, 1372, 1174, 1434), fill=CFG["dark"])
    draw.text((96, 1388), "气候不是装饰条件，而是建筑的第一张平面图。", font=font(FONT_BOLD, 29), fill="#f5f1e7")
    draw.text((68, 1514), "Casabella-Costruzioni｜第130期海岸建筑讨论｜1938年10月", font=font(FONT_SANS, 19), fill=rgba(CFG["dark"], 195))
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
    paths.append(make_summary(out))
    make_preview(paths, out)
    (out / "发布文案.md").write_text(f"{CFG['publish_title']}\n\n{CFG['publish_body']}\n\n{CFG['tags']}\n", encoding="utf-8")
    (out / "图片来源.md").write_text(f"# {CFG['issue'].title()} 图片来源\n\n" + "\n".join(f"- {s}" for s in CFG["sources"]) + "\n", encoding="utf-8")
    post = ROOT / "posts" / CFG["slug"]
    post.mkdir(parents=True, exist_ok=True)
    (post / "post.json").write_text(json.dumps(manifest(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(paths)} cards in {out}")


if __name__ == "__main__":
    render()
