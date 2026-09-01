from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "richard-meier-color-books"
OUT = ROOT / "output" / "richard-meier-colors"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rgba(color, alpha=255):
    value = color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def cover_crop(img, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, round(nw * focal[0] - tw / 2)))
    top = max(0, min(nh - th, round(nh * focal[1] - th / 2)))
    return img.crop((left, top, left + tw, top + th))


def fit_inside(img, box):
    bw, bh = box
    scale = min(bw / img.width, bh / img.height)
    return img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)


def wrap_text(draw, text, fnt, max_width):
    lines, current = [], ""
    no_line_start = "，。；：！？、）》】”’"
    for ch in text:
        test = current + ch
        if current and draw.textbbox((0, 0), test, font=fnt)[2] > max_width:
            if ch in no_line_start:
                current += ch
                lines.append(current)
                current = ""
            else:
                lines.append(current)
                current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return "\n".join(lines)


def grid(draw, color, alpha=22, seed=11):
    random.seed(seed)
    for x in range(70, W, 92):
        draw.line((x, 0, x, H), fill=rgba(color, alpha), width=1)
    for y in range(70, H, 92):
        draw.line((0, y, W, y), fill=rgba(color, alpha), width=1)
    for _ in range(10):
        x = random.randint(40, W - 260)
        y = random.randint(50, H - 80)
        draw.line((x, y, x + random.randint(80, 260), y), fill=rgba(color, alpha + 16), width=2)


def save(canvas, group, name):
    folder = OUT / group
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def mount_book(canvas, cfg, position, box, border=10):
    cover = Image.open(SRC / "covers" / f"{cfg['slug']}.jpg").convert("RGB")
    cover = fit_inside(cover, box)
    x, y = position
    sw, sh = cover.width + 76, cover.height + 76
    shadow_alpha = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(shadow_alpha).rounded_rectangle(
        (22, 18, cover.width + 46, cover.height + 46), 8, fill=150
    )
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(23))
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha)
    canvas.alpha_composite(shadow, (x - 18, y - 9))
    mount = Image.new("RGBA", (cover.width + border * 2, cover.height + border * 2), rgba(cfg["mount"], 255))
    mount.alpha_composite(cover.convert("RGBA"), (border, border))
    canvas.alpha_composite(mount, (x, y))


def page_mark(draw, cfg, number, light=False):
    color = rgba("#ffffff", 190) if light else rgba(cfg["ink"], 150)
    draw.text((1168, 1592), f"0{number} / 06", font=font(FONT_SANS, 21), fill=color, anchor="ra")


def make_cover(cfg):
    base = Image.open(SRC / "ai" / f"{cfg['slug']}-base.png").convert("RGB")
    base = cover_crop(base, (W, H))
    base = ImageEnhance.Contrast(base).enhance(1.025)
    canvas = base.convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    title_fill = rgba(cfg["title_box"], cfg["title_alpha"])
    draw.rounded_rectangle((58, 54, 785, 557), radius=8, fill=title_fill)
    draw.rectangle((58, 54, 76, 557), fill=cfg["accent"])
    draw.text((104, 86), "ARCHITECT × BOOK / COLOR EDITION", font=font(FONT_BOLD, 23), fill=cfg["title_ink"])
    draw.text((104, 147), "理查德·迈耶", font=font(FONT_BOLD, 39), fill=cfg["title_ink"])
    draw.text((100, 210), cfg["han"], font=font(FONT_SERIF, 148), fill=cfg["accent"])
    draw.text((284, 285), cfg["volume"], font=font(FONT_SANS, 28), fill=cfg["title_ink"])
    draw.line((104, 390, 721, 390), fill=cfg["accent"], width=9)
    draw.text((104, 424), cfg["cover_line1"], font=font(FONT_SERIF, 35), fill=cfg["title_ink"])
    draw.text((104, 474), cfg["cover_line2"], font=font(FONT_SERIF, 35), fill=cfg["title_ink"])

    mount_book(canvas, cfg, cfg["cover_pos"], (445, 525))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((66, 1466, 1176, 1558), radius=6, fill=rgba(cfg["footer"], 226))
    draw.text((98, 1495), cfg["keywords"], font=font(FONT_BOLD, 26), fill=cfg["footer_ink"])
    page_mark(draw, cfg, 1, light=cfg["footer_light"])

    path = save(canvas, cfg["slug"], "01.jpg")
    save(canvas, cfg["slug"], "book-cover-composite.jpg")
    return path


def treatment(img, cfg):
    img = ImageEnhance.Contrast(img).enhance(cfg["contrast"])
    img = ImageEnhance.Color(img).enhance(cfg["saturation"])
    img = ImageEnhance.Brightness(img).enhance(cfg["brightness"])
    if cfg.get("photo_overlay"):
        overlay = Image.new("RGBA", img.size, rgba(cfg["photo_overlay"], cfg["photo_overlay_alpha"]))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img


def make_case(cfg, number, case):
    image = Image.open(SRC / "works" / case["source"]).convert("RGB")
    image = cover_crop(image, (W, 990), case.get("focal", (0.5, 0.5)))
    image = treatment(image, cfg)

    canvas = Image.new("RGBA", (W, H), cfg["panel"])
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 152), (0, 0, 0, 72)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=cfg["accent"])
    draw.rectangle((62, 54, 246, 110), fill=cfg["accent"])
    draw.text((81, 68), f"CASE 0{number - 1}", font=font(FONT_BOLD, 23), fill=cfg["accent_ink"])
    draw.text((1168, 68), case["meta"], font=font(FONT_SANS, 23), fill="#ffffff", anchor="ra")
    draw.rounded_rectangle((66, 856, 590, 944), radius=5, fill=rgba(cfg["footer"], 226))
    draw.text((91, 883), case["keyword"], font=font(FONT_BOLD, 24), fill=cfg["footer_ink"])

    draw.rectangle((0, 990, W, H), fill=cfg["panel"])
    grid(draw, cfg["grid"], cfg["grid_alpha"], number * 29 + len(cfg["slug"]))
    draw.rectangle((69, 1040, 81, 1520), fill=cfg["accent"])
    draw.text((116, 1037), case["title"], font=font(FONT_BOLD, 34), fill=cfg["text"])
    draw.text((1165, 1043), cfg["short_label"], font=font(FONT_SANS, 22), fill=cfg["muted"], anchor="ra")

    body_font = font(FONT_SERIF, 42)
    wrapped = wrap_text(draw, case["headline"], body_font, 980)
    draw.multiline_text((116, 1120), wrapped, font=body_font, fill=cfg["text"], spacing=17)

    cap_font = font(FONT_SANS, 23)
    caption = wrap_text(draw, case["caption"], cap_font, 960)
    draw.multiline_text((116, 1438), caption, font=cap_font, fill=cfg["muted"], spacing=8)
    draw.text((116, 1550), case["credit"], font=font(FONT_SANS, 17), fill=cfg["muted"])
    page_mark(draw, cfg, number, light=cfg["dark_panel"])
    return save(canvas, cfg["slug"], f"{number:02d}.jpg")


def make_summary(cfg):
    base = Image.open(SRC / "ai" / f"{cfg['slug']}-base.png").convert("RGB")
    base = cover_crop(base, (W, H))
    base = ImageEnhance.Color(base).enhance(0.48)
    base = ImageEnhance.Brightness(base).enhance(cfg["summary_brightness"])
    base = base.filter(ImageFilter.GaussianBlur(1.2))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba(cfg["summary_overlay"], cfg["summary_alpha"])))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=cfg["accent"])
    draw.rectangle((70, 68, 1170, 1580), outline=rgba(cfg["summary_ink"], 110), width=2)
    draw.text((108, 112), "ONE-SENTENCE BOOK NOTE", font=font(FONT_BOLD, 25), fill=cfg["summary_ink"])
    draw.text((108, 178), cfg["han"], font=font(FONT_SERIF, 124), fill=cfg["accent"])
    draw.text((276, 246), cfg["volume"], font=font(FONT_SANS, 27), fill=cfg["summary_ink"])
    draw.line((108, 352, 1129, 352), fill=cfg["accent"], width=10)

    statement_font = font(FONT_SERIF, 49)
    statement = wrap_text(draw, cfg["summary"], statement_font, 988)
    draw.multiline_text((108, 430), statement, font=statement_font, fill=cfg["summary_ink"], spacing=28)

    draw.rounded_rectangle((108, 1088, 1129, 1398), radius=8, fill=rgba(cfg["summary_box"], 236))
    draw.text((147, 1132), cfg["summary_tag"], font=font(FONT_BOLD, 26), fill=cfg["accent"])
    detail_font = font(FONT_SERIF, 36)
    detail = wrap_text(draw, cfg["summary_detail"], detail_font, 895)
    draw.multiline_text((147, 1200), detail, font=detail_font, fill=cfg["summary_box_ink"], spacing=16)
    draw.text((108, 1508), "编辑性概括｜非书中原句", font=font(FONT_SANS, 22), fill=cfg["summary_ink"])
    page_mark(draw, cfg, 6, light=cfg["summary_light"])
    return save(canvas, cfg["slug"], "06.jpg")


def make_preview(cfg, paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), cfg["preview_bg"])
    for i, path in enumerate(paths):
        img = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(img, (x, y))
    sheet.save(OUT / cfg["slug"] / "preview.jpg", quality=94, subsampling=0)


GROUPS = [
    {
        "slug": "gray", "han": "灰", "volume": "VOLUME 01 / 1964–1984", "short_label": "GRAY / EARLY GRAMMAR",
        "accent": "#777872", "accent_ink": "#ffffff", "ink": "#20211f", "text": "#20211f", "muted": "#71736f",
        "panel": "#eceae3", "grid": "#454741", "grid_alpha": 12, "mount": "#f7f5ee",
        "footer": "#1e201e", "footer_ink": "#f7f5ef", "footer_light": True,
        "title_box": "#f4f1e9", "title_alpha": 236, "title_ink": "#1d1f1d",
        "cover_line1": "从住宅出发，", "cover_line2": "一套空间语法正在形成。",
        "keywords": "网格 · 坡道 · 平面 · 光 · 住宅尺度", "cover_pos": (407, 908),
        "contrast": 1.04, "saturation": 0.28, "brightness": 1.04,
        "dark_panel": False, "summary_overlay": "#f0eee7", "summary_alpha": 190,
        "summary_brightness": 0.77, "summary_ink": "#20211f", "summary_light": False,
        "summary_box": "#f8f6ef", "summary_box_ink": "#20211f", "preview_bg": "#aaa9a4",
        "summary": "灰色卷记录迈耶如何从住宅与小型公共建筑中建立自己的语法：网格划分秩序，坡道组织观看，白色则把光影变成可读的空间结构。",
        "summary_tag": "GRAY IS A GRAMMAR IN FORMATION",
        "summary_detail": "灰不是缺少颜色，而是把注意力还给比例、路径与阴影；在早期作品里，迈耶先把方法练成了语言。",
        "cases": [
            {"source": "douglas-house.jpg", "title": "道格拉斯住宅", "meta": "密歇根｜1971–1973", "keyword": "SECTION / DESCENT",
             "headline": "房子嵌入陡坡，入口从高处进入，空间沿楼梯与平台逐层下降；剖面不是结果，而是组织观看湖景的叙事。",
             "caption": "白色框架把树、坡地与水面切成连续画面，住宅成为一条穿过地形的路径。", "credit": "PHOTO: Χριστίνα Κωστή / CC BY-SA 4.0", "focal": (0.50, 0.48)},
            {"source": "atheneum.jpg", "title": "新和谐雅典娜神庙", "meta": "印第安纳｜1975–1979", "keyword": "PROMENADE / VIEW",
             "headline": "坡道把游客从小镇历史引向河流与远景；移动中的视线被精确编排，建筑因此成为一段可被行走的说明。",
             "caption": "迈耶把住宅里的路径实验放大成公共建筑：观看、转折与抵达共同构成空间。", "credit": "PHOTO: Michael Gäbler / Public Domain", "focal": (0.53, 0.50)},
            {"source": "high-museum.jpg", "title": "高等艺术博物馆", "meta": "亚特兰大｜1980–1983", "keyword": "RAMP / INSTITUTION",
             "headline": "圆形中庭与连续坡道把早期住宅的层叠经验推向博物馆尺度，让参观路线成为建筑最清晰的公共骨架。",
             "caption": "白色不只是外观，它让曲面、开口和投影在强光下被逐一辨认。", "credit": "PHOTO: Marc Merlin / CC BY-SA 4.0", "focal": (0.48, 0.50)},
            {"source": "hartford-seminary.jpg", "title": "哈特福德神学院", "meta": "哈特福德｜1978–1981", "keyword": "PLANES / COMMUNITY",
             "headline": "平面、圆柱与切口围绕教学和交流展开，公共空间被夹在清晰的几何关系之间，形成既开放又有秩序的共同体。",
             "caption": "当几何开始承载机构生活，迈耶的“白色语法”也完成了从住宅到公共建筑的过渡。", "credit": "PHOTO: Daderot / Public Domain", "focal": (0.54, 0.49)},
        ],
    },
    {
        "slug": "black", "han": "黑", "volume": "VOLUME 02 / 1985–1991", "short_label": "BLACK / CIVIC SCALE",
        "accent": "#e32320", "accent_ink": "#ffffff", "ink": "#f6f5ef", "text": "#f6f5ef", "muted": "#a9aaa6",
        "panel": "#111210", "grid": "#ffffff", "grid_alpha": 10, "mount": "#f4f3ed",
        "footer": "#050505", "footer_ink": "#ffffff", "footer_light": True,
        "title_box": "#050505", "title_alpha": 224, "title_ink": "#ffffff",
        "cover_line1": "白色进入城市，", "cover_line2": "尺度与责任同时改变。",
        "keywords": "机构 · 中庭 · 公共路径 · 城市界面", "cover_pos": (404, 970),
        "contrast": 1.12, "saturation": 0.12, "brightness": 0.89,
        "dark_panel": True, "summary_overlay": "#090909", "summary_alpha": 210,
        "summary_brightness": 0.48, "summary_ink": "#ffffff", "summary_light": True,
        "summary_box": "#f4f3ed", "summary_box_ink": "#171817", "preview_bg": "#3b3b39",
        "summary": "黑色卷讲的是尺度转换：当住宅式构图进入博物馆、市政厅与媒体机构，迈耶用中庭、公共路径和光的反差把形式变成城市秩序。",
        "summary_tag": "BLACK MAKES WHITE PUBLIC",
        "summary_detail": "黑色背景让问题变得更清楚：建筑不再只是被观看的对象，而要组织人群、制度与城市中的共同生活。",
        "cases": [
            {"source": "applied-arts-frankfurt.jpg", "title": "法兰克福应用艺术博物馆", "meta": "法兰克福｜1979–1985", "keyword": "VILLA / GRID",
             "headline": "新馆以网格回应旧别墅与花园，把不同年代的建筑纳入同一条公共参观路线；秩序来自关系，而非抹平差异。",
             "caption": "迈耶的几何在这里承担“连接”的任务：旧与新、室内与花园被重新编排。", "credit": "PHOTO: FA2010 / Public Domain", "focal": (0.55, 0.52)},
            {"source": "des-moines.jpg", "title": "得梅因艺术中心扩建", "meta": "爱荷华｜1982–1985", "keyword": "ADDITION / DIALOGUE",
             "headline": "面对沙里宁与贝聿铭留下的既有建筑，扩建没有追求孤立的标志，而是用尺度、转折与光建立第三种对话。",
             "caption": "真正的公共建筑往往从“如何加入”开始，而不是从“如何显眼”开始。", "credit": "PHOTO: Des Moines Guy / CC BY-SA 3.0", "focal": (0.52, 0.50)},
            {"source": "hague-city-hall.jpeg", "title": "海牙市政厅与中央图书馆", "meta": "海牙｜1986–1995", "keyword": "ATRIUM / CIVIC STREET",
             "headline": "巨大的白色中庭像一条室内城市街道，把办事、阅读与穿行放进同一片公共光线里，制度空间因此获得开放的尺度。",
             "caption": "白色在黑色卷里不再轻盈：它必须承受城市流线与公共权力的重量。", "credit": "PHOTO: Frits De Jong / CC0", "focal": (0.50, 0.45)},
            {"source": "paley-beverly-hills.jpg", "title": "佩利媒体中心", "meta": "比佛利山庄｜1992–1996", "keyword": "MEDIA / THRESHOLD",
             "headline": "层叠立面、圆形入口与垂直交通把媒体档案转化成可进入的公共界面，建筑成为屏幕文化与城市街道之间的门槛。",
             "caption": "机构的身份不是贴在立面上的符号，而是由进入、停留与观看的顺序产生。", "credit": "PHOTO: Gary Minnaert / Public Domain", "focal": (0.50, 0.52)},
        ],
    },
    {
        "slug": "red", "han": "红", "volume": "VOLUME 03 / 1992–1999", "short_label": "RED / PUBLIC VISIBILITY",
        "accent": "#f04424", "accent_ink": "#ffffff", "ink": "#1e1b19", "text": "#1e1b19", "muted": "#755f55",
        "panel": "#f2e7dd", "grid": "#e83c21", "grid_alpha": 14, "mount": "#fff6ec",
        "footer": "#191615", "footer_ink": "#fff7ef", "footer_light": True,
        "title_box": "#f04424", "title_alpha": 230, "title_ink": "#fff8ef",
        "cover_line1": "几何成为舞台，", "cover_line2": "公共建筑获得城市能量。",
        "keywords": "文化 · 司法 · 广场 · 城市可见性", "cover_pos": (404, 877),
        "contrast": 1.08, "saturation": 0.55, "brightness": 1.00, "photo_overlay": "#ef4328", "photo_overlay_alpha": 16,
        "dark_panel": False, "summary_overlay": "#de351f", "summary_alpha": 183,
        "summary_brightness": 0.63, "summary_ink": "#fff8f1", "summary_light": True,
        "summary_box": "#fff2e8", "summary_box_ink": "#211b18", "preview_bg": "#9b402c",
        "summary": "红色卷记录迈耶的标志性公共时期：几何不再只是精确构图，而成为组织文化、司法与城市可见性的巨大框架。",
        "summary_tag": "RED MAKES ORDER VISIBLE",
        "summary_detail": "红色指向强度：当项目进入地标尺度，网格、坡道与白色体量开始面对广场、天际线和公共记忆。",
        "cases": [
            {"source": "getty-center.jpg", "title": "盖蒂中心", "meta": "洛杉矶｜1984–1997", "keyword": "CAMPUS / HORIZON",
             "headline": "山顶校园以网格、庭院和步行轴线组织多座文化设施；白色金属与洞石共同把城市远景纳入建筑秩序。",
             "caption": "地标性不来自单一造型，而来自一整套能够被行走、停留和反复辨认的空间系统。", "credit": "PHOTO: Michael Gäbler / CC BY 3.0", "focal": (0.52, 0.51)},
            {"source": "macba.jpg", "title": "巴塞罗那当代艺术博物馆", "meta": "巴塞罗那｜1987–1995", "keyword": "RAMP / PLAZA",
             "headline": "通透长廊与连续坡道把室内参观路线展示给城市，白色立面则与前方广场共同制造新的公共生活。",
             "caption": "博物馆并未封闭艺术，而是把移动的人群变成街区可以看见的事件。", "credit": "PHOTO: Victoriano Javier Tornel García / CC BY-SA 2.0", "focal": (0.50, 0.50)},
            {"source": "damato-courthouse.jpg", "title": "阿方斯·M·达马托法院", "meta": "纽约州｜1993–2000", "keyword": "JUSTICE / SEQUENCE",
             "headline": "圆形公共大厅、层层退进的法庭体量与清晰安检路径，把司法建筑的威严转换成可理解的进入顺序。",
             "caption": "公共性不是取消边界，而是让边界、方向与权力关系被清楚看见。", "credit": "PHOTO: Americasroof / CC BY-SA 3.0", "focal": (0.52, 0.50)},
            {"source": "stadthaus-ulm.jpg", "title": "乌尔姆市民中心", "meta": "乌尔姆｜1986–1993", "keyword": "CONTEXT / COUNTERPOINT",
             "headline": "白色曲面以当代尺度回应大教堂与历史广场：既不复制旧城，也不逃离现场，而是在差异中建立新的公共焦点。",
             "caption": "城市语境不是风格模仿，而是让新旧体量在同一个广场上相互校准。", "credit": "PHOTO: Peter Berger / CC BY-SA 3.0", "focal": (0.50, 0.50)},
        ],
    },
    {
        "slug": "white", "han": "白", "volume": "VOLUME 04 / 2000–2004", "short_label": "WHITE / LIGHT AS MEDIUM",
        "accent": "#9aa99f", "accent_ink": "#ffffff", "ink": "#27302c", "text": "#27302c", "muted": "#718079",
        "panel": "#f6f5f0", "grid": "#91a69b", "grid_alpha": 10, "mount": "#ffffff",
        "footer": "#e6e9e4", "footer_ink": "#27302c", "footer_light": False,
        "title_box": "#ffffff", "title_alpha": 228, "title_ink": "#27302c",
        "cover_line1": "白不是答案，", "cover_line2": "它是接收世界的表面。",
        "keywords": "天空 · 树影 · 仪式 · 反射 · 时间", "cover_pos": (403, 855),
        "contrast": 1.02, "saturation": 0.62, "brightness": 1.10,
        "dark_panel": False, "summary_overlay": "#f6f5f0", "summary_alpha": 194,
        "summary_brightness": 0.91, "summary_ink": "#27302c", "summary_light": False,
        "summary_box": "#ffffff", "summary_box_ink": "#27302c", "preview_bg": "#c8cbc6",
        "summary": "白色卷把“白”从风格推进为媒介：它接收天空、树影、宗教仪式与城市反射，让材料在变化的光中不断获得新的表情。",
        "summary_tag": "WHITE RECEIVES THE WORLD",
        "summary_detail": "如果只把迈耶理解为“白色建筑师”，会漏掉最重要的部分：白色真正关注的是光如何让空间发生变化。",
        "cases": [
            {"source": "jubilee-church.jpg", "title": "千禧教堂", "meta": "罗马｜1996–2003", "keyword": "SHELLS / SACRED LIGHT",
             "headline": "三片弧形壳体过滤方向、尺度与光线，礼拜空间不是由装饰定义，而由一天之中不断变化的明暗完成。",
             "caption": "曲面并非造型特技，它把天空变成室内最主要的宗教图像。", "credit": "PHOTO: Mm4mm / CC BY-SA 4.0", "focal": (0.50, 0.48)},
            {"source": "frieder-burda.jpg", "title": "弗里德·布尔达博物馆", "meta": "巴登-巴登｜2001–2004", "keyword": "PARK / DAYLIGHT",
             "headline": "细长体量藏入公园树木之间，侧光与顶光共同照亮展厅；建筑的白随着季节、雪与枝影改变。",
             "caption": "博物馆不是公园里的孤立物体，而是一块接收自然时间的明亮界面。", "credit": "PHOTO: Gerd Eichmann / CC BY-SA 4.0", "focal": (0.50, 0.50)},
            {"source": "arp-museum.jpg", "title": "阿普博物馆", "meta": "罗兰塞克｜2002–2007", "keyword": "JOURNEY / RHINE",
             "headline": "从旧车站、隧道、升降与桥梁到山顶新馆，参观被拉成长距离的旅程，莱茵河景观最终成为展览的一部分。",
             "caption": "白色新馆不是终点造型，而是把地形、移动与远景串联起来的最后一环。", "credit": "PHOTO: Wolkenkratzer / CC BY-SA 3.0", "focal": (0.50, 0.50)},
            {"source": "ara-pacis.jpg", "title": "和平祭坛博物馆", "meta": "罗马｜1995–2006", "keyword": "HISTORY / FILTERED LIGHT",
             "headline": "玻璃、遮阳与浅色石材为古代祭坛建立可调节的光环境，新馆的任务不是复古，而是重新安排观看历史的条件。",
             "caption": "现代白色框架与古代石刻并置，让时间差异保持清晰，又被同一片自然光连接。", "credit": "PHOTO: Marcvsrvs / CC BY-SA 3.0 + GFDL", "focal": (0.50, 0.50)},
        ],
    },
    {
        "slug": "blue", "han": "蓝", "volume": "RICHARD MEIER / 2003", "short_label": "BLUE / STAGE MAP",
        "accent": "#17589a", "accent_ink": "#ffffff", "ink": "#f4f6f7", "text": "#f5f7f8", "muted": "#bdcfdf",
        "panel": "#123d69", "grid": "#ffffff", "grid_alpha": 12, "mount": "#ffffff",
        "footer": "#0a2c4f", "footer_ink": "#ffffff", "footer_light": True,
        "title_box": "#0e4275", "title_alpha": 225, "title_ink": "#ffffff",
        "cover_line1": "把白色建筑放回天空，", "cover_line2": "一张2003年的阶段总图。",
        "keywords": "天空 · 反射 · 系统 · 全球坐标", "cover_pos": (397, 770),
        "contrast": 1.08, "saturation": 0.56, "brightness": 0.96, "photo_overlay": "#145794", "photo_overlay_alpha": 30,
        "dark_panel": True, "summary_overlay": "#0b3e71", "summary_alpha": 197,
        "summary_brightness": 0.60, "summary_ink": "#ffffff", "summary_light": True,
        "summary_box": "#f4f7f9", "summary_box_ink": "#17334b", "preview_bg": "#315f87",
        "summary": "蓝色特刊像一张阶段性总图：住宅、文化与宗教项目被放进同一套全球坐标中，“白色建筑”真正依赖的其实是天空、反射与精密系统。",
        "summary_tag": "BLUE REVEALS THE SYSTEM",
        "summary_detail": "蓝色把视线从建筑对象移向背景条件：同一种白，在洛杉矶、乌尔姆、罗马与不同年代的光里会变成不同建筑。",
        "cases": [
            {"source": "getty-center.jpg", "title": "盖蒂中心：天空作为第五立面", "meta": "洛杉矶｜阶段坐标 01", "keyword": "SKY / CAMPUS",
             "headline": "在蓝色视角里，山顶校园的关键不只是白色体量，而是建筑如何持续捕捉洛杉矶天空、山脊与城市地平线。",
             "caption": "同一项目在红卷谈公共地标，在蓝卷则被重新阅读为一套天空与远景系统。", "credit": "PHOTO: Michael Gäbler / CC BY 3.0", "focal": (0.52, 0.51)},
            {"source": "stadthaus-ulm.jpg", "title": "乌尔姆：城市坐标中的白", "meta": "乌尔姆｜阶段坐标 02", "keyword": "URBAN FIELD",
             "headline": "俯瞰视角揭示了白色体量并不孤立：它嵌在教堂、屋顶、广场与环形路径组成的密集城市坐标中。",
             "caption": "蓝色卷强调“定位”——建筑的意义来自它在更大场域中的精确位置。", "credit": "PHOTO: Peter Berger / CC BY-SA 3.0", "focal": (0.50, 0.50)},
            {"source": "jubilee-church.jpg", "title": "千禧教堂：曲面捕捉时间", "meta": "罗马｜阶段坐标 03", "keyword": "SHELL / TIME",
             "headline": "弧形壳体像光学仪器：天空亮度、太阳角度与阴影移动被转译为连续变化的宗教空间。",
             "caption": "蓝色不是教堂的颜色，而是它永远在回应的外部条件。", "credit": "PHOTO: Mm4mm / CC BY-SA 4.0", "focal": (0.50, 0.48)},
            {"source": "ara-pacis.jpg", "title": "和平祭坛：玻璃调节历史", "meta": "罗马｜阶段坐标 04", "keyword": "FILTER / REFLECTION",
             "headline": "玻璃幕墙、百叶与屋顶采光共同形成环境控制系统，让古代石刻在城市反射与稳定展陈之间保持平衡。",
             "caption": "当白色与玻璃被理解为系统，迈耶建筑的技术性才真正显现。", "credit": "PHOTO: Marcvsrvs / CC BY-SA 3.0 + GFDL", "focal": (0.50, 0.50)},
        ],
    },
]


def make_overview(all_paths):
    tw, th, gap = 180, 240, 18
    sheet = Image.new("RGB", (6 * tw + 7 * gap, 5 * th + 6 * gap), "#d2d1cd")
    for row, paths in enumerate(all_paths):
        for col, path in enumerate(paths):
            img = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
            sheet.paste(img, (gap + col * (tw + gap), gap + row * (th + gap)))
    sheet.save(OUT / "preview-all.jpg", quality=94, subsampling=0)


def main():
    all_paths = []
    for cfg in GROUPS:
        paths = [make_cover(cfg)]
        for number, case in enumerate(cfg["cases"], start=2):
            paths.append(make_case(cfg, number, case))
        paths.append(make_summary(cfg))
        make_preview(cfg, paths)
        all_paths.append(paths)
        print(f"Created {cfg['slug']}: {len(paths)} cards")
    # Overview follows the user's requested order: white, black, red, gray, blue.
    make_overview([all_paths[i] for i in (3, 1, 2, 0, 4)])
    print(f"Created 30 cards in {OUT}")


if __name__ == "__main__":
    main()
