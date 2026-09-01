from generate_casabella_101_102_cards import render_issue


ISSUE = {
    "slug": "casabella-106",
    "big_number": "106",
    "issue": "CASABELLA 106",
    "date": "OTTOBRE 1936 · ANNO IX",
    "cover": "book-cover.jpg",
    "question": "从竞技场到住宅，\n建筑如何\n组织身体？",
    "thesis_label": "运动 × 游戏 × 居住",
    "thesis": "106 期把体育中心、永久游戏场和现代住宅放在同一条线上：建筑首先要组织身体的运动、观看和停留。",
    "summary": "106 期的核心不是住宅单元本身，而是身体如何被建筑组织：运动场形成公共仪式，游戏场安排日常活动，住宅把这些尺度带回生活。",
    "concepts": ["身体运动", "公共仪式", "日常居住"],
    "takeaways": [
        "大型体育建筑不是单纯容纳观众，而是把集体运动转化为可观看的公共事件。",
        "游戏场把儿童活动放进城市秩序，公共设施因此成为日常生活的组成部分。",
        "现代住宅从家具和家务动作开始，把运动、停留与交流带回身体尺度。",
    ],
    "cards": [
        {
            "image": "02-original-frontispiece.jpg", "mode": "document", "accent": "#ea6c36",
            "source": "Casabella 106｜原刊 frontespizio／目录页｜Ottobre 1936",
            "eyebrow": "观点 01｜本期从身体出发",
            "title": "运动、游戏与居住，共同决定建筑尺度",
            "body": "106 期目录并置柏林体育中心、永久游戏场和现代住宅展；建筑不再只是外壳，而是安排身体运动与公共生活的秩序。",
        },
        {
            "image": "03-reichsportfeld-aerial.jpg", "mode": "photo", "accent": "#ea6c36", "focal": (0.5, 0.52),
            "source": "Attilio Podestà｜Il centro sportivo del Reich a Berlino｜Casabella 106",
            "eyebrow": "观点 02｜体育中心是地形",
            "title": "大型体育场不是看台，而是身体运动的地形",
            "body": "环形看台、入口和运动场共同形成连续地形；观众的抵达、观看和离场被纳入建筑整体，而不是留在场外。",
        },
        {
            "image": "04-reichsportfeld-1936.jpg", "mode": "photo", "accent": "#71816f", "focal": (0.5, 0.52),
            "source": "Attilio Podestà｜Reichssportfeld Berlin，1936｜Casabella 106",
            "eyebrow": "观点 03｜集体运动制造仪式",
            "title": "连续台阶把集体运动组织成公共仪式",
            "body": "重复的座席、清晰的轴线和巨大的开敞面，让个体观看被转化为集体经验；建筑在这里负责安排共同的时间和视线。",
        },
        {
            "image": "07-triennale-games.jpg", "mode": "photo", "accent": "#ea6c36", "focal": (0.5, 0.5),
            "source": "G. Mazzoleni / Giulio Minoletti｜VI Triennale: Il campo permanente di giuochi｜Casabella 106",
            "eyebrow": "观点 04｜游戏场进入城市",
            "title": "儿童活动不是附属设施，而是公共空间的核心",
            "body": "永久游戏场把运动、观看和停留放进日常路径；城市公共性不只发生在广场，也发生在儿童可以自由使用的场地。",
        },
        {
            "image": "02-albini-kitchen.jpg", "mode": "document", "accent": "#ea6c36",
            "source": "Raffaello Giolli｜VI Triennale: La mostra dell’abitazione moderna｜Casabella 106",
            "eyebrow": "观点 05｜现代住宅从动作开始",
            "title": "厨房把家务动作编进住宅骨架",
            "body": "展览中的住宅模型把厨房、学习和收纳放进同一条空间关系；家具不是装饰，而是把身体动作组织成连续日常。",
        },
        {
            "image": "06-barabino-theatre.jpg", "mode": "photo", "accent": "#71816f", "focal": (0.5, 0.5),
            "source": "C. Corradi dell’Acqua｜Disegni inediti di Carlo Barabino｜Teatro Carlo Felice｜Casabella 106",
            "eyebrow": "观点 06｜历史图纸仍能组织当代观看",
            "title": "古典秩序不是静止遗产，而是可重新阅读的空间结构",
            "body": "Barabino 的剧院以轴线、门廊和层叠体量组织进入与观看；重新阅读历史图纸，能看到公共建筑如何控制人的移动。",
        },
    ],
}


if __name__ == "__main__":
    render_issue(ISSUE)
