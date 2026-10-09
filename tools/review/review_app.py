#!/usr/bin/env python3
"""Local review app for review-checklist.md.

Shows each checklist item next to the scan (rendered from the PDF on demand), lets you keep it as is, edit the text on the
spot, or skip it, and writes your decisions to review-decisions.json. Edits are made to the page files in
book-of-mormon-1830-pages/ (with a timestamped backup in work/review-backups/). A button rebuilds the three combined files.

Needs only the Python standard library, plus `pypdfium2` and `pillow` to show the scan (without them the app still works,
and tells you which PDF page to open yourself).

Usage (from anywhere):
    python3 tools/review/review_app.py                 # then open http://127.0.0.1:8765
    python3 tools/review/review_app.py --port 9000 --no-browser
"""
import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]  # repository root (this file is tools/review/review_app.py)
CFG = {}
LOCK = threading.Lock()


# ---------------------------------------------------------------- checklist

def parse_checklist(path):
    items, group = [], ''
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            group = line[3:].strip()
            continue
        if not line.startswith('| '):
            continue
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
        if len(cells) != 6 or not cells[0].isdigit():
            continue
        page = int(cells[0])
        snippet = cells[2].strip('`').replace('\\|', '|')
        question, alt, conf = cells[3], cells[4], cells[5]
        iid = hashlib.sha1(f'{page}|{question}'.encode()).hexdigest()[:8]
        items.append({'id': iid, 'group': group, 'page': page, 'printed': cells[1], 'snippet': snippet,
                      'question': question, 'alt': alt, 'confidence': conf})
    return items


def page_path(page):
    return CFG['pages'] / f'page-{page:03d}.md'


def locate(raw, snippet):
    """Find the snippet (comment-stripped, whitespace-collapsed) in the raw page text; return (start, end) offsets or None."""
    needle = snippet.strip('… ').strip()
    if not needle or needle == '(whole page)':
        return None
    chars, idx = [], []
    for m in re.finditer(r'<!--.*?-->|\s+|[^<\s]+|<', raw, flags=re.S):
        t = m.group(0)
        if t.startswith('<!--'):
            continue
        if t.isspace():
            if chars and chars[-1] != ' ':
                chars.append(' ')
                idx.append(m.start())
            continue
        for k, ch in enumerate(t):
            chars.append(ch)
            idx.append(m.start() + k)
    norm = ''.join(chars)
    pos = norm.find(needle)
    if pos < 0 or norm.find(needle, pos + 1) >= 0:
        return None
    start, end = idx[pos], idx[pos + len(needle) - 1] + 1
    m2 = re.match(r'\s*<!--.*?-->', raw[end:], flags=re.S)
    if m2:
        end += m2.end()
    return start, end


# ---------------------------------------------------------------- decisions

def load_decisions():
    p = CFG['decisions']
    if p.exists():
        return json.loads(p.read_text(encoding='utf-8'))
    return {}


def save_decisions(d):
    p = CFG['decisions']
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(d, indent=1, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    os.replace(tmp, p)


def backup(path):
    bdir = CFG['backups']
    bdir.mkdir(parents=True, exist_ok=True)
    dest = bdir / f'{path.stem}.{time.strftime("%Y%m%d-%H%M%S")}{path.suffix}'
    dest.write_bytes(path.read_bytes())


def write_atomic(path, text):
    tmp = path.with_name(path.name + '.tmp-review')
    tmp.write_text(text, encoding='utf-8')
    os.replace(tmp, path)


# ---------------------------------------------------------------- scan images

_pdf = None
_img_cache = {}


def render(page, part, scale):
    global _pdf
    key = (page, part, scale)
    if key in _img_cache:
        return _img_cache[key]
    import pypdfium2 as pdfium  # may raise ImportError
    if _pdf is None:
        _pdf = pdfium.PdfDocument(str(CFG['pdf']))
    im = _pdf[page - 1].render(scale=scale).to_pil().convert('RGB')
    w, h = im.size
    my, pad = h // 2, h // 20
    box = (0, 0, w, my + pad) if part == 'top' else (0, my - pad, w, h)
    buf = io.BytesIO()
    im.crop(box).save(buf, format='JPEG', quality=88)
    data = buf.getvalue()
    if len(_img_cache) > 40:
        _img_cache.clear()
    _img_cache[key] = data
    return data


# ---------------------------------------------------------------- http

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype='application/json'):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode('utf-8')
        elif isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype + ('; charset=utf-8' if ctype.startswith('text') or ctype == 'application/json' else ''))
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def body(self):
        n = int(self.headers.get('Content-Length') or 0)
        return json.loads(self.rfile.read(n) or b'{}')

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            if u.path == '/':
                return self.send(200, HTML, 'text/html')
            if u.path == '/api/items':
                items = parse_checklist(CFG['checklist'])
                dec = load_decisions()
                for it in items:
                    it['decision'] = dec.get(it['id'])
                return self.send(200, {'items': items, 'pdf': CFG['pdf'].exists()})
            if u.path == '/api/context':
                it = next((i for i in parse_checklist(CFG['checklist']) if i['id'] == q.get('id')), None)
                if not it:
                    return self.send(404, {'error': 'no such item'})
                raw = page_path(it['page']).read_text(encoding='utf-8')
                loc = locate(raw, it['snippet'])
                if not loc:
                    return self.send(200, {'found': False, 'page_text': raw})
                s, e = loc
                return self.send(200, {'found': True, 'before': raw[max(0, s - 220):s], 'target': raw[s:e],
                                       'after': raw[e:e + 220]})
            if u.path == '/img':
                page, part, scale = int(q['page']), q.get('part', 'top'), float(q.get('scale', 3))
                try:
                    data = render(page, part, min(max(scale, 1), 8))
                except ImportError:
                    return self.send(501, {'error': 'pypdfium2/pillow not installed'})
                except Exception as ex:  # missing PDF etc.
                    return self.send(500, {'error': str(ex)})
                return self.send(200, data, 'image/jpeg')
            return self.send(404, {'error': 'not found'})
        except Exception as ex:
            return self.send(500, {'error': repr(ex)})

    def do_POST(self):
        u = urlparse(self.path)
        try:
            b = self.body()
            with LOCK:
                if u.path == '/api/decide':
                    dec = load_decisions()
                    dec[b['id']] = {'status': b['status'], 'note': b.get('note', ''), 'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                                    'page': b.get('page')}
                    save_decisions(dec)
                    return self.send(200, {'ok': True})
                if u.path == '/api/apply':
                    it = next((i for i in parse_checklist(CFG['checklist']) if i['id'] == b['id']), None)
                    if not it:
                        return self.send(404, {'error': 'no such item'})
                    path = page_path(it['page'])
                    raw = path.read_text(encoding='utf-8')
                    loc = locate(raw, it['snippet'])
                    if not loc:
                        return self.send(409, {'error': 'the text has changed; use the full-page editor'})
                    s, e = loc
                    old = raw[s:e]
                    new = b['new_text']
                    if new == old:
                        return self.send(200, {'ok': True, 'unchanged': True})
                    backup(path)
                    write_atomic(path, raw[:s] + new + raw[e:])
                    dec = load_decisions()
                    dec[it['id']] = {'status': 'changed', 'note': b.get('note', ''), 'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                                     'page': it['page'], 'was': old, 'now': new}
                    save_decisions(dec)
                    return self.send(200, {'ok': True})
                if u.path == '/api/savepage':
                    path = page_path(int(b['page']))
                    if not b['text'].startswith(f"<!-- PDF page {int(b['page']):03d} -->"):
                        return self.send(400, {'error': 'the first line must stay the PDF page comment'})
                    backup(path)
                    write_atomic(path, b['text'])
                    return self.send(200, {'ok': True})
                if u.path == '/api/rebuild':
                    out = []
                    for script in ('compile_markdown.py', 'make_plaintext.py', 'make_sparse.py'):
                        r = subprocess.run([sys.executable, str(ROOT / 'tools' / script),
                                            *CFG['rebuild_args'].get(script, [])],
                                           capture_output=True, text=True, cwd=str(ROOT))
                        out.append(f'$ {script}\n{r.stdout}{r.stderr}')
                    return self.send(200, {'ok': True, 'output': '\n'.join(out)})
            return self.send(404, {'error': 'not found'})
        except Exception as ex:
            return self.send(500, {'error': repr(ex)})


HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Review checklist</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#fbfaf6;--fg:#1d1b17;--mut:#6b665c;--card:#fff;--line:#ddd7c9;--acc:#7a3b12;--ok:#2b6b3a;--chg:#8a4b00;--skip:#555}
@media(prefers-color-scheme:dark){:root{--bg:#171512;--fg:#ece7dc;--mut:#a39d8f;--card:#201d19;--line:#3a352d;--acc:#e0a16a;--ok:#7bc58c;--chg:#e6b35c;--skip:#9a9a9a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif}
header{padding:10px 16px;border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header h1{font-size:16px;margin:0}header .sp{flex:1}
select,button,textarea{font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:6px 10px}
button{cursor:pointer}button:hover{border-color:var(--acc)}button.p{background:var(--acc);color:#fff;border-color:var(--acc)}
main{display:grid;grid-template-columns:300px 1fr;min-height:calc(100vh - 53px)}
#list{border-right:1px solid var(--line);overflow:auto;max-height:calc(100vh - 53px)}
#list div{padding:7px 12px;border-bottom:1px solid var(--line);cursor:pointer;font-size:13px}
#list div.cur{background:var(--card);outline:2px solid var(--acc);outline-offset:-2px}
.tag{display:inline-block;font-size:11px;padding:0 6px;border-radius:9px;border:1px solid var(--line);margin-left:6px}
.confirmed{color:var(--ok)}.changed{color:var(--chg)}.skipped{color:var(--skip)}
#view{padding:14px 20px;min-width:0}
.q{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin-bottom:10px}
.ctx{font:14px/1.5 ui-monospace,Menlo,monospace;white-space:pre-wrap;color:var(--mut)}
textarea{width:100%;min-height:90px;font:14px/1.5 ui-monospace,Menlo,monospace}
.row{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0;align-items:center}
.imgs img{width:100%;border:1px solid var(--line);border-radius:6px;margin-top:8px;cursor:zoom-in}
small,.mut{color:var(--mut)}kbd{border:1px solid var(--line);border-radius:4px;padding:0 4px;font-size:12px}
#msg{min-height:20px;font-size:13px}
</style></head><body>
<header><h1>Review checklist</h1>
<select id="fg"><option value="">All groups</option></select>
<select id="fs"><option value="pending">Pending</option><option value="">All</option><option value="confirmed">Confirmed</option><option value="changed">Changed</option><option value="skipped">Skipped</option></select>
<select id="fc"><option value="">Any confidence</option><option>low</option><option>medium</option><option>high</option></select>
<span id="count" class="mut"></span><span class="sp"></span>
<button id="rebuild" title="Rebuild the three combined files from the page files">Rebuild compiled files</button></header>
<main><div id="list"></div><div id="view"><p class="mut">Loading…</p></div></main>
<script>
let ITEMS=[],SHOW=[],CUR=null,CTX=null;const $=s=>document.querySelector(s);
const st=i=>i.decision?i.decision.status:'pending';
async function api(p,b){const r=await fetch(p,b?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}:{});return r.json()}
async function load(keep){const d=await api('/api/items');ITEMS=d.items;window.HASPDF=d.pdf;
 const gs=[...new Set(ITEMS.map(i=>i.group))];const fg=$('#fg'),cur=fg.value;fg.innerHTML='<option value="">All groups</option>'+gs.map(g=>`<option>${g}</option>`).join('');fg.value=cur;refresh(keep)}
function refresh(keep){const g=$('#fg').value,s=$('#fs').value,c=$('#fc').value;
 SHOW=ITEMS.filter(i=>(!g||i.group==g)&&(!s||st(i)==s)&&(!c||i.confidence==c)).sort((a,b)=>a.page-b.page);
 $('#count').textContent=SHOW.length+' shown · '+ITEMS.filter(i=>st(i)=='pending').length+' pending of '+ITEMS.length;
 $('#list').innerHTML=SHOW.map(i=>`<div data-id="${i.id}" class="${CUR&&CUR.id==i.id?'cur':''}">p. ${i.page} <span class="tag ${st(i)}">${st(i)}</span><span class="tag">${i.confidence}</span><br><span class="mut">${esc(i.question).slice(0,70)}</span></div>`).join('');
 document.querySelectorAll('#list div').forEach(d=>d.onclick=()=>openItem(d.dataset.id));
 if(keep&&CUR&&SHOW.find(i=>i.id==CUR.id))return;if(SHOW.length)openItem(SHOW[0].id);else{CUR=null;$('#view').innerHTML='<p class="mut">Nothing to show with these filters.</p>'}}
const esc=t=>String(t).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
async function openItem(id){CUR=ITEMS.find(i=>i.id==id);document.querySelectorAll('#list div').forEach(d=>d.classList.toggle('cur',d.dataset.id==id));
 const c=await api('/api/context?id='+id);CTX=c;const i=CUR;
 let ed;if(c.found)ed=`<div class="ctx">${esc(c.before)}</div><textarea id="ed" spellcheck="false">${esc(c.target)}</textarea><div class="ctx">${esc(c.after)}</div>`;
 else ed=`<p class="mut">${i.snippet=='(whole page)'?'This item concerns the whole page.':'The text has changed since the checklist was made.'} Edit the page below if needed.</p><textarea id="full" spellcheck="false" style="min-height:260px">${esc(c.page_text||'')}</textarea>`;
 $('#view').innerHTML=`<div class="q"><b>PDF page ${i.page}</b> · printed ${i.printed} · <span class="tag">${i.group}</span> <span class="tag">${i.confidence} confidence</span>
 <div style="margin-top:6px"><b>Check:</b> ${esc(i.question)}</div><div><b>Other reading:</b> ${esc(i.alt)}</div></div>${ed}
 <div class="row"><button class="p" id="b-conf">Confirm as is <kbd>c</kbd></button><button id="b-save">Save my edit <kbd>⌘/Ctrl-Enter</kbd></button><button id="b-skip">Skip <kbd>s</kbd></button>
 <button id="b-prev"><kbd>←</kbd> Prev</button><button id="b-next">Next <kbd>→</kbd></button><input id="note" placeholder="optional note" style="flex:1;min-width:140px;border:1px solid var(--line);border-radius:6px;padding:6px 10px;background:var(--card);color:inherit"></div>
 <div id="msg"></div><div class="imgs">${HASPDF?`<img src="/img?page=${i.page}&part=top&scale=3" onclick="window.open('/img?page=${i.page}&part=top&scale=6')"><img src="/img?page=${i.page}&part=bottom&scale=3" onclick="window.open('/img?page=${i.page}&part=bottom&scale=6')"><small class="mut">Top and bottom halves of the page (click an image for a larger view).</small>`:`<p class="mut">The PDF or pypdfium2 is not available here: open Book-of-Mormon-1830.pdf at page ${i.page}.</p>`}</div>`;
 $('#b-conf').onclick=()=>decide('confirmed');$('#b-skip').onclick=()=>decide('skipped');$('#b-save').onclick=save;$('#b-next').onclick=()=>step(1);$('#b-prev').onclick=()=>step(-1)}
async function decide(status){await api('/api/decide',{id:CUR.id,status,note:$('#note').value,page:CUR.page});await after()}
async function save(){let r;if(CTX.found){r=await api('/api/apply',{id:CUR.id,new_text:$('#ed').value,note:$('#note').value})}else{r=await api('/api/savepage',{page:CUR.page,text:$('#full').value});if(r.ok)await api('/api/decide',{id:CUR.id,status:'changed',note:$('#note').value,page:CUR.page})}
 if(r.error){$('#msg').textContent='Not saved: '+r.error;return}await after()}
async function after(){const k=CUR.id;const idx=SHOW.findIndex(i=>i.id==k);await load(true);const nxt=SHOW[idx]||SHOW[SHOW.length-1];if(nxt)openItem(nxt.id)}
function step(d){const idx=SHOW.findIndex(i=>CUR&&i.id==CUR.id);const n=SHOW[idx+d];if(n)openItem(n.id)}
document.addEventListener('keydown',e=>{const t=document.activeElement.tagName;if((e.metaKey||e.ctrlKey)&&e.key=='Enter'){save();return}if(t=='TEXTAREA'||t=='INPUT')return;
 if(e.key=='c')decide('confirmed');else if(e.key=='s')decide('skipped');else if(e.key=='ArrowRight')step(1);else if(e.key=='ArrowLeft')step(-1)});
['fg','fs','fc'].forEach(x=>$('#'+x).onchange=()=>refresh(false));
$('#rebuild').onclick=async()=>{$('#rebuild').textContent='Rebuilding…';const r=await api('/api/rebuild',{});$('#rebuild').textContent='Rebuild compiled files';alert(r.output||'done')};
load(false);
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', type=int, default=8765)
    ap.add_argument('--no-browser', action='store_true')
    ap.add_argument('--pages-dir', default=str(ROOT / 'book-of-mormon-1830-pages'))
    ap.add_argument('--checklist', default=str(ROOT / 'review-checklist.md'))
    ap.add_argument('--pdf', default=str(ROOT / 'Book-of-Mormon-1830.pdf'))
    ap.add_argument('--decisions', default=str(ROOT / 'review-decisions.json'))
    args = ap.parse_args()
    CFG.update(pages=Path(args.pages_dir), checklist=Path(args.checklist), pdf=Path(args.pdf),
               decisions=Path(args.decisions), backups=ROOT / 'work' / 'review-backups', rebuild_args={})
    if Path(args.pages_dir).resolve() != (ROOT / 'book-of-mormon-1830-pages').resolve():
        CFG['rebuild_args'] = {'compile_markdown.py': ['--pages-dir', args.pages_dir, '--out', str(Path(args.decisions).with_suffix('.test.md'))],
                               'make_plaintext.py': ['--md', str(Path(args.decisions).with_suffix('.test.md')), '--out', str(Path(args.decisions).with_suffix('.test.txt'))],
                               'make_sparse.py': ['--md', str(Path(args.decisions).with_suffix('.test.md')), '--out', str(Path(args.decisions).with_suffix('.test-sparse.txt'))]}
    srv = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    url = f'http://127.0.0.1:{args.port}'
    print(f'Review app running at {url}  (Ctrl-C to stop)')
    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\nstopped')


if __name__ == '__main__':
    main()
