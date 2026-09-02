# 小红书建筑书与杂志图文 Skills

> 将一本经过核验的建筑 / 设计书籍，或一期建筑杂志，整理成有清晰命题、连续图卡、发布文案和可追溯图源记录的小红书内容包。

## 预览

以下是本项目实际生成的两类成品示例：

| 建筑大师书籍 | 建筑杂志专题 |
| --- | --- |
| ![建筑大师书籍图卡预览](previews/architecture-book-example.jpg) | ![建筑杂志图卡预览](previews/architecture-magazine-example.jpg) |
| 《Ten Canonical Buildings》：问题 → 机制 → 案例 → 总结 | PIN–UP 40《Independence》：单期主线 → 文章 / 案例 → 总结 |

## 两个 Skill

### [`xhs-designer-single-book`](skills/xhs-designer-single-book/SKILL.md)

把一位建筑师、设计师或设计理论家的**一本书**整理成六页完整叙事：

- 锁定准确书目、版本和真实书封
- 提炼一个可解释、可讨论的核心命题
- 选择四个案例、图纸、段落或档案证据
- 生成 6 张 3:4 JPG、预览图、发布文案、图源记录和 `post.json`

适合理论书、访谈、宣言、方法论、档案和设计思想类书籍。不处理杂志、多书比较或设计师排行榜。

### [`xhs-quick-book-cards`](skills/xhs-quick-book-cards/SKILL.md)

用固定的信息职责快速制作建筑书籍或建筑杂志图文：

- 书籍：6 页，01 问题封面，02 核心机制，03–05 案例证据，06 总结
- 杂志：按期号内容组织单期主线、文章 / 案例与总结
- 复用已核验的书封、案例图片、来源记录和生成配置
- 生成 3:4 JPG、预览图、发布文案、图源记录和结构化 JSON

## 适用场景

- “把这本建筑理论书做成小红书图文”
- “把这期 PIN–UP 或其他建筑杂志拆成一套卡片”
- “围绕一个建筑概念整理几个项目案例”
- “修改已有图卡，但保留来源、页序和发布文案结构”

不适用于纯图片拼贴、没有可靠来源的事实扩写、无人审核的自动发布，或一次性处理大量互不相关的主题。

## 输入

开始前准备以下信息，缺失时先核验再写作：

```text
书籍：书名、作者 / 建筑师、版本或出版社
杂志：刊名、期号、日期、主编（如有）
内容：书籍核心问题，或杂志单期主题
素材：真实书封、项目照片、图纸、原刊页或机构资料
```

选题前先检查 [`book_registry.json`](book_registry.json) 与 [`已做书单.md`](已做书单.md)。书名命中即更换；如果要求未提过的建筑师，设计师命中也视为重复。

## 输出

每套内容遵循以下交付契约：

```text
output/<slug>/
├── 01.jpg ... 06.jpg    # 书籍；杂志为 01.jpg ... 08.jpg
├── preview.jpg          # 整套卡片预览
├── 发布文案.md           # 标题、正文、话题与发布备注
├── 图片来源.md           # 图片出处、许可证、页码或链接
└── post.json            # 命题、案例、页序与布局信息
```

完整案例包可以保留 4–6 个案例；实际上传时按主题选择其中少量案例即可，不需要把全部内容一次上传。

## 工作流

```text
核验选题
  → 研究书目、论点与案例
  → 检索图片并记录来源 / 权利状态
  → 压缩为一个核心命题
  → 组织 6 页书籍或按期号定制杂志叙事
  → 生成 1242 × 1660 的 3:4 JPG
  → 运行验证脚本并人工查看预览
  → 整理发布文案，按需选择案例发布
```

### 内容规则

- 每页只承担一个建筑、空间或设计观点。
- 01 负责建立问题和身份，末页负责总结可迁移的方法。
- 案例图片必须清楚，不能用装饰性图形遮挡主体。
- 真实书封等比缩放，不重绘、不改字、不换版本。
- 不伪造引语；编辑性概括要明确是概括或转述。
- 图片来源至少记录作者 / 机构、来源 URL、许可证或版权状态和修改方式。

### 视觉规则

- 画布固定为 1242 × 1660 px、RGB、3:4 JPG、质量 95。
- 系列感由字体、颜色、线型和信息语气维持，不复制同一套封面模板。
- 01 与末页需要根据命题改变主视觉比例、留白方向、标题轴线或总结结构。
- AI 只能辅助生成无文字的背景或底图；所有可读文字由排版脚本完成。

## 使用方式

### 单本建筑大师书籍

```powershell
cd skills/xhs-designer-single-book
python scripts/scaffold_single_book.py <output-directory> --designer "建筑师" --book "书名"
# 填写 post.json、发布文案和图片来源后
python scripts/validate_single_book.py <output-directory>
```

### 建筑书籍或杂志快速制作

```powershell
cd skills/xhs-quick-book-cards
python scripts/scaffold_post.py <slug> --root <工作目录> --book "书名 / 期号" --author "作者 / 主编" --system anchoring
# 填写 posts/<slug>/post.json 后
python scripts/render_post.py <工作目录>/posts/<slug>/post.json
python scripts/validate_post.py <工作目录>/output/<slug>
```

两个 Skill 都保留自动发现能力；只有在用户明确提出相应任务时才调用对应 Skill。

## 仓库结构

```text
.
├── skills/
│   ├── xhs-designer-single-book/   # 单本建筑大师书籍
│   └── xhs-quick-book-cards/       # 建筑书籍与杂志快速图卡
├── previews/                       # GitHub 首页展示用的少量预览图
├── book_registry.json              # 选题查重登记
├── 已做书单.md                     # 可读版书目清单
└── 封面来源规范.md                 # 书封与来源检查规则
```

生产过程中的原始下载资料、完整素材库和临时生成目录不放在公开仓库；公开仓库只保留最终 Skill、必要参考文档、验证脚本、登记资料和少量示例预览。
