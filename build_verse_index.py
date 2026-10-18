# -*- coding: utf-8 -*-
"""구절로 찾기 인덱스(/dictionary/verses/): 성경 구절 → 관련 사전 항목(인물·사건·지명·용어)."""
import json
import os
import re

from verse_lib import KO_BOOKS, eng_slug, load_text

REF_RE = re.compile(r"^(.+?)\s+(\d+)(?::(\d+))?(?:[-–](?:(\d+):)?(\d+))?$")
CSS = """<style>
.vi-search{display:flex;gap:8px;margin:14px 0 6px}.vi-search input{flex:1;padding:14px 16px;font-size:16px;border:2px solid #cfe0f7;border-radius:14px;font-family:inherit;box-sizing:border-box}
.vi-search button{padding:0 20px;border:0;background:#0073e6;color:#fff;font-weight:700;border-radius:14px;font-size:15px;cursor:pointer}
.vi-msg{margin:8px 0;padding:12px 14px;background:#fff8ec;border:1px solid #fcd9a8;border-radius:12px;color:#7a4a00;display:none}
.vi-msg a{display:inline-block;margin-top:8px;background:#d97706;color:#fff!important;padding:8px 14px;border-radius:18px;font-weight:700;text-decoration:none}
.vrow{background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:12px 14px;margin:10px 0;scroll-margin-top:110px}
.vrow.hit{border-color:#0073e6;box-shadow:0 0 0 3px rgba(0,115,230,.18)}
.vrow .vr{font-weight:700;color:#0b5cad}.vrow .vt{margin:6px 0 8px;color:#445;font-size:15px;line-height:1.75}.vrow .vt b{color:#8a97a6;font-size:12px;margin-right:4px}
.vents{display:flex;flex-direction:column;gap:6px}.vent{display:flex;gap:8px;align-items:baseline;text-decoration:none!important;color:#222!important;padding:6px 8px;border-radius:8px;background:#f7faff}
.vent:hover{background:#e8f1ff}.vent i{font-style:normal;font-size:11px;background:#e1ecfb;color:#33506e;border-radius:10px;padding:1px 8px;white-space:nowrap}
.vent span{font-size:13px;color:#667}
.bgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:8px 0 22px}.bgrid a{display:block;background:#fff;border:1px solid #e5e5e5;border-radius:10px;padding:10px 12px;text-decoration:none;color:#222}
.bgrid a:hover{border-color:#0073e6}.bgrid em{font-style:normal;color:#0073e6;font-size:12px;display:block}
@media(max-width:600px){.bgrid{grid-template-columns:repeat(2,1fr)}}
</style>"""


def parse(ref):
    m = REF_RE.match(ref.strip())
    if m and m.group(1) in KO_BOOKS:
        b, c1, v1, c2or, v2 = m.group(1), int(m.group(2)), m.group(3), m.group(4), m.group(5)
        v1 = int(v1) if v1 else 1
        c2 = int(c2or) if c2or else c1
        v2 = int(v2) if v2 else (v1 if m.group(3) else 999)
        if not m.group(3):  # 장 전체
            v1, v2 = 1, 999
        return b, c1, v1, c2, v2
    m = re.match(r"^(.+?)\s+(\d+)편$", ref.strip())
    if m and m.group(1) in KO_BOOKS:
        return m.group(1), int(m.group(2)), 1, int(m.group(2)), 999
    return None


def collect(ENTRIES, TYPE_LABEL):
    rows = {}  # (book,c1,v1,c2,v2) -> [(entry, note)]
    for e in ENTRIES:
        for ref, note in e["refs"]:
            p = parse(ref)
            if not p:
                continue
            rows.setdefault(p, []).append((e, note, ref))
    return rows


def anchor(ref):
    p = parse(ref)
    if not p:
        return None
    return f"/dictionary/verses/{eng_slug(p[0])}.html#c{p[1]}v{p[2]}"


def render_all(ctx):
    ENTRIES, head, esc, FOOTER, SITE, OUT = (ctx[k] for k in ("ENTRIES", "head", "esc", "FOOTER", "SITE", "OUT"))
    from site_chrome import TYPE2CAT
    rows = collect(ENTRIES, None)
    text = load_text()
    bidx = {b: i + 1 for i, b in enumerate(KO_BOOKS)}
    by_book = {}
    for p, items in rows.items():
        by_book.setdefault(p[0], []).append((p, items))
    vdir = os.path.join(OUT, "verses")
    os.makedirs(vdir, exist_ok=True)

    def vtext(p):
        b, c1, v1, c2, v2 = p
        if c1 != c2 or v2 == 999 or v2 - v1 > 3:
            return ""
        parts = []
        for v in range(v1, v2 + 1):
            t = text.get((bidx[b], c1, v))
            if t:
                parts.append(f'<b>{v}</b>{esc(t)}')
        return " ".join(parts)

    def label(p):
        b, c1, v1, c2, v2 = p
        if v2 == 999:
            return f"{b} {c1}장"
        if c1 != c2:
            return f"{b} {c1}:{v1}–{c2}:{v2}"
        return f"{b} {c1}:{v1}" + (f"-{v2}" if v2 != v1 else "")

    books_meta = []
    for b in KO_BOOKS:
        if b not in by_book:
            continue
        slug = eng_slug(b)
        lst = sorted(by_book[b], key=lambda x: (x[0][1], x[0][2], x[0][3], x[0][4]))
        path = f"/dictionary/verses/{slug}.html"
        title = f"{b} 구절 찾아보기 - 관련 인물·사건·지명 | 성경사전 | 십자가로세로"
        desc = f"{b}의 구절별로 관련된 성경 인물, 사건, 지명, 신앙 용어를 한곳에 모았습니다. {b} 본문에서 궁금한 구절을 찾아 사전 항목으로 이동하세요."
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "성경사전", "item": SITE + "/dictionary/"},
                {"@type": "ListItem", "position": 3, "name": "구절로 찾기", "item": SITE + "/dictionary/verses/"},
                {"@type": "ListItem", "position": 4, "name": b, "item": SITE + path}]}, ensure_ascii=False) + "</script>"
        out = [head(title, desc, path, ld).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
        out.append(f'<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › <a href="/dictionary/verses/">구절로 찾기</a> › {esc(b)}</div>')
        out.append(f'<h1>{esc(b)} 구절 찾아보기</h1><div class="sub">구절에서 인물·사건·지명 항목으로 바로 이동하세요</div>')
        out.append('<div class="vi-msg" id="vimsg"></div>')
        be = next((x for x in ENTRIES if x["slug"] == "book-" + slug), None)
        if be:
            facts = "".join(f"<li><b>{esc(k)}</b> {esc(v)}</li>" for k, v in be["facts"])
            para = be["sections"][0][1][0] if be["sections"] and be["sections"][0][1] else ""
            out.append(f'<h2>{esc(b)} 소개</h2><p>{esc(be["summary"])}</p>' + (f"<ul>{facts}</ul>" if facts else "") + (f"<p>{esc(para)}</p>" if para else "")
                       + f'<p><a href="/dictionary/{be["slug"]}.html">{esc(b)} 요약 전체 보기 →</a> · 아래는 사전 항목에서 인용한 {esc(b)}의 구절과 관련 항목입니다.</p>')
        cur = None
        used = set()
        for p, items in lst:
            if p[1] != cur:
                cur = p[1]
                out.append(f'<h2 id="c{cur}">{esc(b)} {cur}장</h2>')
            ents = "".join(
                f'<a class="vent" href="/dictionary/{e["slug"]}.html"><i>{esc(TYPE2CAT[e["type"]][2] if e["type"] in TYPE2CAT else e["type"])}</i><b>{esc(e["name"])}</b><span>{esc(note)}</span></a>'
                for e, note, _ in items)
            tx = vtext(p)
            rid = f"c{p[1]}v{p[2]}"
            idattr = "" if rid in used else f' id="{rid}"'
            used.add(rid)
            out.append(f'<div class="vrow"{idattr} data-c1="{p[1]}" data-v1="{p[2]}" data-c2="{p[3]}" data-v2="{p[4]}">'
                       f'<div class="vr">{esc(label(p))}</div>' + (f'<div class="vt">{tx}</div>' if tx else "") + f'<div class="vents">{ents}</div></div>')
        body_txt = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", re.sub(r"<script.*?</script>|<style.*?</style>", "", "".join(out[1:]), flags=re.S)))
        thin = len(body_txt) < 800
        if thin:
            out[0] = out[0].replace("</head>", '<meta name="robots" content="noindex,follow">\n</head>', 1)
        out.append("</main>")
        out.append(FOOTER)
        out.append("""<script>(function(){var m=location.hash.match(/^#c(\\d+)v(\\d+)$/);if(!m)return;var c=+m[1],v=+m[2],f=null;
document.querySelectorAll('.vrow').forEach(function(r){var c1=+r.dataset.c1,v1=+r.dataset.v1,c2=+r.dataset.c2,v2=+r.dataset.v2;
var a=c*1000+v,s=c1*1000+v1,e=c2*1000+(v2===999?998:v2);if(a>=s&&a<=e){r.classList.add('hit');if(!f)f=r;}});
if(f){f.scrollIntoView({block:'center'});}else{var b=document.getElementById('vimsg');b.style.display='block';
var q='""" + b + """ '+c+':'+v;b.innerHTML='이 구절('+q+')과 연결된 사전 항목은 아직 없어요.<br><a href="mailto:mandubird@naver.com?subject='+encodeURIComponent('[십자가로세로] 구절 연결 요청: '+q)+'&body='+encodeURIComponent('요청 구절: '+q+'\\n페이지: '+location.href)+'" data-ga="verse_request">✉️ 이 구절에 대한 항목을 요청하기</a>';}})();</script>""")
        out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
        open(os.path.join(vdir, f"{slug}.html"), "w", encoding="utf-8").write("\n".join(out))
        books_meta.append({"b": b, "slug": slug, "n": len(lst), "testament": "구약" if bidx[b] <= 39 else "신약", "thin": thin})
    # 인덱스
    path = "/dictionary/verses/"
    title = "구절로 찾기 - 성경 구절에서 인물·사건·지명 찾기 | 성경사전 | 십자가로세로"
    desc = "성경 구절(예: 창세기 12:1)을 입력하면 관련 인물, 사건, 지명, 신앙 용어 항목으로 이동합니다. 책별로 구절과 사전 항목을 한눈에 볼 수 있어요."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "name": "구절로 찾기", "description": desc, "inLanguage": "ko", "url": SITE + path}, ensure_ascii=False) + "</script>"
    out = [head(title, desc, path, ld).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › 구절로 찾기</div>')
    out.append('<h1>📖 구절로 찾기</h1><div class="sub">성경 구절에서 관련 인물·사건·지명으로 바로 이동합니다</div>')
    out.append('<form class="vi-search" id="vif"><input id="viq" type="search" placeholder="예: 창세기 12:1, 요한복음 3:16, 시편 23" autocomplete="off"><button type="submit">찾기</button></form>')
    out.append('<div class="vi-msg" id="vimsg"></div>')
    for tst in ("구약", "신약"):
        its = [m for m in books_meta if m["testament"] == tst]
        out.append(f'<h2>{tst} ({len(its)}권)</h2><div class="bgrid">' + "".join(
            f'<a href="/dictionary/verses/{m["slug"]}.html"><b>{esc(m["b"])}</b><em>연결된 구절 {m["n"]}곳</em></a>' for m in its) + "</div>")
    out.append('<p style="font-size:14px;color:#556;line-height:1.8">사전 항목에 인용된 성경 구절을 기준으로 정리한 목록입니다. 항목이 늘어나면 구절도 함께 늘어납니다. 찾는 구절이 없으면 요청해 주세요.</p>')
    out.append("</main>")
    out.append(FOOTER)
    names = {m["b"]: m["slug"] for m in books_meta}
    out.append("<script>(function(){var B=" + json.dumps(names, ensure_ascii=False) + """;var f=document.getElementById('vif'),q=document.getElementById('viq'),m=document.getElementById('vimsg');
f.addEventListener('submit',function(e){e.preventDefault();var s=q.value.trim().replace(/편$/,''),r=s.match(/^(.+?)\\s*(\\d+)(?:\\s*[:장]\\s*(\\d+))?/);
if(!r){m.style.display='block';m.textContent='책 이름과 장·절을 입력해 주세요. 예: 창세기 12:1';return;}
var name=r[1].trim(),c=r[2],v=r[3]||'1',slug=B[name];
if(!slug){var k=Object.keys(B).filter(function(x){return x.indexOf(name)===0;});if(k.length)slug=B[k[0]];}
if(!slug){m.style.display='block';m.innerHTML='"'+name+'"에 연결된 구절이 아직 없어요.<br><a href="mailto:mandubird@naver.com?subject='+encodeURIComponent('[십자가로세로] 구절 연결 요청: '+s)+'" data-ga="verse_request">✉️ 요청하기</a>';return;}
if(window.crsTrack)crsTrack('verse_lookup',{q:s});location.href='/dictionary/verses/'+slug+'.html#c'+c+'v'+v;});})();</script>""")
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    open(os.path.join(vdir, "index.html"), "w", encoding="utf-8").write("\n".join(out))
    return books_meta
