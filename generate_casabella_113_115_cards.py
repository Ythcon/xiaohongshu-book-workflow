from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

from generate_casabella_101_102_cards import (
    BLUE,
    FONT_BOLD,
    FONT_SANS,
    FONT_SERIF,
    H,
    INK,
    LIGHT,
    MUTED,
    PAPER,
    ROOT,
    W,
    draw_fit,
    font,
    header,
    make_card,
    make_preview,
    mount,
    page_mark,
    paper_canvas,
    rgba,
)


ISSUES = [
    {
        "slug": "casabella-113",
        "issue": "CASABELLA 113",
        "date": "MAGGIO 1937 · ANNO X",
        "date_cn": "1937年5月",
        "cover": "book-cover.jpg",
        "accent": "#bf5b42",
        "question": "现代设计，\n如何控制\n不同尺度？",
        "thesis_label": "单元 × 流线 × 分区",
        "thesis": "113期从磨坊、最小住宅、医院、殖民城市到展会建筑，讨论同一件事：把复杂需求拆成可组织的功能单元，再用流线与分区建立整体。",
        "summary": "现代设计跨越尺度的关键，不是重复同一种造型，而是反复使用三种动作：拆出功能单元、连接工作流线、让空间分区回应真实关系。",
        "concepts": ["功能单元", "连续流线", "关系分区"],
        "takeaways": [
            "先把设备、房间或使用者拆成明确单元，形态才能从需求中生长。",
            "用运输、就医、居住与参观路径连接单元，减少交叉和无效面积。",
            "分区必须回应地形、气候与公共关系，不能只把权力等级画成轴线。",
        ],
        "publish_title": "113期｜现代设计如何控制尺度",
        "publish_body": "Casabella 113把现代设计放进一组差异极大的对象：磨坊、纽约高层、东非城市、运河医院、最小住宅和米兰展馆。它们共同追问的不是“采用什么风格”，而是怎样把复杂功能拆开，再重新组织成可工作的整体。\n\nPillsbury磨坊把提升、储存和转运分别交给高塔、筒仓与连桥，生产顺序直接形成轮廓。关于美国城市的文章则指出：摩天楼如果只在旧街网里不断增高，只会叠加密度；高层必须与交通、开放空间和地面公共生活一起重组。\n\nBosio的贡德尔规划利用山地安排道路和功能区，也暴露出分区如何固化权力等级。伊斯梅利亚医院把病房朝向、自然通风和洁污流线放在造型之前；最小住宅通过压缩服务空间、减少走廊，让有限面积承担更多日常活动。米兰展会的临时展馆进一步证明，轻结构、清楚入口和可读标识足以快速建立公共形象。\n\n这期最值得带走的三步是：拆出功能单元、连接连续流线、用关系而不是形式完成分区。",
        "tags": "#Casabella #建筑杂志 #现代建筑 #城市规划 #最小住宅 #医院设计 #工业建筑 #展览建筑",
        "cards": [
            {
                "image": "02-original-frontispiece.jpg",
                "mode": "photo",
                "accent": "#3f7591",
                "focal": (0.52, 0.52),
                "source": "The Architectural Review｜Mulino a Pillsbury, Minnesota｜Casabella 113",
                "eyebrow": "观点 01｜生产顺序可以直接生成体量",
                "title": "提升、储存与转运，被拆成高塔、筒仓和连桥",
                "body": "每个体量对应一道明确工序，设备之间再由最短路径连接。工业建筑不需要额外造型，连续生产关系本身就能形成清楚轮廓。",
            },
            {
                "image": "03-new-york-1932.jpg",
                "mode": "photo",
                "accent": "#bf5b42",
                "focal": (0.54, 0.43),
                "source": "Antonia Nava｜L’America medievale di Le Corbusier｜Casabella 113",
                "eyebrow": "观点 02｜高层必须重新组织地面",
                "title": "只在旧街网里叠加高度，会增加密度却不改善城市",
                "body": "高层的价值不只是容纳更多面积；它应同时释放地面、分离交通并扩大公共空间，否则新技术只会放大旧城市的拥堵。",
            },
            {
                "image": "05-bosio-gondar-plan.jpg",
                "mode": "document",
                "accent": "#71816f",
                "source": "Gherardo Bosio｜Città dell’Africa Orientale｜Casabella 113",
                "eyebrow": "观点 03｜地形既组织城市，也暴露权力",
                "title": "道路顺着山地展开，功能区却把社会等级写进平面",
                "body": "规划利用高差安排道路、行政中心与居住区，减少大规模整地；但严格分区也让空间秩序服务于殖民治理，效率与权力无法分开讨论。",
            },
            {
                "image": "04-ismailia.jpg",
                "mode": "photo",
                "accent": "#3f7591",
                "focal": (0.50, 0.52),
                "source": "Attilio Podestà｜Progetto di ospedale per Ismailia｜Casabella 113",
                "eyebrow": "观点 04｜医院平面先处理气候与分流",
                "title": "病房朝向、自然通风和洁污路径，比正面造型更重要",
                "body": "炎热地区的医院需要稳定日照、穿堂风和清楚的医疗流线。把病房单元沿通风面展开，再分开患者、医护与后勤路径，平面才真正服务康复。",
            },
            {
                "image": "06-minimum-house-plan.jpg",
                "mode": "document",
                "accent": "#bf5b42",
                "source": "Giuseppe Pagano｜Elemento di abitazione minima｜Casabella 113",
                "eyebrow": "观点 05｜最小住宅不是缩小所有房间",
                "title": "压缩服务空间和走廊，把面积留给可转换的日常活动",
                "body": "厨房、卫浴与收纳被集中成紧凑服务带，起居空间承担就餐、工作与休息。经济性来自减少重复功能，而不是让每个房间都变得局促。",
            },
            {
                "image": "07-fiera-milano.jpg",
                "mode": "photo",
                "accent": "#71816f",
                "focal": (0.52, 0.48),
                "source": "Mario Labò｜La diciottesima Fiera di Milano｜Casabella 113",
                "eyebrow": "观点 06｜临时建筑要让信息先被看见",
                "title": "轻结构、清楚入口与大尺度标识，快速建立展馆识别",
                "body": "展馆寿命短，设计重点应从永久纪念性转向装配效率与参观判断。结构负责快速搭建，立面节奏和标识负责远距离导向。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella 113 官方历史封面｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/113-nz.jpg｜等比例放大与轻微清晰化，未改字。",
            "`02-original-frontispiece.jpg`｜Mulino a Pillsbury nel Minnesota，Casabella 113 扉页｜Trento大学图书馆数字馆藏｜https://webapps.unitn.it/Biblioteca/it/Web/EngibankFile/1937%20Casabella%20%5Bperiodico%5D%20113.pdf｜原刊扫描图。",
            "`03-new-york-1932.jpg`｜Samuel Gottscho，纽约中城、帝国大厦与克莱斯勒大厦，1932｜Library of Congress / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Chrysler_Building_Midtown_Manhattan_New_York_City_1932.jpg｜Public Domain。",
            "`05-bosio-gondar-plan.jpg`｜Gherardo Bosio，贡德尔总体规划图｜佛罗伦萨大学研究文献｜https://flore.unifi.it/retrieve/e398c378-eddf-179a-e053-3705fe0a4cff/tesi%20parte%202.pdf｜图版裁切。",
            "`04-ismailia.jpg`｜苏伊士运河与伊斯梅利亚历史图像｜Rijksmuseum / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Canal_de_Suez,_Ismailiya,_RP-F-F16209.jpg｜CC0。",
            "`06-minimum-house-plan.jpg`｜1935年小住宅竞赛平面｜Internet Archive / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:1935_house_plans.jpg｜历史图版。",
            "`07-fiera-milano.jpg`｜Padiglione SAFAR alla Fiera di Milano，1933｜Museo Nazionale della Scienza e della Tecnologia / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Padiglione_SAFAR_alla_Fiera_di_Milano.jpg｜历史档案图。",
        ],
    },
    {
        "slug": "casabella-114",
        "issue": "CASABELLA 114",
        "date": "GIUGNO 1937 · ANNO X",
        "date_cn": "1937年6月",
        "cover": "book-cover.jpg",
        "accent": "#d16b43",
        "question": "现代秩序，\n如何从城市\n落到构件？",
        "thesis_label": "轴线 × 模数 × 装配",
        "thesis": "114期把E42总体规划、公共建筑、可拆装家具与工业薄板并置：现代秩序既通过城市轴线建立，也通过重复模数和连接节点落到日常构件。",
        "summary": "从国家尺度的城市计划到一件可拆家具，设计都在处理同一组关系：用轴线建立方向，用模数控制重复，用连接方式决定系统能否快速建造和调整。",
        "concepts": ["建立方向", "控制重复", "简化连接"],
        "takeaways": [
            "总体规划先确定公共轴线、开放空间与交通层级，再安排纪念性单体。",
            "立面、结构和家具都可由稳定模数生成，重复不等于单调。",
            "把湿作业改成干式连接，让建筑与家具更快装配、维修和迁移。",
        ],
        "publish_title": "114期｜从城市轴线到薄板",
        "publish_body": "Casabella 114把两个看似相反的尺度放在同一期：一边是面向1942年罗马世界博览会的E42城市计划，另一边是军官用可拆装家具与Faesite工业板材。它们共同关心的是，秩序怎样从总体规划一直落实到最小构件。\n\nE42总平面用主轴、广场和公共建筑群制造清楚方向，但也让城市承担强烈的国家叙事。文明宫竞赛方案用连续拱券和严格开间把纪念性转化为可重复的立面模块；Libera的会议宫则以大跨空间、顶部采光和连续大厅组织集会。\n\n施工照片揭示出另一层现实：宏大的石质形象仍依赖规则骨架、脚手架和分段施工。Albini与Palanti的军官家具进一步把同样的模数逻辑缩小到柜、床与桌；一个系统通过折叠、拆装和组合承担多种使用。Marescotti讨论Faesite时，重点也不在材料表面，而在薄板如何减少重量、湿作业和运输负担。\n\n这期可以直接带走三条方法：先建立方向，再控制重复，最后把连接做简单。",
        "tags": "#Casabella #建筑杂志 #E42 #EUR罗马 #现代建筑 #家具设计 #装配式设计 #材料设计",
        "cards": [
            {
                "image": "02-e42-masterplan.jpg",
                "mode": "document",
                "accent": "#d16b43",
                "source": "Giuseppe Pagano｜L’Esposizione Universale di Roma 1941–1942｜Casabella 114",
                "eyebrow": "观点 01｜总体规划先建立方向",
                "title": "主轴、广场与公共建筑群，把分散单体组织成城市序列",
                "body": "道路层级和开放空间先给出移动方向，再由公共建筑占据节点。总体规划的作用不是摆放造型，而是控制到达、转折与集体空间。",
            },
            {
                "image": "03-palazzo-civilta-competition.jpg",
                "mode": "document",
                "accent": "#6f8172",
                "source": "G. Guerrini / E. La Padula / M. Romano｜Palazzo della Civiltà Italiana｜Casabella 114",
                "eyebrow": "观点 02｜纪念性可以来自重复模块",
                "title": "连续拱券和严格开间，用同一单元制造巨大尺度",
                "body": "立面没有依靠复杂装饰，而是反复叠加等距拱券。单个开间保持可读，整体通过数量和比例获得稳定、强烈的公共形象。",
            },
            {
                "image": "04-palazzo-congressi-hall.jpg",
                "mode": "photo",
                "accent": "#3f7591",
                "focal": (0.50, 0.49),
                "source": "Adalberto Libera｜Palazzo dei Congressi｜Casabella 114",
                "eyebrow": "观点 03｜大空间需要光线帮助定位",
                "title": "大跨大厅与顶部采光，让集会空间保持方向和尺度感",
                "body": "宽阔大厅减少内部柱列，顶部与端部光线标出行进方向。人在巨大室内仍能判断入口、中心与出口，空间不会只剩空旷。",
            },
            {
                "image": "05-e42-construction.jpg",
                "mode": "photo",
                "accent": "#d16b43",
                "focal": (0.52, 0.46),
                "source": "Giuseppe Pagano｜L’Esposizione Universale di Roma 1941–1942｜Casabella 114",
                "eyebrow": "观点 04｜宏大形象仍依赖施工系统",
                "title": "规则骨架先承担结构，石材表皮再完成纪念性界面",
                "body": "施工过程把承重框架与外部形象清楚分开。重复开间便于分段推进，围护只需跟随模数安装，宏大体量因此可以被标准工序建成。",
            },
            {
                "image": "06-albini-room.jpg",
                "mode": "photo",
                "accent": "#6f8172",
                "focal": (0.52, 0.50),
                "source": "Alfonso Gatto｜Mobili in serie per gli ufficiali in A.O.｜Casabella 114",
                "eyebrow": "观点 05｜家具系统要适应迁移",
                "title": "床、柜与桌采用统一尺度，拆开后更容易运输和重组",
                "body": "家具不再是固定房间的孤立物件，而是一组可装配单元。统一尺寸减少零件种类，使用者可以随驻地变化重新组合空间。",
            },
            {
                "image": "07-faesite-cabinet.jpg",
                "mode": "document",
                "accent": "#3f7591",
                "source": "Franco Marescotti｜Applicazioni della Faesite｜Casabella 114",
                "eyebrow": "观点 06｜薄板改变建造方式",
                "title": "轻质板材替代厚重填充，让围护和家具转向干式装配",
                "body": "Faesite把连续表面压缩成薄而轻的板件，减少运输重量和现场湿作业。价值不只在材料更薄，而在连接、维修与拆换都更直接。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella 114 官方历史封面｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/114-nz.jpg｜等比例放大与轻微清晰化，未改字。",
            "`02-e42-masterplan.jpg`｜EUR 42总体规划图｜ArchiDiAP / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:EUR_42_-_Planimetria_generale.jpg｜CC BY-SA 3.0。",
            "`03-palazzo-civilta-competition.jpg`｜文明宫竞赛方案绘画，Guerrini / La Padula / Romano｜Archivio Lapadula / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Archivio-lapadula_quadro_palazzo-civilt%C3%A0-italiana.jpg｜CC BY-SA 3.0 / GFDL。",
            "`04-palazzo-congressi-hall.jpg`｜Adalberto Libera，Palazzo dei Congressi入口大厅｜Husky / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Palazzo_dei_Congressi_EUR_Rome_-_entrance_hall.jpg｜CC BY 4.0。",
            "`05-e42-construction.jpg`｜Palazzo della Civiltà Italiana施工，1940｜Oggi / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:E42_in_costruzione.jpg｜Public Domain。",
            "`06-albini-room.jpg`｜Franco Albini / Giancarlo Palanti，可拆装军官家具与房间布置｜Domus 145 图版，收录于米兰理工大学研究文献｜https://re.public.polimi.it/retrieve/d68a50d3-805a-4189-96de-bedcbd2fba4b/Libro%20Arq%20y%20vida%20cotidiana%20en%20contextos%20internacionales_LECCE.pdf｜图版裁切。",
            "`07-faesite-cabinet.jpg`｜可拆装柜体与殖民装备图版｜Domus 145，收录于米兰理工大学研究文献｜https://re.public.polimi.it/retrieve/d68a50d3-805a-4189-96de-bedcbd2fba4b/Libro%20Arq%20y%20vida%20cotidiana%20en%20contextos%20internacionales_LECCE.pdf｜图版裁切。",
        ],
    },
    {
        "slug": "casabella-115",
        "issue": "CASABELLA 115",
        "date": "LUGLIO 1937 · ANNO X",
        "date_cn": "1937年7月",
        "cover": "book-cover.jpg",
        "accent": "#c75a40",
        "question": "国家馆，\n如何变成一条\n空间叙事？",
        "thesis_label": "接近 × 识别 × 行走",
        "thesis": "115期集中讨论巴黎世博意大利馆：国家馆不是一张孤立立面，而是从塞纳河远景、塔楼识别、入口阴影到连续展厅的完整参观过程。",
        "summary": "展览建筑的公共形象不是贴在立面上的口号，而是在移动中逐步形成：城市远景负责识别，入口制造尺度变化，连续路径把展品、庭院与出口串成记忆。",
        "concepts": ["远景识别", "入口过渡", "连续参观"],
        "takeaways": [
            "先决定建筑从城市和水岸如何被看见，再确定主入口与标志体量。",
            "用台阶、门廊、阴影和层高变化，让进入过程逐步收紧再展开。",
            "把展厅、庭院和出口编成连续环线，避免参观流线频繁折返。",
        ],
        "publish_title": "115期｜国家馆是一条路径",
        "publish_body": "Casabella 115几乎把整期视线集中到1937年巴黎世博意大利馆。Pagano先质疑展览建筑对表面宣传和临时奇观的依赖，随后由Zveteremich展开国家馆的建筑分析。真正值得看的不是某一张立面，而是建筑怎样控制完整的接近与参观过程。\n\n从塞纳河望去，塔楼先成为远距离标志，较低的展厅体量再沿水岸展开。垂直塔体、水平基座和入口前列柱形成不同速度的识别层次：城市远景先读轮廓，靠近后才看到开间、旗杆与门廊。\n\n入口没有把人直接丢进展厅，而是利用台阶、阴影和层高变化制造过渡。进入之后，连续展厅与中间开放空间共同组织参观，避免路径不断折返。建筑表面的深窗、柱列和石材分缝同时承担遮阳、尺度控制与公共形象，不只是装饰。\n\n这期给展览设计最直接的提醒是：先设计从哪里看见，再设计怎样进入，最后设计如何连续走完。",
        "tags": "#Casabella #建筑杂志 #巴黎世博会 #意大利馆 #展览建筑 #公共建筑 #建筑流线 #建筑史",
        "cards": [
            {
                "image": "02-italy-pavilion-postcard-18.jpg",
                "mode": "document",
                "accent": "#c75a40",
                "source": "Giuseppe Pagano｜Parliamo un po’ di esposizioni｜Casabella 115",
                "eyebrow": "观点 01｜展馆不能只制造正面",
                "title": "公共形象应来自接近、进入和参观，而不是表面宣传",
                "body": "展览建筑寿命短，更需要把资源放在清楚路径、适宜光线和可变展厅。立面只负责第一眼，完整体验必须由空间过程完成。",
            },
            {
                "image": "03-italy-pavilion-postcard-19.jpg",
                "mode": "photo",
                "accent": "#3f7591",
                "focal": (0.43, 0.44),
                "source": "Renato Zveteremich｜Il padiglione Italiano all’Esposizione di Parigi｜Casabella 115",
                "eyebrow": "观点 02｜塔楼负责远景识别",
                "title": "一个垂直体量先标记位置，低矮展厅再连接水岸",
                "body": "塔楼从周边展馆和树冠中抬起，成为跨河可见的坐标；水平基座保持与步行尺度和滨水界面的连续，远近两种尺度同时成立。",
            },
            {
                "image": "04-italy-pavilion-07.jpg",
                "mode": "photo",
                "accent": "#c75a40",
                "focal": (0.62, 0.56),
                "source": "M. Piacentini / G. Pagano｜Padiglione Italiano, Parigi｜Casabella 115",
                "eyebrow": "观点 03｜入口需要一段过渡",
                "title": "旗杆、列柱与深阴影，把滨水步道逐步转成室内门厅",
                "body": "入口前的竖向构件先缩小人的尺度，门廊阴影再降低视觉亮度。进入不是穿过一扇门，而是一段由开放到遮蔽的连续变化。",
            },
            {
                "image": "05-italy-pavilion-day.jpg",
                "mode": "photo",
                "accent": "#71816f",
                "focal": (0.26, 0.55),
                "source": "M. Piacentini / G. Pagano｜Padiglione Italiano, Parigi｜Casabella 115",
                "eyebrow": "观点 04｜体量差异帮助辨认功能",
                "title": "塔楼、展厅和滨水基座保持不同高度，让入口一眼可读",
                "body": "高体量承担城市标志，中层容纳主要展厅，低层连接河岸和到达空间。功能没有被包进一个大盒子，而是通过高度差直接表达。",
            },
            {
                "image": "06-seine-pavilions.jpg",
                "mode": "document",
                "accent": "#3f7591",
                "source": "Renato Zveteremich｜Il padiglione Italiano all’Esposizione di Parigi｜Casabella 115",
                "eyebrow": "观点 05｜国家馆必须回应相邻建筑",
                "title": "沿河保持连续基线，再用塔楼与邻馆建立轮廓差异",
                "body": "滨水建筑共同形成一条公共边界，单馆不能只顾自身正面。连续檐口维持街道秩序，局部高点才获得清楚的城市识别。",
            },
            {
                "image": "07-seine-overview.jpg",
                "mode": "photo",
                "accent": "#c75a40",
                "focal": (0.70, 0.58),
                "source": "M. Piacentini / G. Pagano｜Padiglione Italiano, Parigi｜Casabella 115",
                "eyebrow": "观点 06｜参观路径要形成完整环线",
                "title": "展厅、开放空间与出口连续相接，减少折返和拥堵",
                "body": "参观者沿主序列进入，在不同展厅和开放节点之间持续前进，最后回到滨水公共空间。流线形成闭合叙事，展品顺序也更容易被记住。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella 115 官方历史封面｜Casabella 官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/115-nz.jpg｜等比例放大与轻微清晰化，未改字。",
            "`02-italy-pavilion-postcard-18.jpg`｜1937巴黎世博意大利馆明信片18｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Paris-Expo-1937-carte_postale-18.jpg｜Public Domain。",
            "`03-italy-pavilion-postcard-19.jpg`｜1937巴黎世博意大利馆明信片19｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Paris-Expo-1937-carte_postale-19.jpg｜Public Domain。",
            "`04-italy-pavilion-07.jpg`｜1937巴黎世博意大利馆彩色档案图｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Paris-expo-1937-pavillon_de_l%27Italie-07.jpg｜历史档案图。",
            "`05-italy-pavilion-day.jpg`｜1937巴黎世博意大利馆日景｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Paris_World_Expo_1937_---_Italian_Pavillion_at_daytime_---_Pavillion_italien_%C3%A1_jour.jpg｜历史档案图。",
            "`06-seine-pavilions.jpg`｜塞纳河岸展馆群，意大利馆与瑞士馆｜Nationaal Archief / Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Paviljoens_langs_de_Seinekade_met_rechts_het_Zwitsers_paviljoen_met_diverse_rond,_Bestanddeelnr_254-2677.jpg｜CC0 / Public Domain。",
            "`07-seine-overview.jpg`｜1937巴黎世博塞纳河岸与意大利馆｜Wikimedia Commons｜https://commons.wikimedia.org/wiki/File:Paris_expo_1937_Seine.jpg｜历史档案图。",
        ],
    },
]


def save_rgb(image: Image.Image, path: Path) -> None:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)


def crop_relative(source: Path, target: Path, box: tuple[float, float, float, float], width: int = 1500) -> None:
    image = Image.open(source).convert("RGB")
    crop = image.crop(
        (
            round(image.width * box[0]),
            round(image.height * box[1]),
            round(image.width * box[2]),
            round(image.height * box[3]),
        )
    )
    if crop.width < width:
        height = round(crop.height * width / crop.width)
        crop = crop.resize((width, height), Image.Resampling.LANCZOS)
    crop = ImageEnhance.Contrast(crop).enhance(1.08)
    crop = ImageEnhance.Sharpness(crop).enhance(1.25)
    crop.save(target, quality=96, subsampling=0)


def prepare_assets(cfg: dict, src: Path) -> None:
    if cfg["slug"] == "casabella-113":
        crop_relative(
            ROOT / "tmp" / "pdfs" / "bosio-gondar-43.png",
            src / "05-bosio-gondar-plan.jpg",
            (0.15, 0.275, 0.85, 0.675),
        )
    elif cfg["slug"] == "casabella-114":
        page = ROOT / "tmp" / "pdfs" / "albini-14.png"
        crop_relative(page, src / "06-albini-room.jpg", (0.49, 0.315, 0.87, 0.505), 1600)
        crop_relative(page, src / "07-faesite-cabinet.jpg", (0.14, 0.505, 0.50, 0.69), 1600)


def make_cover_113(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(11301)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, 780, H), fill=rgba(BLUE))
    draw.text((66, 55), cfg["issue"], font=font(FONT_BOLD, 28), fill=LIGHT)
    draw.text((714, 61), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(LIGHT, 175), anchor="ra")

    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (72, 158, 635, 830), True)

    draw.text((838, 120), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (838, 194), cfg["question"], 330, 480, 57, INK, serif=True, spacing=15)
    draw.line((838, 760, 1168, 760), fill=accent, width=8)
    draw.text((838, 807), cfg["thesis_label"], font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (838, 870), cfg["thesis"], 330, 470, 31, INK, serif=True, spacing=13)

    draw.rectangle((70, 1110, 710, 1120), fill=accent)
    draw_fit(draw, (70, 1174), "不同尺度，不需要同一种形式；需要同一种组织能力。", 640, 250, 40, LIGHT, serif=True, spacing=14)
    draw.text((70, 1518), "Casabella 113｜Maggio 1937", font=font(FONT_SANS, 18), fill=rgba(LIGHT, 175))
    page_mark(draw, 1, True)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_cover_114(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(11401)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 330), fill=rgba(BLUE))
    draw.text((68, 54), cfg["issue"], font=font(FONT_BOLD, 28), fill=LIGHT)
    draw.text((1170, 60), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(LIGHT, 180), anchor="ra")
    draw.text((68, 122), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (68, 175), cfg["question"], 1050, 135, 54, LIGHT, serif=True, spacing=8)

    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (570, 350, 610, 800), True)

    draw.text((72, 435), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (72, 500), cfg["thesis"], 450, 510, 38, INK, serif=True, spacing=15)
    draw.rectangle((72, 1190, 1098, 1200), fill=accent)
    draw_fit(draw, (72, 1250), "轴线建立方向，模数控制重复，连接决定建造速度。", 1030, 170, 40, BLUE, serif=True, spacing=12)
    draw.text((72, 1518), "Casabella 114｜Giugno 1937", font=font(FONT_SANS, 18), fill=MUTED)
    page_mark(draw, 1, False)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_cover_115(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(BLUE))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, 420, H), fill=rgba("#102b3d"))
    draw.text((64, 56), cfg["issue"], font=font(FONT_BOLD, 28), fill=LIGHT)
    draw.text((64, 106), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(LIGHT, 170))
    draw.text((64, 205), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (64, 270), cfg["question"], 305, 510, 54, LIGHT, serif=True, spacing=16)

    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.35)
    mount(canvas, cover, (485, 95, 670, 850), True)
    draw.rectangle((485, 1010, 1168, 1020), fill=accent)
    draw.text((485, 1067), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (485, 1130), cfg["thesis"], 670, 330, 35, LIGHT, serif=True, spacing=14)
    draw.text((64, 1518), "Casabella 115｜Luglio 1937", font=font(FONT_SANS, 18), fill=rgba(LIGHT, 170))
    page_mark(draw, 1, True)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_summary_113(cfg: dict, out: Path) -> Path:
    canvas = paper_canvas(11308)
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, False)
    accent = cfg["accent"]
    draw.text((72, 160), "从单元到城市：同一套组织动作", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (72, 230), cfg["summary"], 1080, 290, 47, INK, serif=True, spacing=17)

    colors = ["#3f7591", "#bf5b42", "#71816f"]
    y_positions = [705, 970, 1235]
    widths = [590, 850, 1080]
    for idx, (y, label, body, color, width) in enumerate(
        zip(y_positions, cfg["concepts"], cfg["takeaways"], colors, widths), 1
    ):
        draw.rounded_rectangle((72, y, 72 + width, y + 86), 8, fill=color)
        draw.text((104, y + 43), f"0{idx}", font=font(FONT_BOLD, 26), fill=LIGHT, anchor="lm")
        draw.text((188, y + 43), label, font=font(FONT_BOLD, 29), fill=LIGHT, anchor="lm")
        draw_fit(draw, (96, y + 120), body, 1025, 110, 29, rgba(INK, 215), serif=True, spacing=9)

    page_mark(draw, 8, False)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def make_summary_114(cfg: dict, out: Path) -> Path:
    canvas = paper_canvas(11408)
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, False)
    accent = cfg["accent"]
    draw.rectangle((0, 125, W, 575), fill=rgba(BLUE))
    draw.text((72, 178), "秩序从总体规划落到连接节点", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (72, 252), cfg["summary"], 1080, 250, 46, LIGHT, serif=True, spacing=16)

    columns = [(72, 625), (445, 760), (818, 895)]
    colors = ["#d16b43", "#6f8172", "#3f7591"]
    for idx, ((x, y), label, body, color) in enumerate(zip(columns, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.rounded_rectangle((x, y, x + 320, y + 640), 10, fill=rgba(color, 238))
        draw.text((x + 28, y + 40), f"0{idx}", font=font(FONT_BOLD, 36), fill=LIGHT)
        draw.text((x + 28, y + 112), label, font=font(FONT_BOLD, 34), fill=LIGHT)
        draw.line((x + 28, y + 184, x + 280, y + 184), fill=rgba(LIGHT, 90), width=2)
        draw_fit(draw, (x + 28, y + 230), body, 260, 330, 29, LIGHT, serif=True, spacing=12)

    page_mark(draw, 8, False)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def make_summary_115(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(BLUE))
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, True)
    accent = cfg["accent"]
    draw.text((72, 160), "把公共形象设计成一段行走", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (72, 232), cfg["summary"], 1080, 300, 47, LIGHT, serif=True, spacing=17)

    draw.line((130, 770, 130, 1428), fill=rgba(LIGHT, 110), width=5)
    colors = ["#c75a40", "#80a099", "#e1b25d"]
    y_positions = [745, 990, 1235]
    for idx, (y, label, body, color) in enumerate(zip(y_positions, cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.ellipse((98, y, 162, y + 64), fill=color)
        draw.text((130, y + 32), str(idx), font=font(FONT_BOLD, 25), fill=BLUE, anchor="mm")
        draw.text((215, y + 4), label, font=font(FONT_BOLD, 34), fill=LIGHT)
        draw_fit(draw, (215, y + 68), body, 900, 125, 29, rgba(LIGHT, 220), spacing=10)

    draw.text((72, 1522), "先看见  →  再进入  →  连续走完", font=font(FONT_BOLD, 26), fill=accent)
    page_mark(draw, 8, True)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def post_manifest(cfg: dict) -> dict:
    return {
        "type": "magazine",
        "slug": cfg["slug"],
        "issue": cfg["issue"].title(),
        "date": cfg["date_cn"],
        "core_question": cfg["question"].replace("\n", ""),
        "core_thesis": cfg["thesis"],
        "pages": [
            f"01 单期主线：{cfg['question'].replace(chr(10), '')}",
            *[
                f"{number:02d} {card['source'].split('｜')[0]}：{card['title']}"
                for number, card in enumerate(cfg["cards"], 2)
            ],
            f"08 总结：{'—'.join(cfg['concepts'])}",
        ],
    }


def source_records(cfg: dict) -> str:
    rows = "\n".join(f"- {item}" for item in cfg["sources"])
    return (
        f"# {cfg['issue'].title()} 图片来源\n\n"
        f"{rows}\n\n"
        "本组用于建筑杂志内容整理与教育性发布；公开许可图像按其许可条件署名，"
        "其他历史图像的使用范围以来源页为准，商业投放前请逐张复核。\n"
    )


def write_text_files(cfg: dict, out: Path) -> None:
    publish = f"{cfg['publish_title']}\n\n{cfg['publish_body']}\n\n{cfg['tags']}\n"
    (out / "发布文案.md").write_text(publish, encoding="utf-8")
    (out / "图片来源.md").write_text(source_records(cfg), encoding="utf-8")

    post_dir = ROOT / "posts" / cfg["slug"]
    post_dir.mkdir(parents=True, exist_ok=True)
    (post_dir / "post.json").write_text(
        json.dumps(post_manifest(cfg), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def render_issue(cfg: dict) -> None:
    src = ROOT / "assets" / cfg["slug"]
    out = ROOT / "output" / cfg["slug"]
    out.mkdir(parents=True, exist_ok=True)
    prepare_assets(cfg, src)

    cover_maker = {
        "casabella-113": make_cover_113,
        "casabella-114": make_cover_114,
        "casabella-115": make_cover_115,
    }[cfg["slug"]]
    summary_maker = {
        "casabella-113": make_summary_113,
        "casabella-114": make_summary_114,
        "casabella-115": make_summary_115,
    }[cfg["slug"]]

    paths = [cover_maker(cfg, src, out)]
    paths.extend(make_card(cfg, src, out, number, card) for number, card in enumerate(cfg["cards"], 2))
    paths.append(summary_maker(cfg, out))
    make_preview(paths, out)
    write_text_files(cfg, out)
    print(f"Created {len(paths)} cards, preview and publishing files in {out}")


if __name__ == "__main__":
    for issue in ISSUES:
        render_issue(issue)
