from generate_casabella_101_102_cards import render_issue


ISSUES = [
    {
        "slug": "casabella-104",
        "big_number": "104",
        "issue": "CASABELLA 104",
        "date": "AGOSTO 1936 · ANNO IX",
        "cover": "book-cover.jpg",
        "question": "展览中的住宅原型，\n如何变成\n日常生活？",
        "thesis_label": "原型 × 模数 × 居住",
        "thesis": "第六届米兰三年展把住宅当作可验证的空间系统：尺度、家具与日常动作必须在同一套秩序中协同。",
        "summary": "104 期的重点不是把住宅做成展品，而是把展览变成一次居住实验：从单间尺度出发，推向可复制的住房与公共生活。",
        "concepts": ["居住原型", "模数系统", "日常动作"],
        "takeaways": [
            "住宅设计先处理人的动作，再决定房间、家具与设备的关系。",
            "模数不是视觉风格，而是让不同房间和构件能够协同工作的尺度工具。",
            "展览真正有价值的地方，是把抽象的生活方式变成可观察、可比较的空间。",
        ],
        "cards": [
            {
                "image": "02-albini-room.png", "mode": "document", "accent": "#ea6c36",
                "source": "Franco Albini｜Stanza per un uomo｜VI Triennale di Milano｜Casabella 104",
                "eyebrow": "观点 01｜房间从动作开始",
                "title": "一间房先安排人的动作，再安排家具",
                "body": "Albini把单人房拆成睡眠、工作与收纳几组动作，家具不再是孤立物件，而是组织身体移动的空间骨架。",
            },
            {
                "image": "03-albini-section.jpg", "mode": "document", "accent": "#71816f",
                "source": "Franco Albini｜Alloggio per quattro persone｜VI Triennale｜Casabella 104",
                "eyebrow": "观点 02｜剖面组织生活",
                "title": "住宅的效率藏在剖面，而不只在平面",
                "body": "连续剖面把厨房、起居和睡眠分成不同高度，视线、采光与收纳因此获得层次，有限面积也能容纳多种生活节奏。",
            },
            {
                "image": "04-albini-camera.jpg", "mode": "document", "accent": "#ea6c36",
                "source": "Franco Albini｜Camera matrimoniale, alloggio per quattro persone｜VI Triennale｜Casabella 104",
                "eyebrow": "观点 03｜私密性靠界面",
                "title": "卧室不靠厚墙封闭，而靠层次建立安静",
                "body": "床、半高隔断和储物界面共同形成缓冲带；居住者获得私密性，同时仍与整个住宅保持视觉和空气联系。",
            },
            {
                "image": "05-adami-camera.jpg", "mode": "document", "accent": "#ea6c36",
                "source": "Adami / Masera｜Camera per un ragazzo｜VI Triennale di Milano｜Casabella 104",
                "eyebrow": "观点 04｜儿童房是成长空间",
                "title": "房间要允许身体变化，而不是固定一种姿势",
                "body": "可移动家具与清楚的活动边界让儿童房同时容纳学习、休息和游戏；空间不预设唯一用途，而支持成长中的变化。",
            },
            {
                "image": "06-bbpr-section.png", "mode": "document", "accent": "#71816f",
                "source": "Banfi / Belgiojoso / Peressutti / Rogers｜Modello abitativo BBPR｜VI Triennale｜Casabella 104",
                "eyebrow": "观点 05｜标准化不等于单一",
                "title": "同一套结构，也能容纳不同的家庭生活",
                "body": "BBPR用重复构件建立基本秩序，再用隔断、家具和开口调整使用方式；标准化提供底盘，差异来自生活本身。",
            },
            {
                "image": "07-sironi-dining.jpg", "mode": "photo", "accent": "#ea6c36", "focal": (0.5, 0.5),
                "source": "Mario Sironi｜Sala da pranzo｜VI Triennale di Milano｜Casabella 104",
                "eyebrow": "观点 06｜餐桌制造公共性",
                "title": "公共生活从一张可共享的桌子开始",
                "body": "餐厅不只是摆放家具的房间；桌面、照明与围合关系把个人用餐转化为家庭和邻里可以共享的日常场景。",
            },
        ],
    },
    {
        "slug": "casabella-105",
        "big_number": "105",
        "issue": "CASABELLA 105",
        "date": "SETTEMBRE 1936 · ANNO IX",
        "cover": "book-cover.jpg",
        "question": "现代建筑的\n新技术，如何\n改变空间经验？",
        "thesis_label": "结构 × 展览 × 经验",
        "thesis": "105 期把现代建筑放进展览、工业和住宅的连续谱中：技术只有转化为空间经验，才真正改变建筑。",
        "summary": "105 期关心的不是新形式本身，而是新技术如何改变观看、行走、居住与城市公共性的方式。",
        "concepts": ["技术转译", "空间经验", "公共事件"],
        "takeaways": [
            "结构和材料的进步，必须通过人的行走、观看和停留才成为建筑经验。",
            "展览建筑不是背景，它把新的生活方式提前变成可被公众体验的事件。",
            "现代住宅的开放性来自连续界面、光线和流动，而不是简单地减少墙体。",
        ],
        "cards": [
            {
                "image": "02-melnikov-pavilion.jpg", "mode": "photo", "accent": "#ea6c36", "focal": (0.5, 0.5),
                "source": "Konstantin Melnikov｜Pavillon de l’URSS, Paris 1925｜Casabella 105",
                "eyebrow": "观点 01｜结构本身就是展览",
                "title": "斜向楼梯把观看变成连续运动",
                "body": "梅尔尼科夫用穿插的楼梯和桁架制造方向变化；观众不是站在展品前，而是在结构中不断改变观看位置。",
            },
            {
                "image": "03-exposition-postcard.jpg", "mode": "photo", "accent": "#ea6c36", "focal": (0.5, 0.5),
                "source": "Exposition internationale des Arts décoratifs｜Paris 1925｜Casabella 105",
                "eyebrow": "观点 02｜展览制造城市想象",
                "title": "展览把技术变成一座城市的公共景观",
                "body": "临时建筑、灯光和交通共同构成展览城市；新材料不只服务于单栋建筑，也重新安排公众的观看路径。",
            },
            {
                "image": "04-melnikov-house.jpg", "mode": "photo", "accent": "#71816f", "focal": (0.5, 0.52),
                "source": "Konstantin Melnikov｜Melnikov House, Moscow｜Casabella 105",
                "eyebrow": "观点 03｜住宅是实验室",
                "title": "住宅可以用几何组织光线与私密",
                "body": "两个相交圆柱和蜂巢窗洞让结构、采光与居住尺度互相咬合；住宅因此成为一套持续试验的空间装置。",
            },
            {
                "image": "05-melnikov-garage.jpg", "mode": "photo", "accent": "#ea6c36", "focal": (0.5, 0.5),
                "source": "Konstantin Melnikov｜Intourist Garage｜Casabella 105",
                "eyebrow": "观点 04｜工业空间需要流线",
                "title": "车库的核心不是容积，而是转向关系",
                "body": "连续结构和清晰入口让车辆、工人和设备拥有不同流线；工业建筑的秩序来自运动被准确安排。",
            },
            {
                "image": "06-neutra-vdl.jpg", "mode": "photo", "accent": "#71816f", "focal": (0.5, 0.5),
                "source": "Richard Neutra｜VDL Studio and Residences｜Casabella 105",
                "eyebrow": "观点 05｜开放性来自连续界面",
                "title": "玻璃、平台与花园把住宅推向户外",
                "body": "Neutra用连续窗带、露台和镜面水景消解室内外边界；现代住宅的自由来自光线和视线的连续流动。",
            },
            {
                "image": "07-fontana-camerlata.jpg", "mode": "photo", "accent": "#ea6c36", "focal": (0.5, 0.5),
                "source": "Cesare Cattaneo / Mario Radice｜Fontana di Camerlata｜Casabella 105",
                "eyebrow": "观点 06｜公共艺术改变尺度",
                "title": "重复圆环把交通节点变成城市地标",
                "body": "卡梅拉塔喷泉以重复圆环建立远距离识别，也以水、阴影和人的尺度激活广场；公共艺术因此参与城市组织。",
            },
        ],
    },
    {
        "slug": "casabella-106",
        "big_number": "106",
        "issue": "CASABELLA 106",
        "date": "OTTOBRE 1936 · ANNO IX",
        "cover": "book-cover.jpg",
        "question": "住宅、家具与\n公共设施，如何\n组成完整生活？",
        "thesis_label": "居住 × 家具 × 公共设施",
        "thesis": "106 期把住宅从单个房间推向完整生活系统：家具、社区设施与城市公共空间必须同时被设计。",
        "summary": "106 期的住宅观不止于平面布局，而是把家具、儿童活动、公共设施与城市尺度放进同一套生活框架。",
        "concepts": ["身体尺度", "家具系统", "社区生活"],
        "takeaways": [
            "家具不是装修末端，而是决定动作、收纳和空间分区的建筑构件。",
            "住宅单元只有与公共设施、道路和邻里关系连接，才会成为真正的居住环境。",
            "可重复的构件要服务于不同生活，而不是把每个家庭压缩成同一种模板。",
        ],
        "cards": [
            {
                "image": "02-albini-kitchen.jpg", "mode": "document", "accent": "#ea6c36",
                "source": "Franco Albini｜Sezione cucina e studio, alloggio per quattro persone｜VI Triennale｜Casabella 106",
                "eyebrow": "观点 01｜家具是空间构件",
                "title": "厨房把家务动作编进住宅骨架",
                "body": "Albini把厨房、学习和收纳放进同一条剖面关系；家具既划分功能，也让家务劳动保持可见、可达和连续。",
            },
            {
                "image": "03-bbpr-model.jpg", "mode": "document", "accent": "#71816f",
                "source": "Banfi / Belgiojoso / Peressutti / Rogers｜Alloggio BBPR｜Mostra dell’Abitazione｜Casabella 106",
                "eyebrow": "观点 02｜单元要连接社区",
                "title": "住宅单元的边界，不能切断邻里生活",
                "body": "BBPR通过半公共的入口、共享的结构和可调整隔断，把单个家庭放进更大的邻里网络。",
            },
            {
                "image": "04-camera-singola.jpg", "mode": "document", "accent": "#ea6c36",
                "source": "Franco Albini｜Camera singola, alloggio per quattro persone｜VI Triennale｜Casabella 106",
                "eyebrow": "观点 03｜剖面连接不同年龄",
                "title": "单人房也要容纳独处与联系",
                "body": "床、桌面和储物被压缩进清楚的界面，独处获得边界，视线和空气仍能与住宅其他部分保持联系。",
            },
            {
                "image": "05-kitchen.jpg", "mode": "document", "accent": "#71816f",
                "source": "Franco Albini｜Cucina, alloggio per quattro persone｜VI Triennale｜Casabella 106",
                "eyebrow": "观点 04｜厨房也是生活空间",
                "title": "厨房不是后勤角落，而是家庭共同体",
                "body": "清楚的操作台、储物和通行边界让厨房同时承担制作、交流与照料；生活的公共性从家务空间开始。",
            },
            {
                "image": "06-dining-alt.jpg", "mode": "photo", "accent": "#ea6c36", "focal": (0.5, 0.5),
                "source": "Mario Sironi｜Sala da pranzo（另一视图）｜VI Triennale di Milano｜Casabella 106",
                "eyebrow": "观点 05｜家具组织共同体",
                "title": "餐厅的尺度决定家庭如何相遇",
                "body": "桌面、座椅和照明共同控制停留时间与交流方向；家具系统把家庭成员的相遇变成可持续的日常秩序。",
            },
            {
                "image": "07-albini-studio.jpg", "mode": "document", "accent": "#71816f",
                "source": "Franco Albini｜Studio, alloggio per quattro persone｜VI Triennale｜Casabella 106",
                "eyebrow": "观点 06｜工作也属于住宅",
                "title": "家庭住宅必须容纳工作、学习与休息",
                "body": "工作台、书架和采光被纳入住宅基本单元；生活不再被切成互不相干的房间，而由连续的活动链组成。",
            },
        ],
    },
]


if __name__ == "__main__":
    for issue in ISSUES[:2]:
        render_issue(issue)
    from generate_casabella_106_reset import ISSUE as RESET_106
    render_issue(RESET_106)
