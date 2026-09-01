#!/usr/bin/env python3
"""Validate one designer / one book Xiaohongshu package."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image

EXPECTED_SIZE = (1242, 1660)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for number in range(1, 7):
        path = output / f"{number:02d}.jpg"
        if not path.exists():
            errors.append(f"missing {path.name}")
            continue
        try:
            with Image.open(path) as image:
                if image.size != EXPECTED_SIZE:
                    errors.append(f"{path.name}: expected {EXPECTED_SIZE}, got {image.size}")
                if image.mode != "RGB":
                    errors.append(f"{path.name}: expected RGB, got {image.mode}")
        except Exception as exc:
            errors.append(f"{path.name}: cannot open ({exc})")

    for name in ("preview.jpg", "发布文案.md", "图片来源.md", "post.json"):
        if not (output / name).exists():
            errors.append(f"missing {name}")

    publish = output / "发布文案.md"
    if publish.exists():
        text = publish.read_text(encoding="utf-8")
        for heading in ("标题", "正文", "标签"):
            if heading not in text:
                warnings.append(f"发布文案.md: missing {heading} section")

    sources = output / "图片来源.md"
    if sources.exists():
        text = sources.read_text(encoding="utf-8")
        if not re.search(r"https?://", text):
            warnings.append("图片来源.md: no source URL")
        if not re.search(r"CC BY|CC0|Public Domain|公有领域|版权|许可", text, re.I):
            warnings.append("图片来源.md: no license/copyright record")

    post = output / "post.json"
    if post.exists():
        try:
            data = json.loads(post.read_text(encoding="utf-8"))
            cards = data.get("cards", [])
            if len(cards) != 6:
                errors.append(f"post.json: expected 6 cards, got {len(cards)}")
            for number in ("01", "06"):
                endcard = data.get("endcards", {}).get(number, {})
                if not endcard.get("layout_rationale"):
                    warnings.append(f"post.json: {number} has no layout_rationale")
                if len(endcard.get("changed_variables", [])) < 3:
                    warnings.append(f"post.json: {number} needs at least 3 changed_variables")
        except Exception as exc:
            errors.append(f"post.json: invalid JSON ({exc})")

    for warning in warnings:
        print("WARN", warning)
    for error in errors:
        print("ERROR", error)
    if errors:
        raise SystemExit(1)
    print(f"OK: six-card single-book package found in {output}")


if __name__ == "__main__":
    main()
