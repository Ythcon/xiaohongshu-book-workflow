from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
OUT_ROOT = ROOT / "output" / "八本书成品"
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


def wrap(draw, text, used_font, max_width):
    lines, current = [], ""
    for paragraph in text.split("\n"):
        for ch in paragraph:
            trial = current + ch
            if current and draw.textbbox((0, 0), trial, font=used_font)[2] > max_width:
                lines.append(current)
                current = ch
            else:
                current = trial
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


def page_mark(draw, number):
    draw.text((1158, 1591), f"0{number} / 05", font=font(23), fill=rgba("#f8f3e8", 175), anchor="ra")


def save(canvas, folder, number):
    path = folder / f"{number:02d}.jpg"
    canvas.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    return path


def cover_card(cfg, folder):
    paper, ink, accent = cfg["paper"], cfg["ink"], cfg["accent"]
    canvas = Image.new("RGBA", (W, H), rgba(paper))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=accent)

    draw.text((72, 80), cfg["author"], font=font(56, serif=True), fill=ink)
    title_font = font(cfg.get("title_size", 64), serif=True)
    title = wrap(draw, f"×《{cfg['book']}》", title_font, 1080)
    draw.multiline_text((68, 162), title, font=title_font, fill=accent, spacing=12)
    title_bottom = draw.multiline_textbbox((68, 162), title, font=title_font, spacing=12)[3]
    draw.rectangle((70, title_bottom + 34, 710, title_bottom + 46), fill=accent)

    cover = Image.open(ROOT / cfg["asset_dir"] / cfg["cover"]).convert("RGB")
    cover = fit_inside(cover, (720, 820))
    x = (W - cover.width) // 2
    y = max(475, title_bottom + 100)
    shadow = Image.new("RGBA", (cover.width + 70, cover.height + 70), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((25, 25, cover.width + 45, cover.height + 45), 8, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(shadow, (x - 25, y - 17))
    mount = Image.new("RGBA", (cover.width + 16, cover.height + 16), rgba("#ffffff"))
    mount.alpha_composite(cover.convert("RGBA"), (8, 8))
    canvas.alpha_composite(mount, (x - 8, y - 8))

    draw = ImageDraw.Draw(canvas)
    tagline_font = font(34, serif=True)
    tagline = wrap(draw, cfg["tagline"], tagline_font, 1020)
    draw.multiline_text((72, 1450), tagline, font=tagline_font, fill=ink, spacing=13)
    page_mark(draw, 1)
    return save(canvas, folder, 1)


def case_card(cfg, folder, number, case):
    accent = cfg["accent"]
    photo = Image.open(ROOT / cfg["asset_dir"] / case["file"]).convert("RGB")
    photo = ImageEnhance.Contrast(photo).enhance(1.04)
    photo = ImageEnhance.Color(photo).enhance(0.98)
    photo = crop_fill(photo, (W, 1030), case.get("focal", (0.5, 0.5)))

    canvas = Image.new("RGBA", (W, H), rgba("#101010"))
    canvas.alpha_composite(photo.convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 150), (0, 0, 0, 108)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 24, H), fill=accent)
    label_font = font(25)
    label = wrap(draw, case["name"], label_font, 980)
    box_width = min(1080, draw.multiline_textbbox((0, 0), label, font=label_font, spacing=6)[2] + 54)
    draw.rounded_rectangle((64, 56, 64 + box_width, 122), 5, fill=rgba("#101010", 220))
    draw.multiline_text((88, 72), label, font=label_font, fill=accent, spacing=6)

    draw.rectangle((0, 1030, W, H), fill="#101010")
    draw.rectangle((68, 1080, 230, 1093), fill=accent)
    headline_font = font(56, serif=True)
    headline = wrap(draw, case["headline"], headline_font, 1080)
    draw.multiline_text((68, 1134), headline, font=headline_font, fill="#fffaf0", spacing=12)
    bottom = draw.multiline_textbbox((68, 1134), headline, font=headline_font, spacing=12)[3]
    body_font = font(29)
    body = wrap(draw, case["body"], body_font, 1070)
    draw.multiline_text((70, bottom + 40), body, font=body_font, fill=rgba("#fffaf0", 205), spacing=12)
    page_mark(draw, number)
    return save(canvas, folder, number)


def preview(paths, folder, background):
    tw, th, gap = 280, 374, 18
    sheet = Image.new("RGB", (tw * 3 + gap * 4, th * 2 + gap * 3), background)
    positions = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)]
    for path, (col, row) in zip(paths, positions):
        image = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(image, (gap + col * (tw + gap), gap + row * (th + gap)))
    sheet.save(folder / "preview.jpg", quality=94, optimize=True)


def copy_file(cfg, folder):
    tags = " ".join(cfg["tags"])
    content = (
        f"{cfg['author']} ×《{cfg['book']}》\n\n"
        f"{cfg['copy']}\n\n"
        f"{tags}\n"
    )
    (folder / "发布文案.md").write_text(content, encoding="utf-8")


BOOKS = [
    {
        "slug": "01-隈研吾-反造型", "asset_dir": "assets/kengo-kuma", "cover": "book-cover-2018.jpg",
        "author": "隈研吾", "book": "反造型：与自然连接的建筑", "tagline": "建筑不是一个孤立的物体，而是材料、身体与环境之间的关系。",
        "paper": "#eeeae1", "ink": "#2b2723", "accent": "#a55b42", "preview": "#d8c9ba",
        "cases": [
            {"file": "asakusa.jpg", "name": "浅草文化观光中心", "focal": (0.50, 0.48), "headline": "高楼，也可以像一排小房子叠起来", "body": "倾斜屋顶把垂直体量拆成多个熟悉尺度，让建筑在东京密集街区里保持街道感。"},
            {"file": "gc-prostho.jpg", "name": "GC Prostho Museum Research Center", "focal": (0.50, 0.50), "headline": "结构不必藏起来，它可以成为空间的纹理", "body": "传统木构的千鸟格被放大成三维网格；承重、分隔与光影因此成为同一套秩序。"},
            {"file": "stone-plaza.jpg", "name": "石之美术馆", "focal": (0.52, 0.50), "headline": "沉重的石头，也能被处理得很轻", "body": "旧石材被重新组织成墙、缝隙与通透界面，材料的重量被光和水慢慢化开。"},
            {"file": "va-dundee.jpg", "name": "V&A Dundee", "focal": (0.52, 0.52), "headline": "建筑可以不像物体，更像一段地形", "body": "层叠的水平构件把海岸岩壁转译成建筑，让博物馆与水岸、风和城市轮廓发生联系。"},
        ],
        "copy": "隈研吾在《反造型》中反对把建筑理解为孤立、完整、等待被观看的物体。\n\n他更关心建筑如何与土地、材料、气候和人的身体连接。浅草文化观光中心把高楼拆成一层层小屋，GC Prostho 用木格把结构变成空间纹理，石之美术馆让厚重石材获得呼吸感，V&A Dundee 则把建筑处理成海岸地形。\n\n所谓“反造型”，并不是拒绝形式，而是不让形式成为设计的终点。建筑真正成立的时刻，是它开始回应周围的一切。",
        "tags": ["#隈研吾", "#反造型", "#建筑设计", "#建筑材料", "#日本建筑", "#建筑案例", "#建筑理论", "#建筑书单", "#设计师必读"],
    },
    {
        "slug": "02-彼得卒姆托-建筑氛围", "asset_dir": "assets/peter-zumthor", "cover": "book-cover-cn-v2.jpg",
        "author": "彼得·卒姆托", "book": "建筑氛围", "tagline": "好的空间，不是先被解释，而是先被身体感受到。",
        "paper": "#ddd2c5", "ink": "#332820", "accent": "#8a5b3e", "preview": "#cfc0b0",
        "cases": [
            {"file": "therme-vals.jpg", "name": "瓦尔斯温泉浴场", "focal": (0.50, 0.54), "headline": "先感到温度，才慢慢看见建筑", "body": "石材、热水、阴影与回声共同塑造空间；建筑的边界因此不只由墙决定，也由身体感受决定。"},
            {"file": "bruder-klaus.jpg", "name": "布鲁德·克劳斯田野教堂", "focal": (0.50, 0.50), "headline": "一束光，足以让粗糙空间获得精神性", "body": "烧灼木模留下焦黑内壁，顶部开口引入天气与光线，材料的痕迹成为沉静体验的一部分。"},
            {"file": "kolumba.jpg", "name": "科隆柯伦巴博物馆", "focal": (0.50, 0.50), "headline": "新建筑没有覆盖遗址，而是让时间继续累积", "body": "灰砖、旧墙与考古遗迹被放进同一空间秩序，不同年代彼此保持距离，也彼此照亮。"},
            {"file": "saint-benedict.jpg", "name": "圣本笃教堂", "focal": (0.50, 0.49), "headline": "材料越克制，空间越能集中人的注意力", "body": "木构外壳、柔和天光与安静比例共同制造包裹感，礼拜空间因此接近一件被身体进入的器物。"},
        ],
        "copy": "《建筑氛围》讨论的不是一种风格，而是空间如何在几秒钟内影响人的情绪。\n\n在瓦尔斯温泉，石材、热水和回声共同建立身体经验；布鲁德·克劳斯教堂用焦黑内壁与顶部天光制造精神性；柯伦巴博物馆让新砖与遗址共存；圣本笃教堂则用木材和柔光形成安静的包裹感。\n\n卒姆托提醒我们：建筑不仅被眼睛观看，还会被皮肤、脚步、听觉和记忆共同感知。真正持久的空间，往往不是信息最多，而是感受最完整。",
        "tags": ["#彼得卒姆托", "#建筑氛围", "#空间体验", "#建筑材料", "#光影设计", "#建筑案例", "#建筑理论", "#建筑书单", "#设计师必读"],
    },
    {
        "slug": "03-卡洛斯卡帕-全集", "asset_dir": "assets/carlo-scarpa", "cover": "book-cover-v5.jpg",
        "author": "卡洛·斯卡帕", "book": "卡洛·斯卡帕全集", "tagline": "细部不是装饰，而是时间、材料与身体相遇的位置。",
        "paper": "#e9dfc5", "ink": "#302820", "accent": "#b94e3f", "preview": "#d8c9ad",
        "cases": [
            {"file": "brion.jpg", "name": "布里昂家族墓园", "focal": (0.50, 0.48), "headline": "纪念性，不一定来自宏大", "body": "水、混凝土、几何开口与缓慢路径共同组织情绪，让告别发生在连续的空间体验里。"},
            {"file": "castelvecchio.jpg", "name": "维罗纳城堡博物馆", "focal": (0.50, 0.50), "headline": "新与旧之间，最重要的是留下距离", "body": "楼梯、栏杆和展台不假装属于古城堡；精确接缝让两个时代既彼此独立，又持续对话。"},
            {"file": "olivetti.jpg", "name": "奥利维蒂展厅", "focal": (0.50, 0.50), "headline": "很小的空间，也能拥有完整的建筑节奏", "body": "石材台阶、悬浮展台和水面把商业空间变成连续场景，每次转身都出现新的尺度关系。"},
            {"file": "querini.jpg", "name": "奎里尼·斯坦帕利亚基金会", "focal": (0.50, 0.53), "headline": "与其阻挡威尼斯的水，不如设计它进入的方式", "body": "斯卡帕把潮水纳入入口与庭院，让城市环境不再是建筑的敌人，而成为空间的一部分。"},
        ],
        "copy": "看斯卡帕的建筑，很难只看整体。真正让空间成立的，是接缝、转角、台阶、水面和材料交界处。\n\n布里昂墓园用路径与水组织告别；维罗纳城堡让新构件与旧墙保持清晰距离；奥利维蒂展厅在极小尺度里建立完整节奏；奎里尼基金会则把威尼斯潮水主动纳入建筑。\n\n斯卡帕的细部从来不是装饰性的炫技。它们让不同材料、不同年代和人的身体找到彼此相遇的方式。",
        "tags": ["#卡洛斯卡帕", "#建筑细部", "#建筑材料", "#建筑改造", "#意大利建筑", "#建筑案例", "#建筑书单", "#空间设计", "#设计师必读"],
    },
    {
        "slug": "04-雷姆库哈斯-癫狂的纽约", "asset_dir": "assets/rem-koolhaas", "cover": "book-cover-cn.jpg",
        "author": "雷姆·库哈斯", "book": "癫狂的纽约", "tagline": "城市的矛盾不是故障，它本身就是建筑产生的动力。",
        "paper": "#ecebed", "ink": "#171717", "accent": "#fff000", "preview": "#d2d2d2",
        "cases": [
            {"file": "cctv.jpg", "name": "中央电视台总部大楼", "focal": (0.50, 0.48), "headline": "摩天楼不必是一根塔，也可以是一条回路", "body": "办公、制作与传播被组织成连续环形，建筑用结构直接表达复杂机构之间的相互依赖。"},
            {"file": "seattle-library.jpg", "name": "西雅图中央图书馆", "focal": (0.50, 0.50), "headline": "先承认功能冲突，再让它们找到自己的位置", "body": "稳定功能被堆叠成平台，公共空间填入其间；外部形态由内部程序的碰撞直接生成。"},
            {"file": "casa-da-musica.jpg", "name": "波尔图音乐之家", "focal": (0.50, 0.50), "headline": "一块陌生体量，也能重新组织整座广场", "body": "多面体把演出空间、城市视线与公共地面重新连接，建筑的力量来自与周围关系的改变。"},
            {"file": "de-rotterdam.jpg", "name": "De Rotterdam", "focal": (0.50, 0.50), "headline": "把一座城市，压缩进一栋建筑", "body": "办公、住宅、酒店与公共设施在垂直方向叠加，不同程序共享交通与城市景观。"},
        ],
        "copy": "《癫狂的纽约》不是一本安静讨论形式的书。库哈斯把曼哈顿视为一台由密度、欲望、技术和冲突共同驱动的机器。\n\n这种城市观也延续到他的作品里：央视总部把塔楼变成回路，西雅图图书馆让不同程序公开碰撞，波尔图音乐之家用陌生体量改变广场，De Rotterdam 则把多种城市功能压缩进同一栋建筑。\n\n库哈斯最重要的提醒或许是：面对真实城市，建筑不必消除矛盾。设计也可以从矛盾中获得结构。",
        "tags": ["#雷姆库哈斯", "#癫狂的纽约", "#城市研究", "#OMA", "#建筑设计", "#公共建筑", "#建筑理论", "#建筑书单", "#设计师必读"],
    },
    {
        "slug": "05-伯纳德屈米-红不是一种颜色", "asset_dir": "assets/tschumi", "cover": "book-cover-cn.jpg",
        "author": "伯纳德·屈米", "book": "红不是一种颜色", "tagline": "建筑不是静止物体，而是空间、事件与行动同时发生。",
        "paper": "#eee7e5", "ink": "#231919", "accent": "#d10b2f", "preview": "#d4c4c5",
        "cases": [
            {"file": "01-villette-r4.jpg", "name": "拉维莱特公园：红色构筑物", "focal": (0.50, 0.50), "headline": "红色不是装饰，而是组织城市的坐标", "body": "重复出现的构筑物把巨大公园切成可识别的点，人们的活动在坐标之间自由发生。"},
            {"file": "02-villette-n8.jpg", "name": "拉维莱特公园：路径与事件", "focal": (0.50, 0.50), "headline": "公园不是一幅风景，而是一台事件机器", "body": "点、线、面彼此叠加，路线不再只负责通行，也不断制造相遇、停留与意外。"},
            {"file": "03-le-fresnoy.jpg", "name": "Le Fresnoy 艺术中心", "focal": (0.50, 0.50), "headline": "保留旧建筑，再给它覆盖一片新的天空", "body": "巨大屋顶跨越原有建筑，在新旧之间制造灰空间，让展览、教学与公共活动自由混合。"},
            {"file": "04-acropolis-museum.jpg", "name": "雅典卫城博物馆", "focal": (0.50, 0.50), "headline": "建筑的方向，由遗址和观看共同决定", "body": "底层避让考古遗迹，顶层转向帕特农神庙；不同方向回应不同的城市与历史条件。"},
        ],
        "copy": "伯纳德·屈米认为，建筑不能只用形式来理解。空间里发生的动作、冲突与事件，同样是设计的一部分。\n\n拉维莱特公园用红色构筑物建立坐标，再让路径和活动自由叠加；Le Fresnoy 用一片巨大屋顶覆盖旧建筑，创造介于室内外之间的事件空间；雅典卫城博物馆则同时回应脚下遗址与远处神庙。\n\n“红不是一种颜色”背后，是一种更主动的建筑观：形式不是终点，它需要为行动提供可能。",
        "tags": ["#伯纳德屈米", "#红不是一种颜色", "#建筑概念", "#拉维莱特公园", "#建筑事件", "#建筑案例", "#建筑理论", "#建筑书单", "#设计师必读"],
    },
    {
        "slug": "06-柯林罗-透明性", "asset_dir": "assets/colin-rowe-transparency", "cover": "book-cover-cn.jpg",
        "author": "柯林·罗", "book": "透明性", "tagline": "真正复杂的透明，不一定来自玻璃，而来自空间可以被多种方式阅读。",
        "paper": "#e5e1e5", "ink": "#28232a", "accent": "#9d526c", "preview": "#ccc4cc",
        "cases": [
            {"file": "bauhaus-dessau.jpg", "name": "包豪斯德绍校舍", "focal": (0.50, 0.50), "headline": "玻璃让空间可见，却不等于空间复杂", "body": "柯林·罗将这种直接看穿的视觉效果称为“物理透明”，它清晰，却未必产生多重解释。"},
            {"file": "villa-stein-model.jpg", "name": "斯坦因住宅", "focal": (0.50, 0.50), "headline": "同一立面，可以同时读出几套空间秩序", "body": "平面、网格与体量彼此错位，让前后关系无法一次被看完，这正是“现象透明”的关键。"},
            {"file": "delaunay-windows.jpg", "name": "罗伯特·德劳内《窗》系列", "focal": (0.50, 0.50), "headline": "重叠不只是遮挡，也能制造同时性", "body": "色块和边界彼此穿插，观看者会在前景与背景之间反复切换，画面因此保持多义。"},
            {"file": "juan-gris-still-life.jpg", "name": "胡安·格里斯静物画", "focal": (0.50, 0.50), "headline": "看似平面的画面，也能容纳多个空间层次", "body": "物体被拆解、重组并叠置，空间不再只有一个正确读法，而成为持续变化的理解过程。"},
        ],
        "copy": "《透明性》最有价值的地方，是区分了两种完全不同的“透明”。\n\n一种是物理透明：像玻璃幕墙一样，可以直接看穿。另一种是现象透明：即使材料不透明，空间仍能被同时读出多套层次和秩序。\n\n从包豪斯校舍、斯坦因住宅到德劳内与胡安·格里斯的绘画，柯林·罗关心的始终不是材料本身，而是观看如何在不同解释之间移动。\n\n透明不只是一种视觉效果，也是一种组织复杂空间的思考工具。",
        "tags": ["#柯林罗", "#透明性", "#建筑理论", "#现象透明", "#空间分析", "#建筑概念", "#现代建筑", "#建筑书单", "#设计师必读"],
    },
    {
        "slug": "07-塞西尔巴尔蒙德-异规", "asset_dir": "assets/cecil-balmond", "cover": "book-cover-cn.png",
        "author": "塞西尔·巴尔蒙德", "book": "异规", "tagline": "秩序不只来自整齐重复，也可以从偏移、断裂和变化中生长。",
        "paper": "#ded9ce", "ink": "#202020", "accent": "#efc900", "preview": "#cbc4b7",
        "cases": [
            {"file": "serpentine-2002.jpg", "name": "蛇形画廊临时展亭 2002", "focal": (0.50, 0.50), "headline": "不规则线条，也能形成稳定结构", "body": "连续折线在墙与屋顶之间流动，结构逻辑不再被隐藏，而直接成为空间体验。"},
            {"file": "cctv.jpg", "name": "中央电视台总部大楼", "focal": (0.50, 0.48), "headline": "最困难的形体，需要一套看得见的受力秩序", "body": "斜向网格根据受力密度发生变化，让环形巨构在结构上闭合，也让力量被建筑表面直接读出。"},
            {"file": "orbit.jpg", "name": "ArcelorMittal Orbit", "focal": (0.50, 0.50), "headline": "结构不必追求安静，它也可以制造运动感", "body": "红色钢构绕塔体不断扭转，稳定核心与无序轨迹并置，形成介于建筑、工程和雕塑之间的作品。"},
            {"file": "pedro-ines.jpg", "name": "Pedro e Inês 人行桥", "focal": (0.50, 0.50), "headline": "一次轻微错位，就能改变整座桥的体验", "body": "桥面在中央偏移并交错，结构回应河岸条件，也把普通通行变成一次空间事件。"},
        ],
        "copy": "《异规》讨论的不是没有规则，而是规则如何在变化中形成。\n\n巴尔蒙德不把结构理解为形式背后的技术服务，而是把它当作设计本身。蛇形画廊展亭用连续折线生成空间，央视总部让受力网格直接出现在表面，Orbit 用扭转钢构制造运动感，Pedro e Inês 人行桥则用一次错位改变通行体验。\n\n好的结构并不一定整齐、对称、容易预测。偏移、断裂与不规则，也可以产生新的秩序。",
        "tags": ["#塞西尔巴尔蒙德", "#异规", "#结构设计", "#建筑结构", "#参数化设计", "#建筑案例", "#建筑理论", "#建筑书单", "#设计师必读"],
    },
    {
        "slug": "08-史蒂文霍尔-锚固", "asset_dir": "assets/steven-holl-anchoring", "cover": "book-cover-cn.jpg",
        "author": "史蒂文·霍尔", "book": "锚固", "tagline": "建筑不是被放到场地上，而是从场地的光、地形与记忆中生长出来。",
        "paper": "#ebe9e3", "ink": "#25282a", "accent": "#ba3f45", "preview": "#d0cdc5",
        "cases": [
            {"file": "chapel-st-ignatius.jpg", "name": "圣伊纳爵教堂", "focal": (0.50, 0.50), "headline": "不同的光，可以塑造不同的精神空间", "body": "多个“光之瓶”从不同方向引入色彩与天光，礼拜空间由光的差异而不是装饰建立秩序。"},
            {"file": "kiasma.png", "name": "赫尔辛基当代艺术博物馆 Kiasma", "focal": (0.50, 0.50), "headline": "建筑的曲线，来自城市中原本存在的方向", "body": "城市轴线、地形与远处景观在建筑内部交汇，空间像一条把不同关系缝合起来的路径。"},
            {"file": "simmons-hall.jpg", "name": "MIT Simmons Hall", "focal": (0.50, 0.50), "headline": "厚重体量，也能通过孔洞与颜色获得呼吸", "body": "密集窗格包裹宿舍体量，大尺度空洞切入内部，让公共生活与城市光线进入建筑。"},
            {"file": "linked-hybrid.jpg", "name": "北京当代 MOMA", "focal": (0.50, 0.50), "headline": "公共空间不只在地面，也可以被抬到空中", "body": "连桥把多个塔楼组成开放网络，交通、商业与文化活动在高处形成新的城市层次。"},
        ],
        "copy": "史蒂文·霍尔所说的“锚固”，不是把建筑固定在某块土地上，而是让设计从场地的光、地形、历史和城市关系中获得理由。\n\n圣伊纳爵教堂用不同方向的光塑造精神空间；Kiasma 把城市轴线转化为内部路径；Simmons Hall 用孔洞连接宿舍与公共生活；北京当代 MOMA 则把公共网络抬到空中。\n\n当建筑真正回应场地，它就不再是可以被随意搬走的造型，而成为那个地方独有的一部分。",
        "tags": ["#史蒂文霍尔", "#锚固", "#场地设计", "#光影建筑", "#建筑概念", "#建筑案例", "#建筑理论", "#建筑书单", "#设计师必读"],
    },
]


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for cfg in BOOKS:
        folder = OUT_ROOT / cfg["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        paths = [cover_card(cfg, folder)]
        for index, case in enumerate(cfg["cases"], start=2):
            paths.append(case_card(cfg, folder, index, case))
        preview(paths, folder, cfg["preview"])
        copy_file(cfg, folder)
        print(f"{cfg['slug']}: {len(paths)} cards")


if __name__ == "__main__":
    main()
