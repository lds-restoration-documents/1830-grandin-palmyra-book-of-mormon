#!/usr/bin/env python3
"""Build the sparse plain-text file (Book of Mormon text only) from book-of-mormon-1830.md.

Keeps book titles, chapter headings and paragraphs from the PDF page ranges that
hold the Book of Mormon proper. Drops everything outside those ranges (cover,
title page, preface, testimonies, blank pages, anything added after) and any
paragraph that is only an end marker such as FINIS.

The compiled Markdown carries <!-- page NNN --> markers, which this script uses
to decide what is in range. PAGE_RANGES is specific to the scan (PDF page
numbers, not printed folios): see transcription-notes.md §1.

Usage:  python3 tools/make_sparse.py [--md FILE] [--out FILE] [--verbose]
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Inclusive PDF page ranges that hold Book of Mormon text: PDF 9 (1 Nephi, printed p. 1) through
# PDF 592 (end of Moroni, "THE END,"). The Preface (7-8) and the testimonies (593-594) are outside it.
PAGE_RANGES = [(9, 592)]

END_MARKERS = re.compile(r'\*?(THE END[.,]?|FINIS[.,]?)\*?', re.I)


def in_range(pg):
    return pg is not None and any(a <= pg <= b for a, b in PAGE_RANGES)


def annotate(md_text):
    """Split into paragraphs, each tagged with the PDF page it starts on."""
    page = None
    items = []
    for p in md_text.split('\n\n'):
        ms = re.findall(r'<!-- page (\d+) -->', p)
        clean = re.sub(r'\s*<!-- page \d+ -->\s*', ' ', p).strip()
        if ms and p.startswith('<!-- page'):
            page = int(ms[0])
        if clean:
            items.append((page, clean))
        if ms and not p.startswith('<!-- page'):
            page = int(ms[-1])
    return items


def plain(l):
    l = l.replace('**', '').replace('*', '')
    l = re.sub(r'^#{1,6}[ \t]+', '', l)
    l = re.sub(r'</?[a-zA-Z][^>]*>', '', l)
    return re.sub(r'(?<=\S) {2,}(?=\S)', ' ', l).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=str(ROOT / 'book-of-mormon-1830.md'))
    ap.add_argument('--out', default=str(ROOT / 'book-of-mormon-1830-sparse.txt'))
    ap.add_argument('--verbose', action='store_true', help='list the paragraphs that were dropped')
    args = ap.parse_args()

    if not PAGE_RANGES:
        raise SystemExit('PAGE_RANGES is empty: set the Book of Mormon page ranges at the top of this script first.')

    items = annotate(Path(args.md).read_text(encoding='utf-8'))
    kept, dropped = [], []
    for pg, p in items:
        if in_range(pg) and not END_MARKERS.fullmatch(p.strip()):
            kept.append(p)
        else:
            dropped.append((pg, p))
    text = '\n\n'.join(q for q in (plain(p) for p in kept) if q) + '\n'
    text = re.sub(r'\n{3,}', '\n\n', text)
    Path(args.out).write_text(text, encoding='utf-8')
    print(f'kept {len(kept)} paragraphs, dropped {len(dropped)}, {len(text.split())} words -> {args.out}')
    if args.verbose:
        for pg, p in dropped:
            print(pg, p[:70])


if __name__ == '__main__':
    main()
