# -*- coding: utf-8 -*-
"""구절별 해설 페이지 생성. 실행: python3 build_verse_pages.py
입력: verse_commentary.py(해설), verse_picks.py(주제), BIBLE.csv(본문)
출력: verse/<책영문>-<장>-<절>.html, sitemap.xml 의 VERSEPG 구간"""
import json
import os
import re

import build_dictionary as bd
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT, TITLES
from verse_commentary import C
from verse_picks import PICKS
from verse_lib import KO_BOOKS, eng_slug, parse_ref, verse_slug, verse_url, load_text

BOOK_ENTRY = {b["name"]: b for b in bd.BOOKS}
TOPIC_OF = {}
for t, items in PICKS.items():
    for n, c, v in items:
        TOPIC_OF.setdefault(f"{n} {c}:{v}", t)

EXTRA_CSS = """
.vq{background:linear-gradient(180deg,#fffdf6,#f1f7ff);border:1px solid #d6e4f7;border-radius:16px;padding:26px 24px;margin:0 0 24px;text-align:center}
.vq p{font-size:20px;line-height:1.9;color:#1f2d3d;margin:0 0 10px;word-break:keep-all}
.vq .vr{font-size:15px;color:#6b7b8d;font-weight:600}
.ctx{background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:6px 18px}
.ctx p{margin:10px 0;font-size:15.5px}
.ctx .cur{background:#eef5ff;border-radius:8px;padding:6px 10px;font-weight:600}
.ctx b{color:#0b5cad;font-size:13px;margin-right:6px}
ul.qs{padding-left:20px}ul.qs li{margin:8px 0;font-size:16px}
.src{font-size:12.5px;color:#889;margin-top:18px}
"""


def render_page(ref, data, text, same_topic):
    name, c, v = parse_ref(ref)
    bi = KO_BOOKS.index(name) + 1
    slug = verse_slug(ref)
    path = f"/verse/{slug}.html"
    verse = text[(bi, c, v)]
    prev_t = text.get((bi, c, v - 1))
    next_t = text.get((bi, c, v + 1))
    topic = TOPIC_OF.get(ref, "말씀")
    book = BOOK_ENTRY[name]
    title = f"{ref} 뜻과 해설 - 말씀 묵상 | 십자가로세로"
    desc = f"{ref} '{verse[:38]}…' 말씀의 배경과 뜻을 쉽게 풀어 정리했습니다. 묵상 질문과 자주 묻는 질문, 말씀 카드 저장까지."
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in data["faq"]]}
    art_ld = {"@context": "https://schema.org", "@type": "Article", "headline": f"{ref} 뜻과 해설",
              "description": data["meaning"][:140], "inLanguage": "ko", "dateModified": bd.TODAY,
              "author": {"@type": "Organization", "name": "십자가로세로"},
              "publisher": {"@type": "Organization", "name": "십자가로세로", "url": SITE},
              "image": f"{SITE}/images/verse/{slug}.jpg", "mainEntityOfPage": SITE + path}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "말씀 뽑기", "item": SITE + "/verse/"},
        {"@type": "ListItem", "position": 3, "name": ref, "item": SITE + path}]}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (art_ld, faq_ld, crumb_ld))
    img_url = f"{SITE}/images/verse/{slug}.jpg"
    h = head(title, desc, path, ld, img_url).replace(NAV, NAV.replace(' nav-active', '')).replace("</head>", f"<style>{EXTRA_CSS}</style>\n</head>", 1)

    out = [h, '<main class="wrap">']
    out.append(f'<div class="crumb"><a href="/">홈</a> › <a href="/verse/">말씀 뽑기</a> › {esc(ref)}</div>')
    out.append(f'<span class="badge">{esc(topic)}</span>')
    out.append(f'<h1>{esc(ref)} 뜻과 해설</h1><div class="sub">{esc(name)} {c}장 {v}절 · 개역한글</div>')
    out.append(f'<div class="vq"><p>{esc(verse)}</p><div class="vr">{esc(ref)}</div></div>')
    out.append(f'<figure style="margin:0 0 22px"><img src="/images/verse/{slug}.jpg" width="1200" height="630" alt="{esc(ref)} 말씀 카드 - {esc(topic)}" style="width:100%;height:auto;border-radius:14px;display:block" loading="lazy"></figure>')
    out.append("<h2>말씀의 배경</h2>" + f"<p>{esc(data['who'])}</p>")
    out.append("<h2>이 말씀의 뜻</h2>" + f"<p>{esc(data['meaning'])}</p>")
    ctx = ""
    if prev_t:
        ctx += f'<p><b>{c}:{v-1}</b>{esc(prev_t)}</p>'
    ctx += f'<p class="cur"><b>{c}:{v}</b>{esc(verse)}</p>'
    if next_t:
        ctx += f'<p><b>{c}:{v+1}</b>{esc(next_t)}</p>'
    out.append("<h2>앞뒤 문맥</h2>" + f'<div class="ctx">{ctx}</div>')
    from pilgrim_banner import banner as _pb, PAUL_VERSE_PREFIXES
    if slug.startswith(PAUL_VERSE_PREFIXES):
        out.append(_pb(slug, "verse"))
    out.append("<h2>묵상 질문</h2><ul class=\"qs\">" + "".join(f"<li>{esc(q)}</li>" for q in data["points"]) + "</ul>")
    out.append('<h2>자주 묻는 질문</h2><div class="faq">' + "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in data["faq"]) + "</div>")
    out.append(f'<a class="cta" href="/verse/?v={esc(ref)}" data-ga="versepage_to_card" data-ga-label="{esc(ref)}">📖 이 말씀을 카드·책갈피로 저장하기<small>이미지 저장, 인쇄, 링크 공유</small></a>')
    rel = [r for r in same_topic if r != ref][:4]
    if rel:
        out.append(f'<h2>{esc(topic)} 주제의 다른 말씀</h2><div class="cards">' + "".join(
            f'<a class="card" href="{verse_url(r)}"><b>{esc(r)}</b><span>{esc(text[(KO_BOOKS.index(parse_ref(r)[0])+1, parse_ref(r)[1], parse_ref(r)[2])][:36])}…</span></a>'
            for r in rel) + "</div>")
    more = [f'<a class="card" href="/dictionary/{book["slug"]}.html"><b>{esc(name)} 요약</b><span>책의 흐름과 핵심 메시지 보기</span></a>']
    for pid in book["puzzles"][:2]:
        more.append(f'<a class="card" href="/play.html?id={pid}" data-ga="versepage_to_puzzle" data-ga-label="{pid}"><b>{esc(TITLES.get(pid, pid))}</b><span>퍼즐로 풀어 보기 →</span></a>')
    out.append("<h2>이 책을 더 읽어 보세요</h2><div class=\"cards\">" + "".join(more) + "</div>")
    out.append('<p class="src">본문: 성경전서 개역한글판(대한성서공회). 해설은 십자가로세로가 직접 작성했으며, 개인 묵상과 소모임 나눔용으로 제공합니다.</p>')
    out.append("</main>")
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


def update_sitemap(slugs):
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- VERSEPG-START -->.*?<!-- VERSEPG-END -->", "", s, flags=re.S)
    block = "\n  <!-- VERSEPG-START -->\n" + "\n".join(
        f"  <url>\n    <loc>{SITE}/verse/{sl}.html</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"
        for sl in slugs) + "\n  <!-- VERSEPG-END -->\n"
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    text = load_text()
    by_topic = {}
    for ref in C:
        by_topic.setdefault(TOPIC_OF.get(ref, "말씀"), []).append(ref)
    slugs = []
    for ref, data in C.items():
        name, c, v = parse_ref(ref)
        assert (KO_BOOKS.index(name) + 1, c, v) in text, ref
        for k in ("who", "meaning", "points", "faq"):
            assert data.get(k), (ref, k)
        html = render_page(ref, data, text, by_topic[TOPIC_OF.get(ref, "말씀")])
        open(os.path.join(ROOT, "verse", verse_slug(ref) + ".html"), "w", encoding="utf-8").write(html)
        slugs.append(verse_slug(ref))
    update_sitemap(slugs)
    print(f"구절 해설 페이지 {len(slugs)}개 생성")


if __name__ == "__main__":
    main()
