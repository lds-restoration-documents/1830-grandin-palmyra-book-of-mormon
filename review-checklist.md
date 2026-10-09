# Review checklist

> **Status: completed.** All 76 items were reviewed by the owner against the scan: 45 confirmed as they were, 31 changed (see `review-decisions.json` for each decision with its before and after text). The table below shows the readings **as they were when the list was made**; the page files are the current text. The ten `<!-- uncertain -->` comments listed below were all resolved.

Places in the transcription where a person with the scan in front of them could improve the text. Each row is a reading that was
a close call, a judgment, or a restoration the AI agents made. **It is not a list of known errors**: in most rows the file's
reading is probably right. The **Confidence** column is how sure we are that the file's *current* reading is correct (low = a reviewer is
more likely to change it). 76 items: 43 low confidence (check these first), 31 medium, 2 high.

## How to use it

**Easiest: the review app.** From the repository root run `python3 tools/review/review_app.py` (it opens http://127.0.0.1:8765 in your
browser; `pip install pypdfium2 pillow` first if you want it to show the scan beside each item, otherwise it tells you which
PDF page to open). For each item it shows the question, the other reading, the page text in an editable box and the top and
bottom halves of the scan. **Confirm as is** (`c`) records that you checked it; **Save my edit** (`⌘/Ctrl-Enter`) writes your
change into the page file (with a backup in `work/review-backups/`); **Skip** (`s`); arrow keys move between items. Filters
by group, status and confidence are at the top, and **Rebuild compiled files** regenerates the three combined files when you
finish. Decisions are saved in `review-decisions.json` (in the repository, so you can see what was confirmed). The same
steps by hand:

1. Open `Book-of-Mormon-1830.pdf` (the scan; not in the repository) at the **PDF page** in the first column. In the main text the
   printed page number is the PDF page minus 4 (second column); the front matter and back matter are unnumbered.
2. Find the words in **Now reads** (a snippet of the page file as it stands, with `…` where it is cut). Look at the mark or letter
   described under **What to check**.
3. If the scan shows the **Other reading**, edit the page file `book-of-mormon-1830-pages/page-NNN.md` (the source of truth; never
   edit the combined files), and delete the `<!-- uncertain: … -->` comment on that spot if there is one.
4. When you have finished a batch of edits, rebuild the combined files from the repository root:
   `python3 tools/compile_markdown.py && python3 tools/make_plaintext.py && python3 tools/make_sparse.py`
5. Note what you decided in `transcription-notes.md` §6b.

Rules to apply when you decide (see `tools/transcription-spec.md` and `tools/proofread-spec.md`): write what the scan shows, never
what a later edition says; keep printer's errors; a worn letter that still reads as the expected letter is that letter, but a
clearly different printed letter is kept as printed; ink specks are not text; for an uncertain comma-versus-period mark, more
space + a capitalized next word = period, less space + a lowercase next word = comma (the owner's rule), unless the mark is plainly
one or the other; no space is written before `; : ? !`.

This list is generated from the page files and the notes; if you resolve an item, you can delete its row. The ten
`<!-- uncertain -->` comments still in the page files (pp. 146, 247, 294, 486, 524, 528, 538, 564, 585, 587) are all included below.

## Punctuation marks (comma, period, colon, semicolon, specks)

| PDF p. | Printed p. | Now reads | What to check | Other reading | Confidence |
|---|---|---|---|---|---|
| 5 | — | `…also of the Lamanites; written to the Lamanites, which are a remnant of the House of Israel; and…` | mark after the second "Lamanites" on the title page (tie-breaker: comma) | a period (the earlier readings had a period) | medium |
| 6 | — | `…venants of th Lord, that they are not cast off forever: and also to the convincing of the Jew…` | two dots after "forever" read as a colon | a semicolon | medium |
| 22 | 18 | `…hmael, had come down unto the tent of my father, they did give thanks unto the Lord their G…` | mark after "father" at a line end | a period (gap cannot be measured) | medium |
| 27 | 23 | `…e eternal round. Therefore, remember, O man. for all thy doings, thou shalt be brought…` | round dot with no tail, wide-ish gap, lowercase "for" follows | a comma | low |
| 33 | 29 | `…ecord of the Jews, which contains the covenants of the Lord which he hath made unto the House of …` | small dot after "covenants" (read as a speck, no mark written) | a period or comma | low |
| 52 | 48 | `…rds the promised land; and after that we had been driven forth before the wind, for the space …` | dot-like mark after "and" in "and after that" (read as a speck) | a comma | low |
| 58 | 54 | `…hus saith the Lord, thy Redeemer, the Holy One of Israel I have sent him, the Lord thy God, which teacheth…` | speck cluster after "Israel" (no mark written) | a colon | low |
| 82 | 78 | `… to know of things to come; wherefore I know that ye know that our flesh must waste away a…` | short stub after "ye" at the end of the page (read as a worn mark; the next page starts "know,") | a printed mark | low |
| 83 | 79 | `…l deliver up its dead; which death is the grave, And this death of which I have spoken, wh…` | heavy plain comma with a long tail but a wide gap before a capital (written as printed) | a period, as the gap-and-case rule would say | medium |
| 157 | 153 | `…ht of his body and the faculty of his whole soul, and also the prophets, wherefore, they did onc…` | small blurred dot with a faint tail; gap no wider than a word space | a period | medium |
| 199 | 195 | `…to pass that after they had ended the ceremony; that they returned to the land of Nephi, rejoic…` | tailed mark with a faint upper smudge (semicolon) | a comma | medium |
| 230 | 226 | `…y of the Nephites did fall before the Amlicites; nevertheless the Lord did strengthen …` | a tailed lower mark with a distinct upper dot at the end of the page; the file had no mark and one was inserted | no mark, or a comma | medium |
| 236 | 232 | `…red out of the hands of the people of king Noah. by the mercy and power of God. And behold, after t…` | round dot on the baseline at a line end; kept as a period | a comma | medium |
| 238 | 234 | `… garments have been cleansed and made white, through the blood of Christ, which will come …` | tailed blob at a line end in faded type | a period | medium |
| 247 | 243 | `…and spit upon him, and caused that he should be cast out of their city, he departed thence and…` | tiny faint dot after "be" (probably a speck; an uncertain comment remains) | a comma or period | low |
| 251 | 247 | `…anites than for them. For behold, the promises, of the Lord are extended to the Lamanites, but th…` | faint comma-like mark with no space before "of" | a speck (no mark) | medium |
| 262 | 258 | `…eeding great faith, are called with a holy. calling, yea, with that holy calling which wa…` | small flat dot at a line end, no tail; kept as a period | a comma | medium |
| 263 | 259 | `… of grace, equity and truth. And thus it is. Amen. ## CHAPTER X. Now as I said concerni…` | small dot with a short tail but a wide gap before the capital "Amen"; the rule gives a period | a comma | medium |
| 265 | 261 | `…were desirous that they might destroy Alma, and Amulek: for they were angry with Alma, becau…` | tailed mark at a line end | a speck | medium |
| 272 | 268 | `… And now after the Church having been established, throughout all the land, having got the victory …` | faint small mark with a slight tail | a period | low |
| 278 | 274 | `…because of the faithfulness of Ammon, saying: Surely, there has not been any servant among…` | tiny mark after the colon ("saying:.") read as a speck | a printed period | low |
| 308 | 304 | `…fter the Lamanites were driven out of the land, and their dead were buried by the people of the land…` | small dot without a clear tail; changed to a comma on gap and case alone | a period | low |
| 335 | 331 | `…man can be saved, only in and through Christ: Behold, he is the life and the light of the …` | baseline dot plus a faint upper dot (colon); the page prints colons before capitals elsewhere | a period | medium |
| 454 | 450 | `…eir arrows, they cried out unto their captains, saying, Take this fellow and bind him, for b…` | dot with a small tail; tight gap before lowercase "saying" (comma by the rule) | a period | medium |
| 459 | 455 | `…assed away, since the days of Mosiah, which was king over the people of the Nephites. And …` | tiny fleck after "was" (read as a speck, no mark written) | a comma | low |
| 471 | 467 | `…in this same year, yea, the thirtieth year, they did destroy upon the judgement seat, yea,…` | bold comma with a tiny faint dot beside the r (read as a stray speck) | a semicolon | low |
| 472 | 468 | `… to his tribe; nevertheless they were enemies; notwithstanding they were not a righteous people; yet…` | semicolon with a faint upper dot | a comma | medium |
| 477 | 473 | `… converted, that I may heal you? Yea, verily I say unto you, if ye will come unto me, ye…` | tiny tick after "verily" at the baseline (read as a speck, no mark written) | a comma | low |
| 478 | 474 | `…shall offer for a sacrifice unto me a broken heart and a contrite spirit. And whoso cometh unto me with…` | tiny pale fleck after "heart" (read as a speck) | a comma | low |
| 496 | 492 | `…d shall pray for him unto the Father, in my name. and if it so be that he repenteth, and is ba…` | clear round dot with a wide gap but a lowercase "and" follows; kept as a period | a comma | medium |
| 544 | 540 | `…than the nation which I will raise up unto me, of thy seed, upon all the face of the earth. And …` | tiny dot, tight gap; changed to a comma on gap and case alone | a period | low |
| 587 | 583 | `…e second epistle of Mormon to his son Moroni:* MY beloved son, I write unto you aga…` | mark after "Moroni" at the end of the italic summary (colon with a speck) | a period | low |

## Worn, blotted or doubtful letters and words

| PDF p. | Printed p. | Now reads | What to check | Other reading | Confidence |
|---|---|---|---|---|---|
| 5 | — | `(whole page)` | title page: a comment on the mark after "Lamanites" was removed after the tie-breaker; check the whole title page once against the scan | — | low |
| 144 | 140 | `…h flattery, and much power of speech, according to the power of the Devil. And he had hope to shake me from the…` | the word prints a-c-c-o-?-d-i-n-g with a worn r that looks like a dotless i; written "according" | "accoiding" (a printed i) | medium |
| 146 | 142 | `… the power of the Holy Ghost, and the mimstering of Angels. And he spake plainly unto …` | "mims-/tering": the third letter might be an n (an uncertain comment remains) | "ministering" | medium |
| 151 | 147 | `…ith all long suffering, the people to diligence; teaching the law of Moses, and the i…` | third letter of the second "diligence" looks like a worn i or l | "diiigence" | low |
| 191 | 187 | `…e, and which shall be, even until the resurrection of Christ: for so shall he be called. And now, …` | a worn glyph that reads like "rssurrection" | "rssurrection" | low |
| 216 | 212 | `…s people, and also the prayers of his servant Alma, which is thy father: for he hat…` | "seivant" in the scan: worn r that reads like i; written "servant" | "seivant" | low |
| 294 | 290 | `…hat they called their name Anti-Nephi-Lchies ; and they were called by this name, …` | "Anti-Nephi-Lchies": the second letter prints as an open c without a crossbar (written as printed, with a comment) | "Lehies" (a worn e) | medium |
| 483 | 479 | `…ed are all the peace-makers, for they shall he called the children of ` | an h is printed where "be" is expected (written as printed); a worn b would show a bowl | "shall be called" | medium |
| 486 | 482 | `…s in heaven. Therefore, when ye shall do yoar alms, do not sound a trumpet before y…` | the third letter of "your" is blotted and reads more like an a (written "yoar", with a comment) | "your" | medium |
| 524 | 520 | `…he hardness of their hearts, the land was cursed for their sake. And these Gaddianton …` | a hyphen-like mark after "was" at a line end (an uncertain comment remains) | a printed hyphen: "was-cursed" | low |
| 528 | 524 | `… not of their sins. And when they had sworn by all that had been forbidden them, by our …` | a worn final l reading like "ali" (written "all", with a comment) | "ali" | low |
| 538 | 534 | `…hes, yea, even every one, have become polluted because of the pride of your hearts. ` | the o is filled and reads like c ("pclluted"); written "polluted" with a comment | "pclluted" | low |
| 564 | 560 | `…d linen; and they did work all manner of cloth, that they might clothe themselves fr…` | the first letter of "of" is a filled-in blot, o or e (written o, with a comment) | "ef cloth" | low |
| 585 | 581 | `… and grace, will keep you through the endurance of faith on his name to the end. And …` | a blot hides the n of "endurance" (written "endurance", with a comment) | a different letter | low |

## Letters clipped by the scan edge

| PDF p. | Printed p. | Now reads | What to check | Other reading | Confidence |
|---|---|---|---|---|---|
| 6 | — | `…; written to the Lamanites, who are a remnant of the House of Israel; and also to Jew and Gentil…` | right edge clipped: "th" written "the" (the e is mostly visible) | "th" | medium |
| 6 | — | `…its thereof to the arts of designing, engraving, ar etching historical and other prints." R. R. L…` | right edge clipped: "ar" (a clipped n reading as r, like "Charts, ar Books"), written as visible | "an" or "and" | low |
| 6 | — | `…phesy and of Revelation. Written, and sealed up, an hid up unto the Lord, that they might…` | right edge clipped: "an" (the d is about 40–50% visible; a stricter threshold would write "and"); also "gift an" | "and" | low |
| 6 | — | `…gift of God; an abridgment taken from the Book of Ether. Also which is a Record of the…` | right edge clipped: "o" (the f is a sliver, dropped) | "of" | low |
| 142 | 138 | `…d have kept my commandments, and hath brought unto m again the natural fruit, that my vine…` | right edge clipped: "m" (an e may be half visible, while "because" and "more" keep a clipped e) | "me" | low |
| 142 | 138 | `(whole page)` | right edge clipped on the second half of the page: "and" and "had" are written whole (the d about half visible); other line-end letters such as the final e of "because" and "more" are kept | dropped letters | low |
| 145 | 141 | `…or no man knoweth of such things: for e cannot tell of things to come. And after thi…` | left edge clipped: "e cannot" (an h-sliver may show: "he"); the page has about 18 clipped lines written as visible fragments | "he cannot" | low |
| 145 | 141 | `… let that be a sign unto thee that he hath powr, both in Heaven and in Earth; and als…` | "pow-/er" joined as "powr" (a half-e fragment may show at the clipped edge) | "power" | low |
| 558 | 554 | `(whole page)` | right edge clipped: line-end letters (t of "heart", "secret", "get") are written whole because more than half is visible | dropped letters | low |
| 577 | 573 | `(whole page)` | left edge clipped: the first letter of many lines is partly lost; words are written whole because at least half shows | fragments | low |

## Hyphens, spaces and ticks between words

| PDF p. | Printed p. | Now reads | What to check | Other reading | Confidence |
|---|---|---|---|---|---|
| 127 | 123 | `…ve in Christ, and view his death, and suffer his cross, and bear the shame of the world; whe…` | hyphen-like mark at the end of the line after "suffer" (written as a plain word) | a printed hyphen | low |
| 127 | 123 | `…on me to fulfil the commandment of my brother Nephi. ` | hyphen-like mark at the end of the line after "brother" | a printed hyphen | low |
| 143 | 139 | `…d cast into the fire? Behold, will ye reject these words ` | blotted glyph after "words" at the end of the page that may be a "?" (none written; the next page begins "Will ye reject the words of the Prophets?") | "words?" | low |
| 158 | 154 | `…nt people in keeping the commandments of the Lord. ` | a short dash-like mark with a blot after the period at the end of the page (probably ".—", none written) | ".—" | low |
| 174 | 170 | `…ng of the Lamanites, to the amount of one half of our corn, and our barley, and even all our gra…` | a faint mark between "one" and "half" | "one-half" | low |
| 337 | 333 | `…g beforehand. Behold, I say unto you, Is not a soul at this time as precious unto God, as…` | tiny raised tick between the words (read as a space) | a hyphen | low |
| 338 | 334 | `…on of their house; and these shall be cast out into ` | tiny raised dot between the words (read as a space) | a hyphen | low |
| 350 | 346 | `…ish or conquer. Behold, we are not of your faith; we do not believe that it is God tha…` | tiny tick between the words (read as a space) | a hyphen | low |
| 593 | — | `…that these things are true; and it is marvellous in our eyes: Nevertheless, the voice of the Lord …` | a tiny tick between the s and the colon (read as a speck) | a mark | low |

## Printed folios

| PDF p. | Printed p. | Now reads | What to check | Other reading | Confidence |
|---|---|---|---|---|---|
| 177 | 173 | ` **Header:** BOOK OF MOSIAH. \| 173 called interpreters; and no man can l…` | printed folio: the last digit is worn and could be 3 or 8 | "178" | low |
| 216 | 212 | ` **Header:** 122 \| BOOK OF MOSIAH. churches, that ther…` | printed folio reads "122" (a printer's error for 212), recorded as printed | "212" | medium |

## Restorations of dropped text and printed errors (confirm the scan)

| PDF p. | Printed p. | Now reads | What to check | Other reading | Confidence |
|---|---|---|---|---|---|
| 21 | 17 | `…they have driven him out of the land. Now, behold, I say unto you, that if ye will return unto Jerusale…` | paragraph break restored before "Now, behold," | — | medium |
| 161 | 157 | `…d serve him who hath created you from the beginning, and art preserving you from day to day, by lending you b…` | a dropped clause restored from the scan | — | high |
| 212 | 208 | `…and this because the kingdom had been confered upon none but those which were descen…` | "confered" (one r) restored as printed | "conferred" | medium |
| 220 | 216 | `…, at the time the Lord confounded the langauge of the people; and they were scattere…` | "langauge" restored as printed | "language" | medium |
| 248 | 244 | `… pass that as he entered the city, he was an hungered, and he saith to a man, Will ye give …` | "an" restored | — | high |
| 309 | 305 | `…; for it was strictly contrary to the comnands of God, that there should be a law wh…` | "comnands" restored as printed | "commands" | medium |
| 385 | 381 | `…ord their God, in this their times of affliction. They could not be taken in their sna…` | "affliction" (two f's) restored; earlier recorded as "afliction" | "afliction" | medium |
| 414 | 410 | `…of Helaman, was appointed to fill the judegment seat, by the voice of the people; but…` | "judegment" restored as printed | "judgement" | medium |
| 523 | 519 | `…, and being somewhat of a sober mind, therfore I was visited of the Lord, and tasted…` | "therfore" restored as printed | "therefore" | medium |

## Conventions you may want to confirm (not errors)

- **Thin space before `; : ? !`:** the type sets a thin space before these marks; the files write none (the first audit could not judge it reliably).
- **Specks:** ink specks, foxing, scratches and stains that do not read as a mark or letter are not transcribed.
- **Line-end dashes:** every dash that ends a printed line is written as `.— And` (a space after the dash), because the scan cannot show whether a space is printed at a line wrap. About 224 places.
- **Words split at a line end** are joined (`vis-` + `ions` = `visions`); compounds hyphenated mid-line are kept hyphenated; where nothing in the print settles a hyphenated compound split at a line end the word is closed up (for example `seashore`, `otherwise`, `byword`).
- **Paragraph test:** an indented first line starts a paragraph; a flush-left first line continues the previous paragraph (marked `<!-- cont -->`), even after a full stop on the previous page.
- **Printed folios and running heads** are copied as printed, errors included (for example the folio "122" on PDF page 216).
- **Small caps** at the start of a book's chapter (for example `AND now`) are written in capitals; ordinary capitals are written as printed.
