#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기존 posts/*.html에 "🧩 이 퍼즐에서 배우는 내용" 섹션을 일괄 삽입.
- <div class="answer-section"> 바로 앞에 삽입.
- 이미 삽입된 파일(puzzle-learning 존재)은 건너뜀(재실행 안전).
- 📖 책 소개, 📚 주요 사건 섹션은 절대 건드리지 않음.
"""
import os
import re
import glob
from html import escape

POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")
H1_RE = re.compile(r"<h1>(.*?)</h1>")
ANCHOR = '<div class="answer-section">'


def build_block(title):
    return f"""<section class="puzzle-learning">
<h3>🧩 이 퍼즐에서 배우는 내용</h3>
<p>이 퍼즐은 {escape(title)}의 핵심 단어와 개념을 자연스럽게 복습할 수 있도록 구성되었습니다. 주일학교 수업이나 개인 성경공부에서 학습 내용을 점검하는 용도로 바로 활용할 수 있습니다.</p>
</section>
"""


def main():
    updated, skipped = 0, 0
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.html"))):
        if os.path.basename(path) == "index.html":
            continue
        html = open(path, encoding="utf-8").read()

        if "puzzle-learning" in html:
            skipped += 1
            continue

        if ANCHOR not in html:
            print(f"  (앵커 없음) {os.path.basename(path)}")
            continue

        m = H1_RE.search(html)
        title = m.group(1) if m else "이 퍼즐"

        block = build_block(title)
        new_html = html.replace(ANCHOR, block + ANCHOR, 1)
        open(path, "w", encoding="utf-8").write(new_html)
        updated += 1

    print(f"\n완료: 업데이트 {updated}, 건너뜀(이미 적용) {skipped}")


if __name__ == "__main__":
    main()
