# -*- coding: utf-8 -*-
"""성경공부 가이드(/guide/) 생성. 실행: python3 build_guides.py
데이터: guide_data_*.py 의 A 리스트. 출력: guide/index.html, guide/<slug>/index.html, sitemap.xml 의 GUIDES 구간"""
import glob
import html as _html
import importlib
import json
import os
import re

import build_dictionary as bd
import build_verse as bv
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT

CSS = bv.CSS + """
.gd{max-width:var(--w-read,820px);margin:0 auto;padding:26px 20px 14px;text-align:left;color:#222}
.gd h1{font-size:28px;line-height:1.4;margin:10px 0 6px}.gd h2{font-size:21px;margin:34px 0 10px;color:#0b3d73;scroll-margin-top:70px}
.gd p,.gd li{font-size:16.5px;line-height:1.95;word-break:keep-all}.gd p{margin:0 0 13px}
.gd .lead{font-size:17.5px;color:#334}
.gd .toc{background:#f4f8ff;border:1px solid #cfe0f5;border-radius:14px;padding:14px 18px;margin:18px 0}
.gd .toc b{color:#0b3d73;font-size:15px}.gd .toc ol{margin:8px 0 0;padding-left:20px}.gd .toc li{font-size:15px;line-height:1.8}
.gd .toc a{color:#0b5cad;text-decoration:none}
.gd table{width:100%;border-collapse:collapse;margin:12px 0 16px;font-size:15px;display:block;overflow-x:auto}
.gd th,.gd td{border:1px solid #dfe6ef;padding:9px 11px;text-align:left;line-height:1.7;vertical-align:top;min-width:92px}
.gd th{background:#f1f5fb;white-space:nowrap}
.gd .note{background:#fff8ec;border:1px solid #f0d9a8;border-radius:12px;padding:12px 16px;margin:14px 0;font-size:15px}
.gd .rel{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 4px}
.gd .rel a{padding:8px 14px;border:1px solid #bcd3f0;border-radius:20px;background:#fff;color:#0b5cad;text-decoration:none;font-size:14.5px}
.gd .btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}
.gd .btnrow a{display:inline-block;padding:13px 20px;border-radius:12px;background:#0073e6;color:#fff;text-decoration:none;font-weight:700;font-size:15.5px}
.gd .btnrow a.alt{background:#fff;color:#0b5cad;border:1px solid #bcd3f0}
.gd .gcard{display:block;padding:14px 16px;border:1px solid #d6e4f7;border-radius:14px;background:#fff;text-decoration:none;color:#0b3d73;margin:8px 0}
.gd .gcard b{display:block;font-size:16.5px}.gd .gcard span{display:block;font-size:13.5px;color:#667;margin-top:3px;line-height:1.6}
.gd .gm{font-size:13px;color:#778;margin:0 0 4px}
"""


def load_articles():
    arts = []
    for f in sorted(glob.glob(os.path.join(ROOT, "guide_data_*.py"))):
        mod = importlib.import_module(os.path.basename(f)[:-3])
        arts.extend(mod.A)
    import guide_extra_1
    extra = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "guide_extra_*.py"))):
        extra.update(importlib.import_module(os.path.basename(f)[:-3]).E)
    for a in arts:
        a.update(extra.get(a["slug"], {}))
    slugs = [a["slug"] for a in arts]
    assert len(slugs) == len(set(slugs)), "slug 중복"
    return arts


_DICT = {}


def dict_title(slug):
    if slug not in _DICT:
        p = os.path.join(ROOT, "dictionary", slug + ".html")
        assert os.path.exists(p), f"사전 항목 없음: {slug}"
        s = open(p, encoding="utf-8").read()
        m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        t = _html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else slug
        _DICT[slug] = t.split(" - ")[0].split(":")[0].strip()
    return _DICT[slug]


def block(b):
    if isinstance(b, str):
        return f"<p>{esc(b)}</p>"
    kind = b[0]
    if kind in ("ul", "ol"):
        return f"<{kind}>" + "".join(f"<li>{esc(x)}</li>" for x in b[1]) + f"</{kind}>"
    if kind == "table":
        th = "".join(f"<th>{esc(c)}</th>" for c in b[1])
        tr = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in b[2])
        return f"<table><tr>{th}</tr>{tr}</table>"
    if kind == "note":
        return f'<div class="note">{esc(b[1])}</div>'
    raise ValueError(kind)


def plain_len(a):
    n = len(a["lead"]) + sum(len(q) + len(t) for q, t in a.get("myths", [])) + sum(len(x) for x in a.get("questions", [])) + sum(len(x) for x in a.get("tips", [])) + sum(len(q) + len(t) for q, t in a["faq"])
    for h, bl in a["sections"]:
        for b in bl:
            if isinstance(b, str):
                n += len(b)
            elif b[0] in ("ul", "ol"):
                n += sum(len(x) for x in b[1])
            elif b[0] == "table":
                n += sum(len(c) for r in b[2] for c in r)
            elif b[0] == "note":
                n += len(b[1])
    return n


def page(a, arts):
    path = f"/guide/{a['slug']}/"
    url = SITE + path
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in a["faq"]]}
    art_ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
              "inLanguage": "ko", "mainEntityOfPage": url, "datePublished": a.get("date", "2026-10-19"), "dateModified": bd.TODAY,
              "author": {"@type": "Organization", "name": "십자가로세로", "url": SITE},
              "publisher": {"@type": "Organization", "name": "십자가로세로", "url": SITE}}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "성경공부 가이드", "item": SITE + "/guide/"},
        {"@type": "ListItem", "position": 3, "name": a["title"].split(" - ")[0], "item": url}]}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (art_ld, faq_ld, crumb_ld))
    title = a["title"] + " | 십자가로세로"
    h = head(title, a["desc"], path, ld).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    toc = "".join(f'<li><a href="#s{i}">{esc(re.sub(r"^[0-9]+\\. ", "", s[0]))}</a></li>' for i, s in enumerate(a["sections"], 1))
    secs = "".join(f'<h2 id="s{i}">{esc(s[0])}</h2>' + "".join(block(b) for b in s[1]) for i, s in enumerate(a["sections"], 1))
    rel = "".join(f'<a href="/dictionary/{s}.html">{esc(dict_title(s))}</a>' for s in a["related"])
    same = [x for x in arts if x["slug"] != a["slug"] and x["cat"] == a["cat"]][:3]
    more = [x for x in arts if x["slug"] != a["slug"] and x not in same][:3 - len(same) + 2]
    nxt = "".join(f'<a class="gcard" href="/guide/{x["slug"]}/"><b>{esc(x["title"].split(" - ")[0])}</b><span>{esc(x["desc"][:70])}…</span></a>' for x in (same + more)[:4])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(t)}</p></details>" for q, t in a["faq"])
    ex = ""
    if a.get("myths"):
        ex += "<h2>자주 하는 오해</h2><ul>" + "".join(f"<li><b>{esc(q)}</b> {esc(t)}</li>" for q, t in a["myths"]) + "</ul>"
    if a.get("questions"):
        ex += "<h2>함께 나눌 질문</h2><p>혼자 묵상하거나 소그룹·주일학교에서 나눌 때 사용해 보세요.</p><ol>" + "".join(f"<li>{esc(x)}</li>" for x in a["questions"]) + "</ol>"
    if a.get("tips"):
        ex += "<h2>교사·소그룹 리더를 위한 활용 팁</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in a["tips"]) + "</ul>"
    extras = ex
    body = f"""<main class="gd">
<div class="crumb"><a href="/">홈</a> › <a href="/guide/">성경공부 가이드</a> › {esc(a['title'].split(' - ')[0])}</div>
<span class="badge">{esc(a['cat'])}</span>
<h1>{esc(a['title'])}</h1>
<p class="gm">십자가로세로 편집 · 읽는 시간 약 {max(3, round(plain_len(a) / 500))}분</p>
<p class="lead">{esc(a['lead'])}</p>
<div class="toc"><b>이 글의 차례</b><ol>{toc}</ol></div>
{secs}
{extras}
<h2>더 알아보기</h2>
<p>이 글에 나오는 인물, 장소, 사건을 성경사전에서 더 찾아볼 수 있습니다.</p>
<div class="rel">{rel}</div>
<div class="btnrow"><a href="/list.html" data-ga="guide_to_puzzle">🧩 낱말 퍼즐로 복습하기</a><a class="alt" href="/verse/" data-ga="guide_to_verse">📖 말씀 카드 만들기</a></div>
<h2>자주 묻는 질문</h2>
<div class="faq">{faq}</div>
<h2>함께 읽으면 좋은 글</h2>
{nxt}
<p class="vnote" style="margin-top:22px;font-size:13px;color:#667">성경 본문 인용은 개역한글판을 기준으로 하며, 연대와 해석은 학자와 교단에 따라 다를 수 있어 일반적으로 알려진 내용 중심으로 정리했습니다. 설명에 오류가 있으면 <a href="/feedback/">의견 보내기</a>로 알려 주세요.</p>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "</body>\n</html>\n"])


def hub(arts):
    path = "/guide/"
    cats = []
    for a in arts:
        if a["cat"] not in cats:
            cats.append(a["cat"])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "성경공부 가이드", "url": SITE + path, "inLanguage": "ko",
         "hasPart": [{"@type": "Article", "headline": a["title"], "url": f"{SITE}/guide/{a['slug']}/"} for a in arts]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "성경공부 가이드", "item": SITE + path}]}))
    title = "성경공부 가이드 - 성경 읽는 법·구약 흐름·사복음서·십계명·주기도문 | 십자가로세로"
    desc = f"성경을 처음 읽는 분부터 교사·소그룹 리더까지 활용할 수 있는 성경공부 가이드 {len(arts)}편. 성경 개관, 시대별 흐름, 본문 해설, 묵상과 교육 방법을 쉬운 말로 정리했습니다."
    h = head(title, desc, path, ld).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    groups = "".join(
        f"<h2>{esc(c)}</h2>" + "".join(
            f'<a class="gcard" href="/guide/{a["slug"]}/"><b>{esc(a["title"].split(" - ")[0])}</b><span>{esc(a["desc"])}</span></a>'
            for a in arts if a["cat"] == c) for c in cats)
    body = f"""<main class="gd">
<div class="crumb"><a href="/">홈</a> › 성경공부 가이드</div>
<h1>성경공부 가이드</h1>
<p class="lead">성경을 처음 읽는 분, 주일학교 교사, 소그룹 리더가 바로 쓸 수 있도록 성경 전체의 구조와 흐름, 주요 본문, 읽고 가르치는 방법을 쉬운 말로 정리한 글 모음입니다. 모든 글은 성경사전, 지도, 퍼즐과 연결되어 있어 읽고 나서 바로 확인하고 복습할 수 있습니다.</p>
{groups}
<div class="btnrow"><a href="/dictionary/" data-ga="guidehub_to_dict">📖 성경사전 보기</a><a class="alt" href="/list.html" data-ga="guidehub_to_puzzle">🧩 퍼즐 풀기</a></div>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "</body>\n</html>\n"])


def update_sitemap(arts):
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- GUIDES-START -->.*?<!-- GUIDES-END -->", "", s, flags=re.S)
    urls = ["/guide/"] + [f"/guide/{a['slug']}/" for a in arts]
    block_ = "\n  <!-- GUIDES-START -->\n" + "\n".join(
        f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        for u in urls) + "\n  <!-- GUIDES-END -->\n"
    s = s.replace("</urlset>", block_ + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    arts = load_articles()
    d = os.path.join(ROOT, "guide")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(hub(arts))
    short = []
    for a in arts:
        os.makedirs(os.path.join(d, a["slug"]), exist_ok=True)
        open(os.path.join(d, a["slug"], "index.html"), "w", encoding="utf-8").write(page(a, arts))
        if plain_len(a) < 2000:
            short.append((a["slug"], plain_len(a)))
    update_sitemap(arts)
    print(f"성경공부 가이드 {len(arts)}편 생성")
    for s, n in short:
        print("  2,000자 미만:", s, n)


if __name__ == "__main__":
    main()
