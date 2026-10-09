# 1830 Grandin Palmyra Book of Mormon
[Markdown](#what-is-markdown) &amp; Plain Text extractions of the content of the 1830 edition of the Book of Mormon published by E.B. Grandin, Palmyra, New York, based on the manuscript copy provided by Oliver Cowdery, which he copied from the original manuscript dictated by Joseph Smith &amp; transcribed by Cowdery &amp; others April 1829 through June 1829. Extracted using AI.

## Files
* [book-of-mormon-1830.md](book-of-mormon-1830.md): the whole text in a single [Markdown](#what-is-markdown) file (about 273,000 words): title page, Preface, the Book of Mormon, and the testimonies of the Three and Eight Witnesses. A `<!-- page NNN -->` comment marks where each PDF page begins.
* [book-of-mormon-1830.txt](book-of-mormon-1830.txt): the same text as plain text, with no [Markdown](#what-is-markdown).
* [book-of-mormon-1830-sparse.txt](book-of-mormon-1830-sparse.txt): plain text of the Book of Mormon proper only: the title page (PDF page 5), which was translated from the plates, followed by the text (PDF pages 9–592, from the First Book of Nephi to "THE END."). It leaves out the 1830 imprint at the foot of the title page (author, printer, place and year), the title-page verso, the Preface, the testimonies and the library notes.
* [book-of-mormon-1830-pages/](book-of-mormon-1830-pages/): one [Markdown](#what-is-markdown) file per page of the scan (`page-001.md` to `page-598.md`), with running heads, headings and signature marks. File numbers are PDF page numbers (printed page number = PDF page − 4 in the main text). These are the source of truth; the three files above are generated from them.
* [printer-typos.md](printer-typos.md): a catalog of the likely printer's typos and misspellings in the 1830 text (about 140 occurrences, each with its page and context), leaving out spellings that were normal or intentional for the period, such as "shew".

## What is in the 1830 edition
The 1830 printing is unlike later editions, and the transcription keeps it that way:
* There are **no verse numbers**, no double columns, no footnotes, and no cross-references. The text is set in long paragraphs on a single wide column.
* Punctuation is sparse and very different from modern editions. Spelling, capitalization and grammar are kept exactly as printed, **printer's errors included**; nothing has been corrected from later editions.
* Chapters are numbered within each book. The first chapter of a book (and some others) has an italic summary.
* The books are named as printed: the First and Second Book of Nephi, the Book of Jacob, Enos, Jarom, Omni, the Words of Mormon, Mosiah, Alma, Helaman, then two successive books both headed "The Book of Nephi", then a book headed "Book of Mormon", then Ether and Moroni. The later divisions into numbered books (3 Nephi, 4 Nephi, Mormon) and into verses do not exist in this edition.

## Source
Extracted from the [PDF Scan](https://archive.org/download/book-of-mormon-1830/Book%20of%20Mormon%201830.pdf) of the physical book owned by the University of Pittsburgh's Darlington Memorial Library, hosted by [Archive.org](https://archive.org/details/book-of-mormon-1830). The scan has 598 pages: covers and endpapers, the library bookplate and an Internet Archive notice (PDF pages 1–4), the title page and its verso (5–6), the Preface (7–8), the text (9–592), the two testimonies (593–594), blank pages, and a library conservation record and back endpaper (595–598). The PDF itself is not included in this repository.

## What is Markdown?
Markdown is a simple way of writing formatted text using plain characters, such as `#` for headings and `*asterisks*` for *italics*. A Markdown file is still readable as ordinary text, and can also be displayed with formatting.
* Learn more at [markdown.org](https://markdown.org/).
* Tools for displaying, editing, or converting Markdown files: [https://markdown.org/tools/](https://markdown.org/tools/)

## Artificial Intelligence
Extracted with Claude Code from Anthropic using the Sonnet 5.5 model.

Each page was transcribed from images of the scan (the PDF's own OCR was only a helper). Every page was then checked a second time against the scan by a separate AI agent, and a third time by another agent working blind from fresh high-resolution renders. The text is meant to show what the page shows, so the printer's spellings and errors, punctuation, hyphenation and paragraphing are kept as they appear. Where a mark was too worn to tell a comma from a period, the gap after it and whether the next word starts with a capital letter were used to decide (more space and a capital: a period; less space and a lowercase word: a comma). A few things are deliberately **not** reproduced: the thin space the type puts before `;`, `:`, `?` and `!`, and ink specks and stains that are not letters or punctuation.

**This is an AI transcription. Only its doubtful places have been checked by a person.** The check passes found and fixed a small number of dropped words and silently "corrected" printer's errors, so the text should be very close to the scan, but the book as a whole has not been proofread by a person. The 76 readings that the AI passes marked as close calls (worn type, punctuation marks that look like either a comma or a period, letters clipped at the scan edge, a few folios) were reviewed by a person against the scan: 45 were confirmed as they were and 31 were changed. Marks of punctuation on worn type, and the clipped edges of a few pages (the title-page verso and a few others), are still the most likely places for a remaining error, and no passage is marked unreadable. For anything that matters, check the scan.

See [transcription-notes.md](transcription-notes.md) for how the text was extracted, the conventions used, what the audits found, and the borderline readings that remain.

The files [review-checklist.md](review-checklist.md) and [review-decisions.json](review-decisions.json) detail the 76 close calls that were reviewed by a person against the scan, and the decision on each (45 confirmed, 31 changed).

## Rebuilding the combined files
The page files are the source of truth. After editing any of them, regenerate the three combined files (Python 3, standard library only; run from the repository root):
```
python3 tools/compile_markdown.py   # book-of-mormon-1830.md
python3 tools/make_plaintext.py     # book-of-mormon-1830.txt
python3 tools/make_sparse.py        # book-of-mormon-1830-sparse.txt
```
See [tools/README.md](tools/README.md) for the full pipeline (rendering the scan, transcribing, auditing).
