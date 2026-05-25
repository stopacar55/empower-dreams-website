#!/usr/bin/env python3
"""
Create a side-by-side composite image for a blog card thumbnail.

Use this when a post has exactly two unique images and you need a single
card thumbnail. Resizes both to a common height (default 500px), stitches
them horizontally, saves as JPEG.

Usage:
    python3 make_card_composite.py <left.jpg> <right.jpg> <out.jpg> [--height 500] [--quality 88]

If Pillow isn't installed:
    pip install pillow --break-system-packages
"""

import argparse
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run:", file=sys.stderr)
    print("  pip install pillow --break-system-packages", file=sys.stderr)
    sys.exit(2)


def make_composite(left_path: str, right_path: str, out_path: str,
                   target_height: int = 500, quality: int = 88) -> None:
    left = Image.open(left_path)
    right = Image.open(right_path)

    def resize_to_height(img: Image.Image) -> Image.Image:
        ratio = target_height / img.height
        return img.resize((int(img.width * ratio), target_height), Image.LANCZOS)

    left = resize_to_height(left)
    right = resize_to_height(right)

    composite = Image.new("RGB", (left.width + right.width, target_height), "white")
    composite.paste(left, (0, 0))
    composite.paste(right, (left.width, 0))
    composite.save(out_path, "JPEG", quality=quality)
    print(f"Wrote {out_path}: {composite.width}x{composite.height}px")


def main() -> int:
    parser = argparse.ArgumentParser(description="Side-by-side image composite for blog card thumbnails.")
    parser.add_argument("left", help="Path to the left image (typically <slug>-1.jpg)")
    parser.add_argument("right", help="Path to the right image (typically <slug>-2.jpg)")
    parser.add_argument("out", help="Output path (typically <slug>-card.jpg)")
    parser.add_argument("--height", type=int, default=500, help="Common height in pixels (default: 500)")
    parser.add_argument("--quality", type=int, default=88, help="JPEG quality 1-100 (default: 88)")
    args = parser.parse_args()

    make_composite(args.left, args.right, args.out, args.height, args.quality)
    return 0


if __name__ == "__main__":
    sys.exit(main())
