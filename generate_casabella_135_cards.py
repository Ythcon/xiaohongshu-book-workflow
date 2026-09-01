from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    FONT_BOLD, FONT_SANS, H, INK, LIGHT, PAPER, ROOT, W,
    cover_crop, draw_fit, font, mount, rgba,
)

CFG = {
    "slug": "casabella-135",
    "issue": "CASABELLA-COSTRUZIONI 135",
    "date": "MARZO 1939 | ANNO XII",
    "date_cn": "1939年3月",
    "accent": "#397c82",
    "dark": "#18313b",
    "paper2": "#edf3ef",
    "question": "酒店的舒适感不只在客房里；清洁、补给、通风和客人动线被分开组织，体验才会从入口一直稳定到床边。",
    "thesis": "第135期聚焦酒店的卫生设施。它讨论的并不只是浴缸、洗手台或瓷砖，而是如何把客人的休息、公共停留与后台清洁组织成互不打扰的系统。酒店真正的空间品质，首先来自一套看不见却始终有效的服务秩序。",
    "summary": "酒店空间不是客房数量的堆叠。先把抵达、停留与休息排成清晰的层次；再把卫生间、管线和清洁路线压缩为可重复的核心；最后用日光、通风和耐清洁的表面照顾每一次短暂使用。好住，是整套系统没有一环打扰另一环。",
    "concepts": ["公共与私密分层", "湿区集中成核心", "清洁路线不穿越客人"],
    "takeaways": [
        "入口、大堂、走廊和客房必须有明确的安静梯度。把最嘈杂的交流留在公共层，睡眠空间才不会被抵达与服务持续打断。",
        "将卫浴背靠背布置、统一给排水与排风位置，能减少管线长度，也让客房在不同楼层获得稳定、易维护的服务条件。",
        "布草、清洁与垃圾的路线不应借用客人走廊。后台独立，前台体验才会保持从容，也能减少互相看见与互相等待。",
    ],
    "publish_title": "CASABELLA135｜酒店好住靠什么",
    "publish_body": "Casabella-Costruzioni 135 讨论酒店卫生设施时，真正指向的是一个更大的问题：旅客为什么会觉得一间酒店“好住”？\n\n答案不只是一张舒适的床。入口、大堂、客房与卫生间需要有清楚的安静梯度；卫浴要作为能重复布置的服务核心；清洁、布草和补给则应有自己的路线，尽量不穿过客人正在休息或停留的空间。\n\n这套逻辑今天依然适用。无论是酒店、宿舍、康养空间还是长租公寓，最先该画的不是装饰效果，而是人在哪里抵达、湿区如何叠合、后台怎样进入。把这些看不见的关系理顺，房间才会真正安静、明亮且容易维护。\n\n你住过最舒服的酒店，最打动你的是房间本身，还是那些几乎察觉不到的细节？",
    "tags": "#Casabella #酒店设计 #酒店空间 #卫生间设计 #服务动线 #建筑历史 #室内设计 #旅宿设计",
    "cards": [
        {"image":"02-slavyanska.jpg", "focal":(0.50,0.43), "source":"A. Michailowski｜Slavjanska Beseda 酒店｜Casabella 135", "eyebrow":"观点 01｜酒店先给城市一张清楚的门脸", "title":"一层要承担抵达与识别，上部才适合安静休息；把街道、大堂和客房分层，酒店才能同时开放又不嘈杂", "body":"位于索菲亚中心的 Slavjanska Beseda 以街角体量建立清晰入口。酒店面向城市的一层要让人快速找到门、门厅和接待；真正需要安静的客房，则从公共街道向上退开。"},
        {"image":"03-albergo-moderno.jpg", "focal":(0.50,0.46), "source":"Albergo Moderno｜大堂与楼梯｜Casabella 135", "eyebrow":"观点 02｜大堂不是过道，而是停留的缓冲层", "title":"抵达之后先有一段可以坐下、等人和辨认方向的公共空间，客房层才能不被所有活动直接冲撞", "body":"大堂把城市的快节奏放慢：接待、短暂停留、会面与上楼在这里完成转换。楼梯、吧台和座位不应彼此抢路，而要让每个动作都有清楚的位置。"},
        {"image":"04-hotel-kamp-bathroom.jpg", "focal":(0.50,0.49), "source":"Helsinki City Museum｜Hotel Kämp 卫生间｜Casabella 135", "eyebrow":"观点 03｜卫浴要成为可重复的服务模块", "title":"把浴缸、洗手台、坐便器和通风集中进一套稳定尺寸，客房才能在不同楼层获得同样可靠的使用体验", "body":"一间好卫浴并不依赖面积夸张，而依赖器具之间的顺序。洗漱、如厕、沐浴各自有操作距离，维护点集中在同一侧；这种模块化才适合酒店的重复建设与长期管理。"},
        {"image":"05-domus-nova-bathroom.jpg", "focal":(0.48,0.52), "source":"Gio Ponti、Emilio Lancia｜Domus Nova 浴室｜Casabella 135", "eyebrow":"观点 04｜湿区必须从材料开始考虑清洁", "title":"墙地交接、台盆周边和易溅水的区域，材料应当连续、耐擦洗、易排水；卫生感来自细部而非装饰", "body":"瓷砖并不是卫生间的背景。它通过可冲洗的表面、清楚的收口和耐潮的基层，让短时间高频使用变得可控。酒店里的耐用，往往正是舒适最稳定的来源。"},
        {"image":"06-campo-imperatore.jpg", "focal":(0.50,0.44), "source":"Campo Imperatore 酒店｜公共休息厅｜Casabella 135", "eyebrow":"观点 05｜公共厅要用光线调节停留时间", "title":"大堂或休息厅不必全亮；让天窗、窗边和座位形成不同亮度，人自然会选择停留、阅读或继续前进", "body":"公共空间需要给客人不同速度。稳定的顶光建立整体方向，窗边适合短暂停留，较暗的边缘容纳安静会面；光线把大空间切成可被使用的小片段。"},
        {"image":"07-vai-lobby.jpg", "focal":(0.50,0.46), "source":"Léon Stynen｜接待大厅｜Casabella 135", "eyebrow":"观点 06｜接待台要看见入口，也要看见去处", "title":"前台不是一张孤立柜台；它应面对来客、看见电梯或楼梯，并给第一次到访的人一个马上能读懂的方向", "body":"接待是酒店最密集的信息节点。把柜台放在入口视线可及的位置，再让主要交通从旁边清楚展开，人不必反复询问；服务效率也会直接转化为安心感。"},
        {"image":"08-hotel-principe.jpg", "focal":(0.50,0.49), "source":"Hotel Principe di Savoia｜客房与卫浴｜Casabella 135", "eyebrow":"观点 07｜睡眠区与洗漱区要有一层缓冲", "title":"床边不应直接暴露给湿区；用门、前室或家具形成一段过渡，既保护私密，也让早晚的使用互不干扰", "body":"客房不是把所有功能摊在一个平面上。睡眠、换衣和洗漱的边界越清楚，同行者就越能在不同时间使用房间；小尺度空间也能保有体面与节奏。"},
        {"image":"09-french-bathroom.jpg", "focal":(0.50,0.48), "source":"1930年代酒店卫浴档案｜洗漱与排水｜Casabella 135", "eyebrow":"观点 08｜把清洁动作留在最短的路径里", "title":"水、毛巾、垃圾与清洁工具各有固定位置，使用者不必绕行，保洁也不必穿过最私密的区域", "body":"卫生空间的效率来自动作距离：进门先能挂放，洗手后可顺手取毛巾，沐浴区与排水点相邻。每一个动作少走一步，客人和保洁人员都更轻松。"},
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 135 原刊封面，1939年3月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/135-nz.jpg",
        "`02-slavyanska.jpg`｜Slavjanska Beseda，索菲亚｜Programata｜https://programata.bg/gradat/slavyanska-beseda/｜许可须在商业发布前复核；卡面裁切与文字排版",
        "`03-albergo-moderno.jpg`｜Albergo Moderno，大堂，Catanzaro，1935年｜Gazzetta del Sud｜https://catanzaro.gazzettadelsud.it/foto/cultura/2019/05/25/il-bauhaus-a-catanzaro-100-anni-fa-la-nascita-del-movimento-che-segno-la-storia-della-forma-1f782af6-b871-4d32-a8fe-b1c21e810831/｜许可须在商业发布前复核；卡面裁切与文字排版",
        "`04-hotel-kamp-bathroom.jpg`｜Hotel Kämp 卫生间，1930年代｜Helsingin kaupunki / Helsinki City Museum｜https://historia.hel.fi/fi/media/kuva/hotelli-kampin-kylpyhuone｜许可须在商业发布前复核；卡面裁切与文字排版",
        "`05-domus-nova-bathroom.jpg`｜Gio Ponti、Emilio Lancia，Domus Nova 浴室，1930年，摄影 Bombelli Girolamo｜Lombardia Beni Culturali｜https://www.lombardiabeniculturali.it/fotografie/schede/IMM-3u030-0017657/｜许可须在商业发布前复核；卡面裁切与文字排版",
        "`06-campo-imperatore.jpg`｜Campo Imperatore 酒店公共休息厅｜Foglie Viaggi｜https://www.foglieviaggi.cloud/blog-detail/post/225323/campo-imperatore-e-lalbergo-in-rovina-quando-labruzzo-sognò-una-svizzera-ditalia｜许可须在商业发布前复核；卡面裁切与文字排版",
        "`07-vai-lobby.jpg`｜Léon Stynen，1930年安特卫普装饰艺术展大厅｜Flanders Architecture Institute｜https://www.vai.be/en/collection/collection-highlights/foto-1｜许可须在商业发布前复核；卡面裁切与文字排版",
        "`08-hotel-principe.jpg`｜Hotel Principe di Savoia 客房与卫浴，1930年代｜图像出处待商业发布前复核｜https://i.pinimg.com/736x/2f/7d/21/2f7d21c2115246fb18c0f30c77adef5b.jpg",
        "`09-french-bathroom.jpg`｜1930年代法国卫生间档案照片｜图像出处待商业发布前复核｜https://i.ebayimg.com/images/g/rrIAAOSwMmdlNpG~/s-l1200.jpg",
        "文章与期号核验｜Casabella-Costruzioni 135，1939年3月；同期目录摘录记录“酒店卫生设施”主题｜Warszawa-Rok 1939年第4—5期书评｜https://bcpw.bg.pw.edu.pl/Content/2459/04ab1939_nr4-5.pdf；期号月份｜Casabella 官方年表｜https://casabellaweb.eu/the-magazine/yearannata-1939-xii/",
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
    draw.rounded_rectangle((68, 972, 1172, 1044), 5, fill=rgba(CFG["dark"], 242))
    draw_fit(draw, (94, 988), text, 1048, 34, 19, LIGHT, spacing=4)

def make_case(src: Path, out: Path, number: int, card: dict) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    image = cover_crop(Image.open(src / card["image"]).convert("RGB"), (W, 1070), card["focal"])
    canvas.alpha_composite(ImageEnhance.Contrast(image).enhance(1.05).convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 120), (0, 0, 0, 108)), (0, 0))
    draw = ImageDraw.Draw(canvas); header(draw, number, True); source_strip(draw, card["source"])
    canvas.alpha_composite(Image.new("RGBA", (W, H - 1070), rgba(CFG["paper2"])), (0, 1070))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((68, 1127, 80, 1525), fill=CFG["accent"])
    draw.text((112, 1120), card["eyebrow"], font=font(FONT_BOLD, 22), fill=CFG["accent"])
    bottom = draw_fit(draw, (112, 1180), card["title"], 1010, 175, 46, INK, serif=True, spacing=12)
    draw_fit(draw, (112, bottom + 28), card["body"], 990, 145, 26, rgba(INK, 205), spacing=9)
    mark(draw, number)
    return save_rgb(canvas, out / f"{number:02d}.jpg")

def make_cover(src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#dbe7e2")); draw = ImageDraw.Draw(canvas)
    dark, accent = CFG["dark"], CFG["accent"]
    draw.rectangle((0, 0, W, H), fill="#dbe7e2")
    draw.rectangle((0, 0, W, 146), fill=dark)
    draw.text((68, 56), CFG["issue"], font=font(FONT_BOLD, 24), fill=LIGHT)
    draw.text((1170, 58), CFG["date"], font=font(FONT_SANS, 19), fill=rgba(LIGHT, 190), anchor="ra")
    cover = ImageEnhance.Sharpness(Image.open(src / "book-cover.jpg").convert("RGB")).enhance(1.35)
    mount(canvas, cover, (78, 230, 470, 505), True)
    draw.rectangle((586, 180, 1174, 708), fill=dark)
    draw.text((632, 240), "单期主线｜酒店卫生与服务", font=font(FONT_BOLD, 22), fill="#a8e0d5")
    draw_fit(draw, (632, 304), "酒店好住\n靠什么？", 485, 190, 69, LIGHT, serif=True, spacing=16)
    draw_fit(draw, (632, 520), CFG["question"], 480, 150, 33, rgba(LIGHT, 225), serif=True, spacing=11)
    draw.line((68, 822, 1174, 822), fill=accent, width=9)
    draw.text((68, 878), "把看不见的服务，设计成看得见的舒适。", font=font(FONT_BOLD, 41), fill=dark)
    draw_fit(draw, (68, 962), CFG["thesis"], 1060, 260, 38, dark, serif=True, spacing=14)
    draw.rectangle((0, 1418, W, H), fill=dark)
    draw.text((68, 1480), "进入 → 停留 → 休息", font=font(FONT_BOLD, 37), fill="#a8e0d5")
    draw.text((68, 1560), "Casabella-Costruzioni｜第135期原刊封面｜1939年3月", font=font(FONT_SANS, 19), fill=rgba(LIGHT, 210))
    mark(draw, 1, True)
    return save_rgb(canvas, out / "01.jpg")

def make_summary(out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#dbe7e2")); draw = ImageDraw.Draw(canvas); header(draw, 10)
    draw.text((68, 190), "让酒店\n安静地运转", font=font(FONT_BOLD, 63), fill=CFG["dark"], spacing=12)
    draw_fit(draw, (636, 210), CFG["summary"], 510, 380, 37, CFG["dark"], serif=True, spacing=14)
    steps = [("抵达", "入口与前台清楚相见"), ("停留", "公共厅承接交流与等待"), ("休息", "客房与湿区保持安静秩序"), ("维护", "清洁与补给走独立后台")]
    y = 670
    for i, (a, b) in enumerate(steps, 1):
        draw.line((160, y + 48, 1082, y + 48), fill=rgba(CFG["dark"], 85), width=3)
        draw.ellipse((94, y, 226, y + 132), fill=CFG["accent"])
        draw.text((160, y + 66), f"{i}", font=font(FONT_BOLD, 38), fill=LIGHT, anchor="mm")
        draw.text((278, y + 10), a, font=font(FONT_BOLD, 42), fill=CFG["dark"])
        draw.text((278, y + 70), b, font=font(FONT_SANS, 29), fill=rgba(CFG["dark"], 210))
        y += 172
    draw.rectangle((68, 1422, 1174, 1492), fill=CFG["accent"])
    draw.text((96, 1440), "舒适不是装饰的结果，而是动线互不打扰。", font=font(FONT_BOLD, 29), fill=LIGHT)
    draw.text((68, 1534), "酒店卫生设施｜Casabella-Costruzioni 135｜1939年3月", font=font(FONT_SANS, 19), fill=rgba(CFG["dark"], 195))
    mark(draw, 10)
    return save_rgb(canvas, out / "10.jpg")

def make_preview(paths: list[Path], out: Path) -> None:
    tw, th, gap = 200, 267, 16
    sheet = Image.new("RGB", (5 * tw + 6 * gap, 2 * th + 3 * gap), "#b9c7c2")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(image, (gap + (i % 5) * (tw + gap), gap + (i // 5) * (th + gap)))
    sheet.save(out / "preview.jpg", quality=94, subsampling=0)

def manifest() -> dict:
    return {"type":"magazine","slug":CFG["slug"],"issue":CFG["issue"].title(),"date":CFG["date_cn"],"core_question":CFG["question"],"core_thesis":CFG["thesis"],"pages":[f"01 单期主线：{CFG['question']}", *[f"{i:02d} {c['source']}：{c['title']}" for i,c in enumerate(CFG['cards'],2)], f"10 总结：{'；'.join(CFG['concepts'])}"]}

def render() -> None:
    src, out = ROOT / "assets" / CFG["slug"], ROOT / "output" / CFG["slug"]
    out.mkdir(parents=True, exist_ok=True)
    paths = [make_cover(src, out)] + [make_case(src, out, i, card) for i, card in enumerate(CFG["cards"], 2)] + [make_summary(out)]
    make_preview(paths, out)
    (out / "发布文案.md").write_text(f"{CFG['publish_title']}\n\n{CFG['publish_body']}\n\n{CFG['tags']}\n", encoding="utf-8")
    (out / "图片来源.md").write_text(f"# {CFG['issue'].title()} 图片来源\n\n" + "\n".join(f"- {s}" for s in CFG["sources"]) + "\n", encoding="utf-8")
    post = ROOT / "posts" / CFG["slug"]; post.mkdir(parents=True, exist_ok=True)
    (post / "post.json").write_text(json.dumps(manifest(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(paths)} cards in {out}")

if __name__ == "__main__":
    render()
