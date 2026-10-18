# -*- coding: utf-8 -*-
"""자동 발행 퍼즐 게시글 중 '가치가 낮은' 글을 검색 색인에서 제외한다.
기준: 퍼즐의 주제 전용 힌트(allWords)가 5개 이하라, 게시글 힌트 대부분이 공통 풀 힌트인 글.
- post_quality_low.json 의 ids 에서 id 를 빼면 해당 글은 다시 색인 대상이 된다.
- 실행: python3 post_quality.py  (기존 게시글 noindex 정리 + posts.xml 재생성)"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
META = '<meta name="robots" content="noindex,follow">'
_LOW = None


def low_ids():
    global _LOW
    if _LOW is None:
        try:
            _LOW = set(json.load(open(os.path.join(ROOT, "post_quality_low.json"), encoding="utf-8"))["ids"])
        except Exception:
            _LOW = set()
    return _LOW


def is_low(pid):
    return pid in low_ids()


def ensure_robots(path, pid):
    """게시글 HTML 에 noindex 메타를 넣거나(낮은 가치) 빼 준다. 바뀌면 True."""
    s = open(path, encoding="utf-8").read()
    has = META in s
    if is_low(pid) and not has:
        s = s.replace('<link rel="canonical"', META + '\n<link rel="canonical"', 1)
    elif not is_low(pid) and has:
        s = s.replace(META + "\n", "", 1)
    else:
        return False
    open(path, "w", encoding="utf-8").write(s)
    return True


def main():
    man = json.load(open(os.path.join(ROOT, "published_manifest.json"), encoding="utf-8"))
    changed = sum(ensure_robots(os.path.join(ROOT, "posts", p["slug"] + ".html"), p["id"]) for p in man
                  if os.path.exists(os.path.join(ROOT, "posts", p["slug"] + ".html")))
    keep = [p for p in man if not is_low(p["id"])]
    # posts.xml: 색인 대상만
    entries = sorted(keep, key=lambda x: (x["date"], x["slug"]), reverse=True)
    with open(os.path.join(ROOT, "posts.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for e in entries:
            f.write(f'  <url>\n    <loc>https://crossero.com/posts/{e["slug"]}.html</loc>\n    <lastmod>{e["date"]}</lastmod>\n'
                    '    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>\n')
        f.write("</urlset>\n")
    print(f"게시글 {len(man)}개 중 색인 유지 {len(keep)}개, noindex {len(man) - len(keep)}개 (이번에 수정 {changed}개)")


if __name__ == "__main__":
    main()
