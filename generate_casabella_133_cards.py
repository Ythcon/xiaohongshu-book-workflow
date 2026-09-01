from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    FONT_BOLD, FONT_SANS, H, INK, LIGHT, PAPER, ROOT, W,
    cover_crop, draw_fit, font, mount, rgba,
)


CFG = {
    "slug": "casabella-133",
    "issue": "CASABELLA-COSTRUZIONI 133",
    "date": "GENNAIO 1939 | ANNO XII",
    "date_cn": "1939年1月",
    "cover": "book-cover.jpg",
    "accent": "#cb673f",
    "dark": "#253c52",
    "paper2": "#edf0e9",
    "question": "当基地比街道低 11 米，建筑不必把高差藏起来；它可以把高差变成一座可抵达、可停留的新广场。",
    "thesis": "第133期刊登 Attilio Podestà 对 Luigi Carlo Daneri 热那亚 Sturla 项目的介绍。建筑面对低于街道 11 米的基地，叠加四层形成新的街道标高；上部体量被六根柱子抬起，底部同时成为广场、遮蔽处与连接不同高度的公共空间。",
    "summary": "133期最有力的启示是：高差不是需要被抹平的麻烦，而是可以制造公共空间的材料。先在正确标高建立可用的平台；再让不同功能沿着剖面排布；最后用柱、楼梯和开口把上下层的关系暴露出来。建筑因此不是挡住坡地，而是让坡地变得可用。",
    "concepts": ["先建立公共标高", "让剖面承担分区", "把结构变成路径"],
    "takeaways": [
        "遇到强高差，先判断人真正从哪个标高抵达。把这一层做成完整平台，比一味填土或挖地下室更容易获得清楚的公共入口。",
        "把安静、服务、集会等功能沿垂直方向排开；每层直接回应自己的高度和出入口，建筑的组织会比平面硬塞更自然。",
        "楼梯、柱列与架空层不只是技术构件。让它们参与连接、停留和识别，结构就能把不同高度转化为连续体验。",
    ],
    "publish_title": "CASABELLA133｜坡地也能成广场",
    "publish_body": "Casabella-Costruzioni 133 里的 Casa Littoria Sturla，给了坡地建筑一个很直接的答案：不要急着把高差填平。\n\nDaneri 面对的是一块比 Piazza Sturla 低 11 米的基地。如果顺着原地面盖，建筑几乎会从街道上消失。他选择叠加四层，在街道标高造出一块新的公共平台；下面布置会议、服务与双层体育空间；最上层体量由六根柱子抬起，玻璃砖楼梯塔把垂直交通清楚地写在外部。\n\n这个项目最值得学习的，是它把“剖面”当作城市空间来设计。平台不是屋顶附属物，而是进入建筑前的一段广场；架空也不只是形式，而是让街道、遮蔽和视线在同一高度相遇。面对坡地、桥下、下沉广场或临水地块，都可以先问：人从哪一层抵达？哪一层才应该成为公共地面？\n\n你见过最能把高差变成空间体验的建筑是哪一座？",
    "tags": "#Casabella #坡地建筑 #剖面设计 #公共空间 #LuigiCarloDaneri #建筑历史 #热那亚 #现代建筑",
    "cards": [
        {"image":"02-casa-1938.jpg", "focal":(0.50,0.47), "source":"Luigi Carlo Daneri｜Casa Littoria Sturla｜Casabella 133", "eyebrow":"观点 01｜先在街道高度造一块公共地面", "title":"基地低于街道 11 米时，先把建筑叠到正确的标高；新的平台便能成为真正可抵达的广场", "body":"Daneri 没有让建筑躲在坡底，而是把四层空间叠加成新的街道高度。这个上升出来的平台同时是入口、停留面与城市界面，高差从障碍变成公共空间的起点。"},
        {"image":"03-casa-night.jpg", "focal":(0.52,0.45), "source":"Luigi Carlo Daneri｜Casa Littoria Sturla｜Casabella 133", "eyebrow":"观点 02｜上部体量要给街道留下呼吸", "title":"把最上层抬在六根柱子上，街道层便不会被一整块建筑压死；下方仍保有穿行、遮蔽与看见远处的余地", "body":"抬起体量不只是为了显得轻。柱列在公共标高上留下阴影和可进入的边缘，让人先经历开放空间，再进入室内；建筑因此没有把新广场封成屋顶。"},
        {"image":"04-piazza-sturla.jpg", "focal":(0.50,0.48), "source":"Luigi Carlo Daneri｜Casa Littoria Sturla｜Casabella 133", "eyebrow":"观点 03｜先读懂人从哪里抵达", "title":"坡地项目最重要的不是最低处能放多少面积，而是行人从哪一层看见入口、找到停留面并继续前行", "body":"面对 Piazza Sturla，建筑用与街道一致的标高建立新的入口。先确定公共抵达层，后续的楼梯、体量与功能才不会各自为政；剖面由此获得清楚的第一笔。"},
        {"image":"05-daneri-sturla.jpg", "focal":(0.50,0.45), "source":"Luigi Carlo Daneri｜Casa Littoria Sturla｜Casabella 133", "eyebrow":"观点 04｜平台不是屋顶，而是一间室外大厅", "title":"当平台足够完整、足够接近街道，它就不再是建筑的附属屋顶，而是能等人、集合和转换方向的公共房间", "body":"这个项目把抬升后的水平面赋予公共性：人从街道抵达这里，再选择进入、停留或向不同高度移动。把室外平台当作一间没有围墙的大厅，坡地才会真正被使用。"},
        {"image":"06-daneri-stair.jpg", "focal":(0.50,0.47), "source":"Luigi Carlo Daneri｜Casa Littoria Sturla｜Casabella 133", "eyebrow":"观点 05｜让垂直交通成为空间的一部分", "title":"弧形玻璃砖楼梯塔把上下移动带到室外；沿坡行走不再躲进黑暗楼道，而能持续感知光、树与街道", "body":"高差项目里的楼梯应当参与空间组织。Daneri 让楼梯塔、柱列和平台彼此咬合：人一边转换高度，一边读懂建筑与场地的关系，交通也因此成为停留体验。"},
        {"image":"07-casa-fire.jpg", "focal":(0.49,0.45), "source":"Luigi Carlo Daneri｜Casa Littoria Sturla｜Casabella 133", "eyebrow":"观点 06｜改造前先保护空间逻辑", "title":"旧建筑转换用途时，最该被保留的不只是立面，而是平台、架空层、楼梯与层高共同形成的空间秩序", "body":"这个项目之所以能被重新讨论，是因为它的价值藏在剖面关系里。新的功能必须先理解哪里是公共抵达层、哪里是大空间、哪里承担垂直连接，才能避免把建筑改成普通盒子。"},
        {"image":"08-daneri-detail.jpg", "focal":(0.48,0.47), "source":"Luigi Carlo Daneri｜Casa Littoria Sturla｜Casabella 133", "eyebrow":"观点 07｜小体量也能成为街区锚点", "title":"建筑不需要占满街角才有公共性；只要入口标高、体量转折和可见的交通节点足够清楚，它就能组织周边路径", "body":"从道路看，项目的体量并不夸张，却用抬起的上层、醒目的楼梯塔和平台建立方向感。公共建筑的存在感可以来自空间关系，而不必来自过度巨大的门面。"},
        {"image":"09-daneri-view.jpg", "focal":(0.45,0.47), "source":"Luigi Carlo Daneri｜Casa Littoria Sturla｜Casabella 133", "eyebrow":"观点 08｜把结构直接变成体验", "title":"柱子、玻璃砖楼梯塔和悬出的体量共同讲清上下关系；结构一旦可读，人就能理解自己正处在建筑的哪一层", "body":"Daneri 让垂直交通从封闭核心里走出来，成为外部可见的线索；柱子承重，也标记平台边缘。结构不再躲在墙后，而是帮助人认知高度、方向和进入方式。"},
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 133 原刊封面，1939年1月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/133-nz.jpg",
        "`02-casa-1938.jpg`｜Casa del Soldato / Casa Littoria Sturla，1938年历史照片，匿名｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Casa_del_Soldato,_Genova,_1938.jpg｜公共领域（PD-ItalyGov / PD-anon-70-EU）｜裁切与文字排版",
        "`03-casa-night.jpg`｜Casa Littoria Sturla，Riotforlife，2009年｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:CasaLittoriaSturla.JPG｜CC BY-SA 3.0｜裁切与文字排版；发布须按 CC BY-SA 3.0 署名并兼容分享",
        "`04-piazza-sturla.jpg`｜Piazza Sturla，Genova｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/Category:Casa_del_Soldato｜作者与许可须在商业发布前复核｜裁切与文字排版",
        "`05-daneri-sturla.jpg`、`06-daneri-stair.jpg`、`08-daneri-detail.jpg`、`09-daneri-view.jpg`｜Casa Littoria Sturla，Andrea Canziani / Emanuele Piccardo（原文图注）｜Il Giornale dell’Architettura｜https://partnership.ilgiornaledellarchitettura.com/2019/04/19/genova-per-la-casa-littoria-di-sturla-si-ricomincia-da-zero/｜许可待商业发布前复核｜裁切与文字排版",
        "`07-casa-fire.jpg`｜Casa del Soldato，Genova Quotidiana，2025年｜https://genovaquotidiana.com/2025/01/19/dopo-lincendio-nella-casa-del-soldato-gli-architetti-rilanciano-il-progetto-malamente-abortito-della-casa-di-quartiere/｜许可待商业发布前复核｜裁切与文字排版",
        "文章核验｜Attilio Podestà《Una Casa Littoria a Genova-Sturla》，Casabella-Costruzioni 133，1939年1月；项目为 Luigi Carlo Daneri，1936–38。基地低于 Piazza Sturla 约11米，四层叠加生成新平台，上部体量由六根柱子抬起，低层设会议空间与双层体育空间｜Il Giornale dell’Architettura｜https://partnership.ilgiornaledellarchitettura.com/2019/04/19/genova-per-la-casa-littoria-di-sturla-si-ricomincia-da-zero/",
        "同期目录线索｜Raffaello Giolli《Due teatri di Luigi Cosenza》、Mario Salvadori《Sollecitazioni generate da un carico concentrato in una piastra a sbalzo》、Guido Gambardella《Organizzazione di officine per costruzioni metalliche》均见 Casabella-Costruzioni 133｜Mostra d’Oltremare 文献｜https://www.ilmondonuovo.club/wp-content/uploads/2023/03/Mostredoltremare-1.pdf；Unica 博士论文｜https://iris.unica.it/retrieve/e2f56ed8-4a1d-3eaf-e053-3a05fe0a5d97/PhD_Thesis_PisanuMaddalena.pdf",
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
    canvas = Image.new("RGBA", (W, H), rgba("#e6edf0"))
    draw = ImageDraw.Draw(canvas)
    dark, accent = CFG["dark"], CFG["accent"]
    draw.rectangle((0, 0, W, H), fill="#e6edf0")
    draw.rectangle((0, 0, W, 146), fill=dark)
    draw.text((68, 56), CFG["issue"], font=font(FONT_BOLD, 24), fill=LIGHT)
    draw.text((1170, 58), CFG["date"], font=font(FONT_SANS, 19), fill=rgba(LIGHT, 190), anchor="ra")
    draw.text((68, 198), "单期主线｜坡地与公共空间", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (68, 260), "坡地也能\n成为广场", 670, 235, 72, dark, serif=True, spacing=18)
    draw.line((68, 560, 1170, 560), fill=rgba(dark, 115), width=3)
    draw_fit(draw, (68, 610), CFG["question"], 1060, 210, 43, dark, serif=True, spacing=15)
    cover = ImageEnhance.Sharpness(Image.open(src / CFG["cover"]).convert("RGB")).enhance(1.30)
    mount(canvas, cover, (748, 892, 362, 390), True)
    draw.rectangle((68, 900, 680, 1292), fill=dark)
    draw.text((110, 946), "11 米高差", font=font(FONT_BOLD, 38), fill="#f3c56e")
    draw_fit(draw, (110, 1022), CFG["thesis"], 510, 235, 35, LIGHT, serif=True, spacing=13)
    draw.rectangle((0, 1385, W, H), fill=accent)
    draw_fit(draw, (68, 1440), "把高差设计成可抵达、可停留、可连接的剖面。", 1050, 80, 34, LIGHT, serif=True, spacing=9)
    draw.text((68, 1560), "Casabella-Costruzioni｜第133期原刊封面｜1939年1月", font=font(FONT_SANS, 19), fill=rgba(LIGHT, 205))
    mark(draw, 1, True)
    return save_rgb(canvas, out / "01.jpg")


def make_summary(out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#e6edf0"))
    draw = ImageDraw.Draw(canvas)
    header(draw, 10)
    draw.text((68, 186), "把高差做成\n公共空间", font=font(FONT_BOLD, 60), fill=CFG["dark"], spacing=12)
    draw_fit(draw, (680, 210), CFG["summary"], 465, 385, 38, CFG["dark"], serif=True, spacing=15)
    draw.line((622, 650, 622, 1370), fill=CFG["accent"], width=9)
    y = 690
    for i, (label, body) in enumerate(zip(CFG["concepts"], CFG["takeaways"]), 1):
        draw.ellipse((574, y - 12, 670, y + 84), fill=CFG["accent"])
        draw.text((622, y + 34), f"{i}", font=font(FONT_BOLD, 31), fill=LIGHT, anchor="mm")
        left = 68 if i % 2 else 690
        width = 438
        draw.text((left, y), label, font=font(FONT_BOLD, 36), fill=CFG["dark"])
        draw_fit(draw, (left, y + 62), body, width, 175, 27, rgba(CFG["dark"], 215), serif=True, spacing=9)
        y += 238
    draw.rectangle((68, 1430, 1174, 1494), fill=CFG["dark"])
    draw.text((96, 1446), "真正的坡地建筑，会让每一个标高都值得抵达。", font=font(FONT_BOLD, 29), fill=LIGHT)
    draw.text((68, 1534), "Casabella-Costruzioni｜第133期坡地建筑讨论｜1939年1月", font=font(FONT_SANS, 19), fill=rgba(CFG["dark"], 195))
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
