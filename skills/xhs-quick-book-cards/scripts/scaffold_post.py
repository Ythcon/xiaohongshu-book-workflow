#!/usr/bin/env python3
"""Create a minimal JSON-driven Xiaohongshu book or magazine workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", help="lowercase project slug")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--book", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--kind", choices=("book", "magazine"), default="book")
    parser.add_argument(
        "--system",
        choices=("signage", "anchoring", "event-grid"),
        default="anchoring",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def write_new(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite {path}; use --force")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    project = root / "posts" / args.slug
    assets = root / "assets" / args.slug
    output = root / "output" / args.slug
    assets.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)

    case_count = 6 if args.kind == "magazine" else 4
    config = {
        "slug": args.slug,
        "kind": args.kind,
        "book": args.book,
        "author": args.author,
        "version": "出版社｜年份｜ISBN",
        "system": args.system,
        "asset_dir": f"../../assets/{args.slug}",
        "output_dir": f"../../output/{args.slug}",
        "book_cover": "book-cover.jpg",
        "cover_background": "cover-background.jpg",
        "question": "用一个明确问题提出这本书",
        "thesis": "用一句可争论的命题概括全书，不超过四十字",
        "cases": [
            {
                "image": f"0{i}.jpg",
                "eyebrow": f"CASE 0{i}",
                "name": f"案例 {i}",
                "meta": "地点｜年份",
                "headline": "本页只写一个观点",
                "body": "说明这个案例怎样证明核心命题，控制在一至两句。",
                "focal": [0.5, 0.5],
            }
            for i in range(1, case_count + 1)
        ],
        "summary": {
            "statement": "一句总结：把书的命题转成读者可以带走的观察方法。",
            "concepts": ["概念一", "概念二", "概念三"],
            "takeaways": ["结论一", "结论二", "结论三"],
        },
    }
    write_new(
        project / "post.json",
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        args.force,
    )

    if args.kind == "magazine":
        sequence = "\n".join(["1. 单期主线观点或概念"] + [f"{i}. 主要文章或案例 {i - 1}" for i in range(2, 8)] + ["8. 总结归纳"])
        tag = "建筑杂志"
    else:
        sequence = "\n".join([
            "1. 问题式封面", "2. 核心机制", "3. 案例证据二",
            "4. 案例证据三", "5. 案例证据四", "6. 总结、概念链与三条结论",
        ])
        tag = "建筑书单"

    publish = f"""# 小红书发布文案｜《{args.book}》

## 标题

[问题或反常识命题，约 20 字]

## 正文

[核心问题 → 案例证据 → 可带走的方法 → 一个具体问题；300—500 字]

## 标签

#{args.book.replace(' ', '')} #{args.author.replace(' ', '')} #{tag} #建筑设计

## 组图顺序

{sequence}

## 版本与事实来源

[出版社、年份、ISBN、书目页和案例事实来源]
"""
    write_new(output / "发布文案.md", publish, args.force)

    source_rows = "\n".join(
        f"| {i:02d}.jpg |  |  |  |  | 裁切、调色、排版 |" for i in range(1, case_count + 1)
    )
    sources = f"""# 图片来源（内部记录）

| 文件名 | 画面内容 | 作者/机构 | 来源页 URL | 许可 | 修改 |
|---|---|---|---|---|---|
| book-cover.jpg | 正式书封 |  |  | 版权归原权利人 | 等比缩放 |
{source_rows}
"""
    write_new(output / "图片来源.md", sources, args.force)
    print(project / "post.json")
    print(assets)
    print(output)


if __name__ == "__main__":
    main()
