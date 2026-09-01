from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
W, H = 1242, 1660
PAPER = "#eee9df"
LIGHT = "#f8f4eb"
INK = "#12161a"
BLUE = "#173b53"
ORANGE = "#ea6c36"
MUTED = "#77736c"
SAND = "#c9aa72"
GREEN = "#71816f"

FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"


ISSUES = [
    {
        "slug": "casabella-101",
        "big_number": "101",
        "issue": "CASABELLA 101",
        "date": "MAGGIO 1936 · ANNO IX",
        "cover": "book-cover.jpg",
        "question": "工业城市，如何让\n工作与生活\n不再分离？",
        "thesis_label": "生产 × 服务 × 生活",
        "thesis": "城市规划不只安排建筑，还要把生产、居住、公共服务和日常交通组织成一个可生活的整体。",
        "summary": "现代工业城市的质量，不在工厂有多大，而在生产、居住、服务与街道之间是否形成连续的生活系统。",
        "concepts": ["生产组织", "公共服务", "日常生活"],
        "takeaways": [
            "规划工业新区时，住宅与公共服务必须和工厂同步出现。",
            "改造旧建筑时，让新旧差异可见，也能形成统一空间秩序。",
            "标准化负责效率，公共空间负责把个体连接成社区。",
        ],
        "cards": [
            {
                "image": "02-ivrea-plan.jpg", "mode": "document", "accent": ORANGE,
                "source": "Luigi Figini / Gino Pollini｜Piano di un quartiere nuovo a Ivrea｜Casabella 101, pp. 6—11",
                "eyebrow": "观点 01｜城市不是工厂的附属物",
                "title": "把生产、居住与公共服务放进同一张规划图",
                "body": "Ivrea的新区计划把工厂视为城市发动机，但住宅、交通与公共设施必须同时布局，工业扩张才不会制造碎片化郊区。",
            },
            {
                "image": "03-worker-services.jpg", "mode": "document", "accent": GREEN,
                "source": "Adriano Olivetti｜Architettura al servizio sociale｜Casabella 101, pp. 11—12",
                "eyebrow": "观点 02｜公共服务是空间骨架",
                "title": "住宅之外，托育与集体设施决定社区能否成立",
                "body": "工人住宅可以使用可重复单元，但社区质量不只来自标准化住房；托育、开放空间与步行联系共同构成日常支持系统。",
            },
            {
                "image": "04-villa-borletti.jpg", "mode": "document", "accent": ORANGE,
                "source": "Ignazio Gardella / Raffaello Giolli｜Villa Borletti · Sistemazioni nuove｜Casabella 101, pp. 12—17",
                "eyebrow": "观点 03｜改造不是抹去旧建筑",
                "title": "新体量可以贴着旧房生长，而不必复制旧形式",
                "body": "Gardella在旧别墅外侧加入水平、轻薄的现代空间，以玻璃和连续界面连接花园；新旧差异被保留，却形成新的整体。",
            },
            {
                "image": "05-villa-plans.jpg", "mode": "document", "accent": GREEN,
                "source": "Ignazio Gardella｜Villa Borletti · piante prima e dopo｜Casabella 101, pp. 12—17",
                "eyebrow": "观点 04｜模数统一不同空间",
                "title": "同一网格，让旧房间与新扩建获得连续秩序",
                "body": "扩建没有靠外形模仿旧宅，而是用模数重新对齐墙体、开间和玻璃界面；空间连续性来自比例关系，而不是历史装饰。",
            },
            {
                "image": "06-tabakfabrik.jpg", "mode": "photo", "accent": ORANGE, "focal": (0.50, 0.56),
                "source": "Peter Behrens / Alexander Popp｜Tabakfabrik Linz｜Casabella 101",
                "eyebrow": "观点 05｜工业建筑也需要城市尺度",
                "title": "连续采光带，把巨大厂房拆解成可读的水平秩序",
                "body": "弧形厂房、连续窗带与清楚的结构节奏同时回应生产效率和城市界面，让大体量不再只是封闭机器。",
            },
            {
                "image": "07-parker-shop.jpg", "mode": "document", "accent": ORANGE,
                "source": "Edoardo Persico / Marcello Nizzoli｜Negozio Parker, Milano｜Casabella 101",
                "eyebrow": "观点 06｜商店是街道的视觉界面",
                "title": "展示不靠堆满商品，而靠网格组织视线",
                "body": "Parker商店以细杆、透明界面和悬置展台形成三维框架，让品牌、商品与行人视线在同一空间发生关系。",
            },
        ],
    },
    {
        "slug": "casabella-102-103",
        "big_number": "102",
        "issue": "CASABELLA 102–103",
        "date": "GIUGNO–LUGLIO 1936 · ANNO IX",
        "cover": "book-cover.jpg",
        "question": "展览与工业建筑\n如何变成\n公共空间？",
        "thesis_label": "结构 × 流动 × 公共性",
        "thesis": "结构给出秩序，艺术建立记忆；人的流动让建筑进入公共生活。",
        "summary": "公共建筑和工业城市都不能只解决功能；结构、艺术与人的流动必须共同形成可识别、可参与的公共秩序。",
        "concepts": ["结构秩序", "人的流动", "公共生活"],
        "takeaways": [
            "展陈空间应把光、结构与艺术合成一个整体，而不是事后装饰。",
            "厂房、住宅和公共设施共享模数，城市才能高效扩展。",
            "复制建筑体系时，也要重新组织当地住房与公共生活。",
        ],
        "cards": [
            {
                "image": "02-persico-salone.jpg", "mode": "document", "accent": ORANGE,
                "source": "Edoardo Persico｜Profezia dell’architettura｜Casabella 102–103, pp. 2—5",
                "eyebrow": "观点 01｜艺术不是附加装饰",
                "title": "建筑、雕塑与光线，可以共同构成空间本体",
                "body": "Persico把艺术理解为空间构成的一部分：柱列控制节奏，光线强化深度，雕塑成为视线终点，三者共同建立建筑经验。",
            },
            {
                "image": "03-pagano-pavilion.jpg", "mode": "photo", "accent": ORANGE, "focal": (0.50, 0.56),
                "source": "Giuseppe Pagano｜Il nuovo padiglione · VI Triennale di Milano｜Casabella 102–103, pp. 6—13",
                "eyebrow": "观点 02｜公共性来自可聚集的边界",
                "title": "展馆不仅容纳展览，也要制造城市事件",
                "body": "展馆、露台与庭院共同形成开放边界；当人群可以停留、观看和穿行，建筑才从展品容器变成公共生活的舞台。",
            },
            {
                "image": "04-sala-vittoria.jpg", "mode": "photo", "accent": GREEN, "focal": (0.52, 0.48),
                "source": "Edoardo Persico / Giancarlo Palanti / Marcello Nizzoli｜Sala della Vittoria｜Casabella 102–103",
                "eyebrow": "观点 03｜重复构件制造仪式感",
                "title": "柱列、反射与终点雕塑，把行走变成空间叙事",
                "body": "连续竖向构件拉长透视，深色地面反射光线，Fontana雕塑固定终点；仪式感来自行走中的节奏变化。",
            },
            {
                "image": "05-zlin-aerial.jpg", "mode": "photo", "accent": ORANGE, "focal": (0.50, 0.50),
                "source": "Giuseppe Pagano｜L’architettura delle città industriali｜Casabella 102–103, pp. 28—29",
                "eyebrow": "观点 04｜工业城市也是完整城市",
                "title": "工厂、住宅和公共设施必须共享一套城市秩序",
                "body": "Zlín把生产区、交通、住房与公共建筑编进统一网络；效率不只发生在流水线上，也发生在城市各部分的邻接关系中。",
            },
            {
                "image": "06-zlin-1935.jpg", "mode": "photo", "accent": ORANGE, "focal": (0.50, 0.50),
                "source": "Attilio Podestà｜La città delle scarpe · Zlín｜Casabella 102–103, pp. 24—27",
                "eyebrow": "观点 05｜标准化可以跨越尺度",
                "title": "同一模数，从厂房结构扩展到整座城市",
                "body": "Baťa体系以规则柱网、砖填充与重复开间快速建设厂房，再把同样的效率逻辑扩展到道路、住房与公共设施。",
            },
            {
                "image": "07-east-tilbury.jpg", "mode": "photo", "accent": GREEN, "focal": (0.54, 0.48),
                "source": "Mario Labò｜Colonie Bat’a all’estero · East Tilbury｜Casabella 102–103",
                "eyebrow": "观点 06｜复制体系也必须回应地方",
                "title": "海外工业聚落不能只复制工厂，还要组织住房与公共生活",
                "body": "East Tilbury延续Baťa的结构与生产体系，同时配置住宅、道路和社区设施；工业扩张由单体复制转向完整聚落建设。",
            },
        ],
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def rgba(color, alpha=255):
    value = color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def wrap(draw, text, used_font, max_width):
    lines = []
    for paragraph in str(text).splitlines():
        current = ""
        for char in paragraph:
            trial = current + char
            if current and draw.textbbox((0, 0), trial, font=used_font)[2] > max_width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
    return "\n".join(lines)


def draw_fit(draw, xy, text, width, height, start_size, fill, *, serif=False, bold=False, spacing=12):
    path = FONT_SERIF if serif else FONT_BOLD if bold else FONT_SANS
    for size in range(start_size, 15, -2):
        used = font(path, size)
        wrapped = wrap(draw, text, used, width)
        box = draw.multiline_textbbox(xy, wrapped, font=used, spacing=spacing)
        if box[3] - xy[1] <= height:
            draw.multiline_text(xy, wrapped, font=used, fill=fill, spacing=spacing)
            return box[3]
    raise ValueError(f"Text does not fit: {text[:30]}")


def fit_inside(image, size):
    scale = min(size[0] / image.width, size[1] / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


def cover_crop(image, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / image.width, th / image.height)
    nw, nh = round(image.width * scale), round(image.height * scale)
    image = image.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, round((nw - tw) * focal[0])))
    top = max(0, min(nh - th, round((nh - th) * focal[1])))
    return image.crop((left, top, left + tw, top + th))


def paper_canvas(seed):
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    draw = ImageDraw.Draw(canvas)
    random.seed(seed)
    for _ in range(150):
        y = random.randint(0, H - 1)
        x = random.randint(0, W - 60)
        draw.line((x, y, min(W, x + random.randint(35, 190)), y), fill=rgba(INK, random.randint(3, 9)), width=1)
    return canvas


def page_mark(draw, number, light=False):
    color = rgba(LIGHT if light else INK, 170)
    draw.text((1167, 1602), f"{number:02d} / 08", font=font(FONT_SANS, 21), fill=color, anchor="ra")


def header(draw, cfg, number, light=False):
    color = LIGHT if light else INK
    draw.text((68, 52), cfg["issue"], font=font(FONT_BOLD, 22), fill=color)
    draw.text((1170, 52), cfg["date"], font=font(FONT_SANS, 20), fill=rgba(color, 185), anchor="ra")
    draw.line((68, 96, 1170, 96), fill=rgba(color, 85), width=2)
    page_mark(draw, number, light)


def mount(canvas, image, box, shadow=True):
    x, y, w, h = box
    fitted = fit_inside(image, (w, h))
    px = x + (w - fitted.width) // 2
    py = y + (h - fitted.height) // 2
    if shadow:
        alpha = Image.new("L", (fitted.width + 50, fitted.height + 50), 0)
        ImageDraw.Draw(alpha).rectangle((14, 12, fitted.width + 34, fitted.height + 34), fill=110)
        alpha = alpha.filter(ImageFilter.GaussianBlur(14))
        shade = Image.new("RGBA", alpha.size, (0, 0, 0, 0))
        shade.putalpha(alpha)
        canvas.alpha_composite(shade, (px - 14, py - 8))
    frame = Image.new("RGBA", (fitted.width + 16, fitted.height + 16), rgba(LIGHT))
    frame.alpha_composite(fitted.convert("RGBA"), (8, 8))
    canvas.alpha_composite(frame, (px, py))


def source_strip(draw, text):
    draw.rounded_rectangle((68, 972, 1172, 1044), 5, fill=rgba(BLUE, 238))
    for size in range(18, 11, -1):
        used = font(FONT_SANS, size)
        if draw.textbbox((0, 0), text, font=used)[2] <= 1048:
            draw.text((94, 1008), text, font=used, fill=LIGHT, anchor="lm")
            break


def text_panel(canvas, cfg, number, card):
    panel_y = 1070
    canvas.alpha_composite(Image.new("RGBA", (W, H - panel_y), rgba(PAPER)), (0, panel_y))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((68, 1127, 80, 1525), fill=card["accent"])
    draw.text((112, 1120), card["eyebrow"], font=font(FONT_BOLD, 22), fill=card["accent"])
    bottom = draw_fit(draw, (112, 1180), card["title"], 1010, 175, 49, INK, serif=True, spacing=12)
    draw_fit(draw, (112, bottom + 28), card["body"], 990, 145, 27, rgba(INK, 205), spacing=9)
    page_mark(draw, number, False)


def make_cover(cfg, src, out):
    canvas = paper_canvas(100 + int(cfg["slug"].split("-")[-1].split("-")[0]))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 28, H), fill=BLUE)
    draw.rectangle((0, 0, W, 24), fill=ORANGE)
    draw.text((76, 76), f"{cfg['issue']} / 核心观点", font=font(FONT_BOLD, 23), fill=ORANGE)
    draw.text((76, 136), "GIUSEPPE PAGANO · DIRETTORE", font=font(FONT_SANS, 22), fill=MUTED)
    draw_fit(draw, (76, 228), cfg["question"], 610, 390, 73, INK, serif=True, spacing=10)
    draw.rectangle((76, 650, 570, 662), fill=ORANGE)
    draw.text((76, 698), cfg["issue"], font=font(FONT_BOLD, 35), fill=BLUE)
    draw.text((76, 752), cfg["date"].replace(" · ", "  ·  "), font=font(FONT_SANS, 22), fill=MUTED)
    cover = Image.open(src / cfg["cover"]).convert("RGB")
    cover = ImageEnhance.Sharpness(cover).enhance(1.35)
    mount(canvas, cover, (655, 395, 510, 600), True)
    draw.rounded_rectangle((72, 1254, 1170, 1516), 8, fill=rgba(BLUE, 246))
    draw.text((108, 1296), cfg["thesis_label"], font=font(FONT_BOLD, 22), fill=ORANGE)
    draw_fit(draw, (108, 1344), cfg["thesis"], 1010, 145, 34, LIGHT, serif=True, spacing=10)
    page_mark(draw, 1, False)
    path = out / "01.jpg"
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def make_card(cfg, src, out, number, card):
    canvas = Image.new("RGBA", (W, H), rgba(PAPER))
    image = Image.open(src / card["image"]).convert("RGB")
    if card["mode"] == "photo":
        image = cover_crop(image, (W, 1070), card.get("focal", (0.5, 0.5)))
        image = ImageEnhance.Contrast(image).enhance(1.04)
        canvas.alpha_composite(image.convert("RGBA"), (0, 0))
        canvas.alpha_composite(Image.new("RGBA", (W, 120), (0, 0, 0, 92)), (0, 0))
        draw = ImageDraw.Draw(canvas)
        header(draw, cfg, number, True)
    else:
        canvas.alpha_composite(Image.new("RGBA", (W, 1070), rgba(BLUE)), (0, 0))
        mount(canvas, image, (76, 138, 1090, 790), True)
        draw = ImageDraw.Draw(canvas)
        header(draw, cfg, number, True)
    source_strip(draw, card["source"])
    text_panel(canvas, cfg, number, card)
    path = out / f"{number:02d}.jpg"
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def make_summary(cfg, out):
    canvas = paper_canvas(800 + len(cfg["issue"]))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 28, H), fill=ORANGE)
    header(draw, cfg, 8, False)
    draw.text((74, 154), "建筑观点总结", font=font(FONT_BOLD, 23), fill=ORANGE)
    draw_fit(draw, (74, 238), cfg["summary"], 1080, 390, 61, INK, serif=True, spacing=20)
    x = 74
    for idx, (label, color) in enumerate(zip(cfg["concepts"], [ORANGE, SAND, GREEN])):
        width = 292
        draw.rounded_rectangle((x, 750, x + width, 830), 7, fill=color)
        draw.text((x + width / 2, 790), label, font=font(FONT_BOLD, 27), fill=INK, anchor="mm")
        if idx < 2:
            draw.line((x + width + 12, 790, x + width + 56, 790), fill=BLUE, width=4)
            draw.polygon([(x + width + 56, 790), (x + width + 40, 779), (x + width + 40, 801)], fill=BLUE)
        x += 368
    draw.rounded_rectangle((74, 932, 1168, 1475), 10, fill=rgba(BLUE, 248))
    y = 1000
    for idx, item in enumerate(cfg["takeaways"], 1):
        draw.rounded_rectangle((112, y, 172, y + 60), 8, fill=ORANGE)
        draw.text((142, y + 30), str(idx), font=font(FONT_BOLD, 27), fill=LIGHT, anchor="mm")
        draw_fit(draw, (204, y + 2), item, 900, 92, 29, LIGHT, serif=True, spacing=8)
        y += 142
    page_mark(draw, 8, False)
    path = out / "08.jpg"
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def make_preview(paths, out):
    tw, th, gap = 250, 334, 18
    sheet = Image.new("RGB", (4 * tw + 5 * gap, 2 * th + 3 * gap), "#c8c3b9")
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(image, (gap + (i % 4) * (tw + gap), gap + (i // 4) * (th + gap)))
    sheet.save(out / "preview.jpg", quality=94, subsampling=0)


def render_issue(cfg):
    src = ROOT / "assets" / cfg["slug"]
    out = ROOT / "output" / cfg["slug"]
    out.mkdir(parents=True, exist_ok=True)
    paths = [make_cover(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(make_summary(cfg, out))
    make_preview(paths, out)
    print(f"Created {len(paths)} cards and preview in {out}")


if __name__ == "__main__":
    for issue in ISSUES:
        render_issue(issue)
