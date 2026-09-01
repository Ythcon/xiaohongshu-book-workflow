from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    FONT_BOLD, FONT_SANS, H, INK, LIGHT, PAPER, ROOT, W,
    cover_crop, draw_fit, font, mount, rgba,
)


CFG = {
    "slug": "casabella-134",
    "issue": "CASABELLA-COSTRUZIONI 134",
    "date": "FEBBRAIO 1939 | ANNO XII",
    "date_cn": "1939年2月",
    "accent": "#b65437",
    "dark": "#263b48",
    "paper2": "#f1ede4",
    "question": "材料不是被贴标签的样品；用尺度、光线、路径与触摸，才能让人读懂它的质地、重量和用途。",
    "thesis": "第134期将“建造”与“展示”放在同一张桌面上讨论。1938—39年罗马意大利矿产展把材料编成可行走的场景：图纸、样品、墙面、灯光与行进顺序共同让资源从抽象名词变成身体可以判断的空间经验。",
    "summary": "材料展陈真正有效的地方，不在于堆满样品，而在于让人有机会比较、靠近、绕行和停留。把信息置于物件旁边，用光线显出表面，让结构组织路径，再给每一种材料留出观察距离；展览就会从说明书变成空间。",
    "concepts": ["先让材料可被比较", "用结构安排节奏", "让光线显示质地"],
    "takeaways": [
        "同类样品并列时，人的眼睛会主动识别颜色、颗粒和尺度差异。展陈先给比较关系，再补文字说明，材料才不会沦为孤立道具。",
        "柱、梁、柜台和天花不必退到背景。把它们排成可以预期的节奏，参观者便会自然知道该走向哪里、在哪一处放慢。",
        "面对粗糙、半透明或反光的表面，灯光要帮助材料显形。让亮度、阴影与观看角度不同，才能让质地真正被看见。",
    ],
    "publish_title": "CASABELLA134｜材料如何讲故事",
    "publish_body": "Casabella-Costruzioni 134 把一个今天仍然很有用的问题推到台前：材料怎样不靠标签，而靠空间自己说话？\n\n1938—39 年罗马的意大利矿产展给出了一种答案。平面把陈列分成连续的区域，背景墙、展柜、样品与照片不再各自独立；人在走动时能先看到整体，再靠近实物，最后在光线和尺度里判断材料的颗粒、重量与表面。\n\n这也提示今天的展览、材料馆与销售空间：不要急着把信息塞满墙面。先决定人如何进入、在哪儿停下、哪些样品需要并排、哪些表面必须被光照亮。材料被身体读懂之后，说明文字才会真正有用。\n\n如果要为一种材料设计展览，你会先让人看见它的哪一种特性？",
    "tags": "#Casabella #展陈设计 #材料设计 #空间叙事 #建筑历史 #展览空间 #室内设计 #建造",
    "cards": [
        {"image":"02-cement-plan.jpg", "focal":(0.50,0.50), "source":"Ugo Luccichenti｜水泥泥灰展亭平面｜Casabella 134", "eyebrow":"观点 01｜材料先要有一条可读的路线", "title":"展品不是散放在房间里；先用平面把观看顺序写清，人才能从整体走到细节", "body":"水泥泥灰展亭的平面把墙、展台与行走空间同时组织。先决定人从哪里进入、在哪些边缘绕行、怎样回望实物，信息和样品才会组成完整的空间句子。"},
        {"image":"03-cement-wall.jpg", "focal":(0.50,0.48), "source":"Ugo Luccichenti｜水泥泥灰展亭背景墙图｜Casabella 134", "eyebrow":"观点 02｜一面墙能同时承担信息与尺度", "title":"背景墙不是贴海报的底板；它应为实物提供尺度、方向与记忆点，让参观者知道自己正看什么", "body":"当图像、文字与样品共享一面有秩序的墙，观看就不必在碎片间跳跃。墙面先建立统一坐标，材料本身才会成为画面里最有分量的部分。"},
        {"image":"04-cement-installation.jpg", "focal":(0.52,0.46), "source":"Ugo Luccichenti｜水泥泥灰展亭展陈视图｜Casabella 134", "eyebrow":"观点 03｜用连续构件引导身体前进", "title":"柱列、顶棚和低展台形成重复节奏；人会沿着节奏移动，也会在节点前自然停下来", "body":"展厅里的构件不只是支撑。连续的竖向与水平线把长空间拆成可以读懂的段落，行走因此拥有速度变化；展品在每一段里获得恰当的注意力。"},
        {"image":"05-sulphur-display.png", "focal":(0.50,0.48), "source":"V. Aragozzini｜硫磺展陈｜Casabella 134", "eyebrow":"观点 04｜让图表回到真实样品旁边", "title":"数据、地图和照片负责说明范围；真正的矿物样品负责证明触感与尺度，两者必须在同一视线里相遇", "body":"抽象信息告诉人材料来自哪里、能做什么；实物让人判断它到底是什么。把两者放在连续界面上，知识不会停留在墙上，而会落到身体经验里。"},
        {"image":"06-agriculture-show.png", "focal":(0.50,0.45), "source":"Fondazione Fiera Milano｜农业展厅｜Casabella 134", "eyebrow":"观点 05｜给样品留出观看距离", "title":"展台过密会让物件彼此抵消；留出前后景和退步的距离，样品的轮廓、数量和重量才会显现", "body":"好的陈列不是把能摆的都摆上去。每组展品都需要一段空白作为缓冲，让人先看见组合，再靠近辨认局部；距离本身也是展陈的一种材料。"},
        {"image":"07-marble-show.jpg", "focal":(0.52,0.50), "source":"Montecatini｜石材展陈｜Casabella 134", "eyebrow":"观点 06｜并列让材料产生比较", "title":"石材最适合被并列观看：色泽、纹理、切割方式一旦同时出现，材料差异无需长篇解释", "body":"不要把每一块材料孤立成展品。让同类材料在统一尺度内成组出现，参观者会自动发现它们的共性与差异；比较比说明更快建立判断。"},
        {"image":"08-lead-zinc-1941.jpg", "focal":(0.48,0.50), "source":"Franco Albini｜铅锌展陈｜Casabella 134", "eyebrow":"观点 07｜展台要把材料带到人的高度", "title":"把样品抬到接近视线和手的高度，材料就不再是远处的标本，而能成为可被判断的对象", "body":"展台高度决定人与物的关系。低一点，人会俯看组合；高一点，表面会贴近眼睛。让高度服务于材料的颗粒、厚度或反光，而不是只追求整齐。"},
        {"image":"09-palazzo-esposizioni.jpg", "focal":(0.50,0.43), "source":"Eugenio Faludi｜Palazzo delle Esposizioni｜Casabella 134", "eyebrow":"观点 08｜先用光线建立展览的方向感", "title":"大空间里，均匀照亮并不等于清楚；让亮处标记重点、暗处托住背景，路径才会有方向", "body":"自然光和人工光都能安排注意力。把最需要判断质地的表面放在稳定亮度里，再让较暗的边缘承担过渡，参观者会更容易找到停留与前进的节奏。"},
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 134 原刊封面，1939年2月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/134-nz.jpg",
        "`02-cement-plan.jpg`、`03-cement-wall.jpg`、`04-cement-installation.jpg`｜Ugo Luccichenti，水泥泥灰展亭的平面、背景墙图与展陈视图，1938年｜Fondo Ugo Luccichenti / Accademia Nazionale di San Luca｜https://www.fondoluccichenti.org/elementi_online.php?id=26｜版权归档案馆；发布前须取得相应授权",
        "`05-sulphur-display.png`｜V. Aragozzini，硫磺展陈，1938年｜Cambridge University Press 图版｜https://static.cambridge.org/binary/version/id/urn%3Acambridge.org%3Aid%3Abinary%3A20260205013529760-0705%3AS1353294425100756%3AS1353294425100756_fig7.png?pub-status=live｜许可须在商业发布前复核",
        "`06-agriculture-show.png`｜1938年米兰农业展厅｜Fondazione Fiera Milano 档案｜https://backend.archiviofondazionefieramilano.archiui.it/cataloga/media/fieramilano/images/6/1/98364_ca_object_representations_media_6138_large.png｜许可须在商业发布前复核",
        "`07-marble-show.jpg`｜Montecatini 石材展陈，1936年｜Lombardia Beni Culturali｜https://www.lombardiabeniculturali.it/assets/immagini/liv2/AF310RLSUP/SC/F/3h080/0000/F_SUP-3h080-0000809_IMG-0001041428.jpg｜许可须在商业发布前复核",
        "`08-lead-zinc-1941.jpg`｜Franco Albini，铅锌展陈，1941年｜图像出处待商业发布前复核｜https://i.pinimg.com/originals/9b/ef/f2/9beff213dcfa989bde4e50f46846009d.jpg",
        "`09-palazzo-esposizioni.jpg`｜Eugenio Faludi，Palazzo delle Esposizioni，1937—38年｜Wearch｜https://www.wearch.eu/wp-content/uploads/2022/05/017faludi.jpg｜许可须在商业发布前复核",
        "文章核验｜Giuseppe Pagano《Architettura e costruzione》，Casabella-Costruzioni 134，1939年2月，第34—35页；《Premessa alla mostra autarchica del minerale italiano》，同刊，第6页。期号与月份核对｜Casabella 官方年表｜https://casabellaweb.eu/the-magazine/yearannata-1939-xii/",
    ],
}


def save_rgb(image: Image.Image, path: Path) -> Path:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def assemble_tiles(tile_dir: Path, level: int, cols: int, rows: int, size: tuple[int, int], target: Path) -> None:
    canvas = Image.new("RGB", (cols * 256, rows * 256), "#f4f1e9")
    for y in range(rows):
        for x in range(cols):
            tile = Image.open(tile_dir / f"{level}-{x}-{y}.jpg").convert("RGB")
            canvas.paste(tile, (x * 256, y * 256))
    canvas.crop((0, 0, size[0], size[1])).save(target, quality=96, subsampling=0)


def ensure_archive_assets(src: Path) -> None:
    assemble_tiles(src / "zoomify-01", 4, 9, 6, (2076, 1496), src / "02-cement-plan.jpg")
    assemble_tiles(src / "zoomify-02", 3, 8, 6, (1854, 1342), src / "03-cement-wall.jpg")
    assemble_tiles(src / "zoomify-03", 4, 9, 6, (2075, 1513), src / "04-cement-installation.jpg")


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
    canvas.alpha_composite(ImageEnhance.Contrast(image).enhance(1.06).convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 120), (0, 0, 0, 108)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    header(draw, number, True)
    source_strip(draw, card["source"])
    canvas.alpha_composite(Image.new("RGBA", (W, H - 1070), rgba(CFG["paper2"])), (0, 1070))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((68, 1127, 80, 1525), fill=CFG["accent"])
    draw.text((112, 1120), card["eyebrow"], font=font(FONT_BOLD, 22), fill=CFG["accent"])
    bottom = draw_fit(draw, (112, 1180), card["title"], 1010, 175, 46, INK, serif=True, spacing=12)
    draw_fit(draw, (112, bottom + 28), card["body"], 990, 145, 26, rgba(INK, 205), spacing=9)
    mark(draw, number)
    return save_rgb(canvas, out / f"{number:02d}.jpg")


def make_cover(src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#eee7da"))
    draw = ImageDraw.Draw(canvas)
    dark, accent = CFG["dark"], CFG["accent"]
    draw.rectangle((0, 0, W, 146), fill=dark)
    draw.text((68, 56), CFG["issue"], font=font(FONT_BOLD, 24), fill=LIGHT)
    draw.text((1170, 58), CFG["date"], font=font(FONT_SANS, 19), fill=rgba(LIGHT, 190), anchor="ra")
    draw.text((68, 204), "单期主线｜材料与展览空间", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (68, 268), "材料如何\n讲故事", 620, 200, 74, dark, serif=True, spacing=16)
    cover = ImageEnhance.Sharpness(Image.open(src / "book-cover.jpg").convert("RGB")).enhance(1.35)
    mount(canvas, cover, (756, 204, 366, 394), True)
    draw.line((68, 614, 1170, 614), fill=rgba(dark, 125), width=3)
    draw_fit(draw, (68, 658), CFG["question"], 1050, 180, 41, dark, serif=True, spacing=15)
    plan = Image.open(src / "02-cement-plan.jpg").convert("RGB")
    plan = cover_crop(plan, (1104, 320), (0.5, 0.50))
    canvas.alpha_composite(plan.convert("RGBA"), (68, 920))
    canvas.alpha_composite(Image.new("RGBA", (1104, 320), (38, 59, 72, 118)), (68, 920))
    draw.text((104, 960), "展厅的平面不是后台图纸", font=font(FONT_BOLD, 34), fill=LIGHT)
    draw_fit(draw, (104, 1022), "它先规定观看、比较和停留的顺序，再让每一种材料在合适的距离里出现。", 700, 150, 32, LIGHT, serif=True, spacing=11)
    draw.rectangle((0, 1380, W, H), fill=accent)
    draw_fit(draw, (68, 1436), "让材料被看见，也让人有机会靠近它。", 1040, 72, 35, LIGHT, serif=True, spacing=9)
    draw.text((68, 1560), "Casabella-Costruzioni｜第134期原刊封面｜1939年2月", font=font(FONT_SANS, 19), fill=rgba(LIGHT, 210))
    mark(draw, 1, True)
    return save_rgb(canvas, out / "01.jpg")


def make_summary(out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#eee7da"))
    draw = ImageDraw.Draw(canvas)
    header(draw, 10)
    draw.text((68, 190), "让材料成为\n空间的主角", font=font(FONT_BOLD, 61), fill=CFG["dark"], spacing=12)
    draw_fit(draw, (68, 365), CFG["summary"], 1060, 230, 37, CFG["dark"], serif=True, spacing=14)
    y = 690
    for i, (label, body) in enumerate(zip(CFG["concepts"], CFG["takeaways"]), 1):
        draw.rounded_rectangle((68, y, 1174, y + 202), 18, fill="#f8f5ee", outline=rgba(CFG["dark"], 80), width=2)
        draw.ellipse((96, y + 36, 226, y + 166), fill=CFG["accent"])
        draw.text((161, y + 101), f"0{i}", font=font(FONT_BOLD, 35), fill=LIGHT, anchor="mm")
        draw.text((270, y + 34), label, font=font(FONT_BOLD, 36), fill=CFG["dark"])
        draw_fit(draw, (270, y + 88), body, 830, 86, 27, rgba(CFG["dark"], 215), serif=True, spacing=9)
        y += 226
    draw.rectangle((68, 1426, 1174, 1492), fill=CFG["dark"])
    draw.text((96, 1442), "材料要被理解，先要给身体一段正确的距离。", font=font(FONT_BOLD, 28), fill=LIGHT)
    draw.text((68, 1534), "Giuseppe Pagano｜Architettura e costruzione｜Casabella 134", font=font(FONT_SANS, 19), fill=rgba(CFG["dark"], 195))
    mark(draw, 10)
    return save_rgb(canvas, out / "10.jpg")


def make_preview(paths: list[Path], out: Path) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#c9c2b4")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(image, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(out / "preview.jpg", quality=94, subsampling=0)


def manifest() -> dict:
    return {"type":"magazine","slug":CFG["slug"],"issue":CFG["issue"].title(),"date":CFG["date_cn"],"core_question":CFG["question"],"core_thesis":CFG["thesis"],"pages":[f"01 单期主线：{CFG['question']}", *[f"{i:02d} {c['source']}：{c['title']}" for i,c in enumerate(CFG["cards"],2)], f"10 总结：{'；'.join(CFG['concepts'])}"]}


def render() -> None:
    src, out = ROOT / "assets" / CFG["slug"], ROOT / "output" / CFG["slug"]
    out.mkdir(parents=True, exist_ok=True)
    ensure_archive_assets(src)
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
