#!/usr/bin/env python3
"""Small Pillow utilities for custom single-book card renderers; no fixed layouts."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps

WIDTH, HEIGHT = 1242, 1660


def font_path(bold: bool = False) -> str:
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf" if bold else "C:/Windows/Fonts/simsun.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    raise FileNotFoundError("No supported CJK font found; pass a font path explicitly.")


def font(size: int, bold: bool = False, path: str | None = None) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path or font_path(bold), size=size)


def cover_crop(image: Image.Image, size: tuple[int, int], centering=(0.5, 0.5)) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=centering)


def contain(image: Image.Image, size: tuple[int, int], color=(245, 243, 238)) -> Image.Image:
    canvas = Image.new("RGB", size, color)
    fitted = ImageOps.contain(image.convert("RGB"), size, method=Image.Resampling.LANCZOS)
    canvas.paste(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
    return canvas


def wrap_text(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        current = ""
        for char in paragraph:
            trial = current + char
            if current and draw.textbbox((0, 0), trial, font=face)[2] > max_width:
                lines.append(current)
                current = char
            else:
                current = trial
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    max_width: int,
    spacing: int = 14,
) -> int:
    lines = wrap_text(draw, text, face, max_width)
    line_height = face.size + spacing
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += line_height
    return y


def save_card(image: Image.Image, path: str | Path) -> None:
    if image.size != (WIDTH, HEIGHT):
        raise ValueError(f"Card must be {(WIDTH, HEIGHT)}, got {image.size}")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "JPEG", quality=95, subsampling=0)


def make_preview(card_paths: Iterable[str | Path], output: str | Path, thumb_width: int = 360) -> None:
    paths = [Path(path) for path in card_paths]
    if len(paths) != 6:
        raise ValueError("Single-book preview requires exactly six cards")
    gap = 24
    thumb_height = round(thumb_width * HEIGHT / WIDTH)
    sheet = Image.new("RGB", (thumb_width * 3 + gap * 4, thumb_height * 2 + gap * 3), (225, 223, 218))
    for index, path in enumerate(paths):
        with Image.open(path) as source:
            thumb = source.convert("RGB").resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        x = gap + (index % 3) * (thumb_width + gap)
        y = gap + (index // 3) * (thumb_height + gap)
        sheet.paste(thumb, (x, y))
    sheet.save(output, "JPEG", quality=92, subsampling=0)
