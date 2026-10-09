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
from dictionary_data_books_ot import OT
from dictionary_data_books_nt import NT

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dictionary")
SITE = "https://crossero.com"
TODAY = date.today().isoformat()
BOOKS = OT + NT
ENTRIES = PEOPLE + EVENTS + PLACES + BOOKS
BY_SLUG = {e["slug"]: e for e in ENTRIES}
TYPE_ORDER = [("인물", "성경 인물"), ("사건", "성경 사건"), ("지명", "성경 지명")]
BOOK_GROUPS = [("구약", ["모세오경", "역사서", "시가서", "대선지서", "소선지서"]), ("신약", ["복음서", "역사서", "바울서신", "일반서신", "예언서"])]

GA = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-DN6WXRL3CV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-DN6WXRL3CV');</script>
<script type="text/javascript">(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","vin36biyig");</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-0717185892763061" crossorigin="anonymous"></script>"""

NAV = """<nav class="nav">
  <a href="/index.html" class="nav-item">홈</a>
  <a href="/play.html" class="nav-item">퍼즐하기</a>
  <a href="/list.html" class="nav-item">퍼즐목록</a>
  <a href="/dictionary/" class="nav-item nav-active">성경사전</a>
  <a href="/posts/index.html" class="nav-item">게시판</a>
  <a href="/about.html" class="nav-item">소개</a>
  <a href="/supporters.html" class="nav-item">⭐ 후원자</a>
  <a href="/support.html" class="nav-item">후원하기</a>
  <a href="/faq.html" class="nav-item">FAQ</a>
</nav>"""

FOOTER = """<footer>
  <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-bottom:16px;">
    <a href="/teachers/" style="font-size:13px;color:#666;text-decoration:none;">교사 허브</a>
    <a href="/bible-crossword.html" style="font-size:13px;color:#666;text-decoration:none;">성경 십자말풀이</a>
    <a href="/how-to-crossword.html" style="font-size:13px;color:#666;text-decoration:none;">십자말풀이 하는 법</a>
    <a href="/church-bulletin-puzzle.html" style="font-size:13px;color:#666;text-decoration:none;">교회·주일학교 활용</a>
    <a href="/editorial-policy.html" style="font-size:13px;color:#666;text-decoration:none;">콘텐츠 제작 원칙</a>
    <a href="/terms.html" style="font-size:13px;color:#666;text-decoration:none;">이용약관</a>
    <a href="/privacy.html" style="font-size:13px;color:#666;text-decoration:none;">개인정보처리방침</a>
    <a href="/faq.html" style="font-size:13px;color:#666;text-decoration:none;">FAQ</a>
    <a href="mailto:mandubird@naver.com" style="font-size:13px;color:#666;text-decoration:none;">문의</a>
  </div>
  <p style="font-size:12px;color:#aaa;">© 2025 십자가로세로. All rights reserved.</p>
</footer>"""

CSS = """* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Apple SD Gothic Neo','Noto Sans KR',sans-serif; background:#f8f9fa; color:#333; line-height:1.8; }
a { color:#0073e6; }
.nav { display:flex; justify-content:center; gap:10px; background:#fff; border-bottom:1px solid #e5e5e5; padding:12px 0; flex-wrap:wrap; }
.nav-item { padding:8px 14px; font-size:14px; color:#444; text-decoration:none; border-radius:6px; white-space:nowrap; }
.nav-item:hover { background:#f0f6ff; color:#0073e6; }
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
    out.append(f'<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › {esc(e["name"])}</div>')
    out.append(f'<span class="badge">{esc(e["type"])}</span>')
    out.append(f'<h1>{esc(e["name"])}</h1><div class="sub">{esc(e["sub"])}</div>')
    out.append(f'<div class="summary">{esc(e["summary"])}</div>')
    out.append(f'<figure class="hero"><img src="/images/dictionary/{e["slug"]}-bible-dictionary.png" width="1200" height="630" alt="{esc(e["name"])} - {esc(e["sub"])} 성경사전 안내 이미지" fetchpriority="high"></figure>')
    out.append('<div class="facts">' + "".join(
        f'<div class="fact"><b>{esc(k)}</b><span>{esc(v)}</span></div>' for k, v in e["facts"]) + '</div>')
    for h, paras in e["sections"]:
        out.append(f"<h2>{esc(h)}</h2>")
        out += [f"<p>{esc(p)}</p>" for p in paras]
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
    out.append('</main><div id="crs-subscribe"></div>')
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
    out.append('</main><div id="crs-subscribe"></div>')
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- DICT-START -->.*?<!-- DICT-END -->", "", s, flags=re.S)
    urls = [("/dictionary/", "0.8")] + [(f"/dictionary/{e['slug']}.html", "0.7") for e in ENTRIES]
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
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(render_index())
    open(os.path.join(OUT, "style.css"), "w", encoding="utf-8").write(CSS)
    update_sitemap()
    print(f"생성 완료: {len(ENTRIES)}개 항목 + 인덱스")


if __name__ == "__main__":
    main()
