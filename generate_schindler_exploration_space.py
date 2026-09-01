#!/usr/bin/env python3
"""Render ten Xiaohongshu cards for R. M. Schindler: An Exploration of Space."""
from __future__ import annotations
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import generate_three_unmentioned_masters as base

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "schindler-exploration-space"
OUTPUT = ROOT / "output" / "schindler-exploration-space"
W, H = 1242, 1660
P = {"paper":(235,230,215), "ink":(35,34,32), "terracotta":(183,76,53), "teal":(55,105,103), "orange":(227,150,73), "sage":(149,165,136), "white":(252,250,243), "muted":(106,99,91)}
BOOK = {
    "designer":"R. M. 辛德勒", "designer_en":"RUDOLPH M. SCHINDLER", "book":"Schindler: An Exploration of Space", "book_cn":"《辛德勒：空间的探索》", "edition":"James Steele｜TASCHEN, 2017｜ISBN 9783836564366",
    "question":"墙，为什么可以\n不把人隔开？", "thesis":"墙不只用来封闭房间；它也能转向视线、引出庭院，并把生活拆成相互渗透的片段。", "publish_title":"辛德勒：墙为何不必隔开人？",
    "publish_body":"《Schindler: An Exploration of Space》让人重新认识一件常被误会的事：辛德勒并不是把住宅做成“更开放”的盒子，而是把墙、屋顶、庭院与家具当成连续的空间切片。它们会挡住视线，也会把人带去下一个停留点。\n\n1922 年的辛德勒—切斯住宅以混凝土墙和庭院组织两组家庭与工作室；洛弗尔海滩住宅用连续的框架、挑台和高侧窗把海景、日照与居住层层接通；普韦布洛里贝拉公寓则以转角、露台、壁炉和厚墙，让小户型在相邻而不互相暴露之间取得平衡。\n\n对设计师真正有用的顺序是：先写出需要既分开又联系的两种活动；再让一面墙承担转向、遮挡或框景中的一个动作；最后在交界处安排能停留的台阶、窗边、露台或壁炉。\n\n空间的丰富不靠把墙全部拿掉，而靠每一段边界都决定下一步怎样被看见、走近和使用。本文为基于书籍与案例资料的编辑性阅读，不是原书逐字引语。",
    "tags":"#RMSchindler #辛德勒 #SpaceArchitecture #加州现代主义 #住宅设计 #空间边界 #建筑书单 #设计方法",
}
CASES = [
    ("1922", "辛德勒—切斯住宅｜庭院", "先有共同的院子，\n再有各自的房间", "两组家庭与工作室围绕共享庭院展开。墙没有把生活彻底分成两半，而是让私密与共处在不同方向上彼此可见。", "02-kings-road-court.jpg", (0.48,0.50)),
    ("1922", "辛德勒—切斯住宅｜墙体", "一面墙，也可以同时做三件事", "混凝土墙限定尺度、承接屋顶，也把视线折向院子。边界并非最后加上的围护，而是最早开始组织生活的构件。", "03-kings-road-wall.jpg", (0.50,0.50)),
    ("1926", "洛弗尔海滩住宅｜全景", "框架先拉开关系，\n房间随后出现", "连续混凝土框架把地面、起居层和海景拉成一条竖向链。住宅不是一层层盒子叠加，而是被结构与露台串联的剖面。", "04-lovell-wide.jpg", (0.50,0.47)),
    ("1926", "洛弗尔海滩住宅｜起居", "高侧窗不是采光补丁，\n而是视线的转向器", "高侧窗让光越过邻近边界进入起居空间，同时把视线抬向天空。墙与屋顶在此共同调节明暗、私密和方向。", "05-lovell-living.jpg", (0.50,0.50)),
    ("1923", "普韦布洛里贝拉公寓｜转角", "转角不必封死，\n它能制造下一段空间", "厚重墙体在转角处拉开，露出相邻路径与庭院。小尺度住宅因而不靠大开间取胜，而靠连续转向延长体验。", "06-pueblo-corner.jpg", (0.50,0.50)),
    ("1923", "普韦布洛里贝拉公寓｜露台", "把停留点放在边界上", "壁炉、露台与墙体汇到一起，室内外不靠透明玻璃混成一片，而是在可停留的界面上发生交换。", "07-pueblo-terrace.jpg", (0.50,0.50)),
    ("1922", "辛德勒—切斯住宅｜外部起居区", "住宅可以像营地，\n让生活绕着共享外部展开", "同一历史实景的另一处裁切显示，墙、遮棚和庭院共同构成一种半室外生活。建筑的核心不是客厅，而是不同生活节奏能并置的外部房间。", "02-kings-road-court.jpg", (0.18,0.50)),
    ("1922", "辛德勒—切斯住宅｜光影细部", "光落在墙上，\n墙才真正有厚度", "同一组实拍的细部裁切让材质、缝隙和光影被放大。墙不再只是平面轮廓，也带进了相邻空间的存在。", "03-kings-road-wall.jpg", (0.82,0.50)),
]

def save(image:Image.Image,path:Path):
    path.parent.mkdir(parents=True,exist_ok=True); image.convert("RGB").save(path,"JPEG",quality=95,subsampling=0,optimize=True)
def wall(draw, box, color, width=18):
    x0,y0,x1,y1=box; draw.line((x0,y0,x1,y0,x1,y1),fill=color,width=width,joint="curve")
def cover_card():
    im=Image.new("RGB",(W,H),P["paper"]); d=ImageDraw.Draw(im)
    d.rectangle((0,0,330,H),fill=P["terracotta"]); d.rectangle((330,0,W,164),fill=P["teal"])
    d.text((54,62),"01 / SPACE IS A MEDIUM",font=base.get_font(22,bold=True),fill=P["white"])
    d.text((371,56),BOOK["designer_en"],font=base.get_font(34,bold=True),fill=P["white"])
    cover=Image.open(ASSETS/"cover.png").convert("RGB"); base.paste_cover(im,cover,(58,220,420,1105),shadow=True)
    wall(d,(500,222,1122,497),P["terracotta"],20); wall(d,(610,620,1122,934),P["teal"],18); wall(d,(500,947,919,1162),P["orange"],17)
    y=base.text_block(d,(480,270),BOOK["question"],base.get_font(65,bold=True),P["ink"],650,4)
    base.text_block(d,(482,y+28),BOOK["thesis"],base.get_font(29),P["muted"],590,12)
    d.rounded_rectangle((60,1235,1170,1435),radius=14,fill=P["ink"])
    d.text((94,1272),"SCHINDLER · AN EXPLORATION OF SPACE",font=base.get_font(28,bold=True),fill=P["orange"])
    base.text_block(d,(94,1320),BOOK["edition"],base.get_font(24),P["white"],920,10)
    d.text((480,1513),"转向 / 停留 / 渗透",font=base.get_font(31,bold=True),fill=P["terracotta"])
    base.draw_page_mark(d,1,P["ink"]); return im
def panel(source,size,focus):
    source=ImageEnhance.Contrast(source.convert("RGB")).enhance(1.04); source=ImageEnhance.Color(source).enhance(.88)
    return ImageOps.fit(source,size,Image.Resampling.LANCZOS,centering=focus)
def case_card(case,page):
    year,title,headline,body,asset,focus=case; im=Image.new("RGB",(W,H),P["paper"]); d=ImageDraw.Draw(im)
    photo_left=page%2==0; pw=670; px=0 if photo_left else W-pw; im.paste(panel(Image.open(ASSETS/asset),(pw,H),focus),(px,0))
    d.rectangle((px+(pw-19 if photo_left else 0),0,px+(pw if photo_left else 19),H),fill=P["terracotta"])
    tx=736 if photo_left else 66; width=420 if photo_left else 465
    d.text((tx,82),year,font=base.get_font(30,bold=True),fill=P["terracotta"])
    base.text_block(d,(tx,132),title,base.get_font(29,bold=True),P["teal"],width,6)
    y=base.text_block(d,(tx,215),headline,base.get_font(49,bold=True),P["ink"],width,4)
    base.text_block(d,(tx,y+28),body,base.get_font(28),P["ink"],width,13)
    wall(d,(tx,1030,tx+width-18,1310),P["sage"],12)
    d.rounded_rectangle((px+42,1518,px+304,1562),radius=22,fill=P["ink"])
    d.text((px+65,1526),"真实建筑项目照片",font=base.get_font(18,bold=True),fill=P["white"])
    base.draw_page_mark(d,page,P["ink"],light=not photo_left); return im
def summary_card():
    im=Image.new("RGB",(W,H),P["teal"]); d=ImageDraw.Draw(im)
    d.text((68,62),"10 / MAKE WALLS DO WORK",font=base.get_font(24,bold=True),fill=P["orange"])
    y=base.text_block(d,(68,122),"不要删掉墙，\n让它安排下一步",base.get_font(67,bold=True),P["white"],960,5)
    base.text_block(d,(72,y+22),"辛德勒的墙是连续的空间动作：遮挡、转向、框景，再把人带到能停留的交界处。",base.get_font(29),P["paper"],980,12)
    # A three-room plan rather than the last two sets' bands / icons.
    rooms=[(72,568,580,902,P["terracotta"],"01  遮挡","先保留一个不被一眼看尽的角落。"),(602,735,1168,1068,P["orange"],"02  转向","用墙的折角把行走带到下一个空间。"),(200,1097,913,1430,P["sage"],"03  停留","在边界上安排窗边、台阶或露台。")]
    for x0,y0,x1,y1,color,head,body in rooms:
        d.rectangle((x0,y0,x1,y1),fill=color); d.rectangle((x0+18,y0+18,x1-18,y1-18),outline=P["ink"],width=5)
        d.text((x0+35,y0+40),head,font=base.get_font(35,bold=True),fill=P["white"] if color!=P["sage"] else P["ink"])
        base.text_block(d,(x0+35,y0+109),body,base.get_font(28),P["white"] if color!=P["sage"] else P["ink"],x1-x0-70,11)
    d.line((580,735,602,735),fill=P["paper"],width=10); d.line((553,902,553,1097),fill=P["paper"],width=10)
    d.text((68,1532),"基于书籍与八张真实项目照片的编辑性总结",font=base.get_font(21),fill=(205,219,208))
    base.draw_page_mark(d,10,P["white"],light=True); return im
def preview(paths):
    canvas=Image.new("RGB",(1242,654),P["ink"])
    for i,path in enumerate(paths): canvas.paste(ImageOps.fit(Image.open(path).convert("RGB"),(210,280),Image.Resampling.LANCZOS),(24+(i%5)*234,24+(i//5)*304))
    save(canvas,OUTPUT/"preview.jpg")
def docs(paths):
    manifest=json.loads((ASSETS/"manifest.json").read_text(encoding="utf-8")); copy=f"{BOOK['publish_title']}\n\n{BOOK['publish_body']}\n\n{BOOK['tags']}\n"; (OUTPUT/"发布文案.md").write_text(copy,encoding="utf-8")
    lines=["# 图片来源","","本套共 10 张：01 为问题封面，02–09 为真实项目照片，10 为编辑性总结。","书封使用 TASCHEN 对应版本图，等比缩放；建筑图片均为真实照片，未使用 AI 生成图片。08、09 为 02、03 原始实拍的不同细部裁切，以分别阅读外部起居与光影墙体。",""]
    for item in manifest: lines += [f"## {item['filename']}｜{item['content']}","",f"- 作者/机构：{item['credit']}",f"- 来源：{item['source_url']}",f"- 授权：{item['license']}",f"- 处理：{item['modifications']}",""]
    (OUTPUT/"图片来源.md").write_text("\n".join(lines),encoding="utf-8")
    post={"title":BOOK["publish_title"],"book":BOOK["book"],"edition":BOOK["edition"],"card_count":10,"dimensions":[W,H],"format":"JPEG RGB quality 95","visual_system":"room-slices: walls as spatial actions","cover_policy":"publisher-verified cover, proportional scaling only, no redraw","cards":[{"page":1,"file":"01.jpg","role":"question_cover","layout":"vertical verified cover set inside intersecting wall field"},*[{"page":i+2,"file":f"{i+2:02d}.jpg","role":"real_case_evidence","project":c[1],"year":c[0],"image":c[4]} for i,c in enumerate(CASES)],{"page":10,"file":"10.jpg","role":"synthesis","layout":"three-room plan"}],"copy":copy,"source_manifest":str((ASSETS/"manifest.json").relative_to(ROOT))}
    (OUTPUT/"post.json").write_text(json.dumps(post,ensure_ascii=False,indent=2),encoding="utf-8")
def validate(paths):
    cards=[]
    for path in paths:
        with Image.open(path) as image:
            rgb=image.convert("RGB"); cards.append({"file":path.name,"size":list(rgb.size),"mode":rgb.mode,"nonblank":any(a!=b for a,b in rgb.getextrema())})
    required=all((OUTPUT/name).exists() for name in ("preview.jpg","发布文案.md","图片来源.md","post.json")); report={"pass":len(paths)==10 and required and len(BOOK["publish_title"])<=20 and all(c["size"]==[W,H] and c["mode"]=="RGB" and c["nonblank"] for c in cards),"title_length":len(BOOK["publish_title"]),"body_length":len(BOOK["publish_body"].replace("\n","")),"required_files":required,"cards":cards}; (OUTPUT/"qa-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(report,ensure_ascii=False,indent=2))
def main():
    OUTPUT.mkdir(parents=True,exist_ok=True); images=[cover_card(),*[case_card(case,i+2) for i,case in enumerate(CASES)],summary_card()]; paths=[]
    for i,image in enumerate(images,1): path=OUTPUT/f"{i:02d}.jpg"; save(image,path); paths.append(path)
    preview(paths); docs(paths); validate(paths)
if __name__=="__main__": main()
