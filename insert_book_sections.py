#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기존 posts/*.html에 "책 소개 + 주요 사건" 섹션을 일괄 삽입.
- 퍼즐 이미지, 힌트, 정답 링크 등 기존 내용은 그대로 두고, <div class="intro"> 앞에 섹션만 추가.
- 이미 삽입된 파일(book-info-section 존재)은 건너뜀(재실행 안전).
"""
import os
import re
import glob
from html import escape
from bible_book_info import BOOK_INFO
from topic_info import TOPIC_INFO

POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")

H1_RE = re.compile(r"<h1>(.*?)</h1>")
INTRO_RE = re.compile(r'<div class="intro">')


def build_block(book, title):
    info = BOOK_INFO.get(book) or TOPIC_INFO.get(title)
    if not info:
        return None
    events_html = " · ".join(escape(e) for e in info["events"])
    if book in BOOK_INFO:
        title1, title2 = f"📖 {escape(book)}란?", f"📚 {escape(book)}의 주요 사건·주제"
    else:
        title1, title2 = "📖 이 글은 어떤 내용인가요?", "📚 핵심 포인트"
    return f"""<div class="edu-section book-info-section">
<h3>{title1}</h3>
<p>{escape(info["desc"])}</p>
</div>
<div class="edu-section">
<h3>{title2}</h3>
<p>{events_html}</p>
</div>
"""


def main():
    updated, skipped, no_book = 0, 0, 0
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.html"))):
        if os.path.basename(path) == "index.html":
            continue
        html = open(path, encoding="utf-8").read()

        if "book-info-section" in html:
            skipped += 1
            continue

        m = H1_RE.search(html)
        if not m:
            no_book += 1
            continue
        title = m.group(1)
        book = title.split(":")[0].strip() if ":" in title else title.split()[0]

        block = build_block(book, title)
        if block is None:
            no_book += 1
            print(f"  (정보 없음: {title}) {os.path.basename(path)}")
            continue

        new_html, n = INTRO_RE.subn(block + '<div class="intro">', html, count=1)
        if n == 0:
            print(f"  (intro 위치 못찾음) {os.path.basename(path)}")
            continue

        open(path, "w", encoding="utf-8").write(new_html)
        updated += 1

    print(f"\n완료: 업데이트 {updated}, 건너뜀(이미 적용) {skipped}, 책 정보 없음 {no_book}")


if __name__ == "__main__":
    main()
