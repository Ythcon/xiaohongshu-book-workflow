#!/usr/bin/env python3
"""Validate a rendered six-card book or eight-card magazine package."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from PIL import Image


EXPECTED_SIZE = (1242, 1660)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    hashes: dict[str, list[str]] = {}

    total = 8 if (output / "08.jpg").exists() else 6
    for number in range(1, total + 1):
        path = output / f"{number:02d}.jpg"
        if not path.exists():
            errors.append(f"missing {path.name}")
            continue
        try:
            with Image.open(path) as image:
                if image.size != EXPECTED_SIZE:
                    errors.append(f"{path.name}: {image.size}, expected {EXPECTED_SIZE}")
                if image.mode != "RGB":
                    errors.append(f"{path.name}: mode {image.mode}, expected RGB")
        except Exception as exc:
            errors.append(f"{path.name}: cannot open ({exc})")
            continue
        hashes.setdefault(digest(path), []).append(path.name)

    duplicates = [names for names in hashes.values() if len(names) > 1]
    for names in duplicates:
        warnings.append("duplicate card files: " + ", ".join(names))

    preview = output / "preview.jpg"
    if not preview.exists():
        errors.append("missing preview.jpg")

    publish = output / "发布文案.md"
    sources = output / "图片来源.md"
    for path in (publish, sources):
        if not path.exists():
            errors.append(f"missing {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        if "[" in text and "]" in text:
            warnings.append(f"{path.name}: contains template placeholders")

    if publish.exists():
        text = publish.read_text(encoding="utf-8")
        for heading in ("标题", "正文", "标签"):
            if heading not in text:
                warnings.append(f"发布文案.md: missing {heading} section")
    if sources.exists():
        text = sources.read_text(encoding="utf-8")
        if not re.search(r"https?://", text):
            warnings.append("图片来源.md: no source URL found")
        if not re.search(r"CC BY|CC0|Public Domain|公有领域|版权", text, re.I):
            warnings.append("图片来源.md: no license/copyright record found")

    for warning in warnings:
        print("WARN", warning)
    for error in errors:
        print("ERROR", error)
    if errors:
        raise SystemExit(1)
    print(f"OK: {total} cards, preview, copy and source record found in {output}")


if __name__ == "__main__":
    main()
