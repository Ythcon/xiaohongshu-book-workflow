---
name: xhs-quick-book-cards
description: Rapidly create production-ready Xiaohongshu posts for architecture, urbanism, design, and art books or magazines. Use six cards for books and eight cards for magazine issues, with 3:4 JPG cards, preview, publish copy, and image-source records. Use when Codex must turn a book or magazine issue, thesis, articles, cases, cover, and sourced images into a coherent Chinese graphic post; batch-generate notes; or revise an existing package while minimizing research and prompt tokens.
---

# 小红书建筑书与杂志图文快制

用“一个命题 + 一种视觉操作 + 一条证据链”完成可发布图文。优先复用素材、来源记录和已有生成脚本，不重新研究已核验的信息。

## 类型路由

- `book`：固定六页。01问题封面；02核心机制；03—05案例证据；06总结。
- `magazine`：固定八页。01单期主线观点或概念；02—07主要文章或案例介绍；08总结归纳。
- 杂志内页优先使用原刊图、原始插图、项目照片或项目图纸。纯排版和自制关系图只在没有合适原图时补位，不能成为主体。

## 快速路径

1. 检查当前项目中的书封、案例图、`manifest.json`、`图片来源.md`、发布文案和生成脚本。
2. 缺素材时只补齐：核验封面、1 张可选封面背景；书籍补4张案例图，杂志补6张文章或案例图。01与末页不预设固定构图；总结页可纯排版，也可使用与总结命题直接相关的合法素材。AI背景不能含文字或伪造建筑。
3. 把全书压成一句可争论的核心命题；禁止只写“作者 × 书名”。
4. 选择一个系统：
   - `signage`：城市、传播、符号、速度、日常文化。
   - `anchoring`：场地、材料、光、身体、关系。
   - `event-grid`：概念、规则、程序、运动、事件。
5. 若项目已有相近生成器，复制最接近的脚本并只改内容配置。否则运行 `scripts/scaffold_post.py`，填好 `post.json` 后运行 `scripts/render_post.py`。
6. 书籍生成`01.jpg`—`06.jpg`；杂志生成`01.jpg`—`08.jpg`；同时生成`preview.jpg`、`发布文案.md`、`图片来源.md`。
7. 运行 `scripts/validate_post.py <成品目录>`；再人工查看 `preview.jpg`。

## 固定规格（非固定版式）

- 画布：1242×1660，3:4，RGB JPG，质量 95。
- 书籍页序：01问题封面；02核心机制；03—05案例证据；06总结。
- 杂志页序：01单期主线；02—07主要文章或案例；08总结。
- 只固定01与末页的信息职责，不固定构图。不得连续复用同一套封面落点、标题框、概念标签和结论面板。
- 每页只讲一个观点；内页使用不同案例图；书封只出现在 01。
- 案例照片保持清楚，不在照片上叠装饰性矢量；文字、网格、箭头只承担组织功能。
- AI 只可生成封面背景或辅助底图；所有可读文字由排版脚本添加。
- 核验后的真实书封必须作为锁定图层等比缩放，禁止 AI 重绘、改字、换版本。
- 不要伪造引语。编辑性概括的性质写进发布文案或内部记录，不在图片上出现“非原刊引语”“非原始图纸”“关系示意”等制作过程说明。
- 图片上的出处只写读者需要的信息：`作者名｜项目名或文章标题｜期号/页码`；摄影师署名可放在同一行或图源记录中。

## 01与末页的变化规则

- 01根据核心命题重新决定视觉入口。至少改变以下三项：主视觉占比、留白方向、封面尺度与位置、问题标题轴线、作者/版本信息位置、底图与信息面板关系。
- 06或08根据结论类型重新组织阅读顺序。至少改变以下三项：总结句权重、概念链方向、结论分组方式、编号系统、底图/纯排版选择、结尾标注位置。
- 变化必须解释命题，不能只随机换位。系列一致性由字体、色彩、线型和信息语气维持，不靠复制相同模板。
- `render_post.py`只提供快速骨架。交付前必须对照同批套图检查01与末页；若缩略图结构近似，就修改生成器或单独重排，不直接交付默认构图。

## 对外内容规则

- 每页主标题必须直接输出一个建筑、空间或设计观点，让粉丝无需理解整理过程也能获得知识。
- 优先写：场地如何生成形式、程序如何组织空间、动线如何连接活动、材料或光线如何影响体验、公共空间如何成立。
- 禁止把整理动作、编辑策略、研究方法、配图原则或出处规范写成成品观点，例如“建立杂志判断轴线”“先找编辑主线”“图片承担叙事”。这些只进入内部文档。
- 08总结必须归纳本期可迁移的建筑与设计概念，不总结制作流程。

## 内容压缩规则

先产出这 8 项再出图，不写长篇研究报告：

```text
书名｜作者｜版本
核心问题（18 字内）
核心命题（40 字内）
视觉系统（signage / anchoring / event-grid）
书籍案例 1—4 / 杂志文章或案例 1—6：名称｜事实｜证明什么
总结句（55 字内）
三条结论（每条 35 字内）
发布标题（20 字左右，问题或反常识命题）
```

不确定事实先核验；无法核验时删掉，不用模糊措辞填空。文案默认 300—500 中文字，结尾只留一个具体问题，标签 6—10 个。

## 三组参考的使用原则

三组作品是“论点转译方法”，不是表面风格包。需要选择系统、调整版式或生成提示词时读取 [visual-systems.md](references/visual-systems.md)。禁止把霓虹、红色网格或水彩场地线无理由套在任何书上。

## 图源与发布检查

需要搜图、核验书封、写署名或发布文案时读取 [sources-and-qa.md](references/sources-and-qa.md)。如果素材目录已有 `manifest.json` 或 `图片来源.md`，直接复用并只检查缺口。

## 工具

```powershell
# 创建最小项目骨架
python scripts/scaffold_post.py <slug> --root <工作目录> --book "书名" --author "作者" --system anchoring

# 填写 <工作目录>/posts/<slug>/post.json 后生成
python scripts/render_post.py <工作目录>/posts/<slug>/post.json

# 验证文件、尺寸、文案与图源记录
python scripts/validate_post.py <工作目录>/output/<slug>
```

渲染器是快速骨架，不是固定封面与总结页模板。若用户提供明确参考或当前仓库已有更成熟的同主题脚本，以用户要求和现有视觉系统为准，并保留固定规格与图源规则。
