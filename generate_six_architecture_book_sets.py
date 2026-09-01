from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "six-architecture-books"
OUT = ROOT / "output" / "six-architecture-books"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1242, 1660
FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"
FONT_BOLD = r"C:\Windows\Fonts\NotoSansCHI-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def color(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def crop_fill(image, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / image.width, th / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    x = max(0, min(image.width - tw, round(image.width * focal[0] - tw / 2)))
    y = max(0, min(image.height - th, round(image.height * focal[1] - th / 2)))
    return image.crop((x, y, x + tw, y + th))


def fit_inside(image, size):
    scale = min(size[0] / image.width, size[1] / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


def wrap(draw, text, font, max_width):
    lines = []
    forbidden = "，。；：！？、）》】”’"
    for paragraph in text.split("\n"):
        current = ""
        for ch in paragraph:
            test = current + ch
            if current and draw.textbbox((0, 0), test, font=font)[2] > max_width:
                if ch in forbidden:
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


def add_grid(draw, cfg, seed=1):
    random.seed(seed)
    grid = color(cfg["accent"], 24 if not cfg.get("dark") else 34)
    for x in range(70, W, 88):
        draw.line((x, 980, x, H), fill=grid, width=1)
    for y in range(1012, H, 88):
        draw.line((0, y, W, y), fill=grid, width=1)
    for _ in range(10):
        x, y = random.randint(60, W - 250), random.randint(1030, H - 70)
        draw.line((x, y, x + random.randint(70, 240), y), fill=color(cfg["accent"], 58), width=2)


def page_mark(draw, cfg, page, light=False):
    fill = color("#ffffff", 190) if light else color(cfg["muted"], 220)
    draw.text((1168, 1590), f"0{page} / 06", font=fnt(FONT_SANS, 20), fill=fill, anchor="ra")


def save(canvas, cfg, filename):
    folder = OUT / cfg["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def place_real_cover(canvas, cfg):
    cover = Image.open(SRC / "covers" / cfg["cover"]).convert("RGB")
    cover = fit_inside(cover, (430, 565))
    x = 621 - cover.width // 2
    y = 960
    shadow = Image.new("L", (cover.width + 100, cover.height + 100), 0)
    d = ImageDraw.Draw(shadow)
    d.rounded_rectangle((30, 24, cover.width + 62, cover.height + 62), 10, fill=165)
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    sh = Image.new("RGBA", shadow.size, (0, 0, 0, 0))
    sh.putalpha(shadow)
    canvas.alpha_composite(sh, (x - 30, y - 20))
    mount = Image.new("RGBA", (cover.width + 18, cover.height + 18), cfg["mount"])
    mount.alpha_composite(cover.convert("RGBA"), (9, 9))
    canvas.alpha_composite(mount, (x - 9, y - 9))


def make_cover(cfg):
    base = crop_fill(Image.open(SRC / "ai" / cfg["base"]).convert("RGB"), (W, H))
    base = ImageEnhance.Contrast(base).enhance(1.02)
    canvas = base.convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    panel_fill = color(cfg["cover_panel"], cfg["cover_alpha"])
    draw.rounded_rectangle((52, 48, 814, 565), radius=8, fill=panel_fill)
    draw.rectangle((52, 48, 70, 565), fill=cfg["accent"])
    draw.text((101, 84), "ARCHITECTURE × BOOK", font=fnt(FONT_BOLD, 23), fill=cfg["cover_ink"])
    draw.text((101, 142), cfg["designer"], font=fnt(FONT_BOLD, 47), fill=cfg["cover_ink"])
    title_font = fnt(FONT_SERIF, cfg.get("cover_title_size", 64))
    title = wrap(draw, cfg.get("cover_book", cfg["book"]), title_font, 650)
    draw.multiline_text((101, 229), title, font=title_font, fill=cfg["accent"], spacing=12)
    draw.line((101, 420, 748, 420), fill=cfg["accent"], width=8)
    draw.text((101, 453), cfg["cover_line"], font=fnt(FONT_SERIF, 31), fill=cfg["cover_ink"])
    draw.text((101, 505), cfg["cover_subline"], font=fnt(FONT_SANS, 22), fill=cfg["cover_ink"])
    place_real_cover(canvas, cfg)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((58, 1510, 1184, 1572), radius=5, fill=color(cfg["footer"], 232))
    draw.text((86, 1525), cfg["keywords"], font=fnt(FONT_BOLD, 22), fill=cfg["footer_ink"])
    page_mark(draw, cfg, 1, cfg.get("footer_light", False))
    save(canvas, cfg, "book-cover-composite.jpg")
    return save(canvas, cfg, "01.jpg")


def make_case(cfg, page, case):
    image = Image.open(SRC / "works" / case["file"]).convert("RGB")
    image = crop_fill(image, (W, 980), case.get("focal", (0.5, 0.5)))
    image = ImageEnhance.Contrast(image).enhance(cfg.get("contrast", 1.06))
    image = ImageEnhance.Color(image).enhance(cfg.get("saturation", 0.88))
    if cfg.get("photo_tint"):
        overlay = Image.new("RGBA", image.size, color(cfg["photo_tint"], cfg.get("photo_tint_alpha", 18)))
        image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    canvas = Image.new("RGBA", (W, H), cfg["panel"])
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 150), (0, 0, 0, 76)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 22, H), fill=cfg["accent"])
    draw.rectangle((62, 52, 254, 112), fill=cfg["accent"])
    draw.text((84, 69), f"CASE 0{page - 1}", font=fnt(FONT_BOLD, 22), fill=cfg["accent_ink"])
    draw.text((1168, 72), case["meta"], font=fnt(FONT_SANS, 22), fill="#ffffff", anchor="ra")
    draw.rounded_rectangle((66, 854, 600, 944), radius=5, fill=color(cfg["footer"], 228))
    draw.text((92, 880), case["keyword"], font=fnt(FONT_BOLD, 23), fill=cfg["footer_ink"])

    draw.rectangle((0, 980, W, H), fill=cfg["panel"])
    add_grid(draw, cfg, seed=page * 37 + len(cfg["slug"]))
    draw.rectangle((69, 1034, 81, 1522), fill=cfg["accent"])
    draw.text((116, 1032), case["title"], font=fnt(FONT_BOLD, 34), fill=cfg["text"])
    draw.text((1168, 1040), cfg["label"], font=fnt(FONT_SANS, 20), fill=cfg["muted"], anchor="ra")
    headline = wrap(draw, case["headline"], fnt(FONT_SERIF, 41), 988)
    draw.multiline_text((116, 1114), headline, font=fnt(FONT_SERIF, 41), fill=cfg["text"], spacing=17)
    caption = wrap(draw, case["caption"], fnt(FONT_SANS, 22), 960)
    draw.multiline_text((116, 1442), caption, font=fnt(FONT_SANS, 22), fill=cfg["muted"], spacing=7)
    draw.text((116, 1555), case["credit"], font=fnt(FONT_SANS, 16), fill=cfg["muted"])
    page_mark(draw, cfg, page, cfg.get("dark", False))
    return save(canvas, cfg, f"{page:02d}.jpg")


def make_summary(cfg):
    base = crop_fill(Image.open(SRC / "ai" / cfg["base"]).convert("RGB"), (W, H))
    base = ImageEnhance.Color(base).enhance(0.42)
    base = ImageEnhance.Brightness(base).enhance(cfg.get("summary_brightness", 0.74))
    base = base.filter(ImageFilter.GaussianBlur(1.1))
    canvas = base.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), color(cfg["summary_overlay"], cfg["summary_alpha"])))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 22, H), fill=cfg["accent"])
    draw.rectangle((68, 68, 1172, 1582), outline=color(cfg["summary_ink"], 105), width=2)
    draw.text((106, 112), "ONE-SENTENCE BOOK NOTE", font=fnt(FONT_BOLD, 24), fill=cfg["summary_ink"])
    draw.text((106, 176), cfg["designer"], font=fnt(FONT_BOLD, 42), fill=cfg["summary_ink"])
    draw.text((106, 244), cfg["book"], font=fnt(FONT_SERIF, 57), fill=cfg["accent"])
    draw.line((106, 354, 1134, 354), fill=cfg["accent"], width=9)
    statement = wrap(draw, cfg["summary"], fnt(FONT_SERIF, 49), 980)
    draw.multiline_text((106, 430), statement, font=fnt(FONT_SERIF, 49), fill=cfg["summary_ink"], spacing=28)
    draw.rounded_rectangle((106, 1102, 1134, 1397), radius=8, fill=color(cfg["summary_box"], 235))
    draw.text((144, 1142), cfg["summary_tag"], font=fnt(FONT_BOLD, 24), fill=cfg["accent"])
    detail = wrap(draw, cfg["summary_detail"], fnt(FONT_SERIF, 35), 900)
    draw.multiline_text((144, 1200), detail, font=fnt(FONT_SERIF, 35), fill=cfg["summary_box_ink"], spacing=15)
    draw.text((106, 1510), "编辑性概括｜非书中原句", font=fnt(FONT_SANS, 21), fill=cfg["summary_ink"])
    page_mark(draw, cfg, 6, cfg.get("summary_light", False))
    return save(canvas, cfg, "06.jpg")


def make_group_preview(cfg, paths):
    tw, th, gap = 372, 498, 28
    sheet = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), cfg["preview"])
    for i, path in enumerate(paths):
        img = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % 3) * (tw + gap)
        y = gap + (i // 3) * (th + gap)
        sheet.paste(img, (x, y))
    sheet.save(OUT / cfg["slug"] / "preview.jpg", quality=94, subsampling=0)


GROUPS = [
    {
        "slug": "fujimoto", "cover": "fujimoto.png", "base": "fujimoto-base.png",
        "designer": "藤本壮介", "book": "建筑诞生的时刻", "label": "SPACE AS RELATION",
        "accent": "#b8685d", "accent_ink": "#ffffff", "panel": "#f3eee5", "text": "#252320", "muted": "#736c65",
        "footer": "#2b2825", "footer_ink": "#fffaf2", "mount": "#fffdf8", "cover_panel": "#f7f2e9", "cover_alpha": 232, "cover_ink": "#27231f",
        "keywords": "原始的未来 · 模糊边界 · 渐变 · 关系 · 生长", "cover_line": "建筑不是被画出来，", "cover_subline": "它从身体、距离与边界之间逐渐显形。",
        "preview": "#d7c9bc", "summary_overlay": "#f0e8dc", "summary_alpha": 195, "summary_ink": "#29251f", "summary_box": "#fbf7ef", "summary_box_ink": "#29251f",
        "summary": "《建筑诞生的时刻》把设计理解为关系逐渐显形的过程：建筑不是先有造型再装入生活，而是从身体、距离、边界与环境的微小差异中生长出来。",
        "summary_tag": "ARCHITECTURE BEGINS BETWEEN THINGS", "summary_detail": "从巢穴与洞穴、房间与城市，到内外之间的连续梯度，藤本壮介让建筑保持未完成般的开放，让生活参与空间的最终定义。",
        "cases": [
            {"file": "fujimoto-house-n.jpg", "title": "House N", "meta": "大分，日本｜2008", "keyword": "NESTED SHELLS / GRADATION", "focal": (0.50, 0.52),
             "headline": "三层白色外壳并不把内外一刀切开，而是制造从街道、庭院到房间的连续梯度；家因此像城市，也像一片可以被占据的森林。",
             "caption": "“边界”被拆成多重距离：雨、风、视线与人的活动分别在不同层次发生。", "credit": "PHOTO SOURCE: Wikimedia Commons / N House Sou FUJIMOTO 03"},
            {"file": "fujimoto-final-wooden.jpg", "title": "Final Wooden House", "meta": "熊本，日本｜2008", "keyword": "STRUCTURE / FURNITURE / BODY", "focal": (0.50, 0.50),
             "headline": "巨大的木块同时是结构、墙、台阶、地板和家具；功能没有被固定命名，身体只能在攀爬、坐卧与穿行中不断重新解释空间。",
             "caption": "当建筑构件不再只承担一种角色，居住就从使用房间变成发现关系。", "credit": "PHOTO SOURCE: Wikimedia Commons / Final Wooden House 2008"},
            {"file": "fujimoto-house-before-house.jpg", "title": "House Before House", "meta": "宇都宫，日本｜2009", "keyword": "ROOMS / VILLAGE / SCATTER", "focal": (0.50, 0.50),
             "headline": "房间被拆成大小不同的白色盒子，像一座微型村落散落在树木之间；楼梯与屋顶把“房子之前”的原始聚居重新带回住宅。",
             "caption": "单体不再完整，关系才成为建筑：室内、屋顶、庭院和街道共同构成家。", "credit": "PHOTO SOURCE: Wikimedia Commons / House Before House 2009"},
            {"file": "fujimoto-arbre-blanc.jpg", "title": "L’Arbre Blanc", "meta": "蒙彼利埃，法国｜2019", "keyword": "BALCONY / BRANCH / CITY", "focal": (0.53, 0.55),
             "headline": "向城市伸出的巨大阳台像树枝，把私密住宅变成气候、景观与公共生活的接口；建筑的轮廓来自每户向外延伸的欲望。",
             "caption": "从小住宅到城市尺度，藤本依然用“之间”组织空间：室内与风景互相渗透。", "credit": "PHOTO SOURCE: Wikimedia Commons / L’Arbre Blanc"},
        ],
    },
    {
        "slug": "shinohara", "cover": "shinohara.png", "base": "shinohara-base.png",
        "designer": "筱原一男", "book": "住宅图面", "label": "HOUSE AS ART",
        "accent": "#0b8fc7", "accent_ink": "#ffffff", "panel": "#d9edf4", "text": "#102b38", "muted": "#4f7485", "dark": False,
        "footer": "#102a37", "footer_ink": "#ffffff", "mount": "#ffffff", "cover_panel": "#d8f0f8", "cover_alpha": 225, "cover_ink": "#102a37",
        "keywords": "住宅即艺术 · 图面 · 四种样式 · 混沌 · 抽象", "cover_line": "图纸不是建筑的说明，", "cover_subline": "而是空间秩序第一次被精确发明的现场。",
        "preview": "#78bed9", "summary_overlay": "#cce8f1", "summary_alpha": 182, "summary_ink": "#102a37", "summary_box": "#eaf7fb", "summary_box_ink": "#102a37",
        "summary": "《住宅图面》让住宅通过平面、剖面与细部重新成为思想：图纸不是建筑完成后的说明，而是空间秩序第一次被精确发明的现场。",
        "summary_tag": "A DRAWING IS AN ARCHITECTURAL THOUGHT", "summary_detail": "从伞之家象征性的单一空间，到后期公共建筑中城市混沌的抽象化，筱原一男始终把图面当作思想的压缩装置。",
        "cases": [
            {"file": "shinohara-umbrella.jpg", "title": "伞之家", "meta": "东京，日本｜1961", "keyword": "ONE ROOF / SYMBOLIC SPACE", "focal": (0.50, 0.49),
             "headline": "一把巨大木伞覆盖住宅，结构、象征与日常生活被收进同一个空间；住宅因此不是房间的集合，而是一种完整世界的缩影。",
             "caption": "第一种样式以日本传统为起点，却通过抽象几何把“传统”转化为现代空间。", "credit": "PHOTO SOURCE: Wikimedia Commons / Umbrella House, Vitra Campus"},
            {"file": "shinohara-centennial.jpg", "title": "东京工业大学百年纪念馆", "meta": "东京，日本｜1987", "keyword": "SUSPENDED FORM / MACHINE", "focal": (0.52, 0.52),
             "headline": "悬挑的银色楔体像被放大的机械部件，脱离地面又压向城市；住宅中的形式冲突被推到公共尺度，成为可被直接感知的张力。",
             "caption": "筱原后期不再追求静止的整体，而让不协调与碰撞成为都市建筑的真实。", "credit": "PHOTO SOURCE: Wikimedia Commons / Tokyo Tech Centennial Hall"},
            {"file": "shinohara-ukiyoe.jpg", "title": "日本浮世绘博物馆", "meta": "松本，日本｜1982", "keyword": "FRACTURE / DISCONTINUITY", "focal": (0.50, 0.52),
             "headline": "弧形、斜切与镜面被并置在低矮体量中，立面不再解释内部，而像城市碎片的拼贴；不连续性本身成为新的秩序。",
             "caption": "从住宅的封闭宇宙走向公共建筑，形式被允许保持冲突、陌生与多义。", "credit": "PHOTO SOURCE: Wikimedia Commons / Japan Ukiyo-e Museum"},
            {"file": "shinohara-kumamoto-police.jpg", "title": "熊本北警察署", "meta": "熊本，日本｜1990", "keyword": "CHAOS / PUBLIC SCALE", "focal": (0.50, 0.47),
             "headline": "悬浮玻璃盒与倾斜构件把稳定的机构建筑变成事件；筱原用精确几何容纳都市的混沌，让秩序与失衡同时成立。",
             "caption": "“第四种样式”不是放弃控制，而是把不可预测的城市现实纳入设计。", "credit": "PHOTO SOURCE: Wikimedia Commons / Kumamoto Police Station"},
        ],
    },
    {
        "slug": "kahn", "cover": "kahn.png", "base": "kahn-base.png",
        "designer": "路易·康", "book": "Complete Work 1935–1974", "label": "SILENCE AND LIGHT",
        "accent": "#8795a2", "accent_ink": "#ffffff", "panel": "#eee8dc", "text": "#2b2b29", "muted": "#716f69",
        "footer": "#313331", "footer_ink": "#f7f2e9", "mount": "#fbf7ef", "cover_panel": "#efe8db", "cover_alpha": 230, "cover_ink": "#2b2b29", "cover_title_size": 49,
        "keywords": "房间 · 服务空间 · 结构 · 纪念性 · 自然光", "cover_line": "建筑的纪念性不来自尺度，", "cover_subline": "而来自秩序被光清楚说出的瞬间。",
        "preview": "#b7aea0", "summary_overlay": "#e8dfd1", "summary_alpha": 198, "summary_ink": "#2c2c29", "summary_box": "#f7f1e7", "summary_box_ink": "#2c2c29",
        "summary": "这本全集呈现康如何让结构、服务空间与自然光共同生成“房间”：建筑的纪念性不来自尺度，而来自秩序被光清楚说出的瞬间。",
        "summary_tag": "A ROOM BEGINS WITH LIGHT", "summary_detail": "从研究所、博物馆、图书馆到国家议会，康反复追问制度需要什么空间，并让材料、结构和光回答。",
        "cases": [
            {"file": "kahn-salk.jpg", "title": "萨尔克生物研究所", "meta": "拉霍亚，美国｜1965", "keyword": "PLAZA / OCEAN / SILENCE", "focal": (0.50, 0.48),
             "headline": "两列实验室让出一片通向太平洋的石质广场，中央水线把远方拉进建筑；最强的空间不是房间，而是被精确留空的寂静。",
             "caption": "服务设施被收纳进独立层带，让实验空间保持开放；秩序最终指向天空和海。", "credit": "PHOTO SOURCE: Wikimedia Commons / Salk Institute"},
            {"file": "kahn-kimbell.jpg", "title": "金贝尔艺术博物馆", "meta": "沃思堡，美国｜1972", "keyword": "VAULT / DAYLIGHT / ROOM", "focal": (0.50, 0.52),
             "headline": "连续拱顶把博物馆分解为一间间可辨识的“房间”，顶部反光器让阳光沿混凝土曲面柔和展开；结构同时成为光的仪器。",
             "caption": "材料的重量与自然光的轻盈并置，使展厅既古老又现代。", "credit": "PHOTO SOURCE: Wikimedia Commons / Kimbell Art Museum"},
            {"file": "kahn-exeter.jpg", "title": "埃克塞特学院图书馆", "meta": "埃克塞特，美国｜1972", "keyword": "BRICK / CENTRAL VOID / READING", "focal": (0.50, 0.50),
             "headline": "厚重砖墙保护藏书，中央空洞暴露巨大的混凝土开口，阅读席则贴近窗边；书、人与光被安排在三层清楚的空间秩序里。",
             "caption": "外部像沉默的机构，内部却以中庭把知识的共同体完整显现。", "credit": "PHOTO SOURCE: Wikimedia Commons / Exeter Library exterior"},
            {"file": "kahn-dhaka.jpg", "title": "孟加拉国国民议会大厦", "meta": "达卡，孟加拉国｜1983", "keyword": "GEOMETRY / MONUMENT / LIGHT", "focal": (0.50, 0.55),
             "headline": "圆、三角与矩形穿透巨大的混凝土体，光在深墙中形成可居住的厚度；国家机构被表达为一种既原始又普遍的几何秩序。",
             "caption": "纪念性不是装饰，而是材料、结构、光与集体制度在同一形式中达成一致。", "credit": "PHOTO SOURCE: Wikimedia Commons / National Parliament Building, Dhaka"},
        ],
    },
    {
        "slug": "corbusier", "cover": "corbusier.png", "base": "corbusier-base.png",
        "designer": "勒·柯布西耶", "book": "全住宅 / Le Corbusier HOUSES", "cover_book": "全住宅\nLe Corbusier HOUSES", "label": "HOUSE AS PROTOTYPE",
        "accent": "#22a9cf", "accent_ink": "#ffffff", "panel": "#e9f5f8", "text": "#17303a", "muted": "#587987",
        "footer": "#14333e", "footer_ink": "#ffffff", "mount": "#ffffff", "cover_panel": "#eefafd", "cover_alpha": 225, "cover_ink": "#17303a", "cover_title_size": 50,
        "keywords": "自由平面 · 建筑漫游 · 五点 · 模度 · 最小居住", "cover_line": "住宅是一生持续迭代的实验，", "cover_subline": "每一栋房子都在重新定义现代生活。",
        "preview": "#79c9df", "summary_overlay": "#dff3f8", "summary_alpha": 190, "summary_ink": "#17303a", "summary_box": "#f4fcfd", "summary_box_ink": "#17303a",
        "summary": "《勒·柯布西耶全住宅》把住宅当作一生持续迭代的实验：从自由平面、建筑漫游到模度与最小居住，“家”被不断改写为现代生活的原型。",
        "summary_tag": "THE HOUSE IS A TESTING GROUND", "summary_detail": "106个住宅项目不是单一风格的重复，而是一套关于结构、动线、尺度与生活方式的连续实验。",
        "cases": [
            {"file": "corbusier-la-roche.jpg", "title": "拉罗什住宅", "meta": "巴黎，法国｜1925", "keyword": "PROMENADE / SEQUENCE", "focal": (0.54, 0.55),
             "headline": "坡道、楼梯与转折把观看组织成连续事件；住宅不再由静止房间定义，而是在移动中逐段显现，这就是“建筑漫游”的早期范本。",
             "caption": "空间的意义来自路径：身体每前进一步，比例、光线和视角都被重新编排。", "credit": "PHOTO SOURCE: Wikimedia Commons / Maison La Roche"},
            {"file": "corbusier-villa-stein-model.jpg", "title": "斯坦因别墅", "meta": "加尔什，法国｜1927", "keyword": "FREE PLAN / FREE FAÇADE", "focal": (0.50, 0.50),
             "headline": "柱网把结构从墙体中释放，内部可以自由分隔，立面也成为独立构图；现代住宅由承重规则转向平面与生活关系的主动设计。",
             "caption": "模型清楚呈现自由平面如何让体量、开口和动线获得新的独立性。", "credit": "PHOTO SOURCE: Wikimedia Commons / Villa Stein-de-Monzie model, V&A"},
            {"file": "corbusier-savoye.jpg", "title": "萨伏伊别墅", "meta": "普瓦西，法国｜1931", "keyword": "PROMENADE / COLOR / FRAME", "focal": (0.50, 0.50),
             "headline": "蓝色墙面、倾斜边界与被框取的门洞把一次转身变成空间事件；萨伏伊别墅不只是一组“五点”，更是一条由身体、色彩与光连续完成的漫游。",
             "caption": "外部的白色原型进入内部后，被路径与色彩转化为具体、动态的居住经验。", "credit": "PHOTO: Biscarotte / Wikimedia Commons / CC BY-SA 2.0"},
            {"file": "corbusier-cabanon.jpg", "title": "卡普马丹小木屋", "meta": "罗克布吕讷，法国｜1952", "keyword": "MODULOR / MINIMUM DWELLING", "focal": (0.50, 0.50),
             "headline": "不足十四平方米的木屋以模度控制每一处尺寸，床、桌、储物和开窗被压缩成一个完整生活单元；最小并不等于贫乏。",
             "caption": "晚年的柯布西耶把宏大的住宅理论收束到身体尺度：足够，就是精确。", "credit": "PHOTO SOURCE: Wikimedia Commons / Cabanon Le Corbusier"},
        ],
    },
    {
        "slug": "big", "cover": "big.png", "base": "big-base.png",
        "designer": "BIG / 比亚克·英格斯", "book": "Yes Is More / 漫画建筑进化论", "label": "PRAGMATIC UTOPIA",
        "accent": "#00a9de", "accent_ink": "#ffffff", "panel": "#111111", "text": "#ffffff", "muted": "#b8b8b8", "dark": True,
        "footer": "#ffffff", "footer_ink": "#111111", "mount": "#ffffff", "cover_panel": "#060606", "cover_alpha": 226, "cover_ink": "#ffffff", "cover_title_size": 49,
        "keywords": "漫画叙事 · 程序混合 · 实用乌托邦 · 公共价值", "cover_line": "限制不是句号，", "cover_subline": "它是把更多可能性叠加起来的开场。", "footer_light": False,
        "preview": "#333333", "summary_overlay": "#050505", "summary_alpha": 210, "summary_ink": "#ffffff", "summary_box": "#f5f5f0", "summary_box_ink": "#111111", "summary_light": True,
        "summary": "《Yes Is More》用漫画说明BIG的方法：不把限制当作否定，而把程序、政策、气候与欲望叠加成一个更有公共价值的“是”。",
        "summary_tag": "CONSTRAINTS CAN PRODUCE MORE", "summary_detail": "BIG把复杂条件画成清楚的故事：每次变形都回应一个现实问题，最终让建筑获得意料之外的公共性。",
        "contrast": 1.15, "saturation": 0.08,
        "cases": [
            {"file": "big-vm-houses.jpg", "title": "VM Houses", "meta": "哥本哈根，丹麦｜2005", "keyword": "VIEW / GEOMETRY / DENSITY", "focal": (0.50, 0.50),
             "headline": "V形与M形平面把密集住宅折向阳光和景观，尖角阳台让每户获得独立视野；看似醒目的造型，其实来自采光与视线的连续推导。",
             "caption": "BIG式图解的核心：把一个现实问题转译成一次明确变形。", "credit": "PHOTO SOURCE: Wikimedia Commons / VM Houses"},
            {"file": "big-mountain-dwellings.jpg", "title": "Mountain Dwellings", "meta": "哥本哈根，丹麦｜2008", "keyword": "PARKING + TERRACED HOUSING", "focal": (0.50, 0.48),
             "headline": "停车楼被塑造成坡地，住宅沿其表面层层退台，每户都获得花园与阳光；两个彼此冲突的程序被相加，反而生成新的居住类型。",
             "caption": "“是，而且……”：基础设施不被隐藏，而成为住宅景观与结构的起点。", "credit": "PHOTO SOURCE: Wikimedia Commons / Mountain Dwellings"},
            {"file": "big-8-house.jpg", "title": "8 House", "meta": "哥本哈根，丹麦｜2010", "keyword": "LOOP / SOCIAL PATH", "focal": (0.50, 0.50),
             "headline": "连续坡道把住宅、商业与公共空间缝成一条立体街道，骑行和步行可以绕完整栋建筑；“8”不是符号，而是一条社会路径。",
             "caption": "城市生活被带到屋顶与高层，住宅综合体因此像一座可被骑行的小城。", "credit": "PHOTO SOURCE: Wikimedia Commons / 8 House"},
            {"file": "big-copenhill.jpg", "title": "CopenHill", "meta": "哥本哈根，丹麦｜2019", "keyword": "POWER PLANT + SKI SLOPE", "focal": (0.50, 0.50),
             "headline": "垃圾焚烧发电厂的屋顶被改造成滑雪坡、步道与攀岩墙；工业设施不只减少负面影响，还主动成为城市新的公共地形。",
             "caption": "可持续性从技术指标变成日常体验：基础设施也能制造快乐与公共生活。", "credit": "PHOTO SOURCE: Wikimedia Commons / CopenHill"},
        ],
    },
    {
        "slug": "ando", "cover": "ando.png", "base": "ando-base.png",
        "designer": "安藤忠雄", "book": "连战连败", "label": "FAILURE AS METHOD",
        "accent": "#ee4c1f", "accent_ink": "#ffffff", "panel": "#f3e8dc", "text": "#29231f", "muted": "#75685f",
        "footer": "#162743", "footer_ink": "#ffffff", "mount": "#fff9ef", "cover_panel": "#f5eadf", "cover_alpha": 225, "cover_ink": "#27221e",
        "keywords": "竞赛 · 逆境 · 重做 · 意志 · 昨日を超えて", "cover_line": "失败不是设计的反面，", "cover_subline": "它迫使方案在重做中获得更清楚的意志。",
        "preview": "#c47e60", "summary_overlay": "#eddfd2", "summary_alpha": 190, "summary_ink": "#29231f", "summary_box": "#faf3e9", "summary_box_ink": "#29231f",
        "summary": "《连战连败》把失败写成设计方法：竞赛落选、条件冲突与现实限制并不会终止建筑，反而迫使方案在一次次重做中获得更清楚的意志。",
        "summary_tag": "DESIGN CONTINUES AFTER DEFEAT", "summary_detail": "真正的“战斗”不是赢下每一次竞赛，而是在挫败之后继续追问：这座建筑还能否比昨天更接近它必须成为的样子。",
        "cases": [
            {"file": "ando-rokko.jpg", "title": "六甲集合住宅", "meta": "神户，日本｜1983–99", "keyword": "STEEP SITE / MODULAR ORDER", "focal": (0.50, 0.48),
             "headline": "规则网格嵌入陡峭山体，住宅单元在重复中回应高度、视野与地形；困难场地没有被抹平，而成为结构秩序最强的理由。",
             "caption": "三期持续推进证明设计不是一次完成，而是在时间与现实中反复校正。", "credit": "PHOTO SOURCE: Wikimedia Commons / Rokko Housing"},
            {"file": "ando-awaji.jpg", "title": "淡路梦舞台", "meta": "淡路岛，日本｜2000", "keyword": "LANDSCAPE / SEQUENCE / RECOVERY", "focal": (0.50, 0.48),
             "headline": "花园、平台、阶梯与水庭组成巨大的行走序列，把被采石破坏的山地转化为新的公共景观；工程伤痕通过建筑重新获得生命。",
             "caption": "面对超大尺度，安藤依靠路径与重复，让复杂工程仍能被身体逐步理解。", "credit": "PHOTO SOURCE: Wikimedia Commons / Awaji Yumebutai"},
            {"file": "ando-hyogo.jpg", "title": "兵库县立美术馆", "meta": "神户，日本｜2002", "keyword": "PROMENADE / WATER / CITY", "focal": (0.50, 0.52),
             "headline": "长阶、平台与临水通道把美术馆变成城市散步的一部分；清水混凝土不再只是墙，而是组织灾后城市重新面向海岸的公共界面。",
             "caption": "建筑价值超出展厅：人们如何抵达、停留和眺望，同样属于美术馆。", "credit": "PHOTO SOURCE: Wikimedia Commons / Hyogo Prefectural Museum of Art"},
            {"file": "ando-fort-worth.jpg", "title": "沃思堡现代艺术博物馆", "meta": "沃思堡，美国｜2002", "keyword": "CONCRETE / GLASS / REFLECTION", "focal": (0.50, 0.50),
             "headline": "混凝土平面悬浮在玻璃与水面之间，厚重结构通过倒影获得轻盈；与相邻金贝尔博物馆的对话，被转化为材料与光的克制回应。",
             "caption": "成熟并非重复固定风格，而是在不同语境中继续检验同一份空间意志。", "credit": "PHOTO SOURCE: Wikimedia Commons / Modern Art Museum of Fort Worth"},
        ],
    },
]


def make_all_preview(all_paths):
    tw, th, gx, gy = 207, 277, 0, 16
    canvas = Image.new("RGB", (6 * tw, 6 * th + 5 * gy), "#202020")
    for row, paths in enumerate(all_paths):
        for col, path in enumerate(paths):
            img = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
            canvas.paste(img, (col * tw, row * (th + gy)))
    canvas.save(OUT / "preview-all.jpg", quality=94, subsampling=0)


def main():
    all_paths = []
    for cfg in GROUPS:
        paths = [make_cover(cfg)]
        for page, case in enumerate(cfg["cases"], start=2):
            paths.append(make_case(cfg, page, case))
        paths.append(make_summary(cfg))
        make_group_preview(cfg, paths)
        all_paths.append(paths)
    make_all_preview(all_paths)
    print(f"Generated {sum(len(p) for p in all_paths)} cards in {OUT}")


if __name__ == "__main__":
    main()
