# Proofread spec — second, independent pass over the transcription

Every page has already been transcribed (by one agent) and audited (by a second). This is a **third, independent
reading** meant to catch what both missed. It works from higher-resolution renders and is deliberately blind to the
earlier audits, so that it does not inherit their judgments. The rules for the text itself are those in
`tools/transcription-spec.md` (read it completely first): write what the scan shows, nothing more and nothing less.

## Independence rules

- Do **not** read `work/audit-log-*.md`, `work/proof-log-*.md` of other batches, or `transcription-notes.md` §3, §5, §6.
  (You may read §2 and `tools/transcription-spec.md`.) The point is to form your own reading of the page before seeing
  anyone else's.
- Do not look at the images the earlier agents used if you can avoid it: render your own (below) at 4x.
- Existing `<!-- uncertain: ... -->` and layout comments in the page file are fine to read; they are part of the file.

## Procedure per batch (pages A–B)

1. Render at 4x into a private folder (the PDF is `Book-of-Mormon-1830.pdf` in the repo root):
   `/private/tmp/claude-501/venv/bin/python tools/render_pages.py Book-of-Mormon-1830.pdf --out work/proof --pages A-B --scale 4`
   This writes `work/proof/img/pNNNN_1_top.jpg` and `pNNNN_2_bottom.jpg` (top and bottom halves, overlapping in the middle).
   If the venv fails (`No module named pypdfium2`), rebuild it: `rm -rf /private/tmp/claude-501/venv; python3 -m venv
   /private/tmp/claude-501/venv; /private/tmp/claude-501/venv/bin/pip install pypdfium2 pillow`, and say so in your report.
   For a doubtful spot render only that page at `--scale 6` into `work/proof6`.
2. For each page, in order: view BOTH crops with the Read tool, and read the page file
   `book-of-mormon-1830-pages/page-NNN.md`. Compare **line by line, word by word, mark by mark**. Never read a page from
   memory of the text (you know the Book of Mormon; the scan is authoritative, the 1830 print has many errors).
3. Check, on every page:
   - every word and its spelling (printer's errors kept: `againt`, `wouid`, `numher`, `meroy`, `wben`... if the scan prints
     it, the file must too; a worn letter that still reads as the expected letter is the expected letter);
   - **inserted or dropped words** (e.g. a dropped `of`, an added `which`), doubled words, transposed words, lines skipped
     or repeated at the middle overlap of the two crops;
   - proper names, letter by letter;
   - punctuation marks and their order, the capital after a colon, `.—` dashes, apostrophes, parentheses, italics;
   - hyphenation (line-end hyphens joined, compounds hyphenated mid-line kept) and page-end hyphens;
   - `<!-- cont -->` on the first line: flush-left first line = continuation (marker present); indented first line (or
     a heading at the top) = new paragraph (no marker); also that each page's last paragraph really continues;
   - paragraph breaks inside the page (an indented line starts a paragraph);
   - the running head and printed folio (kept as printed, errors included), footers and signature marks, headings, chapter
     summaries (italic), dinkus comments only where a thick rule is actually printed, book titles and subtitles;
   - no space before `; : ? !`; no verse numbers; no modern punctuation.
4. **Editing policy (important).** Edit the page file only when you are *certain* the file is wrong and the scan right
   (a different letter, a missing/extra word, a wrong name, a wrong marker, a heading error). Make the smallest edit.
   For a borderline mark (comma vs period vs speck, a worn letter that could be two things, a blot) where you read it
   differently from the file, **do not edit**: record it under "Disagreements" in the log. **Exception: an uncertain
   comma-versus-period mark is settled by the tie-breaker rule below, and its result is written (edit the file if the
   rule gives a different mark) and logged as a `tie-breaker` line, not left as a disagreement.** Do not add `uncertain`
   comments of your own and do not remove existing ones, except to delete one you can settle with certainty at 6x
   (then say so). **Never correct a misspelling, a wrong word, a missing or doubled word, odd grammar, a wrong name form or any other
error that is printed in the original** to the standard or expected form: the file must keep exactly what the 1830 print
shows (`againt`, `Prophesy`, `wouid`, `peopeople`, `Gaddianhi`...). The only spelling edit allowed is the reverse one: restoring
a printed error that the transcription had silently normalized, and only when you can see it plainly on the scan.
Do not 'improve' anything from your knowledge of the Book of Mormon or of English. Every edit you log must name the scan
evidence (e.g. 'scan prints d-e-a-d-n-e-s, file had deadness'). An edit that moves the file closer to modern spelling,
punctuation or grammar, rather than closer to the scan, is a mistake.
5. Log to `work/proof-log-A-B.md` (create it): per page `## Page NNN` then `- no changes` or one line per change
   (`where: was "old" -> now "new" (reason)`), and under it, if any, `- disagreement: <where>: file has "x", I read "y"
   (why)`. Skip pages already logged so an interrupted run can resume.

## Tie-breaker for a comma versus a period (user-set rule)

When a mark after a word is genuinely uncertain between a period and a comma (worn type, a dot with a faint tail), decide by
the **gap after the mark and the case of the next word**:

- **more space after the mark, followed by a capitalized word = period**;
- **less (tighter) space after the mark, followed by a lowercase word = comma**.

Compare the gap with the ordinary word spaces on the same line. This is an educated guess for uncertain marks only: a mark that
is plainly a period or plainly a comma at zoom is written as it is, whatever follows (the 1830 print has real periods before
lowercase words, e.g. "fire. and", and real commas before capitals). If the two signals disagree (wide gap before a lowercase
word, or a tight gap before a capital), fall back on the shape of the mark; if that is still unclear, keep the existing
reading and, where there was an `<!-- uncertain -->` comment, leave it in place. Applying this rule does not require a
comment; only a mark that still cannot be settled keeps one. Log each use in the proofread log as
`- tie-breaker: <where>: "x" -> "y" (gap/case)`.

## Dash spacing (do not edit)

After a sentence-final mark an em dash that ends a printed line is followed by the next line's first word; the book is
written `.— And` (a space after the dash). Do **not** add or remove that space: whether the print has a space at a line
wrap cannot be seen, and one convention is applied to the whole book afterwards. A dash inside a word run
(`Jerusalem—that`) has no spaces.

## Hard stops

- If an image Read fails for a page, do not read it from the OCR: skip it and list it as failed.
- If you hit an API usage/rate limit or a content-filter block, stop and say exactly which page you were on and the last
  page you completed.
- Touch only your own page files and your own log; do not edit any other file; do not run git commands.

## Final reply (brief)

Pages proofread, pages failed, total edits grouped by kind (spelling/printer's error, inserted or dropped word, name,
punctuation, cont marker, structure/heading, other), then the list of disagreements.
