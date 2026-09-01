from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

import generate_casabella_135_cards as base
from generate_casabella_101_102_cards import FONT_BOLD, FONT_SANS, H, INK, LIGHT, W, cover_crop, draw_fit, font, mount, rgba


CFG = {
    "slug": "casabella-136",
    "issue": "CASABELLA-COSTRUZIONI 136",
    "date": "APRILE 1939 | ANNO XII",
    "date_cn": "1939年4月",
    "accent": "#d0a12d",
    "dark": "#27333c",
    "paper2": "#f4f0df",
    "question": "教室需要更多日光，但开口越大越要先解决安全、眩光、通风与维护；好的玻璃，让光进入而不把风险带进来。",
    "thesis": "第136期刊载 Diotallevi 与 Marescotti 关于学校钢化玻璃应用的技术文章。它提醒我们：教育空间里的玻璃不只是立面风格，而是决定学生是否看得远、坐得住、开窗安全，以及日常维护是否轻松的一整套构造选择。",
    "summary": "学校中的玻璃不该只追求“通透”。先控制孩子能触及的位置与开启方式；再让日光从侧面或高处稳定进入；把可以开启的扇、遮阳和通风位置分工；最后用耐冲击、易更换的构造面对高频使用。光线越多，细节越需要克制。",
    "concepts": ["采光先于玻璃面积", "开启方式先于造型", "安全玻璃服务高频使用"],
    "takeaways": [
        "开窗尺寸要回应课桌的视线和昼光深度，而不是只追求整面透明。稳定、均匀的光比过强烈直射更适合长时间学习。",
        "让上部采光、侧向视线和可开启通风各自承担任务。孩子能碰到的构件要稳，真正需要开启的部分应在清楚、可管理的位置。",
        "学校的玻璃必须按碰撞、擦洗和替换来设计。把边框、五金与更换路径提前做进构造，明亮才不会变成脆弱。",
    ],
    "publish_title": "CASABELLA136｜教室的光要安全",
    "publish_body": "教室越明亮，就越好吗？Casabella-Costruzioni 136 的回答更克制：光线必须和安全、通风、清洁一起被设计。\n\nDiotallevi 与 Marescotti 在 1939 年讨论学校中的钢化玻璃，关注的不只是材料本身。大开口会带来更深的采光和更远的视线，但也会带来碰撞、眩光、开启管理与日常维护的问题。\n\n所以，学校里的玻璃应当分工：侧窗照顾视线和均匀日光，高处可开启扇排出热空气，遮阳控制直射，孩子能够触及的区域采用耐冲击、易替换的构造。光不再是一片漂亮的立面，而是一套让人能久坐、能呼吸、能安心活动的环境系统。\n\n你学生时代最喜欢哪一种教室采光：靠窗的侧光、天窗，还是能完全打开的玻璃墙？",
    "tags": "#Casabella #学校建筑 #教室采光 #玻璃建筑 #校园设计 #建筑细部 #现代建筑 #空间设计",
    "cards": [
        {"image":"02-suresnes-class.jpg", "focal":(0.50,0.48), "source":"Eugène Beaudouin、Marcel Lods｜Suresnes 露天学校｜Casabella 136", "eyebrow":"观点 01｜教室采光要让每张桌子都得到稳定的光", "title":"窗不必只服务靠墙的一排人；让光线沿教室深度均匀进入，学生才不会一边刺眼、一边昏暗", "body":"Suresnes 的课堂把玻璃面与开放边界带到孩子身旁。好的采光先看桌面上的亮度是否均衡，再谈窗有多大；光线稳定，阅读和书写才能持续。"},
        {"image":"03-suresnes-folding.jpg", "focal":(0.50,0.46), "source":"Eugène Beaudouin、Marcel Lods｜可折叠玻璃教室｜Casabella 136", "eyebrow":"观点 02｜玻璃墙要能在天气变化时切换状态", "title":"需要新鲜空气时打开，需要挡风时关闭；同一面玻璃墙只有具备可控的开启方式，才真正服务教学", "body":"开放并不等于永远敞开。可折叠玻璃让教室在阳光、风和温度变化时调整边界：既保留与花园的联系，也避免孩子被天气完全支配。"},
        {"image":"04-duiker-class.jpg", "focal":(0.51,0.48), "source":"Jan Duiker｜阿姆斯特丹露天学校｜Casabella 136", "eyebrow":"观点 03｜窗边视线应当帮助专注，而不是制造干扰", "title":"大窗可以带来方向感和远景，但课桌与窗的关系必须控制眩光和直射，视线才能成为放松而非分心", "body":"Duiker 的教室用连续开窗把室内与城市光线连起来。真正有效的做法，是让视线从坐姿自然穿出，同时避免低角度阳光直接落在书本和黑板上。"},
        {"image":"05-suresnes-courtyard.webp", "focal":(0.50,0.45), "source":"Eugène Beaudouin、Marcel Lods｜Suresnes 校园庭院｜Casabella 136", "eyebrow":"观点 04｜玻璃把教室延伸到室外，也要给停留留阴影", "title":"当课堂能看见并抵达庭院，外部空间便成为学习的一部分；但树荫、檐下和坐处必须先准备好", "body":"透明边界把学生从封闭房间带向户外。庭院不应只是窗外风景：有遮蔽、有休息点、有可达路径，它才会成为课间活动和露天教学的真正场地。"},
        {"image":"06-bauhaus-facade.jpg", "focal":(0.52,0.48), "source":"Walter Gropius｜Bauhaus Dessau 教学楼｜Casabella 136", "eyebrow":"观点 05｜整面玻璃立面必须先解决热与眩光", "title":"玻璃越连续，阳光和热量越难忽略；遮阳、通风和可清洁的分格要与立面同时设计", "body":"Bauhaus 的玻璃幕墙让工作空间获得明亮与透明，也把构造问题暴露得更清楚。学校使用玻璃，不能只停在视觉轻盈，还要管理夏季热、反射和清洁。"},
        {"image":"07-adgb-reading.jpg", "focal":(0.50,0.46), "source":"Hannes Meyer、Hans Wittwer｜ADGB 阅读室｜Casabella 136", "eyebrow":"观点 06｜读写空间更需要侧向柔光", "title":"长时间阅读不靠更亮的灯，而靠没有强反射的稳定侧光；桌面、窗下和灯具要一起安排", "body":"ADGB 阅读室把长桌放进持续的日光带中。窗边有光，却不把亮点直打在视线前方；人工灯只补足阴天与傍晚，学习空间因而能保持平静。"},
        {"image":"08-crow-island.jpg", "focal":(0.50,0.48), "source":"Perkins、Will、Saarinen｜Crow Island School｜Casabella 136", "eyebrow":"观点 07｜开窗高度要符合孩子的身体尺度", "title":"孩子坐着、站着、活动时看到的世界不同；把窗台、扶手与开扇做在他们可理解的高度，安全才会自然发生", "body":"学校不是缩小版办公楼。窗的下沿、锁具和可触及玻璃都要回应儿童身高与动作范围；让他们能看出去，也不让危险的开启与碰撞发生在顺手的位置。"},
        {"image":"09-30s-school.jpg", "focal":(0.50,0.47), "source":"1930年代学校建筑档案｜钢窗与日光教室｜Casabella 136", "eyebrow":"观点 08｜玻璃细部要为碰撞和替换预留余地", "title":"学校的玻璃不是一次性完成品；边框、分格和五金要考虑擦洗、碰撞和快速更换，才能经得起每天使用", "body":"高频环境最怕“看上去很轻”的细部经不起碰。把受力边、保护高度和维修方式提前纳入设计，透明立面才能在多年后仍然安全、干净、可用。"},
    ],
    "sources": [
        "`book-cover.jpg`｜Casabella-Costruzioni 136 原刊封面，1939年4月｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/136-nz.jpg",
        "`02-suresnes-class.jpg`｜Eugène Beaudouin、Marcel Lods，Suresnes 露天学校课堂，1934—35年｜Monumentum｜https://monumentum.fr/monument-historique/pa00088156/suresnes-ecole-de-plein-air｜许可须在商业发布前复核；裁切与文字排版",
        "`03-suresnes-folding.jpg`｜Suresnes 露天学校可开启玻璃教室｜Espazium｜https://www.espazium.ch/fr/actualites/batir-pour-une-education-en-exterieur｜许可须在商业发布前复核；裁切与文字排版",
        "`04-duiker-class.jpg`｜Jan Duiker，阿姆斯特丹露天学校课堂，1930年｜Architecture History｜https://architecture-history.org/architects/architects/DUIKER/OBJ/1930%2C%20Open-Air%20School%2C%20Amsterdam%2C%20Netherlands%20.html｜许可须在商业发布前复核；裁切与文字排版",
        "`05-suresnes-courtyard.webp`｜Suresnes 露天学校庭院｜Arquitectura Viva｜https://arquitecturaviva.com/articles/escuela-al-aire-libre-suresnes-1935｜许可须在商业发布前复核；裁切与文字排版",
        "`06-bauhaus-facade.jpg`｜Walter Gropius，Bauhaus Dessau 教学楼玻璃立面｜Brewminate｜https://brewminate.com/culture-in-weimar-germany-on-the-edge-of-the-volcano/｜许可须在商业发布前复核；裁切与文字排版",
        "`07-adgb-reading.jpg`｜Walter Peterhans，ADGB 阅读室，约1930年；建筑 Hannes Meyer、Hans Wittwer｜Midgard Licht｜https://midgard.com/pages/typ-113-bauhaus-lamp｜许可须在商业发布前复核；裁切与文字排版",
        "`08-crow-island.jpg`｜Crow Island School 教室，1940年；建筑 Perkins、Will、Eero 与 Eliel Saarinen｜Perkins&Will History｜https://history.perkinswill.com/prologue/｜许可须在商业发布前复核；裁切与文字排版",
        "`09-30s-school.jpg`｜1930年代学校建筑历史照片｜Mary Evans Picture Library｜https://www.prints-online.com/school-architecture-30s-14296386.html｜许可须在商业发布前复核；裁切与文字排版",
        "文章核验｜I. Diotallevi、F. Marescotti《Alcune applicazioni del vetro temperato nelle scuole》，Casabella-Costruzioni 136，1939年4月，第49—52页；Giuseppe Pagano《La funzione rivoluzionaria dell’arte》，同刊｜Fondo Franco Marescotti｜https://www.fondomarescotti.org/p/bibliografia；Antonino Saggio 文献｜https://www.nitrosaggio.net/iquaderni/PDFgratis/AntoninoSaggioGiuseppePagano.pdf",
    ],
}


def make_cover(src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#f4f0df")); draw = ImageDraw.Draw(canvas)
    canvas.alpha_composite(cover_crop(Image.open(src / "04-duiker-class.jpg").convert("RGB"), (W, 760), (0.50, 0.48)).convert("RGBA"), (0, 0))
    canvas.alpha_composite(Image.new("RGBA", (W, 760), (20, 36, 45, 110)), (0, 0))
    draw.text((68, 50), CFG["issue"], font=font(FONT_BOLD, 24), fill=LIGHT)
    draw.text((1170, 52), CFG["date"], font=font(FONT_SANS, 19), fill=rgba(LIGHT, 190), anchor="ra")
    draw.text((68, 140), "单期主线｜学校玻璃与日光", font=font(FONT_BOLD, 22), fill="#f0c950")
    draw_fit(draw, (68, 204), "教室的光\n要安全", 650, 175, 76, LIGHT, serif=True, spacing=16)
    cover = ImageEnhance.Sharpness(Image.open(src / "book-cover.jpg").convert("RGB")).enhance(1.35)
    mount(canvas, cover, (840, 294, 286, 316), True)
    draw.rectangle((0, 760, W, H), fill="#f4f0df")
    draw_fit(draw, (68, 842), CFG["question"], 1060, 168, 43, CFG["dark"], serif=True, spacing=15)
    draw.rectangle((68, 1112, 1174, 1276), fill=CFG["dark"])
    draw_fit(draw, (104, 1140), "钢化玻璃让学校拥有更大的开口，但真正的关键是：它必须同时服务日光、通风、碰撞安全和长期维护。", 970, 102, 31, LIGHT, serif=True, spacing=11)
    draw.text((68, 1360), "日光", font=font(FONT_BOLD, 53), fill=CFG["accent"])
    draw.line((235, 1389, 480, 1389), fill=CFG["dark"], width=4)
    draw.text((514, 1360), "通风", font=font(FONT_BOLD, 53), fill=CFG["accent"])
    draw.line((680, 1389, 920, 1389), fill=CFG["dark"], width=4)
    draw.text((954, 1360), "安全", font=font(FONT_BOLD, 53), fill=CFG["accent"])
    draw.text((68, 1560), "Casabella-Costruzioni｜第136期原刊封面｜1939年4月", font=font(FONT_SANS, 19), fill=rgba(CFG["dark"], 195))
    base.mark(draw, 1)
    return base.save_rgb(canvas, out / "01.jpg")


def make_summary(out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba("#f4f0df")); draw = ImageDraw.Draw(canvas); base.header(draw, 10)
    draw.text((68, 188), "更多日光，\n更少风险", font=font(FONT_BOLD, 64), fill=CFG["dark"], spacing=13)
    draw_fit(draw, (68, 370), CFG["summary"], 1060, 220, 38, CFG["dark"], serif=True, spacing=14)
    labels = [("01", "让光线均匀落到桌面"), ("02", "让开启与通风各有位置"), ("03", "让玻璃经得住碰撞与清洁")]
    x = 68
    for no, text in labels:
        draw.rectangle((x, 690, x + 334, 990), fill=CFG["dark"])
        draw.text((x + 32, 728), no, font=font(FONT_BOLD, 32), fill=CFG["accent"])
        draw_fit(draw, (x + 32, 796), text, 268, 128, 37, LIGHT, serif=True, spacing=11)
        x += 378
    y = 1084
    for i, body in enumerate(CFG["takeaways"], 1):
        draw.text((68, y), f"{i}.", font=font(FONT_BOLD, 31), fill=CFG["accent"])
        draw_fit(draw, (122, y), body, 1010, 88, 27, rgba(CFG["dark"], 220), serif=True, spacing=9)
        y += 116
    draw.rectangle((68, 1452, 1174, 1518), fill=CFG["accent"])
    draw.text((96, 1468), "教室的玻璃，应让孩子看见世界，而不是承担风险。", font=font(FONT_BOLD, 28), fill=LIGHT)
    draw.text((68, 1564), "Diotallevi、Marescotti｜学校中的钢化玻璃｜Casabella 136", font=font(FONT_SANS, 19), fill=rgba(CFG["dark"], 195))
    base.mark(draw, 10)
    return base.save_rgb(canvas, out / "10.jpg")


base.CFG = CFG
base.make_cover = make_cover
base.make_summary = make_summary

if __name__ == "__main__":
    base.render()
