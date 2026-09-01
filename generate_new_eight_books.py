from pathlib import Path
import json
import math

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "new-eight-books"
SOURCE_ASSETS = ROOT / "assets" / "sourced-eight-books"
OUT_ROOT = ROOT / "output" / "新书八本-流量方案"
W, H = 1242, 1660
FONT_SANS = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"


def font(size, serif=False):
    return ImageFont.truetype(FONT_SERIF if serif else FONT_SANS, size)


def rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgba(value, alpha=255):
    return rgb(value) + (alpha,)


def wrap(draw, text, used_font, width):
    lines, current = [], ""
    for paragraph in text.split("\n"):
        for ch in paragraph:
            test = current + ch
            if current and draw.textbbox((0, 0), test, font=used_font)[2] > width:
                lines.append(current)
                current = ch
            else:
                current = test
        if current:
            lines.append(current)
            current = ""
    return "\n".join(lines)


def fit_inside(image, box):
    scale = min(box[0] / image.width, box[1] / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


def crop_fill(image, size, focal=(0.5, 0.5)):
    tw, th = size
    scale = max(tw / image.width, th / image.height)
    nw, nh = round(image.width * scale), round(image.height * scale)
    image = image.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - tw, round((nw - tw) * focal[0])))
    top = max(0, min(nh - th, round((nh - th) * focal[1])))
    return image.crop((left, top, left + tw, top + th))


def sourced_image(cfg, slot):
    folder = SOURCE_ASSETS / cfg["asset_set"]
    matches = [p for p in folder.glob(f"{slot}.*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one sourced image for {cfg['asset_set']}/{slot}, got {matches}")
    return matches[0]


def composite_panel(canvas, box, fill, radius=16):
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle(box, radius, fill=fill)
    canvas.alpha_composite(overlay)


def page_mark(draw, number, light=True):
    color = rgba("#fffaf0", 185) if light else rgba("#111111", 155)
    draw.text((1160, 1592), f"0{number} / 06", font=font(23), fill=color, anchor="ra")


def save(canvas, folder, number):
    path = folder / f"{number:02d}.jpg"
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def draw_name_badge(draw, text, cfg, prefix):
    """Draw an explicit, reader-facing name label for every case or diagram."""
    label = f"{prefix}｜{text}"
    x1, y1, x2, y2 = 62, 48, 1170, 126
    draw.rounded_rectangle((x1, y1, x2, y2), 6, fill=rgba("#101010", 228))
    size = 27
    while size > 19 and draw.textbbox((0, 0), label, font=font(size))[2] > x2 - x1 - 46:
        size -= 1
    draw.text((86, 67), label, font=font(size), fill=cfg["paper"])


def draw_cover_pattern(draw, cfg):
    accent, accent2, ink, paper = cfg["accent"], cfg["accent2"], cfg["ink"], cfg["paper"]
    kind = {
        "肌肤之目": "senses",
        "体验建筑": "movement",
        "场所精神": "place",
        "美国大城市的死与生": "street",
        "城市建筑学": "memory",
        "城市意象": "map",
        "建筑模式语言": "patterns",
        "建筑：形式、空间和秩序": "grammar",
    }[cfg["book"]]
    draw.rectangle((0, 0, W, H), fill=cfg["cover_bg"])

    if kind == "senses":
        # Eye + fingerprint: vision is only one layer of embodied perception.
        draw.polygon([(0, 0), (635, 0), (470, 980), (0, 1180)], fill=accent)
        draw.arc((640, 70, 1320, 650), 190, 350, fill=accent2, width=18)
        draw.arc((640, -80, 1320, 790), 15, 165, fill=accent2, width=18)
        draw.ellipse((910, 245, 1070, 405), fill=accent2)
        draw.ellipse((953, 288, 1027, 362), fill=ink)
        for r in range(90, 520, 45):
            draw.arc((60-r, 1080-r, 60+r, 1080+r), 270, 80, fill=rgba(paper, 115), width=4)
        for y in range(760, 1310, 85):
            draw.line((40, y, 600, y-150), fill=rgba(accent2, 80), width=3)

    elif kind == "movement":
        # A perspectival room, a moving light spot and a changing spatial rhythm.
        vx, vy = 720, 420
        draw.polygon([(0, 0), (760, 0), (vx, vy), (0, 1050)], fill=accent)
        draw.ellipse((800, 80, 1120, 400), fill=accent2)
        for x in [-120, 80, 300, 520, 940, 1160, 1380]:
            draw.line((vx, vy, x, 1410), fill=rgba(paper, 130), width=5)
        for y in [620, 790, 980, 1190]:
            scale = (y-vy)/(1410-vy)
            left = vx + (-120-vx)*scale
            right = vx + (1380-vx)*scale
            draw.line((left, y, right, y), fill=rgba(paper, 90), width=4)
        for i, h in enumerate([130, 260, 170, 340, 220]):
            x = 70 + i*105
            draw.rectangle((x, 1240-h, x+45, 1240), fill=accent2 if i % 2 else paper)

    elif kind == "place":
        # Contours, horizon, centre and direction build a recognisable place.
        draw.rectangle((0, 0, W, 455), fill=accent)
        draw.polygon([(0, 800), (230, 620), (460, 710), (720, 470), (1000, 650), (1242, 510), (1242, 1410), (0, 1410)], fill=rgba(accent, 205))
        for i in range(7):
            pad = 80 + i*58
            draw.ellipse((pad, 420+i*18, 1242-pad//2, 1320-i*25), outline=rgba(paper, 95), width=4)
        draw.ellipse((790, 220, 890, 320), fill=accent2)
        draw.line((840, 320, 840, 660), fill=accent2, width=9)
        draw.polygon([(840, 320), (790, 410), (890, 410)], fill=accent2)
        draw.line((70, 1080, 600, 830), fill=rgba(accent2, 150), width=14)

    elif kind == "street":
        # A dense street grid, active windows and multiple routes.
        draw.rectangle((0, 0, W, H), fill=ink)
        for x in [60, 250, 455, 675, 910, 1130]:
            draw.line((x, 0, x-120, 1410), fill=accent, width=34)
        for y in [330, 610, 900, 1190]:
            draw.line((0, y, W, y+70), fill=accent, width=34)
        for row in range(5):
            for col in range(7):
                x, y = 75 + col*150, 160 + row*205
                if (row+col) % 3 == 0:
                    draw.rectangle((x, y, x+62, y+84), fill=accent2)
        for x in [130, 360, 590]:
            draw.ellipse((x, 1160, x+34, 1194), fill=paper)
            draw.line((x+17, 1194, x+17, 1280), fill=paper, width=8)

    elif kind == "memory":
        # Repeated urban types sit on a visible time axis.
        draw.rectangle((0, 0, W, H), fill=ink)
        draw.line((70, 1160, 1170, 1160), fill=accent2, width=10)
        forms = [(70, 710, 270, 1160), (300, 530, 515, 1160), (550, 760, 770, 1160), (810, 400, 1050, 1160)]
        for i, (x1, y1, x2, y2) in enumerate(forms):
            color = accent if i % 2 == 0 else rgba(accent2, 215)
            draw.rectangle((x1, y1, x2, y2), outline=color, width=16)
            draw.polygon([(x1-15, y1), ((x1+x2)//2, y1-125), (x2+15, y1)], fill=color)
            for yy in range(y1+85, y2-30, 105):
                draw.line((x1+35, yy, x2-35, yy), fill=color, width=5)
        for x in [90, 340, 590, 840, 1090]:
            draw.ellipse((x, 1128, x+64, 1192), fill=accent2)
        draw.arc((760, 40, 1320, 590), 30, 320, fill=accent, width=26)

    elif kind == "map":
        # Paths, edges, districts, nodes and a landmark form a mental map.
        draw.rectangle((0, 0, W, H), fill=ink)
        pts = [(40, 1180), (280, 830), (470, 980), (690, 650), (930, 740), (1190, 300)]
        for p1, p2 in zip(pts, pts[1:]):
            draw.line((*p1, *p2), fill=accent, width=36)
        draw.line((560, 560, 560, 1410), fill=accent2, width=16)
        draw.rectangle((745, 180, 1120, 520), fill=rgba(accent, 180))
        for x, y in [(280, 830), (690, 650), (930, 740)]:
            draw.ellipse((x-48, y-48, x+48, y+48), fill=accent2)
        draw.polygon([(1040, 590), (1120, 770), (960, 770)], fill=paper)
        for r in [80, 140, 205]:
            draw.ellipse((690-r, 650-r, 690+r, 650+r), outline=rgba(paper, 80), width=4)

    elif kind == "patterns":
        # Modular relations combine like words in a language.
        draw.rectangle((0, 0, W, H), fill=ink)
        for row in range(5):
            for col in range(5):
                x, y = 55 + col*205, 570 + row*165
                selected = (row, col) in {(0,1),(1,1),(1,2),(2,2),(3,2),(3,3),(4,3)}
                fill = accent if selected else rgba(paper, 20)
                outline = accent2 if selected else rgba(paper, 90)
                draw.rounded_rectangle((x, y, x+130, y+110), 12, fill=fill, outline=outline, width=6)
        draw.line((315, 735, 520, 900), fill=accent2, width=12)
        draw.line((520, 900, 725, 1065), fill=accent2, width=12)
        draw.line((725, 1065, 930, 1230), fill=accent2, width=12)
        draw.polygon([(930, 1230), (850, 1190), (900, 1140)], fill=accent2)

    else:  # grammar
        # Point, line, plane, volume and path—the book's basic spatial grammar.
        draw.rectangle((0, 0, W, H), fill=ink)
        draw.ellipse((110, 590, 190, 670), fill=accent2)
        draw.line((150, 630, 920, 900), fill=accent, width=24)
        draw.rectangle((210, 700, 650, 1140), outline=paper, width=14)
        draw.polygon([(650, 700), (940, 560), (940, 1000), (650, 1140)], fill=rgba(accent, 150), outline=accent2)
        draw.rectangle((780, 860, 1120, 1200), outline=accent2, width=16)
        draw.arc((35, 980, 690, 1620), 210, 345, fill=paper, width=12)
        for i in range(5):
            draw.line((70+i*105, 560, 350+i*105, 1410), fill=rgba(paper, 45), width=3)

    draw.rectangle((0, 1410, W, H), fill=ink)


def cover_card(cfg, folder):
    hero = Image.open(sourced_image(cfg, "hero")).convert("RGB")
    hero = crop_fill(hero, (W, H), cfg.get("hero_focal", (0.5, 0.5)))
    hero = ImageEnhance.Contrast(hero).enhance(1.10)
    hero = ImageEnhance.Color(hero).enhance(0.82)
    hero = ImageEnhance.Sharpness(hero).enhance(1.15)
    canvas = hero.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 35)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 26, H), fill=cfg["accent2"])
    draw.rectangle((62, 58, 520, 112), fill=cfg["accent2"])
    draw.text((84, 69), "BOOK × ARCHITECTURE / 01", font=font(24), fill=cfg["ink"])

    # A photographic editorial composition inspired by the user's references.
    title_box = (55, 150, 775, 720)
    composite_panel(canvas, title_box, (8, 8, 8, 228), 18)
    draw = ImageDraw.Draw(canvas)
    draw.text((82, 198), f"{cfg['author']} ×《{cfg['book']}》", font=font(31), fill=cfg["paper"])
    hook_font = font(cfg.get("hook_size", 72), serif=True)
    hook = wrap(draw, cfg["hook"], hook_font, 620)
    draw.multiline_text((78, 300), hook, font=hook_font, fill=cfg["paper"], spacing=12)
    hook_bottom = draw.multiline_textbbox((78, 300), hook, font=hook_font, spacing=12)[3]
    draw.rectangle((78, hook_bottom + 30, 715, hook_bottom + 42), fill=cfg["accent2"])
    draw.text((80, hook_bottom + 70), cfg["cover_en"], font=font(29), fill=cfg["accent2"])
    subtitle = wrap(draw, cfg["cover_line"], font(28), 625)
    draw.multiline_text((80, hook_bottom + 117), subtitle, font=font(28), fill=rgba(cfg["paper"], 220), spacing=10)

    cover = Image.open(ASSETS / "covers" / cfg["cover"]).convert("RGB")
    cover = fit_inside(cover, (350, 515))
    swap = int(cfg["slug"][:2]) % 2 == 0
    x = 790 if swap else 82
    y = 870
    shadow = Image.new("RGBA", (cover.width + 70, cover.height + 70), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((25, 25, cover.width + 45, cover.height + 45), 7, fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(shadow, (x - 25, y - 18))
    mount = Image.new("RGBA", (cover.width + 20, cover.height + 20), rgba("#f7f2e7"))
    mount.alpha_composite(cover.convert("RGBA"), (10, 10))
    canvas.alpha_composite(mount, (x - 10, y - 10))

    card_x1, card_x2 = (68, 700) if swap else (470, 1170)
    card_box = (card_x1, 1010, card_x2, 1450)
    composite_panel(canvas, card_box, (244, 239, 225, 242), 18)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((card_x1 + 36, 1050, card_x1 + 56, 1145), fill=cfg["accent2"])
    draw.text((card_x1 + 86, 1050), cfg["cover_en"], font=font(27), fill=cfg["accent"])
    thesis = wrap(draw, cfg["cover_thesis"], font(45, serif=True), card_x2 - card_x1 - 100)
    draw.multiline_text((card_x1 + 86, 1130), thesis, font=font(45, serif=True), fill=cfg["ink"], spacing=16)
    draw.text((70, 1510), f"封面案例｜{cfg['hero_name']}", font=font(24), fill=rgba("#fffaf0", 220))
    page_mark(draw, 1)
    return save(canvas, folder, 1)


def photo_card(cfg, folder, number, slide):
    image = Image.open(sourced_image(cfg, slide["file"])).convert("RGB")
    image = ImageEnhance.Contrast(image).enhance(1.06)
    image = ImageEnhance.Color(image).enhance(0.98)
    image = ImageEnhance.Sharpness(image).enhance(1.18)
    image = crop_fill(image, (W, 1040), slide.get("focal", (0.5, 0.5)))
    canvas = Image.new("RGBA", (W, H), rgba("#0f0f10"))
    canvas.alpha_composite(image.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 150), (0, 0, 0, 105)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=cfg["accent2"])
    draw_name_badge(draw, slide["name"], cfg, slide.get("label", "建筑案例"))
    draw.rectangle((0, 1040, W, H), fill="#101010")
    draw.rectangle((68, 1092, 240, 1105), fill=cfg["accent2"])
    headline_font = font(57, serif=True)
    headline = wrap(draw, slide["headline"], headline_font, 1080)
    draw.multiline_text((68, 1140), headline, font=headline_font, fill="#fffaf0", spacing=12)
    bottom = draw.multiline_textbbox((68, 1140), headline, font=headline_font, spacing=12)[3]
    body = wrap(draw, slide["body"], font(29), 1070)
    draw.multiline_text((70, bottom + 38), body, font=font(29), fill=rgba("#fffaf0", 205), spacing=12)
    page_mark(draw, number)
    return save(canvas, folder, number)


def diagram_base(cfg):
    canvas = Image.new("RGBA", (W, H), rgba(cfg["paper"]))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=cfg["accent"])
    for x in range(60, W, 82):
        draw.line((x, 0, x, 1030), fill=rgba(cfg["ink"], 16), width=1)
    for y in range(55, 1030, 82):
        draw.line((0, y, W, y), fill=rgba(cfg["ink"], 16), width=1)
    return canvas, draw


def diagram_art(draw, kind, cfg):
    a, b, ink, paper = cfg["accent"], cfg["accent2"], cfg["ink"], cfg["paper"]
    if kind == "eye_layers":
        draw.ellipse((185, 210, 1055, 760), outline=ink, width=14)
        draw.ellipse((455, 285, 785, 690), fill=a)
        draw.ellipse((555, 390, 685, 585), fill=b)
        for r in range(70, 370, 55):
            draw.arc((620-r, 485-r, 620+r, 485+r), 205, 335, fill=rgba(ink, 140), width=4)
        draw.text((620, 850), "视觉之外，还有触觉、声音、温度与记忆", font=font(31), fill=ink, anchor="mm")
    elif kind == "door_handle":
        draw.rectangle((210, 130, 800, 900), outline=ink, width=16)
        draw.line((800, 130, 1035, 40), fill=ink, width=10)
        draw.line((800, 900, 1035, 990), fill=ink, width=10)
        draw.rounded_rectangle((610, 470, 920, 555), 38, fill=a)
        draw.ellipse((870, 430, 965, 595), outline=b, width=12)
        draw.text((615, 735), "门把手，是建筑与身体的第一次握手", font=font(32), fill=ink, anchor="mm")
    elif kind == "rhythm":
        widths = [56, 56, 105, 56, 160, 56, 105, 56]
        x = 120
        for i, width in enumerate(widths):
            height = 510 if i % 2 == 0 else 650
            draw.rectangle((x, 880-height, x+width, 880), fill=a if i % 3 else b)
            x += width + 42
        draw.line((100, 905, 1140, 905), fill=ink, width=8)
        draw.text((620, 970), "节奏来自移动中的时间，而不只是重复", font=font(31), fill=ink, anchor="mm")
    elif kind == "body_scale":
        for x, h, color in [(185, 220, b), (430, 410, a), (755, 680, ink)]:
            draw.ellipse((x, 830-h, x+70, 900-h), fill=color)
            draw.rectangle((x+15, 900-h, x+55, 900), fill=color)
            draw.line((x+35, 900-h+100, x-20, 900-h+220), fill=color, width=18)
            draw.line((x+35, 900-h+100, x+90, 900-h+220), fill=color, width=18)
        draw.line((110, 935, 1130, 935), fill=ink, width=7)
        draw.text((620, 990), "尺度不是数字，是身体与空间之间的比较", font=font(31), fill=ink, anchor="mm")
    elif kind == "compass":
        cx, cy = 620, 500
        for angle in [0, 35, 82, 135, 205, 260, 315]:
            r = 380
            x = cx + math.cos(math.radians(angle)) * r
            y = cy + math.sin(math.radians(angle)) * r
            draw.line((cx, cy, x, y), fill=rgba(ink, 110), width=8)
        draw.ellipse((535, 415, 705, 585), fill=a)
        draw.polygon([(620, 210), (675, 380), (620, 350), (565, 380)], fill=b)
        draw.text((620, 920), "方向、中心与边界，让地方拥有可辨认的性格", font=font(31), fill=ink, anchor="mm")
    elif kind == "figure_ground":
        blocks = [(90,120,300,300),(350,100,620,260),(690,110,1135,335),(100,370,520,620),(590,390,810,700),(860,390,1140,590),(120,700,380,920),(440,740,730,940),(810,660,1130,930)]
        for i, rect in enumerate(blocks):
            draw.rounded_rectangle(rect, 12, fill=ink if i % 3 else a)
        draw.line((60, 650, 1180, 530), fill=b, width=24)
        draw.text((620, 985), "空地不是剩余，它与建筑共同定义场所", font=font(31), fill=ink, anchor="mm")
    elif kind == "street_eyes":
        draw.rectangle((80, 160, 1160, 780), fill=rgba(ink, 40), outline=ink, width=10)
        for floor in range(3):
            for col in range(8):
                x, y = 120+col*125, 210+floor*155
                draw.rectangle((x,y,x+75,y+90), fill=a if (col+floor)%3==0 else paper, outline=ink, width=4)
        draw.rectangle((80, 780, 1160, 930), fill=b)
        for x in [220,420,660,910]:
            draw.ellipse((x, 730, x+40, 770), fill=ink)
            draw.line((x+20,770,x+20,865), fill=ink, width=10)
        draw.text((620, 980), "有人看见街道，街道才会产生日常安全", font=font(31), fill=ink, anchor="mm")
    elif kind == "short_blocks":
        draw.text((280, 130), "超级街区", font=font(34), fill=ink, anchor="mm")
        draw.rectangle((80, 210, 530, 830), fill=ink)
        draw.line((305,210,305,830), fill=paper, width=10)
        draw.text((930, 130), "短街区", font=font(34), fill=ink, anchor="mm")
        for x in range(680, 1160, 155): draw.line((x,210,x,830), fill=ink, width=16)
        for y in range(210, 850, 155): draw.line((680,y,1160,y), fill=ink, width=16)
        for x,y in [(720,250),(1030,560),(875,405),(720,720)]: draw.ellipse((x,y,x+45,y+45), fill=a)
        draw.text((620, 935), "街区越短，路线选择越多，偶遇也越多", font=font(31), fill=ink, anchor="mm")
    elif kind == "mixed_use":
        draw.rectangle((180, 130, 1060, 880), outline=ink, width=12)
        colors = [a, b, ink, "#6aa6a6"]
        labels = ["住宅", "商店", "办公", "公共空间"]
        for i in range(4):
            y1 = 150 + i*175
            draw.rectangle((200, y1, 1040, y1+140), fill=colors[i])
            draw.text((620, y1+70), labels[i], font=font(35), fill=paper if i != 1 else ink, anchor="mm")
        draw.text((620, 960), "不同人群在不同时间使用街区，活力才不会断档", font=font(31), fill=ink, anchor="mm")
    elif kind == "typology":
        for i, scale in enumerate([1.0, .82, .65, .48]):
            x = 120+i*260
            w, h = int(210*scale), int(360*scale)
            y = 760-h
            draw.rectangle((x,y,x+w,y+h), outline=ink, width=10)
            draw.polygon([(x-20,y),(x+w//2,y-120),(x+w+20,y)], fill=a if i%2==0 else b)
            for yy in range(y+55,y+h-20,80): draw.line((x+25,yy,x+w-25,yy),fill=rgba(ink,120),width=5)
        draw.line((80, 800, 1160, 800), fill=ink, width=8)
        draw.text((620, 930), "类型会重复，但会在时间和城市中不断变形", font=font(31), fill=ink, anchor="mm")
    elif kind == "city_elements":
        draw.rectangle((75, 100, 1165, 930), outline=ink, width=7)
        draw.line((110,760,1120,210), fill=a, width=26)
        draw.line((360,120,360,900), fill=ink, width=14)
        draw.rectangle((720,180,1080,510), fill=rgba(b,160))
        draw.ellipse((560,520,700,660), fill=b)
        draw.polygon([(900,700),(960,560),(1020,700)], fill=ink)
        for text_, pos in [("路径",(210,690)),("边界",(375,150)),("区域",(900,340)),("节点",(630,590)),("地标",(960,740))]:
            draw.text(pos, text_, font=font(29), fill=paper if text_ in ["区域","节点"] else ink, anchor="mm")
    elif kind == "path_edge":
        for y in [220,420,640,840]: draw.line((80,y,1160,y-80), fill=rgba(ink,100), width=13)
        draw.line((250,80,720,980), fill=a, width=34)
        draw.line((870,80,870,980), fill=b, width=46)
        draw.text((620, 960), "路径负责串联经验，边界决定哪些地方彼此分开", font=font(31), fill=ink, anchor="mm")
    elif kind == "nodes_landmarks":
        pts=[(190,250),(420,610),(700,310),(920,690),(1080,290)]
        for a1,b1 in zip(pts,pts[1:]): draw.line((*a1,*b1),fill=rgba(ink,110),width=10)
        for i,(x,y) in enumerate(pts): draw.ellipse((x-55,y-55,x+55,y+55),fill=a if i%2==0 else b)
        draw.polygon([(700,90),(770,260),(630,260)],fill=ink)
        draw.text((620, 925), "节点让人停下，地标让人重新确认方向", font=font(31), fill=ink, anchor="mm")
    elif kind.startswith("pattern_"):
        draw.rectangle((110, 120, 1130, 900), outline=ink, width=10)
        if kind == "pattern_entry":
            draw.rectangle((160,220,470,830),fill=ink); draw.rectangle((270,420,430,830),fill=paper)
            draw.line((470,520,1020,520),fill=a,width=50); draw.polygon([(1020,520),(900,450),(900,590)],fill=a)
            label="入口需要一段过渡，让身体完成从外到内的转换"
        elif kind == "pattern_light":
            draw.rectangle((300,230,940,850),fill=ink)
            draw.rectangle((300,360,370,670),fill=b); draw.rectangle((870,360,940,670),fill=a)
            for x0,color in [(370,b),(870,a)]: draw.polygon([(x0,360),(620,500),(x0,670)],fill=rgba(color,115))
            label="两侧有光的房间，更容易看清表情和空间深度"
        elif kind == "pattern_pocket":
            draw.rectangle((120,180,1120,850),fill=rgba(ink,40))
            draw.line((120,500,1120,500),fill=ink,width=80)
            for x in [250,520,820]: draw.ellipse((x,430,x+180,610),fill=a)
            label="活动口袋让停留发生在流线边缘，而不是堵住通行"
        else:
            for i in range(7): draw.rectangle((180+i*125,790-i*90,305+i*125,900-i*90),fill=a if i%2==0 else b,outline=ink,width=4)
            for x in [310,560,810]: draw.ellipse((x,540,x+45,585),fill=ink)
            label="可坐的台阶，让高差同时成为公共生活的看台"
        draw.text((620, 980), label, font=font(31), fill=ink, anchor="mm")
    elif kind.startswith("ching_"):
        if kind == "ching_point":
            draw.ellipse((580,450,660,530),fill=a); draw.line((170,490,1070,490),fill=ink,width=12)
            draw.rectangle((340,250,900,780),outline=b,width=18); label="点生成位置，线生成方向，面开始围合空间"
        elif kind == "ching_form":
            for x,y in [(130,260),(420,260),(710,260)]: draw.rectangle((x,y,x+250,y+250),outline=ink,width=12)
            draw.rectangle((475,315,615,455),fill=a); draw.ellipse((770,320,900,450),fill=paper,outline=b,width=12); label="加法与减法，改变体量也改变空间关系"
        elif kind == "ching_org":
            for cx,cy in [(250,350),(620,350),(990,350),(430,720),(810,720)]:
                draw.ellipse((cx-80,cy-80,cx+80,cy+80),fill=a)
                draw.line((620,520,cx,cy),fill=ink,width=8)
            draw.ellipse((530,430,710,610),fill=b); label="集中、线性、放射与组团，是空间组织的基本语法"
        else:
            draw.line((120,790,1120,220),fill=a,width=50)
            for t in [0.15,0.38,0.62,0.84]:
                x=120+(1120-120)*t; y=790+(220-790)*t
                draw.rectangle((x-90,y-90,x+90,y+90),outline=ink,width=10)
            label="流线不是剩余通道，它决定空间被理解的顺序"
        draw.text((620, 960), label, font=font(31), fill=ink, anchor="mm")


def diagram_card(cfg, folder, number, slide):
    canvas, draw = diagram_base(cfg)
    draw_name_badge(draw, slide["name"], cfg, "概念图解")
    diagram_art(draw, slide["kind"], cfg)
    draw.rectangle((0, 1040, W, H), fill=cfg["ink"])
    draw.rectangle((68, 1090, 240, 1103), fill=cfg["accent2"])
    headline = wrap(draw, slide["headline"], font(57, serif=True), 1080)
    draw.multiline_text((68, 1140), headline, font=font(57, serif=True), fill=cfg["paper"], spacing=12)
    bottom = draw.multiline_textbbox((68, 1140), headline, font=font(57, serif=True), spacing=12)[3]
    body = wrap(draw, slide["body"], font(29), 1070)
    draw.multiline_text((70, bottom+38), body, font=font(29), fill=rgba(cfg["paper"], 205), spacing=12)
    page_mark(draw, number)
    return save(canvas, folder, number)


def summary_card(cfg, folder):
    image = Image.open(sourced_image(cfg, "summary")).convert("RGB")
    image = crop_fill(image, (W, H), cfg.get("summary_focal", (0.5, 0.5)))
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Color(image).enhance(0.82)
    image = ImageEnhance.Sharpness(image).enhance(1.12)
    canvas = image.convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 75)))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0,0,24,H),fill=cfg["accent2"])
    draw_name_badge(draw, cfg["summary_name"], cfg, "总结案例")
    composite_panel(canvas, (55, 205, 1185, 1505), (8, 8, 8, 220), 20)
    draw = ImageDraw.Draw(canvas)
    draw.text((90,255),f"{cfg['author']} ×《{cfg['book']}》",font=font(29),fill=cfg["accent2"])
    statement=wrap(draw,cfg["summary"],font(68,serif=True),990)
    draw.multiline_text((88,360),statement,font=font(68,serif=True),fill=cfg["paper"],spacing=24)
    statement_bottom = draw.multiline_textbbox((88,360),statement,font=font(68,serif=True),spacing=24)[3]
    rule_y = max(880, statement_bottom + 70)
    draw.rectangle((90,rule_y,1125,rule_y+14),fill=cfg["accent2"])
    y=rule_y+80
    for item in cfg["takeaways"]:
        draw.ellipse((94,y+8,126,y+40),fill=cfg["accent2"])
        text=wrap(draw,item,font(31),930)
        draw.multiline_text((158,y),text,font=font(31),fill=rgba(cfg["paper"],230),spacing=10)
        y=draw.multiline_textbbox((158,y),text,font=font(31),spacing=10)[3]+48
    page_mark(draw,6)
    return save(canvas,folder,6)


def make_preview(paths, folder, bg):
    tw,th,gap=280,374,18
    sheet=Image.new("RGB",(tw*3+gap*4,th*2+gap*3),bg)
    for i,path in enumerate(paths):
        image=Image.open(path).convert("RGB").resize((tw,th),Image.Resampling.LANCZOS)
        x=gap+(i%3)*(tw+gap); y=gap+(i//3)*(th+gap)
        sheet.paste(image,(x,y))
    sheet.save(folder/"preview.jpg",quality=94,optimize=True)


def copy_file(cfg,folder):
    tags=" ".join(cfg["tags"])
    text=f"{cfg['author']} ×《{cfg['book']}》\n\n{cfg['copy']}\n\n{tags}\n"
    (folder/"发布文案.md").write_text(text,encoding="utf-8")


def source_file(cfg, folder):
    manifest = json.loads((SOURCE_ASSETS / "manifest.json").read_text(encoding="utf-8"))
    labels = {"hero": "01封面背景", "02": "02", "03": "03", "04": "04", "05": "05", "summary": "06总结背景"}
    records = [item for item in manifest if item["set"] == cfg["asset_set"]]
    records.sort(key=lambda item: ["hero", "02", "03", "04", "05", "summary"].index(item["slot"]))
    lines = ["# 图片来源（内部记录，不用于发布文案）", ""]
    for item in records:
        lines.append(f"- {labels[item['slot']]}：{item['commons_title']}；摄影/作者：{item['artist'] or '见原页面'}；许可：{item['license']}；{item['source_page']}")
    (folder / "图片来源.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


BOOKS = [
    {
        "slug":"01-帕拉斯玛-肌肤之目","author":"尤哈尼·帕拉斯玛","book":"肌肤之目","cover":"eyes-of-skin.jpg",
        "hook":"建筑，只用眼睛看就够了吗？","hook_size":79,"cover_line":"当视觉占据一切，身体正在失去理解空间的能力。","cover_footer":"重新唤醒触觉、听觉、温度与记忆",
        "cover_bg":"#160d0b","paper":"#f3e6d1","ink":"#170f0d","accent":"#9e1b16","accent2":"#e9b86a","preview":"#3b201d",
        "slides":[
            {"type":"photo","file":"eyes-01-saynatsalo.jpg","name":"珊纳特赛罗市政厅｜芬兰·阿尔瓦·阿尔托","headline":"砖的粗糙、木的温度，比造型更早抵达身体","body":"帕拉斯玛反对只有轮廓和照片感的建筑。真实空间会通过材料触感、脚步回声与光的变化被身体记住。","focal":(0.5,0.5)},
            {"type":"photo","file":"eyes-02-kamppi.jpg","name":"坎皮中心｜芬兰·赫尔辛基","headline":"建筑不是被观看的物体，而是被穿过的经验","body":"方向、距离、门洞与人群共同塑造城市内部。身体移动时，空间才真正从图像变成现实。","focal":(0.5,0.5)},
            {"type":"diagram","kind":"eye_layers","name":"从视觉中心主义中退一步","headline":"眼睛看到形式，身体判断它能不能被相信","body":"触觉会预判材料的温度，听觉会测量空间的远近，嗅觉和记忆则让地方变得难以替代。"},
            {"type":"diagram","kind":"door_handle","name":"门把手：建筑与身体的握手","headline":"最小的接触点，也能决定整栋建筑有没有人情味","body":"当手触碰把手，建筑第一次回应身体。细部因此不是装饰，而是空间伦理的起点。"},
        ],
        "summary":"建筑不是一张图。\n它是一场由全身完成的体验。","takeaways":["材料要让身体感到重量、温度与时间。","空间要允许听觉、触觉和记忆共同参与。","真正持久的建筑，不会把人降格成旁观者。"],
        "copy":"我们越来越习惯在照片里判断建筑，却很少问：身体进入之后会发生什么？\n\n帕拉斯玛在《肌肤之目》中批评视觉中心主义。建筑不只被眼睛观看，也被皮肤感受、被脚步丈量、被声音确认，并最终进入记忆。\n\n阿尔托的砖与木、城市内部的门洞和距离，甚至一个门把手，都在提醒我们：真正有力量的空间，不会把人变成旁观者。它会让全身参与。\n\n读完这本书，再看建筑时，你可能会先问温度、回声与触感，而不是先问它上不上镜。",
        "tags":["#尤哈尼帕拉斯玛","#肌肤之目","#建筑感官","#空间体验","#建筑材料","#建筑理论","#建筑书单","#设计师必读"]
    },
    {
        "slug":"02-拉斯姆森-体验建筑","author":"斯蒂恩·艾勒·拉斯姆森","book":"体验建筑","cover":"experiencing-architecture.jpg",
        "hook":"建筑不是照片，必须走进去才成立","hook_size":75,"cover_line":"尺度、节奏、质感、光与声音，都发生在移动之中。","cover_footer":"从身体经验重新学习建筑",
        "cover_bg":"#17191a","paper":"#f2ead6","ink":"#17191a","accent":"#d33d2e","accent2":"#f0c96b","preview":"#36322b",
        "slides":[
            {"type":"photo","file":"experience-01-pantheon.jpg","name":"万神殿｜意大利·罗马","headline":"一束移动的天光，让时间进入建筑","body":"穹顶并不只是一种形状。太阳移动时，光斑改变尺度、方向与气氛，人因此通过时间体验空间。","focal":(0.5,0.45)},
            {"type":"photo","file":"experience-02-campidoglio.jpg","name":"卡比托利欧广场｜意大利·罗马","headline":"广场不是空地，而是一间没有屋顶的房间","body":"地面图案、立面角度和入口方向共同制造围合感，让人的移动成为空间构图的一部分。","focal":(0.5,0.54)},
            {"type":"diagram","kind":"rhythm","name":"建筑的节奏","headline":"节奏不是复制同一根柱子，而是控制身体经过的时间","body":"间距、停顿、密度和重复共同形成空间节拍。只有走动起来，节奏才真正被听见。"},
            {"type":"diagram","kind":"body_scale","name":"尺度与身体","headline":"尺度不是图纸上的数字，而是空间如何回应身体","body":"同样的尺寸，因为高度、距离与光线不同，会产生亲密、庄严或压迫等完全不同的感受。"},
        ],
        "summary":"理解建筑，\n不能只靠看图。\n还要靠走、听、触摸与停留。","takeaways":["空间的比例必须回到身体经验中判断。","节奏与光线都需要在移动中被理解。","优秀建筑把日常使用转化为连续体验。"],
        "copy":"为什么很多建筑照片很好看，真正走进去却没有感觉？\n\n拉斯姆森在《体验建筑》中给出的答案很直接：建筑不是静止图像，而是一门必须被身体经历的艺术。尺度要靠身体比较，节奏要靠移动感受，光线会随着时间改变空间，声音也会暴露空间的真实形状。\n\n万神殿的天光、卡比托利欧广场的围合，都不是单独看立面就能理解的。\n\n读建筑，先别急着找最佳机位。走进去，停一下，听一听。",
        "tags":["#拉斯姆森","#体验建筑","#空间体验","#建筑尺度","#建筑光影","#建筑理论","#建筑书单","#设计师必读"]
    },
    {
        "slug":"03-诺伯格舒尔茨-场所精神","author":"克里斯蒂安·诺伯格-舒尔茨","book":"场所精神","cover":"genius-loci.jpg",
        "hook":"为什么有些地方，一到就能记住？","hook_size":78,"cover_line":"场所不是坐标，而是方向、边界、气候与生活共同形成的性格。","cover_footer":"建筑的任务，是让地方变得可辨认",
        "cover_bg":"#101817","paper":"#e7eadf","ink":"#101817","accent":"#2f6b5d","accent2":"#e1ba55","preview":"#263a34",
        "slides":[
            {"type":"photo","file":"genius-01-prague.jpg","name":"布拉格老城｜捷克·布拉格","headline":"天际线、街巷与地形共同制造城市性格","body":"地方之所以难以替代，不只因为单体建筑，而是因为方向、尺度和历史层次形成了稳定关系。","focal":(0.5,0.5)},
            {"type":"photo","file":"genius-02-navona.jpg","name":"纳沃纳广场｜意大利·罗马","headline":"一座广场的性格，来自边界如何围住生活","body":"连续立面、长轴空间与喷泉节点共同建立中心感，让日常活动获得清晰舞台。","focal":(0.5,0.5)},
            {"type":"diagram","kind":"compass","name":"方向与中心","headline":"知道自己面向哪里，是产生归属感的第一步","body":"路径、中心和地标让人在环境中建立位置。没有方向的空间，很难形成稳定记忆。"},
            {"type":"diagram","kind":"figure_ground","name":"边界与空地","headline":"场所不是剩下的空白，而是被边界认真定义的空间","body":"建筑体量与开放空间彼此塑造。边界过弱，地方失去性格；边界过强，生活又难以进入。"},
        ],
        "summary":"场所不是背景。\n它决定建筑为什么必须长成这样。","takeaways":["方向、中心与边界构成地方的基本结构。","气候、材料和生活方式赋予场所具体性格。","建筑应强化地方，而不是用通用造型覆盖地方。"],
        "copy":"为什么有些城市走过一次就能记住，有些空间离开后立刻模糊？\n\n《场所精神》认为，地方不是地图坐标，而是一套可以被身体识别的方向、边界、中心、气候与生活关系。\n\n布拉格的天际线与街巷、纳沃纳广场的围合与中心，都让人清楚知道自己在哪里。建筑的任务不是把一个通用造型放进场地，而是让地方原本隐藏的性格变得可见。\n\n真正属于场地的建筑，换一个地方就不再成立。",
        "tags":["#诺伯格舒尔茨","#场所精神","#建筑现象学","#场地设计","#城市空间","#建筑理论","#建筑书单","#设计师必读"]
    },
    {
        "slug":"04-简雅各布斯-美国大城市的死与生","author":"简·雅各布斯","book":"美国大城市的死与生","cover":"death-life.jpg",
        "hook":"城市越整齐，街道可能越没有生命","hook_size":77,"cover_line":"真正的安全与活力，来自混合、密度、短街区和持续出现的人。","cover_footer":"从真实街道出发，反对抽象规划",
        "cover_bg":"#15120f","paper":"#f1e6ce","ink":"#15120f","accent":"#b1452f","accent2":"#efc24f","preview":"#41322a",
        "slides":[
            {"type":"photo","file":"jacobs-01-washington-square.jpg","name":"华盛顿广场公园｜美国·纽约","headline":"公园的价值，不在图纸形状，而在周围有没有持续生活","body":"住宅、商店、街道与不同人群共同支持公共空间。孤立的绿地无法自动产生安全和活力。","focal":(0.5,0.52)},
            {"type":"diagram","kind":"street_eyes","name":"街道眼睛","headline":"街道安全，不只依靠监控，还依靠彼此看见","body":"面向街道的门窗、持续营业的店铺和真实行人，共同构成日常而有效的公共监督。"},
            {"type":"diagram","kind":"short_blocks","name":"短街区","headline":"路口越多，选择越多，城市生活越容易相遇","body":"短街区增加路线与转角，让步行、商业和偶遇不断发生；超级街区则更容易切断联系。"},
            {"type":"diagram","kind":"mixed_use","name":"混合使用","headline":"只有功能混合，街道才能从早到晚保持有人","body":"住宅、办公、商店与公共空间在不同时间带来人流，让街区避免只在某个时段短暂活跃。"},
        ],
        "summary":"好城市不是被一次规划完成的。\n它由无数日常关系持续生成。","takeaways":["街道安全来自持续出现的人和彼此看见。","短街区与功能混合增加选择和偶遇。","规划应观察真实生活，而不是迷信整齐图形。"],
        "copy":"城市越整齐，就一定越好吗？\n\n简·雅各布斯在《美国大城市的死与生》中反复提醒：从高空看起来完整的规划，可能正在地面上消灭真正的城市生活。\n\n安全来自“街道眼睛”，活力来自混合使用，短街区制造更多路线与偶遇，而公园必须依赖周边持续的人流。\n\n这本书最重要的方法不是一套固定答案，而是回到街道，观察真实的人怎样使用城市。城市不是被一次设计完成的，它每天都在被生活重新生成。",
        "tags":["#简雅各布斯","#美国大城市的死与生","#城市设计","#城市更新","#街道空间","#城市规划","#建筑书单","#设计师必读"]
    },
    {
        "slug":"05-阿尔多罗西-城市建筑学","author":"阿尔多·罗西","book":"城市建筑学","cover":"architecture-city.jpg",
        "hook":"城市会记住已经消失的建筑","hook_size":80,"cover_line":"类型、纪念物与集体记忆，让城市跨越具体功能继续存在。","cover_footer":"建筑不只服务当下，也储存时间",
        "cover_bg":"#1a1110","paper":"#f3e6cb","ink":"#1a1110","accent":"#df5a22","accent2":"#ffd84a","preview":"#4a2f24",
        "slides":[
            {"type":"photo","file":"rossi-01-san-cataldo.jpg","name":"圣卡塔尔多公墓｜意大利·摩德纳·阿尔多·罗西","headline":"没有窗的立方体，像一栋被抽空功能的城市住宅","body":"罗西用熟悉类型承载死亡与记忆。形式保持可辨认，却不再服从日常居住功能。","focal":(0.5,0.45)},
            {"type":"photo","file":"rossi-02-gallaratese.jpg","name":"加拉拉泰西住宅区｜意大利·米兰·阿尔多·罗西","headline":"重复不是单调，它可以制造城市尺度的背景","body":"长廊、柱列与连续立面弱化单个住宅，让集体生活获得稳定而可识别的框架。","focal":(0.5,0.5)},
            {"type":"photo","file":"rossi-03-teatro-del-mondo.jpg","name":"世界剧场｜意大利·威尼斯·阿尔多·罗西","headline":"一座临时建筑，也能唤起整座城市的记忆","body":"剧场以熟悉的塔楼原型漂浮在威尼斯水面，短暂存在却与城市历史形成强烈联系。","focal":(0.5,0.5)},
            {"type":"diagram","kind":"typology","name":"类型与城市记忆","headline":"功能会变化，类型却能在城市中长期存活","body":"住宅、塔楼、庭院与街道反复出现并持续变形。城市记忆因此不依赖单一建筑，而依赖可延续的类型。"},
        ],
        "summary":"城市不是建筑的集合。\n它是一套被时间不断改写的集体记忆。","takeaways":["类型让建筑跨越具体功能继续存在。","纪念物是城市记忆的稳定锚点。","理解城市，需要同时阅读空间与时间。"],
        "copy":"城市为什么会记住某些建筑，却忘掉另一些？\n\n阿尔多·罗西在《城市建筑学》中把城市理解为一套被时间不断改写的集体记忆。功能会消失，生活会变化，但住宅、塔楼、庭院和街道等类型仍会持续出现。\n\n圣卡塔尔多墓园、加拉拉泰西住宅和漂浮在威尼斯水面的世界剧场，都在使用熟悉形式储存新的意义。\n\n建筑不只服务眼前功能。它也可能成为城市记住自己的一种方式。",
        "tags":["#阿尔多罗西","#城市建筑学","#城市记忆","#建筑类型学","#后现代建筑","#建筑理论","#建筑书单","#设计师必读"]
    },
    {
        "slug":"06-凯文林奇-城市意象","author":"凯文·林奇","book":"城市意象","cover":"image-city.jpg",
        "hook":"为什么有些城市，让人永远找不到方向？","hook_size":74,"cover_line":"路径、边界、区域、节点与地标，共同构成脑海里的城市地图。","cover_footer":"可识别，比整齐更重要",
        "cover_bg":"#071827","paper":"#e5eef2","ink":"#071827","accent":"#0873a9","accent2":"#f5c34d","preview":"#18384d",
        "slides":[
            {"type":"photo","file":"lynch-01-boston.jpg","name":"波士顿城市中心｜美国·马萨诸塞州","headline":"城市可以复杂，但必须让人知道自己在哪里","body":"水岸、绿地、街区与天际线形成不同层次。可识别性并不要求城市简单，而要求线索清楚。","focal":(0.5,0.5)},
            {"type":"diagram","kind":"city_elements","name":"城市意象的五个元素","headline":"我们不是记住整张地图，而是记住五类线索","body":"路径、边界、区域、节点和地标共同组成认知地图，让人在复杂环境里建立方向。"},
            {"type":"diagram","kind":"path_edge","name":"路径与边界","headline":"路径负责串联经验，边界决定城市如何被分开","body":"道路、河流、铁路与街墙既组织移动，也会形成心理上的连接或阻隔。"},
            {"type":"diagram","kind":"nodes_landmarks","name":"节点与地标","headline":"节点让人停下，地标让人重新确认方向","body":"路口、广场和交通枢纽承担决策；高塔、山体和独特建筑则提供远距离参照。"},
        ],
        "summary":"一座好读的城市，\n会不断告诉你：\n你在哪里，下一步可以去哪里。","takeaways":["路径、边界、区域、节点与地标构成认知地图。","可识别性允许复杂，但拒绝没有线索。","城市设计应从人的移动和记忆出发。"],
        "copy":"为什么有些城市第一次去就能找到方向，有些地方导航一关就立刻迷路？\n\n凯文·林奇在《城市意象》中提出五个基础元素：路径、边界、区域、节点和地标。人并不会记住完整地图，而是依靠这些线索在脑海里拼出城市。\n\n道路串联经验，河流和街墙形成边界，广场与路口承担决策，地标则帮助我们重新定位。\n\n一座城市可以复杂，但不能没有线索。真正友好的城市，会不断告诉人：你在哪里，下一步可以去哪里。",
        "tags":["#凯文林奇","#城市意象","#城市设计","#认知地图","#城市规划","#空间分析","#建筑书单","#设计师必读"]
    },
    {
        "slug":"07-亚历山大-建筑模式语言","author":"克里斯托弗·亚历山大","book":"建筑模式语言","cover":"pattern-language.jpg",
        "hook":"好建筑，真的可以像语言一样被学习","hook_size":73,"cover_line":"模式不是标准答案，而是反复有效的空间关系。","cover_footer":"从门口、窗边到街区，重新组织日常生活",
        "cover_bg":"#16110a","paper":"#f2e8cc","ink":"#16110a","accent":"#9a3d27","accent2":"#e7b84c","preview":"#403224",
        "slides":[
            {"type":"diagram","kind":"pattern_entry","name":"模式 112｜入口过渡","headline":"好的入口，不会让人从街道一步跌进室内","body":"门廊、台阶、转折和光线变化共同形成过渡，让身体有时间完成公共与私密之间的转换。"},
            {"type":"diagram","kind":"pattern_light","name":"模式 159｜房间两侧有光","headline":"只有一面采光的房间，表情和空间都容易变平","body":"来自不同方向的光减少强烈反差，也让人、家具与墙面拥有更清楚的空间层次。"},
            {"type":"diagram","kind":"pattern_pocket","name":"模式 124｜活动口袋","headline":"人喜欢停在流线边缘，而不是站在流线中央","body":"把座位与小空间安排在主要通行旁边，既能观察活动，也不会阻挡他人经过。"},
            {"type":"diagram","kind":"pattern_stairs","name":"模式 125｜可坐的台阶","headline":"台阶不仅解决高差，也可以成为公共生活的看台","body":"当踏步尺度允许停留，交通构件就会转化为见面、观看和休息的场所。"},
        ],
        "summary":"模式不是复制形式。\n它是在不同场地里，\n反复解决同类生活问题。","takeaways":["先描述真实问题，再寻找空间关系。","模式可以组合，却必须根据场地重新解释。","好设计让日常行为自然发生，而不是强迫发生。"],
        "copy":"好建筑有没有可以学习的“语法”？\n\n克里斯托弗·亚历山大在《建筑模式语言》中整理了从城市到房间的大量空间模式。它们不是标准图集，而是对反复出现的生活问题所做的关系总结。\n\n入口需要过渡，房间最好两侧有光，人喜欢停在流线边缘，台阶也可以成为公共看台。\n\n模式真正有用的地方，不是让所有建筑长得一样，而是帮助设计者先看见生活，再组织空间。",
        "tags":["#克里斯托弗亚历山大","#建筑模式语言","#空间设计","#建筑方法","#建筑概念","#建筑理论","#建筑书单","#设计师必读"]
    },
    {
        "slug":"08-程大锦-建筑形式空间和秩序","author":"程大锦","book":"建筑：形式、空间和秩序","cover":"form-space-order.jpg",
        "hook":"所有建筑形式，都从几种基本关系开始","hook_size":75,"cover_line":"点、线、面、体量、空间组织与流线，是复杂设计背后的共同语法。","cover_footer":"把建筑拆开，再重新理解它",
        "cover_bg":"#0b1823","paper":"#e8edf0","ink":"#0b1823","accent":"#146f9b","accent2":"#e34a38","preview":"#203746",
        "slides":[
            {"type":"diagram","kind":"ching_point","name":"点、线、面","headline":"空间不是突然出现的，它从位置和方向开始","body":"点确定位置，线建立方向，面形成边界。最复杂的建筑，也可以追溯到这些基础元素。"},
            {"type":"diagram","kind":"ching_form","name":"加法与减法","headline":"增加体量与挖去体量，会产生完全不同的空间性格","body":"加法强调组合与连接，减法强调内部与空洞。形式变化同时改变光、入口与流线。"},
            {"type":"diagram","kind":"ching_org","name":"空间组织","headline":"房间怎样彼此连接，决定建筑怎样被使用","body":"集中、线性、放射、组团和网格等组织方式，会带来不同的中心、层级与方向感。"},
            {"type":"diagram","kind":"ching_circulation","name":"流线与空间顺序","headline":"流线不是剩余通道，而是建筑被理解的顺序","body":"入口、路径、转折与终点共同控制空间怎样逐步展开，也决定人先看见什么、后到达哪里。"},
        ],
        "summary":"复杂建筑并不神秘。\n它只是把基础元素，\n组织成更丰富的关系。","takeaways":["从点、线、面理解形式的生成。","用空间组织建立中心、层级与方向。","让流线主动参与空间叙事。"],
        "copy":"建筑形式看起来千变万化，背后却始终在处理一些基础关系。\n\n程大锦在《建筑：形式、空间和秩序》中，从点、线、面开始，逐步解释体量怎样生成、空间怎样组织、流线怎样展开。\n\n加法与减法改变形体，集中、线性和组团建立不同秩序，入口与路径则决定建筑被理解的先后顺序。\n\n这是一本很适合反复翻看的工具书。设计卡住时，把问题拆回最基础的元素，复杂关系往往会重新变得清楚。",
        "tags":["#程大锦","#建筑形式空间和秩序","#建筑基础","#空间设计","#建筑制图","#建筑概念","#建筑书单","#设计师必读"]
    },
]


PHOTO_EDITORIAL = {
    "01-帕拉斯玛-肌肤之目": {
        "asset_set": "01-eyes-of-skin",
        "cover_en": "SENSE / BODY / MEMORY",
        "cover_thesis": "空间先被身体感到，之后才被眼睛解释。",
        "hero_name": "玛利亚别墅｜芬兰·诺尔马库·阿尔瓦·阿尔托",
        "summary_name": "芬兰大厦室内细部｜芬兰·赫尔辛基·阿尔瓦·阿尔托",
        "hero_focal": (0.55, 0.52), "summary_focal": (0.5, 0.5),
        "slides": [
            {"type":"photo","file":"02","name":"珊纳特赛罗市政厅｜芬兰·阿尔瓦·阿尔托","headline":"砖的粗糙、木的温度，比造型更早抵达身体","body":"庭院、砖墙与木构共同形成可触摸的公共性。帕拉斯玛关心的不是表面效果，而是材料如何留下重量、温度和时间。","focal":(0.5,0.5)},
            {"type":"photo","file":"03","name":"珊纳特赛罗市政厅室内细部｜芬兰·阿尔瓦·阿尔托","headline":"真正的细部，会主动邀请身体靠近","body":"窗边植物、砖、木框与光线形成多重触感。空间的可信度，常常来自这些不抢镜却可被身体确认的细节。","focal":(0.5,0.48)},
            {"type":"photo","file":"04","name":"帕伊米奥疗养院｜芬兰·阿尔瓦·阿尔托","headline":"建筑可以照顾身体，而不只是容纳身体","body":"尺度、色彩、日照与安静程度都围绕病人的感受组织。功能在这里不是抽象指标，而是具体的身心经验。","focal":(0.5,0.5)},
            {"type":"photo","file":"05","name":"阿尔瓦·阿尔托自宅室内｜芬兰·赫尔辛基","headline":"居住感来自光、材料与日常物件的共同作用","body":"窗光、木材、织物与家具把空间从几何容器变成生活场所。建筑因此进入记忆，而不只是进入照片。","focal":(0.5,0.48)},
        ],
    },
    "02-拉斯姆森-体验建筑": {
        "asset_set": "02-experiencing-architecture",
        "cover_en": "LIGHT / RHYTHM / SCALE",
        "cover_thesis": "建筑只有在移动、停留与时间中才真正成立。",
        "hero_name": "万神殿穹顶天窗｜意大利·罗马",
        "summary_name": "圣母大殿穹顶｜意大利·罗马",
        "hero_focal": (0.5, 0.5), "summary_focal": (0.5, 0.46),
        "slides": [
            {"type":"photo","file":"02","label":"历史图像","name":"万神殿内部｜乔瓦尼·保罗·帕尼尼绘画","headline":"一束移动的天光，让时间进入建筑","body":"穹顶并不只是一种形状。光斑随着太阳移动，尺度、方向与气氛也随之变化，空间因此拥有时间。","focal":(0.5,0.45)},
            {"type":"photo","file":"03","name":"卡比托利欧广场｜意大利·罗马·米开朗琪罗","headline":"广场不是空地，而是一间没有屋顶的房间","body":"地面图案、围合立面和进入方向共同塑造空间。只有实际走过，人才能感到尺度怎样控制秩序。","focal":(0.5,0.5)},
            {"type":"photo","file":"04","label":"历史图像","name":"圣马可广场｜卡纳莱托绘画","headline":"连续立面和钟楼，共同建立城市的节奏","body":"重复、变化与远近层次让广场拥有可被行走感知的节拍。节奏不是图纸符号，而是移动中的时间。","focal":(0.5,0.48)},
            {"type":"photo","file":"05","name":"总督宫柱廊｜意大利·威尼斯","headline":"柱列的间距，让身体直接读懂空间秩序","body":"明暗交替、重复拱券和步行速度形成连续经验。建筑的比例，最终仍要由身体来完成判断。","focal":(0.5,0.5)},
        ],
    },
    "03-诺伯格舒尔茨-场所精神": {
        "asset_set": "03-genius-loci",
        "cover_en": "PLACE / ORIENTATION / IDENTITY",
        "cover_thesis": "地方不是坐标，而是一套可被辨认和记住的关系。",
        "hero_name": "布拉格城市天际线｜捷克·布拉格",
        "summary_name": "查理大桥与布拉格天际线｜捷克·布拉格",
        "hero_focal": (0.5, 0.45), "summary_focal": (0.5, 0.48),
        "slides": [
            {"type":"photo","file":"02","name":"布拉格老城广场｜捷克·布拉格","headline":"天际线、街巷与地标，共同制造城市性格","body":"地方的可辨认性来自多种关系叠加：方向、尺度、历史层次和持续使用，而不是某一栋孤立建筑。","focal":(0.5,0.46)},
            {"type":"photo","file":"03","name":"纳沃纳广场｜意大利·罗马","headline":"一座广场的性格，来自边界如何围住生活","body":"连续立面、长轴空间和喷泉节点建立中心感，让人在进入时迅速理解方向与位置。","focal":(0.5,0.52)},
            {"type":"photo","file":"04","name":"古罗马广场｜意大利·罗马","headline":"遗迹、地形与城市生活，让场所拥有时间厚度","body":"场所精神不是复古造型，而是自然、建造和历史彼此留下的痕迹。建筑要回应这些已经存在的关系。","focal":(0.5,0.52)},
            {"type":"photo","file":"05","name":"特拉斯提弗列街道｜意大利·罗马","headline":"普通街道也能形成强烈的地方身份","body":"墙面尺度、路面材料、光影和转折共同构成可感知的日常环境。地方感往往藏在连续而具体的细节里。","focal":(0.5,0.5)},
        ],
    },
    "04-简雅各布斯-美国大城市的死与生": {
        "asset_set": "04-death-and-life",
        "cover_en": "STREET / DIVERSITY / LIFE",
        "cover_thesis": "真正的城市活力，来自持续发生的普通生活。",
        "hero_name": "西四街街景｜美国·纽约·格林尼治村",
        "summary_name": "华盛顿广场公园｜美国·纽约",
        "hero_focal": (0.5, 0.52), "summary_focal": (0.5, 0.48),
        "slides": [
            {"type":"photo","file":"02","name":"华盛顿广场拱门｜美国·纽约","headline":"公园的价值，取决于周围有没有持续生活","body":"公共空间不会自动产生安全和活力。住宅、商店、街道与不断出现的人，才是公园真正的支持系统。","focal":(0.5,0.48)},
            {"type":"photo","file":"03","name":"格林尼治村沿街商店｜美国·纽约","headline":"面向街道的店铺，就是最日常的“街道眼睛”","body":"透明橱窗、频繁出入和长期经营让街道被持续看见。安全由真实关系产生，而不只依靠设备。","focal":(0.5,0.5)},
            {"type":"photo","file":"04","name":"西四街路口｜美国·纽约·格林尼治村","headline":"路口越多，选择越多，城市生活越容易相遇","body":"短街区制造更多转弯、路径和偶遇，也让步行与小商业获得连续机会。连接比整齐更重要。","focal":(0.5,0.52)},
            {"type":"photo","file":"05","name":"The Bitter End音乐酒吧｜美国·纽约","headline":"混合使用，让街道在不同时间保持有人","body":"餐饮、演出、住宅和日常零售交错出现，街区就不会只在单一时段短暂活跃。","focal":(0.5,0.52)},
        ],
    },
    "05-阿尔多罗西-城市建筑学": {
        "asset_set": "05-architecture-city",
        "cover_en": "TYPE / MEMORY / TIME",
        "cover_thesis": "功能会消失，建筑类型却能继续储存城市记忆。",
        "hero_name": "圣卡塔尔多公墓｜意大利·摩德纳·阿尔多·罗西",
        "summary_name": "舒岑大街街区｜德国·柏林·阿尔多·罗西",
        "hero_focal": (0.5, 0.48), "summary_focal": (0.5, 0.52),
        "slides": [
            {"type":"photo","file":"02","name":"圣卡塔尔多公墓｜意大利·摩德纳·阿尔多·罗西","headline":"熟悉的城市类型，可以承载死亡与记忆","body":"柱廊、庭院和纪念性体量延续城市语汇，却不再服务日常居住。类型因此跨越具体功能继续存在。","focal":(0.5,0.5)},
            {"type":"photo","file":"03","name":"加拉拉泰西住宅区｜意大利·米兰·阿尔多·罗西","headline":"重复不是单调，它可以制造城市尺度的背景","body":"长廊、柱列与连续立面弱化单个住宅，让集体生活获得稳定且可辨认的框架。","focal":(0.5,0.5)},
            {"type":"photo","file":"04","name":"世界剧场｜意大利·威尼斯·阿尔多·罗西","headline":"一座临时建筑，也能唤起整座城市的记忆","body":"塔楼原型漂浮在威尼斯水面，短暂存在却与城市历史建立强烈联系。记忆不等于永久。","focal":(0.5,0.52)},
            {"type":"photo","file":"05","name":"博纳方坦博物馆｜荷兰·马斯特里赫特·阿尔多·罗西","headline":"新建筑也可以用类型回应城市，而不是模仿历史","body":"塔、轴线和厚重体量构成清晰的城市标志，同时与河岸尺度和城市轮廓发生关系。","focal":(0.5,0.5)},
        ],
    },
    "06-凯文林奇-城市意象": {
        "asset_set": "06-image-city",
        "cover_en": "PATH / EDGE / NODE / LANDMARK",
        "cover_thesis": "好读的城市，会不断告诉人自己在哪里。",
        "hero_name": "波士顿城市天际线｜美国·马萨诸塞州",
        "summary_name": "波士顿与查尔斯河｜美国·马萨诸塞州",
        "hero_focal": (0.5, 0.48), "summary_focal": (0.5, 0.5),
        "slides": [
            {"type":"photo","file":"02","name":"波士顿市中心航拍｜美国·马萨诸塞州","headline":"城市不怕复杂，怕的是没有清晰线索","body":"道路、街区、绿地与高层形成不同层级。城市可以密集，但必须让人在移动中不断重新定位。","focal":(0.5,0.48)},
            {"type":"photo","file":"03","name":"泽西市滨水天际线｜美国·新泽西州","headline":"水岸既是边界，也可以成为识别城市的正面","body":"河流分隔地区，同时提供连续视线和远距离参照。边界不一定封闭，也能组织城市形象。","focal":(0.5,0.5)},
            {"type":"photo","file":"04","name":"洛杉矶河与城市网格航拍｜美国·洛杉矶","headline":"交通廊道会连接城市，也可能切断城市","body":"河道、铁路和高速路都是强边界。它们组织方向，却也可能制造难以跨越的心理与空间阻隔。","focal":(0.5,0.5)},
            {"type":"photo","file":"05","name":"洛杉矶市政厅｜美国·洛杉矶","headline":"地标让人在远处就能重新确认方向","body":"独特轮廓和城市位置使建筑成为认知锚点。地标的价值不只在造型，更在它与路径和节点的关系。","focal":(0.5,0.5)},
        ],
    },
    "07-亚历山大-建筑模式语言": {
        "asset_set": "07-pattern-language",
        "cover_en": "PATTERN / RELATION / LIFE",
        "cover_thesis": "模式不是复制形式，而是反复解决真实生活问题。",
        "hero_name": "帕利公园入口花植活动｜美国·纽约",
        "summary_name": "田野广场｜意大利·锡耶纳",
        "hero_focal": (0.5, 0.5), "summary_focal": (0.5, 0.5),
        "slides": [
            {"type":"photo","file":"02","name":"冈布尔住宅入口｜美国·帕萨迪纳·格林兄弟","headline":"好的入口，会让身体逐步完成从外到内的转换","body":"车道、台阶、深檐与门廊构成连续过渡。入口不是墙上的洞，而是一段有时间的空间。","focal":(0.5,0.5)},
            {"type":"photo","file":"03","name":"冈布尔住宅室内｜美国·帕萨迪纳·格林兄弟","headline":"光、木作与家具共同组织可停留的房间","body":"模式关注的是生活关系：人坐在哪里、光从哪里进入、视线怎样连接，而不是单一造型。","focal":(0.5,0.5)},
            {"type":"photo","file":"04","name":"西班牙阶梯｜意大利·罗马","headline":"台阶不仅解决高差，也能成为公共生活的看台","body":"当踏步尺度允许停留，交通构件就会转化为见面、观看和休息的公共场所。","focal":(0.5,0.5)},
            {"type":"photo","file":"05","name":"帕利公园｜美国·纽约","headline":"人喜欢停在流线边缘，而不是站在流线中央","body":"树荫、座椅、水墙和入口视线构成城市活动口袋，让人既能观察街道，也能短暂停留。","focal":(0.5,0.5)},
        ],
    },
    "08-程大锦-建筑形式空间和秩序": {
        "asset_set": "08-form-space-order",
        "cover_en": "FORM / SPACE / ORDER",
        "cover_thesis": "复杂建筑，始终由基础元素与关系组织而成。",
        "hero_name": "巴塞罗那德国馆室内｜西班牙·密斯·凡·德·罗",
        "summary_name": "圆厅别墅｜意大利·维琴察·安德烈亚·帕拉第奥",
        "hero_focal": (0.5, 0.5), "summary_focal": (0.5, 0.5),
        "slides": [
            {"type":"photo","file":"02","name":"巴塞罗那德国馆｜西班牙·密斯·凡·德·罗","headline":"墙面、柱与屋顶，可以把开放空间组织出方向","body":"独立平面不只围合房间，也引导视线和移动。点、线、面在真实建筑中变成可被穿过的秩序。","focal":(0.5,0.5)},
            {"type":"photo","file":"03","name":"Habitat 67｜加拿大·蒙特利尔·莫西·萨夫迪","headline":"体量的加法组合，会同时创造室内与露台","body":"标准模块通过叠加、错动和留空形成复杂住宅群。形式变化同时改变采光、入口与公共关系。","focal":(0.5,0.5)},
            {"type":"photo","file":"04","name":"古根海姆博物馆室内坡道｜美国·纽约·弗兰克·劳埃德·赖特","headline":"流线不是剩余通道，而是建筑被理解的顺序","body":"连续坡道把移动、观看和空间中心结合起来。人的路径直接成为建筑最主要的组织结构。","focal":(0.5,0.5)},
            {"type":"photo","file":"05","name":"索尔克研究所庭院｜美国·拉霍亚·路易·康","headline":"一条轴线，可以同时建立中心、方向与远景","body":"对称体量、中央水渠与海平线形成强烈秩序。空间组织让复杂建筑获得清楚的阅读方式。","focal":(0.5,0.5)},
        ],
    },
}


# Distinct visual systems for the revised eight-book series.  The original book
# cover is always mounted as-is; only sourced architecture photographs are
# cropped, colour-balanced and sharpened for editorial composition.
VISUAL_PROFILES = {
    "01-帕拉斯玛-肌肤之目": {"kind": "senses", "c1": "玛利亚别墅室内｜芬兰·阿尔瓦·阿尔托", "c2": "阿尔托工作室｜芬兰·赫尔辛基", "02b": "帕伊米奥疗养院｜芬兰·阿尔瓦·阿尔托", "06b": "芬兰大厦外观｜芬兰·赫尔辛基·阿尔瓦·阿尔托"},
    "02-拉斯姆森-体验建筑": {"kind": "movement", "c1": "万神殿外观｜意大利·罗马", "c2": "圆厅别墅｜意大利·维琴察·帕拉第奥", "02b": "坦比哀多礼拜堂｜意大利·罗马·布拉曼特", "06b": "圣马可广场柱廊｜卡纳莱托绘画"},
    "03-诺伯格舒尔茨-场所精神": {"kind": "place", "c1": "小城区街道｜捷克·布拉格", "c2": "圣尼古拉教堂与布拉格屋顶｜捷克·布拉格", "02b": "查理大桥｜捷克·布拉格", "06b": "田野广场｜意大利·锡耶纳"},
    "04-简雅各布斯-美国大城市的死与生": {"kind": "street", "c1": "格林尼治村公共空间｜美国·纽约", "c2": "格林尼治村住宅街｜美国·纽约", "02b": "华盛顿广场公园｜美国·纽约", "06b": "格林尼治村沿街店铺｜美国·纽约"},
    "05-阿尔多罗西-城市建筑学": {"kind": "memory", "c1": "圣卡塔尔多公墓骨灰堂｜意大利·摩德纳·阿尔多·罗西", "c2": "卡洛·费利切剧院｜意大利·热那亚·阿尔多·罗西", "02b": "加拉拉泰西住宅区｜意大利·米兰·阿尔多·罗西", "06b": "舒岑大街街区｜德国·柏林·阿尔多·罗西"},
    "06-凯文林奇-城市意象": {"kind": "map", "c1": "1911年波士顿城市地图｜美国·波士顿", "c2": "波士顿港历史航拍｜美国·波士顿", "02b": "马歇尔街与联合街路口｜美国·波士顿", "06b": "港湾高速公路｜美国·洛杉矶"},
    "07-亚历山大-建筑模式语言": {"kind": "pattern", "c1": "克雷斯吉学院｜美国·圣克鲁兹·查尔斯·摩尔", "c2": "皮蒂宫庭院｜意大利·佛罗伦萨", "02b": "冈布尔住宅入口｜美国·帕萨迪纳·格林兄弟", "06b": "西班牙阶梯公共生活｜意大利·罗马"},
    "08-程大锦-建筑形式空间和秩序": {"kind": "grammar", "c1": "范斯沃斯住宅｜美国·伊利诺伊·密斯·凡·德·罗", "c2": "流水别墅｜美国·宾夕法尼亚·弗兰克·劳埃德·赖特", "02b": "圣索菲亚大教堂穹顶空间｜土耳其·伊斯坦布尔", "06b": "万神殿外观｜意大利·罗马"},
}


DESIGN_LOGIC = {
    "01-帕拉斯玛-肌肤之目": {"operator": "感官回波", "chain": ["材料", "身体", "记忆"], "rule": "照片呈现真实触感，信息区记录身体收到的信号。"},
    "02-拉斯姆森-体验建筑": {"operator": "移动序列", "chain": ["行走", "光线", "时间"], "rule": "空间用连续视点组织，阅读顺序模拟身体移动。"},
    "03-诺伯格舒尔茨-场所精神": {"operator": "场所剖面", "chain": ["方向", "边界", "身份"], "rule": "天际线、街道与地标分层出现，建立地方的可辨认性。"},
    "04-简雅各布斯-美国大城市的死与生": {"operator": "街道观察", "chain": ["街道眼睛", "混合使用", "持续生活"], "rule": "用观察记录与并置照片呈现日常关系，而非抽象规划。"},
    "05-阿尔多罗西-城市建筑学": {"operator": "类型档案", "chain": ["类型", "时间", "集体记忆"], "rule": "案例像档案被编号、归类，强调形式如何跨越功能延续。"},
    "06-凯文林奇-城市意象": {"operator": "认知图例", "chain": ["路径", "边界", "节点", "地标"], "rule": "照片保持清楚，路径与图例只在独立信息区建立阅读框架。"},
    "07-亚历山大-建筑模式语言": {"operator": "模式节点", "chain": ["问题", "空间关系", "生活"], "rule": "每页像一张可组合的模式卡，先说明问题，再给出关系。"},
    "08-程大锦-建筑形式空间和秩序": {"operator": "空间语法", "chain": ["点", "线", "面", "体量", "秩序"], "rule": "案例照片与基础元素清单分开呈现，从构件关系解释形式。"},
}


def _profile(cfg):
    return VISUAL_PROFILES[cfg["slug"]]


def _logic(cfg):
    return DESIGN_LOGIC[cfg["slug"]]


def _load_photo(cfg, slot, focal=(0.5, 0.5), mono=False):
    image = Image.open(sourced_image(cfg, slot)).convert("RGB")
    image = ImageEnhance.Contrast(image).enhance(1.10)
    image = ImageEnhance.Color(image).enhance(0.76 if mono else 0.96)
    image = ImageEnhance.Sharpness(image).enhance(1.22)
    return image


def _paste_crop(canvas, image, box, focal=(0.5, 0.5), border=None, width=0):
    x1, y1, x2, y2 = box
    crop = crop_fill(image, (x2 - x1, y2 - y1), focal)
    canvas.alpha_composite(crop.convert("RGBA"), (x1, y1))
    if border and width:
        ImageDraw.Draw(canvas).rectangle(box, outline=border, width=width)


def _paste_circle(canvas, image, box, focal=(0.5, 0.5), border="#ffffff", width=10):
    x1, y1, x2, y2 = box
    crop = crop_fill(image, (x2 - x1, y2 - y1), focal).convert("RGBA")
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, crop.width - 1, crop.height - 1), fill=255)
    crop.putalpha(mask)
    canvas.alpha_composite(crop, (x1, y1))
    ImageDraw.Draw(canvas).ellipse(box, outline=border, width=width)


def _mounted_cover(canvas, cfg, box):
    cover = Image.open(ASSETS / "covers" / cfg["cover"]).convert("RGB")
    x1, y1, x2, y2 = box
    fitted = fit_inside(cover, (x2 - x1 - 24, y2 - y1 - 24))
    x = x1 + (x2 - x1 - fitted.width) // 2
    y = y1 + (y2 - y1 - fitted.height) // 2
    shadow = Image.new("RGBA", (fitted.width + 54, fitted.height + 54), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle((19, 19, fitted.width + 35, fitted.height + 35), fill=(0, 0, 0, 175))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    canvas.alpha_composite(shadow, (x - 19, y - 13))
    ImageDraw.Draw(canvas).rectangle((x - 10, y - 10, x + fitted.width + 10, y + fitted.height + 10), fill="#f7f3e9")
    canvas.alpha_composite(fitted.convert("RGBA"), (x, y))


def _small_label(draw, text, box, fill=(8, 8, 8, 214), color="#fffaf0"):
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill=fill)
    size = 20
    f = font(size)
    while size > 14 and draw.textbbox((0, 0), text, font=f)[2] > x2 - x1 - 26:
        size -= 1
        f = font(size)
    clipped = text
    while draw.textbbox((0, 0), clipped, font=f)[2] > x2 - x1 - 26 and len(clipped) > 8:
        clipped = clipped[:-2]
    if clipped != text:
        clipped += "…"
    draw.text((x1 + 13, (y1 + y2) // 2), clipped, font=f, fill=color, anchor="lm")


def _draw_cover_title(canvas, cfg, box, light=False):
    draw = ImageDraw.Draw(canvas)
    x1, y1, x2, y2 = box
    fill = rgba("#f4efe3", 238) if light else (7, 7, 7, 224)
    ink = cfg["ink"] if light else cfg["paper"]
    composite_panel(canvas, box, fill, 12)
    draw = ImageDraw.Draw(canvas)
    draw.text((x1 + 34, y1 + 28), f"{cfg['author']} ×《{cfg['book']}》", font=font(29), fill=cfg["accent2"] if not light else cfg["accent"])
    hook_font = font(63 if len(cfg["hook"]) < 18 else 57, serif=True)
    hook = wrap(draw, cfg["hook"], hook_font, x2 - x1 - 68)
    draw.multiline_text((x1 + 32, y1 + 96), hook, font=hook_font, fill=ink, spacing=8)
    hb = draw.multiline_textbbox((x1 + 32, y1 + 96), hook, font=hook_font, spacing=8)[3]
    rule_y = min(y2 - 120, hb + 24)
    draw.rectangle((x1 + 34, rule_y, x2 - 34, rule_y + 9), fill=cfg["accent2"])
    draw.text((x1 + 34, rule_y + 27), cfg["cover_en"], font=font(27), fill=cfg["accent"] if light else cfg["accent2"])
    line_size = 22 if len(cfg["cover_line"]) > 25 else 24
    line_font = font(line_size)
    line = wrap(draw, cfg["cover_line"], line_font, x2 - x1 - 68)
    draw.multiline_text((x1 + 34, rule_y + 70), line, font=line_font, fill=rgba(cfg["ink"] if light else cfg["paper"], 220), spacing=6)


def cover_card(cfg, folder):
    profile = _profile(cfg)
    kind = profile["kind"]
    hero = _load_photo(cfg, "hero", mono=kind in {"memory", "map"})
    c1 = _load_photo(cfg, "c1", mono=kind == "memory")
    c2 = _load_photo(cfg, "c2", mono=kind == "memory")
    canvas = Image.new("RGBA", (W, H), rgba(cfg["ink"]))
    draw = ImageDraw.Draw(canvas)

    # Eight different collage grammars: tactile strips, oculus/perspective,
    # landscape strata, contact sheet, typology archive, cognitive map,
    # pattern modules and point-line-plane analysis.
    if kind == "senses":
        _paste_crop(canvas, hero, (0, 0, 810, H), cfg.get("hero_focal", (0.5, 0.5)))
        _paste_crop(canvas, c1, (735, 0, W, 780), (0.55, 0.5), cfg["paper"], 10)
        _paste_crop(canvas, c2, (720, 810, W, 1380), (0.5, 0.5), cfg["accent2"], 10)
        draw.rectangle((0, 0, 30, H), fill=cfg["accent2"])
        title_box, cover_box = (55, 120, 735, 760), (785, 1110, 1165, 1580)
    elif kind == "movement":
        _paste_crop(canvas, hero, (0, 0, W, H), cfg.get("hero_focal", (0.5, 0.5)))
        canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 55)))
        _paste_circle(canvas, c1, (715, 80, 1180, 545), (0.5, 0.5), cfg["accent2"], 13)
        _paste_crop(canvas, c2, (715, 590, 1180, 1015), (0.5, 0.5), cfg["paper"], 11)
        title_box, cover_box = (55, 170, 710, 805), (80, 1090, 425, 1575)
    elif kind == "place":
        _paste_crop(canvas, hero, (0, 0, W, 750), cfg.get("hero_focal", (0.5, 0.5)))
        _paste_crop(canvas, c1, (0, 760, 690, 1240), (0.5, 0.5), cfg["paper"], 8)
        _paste_crop(canvas, c2, (700, 760, W, H), (0.5, 0.5), cfg["accent2"], 8)
        title_box, cover_box = (60, 115, 780, 695), (82, 1110, 410, 1580)
    elif kind == "street":
        draw.rectangle((0, 0, W, H), fill="#eee9dd")
        _paste_crop(canvas, hero, (40, 50, 760, 850), cfg.get("hero_focal", (0.5, 0.5)), "#111111", 12)
        _paste_crop(canvas, c1, (785, 50, 1202, 555), (0.5, 0.5), "#111111", 10)
        _paste_crop(canvas, c2, (785, 580, 1202, 1050), (0.5, 0.5), cfg["accent2"], 10)
        for x in range(55, 1220, 145):
            draw.line((x, 1065, x-90, H), fill=rgba(cfg["ink"], 45), width=5)
        title_box, cover_box = (55, 760, 780, 1365), (830, 1080, 1165, 1575)
    elif kind == "memory":
        _paste_crop(canvas, hero, (0, 0, 760, H), cfg.get("hero_focal", (0.5, 0.5)))
        _paste_crop(canvas, c1, (700, 0, W, 715), (0.5, 0.5), cfg["accent2"], 12)
        _paste_crop(canvas, c2, (700, 735, W, 1215), (0.5, 0.5), cfg["paper"], 12)
        draw.rectangle((36, 36, 106, 1180), fill=rgba(cfg["accent2"], 210))
        draw.text((70, 120), "TYPE / MEMORY / TIME", font=font(22), fill=cfg["ink"], anchor="mm")
        title_box, cover_box = (100, 180, 715, 815), (785, 1140, 1155, 1580)
    elif kind == "map":
        _paste_crop(canvas, hero, (0, 0, W, H), cfg.get("hero_focal", (0.5, 0.5)))
        _paste_crop(canvas, c1, (60, 70, 535, 630), (0.5, 0.5), cfg["accent2"], 10)
        _paste_crop(canvas, c2, (730, 65, 1180, 590), (0.5, 0.5), cfg["paper"], 10)
        title_box, cover_box = (155, 555, 945, 1125), (785, 1115, 1165, 1585)
    elif kind == "pattern":
        draw.rectangle((0, 0, W, H), fill=cfg["paper"])
        _paste_crop(canvas, hero, (45, 45, 790, 720), cfg.get("hero_focal", (0.5, 0.5)), cfg["ink"], 12)
        _paste_crop(canvas, c1, (820, 45, 1195, 515), (0.5, 0.5), cfg["accent"], 12)
        _paste_crop(canvas, c2, (820, 545, 1195, 970), (0.5, 0.5), cfg["ink"], 12)
        for i, (x, y) in enumerate([(80, 820), (275, 900), (470, 820), (665, 900)]):
            draw.rounded_rectangle((x, y, x+145, y+110), 12, fill=cfg["accent"] if i % 2 == 0 else cfg["accent2"])
            draw.text((x+72, y+55), f"{i+1:02d}", font=font(30), fill=cfg["paper"], anchor="mm")
        title_box, cover_box = (55, 1000, 800, 1555), (830, 1035, 1165, 1575)
    else:  # grammar
        draw.rectangle((0, 0, W, H), fill="#0b1014")
        _paste_crop(canvas, hero, (0, 0, 780, 980), cfg.get("hero_focal", (0.5, 0.5)))
        _paste_crop(canvas, c1, (800, 0, W, 610), (0.5, 0.5), cfg["paper"], 10)
        _paste_crop(canvas, c2, (800, 630, W, 1050), (0.5, 0.5), cfg["accent2"], 10)
        title_box, cover_box = (55, 185, 720, 800), (805, 1120, 1165, 1580)

    _draw_cover_title(canvas, cfg, title_box, light=kind in {"street", "pattern"})
    _mounted_cover(canvas, cfg, cover_box)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((52, 1578, 610, 1630), fill=cfg["accent2"])
    draw.text((74, 1604), cfg["cover_en"], font=font(25), fill=cfg["ink"], anchor="lm")
    # Reader-facing image names only; keep the mounted book cover unobstructed.
    if kind in {"movement", "place"}:
        label_x1, label_x2 = 455, 1185
    else:
        label_x1, label_x2 = 40, 775
    _small_label(draw, cfg["hero_name"], (label_x1, 1392, label_x2, 1436))
    _small_label(draw, profile["c1"], (label_x1, 1442, label_x2, 1486))
    _small_label(draw, profile["c2"], (label_x1, 1492, label_x2, 1536))
    page_mark(draw, 1, light=kind not in {"street", "pattern"})
    return save(canvas, folder, 1)


def _content_header(draw, cfg, number, label, dark=True):
    fill = rgba("#0b0b0b", 226) if dark else rgba("#f4efe3", 235)
    color = cfg["paper"] if dark else cfg["ink"]
    draw.rectangle((48, 48, 1194, 126), fill=fill)
    draw.text((72, 86), f"0{number}  {label}", font=font(25), fill=cfg["accent2"], anchor="lm")
    draw.text((1168, 86), cfg["cover_en"], font=font(20), fill=color, anchor="rm")


def _content_text(draw, cfg, slide, box, dark=True, accent_rule=True):
    x1, y1, x2, y2 = box
    panel = (10, 10, 10, 232) if dark else (245, 240, 228, 240)
    ink = cfg["paper"] if dark else cfg["ink"]
    draw.rounded_rectangle(box, 13, fill=panel)
    if accent_rule:
        draw.rectangle((x1 + 30, y1 + 30, x1 + 210, y1 + 40), fill=cfg["accent2"])
    headline_f = font(48, serif=True)
    headline = wrap(draw, slide["headline"], headline_f, x2 - x1 - 62)
    draw.multiline_text((x1 + 30, y1 + 62), headline, font=headline_f, fill=ink, spacing=10)
    hb = draw.multiline_textbbox((x1 + 30, y1 + 62), headline, font=headline_f, spacing=10)[3]
    body = wrap(draw, slide["body"], font(27), x2 - x1 - 62)
    draw.multiline_text((x1 + 30, hb + 28), body, font=font(27), fill=rgba(cfg["paper"] if dark else cfg["ink"], 215), spacing=9)


def photo_card(cfg, folder, number, slide):
    profile = _profile(cfg)
    kind = profile["kind"]
    main = _load_photo(cfg, slide["file"], mono=kind == "memory")
    second = _load_photo(cfg, "02b", mono=kind == "memory") if number == 2 else None
    canvas = Image.new("RGBA", (W, H), rgba(cfg["ink"]))
    draw = ImageDraw.Draw(canvas)

    if kind == "senses":
        _paste_crop(canvas, main, (0, 0, 850, 1120), slide.get("focal", (0.5, 0.5)))
        draw.rectangle((850, 0, W, H), fill="#15110e")
        if second:
            _paste_crop(canvas, second, (780, 150, W, 900), (0.5, 0.5), cfg["accent2"], 9)
            _small_label(draw, profile["02b"], (785, 905, 1205, 965))
        _content_header(draw, cfg, number, slide["name"])
        _content_text(draw, cfg, slide, (55, 1050, 1120, 1535), True)
    elif kind == "movement":
        draw.rectangle((0, 0, W, H), fill="#17191a")
        _paste_circle(canvas, main, (70, 140, 840, 910), slide.get("focal", (0.5, 0.5)), cfg["accent2"], 14)
        if second:
            _paste_crop(canvas, second, (790, 285, 1200, 820), (0.5, 0.5), cfg["paper"], 9)
            _small_label(draw, profile["02b"], (790, 820, 1200, 880))
        _content_header(draw, cfg, number, slide["name"])
        _content_text(draw, cfg, slide, (105, 965, 1160, 1515), True)
    elif kind == "place":
        draw.rectangle((0, 0, W, H), fill=cfg["paper"])
        _paste_crop(canvas, main, (0, 0, W, 870), slide.get("focal", (0.5, 0.5)))
        if second:
            _paste_crop(canvas, second, (85, 690, 1155, 1060), (0.5, 0.5), cfg["paper"], 10)
            _small_label(draw, profile["02b"], (100, 1000, 630, 1060))
        _content_header(draw, cfg, number, slide["name"], False)
        _content_text(draw, cfg, slide, (58, 1045, 1184, 1538), False)
    elif kind == "street":
        draw.rectangle((0, 0, W, H), fill="#ede8db")
        if second:
            _paste_crop(canvas, main, (45, 150, 720, 940), slide.get("focal", (0.5, 0.5)), "#111", 12)
            _paste_crop(canvas, second, (750, 150, 1195, 940), (0.5, 0.5), cfg["accent2"], 12)
            _small_label(draw, profile["02b"], (750, 880, 1195, 940))
        else:
            _paste_crop(canvas, main, (45, 150, 1195, 960), slide.get("focal", (0.5, 0.5)), "#111", 12)
        for x in range(65, 1200, 150):
            draw.line((x, 950, x-70, 1640), fill=rgba(cfg["ink"], 35), width=4)
        _content_header(draw, cfg, number, slide["name"], False)
        _content_text(draw, cfg, slide, (58, 1010, 1184, 1535), False)
    elif kind == "memory":
        draw.rectangle((0, 0, W, H), fill="#101010")
        _paste_crop(canvas, main, (90, 145, 850, 1030), slide.get("focal", (0.5, 0.5)), cfg["paper"], 10)
        if second:
            _paste_crop(canvas, second, (785, 330, 1195, 890), (0.5, 0.5), cfg["accent2"], 11)
            _small_label(draw, profile["02b"], (785, 890, 1195, 950))
        draw.text((1050, 175), f"TYPE\n0{number-1}", font=font(58, serif=True), fill=cfg["accent2"], anchor="ma", spacing=5)
        draw.line((45, 1060, 1195, 1060), fill=cfg["accent2"], width=10)
        _content_header(draw, cfg, number, slide["name"])
        _content_text(draw, cfg, slide, (90, 1085, 1155, 1535), True)
    elif kind == "map":
        _paste_crop(canvas, main, (0, 0, W, 1080), slide.get("focal", (0.5, 0.5)))
        if second:
            _paste_crop(canvas, second, (730, 160, 1190, 670), (0.5, 0.5), cfg["paper"], 9)
            _small_label(draw, profile["02b"], (730, 670, 1190, 730))
        _content_header(draw, cfg, number, slide["name"])
        _content_text(draw, cfg, slide, (55, 1030, 1185, 1535), True)
    elif kind == "pattern":
        draw.rectangle((0, 0, W, H), fill=cfg["paper"])
        if second:
            _paste_crop(canvas, main, (55, 150, 745, 920), slide.get("focal", (0.5, 0.5)), cfg["ink"], 10)
            _paste_crop(canvas, second, (775, 150, 1185, 920), (0.5, 0.5), cfg["accent"], 10)
            _small_label(draw, profile["02b"], (775, 860, 1185, 920))
        else:
            _paste_crop(canvas, main, (55, 150, 1185, 925), slide.get("focal", (0.5, 0.5)), cfg["ink"], 10)
        for i, x in enumerate([70, 260, 450, 640, 830, 1020]):
            draw.rounded_rectangle((x, 955, x+120, 1045), 10, fill=cfg["accent"] if i % 2 == 0 else cfg["accent2"])
            draw.text((x+60, 1000), f"{number-1}.{i+1}", font=font(22), fill=cfg["paper"], anchor="mm")
        _content_header(draw, cfg, number, slide["name"], False)
        _content_text(draw, cfg, slide, (55, 1080, 1185, 1545), False)
    else:  # grammar
        draw.rectangle((0, 0, W, H), fill="#0b1014")
        _paste_crop(canvas, main, (0, 0, 845, 1020), slide.get("focal", (0.5, 0.5)))
        if second:
            _paste_crop(canvas, second, (790, 150, 1205, 870), (0.5, 0.5), cfg["paper"], 10)
            _small_label(draw, profile["02b"], (790, 810, 1205, 870))
        _content_header(draw, cfg, number, slide["name"])
        _content_text(draw, cfg, slide, (55, 1040, 1185, 1535), True)

    draw = ImageDraw.Draw(canvas)
    page_mark(draw, number, light=kind not in {"place", "street", "pattern"})
    return save(canvas, folder, number)


def _draw_logic_band(draw, cfg, box, dark):
    """Book-specific reading key, kept entirely off the documentary photos."""
    logic = _logic(cfg)
    kind = _profile(cfg)["kind"]
    x1, y1, x2, y2 = box
    text_color = cfg["paper"] if dark else cfg["ink"]
    draw.text((x1, y1), logic["operator"], font=font(23), fill=cfg["accent2"])
    label_y = y1 + 43
    count = len(logic["chain"])
    gap = 12
    cell_w = (x2 - x1 - gap * (count - 1)) // count
    for index, label in enumerate(logic["chain"]):
        left = x1 + index * (cell_w + gap)
        if kind in {"street", "pattern"}:
            fill = cfg["accent"] if index % 2 == 0 else cfg["accent2"]
        elif kind == "memory":
            fill = cfg["accent2"] if index == 0 else rgba(cfg["paper"], 26)
        else:
            fill = cfg["accent"] if index == 0 else rgba(cfg["accent2"], 185 - index * 18)
        draw.rounded_rectangle((left, label_y, left + cell_w, label_y + 48), 7, fill=fill,
                               outline=rgba(text_color, 70), width=1)
        draw.text((left + cell_w / 2, label_y + 24), label, font=font(21), fill=text_color, anchor="mm")


def summary_card(cfg, folder):
    profile = _profile(cfg)
    kind = profile["kind"]
    main = _load_photo(cfg, "summary", mono=kind == "memory")
    second = _load_photo(cfg, "06b", mono=kind == "memory")
    canvas = Image.new("RGBA", (W, H), rgba(cfg["ink"]))
    draw = ImageDraw.Draw(canvas)
    # The final card is deliberately a synthesis page: two contextual images,
    # one conclusion and three actionable takeaways—never another case slide.
    if kind in {"street", "pattern", "place"}:
        draw.rectangle((0, 0, W, H), fill=cfg["paper"])
        dark = False
    else:
        draw.rectangle((0, 0, W, H), fill="#101010")
        dark = True
    _paste_crop(canvas, main, (0, 0, 805, 735), cfg.get("summary_focal", (0.5, 0.5)))
    _paste_crop(canvas, second, (825, 0, W, 735), (0.5, 0.5), cfg["accent2"], 10)
    draw = ImageDraw.Draw(canvas)
    _small_label(draw, cfg["summary_name"], (35, 650, 790, 710))
    _small_label(draw, profile["06b"], (825, 650, 1208, 710))
    panel_fill = (8, 8, 8, 238) if dark else (245, 240, 228, 246)
    draw.rounded_rectangle((52, 765, 1190, 1550), 16, fill=panel_fill)
    text_color = cfg["paper"] if dark else cfg["ink"]
    draw.rectangle((82, 805, 302, 864), fill=cfg["accent2"])
    draw.text((192, 834), "本书总结", font=font(27), fill=cfg["ink"], anchor="mm")
    draw.text((330, 833), f"{cfg['author']} ×《{cfg['book']}》", font=font(27), fill=text_color, anchor="lm")
    statement = wrap(draw, cfg["summary"].replace("\n", ""), font(56, serif=True), 1020)
    draw.multiline_text((82, 915), statement, font=font(56, serif=True), fill=text_color, spacing=14)
    sb = draw.multiline_textbbox((82, 915), statement, font=font(56, serif=True), spacing=14)[3]
    band_y = max(1105, sb + 34)
    draw.line((82, band_y, 1155, band_y), fill=cfg["accent2"], width=8)
    _draw_logic_band(draw, cfg, (84, band_y + 25, 1155, band_y + 122), dark)
    y = band_y + 143
    for i, item in enumerate(cfg["takeaways"], 1):
        draw.rounded_rectangle((84, y, 132, y+48), 8, fill=cfg["accent"])
        draw.text((108, y+24), str(i), font=font(24), fill=cfg["paper"], anchor="mm")
        text = wrap(draw, item, font(25), 950)
        draw.multiline_text((155, y+4), text, font=font(25), fill=rgba(cfg["paper"] if dark else cfg["ink"], 225), spacing=6)
        y = draw.multiline_textbbox((155, y+4), text, font=font(25), spacing=6)[3] + 21
    page_mark(draw, 6, light=dark)
    return save(canvas, folder, 6)


def source_file(cfg, folder):
    manifest = json.loads((SOURCE_ASSETS / "manifest.json").read_text(encoding="utf-8"))
    order = ["hero", "c1", "c2", "02", "02b", "03", "04", "05", "summary", "06b"]
    labels = {"hero": "01主图", "c1": "01拼贴图A", "c2": "01拼贴图B", "02": "02主图", "02b": "02补充图", "03": "03", "04": "04", "05": "05", "summary": "06总结主图", "06b": "06总结补充图"}
    records = [item for item in manifest if item["set"] == cfg["asset_set"]]
    records.sort(key=lambda item: order.index(item["slot"]))
    lines = ["# 图片来源（内部记录，不用于发布文案）", ""]
    for item in records:
        lines.append(f"- {labels[item['slot']]}：{item['commons_title']}；摄影/作者：{item['artist'] or '见原页面'}；许可：{item['license']}；{item['source_page']}")
    (folder / "图片来源.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for cfg in BOOKS:
        cfg.update(PHOTO_EDITORIAL[cfg["slug"]])
        folder=OUT_ROOT/cfg["slug"]
        folder.mkdir(parents=True,exist_ok=True)
        paths=[cover_card(cfg,folder)]
        for number,slide in enumerate(cfg["slides"],start=2):
            if slide["type"]=="photo": paths.append(photo_card(cfg,folder,number,slide))
            else: paths.append(diagram_card(cfg,folder,number,slide))
        paths.append(summary_card(cfg,folder))
        make_preview(paths,folder,cfg["preview"])
        copy_file(cfg,folder)
        source_file(cfg,folder)
        print(f"{cfg['slug']}: {len(paths)} cards")


if __name__=="__main__":
    main()
