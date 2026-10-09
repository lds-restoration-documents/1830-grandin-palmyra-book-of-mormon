#!/usr/bin/env python3
"""Render PDF pages into the inputs used for transcription.

The 1830 Book of Mormon is printed in a single full-width column, so each page is
cut into two overlapping horizontal crops (top and bottom) instead of four quadrants.

For each page N this writes, under <out>/:
  img/pNNNN_0_overview.jpg   whole page, low resolution (layout only)
  img/pNNNN_1_top.jpg        top half at 2x (overlaps the bottom half slightly)
  img/pNNNN_2_bottom.jpg     bottom half at 2x
  ocr/pNNNN.txt              the PDF's embedded (noisy) OCR text, if any

Requires: pypdfium2 and Pillow.

Usage:
  python3 tools/render_pages.py scan.pdf --out work               # all pages
  python3 tools/render_pages.py scan.pdf --out work --pages 1-16,302
  python3 tools/render_pages.py scan.pdf --out work --pages 40 --scale 4   # zoom for a doubtful spot
"""
import argparse
from pathlib import Path

import pypdfium2 as pdfium


def parse_pages(spec, total):
    if not spec:
        return list(range(1, total + 1))
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="path to the scan PDF")
    ap.add_argument("--out", default="work", help="output directory (default: ./work)")
    ap.add_argument("--pages", help="pages to render, e.g. 1-16,302 (default: all)")
    ap.add_argument("--scale", type=float, default=2, help="render scale for the crops (default: 2)")
    args = ap.parse_args()

    out = Path(args.out)
    (out / "img").mkdir(parents=True, exist_ok=True)
    (out / "ocr").mkdir(parents=True, exist_ok=True)

    doc = pdfium.PdfDocument(args.pdf)
    print(f"{len(doc)} pages in {args.pdf}")
    for n in parse_pages(args.pages, len(doc)):
        page = doc[n - 1]
        (out / "ocr" / f"p{n:04d}.txt").write_text(page.get_textpage().get_text_range())
        im = page.render(scale=args.scale).to_pil().convert("RGB")
        w, h = im.size
        my = h // 2
        pad = h // 20
        im.crop((0, 0, w, my + pad)).save(out / "img" / f"p{n:04d}_1_top.jpg", quality=85)
        im.crop((0, my - pad, w, h)).save(out / "img" / f"p{n:04d}_2_bottom.jpg", quality=85)
        im.resize((w // 3, h // 3)).save(out / "img" / f"p{n:04d}_0_overview.jpg", quality=70)


if __name__ == "__main__":
    main()
