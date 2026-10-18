# -*- coding: utf-8 -*-
"""얇은 페이지·빈 페이지·중복 점검. 사용: python3 thin_audit.py"""
import collections, glob, os, re, statistics as st, sys
from urllib.parse import unquote
ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = ("node_modules", "backup", "youtube_shorts_generator", "blog_drafts", ".git")
def main_text(s):
    m = re.search(r"<main.*?</main>", s, re.S)
    body = m.group(0) if m else re.sub(r"<head.*?</head>", "", s, flags=re.S)
    body = re.sub(r"<script.*?</script>|<style.*?</style>|<nav.*?</nav>", "", body, flags=re.S)
    return re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", body))
sitemap = set()
for sm in ("sitemap.xml", "posts.xml"):
    p = os.path.join(ROOT, sm)
    if os.path.exists(p):
        for loc in re.findall(r"<loc>([^<]+)</loc>", open(p, encoding="utf-8").read()):
            sitemap.add(unquote(re.sub(r"^https://crossero\.com", "", loc)))
rows = []
for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(SKIP) or rel.startswith(("naver", "google")):
        continue
    s = open(f, encoding="utf-8", errors="ignore").read()
    url = "/" + rel
    url_dir = url[:-10] if url.endswith("/index.html") else url
    in_sm = any(u in sitemap for u in (url, url_dir, url_dir + "/")) or url == "/index.html" and "/" in sitemap
    noindex = bool(re.search(r'<meta[^>]+name="robots"[^>]+noindex', s))
    title = (re.search(r"<title>([^<]*)", s) or [0, ""])[1].strip()
    canon = (re.search(r'rel="canonical" href="([^"]+)"', s) or [0, ""])[1]
    rows.append({"rel": rel, "n": len(main_text(s)), "in_sm": in_sm, "noindex": noindex, "title": title, "canon": canon})
def grp(r):
    p = r["rel"]
    if p.startswith("posts/"): return "퍼즐 게시글"
    if p.startswith("dictionary/verses/"): return "구절 인덱스"
    if p.startswith("dictionary/timeline/"): return "연대표"
    if p.startswith("dictionary/map/"): return "지도"
    if p.startswith("dictionary/") and p.count("/") == 1 and p != "dictionary/index.html": return "사전 항목"
    if p.startswith("dictionary/"): return "사전 목록·기타"
    if p.startswith("verse/"): return "구절 해설·말씀 뽑기"
    if p.startswith("christmas/"): return "성탄"
    if p.startswith("teachers/"): return "교사 허브"
    if p.startswith("bible-quiz/"): return "bible-quiz(옛)"
    return "일반 페이지"
g = collections.defaultdict(list)
for r in rows: g[grp(r)].append(r)
print(f"전체 {len(rows)}페이지")
print(f"{'구분':14s}{'수':>5}{'중앙값':>8}{'<800자':>8}{'<500자':>8}")
for k, v in sorted(g.items(), key=lambda x: -len(x[1])):
    ns = [x["n"] for x in v]
    print(f"{k:14s}{len(v):5d}{int(st.median(ns)):8d}{sum(1 for n in ns if n<800):8d}{sum(1 for n in ns if n<500):8d}")
print("\n[500자 미만 페이지 — 사이트맵 포함 여부]")
for r in sorted(rows, key=lambda x: x["n"]):
    if r["n"] < 500:
        print(f"  {r['n']:4d}자  sm={'Y' if r['in_sm'] else 'N'} noindex={'Y' if r['noindex'] else 'N'}  {r['rel']}")
t = collections.defaultdict(list)
for r in rows: t[r["title"]].append(r["rel"])
print("\n[같은 제목 페이지]", [(k[:30], len(v)) for k, v in t.items() if len(v) > 1 and k][:10])
