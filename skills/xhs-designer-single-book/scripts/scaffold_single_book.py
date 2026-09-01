#!/usr/bin/env python3
"""Create the minimum editable skeleton for one designer / one book post."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--designer", required=True)
    parser.add_argument("--book", required=True)
    args = parser.parse_args()

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    data = {
        "designer": args.designer,
        "book": args.book,
        "edition": {"author_or_editor": "", "publisher": "", "year": "", "isbn": ""},
        "thesis": "",
        "concept_chain": [],
        "cards": [
            {"number": "01", "role": "problem cover", "headline": "", "evidence": "", "asset": ""},
            {"number": "02", "role": "mechanism", "headline": "", "evidence": "", "asset": ""},
            {"number": "03", "role": "evidence", "headline": "", "evidence": "", "asset": ""},
            {"number": "04", "role": "evidence", "headline": "", "evidence": "", "asset": ""},
            {"number": "05", "role": "evidence", "headline": "", "evidence": "", "asset": ""},
            {"number": "06", "role": "synthesis", "headline": "", "evidence": "", "asset": ""},
        ],
        "endcards": {
            "01": {"layout_rationale": "", "changed_variables": []},
            "06": {"layout_rationale": "", "changed_variables": []},
        },
        "transferable_methods": ["", "", ""],
        "sources": [],
    }
    post_json = output / "post.json"
    if not post_json.exists():
        post_json.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    publish = output / "发布文案.md"
    if not publish.exists():
        publish.write_text("# 标题\n\n# 正文\n\n# 标签\n", encoding="utf-8")

    sources = output / "图片来源.md"
    if not sources.exists():
        sources.write_text(
            "# 图片来源\n\n| 文件名 | 内容 | 作者/机构 | 来源 URL | 许可/版权 | 修改 |\n"
            "|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )

    print(f"Created single-book post skeleton: {output}")


if __name__ == "__main__":
    main()
