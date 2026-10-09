# -*- coding: utf-8 -*-
"""기존 게시글에 성경사전 링크 블록을 삽입(이미 있으면 교체). 실행: python3 add_dictionary_links.py"""
import glob
import os
import re

from bible_book_info import BOOK_INFO
from topic_info import TOPIC_INFO
from dict_links import dict_links_html, MARK_START, MARK_END

ROOT = os.path.dirname(os.path.abspath(__file__))
H1 = re.compile(r"<h1>(.*?)</h1>", re.S)
OLD = re.compile(re.escape(MARK_START) + r".*?" + re.escape(MARK_END) + r"\n?", re.S)
ANCHOR = '<section class="puzzle-learning">'


def main():
    done = skipped = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "posts", "*.html"))):
        if f.endswith("index.html"):
            continue
        s = open(f, encoding="utf-8").read()
        m = H1.search(s)
        if not m or ANCHOR not in s:
            skipped += 1
            continue
        title = re.sub(r"<[^>]+>", "", m.group(1)).replace("&amp;", "&").strip()
        book = title.split(":")[0].strip() if ":" in title else title.split()[0]
        info = BOOK_INFO.get(book) or TOPIC_INFO.get(title)
        events = " ".join(info["events"]) if info else ""
        block = dict_links_html(title, book, events)
        s = OLD.sub("", s)
        s = s.replace(ANCHOR, block + ANCHOR, 1)
        open(f, "w", encoding="utf-8").write(s)
        done += 1
    print(f"삽입/갱신 {done}개, 건너뜀 {skipped}개")


if __name__ == "__main__":
    main()
