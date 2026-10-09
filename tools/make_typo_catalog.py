#!/usr/bin/env python3
"""Build printer-typos.md: a catalog of the likely printer's typos and misspellings in the 1830 text.

The list of forms is curated below (triaged from a dictionary scan of the compiled text plus the audit notes); this script
finds every occurrence of each form in book-of-mormon-1830.md, with its PDF page and a snippet of context, so the page
numbers and contexts always come from the current text. Spellings that were normal or intentional for the period or the edition
(shew, sayeth, marvellous, ...) are deliberately NOT cataloged; see the NOT_INCLUDED notes at the end of the output.

Usage:  python3 tools/make_typo_catalog.py [--md FILE] [--out FILE]
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (printed, should be, note). `printed` is matched as a whole word, case-sensitive; a tuple (regex, label) matches a pattern.
SECTIONS = [
    ('Letter or letters dropped', [
        ('adminster', 'administer', ''), ('adultry', 'adultery', ''), ('againt', 'against', ''), ('aginst', 'against', ''),
        ('atempt', 'attempt', ''), ('beold', 'behold', ''), ('bgan', 'began', ''), ('brethen', 'brethren', ''),
        ('changeble', 'changeable', ''), ('chid', 'child', ''), ('clowd', 'cloud', ''), ('covenated', 'covenanted', ''),
        ('crated', 'created', ''), ('daghter', 'daughter', ''), ('deadnes', 'deadness', ''), ('destoy', 'destroy', ''),
        ('dilgence', 'diligence', ''), ('encirled', 'encircled', ''), ('establised', 'established', ''),
        ('expdient', 'expedient', ''), ('fait', 'faith', ''), ('fo', 'for', '"fo notwithstanding"'),
        ('hardnes', 'hardness', ''), ('higway', 'highway', ''), ('holines', 'holiness', ''), ('iniqities', 'iniquities', ''),
        ('Kowest', 'Knowest', ''), ('maner', 'manner', ''), ('belive', 'believe', ''), ('Nevertheles', 'Nevertheless', ''),
        ('possesion', 'possession', ''), ('provisons', 'provisions', ''), ('remant', 'remnant', ''),
        ('remebrance', 'remembrance', ''), ('Sprit', 'Spirit', ''), ('spritual', 'spiritual', ''), ('surronded', 'surrounded', ''),
        ('to-mrrow', 'to-morrow', ''), ('traditons', 'traditions', ''), ('uncircumsised', 'uncircumcised', ''),
        ('vison', 'vision', ''), ('wat', 'what', ''), ('withersoever', 'whithersoever', ''), ('writen', 'written', ''),
        ('yourselve', 'yourselves', ''), ('bablings', 'babblings', ''), ('havgn', 'having', 'at a page break: "hav-" / "gn"'),
    ]),
    ('Letter added or doubled', [
        ('beginnning', 'beginning', ''), ('citties', 'cities', ''), ('commannded', 'commanded', ''),
        ('commmandments', 'commandments', ''), ('continnally', 'continually', ''), ('evidencess', 'evidences', ''),
        ('fiulfilled', 'fulfilled', ''), ('iniqutity', 'iniquity', ''), ('neeeds', 'needs', ''), ('reedeemed', 'redeemed', ''),
        ('utttered', 'uttered', ''), ('verry', 'very', ''), ('againstt', 'against', '"againstt hem"'), ('wrent', 'rent', '"wrent in twain"'),
        ('arrriven', 'arriven', 'the edition otherwise prints "arriven"'), ('engravened', 'engraven', '"I engravened"'),
    ]),
    ('Letters transposed', [
        ('iniqiuty', 'iniquity', ''), ('knwon', 'known', ''), ('langauge', 'language', ''), ('eigth', 'eighth', ''),
        ('berak', 'break', ''), ('savlation', 'salvation', ''), ('Irsael', 'Israel', ''),
    ]),
    ('Wrong letter (one letter printed for another)', [
        ('aaswer', 'answer', ''), ('angles', 'ankles', '"mine angles were much swollen"'), ('af', 'of', 'in an italic chapter summary'),
        ('babtized', 'baptized', ''), ('bebeld', 'beheld', ''), ('betweem', 'between', ''), ('exeeeding', 'exceeding', ''),
        ('govereor', 'governor', ''), ('heen', 'been', '"heen racked"'), ('hy', 'by', '"hy the hill of Shim"'), ('meroy', 'mercy', ''),
        ('mnltitude', 'multitude', ''), ('muititude', 'multitude', 'a dotted i for l'), ('neverthelers', 'nevertheless', ''),
        ('nnto', 'unto', ''), ('obout', 'about', ''), ('opon', 'upon', ''), ('peeple', 'people', ''), ('plaees', 'places', ''),
        ('possessson', 'possession', ''), ('restoiation', 'restoration', ''), ('ro', 'no', '"shew ro greater things"'),
        ('rumderers', 'murderers', ''), ('seeond', 'second', ''), ('tbat', 'that', ''), ('theit', 'their', ''), ('tne', 'the', ''),
        ('wben', 'when', ''), ('whieh', 'which', ''), ('wildernsss', 'wilderness', ''), ('wouid', 'would', 'a dotted i for l'),
        ('GHAPTER', 'CHAPTER', 'a chapter heading'), ('rssurrection', 'resurrection', 'worn type; read as printed by the reviewer'),
        ('numerority', 'numerousness', 'not a word in any edition; the intended word is uncertain'),
        ('Samnel', 'Samuel', 'a name, in an italic chapter summary'), ('Lananites', 'Lamanites', 'a name'),
        ('Lamanitas', 'Lamanites', 'a name'), ('Helama', 'Helaman', 'a name'),
    ]),
    ('Syllable repeated or dropped', [
        ('peopeople', 'people', '"peo-" / "people" at a line end'), ('transgransgressions', 'transgressions', '"trans-" / "gransgressions"'),
        ('rerecord', 'record', '"bare re-" / "record" at a line end'), ('powful', 'powerful', '"pow-" / "ful" at a line end'),
    ]),
    ('Words run together', [
        ('thejoy', 'the joy', ''),
    ]),
    ('Doubled words', [
        (('for the the space', 'the the'), 'the', 'printed twice across a line break'), (('came to to pass', 'to to'), 'to', ''),
        (('that that they should not lie', 'that that'), 'that', 'printed twice across a line break ("that" ends one line and begins the next)'),
    ]),
    ('Wrong word (a real word printed for the intended one)', [
        (('shall he called', 'he called'), 'be called', 'an h printed for b'),
    ]),
    ('Names printed in a variant spelling', [
        ('Morionton', 'Morianton', 'Morianton occurs 24 times'), ('Gaddianhi', 'Giddianhi', 'Giddianhi occurs 12 times'),
        ('Antionam', 'Antionum', 'Antionum occurs 4 times'), ('Mulok', 'Mulek', 'Mulek occurs 16 times; possibly the actual name in this passage'),
        ('Zenas', 'Zenos', 'Zenos occurs 11 times; possibly a different spelling by intent'),
    ]),
]

# Misspellings that recur (the same slip printed several times): listed in their own section, with all pages.
RECURRING = [
    ('recieve / recieved / recieveth', ['recieve', 'recieved', 'recieveth'], 'receive', 'ie for ei'),
    ('percieve / percieved', ['percieve', 'percieved'], 'perceive', 'ie for ei'),
    ('harrass', ['harrass'], 'harass', 'doubled r'),
    ('brethern', ['brethern'], 'brethren', 'letters transposed'),
    ('eatheth', ['eatheth'], 'eateth', 'extra h (printed both times in one verse)'),
    ('fraid', ['fraid'], 'afraid', 'initial a dropped ("exceeding fraid"); printed three times, so possibly the edition\'s own form'),
]

NOT_INCLUDED = """## Not included: spellings that were normal or intentional

These are non-standard by modern rules but are **not** printer's slips, and are left out of the catalog:

- **The edition's own forms:** `shew`, `shewn`, `shewed`, `shewing`, `sheweth`; `-eth` and `-est` verb forms (`sayeth`, `cometh`, `doth`, `hath`, `saith`, `speakest`, `wo`); `to-day`, `to-morrow`, `every where`, `for ever`, `no where`.
- **Period spellings (1830, and mostly the King James Bible's):** `marvellous`, `centre`, `armour`, `vapour`, `lustre`, `savour`, `fulness`, `fulfil`, `wilfully`, `offence`, `baptise`, `baptised`, `immoveable`, `moulten`, `mouldering`, `sepulchre`, `rereward`, `cimeter`, `journied`, `dissention`, `threatnings`, `burthen`, `counsellor`, `carcases`, `realise`, `phrensied`, `wrapt`, `ancles`, `firy`, `sware`, `wist`, `engraven`, `abridgement`, `quarrellings`, `skilful`, `judgement`, `adhear`, `suredly`.
- **Words and forms peculiar to the text:** `arriven`, `unwearyingness`, `stiffneckedness`, `woundedness`, `prophesyings`; the measures and names in Alma 11 (`senine`, `senum`, `seon`, `shiblon`, `shum`, `limnah`, `antion`, `ziff`, `ezrom`, `onti`, `amnor`); and all the proper names (including `Jacom`, `Gilgah`, `Mahah`, `Orihah`, `Zenoch`, `Shemnon`, `Amoron`).
- **Grammar of the dictated text:** `had came`, `he has fell`, `those who was`, `wo unto they`, `ye had ought`, `ye ... hath`, `had had`, `do do` (grammatical: "do slay ... and do do all manner of iniquity").
- **Letters lost to the scan edge** on pp. 6, 142, 145, 558 and 577 (clipped at the page edge), which are not printing errors.
"""


def load(md):
    raw = md.read_text(encoding='utf-8')
    parts = re.split(r'<!-- page (\d+) -->', raw)
    segs, cur = [], 0
    for i, t in enumerate(parts):
        if i % 2 == 1:
            cur = int(t)
            continue
        t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
        segs.append((cur, re.sub(r'\s+', ' ', t)))
    return segs


def find(segs, spec):
    """Yield (page, snippet) for each occurrence."""
    if isinstance(spec, tuple):
        pat, hit = spec
        rx = re.compile(re.escape(pat))
        hl = hit
    else:
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(spec) + r'(?![A-Za-z])')
        hl = spec
    for pg, t in segs:
        if pg < 5 or pg > 598:
            continue
        for m in rx.finditer(t):
            a = max(0, m.start() - 38)
            b = min(len(t), m.end() + 30)
            s = t[a:b]
            i = s.find(hl) if hl in s else 0
            s = s[:i] + '**' + s[i:i + len(hl)] + '**' + s[i + len(hl):]
            yield pg, ('…' if a else '') + s.strip() + ('…' if b < len(t) else '')


def printed(pg):
    return str(pg - 4) if 9 <= pg <= 592 else '—'


def row(spec, should, note, segs):
    out = []
    for pg, snip in find(segs, spec):
        label = spec[1] if isinstance(spec, tuple) else spec
        out.append((pg, '| `%s` | %s | %d | %s | %s%s |' % (label, should, pg, printed(pg), snip.replace('|', '\\|'),
                                                           (' (' + note + ')') if note else '')))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=str(ROOT / 'book-of-mormon-1830.md'))
    ap.add_argument('--out', default=str(ROOT / 'printer-typos.md'))
    args = ap.parse_args()
    segs = load(Path(args.md))
    out, total, missing = [], 0, []
    header = '| Printed | Should be | PDF p. | Printed p. | In context |\n|---|---|---|---|---|'
    body = []
    for title, items in SECTIONS:
        rows = []
        for spec, should, note in items:
            r = row(spec, should, note, segs)
            if not r:
                missing.append(spec)
            rows += r
        rows.sort(key=lambda x: x[0])
        total += len(rows)
        body.append('\n## %s (%d)\n\n%s\n%s' % (title, len(rows), header, '\n'.join(r for _, r in rows)))
    rec = []
    for label, forms, should, why in RECURRING:
        hits = [h for f in forms for h in find(segs, f)]
        hits.sort()
        total += len(hits)
        pages = ', '.join(str(p) for p, _ in hits)
        rec.append('| `%s` | %s | %d | %s | %s |' % (label, should, len(hits), why, pages))
    intro = f"""# Printer's typos and misspellings in the 1830 Book of Mormon

A catalog of the places where the 1830 print itself has a slip of the type, a misspelling, or a doubled word, as the transcription records
it. {total} occurrences, grouped by the kind of slip, each with its PDF page, printed page (PDF − 4 in the text) and context.

**What is and is not here.** The transcription keeps every printed error exactly as printed (nothing was corrected from later editions), so
all of these are in the page files as printed. This list leaves out spellings that were normal or intentional for the period or the edition
(`shew`, `sayeth`, `marvellous`, `wilfully` and the like; see the end of the file). It was built from a dictionary scan of the whole text,
triaged by hand, so it is **likely, not exhaustive**: a slip that happens to produce another real word (`he` for `be`) is only caught where it was noticed, and a few
entries are judgment calls (marked in the notes). Some rows are worn-type readings (`wouid`, `wben`): the scan shows a letter that looks like the printed one, which the
audits kept as printed. Names are listed only where a variant sits next to a much more frequent spelling of the same name; whether such a variant is a typo or a deliberate spelling is not always certain.

**Checked against the scan.** Every form below was compared with the scanned page at standard size (no zoom) by a separate pass: all were found printed as listed. Three could not be settled at that size and rest on the earlier zoomed audits: `utttered` (three t's, p. 499) and `wben` (a closed-bowl b, p. 577) were settled at zoom by the audits, and `Mulok` (p. 211) is the closest of the names to a worn-type reading.

Generated by `tools/make_typo_catalog.py` from the live text, so page numbers and contexts stay current if the pages are edited.
"""
    recsec = '\n## Misspellings that recur\n\nThe same slip printed more than once (compositor habits rather than one-off slips).\n\n| Printed | Should be | Times | Slip | PDF pages |\n|---|---|---|---|---|\n' + '\n'.join(rec)
    Path(args.out).write_text(intro + '\n'.join(body) + '\n' + recsec + '\n\n' + NOT_INCLUDED, encoding='utf-8')
    print(f'{total} occurrences -> {args.out}')
    if missing:
        print('NOT FOUND in the text:', missing)


if __name__ == '__main__':
    main()
