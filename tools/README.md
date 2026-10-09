# tools

The scripts and instructions used to produce the files in this repository. The page files in
`../book-of-mormon-1830-pages/` are the source of truth; the combined text files are generated from them.
(Adapted from the tooling in the sibling `1828-phinney-cooperstown-bible` repo.)

## Pipeline

1. **Render the scan** (needs the scan PDF, which is not in this repo, and `pip install pypdfium2 pillow`):
   `python3 tools/render_pages.py "Book of Mormon 1830.pdf" --out work [--pages 1-16,302] [--scale 4]`
   writes a top and a bottom crop, a low-resolution overview and the PDF's own noisy OCR text (if any) for each page.
2. **Transcribe**: AI agents (Claude) read the crops and write one `page-NNN.md` per page following
   [transcription-spec.md](transcription-spec.md). Pages may then be audited against the scan per
   [audit-spec.md](audit-spec.md). This step is done by agents, not by a script.
3. **Rebuild the combined files** from the page files (Python 3, standard library only; run from anywhere):
   ```
   python3 tools/compile_markdown.py     # -> book-of-mormon-1830.md
   python3 tools/make_plaintext.py       # -> book-of-mormon-1830.txt        (from book-of-mormon-1830.md)
   python3 tools/make_sparse.py          # -> book-of-mormon-1830-sparse.txt (from book-of-mormon-1830.md)
   ```
   Each script writes to the repo root by default; `--out` redirects the output. Run in that order.

## Notes on the scripts

- `compile_markdown.py` strips comments, running heads, footers and any marginal-notes section, and rejoins paragraphs
  that run across a page break. The join is driven by the `<!-- cont -->` marker the transcriber puts at the start of a
  continued paragraph (the 1830 text has long paragraphs and no verse numbers, so punctuation heuristics are not reliable).
  It aborts if a `<!-- cont -->` has no paragraph to continue.
- `make_sparse.py` keeps only the PDF page ranges in `PAGE_RANGES`: the title page (PDF 5, translated from the plates) and the Book of
  Mormon text (PDF 9–592). On the title page the 1830 imprint paragraphs (author, printer, place, year; `IMPRINT_PREFIXES`) are dropped. The title-page
  verso, Preface, testimonies and library notes are left out.
- Differences from the Phinney tooling: single-column pages (two crops, not four), no verses, no marginal notes, no reference letters,
  no tables-specific or Apocrypha logic.

## Review app

`review/review_app.py` (standard library only; `pypdfium2` and `pillow` are needed to show the scan) is a small local web app for working
through `../../review-checklist.md`: it shows each item beside the scan, lets you confirm it, edit the text on the spot or skip it,
saves your decisions to `../../review-decisions.json`, and can rebuild the three combined files. Run `python3 tools/review/review_app.py`
and open http://127.0.0.1:8765. `proofread-spec.md` and `audit-spec.md` are the instructions the proofreading and auditing agents followed.

## Typo catalog

`make_typo_catalog.py` (standard library only) builds `../printer-typos.md`: it finds each form in a curated list of printer's typos and misspellings in `../book-of-mormon-1830.md` and writes its PDF page, printed page and context, so the catalog stays in sync with the text. The list of forms (and the spellings deliberately left out, such as `shew`) is in the script; run `python3 tools/make_typo_catalog.py`.
