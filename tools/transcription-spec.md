# Transcription spec — 1830 E. B. Grandin (Palmyra) Book of Mormon

These are the instructions for the transcribing agents, one batch of pages at a time.
`<WORKDIR>` is the directory produced by `tools/render_pages.py`.

Inputs for PDF page N (NNNN = 4-digit zero-padded) in `<WORKDIR>`:
- `img/pNNNN_0_overview.jpg`: whole page, low-res (layout only)
- `img/pNNNN_1_top.jpg`, `img/pNNNN_2_bottom.jpg`: readable crops of the top and bottom of the page
  (they overlap in the middle; do not duplicate lines that appear in both)
- `ocr/pNNNN.txt`: noisy OCR draft of the same page, if the PDF has one. Use it only as a helper; the IMAGE is authoritative.

Output: `book-of-mormon-1830-pages/page-NNN.md` (3-digit zero-padded PDF page number, e.g. `page-021.md`).
Page numbers are PDF page numbers, not the printed folios.

Procedure per page: read the overview, then both crops, then the OCR draft; write the corrected text.
Read carefully; accuracy matters more than speed. Transcribe exactly what is printed: 1830 spelling, punctuation,
capitalization, abbreviations (`&c.`), run-together or split words, and the very sparse punctuation of the 1830 text.
Words split across lines by a hyphen are JOINED into the whole word; words hyphenated in the original stay hyphenated.
The edition has no verse numbers and no marginal notes. Do not add either.

## Markdown format

```
<!-- PDF page NNN -->
**Header:** THE BOOK OF NEPHI. | 17        <- running head as printed, parts separated by " | " (omit line if none)

# THE FIRST BOOK OF NEPHI.               <- book titles as #, with any printed subtitle as plain or italic text as printed

## CHAPTER II.                           <- chapter headings as ##

AND it came to pass that ...             <- one paragraph per printed paragraph (blank line between)

---

Footer: B                                <- printer's signature mark, catchword or folio not already in the Header (omit if none)
```

Rules:
- One markdown paragraph per printed paragraph. A printed paragraph starts with an indented first line; text that merely wraps is the same paragraph.
- **Paragraphs across page breaks.** If the first paragraph on the page is the continuation of a paragraph begun on the previous page, start that line with `<!-- cont -->` (e.g. `<!-- cont --> ly went on ...`). `tools/compile_markdown.py` uses this marker to rejoin the paragraph. Do not put it on a paragraph that starts on the page. If the page ends mid-paragraph, write the fragment; the next page carries the marker.
- Keep the printed capitalization of paragraph openings, which often start with all-caps or a large initial ("AND it came to pass"). Write the full first word.
- Italic type is `*italic*`; check carefully for it. Small caps printed as capitals are written as capitals.
- Headings: write the book title, chapter heading and any subtitle as printed.
- **Decorative rules.** A thick decorative rule (dinkus) is printed above each chapter heading after the first in a book. Record it with the comment `<!-- thick decorative rule (dinkus) printed above the chapter heading -->` on its own line directly above the `## CHAPTER` line. Other ornaments in margins are noted briefly in a comment, not transcribed.
- **Chapter summaries.** The first chapter of a book (and others) opens with a printed summary ("An account of Lehi and his wife Sariah…"). It is set in italics: write it as one italic paragraph (`*…*`) directly under the chapter heading, keeping its spelling and punctuation.
- **Running heads.** Most pages have a running head with the book name (small caps, write as capitals) and the printed page number, the number on the left on even-numbered pages and on the right on odd ones: `**Header:** 6 | FIRST BOOK OF NEPHI.` / `**Header:** FIRST BOOK OF NEPHI. | 7`. Pages that open a book (title, subtitle, chapter heading) have no running head and no `Header:` line.
- **Printed page number = PDF page − 4** in the main text (PDF 10 prints "6", PDF 63 prints "59"; the Preface is iii–iv on PDF 7–8, and 1 Nephi opens on PDF 9 = printed p. 5, where no number is shown). This is only a cross-check: always record the number as it appears in the scan.
- **Spacing before punctuation.** The type has a thin space before `;`, `:`, `?` and `!` in many places, but it is typesetting, not text, and it cannot be judged reliably at this size. Write NO space before `; : ? !` (`life; and`, `saying: Blessed`). All the punctuation marks themselves, their order, and the capital after a colon are kept exactly as printed.
- **Text cut off by the scan edge.** If the scan itself trims the page (as on the title-page verso, PDF 6) write the visible fragment of each line exactly as it appears (`the`, `get t`, `Clerk of the Northern District of New-Yor`), never complete it from memory of the text, and say so in a comment at the top of the page. Do not use `[illegible]` for text that is simply cut off. Keep a clipped letter if about half or more of it is visible and drop a mere sliver; a word that is only partly clipped but still readable is written whole. Put a comment at the top of the page saying which edge is trimmed.
- **A new book opening mid-page.** Put the dinkus comment above the book title, then the `# THE SECOND BOOK OF NEPHI.`-style title, `## CHAPTER I.` and the italic summary. The page keeps the running head of the book it started in; note that in a comment. A rule is recorded only where it is actually printed: a chapter heading at the very top of a page often has none, so write no dinkus comment there.
- **Front and back matter, covers, bookplates, endpapers, notices.** Describe the physical item briefly in an HTML comment (what it is, colours, layout) and transcribe any legible printed text under it, as plain lines. Handwritten annotations, shelfmarks and library stamps are described in the comment only, not transcribed as text. A page with nothing to read is just the page comment and a one-line description. The title page is written as stacked lines in the printed order and capitalization, with a layout comment (centering, type sizes, rules); a display word split at a line end is joined (`MOR-/MON` becomes `MORMON`).
- **Hyphens at a line end that split an already hyphenated word or compound.** Let the printing decide: if the same word appears mid-line elsewhere in the page files (grep for it), follow that; names keep their own hyphens (`Maher-shalal-hash-baz`). If nothing settles it, close the word up and add a one-line comment only when the break is truly ambiguous.
- **Small caps versus ordinary type.** Opening words in small caps (`AND`, `THE`) are written in capitals; a word that is merely capitalized in ordinary type is written with its printed case (`And now`). Check the scan before choosing.
- **Specks and blemishes.** Foxing, ink specks, worn or filled-in type and stray dots near the trim edge are not text. A mark that does not read as a deliberate punctuation mark or letter is ignored: do not transcribe it and do not add a comment (e.g. a speck after a comma, "seen,."). Use `<!-- uncertain: … -->` only when a real mark or letter is in doubt (is it a comma or a period? an e or an o?).
- **Comma versus period when the mark is uncertain.** Use the gap after the mark and the case of the next word: more space and a capitalized word = period; less space and a lowercase word = comma (an educated guess for uncertain marks only; a mark that is plainly one or the other is written as it is). See `tools/proofread-spec.md` for the full rule.
- **Flush-left versus indented.** Decide whether the first line of the page is indented (new paragraph) or flush-left (continuation of the previous page's paragraph, which may begin a new sentence). Mark a flush-left first line with `<!-- cont -->` even when the previous page ended with a full stop.
- **Hyphens at the end of a page.** If the last line ends in a hyphenated word break, keep the hyphen (`vis-`) on this page and begin the next page with `<!-- cont --> ions …`; `compile_markdown.py` closes the word up. Hyphens at the end of a line inside the page are joined by the transcriber.
- Preliminary and closing matter (title page, preface, testimonies of the witnesses, contents, errata, endpapers): transcribe as printed with sensible markdown; center or layout-only features are noted in an HTML comment.
- Footer items (signature marks, catchwords, printed page numbers if not in the Header) go on a `Footer:` line after a `---` rule.
- Covers, endpapers, library stamps, bookplates, blank pages, marginalia and pencil notes: describe briefly in an HTML comment and transcribe any legible text.
- Do not add commentary, summaries, or modern corrections. If a word is truly illegible write `[illegible]`.

## Addenda

Never silently "correct" a reading to what you think it should be, whether from knowledge of later editions of the Book of Mormon,
the King James Bible, or the Original or Printer's Manuscript. Write what the scan shows. Printer's errors, odd spellings,
missing or doubled words, damaged type and wrong running heads are all kept as printed. If a reading is doubtful, keep your best
reading and add an HTML comment right after it, e.g. `Zarahemla <!-- uncertain: maybe Zarahenla -->`.

Do not "fix" the 1830 punctuation or paragraphing to match modern editions: this edition has long paragraphs and little punctuation, and that is the point.

## How the agents are run (not part of the spec they see)

- The agent must view the crop images for every page. If the image tool fails, it stops and reports the page as failed; transcribing from the OCR text alone is not allowed.
- Pages are processed in batches of 16, one page at a time, writing each file right after reading it; a batch skips pages whose output file already exists, so an interrupted batch can resume.
