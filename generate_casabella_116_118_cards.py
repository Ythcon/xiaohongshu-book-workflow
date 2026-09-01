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
        "slug": "casabella-116",
        "issue": "CASABELLA 116",
        "date": "AGOSTO 1937 · ANNO X",
        "date_cn": "1937年8月",
        "cover": "book-cover.jpg",
        "accent": "#c65a3f",
        "question": "儿童建筑，\n如何组织\n阳光、空气与集体生活？",
        "thesis_label": "日照  流线  集体单元",
        "thesis": "116期把儿童营看成环境基础设施：建筑用朝向、通廊、寝室单元和公共场地安排身体活动，也让集体照护与政治纪律同时进入平面。",
        "summary": "儿童建筑的现代性不只来自白色墙面，而来自三种可检验的组织动作：让日照进入每个生活单元，让移动路线连接学习、休息与户外，让集体空间既便于照护也保留人的尺度。",
        "concepts": ["朝向先于造型", "流线连接生活", "集体尺度可被拆分"],
        "takeaways": [
            "先用日照、风向和地形确定建筑的弯折与开口，再决定立面节奏。",
            "寝室、餐厅、运动场和户外平台要形成连续路线，减少封闭走廊。",
            "大规模集体生活应拆成可识别的小单元，避免空间只剩纪律和队列。",
        ],
        "publish_title": "116期｜儿童建筑与集体生活",
        "publish_body": "Casabella 116把儿童营、儿童救助展览和集体生活建筑放到同一条主线上：建筑如何把日照、空气、运动和照护变成可以被组织的空间。\n\n罗马儿童营展览以一条连续大道串起多个机构馆，入口、展馆、公共活动和大会堂形成清晰顺序。它证明流线可以让复杂内容变得易读，也提醒我们：当参观、训练和展示被编成同一条路线，建筑同样会参与塑造纪律。\n\n不同儿童营给出更具体的空间答案。塔式方案用垂直交通压缩占地，却增加了日常移动距离；低层海滨营把寝室和公共空间铺向阳光与海风；船形长条把集体单元组织在连续主轴两侧；庭院式营地则用多个可识别的小体量降低机构尺度。Roio山地营更直接：双重弯折的长体量争取冬季日照，连续顶层通廊把疗养、远眺和户外活动叠在一起。\n\n这一期最值得带走的不是某种白色现代主义造型，而是三条方法：朝向先于造型，流线连接生活，大集体必须拆成可照护的小单元。",
        "tags": "#Casabella #建筑杂志 #现代建筑 #儿童建筑 #集体生活 #疗养建筑 #建筑流线 #建筑设计",
        "cards": [
            {
                "image": "02-exhibition-avenue.jpg",
                "mode": "photo",
                "accent": "#c65a3f",
                "focal": (0.48, 0.66),
                "source": "Giuseppe Pagano｜La Mostra Nazionale delle Colonie Estive｜Casabella 116",
                "eyebrow": "观点 01｜展览路线就是空间叙事",
                "title": "入口、机构馆与大会堂排成连续序列，让复杂救助体系一眼可读",
                "body": "主轴把多个独立展馆接成单向进程，参观者不必反复折返。路线提高信息效率，也把观看、训练与集体秩序绑定在一起。",
            },
            {
                "image": "03-roio-strategy.png",
                "mode": "document",
                "accent": "#4b7890",
                "source": "Giuseppe Pagano｜Una colonia montana｜Casabella 116",
                "eyebrow": "观点 02｜弯折体量追随山地日照",
                "title": "双重弯折的长体量调整寝室朝向，顶层通廊把疗养与远眺合并",
                "body": "连续寝室带不必僵直地落在山地上。轻微转折能扩大向阳面，公共核心放在折点，顶层开放通廊则提供可控的户外活动空间。",
            },
            {
                "image": "04-torre-balilla.jpg",
                "mode": "photo",
                "accent": "#71816f",
                "focal": (0.50, 0.52),
                "source": "Vittorio Bonadè-Bottino｜Colonia FIAT Torre Balilla｜Casabella 116",
                "eyebrow": "观点 03｜垂直集中会改变日常距离",
                "title": "塔楼压缩了场地占用，却把寝室、餐厅与户外活动拉成垂直长路",
                "body": "高层集体建筑节省用地，但电梯、坡道与楼梯会成为生活主干。评价塔式方案不能只看轮廓，还要计算儿童每天上下移动的次数和距离。",
            },
            {
                "image": "05-calambrone.jpg",
                "mode": "photo",
                "accent": "#c65a3f",
                "focal": (0.50, 0.54),
                "source": "Angiolo Mazzoni｜Colonia di Calambrone｜Casabella 116",
                "eyebrow": "观点 04｜低层分段让海风穿过建筑",
                "title": "寝室体量分段排列，端部楼梯塔承担识别与垂直交通",
                "body": "长建筑被拆成数个低层单元，单元之间保留通风间隙。两端楼梯塔把公共交通从寝室带中抽离，也让大型机构获得清楚的方向标记。",
            },
            {
                "image": "06-le-navi.jpg",
                "mode": "photo",
                "accent": "#4b7890",
                "focal": (0.56, 0.50),
                "source": "Clemente Busiri Vici｜Colonia Le Navi｜Casabella 116",
                "eyebrow": "观点 05｜连续主轴组织集体单元",
                "title": "船形长条沿主轴展开，寝室、服务与户外平台保持同一方向",
                "body": "狭长体量减少复杂转角，让采光面、交通面和服务面保持稳定关系。重复单元便于管理，但必须用开敞节点打断无尽走廊。",
            },
            {
                "image": "07-marina-massa.jpg",
                "mode": "photo",
                "accent": "#71816f",
                "focal": (0.50, 0.48),
                "source": "Francesco Mansutti / Gino Miozzo｜Colonia ONB Marina di Massa｜Casabella 116",
                "eyebrow": "观点 06｜庭院降低机构尺度",
                "title": "多个低体量围合庭院，让大集体被拆成可识别的生活片区",
                "body": "餐厅、寝室和活动空间不必塞进单一巨构。用连廊串联若干院落，每个组团都能获得独立入口、近距离户外场地和更清楚的照护边界。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella 116官方历史封面｜Casabella官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/116-nz.jpg",
            "`02-exhibition-avenue.jpg`｜1937年罗马儿童营与儿童救助展览大道｜Accademia Nazionale di San Luca / Fondo Mario De Renzi，经docomomo Journal收录｜https://docomomojournal.com/index.php/journal/article/download/336/88/88",
            "`03-roio-strategy.png`｜Roio山地儿童营朝向、弯折体量与顶层通廊｜依据Giuseppe Pagano《Una colonia montana》及历史建筑资料｜https://assergiracconta.altervista.org/archivioNews.php?id=25731&page=1",
            "`04-torre-balilla.jpg`｜Vittorio Bonadè-Bottino，FIAT Torre Balilla儿童营｜Archivio storico FIAT，经docomomo Journal收录｜https://docomomojournal.com/index.php/journal/article/download/336/88/88",
            "`05-calambrone.jpg`｜Angiolo Mazzoni，Calambrone儿童营｜MART Fondo Angiolo Mazzoni，经docomomo Journal收录｜https://docomomojournal.com/index.php/journal/article/download/336/88/88",
            "`06-le-navi.jpg`｜Clemente Busiri Vici，Le Navi儿童营｜Archivio Clemente Busiri Vici，经docomomo Journal收录｜https://docomomojournal.com/index.php/journal/article/download/336/88/88",
            "`07-marina-massa.jpg`｜Francesco Mansutti、Gino Miozzo，Marina di Massa儿童营｜MART Fondo Angiolo Mazzoni，经docomomo Journal收录｜https://docomomojournal.com/index.php/journal/article/download/336/88/88",
        ],
    },
    {
        "slug": "casabella-117",
        "issue": "CASABELLA 117",
        "date": "SETTEMBRE 1937 · ANNO X",
        "date_cn": "1937年9月",
        "cover": "book-cover.jpg",
        "accent": "#3f7894",
        "question": "空间，\n如何主动控制\n视线、气候与安全？",
        "thesis_label": "视线  气候  防护  声学",
        "thesis": "117期把现代生活理解为环境控制：餐厅用连续玻璃占据海景，住宅用庭院重新编排身体与气候，防空空间和多孔材料则把安全、温度与声音纳入构造。",
        "summary": "环境不会自动变舒适。建筑必须主动决定看向哪里、何时遮蔽、危险时如何撤离，以及墙体怎样阻断热量和噪声。117期把这些看似分散的问题收束成一套空间控制方法。",
        "concepts": ["框定视线", "驯化气候", "构造承担防护"],
        "takeaways": [
            "连续开窗应同时处理景观、眩光、遮阳和家具布置，而不是只追求透明。",
            "庭院让室外成为可使用的房间，围墙、树荫和开口共同调节微气候。",
            "避难、气密与吸声必须进入平面和节点，不能等主体完成后再外挂设备。",
        ],
        "publish_title": "117期｜空间如何控制环境",
        "publish_body": "Casabella 117讨论的不是一种统一风格，而是现代空间怎样主动控制环境。\n\nMario Labò在热那亚的海滨餐厅用连续转角玻璃把就餐空间推向海面。视线几乎没有中断，但真正有效的是玻璃、深檐、桌椅方向和条纹地面共同把人的身体朝向水平线。Rudofsky的Procida住宅更进一步：庭院不是剩余空地，而是住宅的主要房间；树木、围墙、开口和地面活动一起规定休息、用餐、沐浴和观看。\n\n同一期把舒适扩展到危险和材料。Palanti讨论住宅防空与防毒时，核心不是在地下室塞进一个房间，而是预先安排最短到达路线、气密前室、第二出口和可独立工作的通风。Cel-Bes与多孔Faesite则把温度和声音交给材料内部的空气胞腔；板材的孔隙、厚度、接缝和铺设连续性共同决定性能。\n\n这一期留下的判断很直接：开窗控制视线，庭院驯化气候，构造承担安全与声学。舒适不是装饰结果，而是平面、剖面和节点协同工作的结果。",
        "tags": "#Casabella #建筑杂志 #现代住宅 #室内设计 #环境控制 #防空建筑 #建筑声学 #材料设计",
        "cards": [
            {
                "image": "02-restaurant.jpg",
                "mode": "photo",
                "accent": "#3f7894",
                "focal": (0.54, 0.52),
                "source": "Mario Labò / Attilio Podestà｜Un ristorante a Genova｜Casabella 117",
                "eyebrow": "观点 01｜连续玻璃把用餐朝向海面",
                "title": "转角玻璃、深檐与桌椅方向共同组织视线，而不只是制造透明",
                "body": "玻璃面连续包裹餐厅，水平线成为室内的主要参照。深檐控制眩光，桌椅顺着景观布置，地面条纹则进一步强化朝海的方向。",
            },
            {
                "image": "03-procida-plan.jpg",
                "mode": "document",
                "accent": "#c65a3f",
                "source": "Bernard Rudofsky / Attilio Podestà｜Una casa a Procida｜Casabella 117",
                "eyebrow": "观点 02｜平面从生活动作开始",
                "title": "房间不按名称排列，而按躺卧、进食、沐浴和穿行的动作组织",
                "body": "住宅把身体使用方式直接画进平面。家具、地面与门洞围绕动作确定位置，空间因此不再是装功能的盒子，而是生活习惯的具体构造。",
            },
            {
                "image": "04-procida-perspective.jpg",
                "mode": "document",
                "accent": "#71816f",
                "source": "Bernard Rudofsky / Attilio Podestà｜Una casa a Procida｜Casabella 117",
                "eyebrow": "观点 03｜庭院是主要起居空间",
                "title": "围墙、树荫和开口把室外驯化成房间，天空直接成为顶棚",
                "body": "低矮围护保护隐私和避风，树木提供季节性阴影，室内开口则围绕庭院展开。自然没有被隔在窗外，而是被组织成可长期停留的生活空间。",
            },
            {
                "image": "05-airraid-plan.jpg",
                "mode": "document",
                "accent": "#3f7894",
                "source": "Giancarlo Palanti｜Ricoveri antiaerei e protezione antigas｜Casabella 117",
                "eyebrow": "观点 04｜避难空间必须进入住宅平面",
                "title": "最短到达路线、气密前室与第二出口，决定避难所是否真正可用",
                "body": "危险发生时，入口距离和转折数量比房间面积更关键。气密前室隔开污染空气，独立通风和备用出口则让避难空间在主体系统失效后仍能工作。",
            },
            {
                "image": "06-celbes-ad.jpg",
                "mode": "document",
                "accent": "#c65a3f",
                "source": "Tullio Bussi｜Note tecniche sul Cel-Bes｜Casabella 117",
                "eyebrow": "观点 05｜空气胞腔同时减轻与隔绝",
                "title": "木纤维板内部保存大量空气，降低重量并减缓热量与声音传递",
                "body": "材料性能来自内部结构而不是表面图案。连续胞腔把密实墙体变成轻质隔层，但接缝如果不连续，隔热与吸声都会在节点处失效。",
            },
            {
                "image": "07-faesite-ad.jpg",
                "mode": "document",
                "accent": "#71816f",
                "source": "Franco Marescotti｜Il Faesite tipo poroso｜Casabella 117",
                "eyebrow": "观点 06｜孔隙决定室内声场",
                "title": "多孔板让声能进入内部并被摩擦消耗，墙面因此参与控制混响",
                "body": "吸声不等于把墙做软。孔径、板厚、背后空腔和覆盖面积共同决定有效频段；只有连续布置并处理好边缘，材料才会真正改变室内听感。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella 117官方历史封面｜Casabella官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/117-nz.jpg",
            "`02-restaurant.jpg`｜Mario Labò，热那亚San Pietro餐厅室内｜Casabella 117原刊扉页｜https://webapps.unitn.it/Biblioteca/it/Web/EngibankFile/1937%20Casabella%20%5Bperiodico%5D%20117.pdf",
            "`03-procida-plan.jpg`｜Bernard Rudofsky，Procida住宅平面与剖面｜Drawing Architecture研究论文｜https://riunet.upv.es/bitstreams/3b1f2c34-a750-4323-8ba4-b95a7af07ddc/download",
            "`04-procida-perspective.jpg`｜Bernard Rudofsky，Procida住宅外部透视｜Drawing Architecture研究论文｜https://riunet.upv.es/bitstreams/3b1f2c34-a750-4323-8ba4-b95a7af07ddc/download",
            "`05-airraid-plan.jpg`｜带气密前室的住宅防空掩体图，1943｜Momentothek Oberwart｜https://www.momentothek-oberwart.at/detail/2164-plan-zur-errichtung-eines-luftschutzraumes-mit-gasschleuse-fur-und-von-baumeister-michael-gaal-steinamangererstrasse-91",
            "`06-celbes-ad.jpg`｜Cel-Bes历史广告｜Giulia Favaretto博士论文图49｜https://amsdottorato.unibo.it/9062/1/favaretto_giulia_tesi.pdf",
            "`07-faesite-ad.jpg`｜Faesite历史广告｜Giulia Favaretto博士论文图49｜https://amsdottorato.unibo.it/9062/1/favaretto_giulia_tesi.pdf",
        ],
    },
    {
        "slug": "casabella-118",
        "issue": "CASABELLA 118",
        "date": "OTTOBRE 1937 · ANNO X",
        "date_cn": "1937年10月",
        "cover": "book-cover.jpg",
        "accent": "#4a8b8c",
        "question": "工业与医疗建筑，\n怎样摆脱纪念性？",
        "thesis_label": "流程  分区  构造性能",
        "thesis": "118期把现代建筑的价值放到工作与照护中：试验室以生产流程组织空间，婴儿医院以洁污分区、日照和独立流线取代纪念性正面。",
        "summary": "当建筑面对试验、治疗和婴儿照护，最重要的不再是正面像什么，而是流程是否清楚、互相冲突的人流是否分开、每个房间能否获得稳定光线，以及围护构造能否维持环境性能。",
        "concepts": ["流程生成平面", "分区阻断冲突", "构造稳定环境"],
        "takeaways": [
            "先画工作和照护流程，再让结构网格、开口和服务空间跟随它们落位。",
            "普通、传染、门诊、后勤和遗体路线必须独立，连接只发生在受控节点。",
            "连续阳台与保温吸声层不是附加装饰，而是医疗环境能否稳定工作的条件。",
        ],
        "publish_title": "118期｜功能如何取代纪念性",
        "publish_body": "Casabella 118把现代建筑的判断标准放到两类最不能含糊的空间里：工业试验室与婴儿医院。\n\nGiancarlo Palanti在Livorno试验室中让工作过程成为建筑的主线。样品接收、预处理、试验和记录需要连续前进，结构网格、采光带和设备区因此跟随流程安排。建筑的公共形象来自清楚的构造和真实工作，而不是给工厂套上纪念性正面。\n\nCesare Cattaneo、Vito Latis与Franco Longoni的婴儿医院则把卫生逻辑彻底转成平面：普通与传染病患各自形成独立单元，门诊、病房和员工区相互连接却不交叉；预防与咨询另设一翼；停尸房独立放在园地中，避免与治疗路线冲突。连续薄阳台为病房提供稳定日照、遮阳和受保护的户外过渡。\n\nMarescotti关于Cel-Bes的讨论补上构造层面：隔热和吸声必须连续通过墙、顶和节点，任何缝隙都会让性能中断。\n\n这一期最核心的观点是：现代性不是少装饰，而是让流程生成平面、让分区阻断冲突、让构造稳定环境。",
        "tags": "#Casabella #建筑杂志 #工业建筑 #医院设计 #医疗建筑 #建筑流线 #建筑构造 #现代建筑",
        "cards": [
            {
                "image": "02-lab-cover-crop.jpg",
                "mode": "photo",
                "accent": "#4a8b8c",
                "focal": (0.50, 0.50),
                "source": "Giancarlo Palanti｜Laboratorio prove a Livorno｜Casabella 118",
                "eyebrow": "观点 01｜工作逻辑取代纪念性正面",
                "title": "连续结构网格和水平采光带，直接表达试验室的工作尺度",
                "body": "立面不再模拟宫殿秩序，而是让柱距、楼层、设备和自然光留下真实痕迹。工业建筑的公共形象来自清楚、可读且能工作的构造。",
            },
            {
                "image": "03-lab-flow.png",
                "mode": "document",
                "accent": "#c65a3f",
                "source": "Giuseppe Pagano / Giancarlo Palanti｜Quando si incontrano due uomini moderni｜Casabella 118",
                "eyebrow": "观点 02｜试验流程生成平面",
                "title": "样品接收、预处理、试验与记录连续前进，减少回流和交叉",
                "body": "把设备最重、振动最大和需要稳定光线的环节分别定位，再用最短路线连接。结构网格服从工作顺序，平面自然获得清楚的层级。",
            },
            {
                "image": "04-hospital-model.jpg",
                "mode": "photo",
                "accent": "#71816f",
                "focal": (0.52, 0.48),
                "source": "C. Cattaneo / V. Latis / F. Longoni｜Ospedale tipo per lattanti｜Casabella 118",
                "eyebrow": "观点 03｜不同医疗功能形成独立体量",
                "title": "普通、传染、门诊与预防单元分开布置，只在受控节点连接",
                "body": "医院不是一栋被走廊填满的大楼。把风险和服务对象不同的单元拆开，可以分别控制入口、庭院、采光与人员配置，同时避免洁污路线相互穿越。",
            },
            {
                "image": "05-hospital-ward.jpg",
                "mode": "document",
                "accent": "#4a8b8c",
                "source": "C. Cattaneo / V. Latis / F. Longoni｜Ospedale tipo per lattanti｜Casabella 118",
                "eyebrow": "观点 04｜病房单元把照护距离压到最短",
                "title": "床位、护理点、清洗与卫生空间围绕短走廊组成可重复单元",
                "body": "每个病房组都有明确服务核心，护士不必穿越整层寻找设备。重复单元便于扩展，也让感染控制、清洁和日常观察获得稳定边界。",
            },
            {
                "image": "06-hospital-elevation.jpg",
                "mode": "document",
                "accent": "#c65a3f",
                "source": "C. Cattaneo / V. Latis / F. Longoni｜Ospedale tipo per lattanti｜Casabella 118",
                "eyebrow": "观点 05｜连续阳台是环境装置",
                "title": "薄阳台沿病房正面连续展开，同时提供日照、遮阳和户外过渡",
                "body": "阳台把病床与花园之间增加一层可控空间。上层板遮挡高角度夏季太阳，冬季低角度光线仍可深入，病患也能在保护下接触室外空气。",
            },
            {
                "image": "07-celbes-performance.png",
                "mode": "document",
                "accent": "#71816f",
                "source": "Franco Marescotti｜Isolazione termo-acustica a mezzo del Cel-Bes｜Casabella 118",
                "eyebrow": "观点 06｜性能必须连续穿过节点",
                "title": "空气胞腔减缓热与声音传递，接缝密封决定整面围护是否有效",
                "body": "保温和吸声不能只比较单块板材。墙角、楼板边、门窗洞口与固定件必须维持连续层；一个未处理的缝隙，就会成为热桥和声桥。",
            },
        ],
        "sources": [
            "`book-cover.jpg`｜Casabella 118官方历史封面｜Casabella官方档案｜https://casabellaweb.eu/wp-content/uploads/2010/04/118-nz.jpg",
            "`02-lab-cover-crop.jpg`｜Giancarlo Palanti，Livorno试验室外观｜Casabella 118官方封面原图局部｜https://casabellaweb.eu/wp-content/uploads/2010/04/118-nz.jpg",
            "`03-lab-flow.png`｜Livorno试验室的接收、准备、试验与记录流程｜信息依据Casabella 118目录及Giancarlo Palanti作品资料｜https://www.iuav.it/it/ateneo/archivio-progetti%E2%80%93petit-tour/74",
            "`04-hospital-model.jpg`｜Cesare Cattaneo、Vito Latis、Franco Longoni，Ospedale tipo per lattanti模型｜Archivio Cattaneo｜https://www.cesarecattaneo.com/ospedale-tipo-per-lattanti-1935-1936/",
            "`05-hospital-ward.jpg`｜Ospedale tipo per lattanti病房单元图｜Archivio Cattaneo｜https://www.cesarecattaneo.com/ospedale-tipo-per-lattanti-1935-1936/",
            "`06-hospital-elevation.jpg`｜Ospedale tipo per lattanti剖面与立面｜Archivio Cattaneo｜https://www.cesarecattaneo.com/ospedale-tipo-per-lattanti-1935-1936/",
            "`07-celbes-performance.png`｜Cel-Bes空气胞腔、连续铺设与节点密封｜信息依据Franco Marescotti《Isolazione termo-acustica a mezzo del Cel-Bes》｜Casabella 118",
        ],
    },
]


def save_rgb(image: Image.Image, path: Path) -> None:
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)


def crop_box(source: Path, target: Path, box: tuple[int, int, int, int], width: int = 1600) -> None:
    image = Image.open(source).convert("RGB").crop(box)
    if image.width < width:
        image = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.06)
    image = ImageEnhance.Sharpness(image).enhance(1.22)
    image.save(target, quality=96, subsampling=0)


def draw_roio_strategy(path: Path) -> None:
    image = Image.new("RGB", (1600, 1000), "#eee9df")
    draw = ImageDraw.Draw(image)
    draw.text((90, 70), "ROIO  山地儿童营", font=font(FONT_BOLD, 48), fill=INK)
    draw.text((90, 140), "弯折朝向  ·  连续寝室  ·  顶层通廊", font=font(FONT_SANS, 27), fill=MUTED)

    points = [(180, 670), (560, 480), (930, 545), (1410, 320)]
    draw.line(points, fill="#c65a3f", width=160, joint="curve")
    draw.line(points, fill="#f5f1e9", width=105, joint="curve")
    for x, y in [(340, 590), (730, 510), (1120, 455)]:
        draw.rectangle((x - 45, y - 45, x + 45, y + 45), fill="#3f7894")

    draw.arc((140, 140, 520, 520), 205, 335, fill="#d9a441", width=8)
    for x in range(260, 1390, 170):
        draw.line((x, 160, x - 120, 350), fill="#d9a441", width=5)
        draw.polygon([(x - 120, 350), (x - 93, 335), (x - 101, 370)], fill="#d9a441")

    draw.text((120, 820), "连续寝室带", font=font(FONT_BOLD, 31), fill=INK)
    draw.text((590, 820), "折点公共核心", font=font(FONT_BOLD, 31), fill=INK)
    draw.text((1110, 820), "向阳开放面", font=font(FONT_BOLD, 31), fill=INK)
    draw.line((115, 875, 1480, 875), fill="#bdb5a8", width=2)
    draw.text((120, 912), "轻微转折扩大冬季受光面，公共核心缩短集体移动距离", font=font(FONT_SERIF, 29), fill=MUTED)
    image.save(path, quality=96, subsampling=0)


def draw_lab_flow(path: Path) -> None:
    image = Image.new("RGB", (1600, 1000), BLUE)
    draw = ImageDraw.Draw(image)
    draw.text((86, 70), "LABORATORIO  工作序列", font=font(FONT_BOLD, 48), fill=LIGHT)
    draw.text((86, 142), "结构与采光跟随试验流程落位", font=font(FONT_SANS, 28), fill="#a8c5c8")
    labels = ["样品接收", "预处理", "试验", "记录"]
    colors = ["#4a8b8c", "#6fa5a4", "#c65a3f", "#d5a54b"]
    xs = [90, 460, 830, 1200]
    for i, (x, label, color) in enumerate(zip(xs, labels, colors)):
        draw.rounded_rectangle((x, 350, x + 280, 650), 18, fill=color)
        draw.text((x + 140, 500), f"0{i + 1}", font=font(FONT_BOLD, 74), fill=rgba(LIGHT, 120), anchor="mm")
        draw.text((x + 140, 595), label, font=font(FONT_BOLD, 34), fill=LIGHT, anchor="mm")
        if i < 3:
            draw.line((x + 292, 500, x + 350, 500), fill=LIGHT, width=7)
            draw.polygon([(x + 350, 500), (x + 326, 485), (x + 326, 515)], fill=LIGHT)
    draw.line((90, 760, 1480, 760), fill="#73899a", width=3)
    draw.text((90, 805), "重设备靠近结构核心", font=font(FONT_BOLD, 29), fill="#b8c8d4")
    draw.text((625, 805), "稳定采光沿连续外墙", font=font(FONT_BOLD, 29), fill="#b8c8d4")
    draw.text((1140, 805), "路线避免回流", font=font(FONT_BOLD, 29), fill="#b8c8d4")
    image.save(path, quality=96, subsampling=0)


def draw_celbes_performance(path: Path) -> None:
    image = Image.new("RGB", (1600, 1000), "#f0ece3")
    draw = ImageDraw.Draw(image)
    draw.text((88, 70), "CEL-BES  连续性能层", font=font(FONT_BOLD, 48), fill=INK)
    draw.text((88, 140), "空气胞腔减缓传递，节点密封阻断热桥与声桥", font=font(FONT_SANS, 28), fill=MUTED)

    draw.rectangle((640, 245, 960, 820), fill="#b87850")
    for row in range(7):
        for col in range(4):
            x = 690 + col * 72 + (row % 2) * 22
            y = 300 + row * 70
            draw.ellipse((x, y, x + 36, y + 36), fill="#ead7bd", outline="#6d4734", width=3)
    draw.rectangle((615, 220, 985, 845), outline="#334b5f", width=12)

    for y in (330, 470, 610):
        draw.arc((120, y - 95, 520, y + 95), 295, 65, fill="#3f7894", width=8)
        draw.arc((190, y - 70, 520, y + 70), 300, 60, fill="#3f7894", width=6)
        draw.line((520, y, 600, y), fill="#3f7894", width=6)
    draw.text((145, 785), "声音", font=font(FONT_BOLD, 32), fill="#3f7894")

    for y in (315, 455, 595, 735):
        draw.line((1030, y, 1390, y), fill="#c65a3f", width=7)
        draw.polygon([(1030, y), (1060, y - 18), (1060, y + 18)], fill="#c65a3f")
    draw.text((1180, 785), "热量", font=font(FONT_BOLD, 32), fill="#c65a3f")
    draw.text((650, 890), "接缝连续密封", font=font(FONT_BOLD, 34), fill=INK)
    image.save(path, quality=96, subsampling=0)


def prepare_assets(cfg: dict, src: Path) -> None:
    renders = ROOT / "tmp" / "renders-116-118"
    if cfg["slug"] == "casabella-116":
        crop_box(renders / "colonies-1.png", src / "02-exhibition-avenue.jpg", (0, 360, 1180, 1937))
        draw_roio_strategy(src / "03-roio-strategy.png")
        crop_box(renders / "colonies-3.png", src / "04-torre-balilla.jpg", (180, 135, 596, 445))
        crop_box(renders / "colonies-3.png", src / "05-calambrone.jpg", (688, 135, 1230, 447))
        crop_box(renders / "colonies-3.png", src / "06-le-navi.jpg", (688, 1307, 1230, 1636))
        crop_box(renders / "colonies-5.png", src / "07-marina-massa.jpg", (118, 135, 660, 485))
    elif cfg["slug"] == "casabella-117":
        crop_box(renders / "117front-1.png", src / "02-restaurant.jpg", (382, 345, 1410, 1590))
        crop_box(renders / "procida-8.png", src / "03-procida-plan.jpg", (100, 900, 455, 1370))
        crop_box(renders / "procida-9.png", src / "04-procida-perspective.jpg", (58, 140, 515, 760))
        crop_box(renders / "materials-89.png", src / "06-celbes-ad.jpg", (440, 378, 710, 682))
        crop_box(renders / "materials-89.png", src / "07-faesite-ad.jpg", (938, 378, 1205, 682))
    else:
        cover = Image.open(src / "book-cover.jpg").convert("RGB")
        crop = cover.crop((82, 143, 278, 196)).resize((1700, 900), Image.Resampling.LANCZOS)
        crop = ImageEnhance.Contrast(crop).enhance(1.12)
        crop = ImageEnhance.Sharpness(crop).enhance(1.35)
        crop.save(src / "02-lab-cover-crop.jpg", quality=96, subsampling=0)
        draw_lab_flow(src / "03-lab-flow.png")
        board = src / "02-hospital-board.jpg"
        crop_box(board, src / "04-hospital-model.jpg", (60, 95, 1335, 900))
        crop_box(board, src / "05-hospital-ward.jpg", (1330, 70, 1840, 705))
        crop_box(board, src / "06-hospital-elevation.jpg", (160, 875, 1660, 1270))
        draw_celbes_performance(src / "07-celbes-performance.png")


def make_cover_116(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(11601)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, 700, H), fill=rgba(BLUE))
    draw.text((62, 52), cfg["issue"], font=font(FONT_BOLD, 27), fill=LIGHT)
    draw.text((640, 58), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(LIGHT, 170), anchor="ra")
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
    mount(canvas, cover, (72, 176, 556, 710), True)
    draw.text((760, 95), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (760, 165), cfg["question"], 400, 470, 55, INK, serif=True, spacing=13)
    draw.rectangle((760, 720, 1140, 730), fill=accent)
    draw.text((760, 782), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (760, 845), cfg["thesis"], 400, 510, 33, INK, serif=True, spacing=14)
    draw_fit(draw, (72, 1220), "健康空间，也可能成为纪律空间。设计必须同时检查身体舒适与权力组织。", 560, 220, 36, LIGHT, serif=True, spacing=14)
    page_mark(draw, 1, True)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_cover_117(cfg: dict, src: Path, out: Path) -> Path:
    canvas = paper_canvas(11701)
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 280), fill=rgba(BLUE))
    draw.text((68, 52), cfg["issue"], font=font(FONT_BOLD, 27), fill=LIGHT)
    draw.text((1170, 58), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(LIGHT, 170), anchor="ra")
    draw.text((68, 125), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (68, 170), cfg["question"].replace("\n", " "), 1050, 90, 51, LIGHT, serif=True, spacing=8)
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
    mount(canvas, cover, (575, 335, 590, 740), True)
    draw.text((72, 385), cfg["thesis_label"], font=font(FONT_BOLD, 24), fill=accent)
    draw_fit(draw, (72, 455), cfg["thesis"], 440, 525, 37, INK, serif=True, spacing=15)
    draw.rounded_rectangle((72, 1190, 1170, 1480), 8, fill="#dfe7e8")
    draw_fit(draw, (112, 1250), "透明、庭院、防护与多孔材料，都在回答同一件事：环境怎样被空间主动调节。", 1010, 170, 42, BLUE, serif=True, spacing=13)
    page_mark(draw, 1, False)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_cover_118(cfg: dict, src: Path, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(BLUE))
    draw = ImageDraw.Draw(canvas)
    accent = cfg["accent"]
    draw.rectangle((0, 0, W, 1050), fill="#112f42")
    draw.text((66, 52), cfg["issue"], font=font(FONT_BOLD, 27), fill=LIGHT)
    draw.text((1172, 58), cfg["date"], font=font(FONT_SANS, 18), fill=rgba(LIGHT, 170), anchor="ra")
    cover = ImageEnhance.Sharpness(Image.open(src / cfg["cover"]).convert("RGB")).enhance(1.25)
    mount(canvas, cover, (70, 150, 640, 760), True)
    draw.text((780, 150), "单期主线", font=font(FONT_BOLD, 22), fill=accent)
    draw_fit(draw, (780, 225), cfg["question"], 385, 360, 55, LIGHT, serif=True, spacing=15)
    draw.line((780, 680, 1160, 680), fill=accent, width=9)
    draw.text((780, 735), cfg["thesis_label"], font=font(FONT_BOLD, 23), fill=accent)
    draw_fit(draw, (780, 800), cfg["thesis"], 390, 320, 32, LIGHT, serif=True, spacing=14)
    draw_fit(draw, (72, 1180), "功能不是削弱建筑表达，而是让结构、光线和流线获得更准确的表达。", 1080, 220, 46, LIGHT, serif=True, spacing=17)
    draw.text((72, 1518), "Casabella 118 · Ottobre 1937", font=font(FONT_SANS, 18), fill=rgba(LIGHT, 160))
    page_mark(draw, 1, True)
    path = out / "01.jpg"
    save_rgb(canvas, path)
    return path


def make_summary_116(cfg: dict, out: Path) -> Path:
    canvas = paper_canvas(11608)
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, False)
    accent = cfg["accent"]
    draw.text((72, 150), "从身体舒适到集体秩序", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (72, 220), cfg["summary"], 1080, 300, 47, INK, serif=True, spacing=17)
    y = 690
    colors = ["#c65a3f", "#3f7894", "#71816f"]
    for idx, (label, body, color) in enumerate(zip(cfg["concepts"], cfg["takeaways"], colors), 1):
        draw.rounded_rectangle((72, y, 1170, y + 190), 10, fill=color)
        draw.text((115, y + 44), f"0{idx}", font=font(FONT_BOLD, 34), fill=rgba(LIGHT, 150))
        draw.text((220, y + 42), label, font=font(FONT_BOLD, 34), fill=LIGHT)
        draw_fit(draw, (220, y + 98), body, 890, 70, 28, LIGHT, spacing=8)
        y += 235
    page_mark(draw, 8, False)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def make_summary_117(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), "#e9eeec")
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, False)
    accent = cfg["accent"]
    draw.text((72, 150), "环境控制的四个入口", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (72, 220), cfg["summary"], 1080, 300, 47, INK, serif=True, spacing=17)
    boxes = [
        (72, 680, 585, 1010, "视线", "开窗与家具共同决定观看方向", "#3f7894"),
        (657, 680, 1170, 1010, "气候", "庭院、阴影与开口调节微环境", "#71816f"),
        (72, 1060, 585, 1390, "安全", "最短路线、气密与备用出口", "#c65a3f"),
        (657, 1060, 1170, 1390, "声学", "孔隙、空腔与接缝控制混响", "#b28a45"),
    ]
    for x1, y1, x2, y2, title, body, color in boxes:
        draw.rounded_rectangle((x1, y1, x2, y2), 12, fill=color)
        draw.text((x1 + 34, y1 + 42), title, font=font(FONT_BOLD, 38), fill=LIGHT)
        draw.line((x1 + 34, y1 + 112, x2 - 34, y1 + 112), fill=rgba(LIGHT, 100), width=2)
        draw_fit(draw, (x1 + 34, y1 + 154), body, x2 - x1 - 68, 130, 30, LIGHT, serif=True, spacing=10)
    page_mark(draw, 8, False)
    path = out / "08.jpg"
    save_rgb(canvas, path)
    return path


def make_summary_118(cfg: dict, out: Path) -> Path:
    canvas = Image.new("RGBA", (W, H), rgba(BLUE))
    draw = ImageDraw.Draw(canvas)
    header(draw, cfg, 8, True)
    accent = cfg["accent"]
    draw.text((72, 150), "功能如何获得建筑表达", font=font(FONT_BOLD, 25), fill=accent)
    draw_fit(draw, (72, 220), cfg["summary"], 1080, 300, 47, LIGHT, serif=True, spacing=17)
    labels = ["流程生成平面", "分区阻断冲突", "构造稳定环境"]
    bodies = cfg["takeaways"]
    widths = [970, 810, 650]
    colors = ["#4a8b8c", "#c65a3f", "#71816f"]
    y = 710
    for idx, (label, body, width, color) in enumerate(zip(labels, bodies, widths, colors), 1):
        draw.rounded_rectangle((72, y, 72 + width, y + 115), 10, fill=color)
        draw.text((108, y + 57), f"0{idx}", font=font(FONT_BOLD, 31), fill=rgba(LIGHT, 150), anchor="lm")
        draw.text((205, y + 57), label, font=font(FONT_BOLD, 33), fill=LIGHT, anchor="lm")
        draw_fit(draw, (96, y + 145), body, 1040, 100, 29, rgba(LIGHT, 220), spacing=9)
        y += 255
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
                f"{number:02d} {card['source'].split('｜')[1]}：{card['title']}"
                for number, card in enumerate(cfg["cards"], 2)
            ],
            f"08 总结：{'、'.join(cfg['concepts'])}",
        ],
    }


def source_records(cfg: dict) -> str:
    rows = "\n".join(f"- {item}" for item in cfg["sources"])
    return f"# {cfg['issue'].title()} 图片来源\n\n{rows}\n"


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
        "casabella-116": make_cover_116,
        "casabella-117": make_cover_117,
        "casabella-118": make_cover_118,
    }[cfg["slug"]]
    summary_maker = {
        "casabella-116": make_summary_116,
        "casabella-117": make_summary_117,
        "casabella-118": make_summary_118,
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
