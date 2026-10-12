# -*- coding: utf-8 -*-
"""말씀 뽑기·구절 해설 페이지가 공유하는 도구."""
import csv
import os
import re

from bible_book_info import BOOK_INFO

ROOT = os.path.dirname(os.path.abspath(__file__))
KO_BOOKS = list(BOOK_INFO)

# dictionary_books의 slug_en(book-xxx)과 같은 영문 슬러그를 만들기 위해 책 항목에서 읽는다
_ENG = {}


def _load_eng():
    if _ENG:
        return
    from dictionary_data_books_ot import OT
    from dictionary_data_books_nt import NT
    for b in OT + NT:
        _ENG[b["name"]] = b["slug"][len("book-"):]


def eng_slug(book_name):
    _load_eng()
    return _ENG[book_name]


def parse_ref(ref):
    m = re.match(r"^(.+?)\s+(\d+):(\d+)$", ref)
    return m.group(1), int(m.group(2)), int(m.group(3))


def verse_slug(ref):
    name, c, v = parse_ref(ref)
    return f"{eng_slug(name)}-{c}-{v}"


def verse_url(ref):
    return f"/verse/{verse_slug(ref)}.html"


def load_text():
    rows = csv.reader(open(os.path.join(ROOT, "BIBLE.csv"), encoding="utf-8"))
    next(rows)
    verses = {}
    for b, c, v, t in rows:
        try:
            bi, ci, vi = int(float(b)), int(float(c)), int(float(v))
        except ValueError:
            continue
        t = t.strip()
        if bi >= 1 and len(t) > 3 and not re.match(r"^\(.*절에.*\)$", t):
            verses[(bi, ci, vi)] = t
    return verses
