# -*- coding: utf-8 -*-
"""성경 사전 정적 페이지 생성기.
실행: python3 build_dictionary.py
입력: dictionary_data_people.py, dictionary_data_events_places.py
출력: dictionary/*.html, dictionary/style.css, sitemap.xml 의 사전 구간
"""
import html
import json
import os
import re
from datetime import date

from dictionary_data_people import PEOPLE
from dictionary_data_events_places import EVENTS, PLACES
from dictionary_data_events2 import EVENTS2
from dictionary_data_places2 import PLACES2
from dictionary_data_terms import TERMS
from dictionary_data_books_ot import OT
from dictionary_data_books_nt import NT

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dictionary")
SITE = "https://crossero.com"
TODAY = date.today().isoformat()
BOOKS = OT + NT
from dictionary_data_books_deep import DEEP
from dictionary_data_books_deep2 import DEEP2
from dictionary_data_books_deep3 import DEEP3
DEEP = {**DEEP, **DEEP2, **DEEP3}
for _b in BOOKS:
    if _b["slug"] in DEEP:
        _secs = _b["sections"]
        _i = [h for h, _ in _secs].index("핵심 메시지와 읽는 법")
        _b["sections"] = _secs[:_i] + DEEP[_b["slug"]] + _secs[_i:]
ENTRIES = PEOPLE + EVENTS + EVENTS2 + PLACES + PLACES2 + TERMS + BOOKS
BY_SLUG = {e["slug"]: e for e in ENTRIES}
TYPE_ORDER = [("인물", "성경 인물"), ("사건", "성경 사건"), ("지명", "성경 지명"), ("신앙 용어", "신앙 용어")]
BOOK_GROUPS = [("구약", ["모세오경", "역사서", "시가서", "대선지서", "소선지서"]), ("신약", ["복음서", "역사서", "바울서신", "일반서신", "예언서"])]

GA = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-DN6WXRL3CV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-DN6WXRL3CV');</script>
<script type="text/javascript">(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","vin36biyig");</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-0717185892763061" crossorigin="anonymous"></script>"""

from site_chrome import nav_html, footer_html
from pilgrim_banner import banner as pilgrim_banner, PAUL_ENTRY_SLUGS
try:
    from dictionary_geo_data import GEO
except ImportError:
    GEO = {}

NAV = nav_html("dict")

FOOTER = f"""<footer>
{footer_html()}
  <p style="font-size:12px;color:#aaa;">© 2026 십자가로세로. All rights reserved.</p>
</footer>"""

CSS = """* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Apple SD Gothic Neo','Noto Sans KR',sans-serif; background:#f8f9fa; color:#333; line-height:1.8; }
a { color:#0073e6; }
.nav { display:flex; justify-content:center; gap:10px; background:#fff; border-bottom:1px solid #e5e5e5; padding:12px 0; flex-wrap:wrap; }
.nav-item { padding:8px 14px; font-size:14px; color:#444; text-decoration:none; border-radius:6px; white-space:nowrap; }
.nav-item:not(.nav-active):hover { background:#f0f6ff; color:#0073e6; }
.nav-active { background:#0073e6; color:#fff !important; font-weight:600; }
.wrap { max-width:780px; margin:0 auto; padding:28px 20px 48px; }
.crumb { font-size:13px; color:#888; margin-bottom:14px; }
.crumb a { color:#888; text-decoration:none; }
.badge { display:inline-block; background:#e8f1ff; color:#0b5cad; font-size:12px; font-weight:700; padding:3px 12px; border-radius:20px; }
h1 { font-size:30px; color:#16324f; margin:10px 0 4px; line-height:1.35; }
.sub { font-size:16px; color:#6b7b8d; margin-bottom:18px; }
.summary { background:#fff; border-left:4px solid #0073e6; padding:16px 18px; border-radius:8px; font-size:16px; margin-bottom:20px; }
.hero { margin:0 0 22px; } .hero img { width:100%; height:auto; border-radius:14px; display:block; }
.facts { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-bottom:28px; }
.fact { background:#fff; border:1px solid #e5e5e5; border-radius:10px; padding:10px 14px; }
.fact b { display:block; font-size:12px; color:#8a97a6; font-weight:600; }
.fact span { font-size:14px; }
.geo { background:#fff; border:1px solid #e5e5e5; border-radius:14px; padding:16px; margin:8px 0 26px; }
.geo h2 { margin-top:0; }
.geo-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.geo figure, .geo .gmap { margin:0; }
.geo img, .geo iframe { width:100%; height:220px; object-fit:cover; border:0; border-radius:10px; background:#eef2f6; display:block; }
.geo figcaption, .geo .gnote { font-size:12px; color:#7b8794; margin-top:6px; line-height:1.5; }
.geo dl { margin:12px 0 0; font-size:14px; }
.geo dt { display:inline; color:#8a97a6; font-weight:600; font-size:12px; }
.geo dd { display:inline; margin:0 12px 0 4px; }
@media (max-width:600px) { .geo-grid { grid-template-columns:1fr; } }
h2 { font-size:20px; color:#16324f; margin:30px 0 10px; padding-bottom:6px; border-bottom:2px solid #e8f1ff; }
.wrap p { margin-bottom:14px; font-size:16px; }
.refs { list-style:none; background:#fff; border:1px solid #e5e5e5; border-radius:12px; padding:6px 16px; }
.refs li { padding:10px 0; border-bottom:1px solid #f0f0f0; font-size:15px; }
.refs li:last-child { border-bottom:none; }
.refs b { color:#16324f; }
.note { font-size:13px; color:#888; margin-top:8px; }
.faq details { background:#fff; border:1px solid #e5e5e5; border-radius:10px; padding:12px 16px; margin-bottom:8px; }
.faq summary { font-weight:600; cursor:pointer; }
.faq p { margin:8px 0 0; font-size:15px; }
.cards { display:grid; grid-template-columns:repeat(2,1fr); gap:12px; }
.card { display:block; background:#fff; border:1px solid #e5e5e5; border-radius:12px; padding:14px 16px; text-decoration:none; color:#333; transition:transform .15s, box-shadow .15s; }
.card:hover { transform:translateY(-2px); box-shadow:0 6px 16px rgba(0,0,0,.08); border-color:#0073e6; }
.card b { display:block; font-size:16px; color:#16324f; }
.card span { font-size:13px; color:#6b7b8d; }
.cta { display:block; text-align:center; background:linear-gradient(135deg,#0073e6,#0052cc); color:#fff !important; text-decoration:none; font-weight:700; padding:16px; border-radius:14px; margin:26px 0 6px; font-size:16px; }
.cta small { display:block; font-weight:400; opacity:.85; font-size:13px; margin-top:2px; }
.idx-section h2 { margin-top:34px; }
.idx-group { font-size:15px; color:#6b7b8d; margin:18px 0 8px; }
footer { text-align:center; padding:32px 20px; background:#fff; border-top:1px solid #e5e5e5; }
@media (max-width:600px) { h1 { font-size:25px; } .facts, .cards { grid-template-columns:1fr; } .nav-item { padding:6px 10px; font-size:12px; } }
"""


def esc(s):
    return html.escape(s, quote=True)


def puzzle_titles():
    titles = {}
    for f in ("data.js", "data_bible_extra.js", "data_christian_figures.js"):
        s = open(os.path.join(ROOT, f), encoding="utf-8").read()
        for m in re.finditer(r'"([a-z]{3}_\d{3})":\s*\{\s*title:\s*"([^"]+)"', s):
            titles[m.group(1)] = m.group(2)
    return titles


TITLES = puzzle_titles()


def head(title, desc, path, extra_ld="", image=None):
    url = f"{SITE}{path}"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image or SITE + '/images/og-image.png'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/images/favicon.png" type="image/png">
<link rel="stylesheet" href="/dictionary/style.css">
{GA}
{extra_ld}
</head>
<body>
{NAV}
"""


def render_geo(e):
    g = GEO.get(e["slug"])
    if not g:
        return ""
    lat, lon = g["lat"], g["lon"]
    d = 0.02 if e["slug"] not in ("egypt",) else 1.0
    bbox = f"{lon-d},{lat-d*0.6},{lon+d},{lat+d*0.6}"
    embed = f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={lat},{lon}"
    big = f"https://www.openstreetmap.org/?mlat={lat}&amp;mlon={lon}#map=14/{lat}/{lon}"
    ob = f"https://www.openbible.info/geo/ancient/{g['ob_id']}/{g['ob_slug']}"
    out = [f'<section class="geo"><h2>{esc(e["name"])} 오늘의 모습</h2><div class="geo-grid">']
    if g.get("img"):
        out.append(f'<figure><img src="{g["img"]}" loading="lazy" alt="{esc(e["name"])} 현재 모습 사진"><figcaption>'
                   f'사진: <a href="{g["credit_url"]}" rel="noopener nofollow" target="_blank">{esc(g["credit"])}</a> · {esc(g["license"])}</figcaption></figure>')
    out.append(f'<div class="gmap"><iframe src="{embed}" loading="lazy" title="{esc(e["name"])} 현재 지도"></iframe>'
               f'<div class="gnote"><a href="{big}" rel="noopener nofollow" target="_blank">큰 지도에서 보기</a> · 지도 © OpenStreetMap 기여자</div></div>')
    out.append('</div>')
    out.append(f'<dl><dt>오늘의 위치</dt><dd>{esc(g["where"])}</dd><dt>현재 지명(추정)</dt><dd>{esc(g["modern"])}</dd>'
               f'<dt>성경 언급</dt><dd>{g["verses"]}절</dd></dl>')
    out.append(f'<p class="gnote">위치는 학자들의 식별을 모은 OpenBible.info 성경 지오코딩 데이터(CC BY 4.0)를 따르며, 일부 장소는 학설에 따라 달라질 수 있습니다. '
               f'<a href="{ob}" rel="noopener nofollow" target="_blank">원자료 보기</a> · <a href="/dictionary/map/">성경 지도에서 모든 지명 보기</a></p></section>')
    return "".join(out)


def _cat_crumb(e):
    from site_chrome import TYPE2CAT
    c = TYPE2CAT.get(e["type"])
    return f'<a href="/dictionary/{c[1]}/">{c[2]}</a> › ' if c else ""


def render_entry(e):
    path = f"/dictionary/{e['slug']}.html"
    if e["type"] == "성경 책":
        title = f"{e['name']} 요약 - 핵심 내용·구절·핵심 메시지 | 성경사전 | 십자가로세로"
    else:
        title = f"{e['name']} - {e['sub']} | 성경사전 | 십자가로세로"
    desc = e["summary"][:140]
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in e["faq"]],
    }
    img_wide = f"{SITE}/images/dictionary/{e['slug']}-bible-dictionary.png"
    img_sq = f"{SITE}/images/dictionary/{e['slug']}-bible-dictionary-square.png"
    article_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": (f"{e['name']} 요약" if e["type"] == "성경 책" else f"{e['name']} - {e['sub']}"), "description": e["summary"],
        "inLanguage": "ko", "dateModified": TODAY,
        "image": [img_wide, img_sq],
        "author": {"@type": "Organization", "name": "십자가로세로"},
        "publisher": {"@type": "Organization", "name": "십자가로세로", "url": SITE},
        "mainEntityOfPage": f"{SITE}{path}",
    }
    crumb_ld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "성경사전", "item": SITE + "/dictionary/"},
            {"@type": "ListItem", "position": 3, "name": e["name"], "item": SITE + path},
        ],
    }
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n'
                 for x in (article_ld, faq_ld, crumb_ld))

    out = [head(title, desc, path, ld, img_wide), '<main class="wrap">']
    out.append(f'<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › {_cat_crumb(e)}{esc(e["name"])}</div>')
    out.append(f'<span class="badge">{esc(e["type"])}</span>')
    out.append(f'<h1>{esc(e["name"])}</h1><div class="sub">{esc(e["sub"])}</div>')
    out.append(f'<div class="summary">{esc(e["summary"])}</div>')
    out.append(f'<figure class="hero"><img src="/images/dictionary/{e["slug"]}-bible-dictionary.png" width="1200" height="630" alt="{esc(e["name"])} - {esc(e["sub"])} 성경사전 안내 이미지" fetchpriority="high"></figure>')
    out.append('<div class="facts">' + "".join(
        f'<div class="fact"><b>{esc(k)}</b><span>{esc(v)}</span></div>' for k, v in e["facts"]) + '</div>')
    for h, paras in e["sections"]:
        out.append(f"<h2>{esc(h)}</h2>")
        out += [f"<p>{esc(p)}</p>" for p in paras]
    if e["slug"] in PAUL_ENTRY_SLUGS:
        out.append(pilgrim_banner(e["slug"], "place" if e["type"] == "지명" else "default"))
    out.append(render_geo(e))
    out.append("<h2>함께 읽을 본문</h2><ul class=\"refs\">" + "".join(
        f'<li><b>{esc(r)}</b> — {esc(n)}</li>' for r, n in e["refs"]) + "</ul>")
    out.append('<p class="note">성경 구절은 장·절 표기로 안내합니다. 본문은 사용하시는 번역본으로 직접 읽어 보세요.</p>')
    out.append('<h2>자주 묻는 질문</h2><div class="faq">' + "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in e["faq"]) + "</div>")

    if not e["puzzles"]:
        out.append(f'<a class="cta" href="/bible-crossword.html" data-ga="dictionary_to_puzzle" data-ga-label="{esc(e["slug"])}">🧩 성경 퍼즐 둘러보기<small>66권과 인물·사건 주제로 풀어 보는 가로세로 낱말퀴즈</small></a>')
    if e["puzzles"]:
        pid = e["puzzles"][0]
        out.append(f'<a class="cta" href="/play.html?id={pid}" data-ga="dictionary_to_puzzle" data-ga-label="{esc(e["slug"])}">'
                   f'🧩 {esc(TITLES.get(pid, e["name"] + " 퍼즐"))} 퍼즐 풀어보기'
                   f'<small>읽은 내용을 가로세로 낱말 퍼즐로 복습해 보세요</small></a>')
        if len(e["puzzles"]) > 1:
            out.append('<h2>관련 퍼즐</h2><div class="cards">' + "".join(
                f'<a class="card" href="/play.html?id={p}" data-ga="dictionary_to_puzzle" data-ga-label="{esc(e["slug"])}">'
                f'<b>{esc(TITLES.get(p, p))}</b><span>퍼즐 풀기 →</span></a>' for p in e["puzzles"]) + "</div>")

    rel = [BY_SLUG[s] for s in e["related"] if s in BY_SLUG]
    if e["type"] == "성경 책":
        i = BOOKS.index(e)
        for j in (i - 1, i + 1):
            if 0 <= j < len(BOOKS) and BOOKS[j] not in rel:
                rel.append(BOOKS[j])
    if rel:
        out.append('<h2>함께 보면 좋은 항목</h2><div class="cards">' + "".join(
            f'<a class="card" href="/dictionary/{r["slug"]}.html"><b>{esc(r["name"])}</b><span>{esc(r["type"])} · {esc(r["sub"])}</span></a>'
            for r in rel) + "</div>")
    out.append('</main>')
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


def render_index():
    path = "/dictionary/"
    title = "성경사전 - 성경 66권 요약과 인물·사건·지명 | 십자가로세로"
    desc = f"성경 66권 책별 요약과 인물·사건·지명 {len(ENTRIES)}개 항목을 쉽게 정리한 사전. 구절 위치와 자주 묻는 질문, 관련 퍼즐까지 함께 확인하세요."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "name": "성경사전",
        "description": desc, "inLanguage": "ko", "url": SITE + path,
        "hasPart": [{"@type": "Article", "name": e["name"], "url": f"{SITE}/dictionary/{e['slug']}.html"} for e in ENTRIES],
    }, ensure_ascii=False) + "</script>"
    out = [head(title, desc, path, ld), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › 성경사전</div>')
    out.append('<h1>성경사전</h1><div class="sub">성경 66권 요약, 인물 · 사건 · 지명을 쉽게 풀어 정리했습니다</div>')
    out.append('<div class="summary">각 항목은 성경 본문의 구절 위치를 기준으로 직접 정리했습니다. 읽고 나서 관련 가로세로 퍼즐을 풀며 내용을 복습할 수 있고, 주일학교·소그룹 준비에도 활용하실 수 있습니다. 해석이 갈리는 부분은 그렇다고 밝혀 두었습니다. 자세한 작성 원칙은 <a href="/editorial-policy.html">콘텐츠 제작 원칙</a>을 참고해 주세요.</div>')
    out.append('<a class="cta" href="/dictionary/map/">🗺️ 성경 지도 - 지명이 지금은 어디에 있을까?<small>예루살렘·갈릴리·여리고 등 지명의 오늘의 위치와 사진</small></a>')
    for typ, label in TYPE_ORDER:
        items = [e for e in ENTRIES if e["type"] == typ]
        if not items:
            continue
        out.append(f'<div class="idx-section"><h2>{label} ({len(items)})</h2><div class="cards">' + "".join(
            f'<a class="card" href="/dictionary/{e["slug"]}.html"><b>{esc(e["name"])}</b><span>{esc(e["sub"])}</span></a>'
            for e in items) + "</div></div>")
    for testament, groups in BOOK_GROUPS:
        items = [e for e in BOOKS if e["testament"] == testament]
        out.append(f'<div class="idx-section"><h2>{testament} 성경 책별 요약 ({len(items)}권)</h2>')
        for g in groups:
            gi = [e for e in items if e["group"] == g]
            if not gi:
                continue
            out.append(f'<h3 class="idx-group">{g}</h3><div class="cards">' + "".join(
                f'<a class="card" href="/dictionary/{e["slug"]}.html"><b>{esc(e["name"])}</b><span>{esc(e["sub"])}</span></a>' for e in gi) + "</div>")
        out.append("</div>")
    out.append('</main>')
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- DICT-START -->.*?<!-- DICT-END -->", "", s, flags=re.S)
    from build_routes import ROUTES as _R
    urls = [("/dictionary/", "0.8"), ("/dictionary/map/", "0.8")] + [(f"/dictionary/{c[1]}/", "0.8") for c in __import__("site_chrome").CATS] + [(f"/dictionary/map/{r['slug']}.html", "0.7") for r in _R]
    urls += [(f"/dictionary/{e['slug']}.html", "0.7") for e in ENTRIES]
    block = "\n  <!-- DICT-START -->\n" + "\n".join(
        f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for u, pr in urls) + "\n  <!-- DICT-END -->\n"
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    os.makedirs(OUT, exist_ok=True)
    slugs = set()
    for e in ENTRIES:
        assert e["slug"] not in slugs, e["slug"]
        slugs.add(e["slug"])
        for r in e["related"]:
            assert r in BY_SLUG, (e["slug"], r)
        for p in e["puzzles"]:
            assert p in TITLES, (e["slug"], p)
        open(os.path.join(OUT, f"{e['slug']}.html"), "w", encoding="utf-8").write(render_entry(e))
    from build_dict_categories import render_index as _ri, render_category as _rc
    from site_chrome import CATS as _CATS
    ctx = dict(ENTRIES=ENTRIES, BY_SLUG=BY_SLUG, head=head, esc=esc, FOOTER=FOOTER, SITE=SITE, BOOKS=BOOKS, BOOK_GROUPS=BOOK_GROUPS)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(_ri(ctx))
    for c in _CATS:
        os.makedirs(os.path.join(OUT, c[1]), exist_ok=True)
        open(os.path.join(OUT, c[1], "index.html"), "w", encoding="utf-8").write(_rc(c, ctx))
    from build_map_page import render_map
    os.makedirs(os.path.join(OUT, "map"), exist_ok=True)
    open(os.path.join(OUT, "map", "index.html"), "w", encoding="utf-8").write(render_map(GEO, BY_SLUG, head, esc, FOOTER, SITE))
    from build_routes import ROUTES, render_route
    for r in ROUTES:
        open(os.path.join(OUT, "map", f"{r['slug']}.html"), "w", encoding="utf-8").write(render_route(r, head, FOOTER, SITE, BY_SLUG))
    open(os.path.join(OUT, "style.css"), "w", encoding="utf-8").write(CSS)
    update_sitemap()
    print(f"생성 완료: {len(ENTRIES)}개 항목 + 인덱스")


if __name__ == "__main__":
    main()
