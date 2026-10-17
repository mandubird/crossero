# -*- coding: utf-8 -*-
"""사이트 정적 점검: 깨진 내부 링크·이미지, 중복 제목, 메타 설명, JSON-LD, 사이트맵, 용량.
사용: python3 site_audit.py"""
import collections
import glob
import json
import os
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = ("node_modules", "backup", "youtube_shorts_generator", ".git", "naver", "google", "blog_drafts")


def pages():
    for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith(SKIP) or os.path.basename(rel).startswith(("naver", "google")):
            continue
        yield rel, f


def resolve(base_rel, href):
    u = urlparse(href)
    if u.scheme in ("http", "https", "mailto", "tel", "javascript", "data") or href.startswith(("#", "//")) or "'+" in href or "'" in href:
        return "skip"
    p = unquote(u.path)
    if not p:
        return "skip"
    if p.startswith("/"):
        tgt = os.path.join(ROOT, p.lstrip("/"))
    else:
        tgt = os.path.normpath(os.path.join(ROOT, os.path.dirname(base_rel), p))
    if os.path.isdir(tgt):
        tgt = os.path.join(tgt, "index.html")
    return tgt if os.path.exists(tgt) else None


def main():
    bad_links, bad_img, titles, nodesc, longdesc, badld, dupid = [], [], collections.defaultdict(list), [], [], [], []
    count = 0
    heavy = []
    for rel, f in pages():
        count += 1
        s = open(f, encoding="utf-8", errors="ignore").read()
        heavy.append((len(s.encode()), rel))
        for m in re.finditer(r'<a\s[^>]*href="([^"]+)"', s):
            if resolve(rel, m.group(1)) is None:
                bad_links.append((rel, m.group(1)))
        for m in re.finditer(r'<(?:img|source)\s[^>]*src="([^"]+)"', s):
            if resolve(rel, m.group(1)) is None:
                bad_img.append((rel, m.group(1)))
        t = re.search(r"<title>([^<]*)</title>", s)
        if t:
            titles[t.group(1).strip()].append(rel)
        d = re.search(r'<meta name="description" content="([^"]*)"', s)
        if not d:
            nodesc.append(rel)
        elif len(d.group(1)) > 170:
            longdesc.append((rel, len(d.group(1))))
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(m.group(1))
            except Exception as ex:
                badld.append((rel, str(ex)[:60]))
        ids = re.findall(r'\sid="([^"]+)"', s)
        c = [k for k, v in collections.Counter(ids).items() if v > 1]
        if c:
            dupid.append((rel, c[:3]))
    # 사이트맵 대조
    miss_sitemap = []
    for sm in ("sitemap.xml", "posts.xml"):
        p = os.path.join(ROOT, sm)
        if os.path.exists(p):
            for loc in re.findall(r"<loc>([^<]+)</loc>", open(p, encoding="utf-8").read()):
                path = urlparse(loc).path
                tgt = os.path.join(ROOT, unquote(path).lstrip("/"))
                if os.path.isdir(tgt) or path.endswith("/") or path == "":
                    tgt = os.path.join(tgt, "index.html")
                if not os.path.exists(tgt):
                    miss_sitemap.append((sm, loc))
    # 용량
    def du(d):
        tot = 0
        for r, _, fs in os.walk(os.path.join(ROOT, d)):
            tot += sum(os.path.getsize(os.path.join(r, x)) for x in fs)
        return tot / 1e6
    imgs = sorted(((os.path.getsize(f), os.path.relpath(f, ROOT)) for f in glob.glob(os.path.join(ROOT, "images/**/*.*"), recursive=True)), reverse=True)
    print(f"페이지 {count}개")
    print(f"깨진 링크 {len(bad_links)}, 깨진 이미지 {len(bad_img)}, 사이트맵 누락 {len(miss_sitemap)}")
    print(f"중복 제목 {sum(1 for v in titles.values() if len(v) > 1)}종, 설명 없음 {len(nodesc)}, 긴 설명 {len(longdesc)}, 잘못된 JSON-LD {len(badld)}, 중복 id {len(dupid)}")
    print("폴더 용량(MB):", {d: round(du(d), 1) for d in ("images", "posts", "dictionary", "verse", "data")})
    print("큰 이미지:", [(round(s / 1e3), p) for s, p in imgs[:5]])
    print("큰 HTML:", [(round(s / 1e3), p) for s, p in sorted(heavy, reverse=True)[:5]])
    for name, lst in (("깨진 링크", bad_links), ("깨진 이미지", bad_img), ("사이트맵 누락", miss_sitemap), ("설명 없음", nodesc), ("긴 설명", longdesc), ("JSON-LD 오류", badld), ("중복 id", dupid)):
        if lst:
            print(f"\n[{name}]")
            for x in lst[:15]:
                print(" ", x)
    dups = [(k, v) for k, v in titles.items() if len(v) > 1]
    if dups:
        print("\n[중복 제목]")
        for k, v in dups[:10]:
            print(" ", k[:50], len(v), v[:3])


if __name__ == "__main__":
    main()
