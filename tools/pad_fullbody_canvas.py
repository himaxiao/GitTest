#!/usr/bin/env python3
"""半身图向下留白，供 ComfyUI 图生图补全身。

用法:
  python tools/pad_fullbody_canvas.py 输入.png [输出.png] [高度倍数]

默认高度倍数 1.75，宽高对齐到 16 的倍数。
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


def pad_down(src: Path, dst: Path, scale: float = 1.75) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    new_h = ((int(h * scale) + 15) // 16) * 16
    new_w = ((w + 15) // 16) * 16

    bottom = im.crop((0, max(0, h - 8), w, h)).convert("RGB")
    pixels = list(bottom.getdata())
    avg = tuple(sum(c[i] for c in pixels) // len(pixels) for i in range(3))

    canvas = Image.new("RGBA", (new_w, new_h), avg + (255,))
    x = (new_w - w) // 2
    canvas.paste(im, (x, 0), im)
    canvas.convert("RGB").save(dst, "PNG")
    print(f"{w}x{h} -> {new_w}x{new_h}")
    print(f"saved: {dst}")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + "_向下留白.png")
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.75
    pad_down(src, dst, scale)


if __name__ == "__main__":
    main()
