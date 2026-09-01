from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    FONT_BOLD, FONT_SANS, H, INK, LIGHT, PAPER, ROOT, W,
    cover_crop, draw_fit, font, mount, rgba,
)


CFG = {
    "slug": "casabella-131",
    "issue": "CASABELLA-COSTRUZIONI 131",
    "date": "NOVEMBRE 1938 | ANNO XI",
    "date_cn": "1938年11月",
    "cover": "book-cover.jpg",
    "accent": "#b8454c",
    "dark": "#273555",
    "paper2": "#ebe6da",
    "question": "广场不是建筑之间剩下的空地；它要同时安排抵达、穿越、停留与朝向城市的视线。",
    "thesis": "第131期以 Attilio Podestà 的热那亚 Foce 海滨新广场为线索。广场并非在建筑盖完后再填进去的空白，而是先用边界、路径、地面与临街功能，把海岸城市的公共生活组织出来。",
    "summary": "131期提出了一个仍然锋利的问题：城市怎样把一块土地变成公共场所？答案不在单一地标，而在开放面的大小、到达方式、建筑首层与街道的连续性。好的广场让不同速度的人相遇，也让海、街区与日常服务互相可见。",
    "concepts": ["先留出可用的空", "让边界持续工作", "让路径交汇而不打架"],
    "takeaways": [
        "先确定可走、可站、可集会的连续地面，再安排周边体量。空出来的地方必须有尺度、朝向和到达方式，才会成为广场。",
        "建筑首层、骑楼、店面和树荫共同定义广场边缘。边界越能停留、进出与观看，中心就越不需要依赖一座夸张的纪念物。",
        "把步行、车行、临停和观景的速度分层布置。广场不怕人多，怕的是所有路线在同一个狭窄节点互相争抢。",
    ],
    "publish_title": "CASABELLA131｜广场不是空地",
    "publish_body": "Casabella-Costruzioni 131 讨论热那亚 Foce 的海滨新广场。它提醒我们：广场不是在楼盖完以后留下的一片空白，而是一套先行的城市结构——人从哪里进入，车在哪里减速，街道怎样通向海，建筑首层又如何接住停留和日常服务。\n\n从旧海岸、船厂到新广场与连续住宅，Foce 的变化让“空地”变得具体：边界需要连续，地面需要可走，临街首层需要有用，远处的风景也要被保留为公共视线。真正的公共空间不是摆一座地标，而是让不同速度的人都能自然找到位置。\n\n做社区入口、校园前场或商业街更新时，可以先画出四件事：步行线、车行线、停留面和首层开口。它们处理清楚，广场才会开始发生生活。你身边哪一座广场最愿意让人停下来？",
    "tags": "#Casabella #公共空间 #城市设计 #广场设计 #热那亚 #建筑历史 #空间设计 #现代建筑",
    "cards": [
        {"image":"02-foce-plan.jpg", "focal":(0.49,0.49), "source":"Attilio Podestà｜Foce 海滨新广场｜Casabella 131", "eyebrow":"观点 01｜先把公共空地画出来", "title":"广场要先被当作一块完整的城市地面规划；周边建筑、海岸道路与入口都围绕它校准", "body":"Foce 的海滨广场方案把开放面当成总体布局的起点。不是把楼摆满后再找余地，而是先确认公共空间的尺度、朝向与边界，城市才有共同的会合面。"},
        {"image":"03-vittoria-1930.jpg", "focal":(0.50,0.47), "source":"城市档案｜Piazza della Vittoria｜Casabella 131", "eyebrow":"观点 02｜大尺度也要可被步行读懂", "title":"开阔场地不能只服务远观：用连续边界、树列与可辨识的步行方向，让人在其中知道该往哪里走", "body":"一片很大的广场容易让人失去方向。沿边的建筑、绿化和道路需要给出稳定参照；走路的人能读出入口和目的地，开放面才不会只是交通缝隙。"},
        {"image":"04-vittoria-1933.jpg", "focal":(0.50,0.46), "source":"城市档案｜Piazza della Vittoria｜Casabella 131", "eyebrow":"观点 03｜让快慢两种流线并存", "title":"电车、汽车与步行可以共享一片城市前场，但要让每一种速度拥有清楚的线位和过渡", "body":"公共空间不等于拒绝交通。关键是把穿越与停留区分开：快的流线沿边通过，慢的流线靠近树荫、店面和入口展开；人不必在车流中寻找空隙。"},
        {"image":"05-foce-shore.jpg", "focal":(0.52,0.48), "source":"城市档案｜Foce 海岸线｜Casabella 131", "eyebrow":"观点 04｜改造前先看原有地景", "title":"海岸不是待填平的背景；旧海滩、堤岸与城市坡地共同决定新广场该朝哪里开口、留多大视线", "body":"Foce 原有的海岸与坡地提醒人们，公共空间从来不是抽象平面。面对水、风和起伏地形，广场需要把远景留在人的视线里，才能成为城市向外展开的窗口。"},
        {"image":"06-foce-shipyard.jpg", "focal":(0.50,0.48), "source":"城市档案｜Foce 船厂地带｜Casabella 131", "eyebrow":"观点 05｜把工业边缘转成公共前沿", "title":"船厂与仓库留下的大尺度边界，不必只用围墙结束；它可以被转译成面向街区的步行面与公共界面", "body":"城市更新常从一条旧生产边界开始。与其把它封成背面，不如让沿街首层、步行线和开放地面接续起来；公共空间由此把曾经割裂的地区重新缝合。"},
        {"image":"07-foce-1912.jpg", "focal":(0.50,0.47), "source":"城市档案｜San Pietro alla Foce｜Casabella 131", "eyebrow":"观点 06｜让街道抵达水边", "title":"通向海岸的路线不该在最后一栋建筑前中断；把步行方向延续到水边，城市才能真正拥有海景与风", "body":"海滨城市的公共性取决于抵达，而不是地图上的距离。街道、巷口和公共地面若能连续抵达水边，海岸才属于每个步行者，而非只属于沿线建筑。"},
        {"image":"08-via-rimassa-1937.jpg", "focal":(0.51,0.44), "source":"城市档案｜Via Rimassa 住宅街｜Casabella 131", "eyebrow":"观点 07｜住宅立面也是广场的一部分", "title":"沿街住宅不该只是面向自己的窗；首层开口、退界与连续檐下空间决定公共面是否愿意被使用", "body":"广场的边界由日常建筑完成。住宅与街道之间若只剩一堵封闭墙，中心再漂亮也会显得空；能进、能看、能短暂停留的首层，才会让边缘持续有活力。"},
        {"image":"09-rossetti.jpg", "focal":(0.50,0.46), "source":"Luigi Carlo Daneri｜Piazza Rossetti 住宅｜Casabella 131", "eyebrow":"观点 08｜体量之间必须留下城市距离", "title":"高层住宅围合公共空间时，楼间距离不是剩余量；它要容纳日照、风、视线、店面与穿行的路", "body":"Piazza Rossetti 的长条住宅把居住、底层商业与开阔地面并置。建筑越高，越要用清楚的退距和开放首层换取空气、可见性与行走的余地。"},
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 131 原刊封面，1938年11月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/131-nz.jpg",
        "`02-foce-plan.jpg`｜Foce 原船厂海滨广场透视方案｜La Città Conquistatrice｜https://www.cittaconquistatrice.it/genova-e-la-city-fascista/｜许可待商业发布前复核｜裁切与文字排版",
        "`03-vittoria-1930.jpg`、`04-vittoria-1933.jpg`｜Piazza della Vittoria 历史明信片｜C'era una volta Genova，Giovanni Assereto 收藏｜https://ceraunavoltagenova.blogspot.com/2013/05/piazza-verdi-e-piazza-della-vittoria_29.html；https://ceraunavoltagenova.blogspot.com/2013/05/piazza-della-vittoria-e-copertura-del.html｜许可待商业发布前复核｜裁切与文字排版",
        "`05-foce-shore.jpg`、`06-foce-shipyard.jpg`｜Foce 海岸与船厂历史明信片｜C'era una volta Genova，Giovanni Assereto 收藏｜https://ceraunavoltagenova.blogspot.com/2013/04/cera-una-volta-il-bisagno-parte-terza-i.html｜许可待商业发布前复核｜裁切与文字排版",
        "`07-foce-1912.jpg`｜San Pietro alla Foce 历史明信片｜Il Mugugno Genovese｜https://www.ilmugugnogenovese.it/la-storia-dei-quartieri-la-foce/｜许可待商业发布前复核｜裁切与文字排版",
        "`08-via-rimassa-1937.jpg`｜Via Rimassa，Foce，1937年历史照片｜Studio Foto Cresta，经 Pinterest 图像索引｜https://www.pinterest.com/pin/288230444874253929/｜许可待商业发布前复核｜裁切与文字排版",
        "`09-rossetti.jpg`｜Luigi Carlo Daneri / Bagnasco，Piazza Rossetti - Case Alte alla Foce｜意大利文化部现代建筑普查｜https://censimentoarchitetturecontemporanee.cultura.gov.it/scheda-opera?id=4357｜许可待商业发布前复核｜裁切与文字排版",
        "文章核验｜Attilio Podestà《La sistemazione di una piazza nuova a Genova》，Casabella 131，1938年11月，第12–17页；该文对应 Genova Foce 的海滨新广场竞赛与建设背景｜意大利文化部现代建筑普查｜https://censimentoarchitetturecontemporanee.cultura.gov.it/scheda-opera?id=4357",
        "同期评论线索｜Giuseppe Pagano《Anche i giovani possono insegnare》，Casabella-Costruzioni 131，1938年11月｜Scribd 目录索引｜https://it.scribd.com/document/611046568/Casabella-131-1938",
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
    canvas.alpha_composite(ImageEnhance.Contrast(image).enhance(1.06).convert("RGBA"), (0, 0))
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
    canvas = Image.new("RGBA", (W, H), rgba("#d9dde6"))
    draw = ImageDraw.Draw(canvas)
    dark, accent = CFG["dark"], CFG["accent"]
    draw.rectangle((0, 0, W, 238), fill=dark)
    draw.text((68, 60), CFG["issue"], font=font(FONT_BOLD, 24), fill=LIGHT)
    draw.text((1170, 62), CFG["date"], font=font(FONT_SANS, 19), fill=rgba(LIGHT, 190), anchor="ra")
    draw.text((68, 132), "单期主线｜公共空间", font=font(FONT_BOLD, 22), fill="#e8c87b")
    draw.rectangle((68, 292, 1174, 316), fill=accent)
    draw.text((68, 362), "广场不是空地", font=font(FONT_BOLD, 70), fill=dark)
    cover = ImageEnhance.Sharpness(Image.open(src / CFG["cover"]).convert("RGB")).enhance(1.28)
    mount(canvas, cover, (706, 430, 430, 462), True)
    draw.line((68, 452, 680, 452), fill=rgba(dark, 120), width=3)
    draw_fit(draw, (68, 494), CFG["question"], 610, 410, 50, dark, serif=True, spacing=17)
    draw.text((68, 942), "一块公共地面要同时处理", font=font(FONT_BOLD, 26), fill=accent)
    for i, label in enumerate(("抵达", "穿越", "停留", "观看")):
        x = 68 + i * 163
        draw.rectangle((x, 1010, x + 138, 1090), fill=dark if i % 2 == 0 else accent)
        draw.text((x + 69, 1035), label, font=font(FONT_BOLD, 27), fill=LIGHT, anchor="ma")
    draw.rectangle((0, 1180, W, H), fill="#bfc9d8")
    draw_fit(draw, (68, 1245), CFG["thesis"], 1050, 260, 45, dark, serif=True, spacing=16)
    draw.text((68, 1538), "Casabella-Costruzioni｜第131期原刊封面｜1938年11月", font=font(FONT_SANS, 19), fill=rgba(dark, 195))
    mark(draw, 1)
    return save_rgb(canvas, out / "01.jpg")


def make_summary(out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#f0eadc"))
    draw = ImageDraw.Draw(canvas)
    header(draw, 10)
    draw.text((68, 190), "一座广场的三条规则", font=font(FONT_BOLD, 47), fill=CFG["dark"])
    draw_fit(draw, (68, 278), CFG["summary"], 1060, 278, 42, CFG["dark"], serif=True, spacing=15)
    cols = [(68, 680, 394), (424, 680, 750), (780, 680, 1106)]
    colors = [CFG["dark"], CFG["accent"], "#6b856f"]
    for i, ((left, top, right), label, body, color) in enumerate(zip(cols, CFG["concepts"], CFG["takeaways"], colors), 1):
        draw.rectangle((left, top, right, 1330), fill=color)
        draw.text((left + 34, top + 36), f"0{i}", font=font(FONT_BOLD, 31), fill=rgba(LIGHT, 185))
        draw_fit(draw, (left + 30, top + 112), label, right - left - 60, 120, 35, LIGHT, serif=True, spacing=12)
        draw.line((left + 30, top + 280, right - 30, top + 280), fill=rgba(LIGHT, 120), width=2)
        draw_fit(draw, (left + 30, top + 320), body, right - left - 60, 300, 26, rgba(LIGHT, 230), serif=True, spacing=10)
    draw.rectangle((68, 1402, 1174, 1464), fill=CFG["accent"])
    draw.text((96, 1418), "广场的中心不是摆设，而是让城市关系发生的地面。", font=font(FONT_BOLD, 29), fill=LIGHT)
    draw.text((68, 1532), "Casabella-Costruzioni｜第131期城市空间讨论｜1938年11月", font=font(FONT_SANS, 19), fill=rgba(CFG["dark"], 195))
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
